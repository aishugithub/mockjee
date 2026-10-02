"""
Write the jee-analysis skill's results into Akil's database: one row in `analyses`
(the Markdown report) and new or updated rows in `flags` (shown read-only in the app).

Usage:  python tools/save_analysis.py result.json [--db data/akil.db]

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('result')
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
    with con:
        con.execute('INSERT INTO analyses (created_at, attempts, summary) VALUES (?,?,?)',
                    (now, json.dumps(res.get('attempts', [])), res['summary']))
        n_new = n_upd = 0
        for f in res.get('flags', []):
            row = con.execute('SELECT id, evidence FROM flags WHERE id = ?', (f['id'],)).fetchone() if f.get('id') else \
                con.execute('SELECT id, evidence FROM flags WHERE subject = ? AND chapter = ? AND concept = ?',
                            (f['subject'], f['chapter'], f['concept'])).fetchone()
            if row:
                ev = json.loads(row[1] or '[]')
                seen = {(e.get('attempt_id'), e.get('q_index')) for e in ev}
                ev += [e for e in f.get('evidence', []) if (e.get('attempt_id'), e.get('q_index')) not in seen]
                con.execute('UPDATE flags SET kind=?, severity=?, status=?, evidence=?, action=?, updated_at=? WHERE id=?',
                            (f['kind'], f['severity'], f.get('status', 'open'), json.dumps(ev), f.get('action'), now, row[0]))
                n_upd += 1
            else:
                con.execute('INSERT INTO flags (subject, chapter, concept, kind, severity, status, evidence, action, created_at, updated_at) '
                            'VALUES (?,?,?,?,?,?,?,?,?,?)',
                            (f['subject'], f['chapter'], f['concept'], f['kind'], f['severity'], f.get('status', 'open'),
                             json.dumps(f.get('evidence', [])), f.get('action'), now, now))
                n_new += 1
    print(f'Saved analysis; {n_new} new flags, {n_upd} updated ({a.db})')


if __name__ == '__main__':
    main()
