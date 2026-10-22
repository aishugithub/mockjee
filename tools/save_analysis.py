"""
Write the jee-analysis skill's results into a student's database: one row in `analyses`
(the Markdown report) and new or updated rows in `flags` (shown read-only in the app).

Usage:
  python tools/save_analysis.py result.json --user akil              # local database (data/akil.db)
  python tools/save_analysis.py result.json --user akil --online     # the website's database (PythonAnywhere)
  python tools/save_analysis.py result.json --user akil --db PATH    # any other copy

--online sends result.json to POST /api/import-analysis with the X-Export-Key header, using
JEE_SERVER_URL / JEE_EXPORT_KEY from .secrets (same as tools/pull_db.py). The tests live online,
so the online database is the one that keeps the running record; save there.

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
import argparse, json, os, sqlite3, sys, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis_store  # noqa: E402
from pull_db import read_secrets  # noqa: E402  (tools/ is on sys.path when run as a script)


def send_online(res, username):
    sec = read_secrets()
    url, key = sec.get('JEE_SERVER_URL'), sec.get('JEE_EXPORT_KEY')
    if not url or not key:
        sys.exit('No JEE_SERVER_URL / JEE_EXPORT_KEY in .secrets.')
    body = json.dumps({'username': username, 'result': res}).encode('utf-8')
    req = urllib.request.Request(url.rstrip('/') + '/api/import-analysis', data=body, method='POST',
                                 headers={'Content-Type': 'application/json', 'X-Export-Key': key})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            out = json.loads(r.read())
    except urllib.error.HTTPError as e:
        msg = e.read().decode('utf-8', 'replace')[:300]
        sys.exit(f'Server refused (HTTP {e.code}): {msg}' + ('\nIs the new server.py uploaded and reloaded?' if e.code == 404 else ''))
    except urllib.error.URLError as e:
        sys.exit(f'Could not reach {url}: {e.reason}')
    print(f"Saved online; {out['new']} new flags, {out['updated']} updated ({url})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('result')
    ap.add_argument('--user', help='username of the student the analysis is about')
    ap.add_argument('--online', action='store_true', help="save into the website's database")
    ap.add_argument('--db', default=os.environ.get('JEE_DB_PATH', os.path.join(ROOT, 'data', 'akil.db')))
    a = ap.parse_args()
    res = json.load(open(a.result, encoding='utf-8'))
    try:
        analysis_store.check(res)
    except analysis_store.AnalysisError as e:
        sys.exit(str(e))
    if a.online:
        return send_online(res, a.user)
    try:
        n_new, n_upd = analysis_store.save(sqlite3.connect(a.db), res, a.user)
    except analysis_store.AnalysisError as e:
        sys.exit(str(e))
    print(f'Saved analysis; {n_new} new flags, {n_upd} updated ({a.db})')


if __name__ == '__main__':
    main()
