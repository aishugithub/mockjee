"""
Write one analysis (the jee-analysis skill's result.json) into the database: a row in `analyses`
(the Markdown report) and new or updated rows in `flags`. Used by tools/save_analysis.py (local
database) and by server.py's key-protected POST /api/import-analysis (the online database), so both
write exactly the same way.
"""
import json
import sqlite3
from datetime import datetime, timezone

KINDS = {'concept_gap', 'formula_misapplied', 'calculation', 'units', 'misread', 'ncert_fact', 'speed'}


class AnalysisError(ValueError):
    pass


def check(res):
    bad = []
    for f in res.get('flags', []):
        if f.get('kind') not in KINDS: bad.append(f"kind {f.get('kind')!r}")
        if f.get('severity') not in ('high', 'medium', 'low'): bad.append(f"severity {f.get('severity')!r}")
        if f.get('status', 'open') not in ('open', 'improving', 'resolved'): bad.append(f"status {f.get('status')!r}")
        if not all(f.get(k) for k in ('subject', 'chapter', 'concept')): bad.append('subject/chapter/concept missing')
    if not res.get('summary'): bad.append('summary missing')
    if bad:
        raise AnalysisError('Not saved: ' + '; '.join(bad))


def user_id(con, username):
    """users.id for a username; None for databases made before accounts existed (one student only)."""
    if not con.execute("SELECT 1 FROM sqlite_master WHERE name = 'users'").fetchone():
        if username:
            raise AnalysisError('This database has no accounts yet; leave out the username.')
        return None
    if not username:
        names = [r[0] for r in con.execute("SELECT username FROM users WHERE role = 'student' ORDER BY username")]
        raise AnalysisError('Say whose tests these are (username). Students: ' + (', '.join(names) or 'none yet'))
    row = con.execute('SELECT id FROM users WHERE username = ?', (username.lower(),)).fetchone()
    if not row:
        raise AnalysisError(f'No user "{username}".')
    return row[0]


def save(con, res, username):
    """Validate and write; returns (new flags, updated flags). Raises AnalysisError on bad input."""
    check(res)
    uid = user_id(con, username)
    mine = '' if uid is None else ' AND user_id = ?'
    me = () if uid is None else (uid,)
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    with con:
        if uid is None:
            con.execute('INSERT INTO analyses (created_at, attempts, summary) VALUES (?,?,?)',
                        (now, json.dumps(res.get('attempts', [])), res['summary']))
        else:
            con.execute('INSERT INTO analyses (created_at, attempts, summary, user_id) VALUES (?,?,?,?)',
                        (now, json.dumps(res.get('attempts', [])), res['summary'], uid))
        n_new = n_upd = 0
        for f in res.get('flags', []):
            row = con.execute('SELECT id, evidence FROM flags WHERE id = ?' + mine, (f['id'],) + me).fetchone() if f.get('id') else \
                con.execute('SELECT id, evidence FROM flags WHERE subject = ? AND chapter = ? AND concept = ?' + mine,
                            (f['subject'], f['chapter'], f['concept']) + me).fetchone()
            if row:
                ev = json.loads(row[1] or '[]')
                seen = {(e.get('attempt_id'), e.get('q_index')) for e in ev}
                ev += [e for e in f.get('evidence', []) if (e.get('attempt_id'), e.get('q_index')) not in seen]
                con.execute('UPDATE flags SET kind=?, severity=?, status=?, evidence=?, action=?, updated_at=? WHERE id=?',
                            (f['kind'], f['severity'], f.get('status', 'open'), json.dumps(ev), f.get('action'), now, row[0]))
                n_upd += 1
            else:
                con.execute('INSERT INTO flags (subject, chapter, concept, kind, severity, status, evidence, action, created_at, updated_at'
                            + ('' if uid is None else ', user_id') + ') VALUES (?,?,?,?,?,?,?,?,?,?' + ('' if uid is None else ',?') + ')',
                            (f['subject'], f['chapter'], f['concept'], f['kind'], f['severity'], f.get('status', 'open'),
                             json.dumps(f.get('evidence', [])), f.get('action'), now, now) + me)
                n_new += 1
    return n_new, n_upd
