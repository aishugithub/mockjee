"""
Bundle every extracted paper under pyq/<year>/<shift>/questions.json into
pyq_bank.js (window.JEE_PYQ_BANK), which index.html loads as the built-in bank.

Questions NTA dropped, or whose final key has no single answer, are left out
(they stay listed in each paper's review.csv).

Worked solutions come from pyq/<year>/<shift>/solutions.csv (Claude's, labelled as such; see
tools/verify_pyq_solutions.py). Chapter tags come from pyq/<year>/<shift>/tags.csv (written by Claude after reading each
question image; see tools/chapters.py). They are kept apart from questions.json so that
re-running the extractor never wipes them. Every code is checked against the official list
and against the question's subject from NTA's paper.

Usage:  python tools/build_pyq_bank.py
"""
import csv, glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapters import CODES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP = ['id', 'subject', 'chapter', 'subtopic', 'secondary_chapter', 'tag_confidence', 'year', 'type',
        'source', 'question', 'image', 'options', 'option_images', 'answer', 'accept', 'solution',
        'solution_by', 'solution_check', 'solution_note', 'hints', 'concept', 'revise']
CHECKS = ('sympy', 'arithmetic', 'conceptual')
HELD = []   # solutions Claude disputes with NTA's key: not bundled until the owner decides


def load_tags(folder, questions):
    """{question id: tag fields} from tags.csv (q = question number in the paper)."""
    path = os.path.join(folder, 'tags.csv')
    if not os.path.exists(path):
        return {}
    tags, errors = {}, []
    for row in csv.DictReader(open(path, encoding='utf-8')):
        n = int(row['q']); q = questions[n - 1]
        code, sec = row['chapter'].strip(), (row.get('secondary') or '').strip()
        if code not in CODES:
            errors.append(f'Q{n}: unknown chapter code {code}'); continue
        subj, chap = CODES[code]
        if subj != q['subject']:
            errors.append(f"Q{n}: code {code} is {subj} but NTA lists the question under {q['subject']}"); continue
        t = {'chapter': chap, 'subtopic': row['subtopic'].strip(),
             'tag_confidence': row['confidence'].strip()}
        if sec:
            if sec not in CODES:
                errors.append(f'Q{n}: unknown secondary code {sec}'); continue
            t['secondary_chapter'] = CODES[sec][1]
        if t['tag_confidence'] not in ('high', 'low'):
            errors.append(f'Q{n}: confidence must be high or low')
        tags[q['id']] = t
    if errors:
        raise SystemExit(f'{path}:' + ''.join('\n  ' + e for e in errors))
    return tags

def load_solutions(folder, questions):
    """{question id: solution fields} from solutions.csv (Claude's worked solutions, step 2).

    A solution is only bundled when Claude's answer equals NTA's final key; a disagreement
    stops the build so it gets flagged to the owner instead of shipping a contradicting solution.
    """
    path = os.path.join(folder, 'solutions.csv')
    if not os.path.exists(path):
        return {}
    sols, errors = {}, []
    for row in csv.DictReader(open(path, encoding='utf-8')):
        n = int(row['q']); q = questions[n - 1]
        if q.get('exclude') or q.get('answer') is None:
            continue
        key = q['answer'] + 1 if q['type'] == 'MCQ' else q['answer']
        if row['check'] == 'disputed':
            HELD.append(f"{q['source']}: Claude gets {row['claude_answer']}, NTA's final key {key}")
            continue
        ok = [key] + ([a + 1 for a in q.get('accept', [])] if q['type'] == 'MCQ' else q.get('accept', []))
        if not any(float(row['claude_answer']) == float(a) for a in ok):
            errors.append(f"Q{n}: Claude's answer {row['claude_answer']} differs from NTA's final key {key}: flag it for the owner"); continue
        if row['check'] not in CHECKS:
            errors.append(f'Q{n}: check must be one of {CHECKS}'); continue
        s = {'solution': row['solution'].strip(), 'solution_by': 'claude', 'solution_check': row['check']}
        if row.get('note', '').strip():
            s['solution_note'] = row['note'].strip()
        hints = [row.get(h, '').strip() for h in ('hint1', 'hint2') if row.get(h, '').strip()]
        if hints:
            s['hints'] = hints
        for k in ('concept', 'revise'):
            if row.get(k, '').strip():
                s[k] = row[k].strip()
        sols[q['id']] = s
    if errors:
        raise SystemExit(f'{path}:' + ''.join('\n  ' + e for e in errors))
    return sols

sys.stdout.reconfigure(encoding='utf-8')
bank, skipped, papers = [], [], []
for path in sorted(glob.glob(os.path.join(ROOT, 'pyq', '*', '*', 'questions.json'))):
    folder = os.path.relpath(os.path.dirname(path), ROOT).replace(os.sep, '/')
    paper = json.load(open(path, encoding='utf-8'))
    tags = load_tags(os.path.dirname(path), paper['questions'])
    sols = load_solutions(os.path.dirname(path), paper['questions'])
    untagged = 0
    n = 0
    for q in paper['questions']:
        if q.get('exclude'):
            skipped.append(f"{q['source']}: {q['exclude']}"); continue
        if q.get('answer') is None:
            skipped.append(f"{q['source']}: no answer"); continue
        q = dict(q, **tags.get(q['id'], {}), **sols.get(q['id'], {}))
        if q['id'] not in tags: untagged += 1
        r = {k: q[k] for k in KEEP if k in q}
        if 'image' in r: r['image'] = f"{folder}/{r['image']}"
        if 'option_images' in r: r['option_images'] = [f'{folder}/{p}' if p else '' for p in r['option_images']]
        bank.append(r); n += 1
    papers.append(f"{paper['source']}: {n}" + (f' ({untagged} not tagged yet)' if untagged else '')
                  + (f', {len(sols)} with worked solutions' if sols else ''))

with open(os.path.join(ROOT, 'pyq_bank.js'), 'w', encoding='utf-8') as f:
    f.write('/* Generated by tools/build_pyq_bank.py. Do not edit by hand.\n'
            ' * Official questions from public NTA question papers (images as printed by NTA),\n'
            " * answers from NTA's FINAL answer keys. Sources: sources/<year>/SOURCES.md */\n")
    f.write('window.JEE_PYQ_BANK = ')
    json.dump(bank, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';\n')
print('\n'.join(papers))
if HELD:
    print(f'{len(HELD)} worked solutions held back (Claude disagrees with the key; owner to review):')
    print('\n'.join('  ' + h for h in HELD))
print(f'{len(bank)} questions in pyq_bank.js; left out {len(skipped)}:')
print('\n'.join('  ' + s for s in skipped))
