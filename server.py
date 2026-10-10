"""JEE Mock CBT: small Flask server that serves the app, keeps every attempt in SQLite, and has
student accounts (the owner creates them; there is no public sign-up).

Run locally:   python server.py          (then open http://localhost:8000)
PythonAnywhere: see DEPLOY.md.
Accounts:      python tools/manage_users.py --help   (first admin, students, password resets)

The app works without this server too (opened as a file or as a claude.ai Artifact);
it then keeps results in the browser only.

Every page, question image and /api/* call needs a signed-in user, except the login page and /api/export.
A student only ever sees their own attempts; an admin sees everyone (?user=<id> on the read endpoints).

Endpoints
  POST /api/login             {username, password} -> starts a session
  POST /api/logout
  GET  /api/me                who is signed in
  POST /api/password          {current, new} change your own password
  POST /api/attempts          save (or update) one finished exam of the signed-in user
  GET  /api/attempts          list your saved attempts (admin: ?user=<id>)
  GET  /api/progress          your attempts' responses and review outcomes (admin: ?user=<id>)
  GET  /api/flags             your concept flags written by Claude's analysis (admin: ?user=<id>)
  GET  /api/admin/users       admin: every user with test counts
  POST /api/admin/users       admin: {username, name} -> new student with a one-time password
  POST /api/admin/users/<id>/reset    admin: new one-time password
  POST /api/admin/users/<id>/active   admin: {active: true|false}
  GET  /api/export            download a copy of the database; needs header X-Export-Key
"""
import json
import os
import re
import secrets
import sqlite3
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Flask, abort, g, jsonify, redirect, request, send_file, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get('JEE_DB_PATH', ROOT / 'data' / 'akil.db'))
STATIC_FILES = {'index.html', 'questions.js', 'pyq_bank.js'}
PUBLIC_FILES = {'login.html'}          # served without a session

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  username      TEXT NOT NULL UNIQUE COLLATE NOCASE,
  name          TEXT NOT NULL,             -- shown on the exam screen and report
  pw_hash       TEXT NOT NULL,             -- werkzeug hash, never the password itself
  role          TEXT NOT NULL DEFAULT 'student',   -- student | admin
  must_change   INTEGER NOT NULL DEFAULT 1,        -- 1 = one-time password: choose a new one at the next login
  active        INTEGER NOT NULL DEFAULT 1,
  created_at    TEXT,
  last_login    TEXT
);
CREATE TABLE IF NOT EXISTS attempts (
  id            TEXT PRIMARY KEY,          -- the app's exam id
  student       TEXT NOT NULL,
  test_name     TEXT,
  started_at    TEXT,                      -- ISO 8601, UTC
  submitted_at  TEXT,
  duration_min  REAL,
  time_used_s   REAL,
  time_up       INTEGER,
  bank_name     TEXT,
  years         TEXT,                      -- JSON list
  marking       TEXT,                      -- JSON {mcqC, mcqW, numC, numW}
  score         REAL,
  max_score     REAL,
  n_questions   INTEGER,
  n_correct     INTEGER,
  n_wrong       INTEGER,
  n_skipped     INTEGER,
  raw_json      TEXT,                      -- the full exam object as the app sent it
  saved_at      TEXT,
  updated_at    TEXT
  -- user_id (users.id) is added by init_db, so older databases get it too
);
CREATE TABLE IF NOT EXISTS responses (
  attempt_id      TEXT NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
  q_index         INTEGER NOT NULL,        -- 0-based position in the paper
  question_id     TEXT,                    -- NTA question ID (join with the bank for current tags)
  subject         TEXT,
  chapter         TEXT,                    -- chapter tag at the time of the attempt
  subtopic        TEXT,
  source          TEXT,
  year            INTEGER,
  qtype           TEXT,                    -- MCQ | NUM
  given           TEXT,                    -- final answer: option index (0-based) for MCQ, value for NUM; NULL = skipped
  first_answer    TEXT,                    -- first answer he saved, before any change
  correct_answer  TEXT,                    -- JSON: answer or accept list
  attempted       INTEGER,
  correct         INTEGER,
  marks           REAL,
  time_ms         INTEGER,
  visits          INTEGER,
  answer_changes  INTEGER,
  marked_review   INTEGER,
  status          TEXT,                    -- nv | na | ans | mr | amr (palette state at submit)
  reason          TEXT,                    -- Akil's own label for a wrong answer: concept | approach | calc | recall | misread | rushed
  PRIMARY KEY (attempt_id, q_index)
);
CREATE INDEX IF NOT EXISTS idx_resp_q ON responses(question_id);
CREATE INDEX IF NOT EXISTS idx_resp_chapter ON responses(subject, chapter);

