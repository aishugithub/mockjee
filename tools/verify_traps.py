"""
Checks every pyq/<year>/<shift>/traps.csv (Claude's trap analysis, step 3 in CLAUDE.md) and runs the
wrong-path recomputations in tools/trap_checks/y<year>_<shift>.py.

Fails (exit 1) on: an unknown mistake_type or check, an empty trap text, a row for the key (or an accepted
answer), a wrong MCQ option with no row, a duplicate row, a row labelled sympy/arithmetic with no check, a check
with no matching row, or a check whose wrong path does not land exactly on the option's value.
NTA's key is never touched: a trap only explains a wrong option.

Usage:  python tools/verify_traps.py
"""
import csv, glob, importlib.util, json, os, sys
from fractions import Fraction

from sympy import simplify, sympify

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from traps_common import CHECKS, COLS, MISTAKE_TYPES, NO_PATH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def same(a, b):
    if isinstance(a, tuple) or isinstance(b, tuple):
        return isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b) and all(same(p, q) for p, q in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return abs(float(a) - float(b)) <= 1e-9 * max(1.0, abs(float(b)))
    if isinstance(a, Fraction) or isinstance(b, Fraction):
        return Fraction(a) == Fraction(b)
    return simplify(sympify(a) - sympify(b)) == 0


def load_checks(year, shift):
    path = os.path.join(ROOT, 'tools', 'trap_checks', f'y{year}_{shift}.py')
    if not os.path.exists(path):
        return {}
    spec = importlib.util.spec_from_file_location(f'trap_checks.y{year}_{shift}', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.checks()


def verify(year, shift):
    folder = os.path.join(ROOT, 'pyq', year, shift)
    qs = json.load(open(os.path.join(folder, 'questions.json'), encoding='utf-8'))['questions']
    rows = list(csv.DictReader(open(os.path.join(folder, 'traps.csv'), encoding='utf-8')))
    bad, seen = [], {}
    if rows and list(rows[0].keys()) != COLS:
        bad.append(f'columns must be {COLS}')
    for r in rows:
        n, opt = int(r['q']), r['option'].strip()
        q = qs[n - 1]
        where = f'Q{n} option {opt}'
        if q.get('exclude') or q.get('answer') is None:
            bad.append(f'{where}: question is left out of the bank'); continue
        if q['type'] == 'MCQ':
            right = {q['answer'] + 1} | {a + 1 for a in q.get('accept', [])}
            if opt not in ('1', '2', '3', '4'): bad.append(f'{where}: MCQ option must be 1-4')
        else:
            right = {q['answer']} | set(q.get('accept', []))
        if any(float(opt) == float(k) for k in right): bad.append(f'{where}: a trap on the key / an accepted answer')
        if r['mistake_type'] not in MISTAKE_TYPES: bad.append(f"{where}: unknown mistake_type {r['mistake_type']}")
        if r['check'] not in CHECKS: bad.append(f"{where}: check must be one of {CHECKS}")
        if not r['trap'].strip(): bad.append(f'{where}: trap text is empty')
        if (r['mistake_type'] == 'none') != (r['trap'].strip() == NO_PATH):
            bad.append(f"{where}: mistake_type none goes with '{NO_PATH}' only")
        if r['mistake_type'] == 'none' and r['check'] != 'conceptual':
            bad.append(f'{where}: a row with no mistake path cannot claim a computed check')
        if (n, float(opt)) in seen: bad.append(f'{where}: duplicate row')
        seen[(n, float(opt))] = r
    for n, q in enumerate(qs, 1):          # every wrong MCQ option needs a row ("No clear mistake path" is fine)
        if q['type'] != 'MCQ' or q.get('exclude') or q.get('answer') is None or not any(k[0] == n for k in seen):
            continue
        right = {q['answer'] + 1} | {a + 1 for a in q.get('accept', [])}
        for o in sorted({1, 2, 3, 4} - right):
            if (n, float(o)) not in seen: bad.append(f'Q{n}: wrong option {o} has no row')
    checks = load_checks(year, shift)
    keyed = {(n, float(o)): f for (n, o), f in checks.items()}
    for k, r in seen.items():
        if r['check'] in ('sympy', 'arithmetic') and k not in keyed:
            bad.append(f"Q{k[0]} option {r['option']}: labelled '{r['check']}' but has no check in tools/trap_checks")
    ok = 0
    for (n, o), f in sorted(keyed.items()):
        r = seen.get((n, o))
        if r is None:
            bad.append(f'Q{n} option {o:g}: a check with no row in traps.csv'); continue
        if r['check'] == 'conceptual':
            bad.append(f"Q{n} option {r['option']}: has a check, so label it sympy or arithmetic")
        got, want = f()
        if qs[n - 1]['type'] != 'MCQ' and not same(want, Fraction(r['option'])):
            bad.append(f"Q{n}: check's trap value {want} differs from the row's value {r['option']}")
        if same(got, want):
            ok += 1
        else:
            bad.append(f"Q{n} option {r['option']}: MISMATCH, the wrong path gives {got}, the option is {want}")
    counts = {}
    for r in seen.values():
        counts[r['mistake_type']] = counts.get(r['mistake_type'], 0) + 1
    print(f'{year} {shift}: {len(rows)} trap rows, {ok} wrong paths recomputed; '
          + ', '.join(f'{k} {v}' for k, v in sorted(counts.items())))
    for b in bad:
        print(f'{year} {shift} {b}')
    return len(bad)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    bad = 0
    for path in sorted(glob.glob(os.path.join(ROOT, 'pyq', '*', '*', 'traps.csv'))):
        year, shift = os.path.normpath(path).split(os.sep)[-3:-1]
        bad += verify(year, shift)
    if bad:
        print(f'{bad} problems in the trap analysis'); sys.exit(1)
    print('OK: all trap rows valid')


if __name__ == '__main__':
    main()
