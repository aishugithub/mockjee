"""
One command for the end of a shift: writes solutions.csv from the data file, runs the answer checks,
rebuilds pyq_bank.js and writes the review page. Stops (exit 1) on the first problem, so nothing is
committed with a disagreement, a missing check or a malformed solution.

Usage:  python tools/finish_shift.py <data.py> pyq/<year>/<shift>
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def repair_split_strings(path):
    """Join double-quoted literals that were broken across physical lines (newline -> backslash-n)."""
    lines = open(path, encoding='utf-8').read().split('\n')
    out, buf = [], None
    for line in lines:
        buf = line if buf is None else buf + '\\n' + line
        n, i = 0, 0
        while i < len(buf):
            if buf[i] == '\\':
                i += 2; continue
            n += buf[i] == '"'
            i += 1
        if n % 2 == 0:
            out.append(buf); buf = None
    if buf is not None:
        out.append(buf)
    text = '\n'.join(out)
    compile(text, path, 'exec')
    open(path, 'w', encoding='utf-8').write(text)


def run(*args):
    r = subprocess.run([sys.executable, '-W', 'ignore', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    return r.returncode, r.stdout + r.stderr


def main():
    data, folder = sys.argv[1], sys.argv[2].rstrip('/\\')
    year, shift = folder.replace('\\', '/').split('/')[-2:]
    repair_split_strings(data)
    code, out = run('tools/write_solutions_csv.py', data, folder)
    print(out.strip())
    if code: sys.exit(1)
    code, out = run('tools/verify_pyq_solutions.py')
    problems = [l for l in out.splitlines() if (' MISMATCH ' in l or 'FLAG' in l or 'labelled' in l or 'differs from claude_answer' in l
                                               or 'is empty' in l or 'Traceback' in l or 'Error' in l)]
    mine = [l for l in out.splitlines() if l.startswith(f'{year} {shift}')]
    print('\n'.join(l for l in mine if ' ok ' not in l))
    if problems:
        print('PROBLEMS:\n' + '\n'.join(problems)); sys.exit(1)
    code, out = run('tools/build_pyq_bank.py')
    print('\n'.join(l for l in out.splitlines() if shift[:5] in l or 'held back' in l or 'Claude gets' in l or 'questions in' in l))
    if code: print(out); sys.exit(1)
    code, out = run('tools/make_solution_review.py', folder)
    if code: print(out); sys.exit(1)
    print('OK: ready to commit')


if __name__ == '__main__':
    main()