-- What Akil did in the answer review with each wrong or skipped question (hint ladder).
-- outcome: solved_no_hint | solved_hint1 | solved_hint2 | saw_solution | skipped | open (started, no result yet)
CREATE TABLE IF NOT EXISTS practice (
  attempt_id      TEXT NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
  q_index         INTEGER NOT NULL,
  question_id     TEXT,
  subject         TEXT,
  chapter         TEXT,
  in_test         TEXT,                    -- wrong | skipped (how it went in the timed test)
  outcome         TEXT,
  hints_used      INTEGER,                 -- 0, 1 or 2 hints opened before the outcome
  tries           INTEGER,                 -- answers tried in the review
  wrong_tries     INTEGER,
  practice_ms     INTEGER,                 -- time from opening the question in review to the outcome
  events          TEXT,                    -- JSON list of {t: try|hint1|hint2|solution|skip|reopen, v?, ok?, at (ms epoch)}
  updated_at      TEXT,
  PRIMARY KEY (attempt_id, q_index)
);
CREATE INDEX IF NOT EXISTS idx_prac_chapter ON practice(subject, chapter);

-- Written by Claude during analysis (jee-analysis skill), shown read-only in the app. user_id is added by init_db.
CREATE TABLE IF NOT EXISTS flags (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  subject       TEXT NOT NULL,
  chapter       TEXT NOT NULL,
  concept       TEXT NOT NULL,             -- the specific idea, e.g. "capacitor with partial dielectric"
  kind          TEXT NOT NULL,             -- concept_gap | formula_misapplied | calculation | units | misread | ncert_fact | speed
  severity      TEXT NOT NULL,             -- high | medium | low
  status        TEXT NOT NULL DEFAULT 'open',  -- open | improving | resolved
  evidence      TEXT,                      -- JSON list of {attempt_id, q_index, question_id, note}
  action        TEXT,                      -- what to study / practise
  created_at    TEXT,
  updated_at    TEXT
);
CREATE TABLE IF NOT EXISTS analyses (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at    TEXT,
  attempts      TEXT,                      -- JSON list of attempt ids covered
  summary       TEXT                       -- Markdown report
);
"""

app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=os.environ.get('JEE_SECURE_COOKIE') == '1',   # 1 on PythonAnywhere (HTTPS only)
    PERMANENT_SESSION_LIFETIME=timedelta(days=30),
)


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def ms_iso(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat(timespec='seconds') if ms else None


def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys = ON')
    return con


def init_db():
    with db() as con:
        con.executescript(SCHEMA)
        for table in ('attempts', 'flags', 'analyses'):
            if 'user_id' not in [r[1] for r in con.execute(f'PRAGMA table_info({table})')]:
                con.execute(f'ALTER TABLE {table} ADD COLUMN user_id INTEGER REFERENCES users(id)')
        con.execute('CREATE INDEX IF NOT EXISTS idx_att_user ON attempts(user_id)')
        # attempts saved by an older server kept the hint-ladder log only in raw_json: rebuild those practice rows
        todo = [r[0] for r in con.execute(
            "SELECT raw_json FROM attempts a WHERE raw_json LIKE '%\"practice\"%' "
            "AND NOT EXISTS (SELECT 1 FROM practice p WHERE p.attempt_id = a.id)")]
    for raw in todo:
        try:
            save_attempt(json.loads(raw))
        except (KeyError, TypeError, ValueError):
            pass


def read_secret(name):
    """A value from the environment (PythonAnywhere) or from .secrets (KEY=value lines) next to this file."""
    if os.environ.get(name):
        return os.environ[name].strip()
    f = ROOT / '.secrets'
    if f.exists():
        for line in f.read_text(encoding='utf-8').splitlines():
            if line.strip().startswith(name + '='):
                return line.split('=', 1)[1].strip()
    return None


def export_key():
    return read_secret('JEE_EXPORT_KEY')


def session_secret():
    """Signs the login cookie. Made once and kept in .secrets (gitignored), so logins survive restarts."""
    key = read_secret('JEE_SECRET_KEY')
    if not key:
        key = secrets.token_hex(32)
        with open(ROOT / '.secrets', 'a', encoding='utf-8') as f:
            f.write(f'\nJEE_SECRET_KEY={key}\n')
    return key


def is_correct(q, given):
    if given is None or given == '':
        return False
    try:
        if q.get('type') == 'MCQ':
            k = int(given)
            return k in q['accept'] if isinstance(q.get('accept'), list) else k == q.get('answer')
        v = float(given)
        if isinstance(q.get('accept'), list):
            return any(abs(v - float(a)) < 1e-9 for a in q['accept'])
        a = q.get('answer')
        if isinstance(a, list):
            return min(a) - 1e-9 <= v <= max(a) + 1e-9
        return abs(v - float(a)) < 1e-9
    except (TypeError, ValueError, KeyError):
        return False


def practice_outcome(events):
    """The result of the hint ladder, recomputed from the event log (the last result counts if he reopened it)."""
    out, hints = 'open', 0
    for e in events:
        t = e.get('t')
        if t == 'reopen':
            out = 'open'
        elif t in ('hint1', 'hint2'):
            hints = max(hints, int(t[-1]))
        elif t == 'try' and e.get('ok') and out == 'open':
            out = ('solved_no_hint', 'solved_hint1', 'solved_hint2')[hints]
        elif t == 'solution' and out == 'open':
            out = 'saw_solution'
        elif t == 'skip' and out == 'open':
            out = 'skipped'
    return out


def save_attempt(ex, user_id=None, student=None):
    """Recompute marks on the server from the exam object so the database never depends on the browser's arithmetic.
    user_id None keeps the attempt's current owner (used when rebuilding rows on startup)."""
    cfg, qs, resp = ex['cfg'], ex['qs'], ex['resp']
    if len(qs) != len(resp):
        raise ValueError('qs and resp differ in length')
    reasons = ex.get('reasons') or {}
    practice = ex.get('practice') or {}
    rows, prows, score, mx, nc, nw, ns = [], [], 0.0, 0.0, 0, 0, 0
    for i, (q, r) in enumerate(zip(qs, resp)):
        given = r.get('v')
        att = given is not None and given != ''
        ok = is_correct(q, given) if att else False
        pc, pw = (cfg['mcqC'], cfg['mcqW']) if q.get('type') == 'MCQ' else (cfg['numC'], cfg['numW'])
        marks = 0 if not att else pc if ok else -pw
        score += marks
        mx += pc
        nc += ok
        nw += att and not ok
        ns += not att
        visited, marked = bool(r.get('visited')), bool(r.get('marked'))
        st = 'nv' if not visited else ('amr' if att else 'mr') if marked else ('ans' if att else 'na')
        correct = q['accept'] if isinstance(q.get('accept'), list) else q.get('answer')
        first = r.get('first')
        rows.append((
            ex['id'], i, str(q.get('id', '')), q.get('subject'), q.get('chapter'), q.get('subtopic'),
            q.get('source'), q.get('year'), q.get('type'),
            None if not att else str(given), None if first is None else str(first), json.dumps(correct),
            int(att), int(ok), marks, int(r.get('t') or 0), int(r.get('visits') or (1 if visited else 0)),
            int(r.get('changes') or 0), int(marked), st, reasons.get(str(i))
        ))
        p = practice.get(str(i))
        if p and p.get('events'):
            ev = p['events']
            tries = [e for e in ev if e.get('t') == 'try']
            prows.append((ex['id'], i, str(q.get('id', '')), q.get('subject'), q.get('chapter'),
                          'skipped' if not att else 'wrong' if not ok else 'correct', practice_outcome(ev),
                          max([int(e['t'][-1]) for e in ev if e.get('t') in ('hint1', 'hint2')] or [0]), len(tries), sum(1 for e in tries if not e.get('ok')),
                          int(p.get('ms') or 0), json.dumps(ev), now_iso()))
    started, submitted = ex.get('startedAt'), ex.get('submittedAt')
    t = now_iso()
    with db() as con:
        existing = con.execute('SELECT saved_at, user_id, student FROM attempts WHERE id = ?', (ex['id'],)).fetchone()
        if user_id is None and existing:
            user_id, student = existing['user_id'], existing['student']
        con.execute('DELETE FROM responses WHERE attempt_id = ?', (ex['id'],))
        con.execute('DELETE FROM practice WHERE attempt_id = ?', (ex['id'],))
        con.execute('DELETE FROM attempts WHERE id = ?', (ex['id'],))
        con.execute('INSERT INTO attempts (id, student, test_name, started_at, submitted_at, duration_min, time_used_s, time_up, '
                    'bank_name, years, marking, score, max_score, n_questions, n_correct, n_wrong, n_skipped, raw_json, '
                    'saved_at, updated_at, user_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (
            ex['id'], student or cfg.get('candidate') or 'Candidate', cfg.get('testName'), ms_iso(started), ms_iso(submitted),
            cfg.get('duration'), (submitted - started) / 1000 if started and submitted else None, int(bool(ex.get('timeUp'))),
            cfg.get('bankName'), json.dumps(cfg.get('years') or []),
            json.dumps({k: cfg.get(k) for k in ('mcqC', 'mcqW', 'numC', 'numW')}),
            score, mx, len(qs), nc, nw, ns, json.dumps(ex, ensure_ascii=False),
            existing['saved_at'] if existing else t, t, user_id))
        con.executemany('INSERT INTO responses VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', rows)
        con.executemany('INSERT INTO practice VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', prows)
    return {'id': ex['id'], 'score': score, 'max': mx}


