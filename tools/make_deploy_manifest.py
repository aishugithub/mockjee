"""
Writes deploy_manifest.txt: every file the online app needs (the same list as make_deploy_bundle.py), with its
git blob hash and size. tools/pa_sync.py reads it on PythonAnywhere and downloads only the files that differ.
Commit and push the manifest after running this (the hashes must be of committed files).

Usage:  python tools/make_deploy_manifest.py
"""
import os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_deploy_bundle import APP_FILES, ROOT


def main():
    out = subprocess.run(['git', 'ls-files', '-s', '--', *APP_FILES, 'pyq/*/*/img/*'], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    entries = [(line.split('\t', 1)[0].split()[1], line.split('\t', 1)[1]) for line in out.splitlines()]
    # Blob sizes from git, not the working tree: on Windows the checkout has CRLF line endings, while
    # PythonAnywhere gets the LF files from GitHub, and pa_sync.py compares images and app files by size.
    sizes = subprocess.run(['git', 'cat-file', '--batch-check=%(objectsize)'], cwd=ROOT, capture_output=True,
                           text=True, check=True, input=''.join(sha + '\n' for sha, _ in entries)).stdout.split()
    rows = [f'{sha} {size} {path}' for (sha, path), size in zip(entries, sizes)]
    missing = [f for f in APP_FILES if not any(r.endswith(' ' + f) for r in rows)]
    if missing:
        sys.exit(f'Not committed: {missing}')
    with open(os.path.join(ROOT, 'deploy_manifest.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(rows) + '\n')
    print(f'deploy_manifest.txt: {len(rows)} files, {sum(int(r.split()[1]) for r in rows) / 2**20:.0f} MB')


if __name__ == '__main__':
    main()
