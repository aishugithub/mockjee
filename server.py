"""JEE Mock CBT: small Flask server that serves the app and keeps every attempt in SQLite.

Run locally:   python server.py          (then open http://localhost:8000)
PythonAnywhere: point the WSGI file at `app` in this module (see DEPLOY notes in README.md).

The app works without this server too (opened as a file or as a claude.ai Artifact);
it then keeps results in the browser and sends them here the next time the server is reachable.

Endpoints
  POST /api/attempts          save (or update) one finished exam, JSON body = the app's exam object
  GET  /api/attempts          list saved attempts (summary rows)
  GET  /api/progress          every saved attempt's responses and review outcomes (read-only, for the progress view)
  GET  /api/flags             concept flags written by Claude's analysis (read-only for the app)
  GET  /api/export            download a copy of the database; needs header X-Export-Key
"""
import json
import os
import sqlite3
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_file, send_from_directory

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get('JEE_DB_PATH', ROOT / 'data' / 'akil.db'))
STATIC_FILES = {'index.html', 'questions.js', 'pyq_bank.js'}

SCHEMA = """
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

-- Written by Claude during analysis (jee-analysis skill), shown read-only in the app.
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
        # attempts saved by an older server kept the hint-ladder log only in raw_json: rebuild those practice rows
        todo = [r[0] for r in con.execute(
            "SELECT raw_json FROM attempts a WHERE raw_json LIKE '%\"practice\"%' "
            "AND NOT EXISTS (SELECT 1 FROM practice p WHERE p.attempt_id = a.id)")]
    for raw in todo:
        try:
            save_attempt(json.loads(raw))
        except (KeyError, TypeError, ValueError):
            pass


def export_key():
    """The export key comes from the environment (PythonAnywhere) or from .secrets next to this file."""
    key = os.environ.get('JEE_EXPORT_KEY')
    if key:
        return key.strip()
    f = ROOT / '.secrets'
    if f.exists():
        for line in f.read_text(encoding='utf-8').splitlines():
            if line.strip().startswith('JEE_EXPORT_KEY='):
                return line.split('=', 1)[1].strip()
    return None


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


def save_attempt(ex):
    """Recompute marks on the server from the exam object so the database never depends on the browser's arithmetic."""
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
        existing = con.execute('SELECT saved_at FROM attempts WHERE id = ?', (ex['id'],)).fetchone()
        con.execute('DELETE FROM responses WHERE attempt_id = ?', (ex['id'],))
        con.execute('DELETE FROM practice WHERE attempt_id = ?', (ex['id'],))
        con.execute('DELETE FROM attempts WHERE id = ?', (ex['id'],))
        con.execute('INSERT INTO attempts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (
            ex['id'], cfg.get('candidate') or 'Candidate', cfg.get('testName'), ms_iso(started), ms_iso(submitted),
            cfg.get('duration'), (submitted - started) / 1000 if started and submitted else None, int(bool(ex.get('timeUp'))),
            cfg.get('bankName'), json.dumps(cfg.get('years') or []),
            json.dumps({k: cfg.get(k) for k in ('mcqC', 'mcqW', 'numC', 'numW')}),
            score, mx, len(qs), nc, nw, ns, json.dumps(ex, ensure_ascii=False),
            existing['saved_at'] if existing else t, t))
        con.executemany('INSERT INTO responses VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', rows)
        con.executemany('INSERT INTO practice VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', prows)
    return {'id': ex['id'], 'score': score, 'max': mx}


@app.post('/api/attempts')
def post_attempt():
    ex = request.get_json(silent=True)
    if not isinstance(ex, dict) or not ex.get('id') or not ex.get('submittedAt') or 'qs' not in ex or 'resp' not in ex:
        return jsonify(error='Expected a submitted exam object.'), 400
    try:
        return jsonify(ok=True, **save_attempt(ex))
    except (KeyError, TypeError, ValueError) as e:
        return jsonify(error=f'Could not read the exam: {e}'), 400


@app.get('/api/attempts')
def list_attempts():
    with db() as con:
        rows = con.execute('SELECT id, student, test_name, submitted_at, score, max_score, n_questions, n_correct, n_wrong, n_skipped '
                           'FROM attempts ORDER BY submitted_at DESC').fetchall()
    return jsonify([dict(r) for r in rows])


@app.get('/api/progress')
def progress():
    """Read-only: every saved attempt with its responses and review outcomes, for the app's progress view.
    The app does the counting with the same rules as tools/analysis_data.py."""
    with db() as con:
        atts = con.execute('SELECT id, student, test_name, submitted_at, score, max_score, n_questions, n_correct, n_wrong, n_skipped '
                           'FROM attempts ORDER BY submitted_at').fetchall()
        resp = con.execute('SELECT attempt_id, q_index, question_id, subject, chapter, qtype, given, attempted, correct, marks, time_ms, reason '
                           'FROM responses ORDER BY attempt_id, q_index').fetchall()
        prac = con.execute('SELECT attempt_id, q_index, question_id, in_test, outcome, hints_used FROM practice').fetchall()
    return jsonify(attempts=[dict(r) for r in atts], responses=[dict(r) for r in resp], practice=[dict(r) for r in prac])


@app.get('/api/flags')
def list_flags():
    with db() as con:
        rows = con.execute("SELECT id, subject, chapter, concept, kind, severity, status, action, updated_at FROM flags "
                           "WHERE status != 'resolved' ORDER BY CASE severity WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END, updated_at DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get('/api/export')
def export_db():
    key = export_key()
    if not key:
        abort(404)
    if request.headers.get('X-Export-Key', '') != key:
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
    return send_from_directory(ROOT, 'index.html')


@app.get('/<name>')
def static_root(name):
    if name not in STATIC_FILES:
        abort(404)
    return send_from_directory(ROOT, name)


@app.get('/pyq/<path:p>')
def pyq_images(p):
    if not p.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        abort(404)
    return send_from_directory(ROOT / 'pyq', p)


init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f'JEE Mock CBT running at http://localhost:{port}  (database: {DB_PATH})')
    app.run(host='127.0.0.1', port=port, debug=False)