# ---------- accounts ----------
USERNAME_RE = re.compile(r'^[a-z0-9._-]{3,30}$')
OTP_ALPHABET = 'abcdefghjkmnpqrstuvwxyz23456789'          # no 0/o, 1/l/i: easy to read out to a friend
FAILS = {}                                               # login failures: key -> [timestamps] (per process)
FAIL_WINDOW = 15 * 60
FAIL_LIMIT = {'user': 8, 'ip': 40}                  # per username; per address is looser (friends may share a Wi-Fi)
DUMMY_HASH = generate_password_hash('not-a-real-password')


def one_time_password():
    return '-'.join(''.join(secrets.choice(OTP_ALPHABET) for _ in range(4)) for _ in range(3))


def password_problem(pw, username=''):
    if not isinstance(pw, str) or len(pw) < 8:
        return 'Use at least 8 characters.'
    if len(pw) > 200:
        return 'That password is too long.'
    if username and pw.lower() == username.lower():
        return 'The password cannot be the same as the username.'
    return None


def create_user(con, username, name, password=None, role='student'):
    """Adds a user and returns their one-time password (or None when a password was given). Raises ValueError."""
    username = (username or '').strip().lower()
    name = (name or '').strip()
    if not USERNAME_RE.match(username):
        raise ValueError('Username: 3-30 characters, lowercase letters, digits, dot, dash or underscore.')
    if not name or len(name) > 60:
        raise ValueError('Give a name of up to 60 characters.')
    if role not in ('student', 'admin'):
        raise ValueError('Role must be student or admin.')
    if con.execute('SELECT 1 FROM users WHERE username = ?', (username,)).fetchone():
        raise ValueError(f'The username "{username}" is already taken.')
    otp = None
    if password is None:
        password = otp = one_time_password()
    elif password_problem(password, username):
        raise ValueError(password_problem(password, username))
    con.execute('INSERT INTO users (username, name, pw_hash, role, must_change, active, created_at) VALUES (?,?,?,?,?,1,?)',
                (username, name, generate_password_hash(password), role, int(otp is not None), now_iso()))
    return otp


