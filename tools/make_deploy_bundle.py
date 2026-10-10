"""
Packs what the online app needs into zip files small enough for PythonAnywhere's Files page
(uploads there are limited to 100 MB each). The NTA PDFs in sources/, the checker tools and git history
are left out: the free account has 512 MB of disk and the question images alone are about 265 MB.

Usage:  python tools/make_deploy_bundle.py [--with-db]      ->  dist/jee_part1.zip, jee_part2.zip, ...

  --with-db   also pack data/akil.db (Akil's saved tests), so his history continues online.
              Run `python tools/manage_users.py assign-tests akil` on it first (see DEPLOY.md).

Unzip every part into the same folder on PythonAnywhere: see DEPLOY.md.
"""
import glob, os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART_LIMIT = 80 * 1024 * 1024
APP_FILES = ['server.py', 'index.html', 'login.html', 'questions.js', 'pyq_bank.js', 'requirements.txt',
             'tools/manage_users.py', 'DEPLOY.md']


def main():
    with_db = '--with-db' in sys.argv[1:]
    out = os.path.join(ROOT, 'dist')
    os.makedirs(out, exist_ok=True)
    for old in glob.glob(os.path.join(out, 'jee_part*.zip')):
        os.remove(old)
    files = list(APP_FILES)
    if with_db:
        if not os.path.exists(os.path.join(ROOT, 'data', 'akil.db')):
            sys.exit('No data/akil.db to pack.')
        files.append('data/akil.db')
    images = sorted(os.path.relpath(p, ROOT).replace(os.sep, '/')
                    for p in glob.glob(os.path.join(ROOT, 'pyq', '*', '*', 'img', '*')) if os.path.isfile(p))
    parts, cur, size = [], [], 0
    for f in files + images:
        n = os.path.getsize(os.path.join(ROOT, f))
        if cur and size + n > PART_LIMIT:
            parts.append(cur); cur, size = [], 0
        cur.append(f); size += n
    parts.append(cur)
    for k, part in enumerate(parts, 1):
        path = os.path.join(out, f'jee_part{k}.zip')
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
            for f in part:
                z.write(os.path.join(ROOT, f), 'mockjee/' + f)
        print(f'{os.path.relpath(path, ROOT)}: {len(part)} files, {os.path.getsize(path) / 2**20:.0f} MB')
    total = sum(os.path.getsize(os.path.join(ROOT, f)) for p in parts for f in p)
    print(f'{len(images)} question images; {total / 2**20:.0f} MB once unzipped. Upload every part (see DEPLOY.md).')
    if not with_db:
        print('Akil\'s saved tests are NOT included (add --with-db to include data/akil.db).')


if __name__ == '__main__':
    main()
