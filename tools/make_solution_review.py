"""
Review page for one shift's worked solutions (step 2): each NTA question image, its options,
NTA's final-key answer, Claude's solution, how the answer was checked, and any note.
For the owner or a subject teacher to read before the next batch. Working aid, not part of the app.

Usage: python tools/make_solution_review.py pyq/<year>/<shift>
       -> writes pyq/<year>/<shift>/solutions_review.html (open it straight from disk)
"""
import csv, html, json, os, re, sys

CHECK = {'sympy': 'Answer recomputed with SymPy (tools/verify_pyq_solutions.py)',
         'arithmetic': 'Answer recomputed by script (tools/verify_pyq_solutions.py)',
         'conceptual': 'Theory question: not computable, needs a teacher’s review'}


def rich(s):
    s = html.escape(s)
    s = re.sub(r'\^\{([^}]*)\}', r'<sup>\1</sup>', s)
    s = re.sub(r'_\{([^}]*)\}', r'<sub>\1</sub>', s)
    return s.replace('\n', '<br>')


def main():
    folder = sys.argv[1]
    paper = json.load(open(os.path.join(folder, 'questions.json'), encoding='utf-8'))
    sols = {int(r['q']): r for r in csv.DictReader(open(os.path.join(folder, 'solutions.csv'), encoding='utf-8'))}
    out = []
    for n, q in enumerate(paper['questions'], 1):
        s = sols.get(n)
        key = q['answer'] + 1 if q['type'] == 'MCQ' else q['answer']
        opts = ''.join(f'<div class="opt{" key" if q["type"] == "MCQ" and k == key else ""}"><b>({k})</b> <img src="{html.escape(p)}"></div>'
                       for k, p in enumerate(q.get('option_images', []), 1))
        if not s:
            body = '<p class="miss">No solution written yet.</p>'
        else:
            agree = str(key) == s['claude_answer'] or (q['type'] != 'MCQ' and float(key) == float(s['claude_answer']))
            extra = ''.join(f'<p class="hint"><b>{lab}:</b> {rich(s[k])}</p>' for k, lab in
                            (('hint1', 'Hint 1'), ('hint2', 'Hint 2'), ('concept', 'What this tests')) if s.get(k))
            body = (extra + f'<div class="sol">{rich(s["solution"])}</div>'
                    + (f'<p class="hint"><b>If this felt hard:</b> {rich(s["revise"])}</p>' if s.get('revise') else '')
                    + f'<p class="meta">Claude’s answer: <b>{html.escape(s["claude_answer"])}</b> · NTA final key: <b>{key}</b> · '
                    f'{"agrees" if agree else "<span class=bad>DISAGREES: flag for the owner</span>"} · {CHECK.get(s["check"], s["check"])}</p>'
                    + (f'<p class="note">Note: {html.escape(s["note"])}</p>' if s.get('note') else ''))
        out.append(f'<section><h2>Q{n} · {q["subject"]} · {"MCQ" if q["type"] == "MCQ" else "Numerical"} · ID {q["id"]}</h2>'
                   f'<img class="q" src="{html.escape(q["image"])}">{opts}{body}</section>')
    page = f'''<!doctype html><meta charset="utf-8"><title>Solutions review: {html.escape(paper["source"])}</title>
<style>body{{font:15px/1.5 system-ui,sans-serif;max-width:900px;margin:20px auto;padding:0 16px;color:#1d2733}}
section{{border-top:2px solid #d5dce6;padding:10px 0 18px}}h2{{font-size:15px;color:#40506a}}img.q{{max-width:100%}}
.opt{{display:inline-block;margin:4px 16px 4px 0;padding:2px 6px;border-radius:4px}}.opt.key{{background:#e3f4e1;outline:1px solid #8fca88}}
.sol{{background:#f6f8fb;border-radius:6px;padding:8px 12px;margin-top:8px}}.meta{{font-size:13px;color:#5a6676}}
.note{{font-size:13px;color:#7a5a12;font-style:italic}}.bad{{color:#b00020;font-weight:bold}}.miss{{color:#b00020}}.hint{{background:#fff8e6;border-left:3px solid #e2b33b;padding:4px 10px;margin:6px 0}}</style>
<h1>{html.escape(paper["source"])}: worked solutions for review</h1>
<p>Questions and options are NTA’s own images; the green option is NTA’s final key. Every solution below was written by Claude
and checked against NTA’s final key. It is not NTA’s solution. Please mark anything unclear or wrong.</p>
{"".join(out)}'''
    path = os.path.join(folder, 'solutions_review.html')
    open(path, 'w', encoding='utf-8').write(page)
    print(path)


if __name__ == '__main__':
    main()