def pw_tag(pw_hash):
    """Stored in the session; changes whenever the password does, which signs out old sessions."""
    return pw_hash[-12:]


def current_user():
    uid = session.get('uid')
    if not uid:
        return None
    with db() as con:
        u = con.execute('SELECT id, username, name, role, must_change, active, pw_hash FROM users WHERE id = ?', (uid,)).fetchone()
    if not u or not u['active'] or session.get('pw') != pw_tag(u['pw_hash']):
        session.clear()
        return None
    return u


def client_ip():
    return request.headers.get('X-Real-IP') or request.remote_addr or '?'


def too_many_fails(*keys):
    cut = time.time() - FAIL_WINDOW
    for k in keys:
        FAILS[k] = [t for t in FAILS.get(k, []) if t > cut]
    return any(len(FAILS[k]) >= FAIL_LIMIT[k.split(':', 1)[0]] for k in keys)


def user_json(u):
    return {'id': u['id'], 'username': u['username'], 'name': u['name'], 'role': u['role'], 'must_change': bool(u['must_change'])}


OPEN_PATHS = {'/login', '/login.html', '/api/login', '/api/export', '/favicon.ico'}
ALLOWED_WHILE_CHANGING = {'/api/me', '/api/password', '/api/logout'}


@app.before_request
def gate():
    """Everything needs a signed-in user except the login page, /api/login and the key-protected export."""
    path = request.path
    if path in OPEN_PATHS:
        return None
    is_api = path.startswith('/api/')
    if is_api and request.method == 'POST':
        # JSON only: a plain cross-site form cannot send application/json, so a hostile page can't post as the user
        if not request.is_json:
            return jsonify(error='Expected JSON.'), 415
        origin = request.headers.get('Origin')
        if origin and origin.split('://', 1)[-1] != request.host:
            return jsonify(error='Cross-site request refused.'), 403
    u = current_user()
    if not u:
        return (jsonify(error='Please sign in.', login=True), 401) if is_api else redirect('/login')
    if u['must_change'] and path not in ALLOWED_WHILE_CHANGING:
        return (jsonify(error='Choose a new password first.', must_change=True), 403) if is_api else redirect('/login?change=1')
    g.user = u
    return None


