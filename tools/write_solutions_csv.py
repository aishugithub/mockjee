"""
Write pyq/<year>/<shift>/solutions.csv from a Python data file, so long solution texts are easy to
author without CSV quoting. Format and tone: tools/SOLUTION_STYLE.md.

The data file defines S = {q: (claude_answer, check, hint1, hint2, solution, concept, revise, note), ...}
for q = 1..75 (questions NTA dropped may be left out).

Usage:  python tools/write_solutions_csv.py <data.py> pyq/<year>/<shift>
"""
import csv, importlib.util, json, os, sys

COLS = ['q', 'claude_answer', 'check', 'hint1', 'hint2', 'solution', 'concept', 'revise', 'note']


def main():
    data, folder = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location('sol_data', data)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    qs = json.load(open(os.path.join(folder, 'questions.json'), encoding='utf-8'))['questions']
    need = {n for n, q in enumerate(qs, 1) if not q.get('exclude') and q.get('answer') is not None}
    missing = sorted(need - set(m.S))
    if missing:
        sys.exit(f'missing solutions for Q{missing}')
    with open(os.path.join(folder, 'solutions.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for q in sorted(m.S):
            row = m.S[q]
            assert len(row) == 8, f'Q{q}: expected 8 fields, got {len(row)}'
            w.writerow([q, str(row[0])] + [str(x).strip() for x in row[1:]])
    print(f'{len(m.S)} solutions -> {folder}/solutions.csv')


if __name__ == '__main__':
    main()
