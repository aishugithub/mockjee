"""
Runs ON PythonAnywhere (Bash console, inside ~/mockjee): brings the app files and question images up to date
from the public GitHub repo, downloading only files that are missing or differ (compared by git blob hash with
deploy_manifest.txt at that commit). The database (data/) and .secrets are never touched.

    cd ~/mockjee && python3 tools/pa_sync.py <commit>            # see what would change, then:
    cd ~/mockjee && python3 tools/pa_sync.py <commit> --go       # download; add --prune to delete images no
                                                                 # longer in the bank. Then Reload on the Web tab.
To save the free account's 100 CPU-seconds a day, question images are compared by size only (an image that
changed but kept exactly the same size is missed); the few app files are always hashed. Sizes in the manifest
are git's (LF line endings), so check a Windows checkout with --full only. Add --full to hash
every image too (reads about 250 MB, so expect tens of CPU-seconds).
Standard library only (the free account allows raw.githubusercontent.com).
"""
import hashlib, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO = 'https://raw.githubusercontent.com/aishugithub/mockjee'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def blob_sha(path):
    data = open(path, 'rb').read()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def fetch(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:
            if attempt == 3:
                raise


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    commit, go, prune, full = args[0], '--go' in sys.argv, '--prune' in sys.argv, '--full' in sys.argv
    manifest = [l.split(' ', 2) for l in fetch(f'{REPO}/{commit}/deploy_manifest.txt').decode().splitlines() if l]
    wanted = {p: (sha, int(n)) for sha, n, p in manifest}

    def stale(p):
        path = os.path.join(ROOT, p)
        sha, size = wanted[p]
        if not os.path.exists(path) or os.path.getsize(path) != size:
            return True
        if '/img/' in p and not full:
            return False
        return blob_sha(path) != sha

    todo = [p for p in wanted if stale(p)]
    extra = [os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')
             for d, _, fs in os.walk(os.path.join(ROOT, 'pyq')) for f in fs]
    extra = [p for p in extra if '/img/' in p and p not in wanted]
    print(f'{len(wanted)} files in the manifest; {len(todo)} to download '
          f'({sum(wanted[p][1] for p in todo) / 2**20:.0f} MB); {len(extra)} old images not in the bank.')
    if not go:
        print('Nothing changed yet. Run again with --go (and --prune to delete the old images).'); return

    def one(p):
        data = fetch(f'{REPO}/{commit}/{p}')
        if hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() != wanted[p][0]:
            raise RuntimeError(f'{p}: downloaded file does not match the manifest')
        dest = os.path.join(ROOT, p)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest + '.part', 'wb') as f:
            f.write(data)
        os.replace(dest + '.part', dest)

    done = 0
    with ThreadPoolExecutor(8) as ex:
        for _ in ex.map(one, todo):
            done += 1
            if done % 1000 == 0:
                print(f'  {done}/{len(todo)}', flush=True)
    print(f'Downloaded {done} files.')
    if prune:
        for p in extra:
            os.remove(os.path.join(ROOT, p))
        print(f'Deleted {len(extra)} old images.')
    print('Now press Reload on the Web tab.')


if __name__ == '__main__':
    main()