def target_user_id():
    """Whose data a read endpoint returns: your own; an admin may ask for anyone's with ?user=<id>."""
    want = request.args.get('user')
    if want and g.user['role'] == 'admin':
        try:
            return int(want)
        except ValueError:
            abort(400)
    return g.user['id']


@app.post('/api/login')
def login():
    d = request.get_json(silent=True) or {}
    username, password = str(d.get('username', '')).strip().lower(), str(d.get('password', ''))
    keys = ('ip:' + client_ip(), 'user:' + username)
    if too_many_fails(*keys):
        return jsonify(error='Too many wrong tries. Wait 15 minutes and try again.'), 429
    with db() as con:
        u = con.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        ok = check_password_hash(u['pw_hash'] if u else DUMMY_HASH, password) and u is not None and u['active']
        if ok:
            con.execute('UPDATE users SET last_login = ? WHERE id = ?', (now_iso(), u['id']))
    if not ok:
        for k in keys:
            FAILS.setdefault(k, []).append(time.time())
        return jsonify(error='Wrong username or password.'), 401
    session.clear()
    session.permanent = True
    session['uid'], session['pw'] = u['id'], pw_tag(u['pw_hash'])
    return jsonify(ok=True, user=user_json(u))


@app.post('/api/logout')
def logout():
    session.clear()
    return jsonify(ok=True)


