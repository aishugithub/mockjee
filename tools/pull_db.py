"""Fetch the latest progress database for analysis.

Local use (app run with server.py on this computer): nothing to fetch, data/akil.db is already here.
Online use (PythonAnywhere): put these two lines in .secrets next to server.py (never commit that file):

    JEE_SERVER_URL=https://<username>.pythonanywhere.com
    JEE_EXPORT_KEY=<a long random key, same value as the JEE_EXPORT_KEY set on PythonAnywhere>

Then:  python tools/pull_db.py      -> saves data/akil.db (the old copy is kept as data/akil.prev.db)
"""
import shutil
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'data' / 'akil.db'


def read_secrets():
    f = ROOT / '.secrets'
    out = {}
    if f.exists():
        for line in f.read_text(encoding='utf-8').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.split('=', 1)
                out[k.strip()] = v.strip()
    return out


def main():
    sec = read_secrets()
    url, key = sec.get('JEE_SERVER_URL'), sec.get('JEE_EXPORT_KEY')
    if not url or not key:
        if DB.exists():
            print(f'No online server set up in .secrets; using the local database {DB}')
            return 0
        print('No .secrets with JEE_SERVER_URL and JEE_EXPORT_KEY, and no local data/akil.db.', file=sys.stderr)
        return 1
    req = urllib.request.Request(url.rstrip('/') + '/api/export', headers={'X-Export-Key': key})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        print(f'Server refused the export (HTTP {e.code}). Check JEE_EXPORT_KEY matches the one on the server.', file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f'Could not reach {url}: {e.reason}', file=sys.stderr)
        return 1
    DB.parent.mkdir(parents=True, exist_ok=True)
    tmp = DB.with_suffix('.download')
    tmp.write_bytes(data)
    try:
        n = sqlite3.connect(tmp).execute('SELECT COUNT(*) FROM attempts').fetchone()[0]
    except sqlite3.DatabaseError:
        tmp.unlink()
        print('The download is not a valid database.', file=sys.stderr)
        return 1
    if DB.exists():
        shutil.copy2(DB, DB.with_name('akil.prev.db'))
    tmp.replace(DB)
    print(f'Downloaded {DB} ({len(data) // 1024} KB, {n} attempts).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
