"""
Write the jee-analysis skill's results into Akil's database: one row in `analyses`
(the Markdown report) and new or updated rows in `flags` (shown read-only in the app).

Usage:  python tools/save_analysis.py result.json --user akil [--db data/akil.db]

result.json:
{
  "attempts": ["<attempt id>", ...],          # attempts this analysis covered
  "summary": "<Markdown report>",
  "flags": [                                   # one per specific weakness; update rather than duplicate
    {"id": 12,                                 # optional: update this existing flag
     "subject": "Physics", "chapter": "Electrostatic Potential and Capacitance",
     "concept": "capacitor with a dielectric layer (series vs parallel)",
     "kind": "concept_gap",                    # concept_gap | formula_misapplied | calculation | units | misread | ncert_fact | speed
     "severity": "high",                       # high | medium | low
     "status": "open",                         # open | improving | resolved
     "evidence": [{"attempt_id": "...", "q_index": 31, "question_id": "69112132", "note": "picked 200%: treated layers as parallel"}],
     "action": "Revise ...; then practise 5 questions from ..."}
  ]
}
"""
import argparse, json, os, sqlite3, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KINDS = {'concept_gap', 'formula_misapplied', 'calculation', 'units', 'misread', 'ncert_fact', 'speed'}


def user_id(con, username):
    """users.id for a username; None for databases made before accounts existed (one student only)."""
    if not con.execute("SELECT 1 FROM sqlite_master WHERE name = 'users'").fetchone():
        if username:
            sys.exit('This database has no accounts yet; leave out --user.')
        return None
    if not username:
        names = [r[0] for r in con.execute("SELECT username FROM users WHERE role = 'student' ORDER BY username")]
        sys.exit('Say whose tests to use with --user <username>. Students: ' + (', '.join(names) or 'none yet'))
    row = con.execute('SELECT id FROM users WHERE username = ?', (username.lower(),)).fetchone()
    if not row:
        sys.exit(f'No user "{username}".')
    return row[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('result')
    ap.add_argument('--user', help='username of the student the analysis is about')
    ap.add_argument('--db', default=os.environ.get('JEE_DB_PATH', os.path.join(ROOT, 'data', 'akil.db')))
    a = ap.parse_args()
    res = json.load(open(a.result, encoding='utf-8'))
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    bad = []
    for f in res.get('flags', []):
        if f.get('kind') not in KINDS: bad.append(f"kind {f.get('kind')!r}")
        if f.get('severity') not in ('high', 'medium', 'low'): bad.append(f"severity {f.get('severity')!r}")
        if f.get('status', 'open') not in ('open', 'improving', 'resolved'): bad.append(f"status {f.get('status')!r}")
        if not all(f.get(k) for k in ('subject', 'chapter', 'concept')): bad.append('subject/chapter/concept missing')
    if not res.get('summary'): bad.append('summary missing')
    if bad:
        sys.exit('Not saved: ' + '; '.join(bad))
    con = sqlite3.connect(a.db)
    uid = user_id(con, a.user)
    mine = '' if uid is None else ' AND user_id = ?'
    me = () if uid is None else (uid,)
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
    print(f'Saved analysis; {n_new} new flags, {n_upd} updated ({a.db})')


if __name__ == '__main__':
    main()