@app.get('/api/me')
def me():
    return jsonify(user_json(g.user))


@app.post('/api/password')
def change_password():
    d = request.get_json(silent=True) or {}
    new = d.get('new')
    with db() as con:
        u = con.execute('SELECT * FROM users WHERE id = ?', (g.user['id'],)).fetchone()
        if not check_password_hash(u['pw_hash'], str(d.get('current', ''))):
            return jsonify(error='Your current password is not right.'), 400
        problem = password_problem(new, u['username'])
        if problem:
            return jsonify(error=problem), 400
        if check_password_hash(u['pw_hash'], new):
            return jsonify(error='Choose a password different from the current one.'), 400
        h = generate_password_hash(new)
        con.execute('UPDATE users SET pw_hash = ?, must_change = 0 WHERE id = ?', (h, u['id']))
    session['pw'] = pw_tag(h)          # this session stays signed in; any other session is signed out
    return jsonify(ok=True)


def require_admin():
    if g.user['role'] != 'admin':
        abort(403)


@app.get('/api/admin/users')
def admin_users():
    require_admin()
    with db() as con:
        rows = con.execute('''
            SELECT u.id, u.username, u.name, u.role, u.active, u.must_change, u.created_at, u.last_login,
                   COUNT(a.id) AS tests, MAX(a.submitted_at) AS last_test,
                   (SELECT score || ' / ' || max_score FROM attempts b WHERE b.user_id = u.id ORDER BY submitted_at DESC LIMIT 1) AS last_score
            FROM users u LEFT JOIN attempts a ON a.user_id = u.id
            GROUP BY u.id ORDER BY u.role DESC, u.name COLLATE NOCASE''').fetchall()
        unowned = con.execute('SELECT COUNT(*) FROM attempts WHERE user_id IS NULL').fetchone()[0]
    return jsonify(users=[dict(r) for r in rows], unowned_tests=unowned)


@app.post('/api/admin/users')
def admin_add_user():
    require_admin()
    d = request.get_json(silent=True) or {}
    try:
        with db() as con:
            otp = create_user(con, d.get('username'), d.get('name'))
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(ok=True, username=str(d.get('username')).strip().lower(), one_time_password=otp)


@app.post('/api/admin/users/<int:uid>/reset')
def admin_reset(uid):
    require_admin()
    if uid == g.user['id']:
        return jsonify(error='Change your own password from your account menu.'), 400
    otp = one_time_password()
    with db() as con:
        n = con.execute('UPDATE users SET pw_hash = ?, must_change = 1 WHERE id = ?', (generate_password_hash(otp), uid)).rowcount
    if not n:
        abort(404)
    return jsonify(ok=True, one_time_password=otp)


@app.post('/api/admin/users/<int:uid>/active')
def admin_active(uid):
    require_admin()
    if uid == g.user['id']:
        return jsonify(error='You cannot switch off your own account.'), 400
    active = bool((request.get_json(silent=True) or {}).get('active'))
    with db() as con:
        n = con.execute('UPDATE users SET active = ? WHERE id = ?', (int(active), uid)).rowcount
    if not n:
        abort(404)
    return jsonify(ok=True, active=active)


# ---------- attempts ----------
@app.post('/api/attempts')
def post_attempt():
    ex = request.get_json(silent=True)
    if not isinstance(ex, dict) or not ex.get('id') or not ex.get('submittedAt') or 'qs' not in ex or 'resp' not in ex:
        return jsonify(error='Expected a submitted exam object.'), 400
    with db() as con:
        owner = con.execute('SELECT user_id FROM attempts WHERE id = ?', (str(ex['id']),)).fetchone()
    if owner and owner['user_id'] != g.user['id']:
        return jsonify(error='This test was saved by another account.'), 403
    try:
        return jsonify(ok=True, **save_attempt(ex, g.user['id'], g.user['name']))
    except (KeyError, TypeError, ValueError) as e:
        return jsonify(error=f'Could not read the exam: {e}'), 400


