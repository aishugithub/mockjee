"""
Write pyq/<year>/<shift>/traps.csv from a Python data file (kept outside the repo), like
write_solutions_csv.py does for solutions. Format: tools/traps_common.py and CLAUDE.md step 3.

The data file defines T = {q: {option: (trap, mistake_type, check, note), ...}, ...}
  - MCQ: option is 1-4 and EVERY wrong option needs a row; when no real mistake leads to it, write
    ('No clear mistake path', 'none', 'conceptual', ''). Never a row for the key.
  - Numerical: option is the trap value; add rows only for well-known slips (questions may be left out).

Usage:  python tools/write_traps_csv.py <data.py> pyq/<year>/<shift>
"""
import csv, importlib.util, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from traps_common import CHECKS, COLS, MISTAKE_TYPES, NO_PATH


def main():
    data, folder = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location('trap_data', data)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    qs = json.load(open(os.path.join(folder, 'questions.json'), encoding='utf-8'))['questions']
    errors, rows = [], []
    for n, q in enumerate(qs, 1):
        if q.get('exclude') or q.get('answer') is None:
            if n in m.T: errors.append(f'Q{n}: left out of the bank, so no traps')
            continue
        traps = m.T.get(n, {})
        if q['type'] == 'MCQ':
            right = {q['answer'] + 1} | {a + 1 for a in q.get('accept', [])}
            missing = sorted({1, 2, 3, 4} - right - set(traps))
            if missing: errors.append(f'Q{n}: no row for wrong option(s) {missing}')
        else:
            right = {q['answer']} | set(q.get('accept', []))
        for opt, row in sorted(traps.items()):
            if len(row) != 4:
                errors.append(f'Q{n} option {opt}: expected 4 fields, got {len(row)}'); continue
            trap, mt, check, note = (str(v).strip() for v in row)
            if any(float(opt) == float(r) for r in right): errors.append(f'Q{n}: option {opt} is the key, it cannot have a trap')
            if mt not in MISTAKE_TYPES: errors.append(f'Q{n} option {opt}: unknown mistake_type {mt}')
            if check not in CHECKS: errors.append(f'Q{n} option {opt}: check must be one of {CHECKS}')
            if not trap: errors.append(f'Q{n} option {opt}: empty trap text')
            if (mt == 'none') != (trap == NO_PATH): errors.append(f"Q{n} option {opt}: mistake_type none goes with '{NO_PATH}' only")
            rows.append([n, opt, trap, mt, check, note])
    if errors:
        sys.exit('\n'.join(errors))
    with open(os.path.join(folder, 'traps.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(COLS)
        w.writerows(rows)
    print(f'{len(rows)} trap rows -> {folder}/traps.csv')


if __name__ == '__main__':
    main()