@app.get('/api/attempts')
def list_attempts():
    with db() as con:
        rows = con.execute('SELECT id, student, test_name, submitted_at, score, max_score, n_questions, n_correct, n_wrong, n_skipped '
                           'FROM attempts WHERE user_id = ? ORDER BY submitted_at DESC', (target_user_id(),)).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get('/api/progress')
def progress():
    """Read-only: one user's saved attempts with their responses and review outcomes, for the app's progress view.
    The app does the counting with the same rules as tools/analysis_data.py."""
    uid = target_user_id()
    with db() as con:
        who = con.execute('SELECT id, username, name FROM users WHERE id = ?', (uid,)).fetchone()
        if not who:
            abort(404)
        atts = con.execute('SELECT id, student, test_name, submitted_at, score, max_score, n_questions, n_correct, n_wrong, n_skipped '
                           'FROM attempts WHERE user_id = ? ORDER BY submitted_at', (uid,)).fetchall()
        mine = 'SELECT id FROM attempts WHERE user_id = ?'
        resp = con.execute('SELECT attempt_id, q_index, question_id, subject, chapter, qtype, given, attempted, correct, marks, time_ms, reason '
                           f'FROM responses WHERE attempt_id IN ({mine}) ORDER BY attempt_id, q_index', (uid,)).fetchall()
        prac = con.execute('SELECT attempt_id, q_index, question_id, in_test, outcome, hints_used FROM practice '
                           f'WHERE attempt_id IN ({mine})', (uid,)).fetchall()
    return jsonify(user=dict(who), attempts=[dict(r) for r in atts], responses=[dict(r) for r in resp], practice=[dict(r) for r in prac])


@app.get('/api/flags')
def list_flags():
    with db() as con:
        rows = con.execute("SELECT id, subject, chapter, concept, kind, severity, status, action, updated_at FROM flags "
                           "WHERE status != 'resolved' AND user_id = ? "
                           "ORDER BY CASE severity WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END, updated_at DESC",
                           (target_user_id(),)).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get('/api/export')
def export_db():
    key = export_key()
    if not key:
        abort(404)
    if not secrets.compare_digest(request.headers.get('X-Export-Key', ''), key):
        abort(403)
    # a consistent snapshot even while the app is writing
    fd, tmp = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    with db() as src, sqlite3.connect(tmp) as dst:
        src.backup(dst)
    return send_file(tmp, as_attachment=True, download_name='akil.db', mimetype='application/vnd.sqlite3')


# ---------- static files: only the app itself and NTA question images, never data/ or .secrets ----------
@app.get('/')
def index():
    # the signed-in user goes into the page, so the app knows whose browser storage and name to use before anything loads
    me = json.dumps(user_json(g.user)).replace('<', '\\u003c')
    html = (ROOT / 'index.html').read_text(encoding='utf-8').replace('<head>', f'<head>\n<script>window.JEE_ME = {me};</script>', 1)
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}


@app.get('/login')
def login_page():
    return send_from_directory(ROOT, 'login.html')


@app.get('/<name>')
def static_root(name):
    if name not in STATIC_FILES | PUBLIC_FILES or name == 'index.html':
        abort(404)
    return send_from_directory(ROOT, name)


@app.get('/pyq/<path:p>')
def pyq_images(p):
    if not p.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        abort(404)
    return send_from_directory(ROOT / 'pyq', p)


@app.after_request
def no_cache_for_private(resp):
    if request.path.startswith('/api/') or request.path in ('/', '/index.html'):
        resp.headers['Cache-Control'] = 'no-store'
    return resp


app.secret_key = session_secret()
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f'JEE Mock CBT running at http://localhost:{port}  (database: {DB_PATH})')
    with db() as con:
        if not con.execute("SELECT 1 FROM users WHERE role = 'admin' AND active = 1").fetchone():
            print('No admin account yet: run  python tools/manage_users.py add-admin <username> "<your name>"')
    app.run(host='127.0.0.1', port=port, debug=False)
