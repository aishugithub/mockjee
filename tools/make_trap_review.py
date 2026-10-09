"""
Review page for one shift's trap analysis (step 3): each NTA question image, its options, NTA's final key, and for
every wrong option the mistake Claude thinks leads to it, its mistake type and how it was checked.
For the owner or a subject teacher to spot-check before the other shifts. Working aid, not part of the app.

Usage: python tools/make_trap_review.py pyq/<year>/<shift>
       -> writes pyq/<year>/<shift>/traps_review.html (open it straight from disk)
"""
import csv, html, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_solution_review import rich
from traps_common import MISTAKE_TYPES

CHECK = {'sympy': 'wrong path recomputed with SymPy (tools/verify_traps.py)',
         'arithmetic': 'wrong path recomputed by script (tools/verify_traps.py)',
         'conceptual': 'misconception, not computable: teacher to judge'}
LABEL = 'Trap analysis written by Claude; a subject teacher should spot-check it.'


def main():
    folder = sys.argv[1]
    paper = json.load(open(os.path.join(folder, 'questions.json'), encoding='utf-8'))
    rows = {}
    for r in csv.DictReader(open(os.path.join(folder, 'traps.csv'), encoding='utf-8')):
        rows.setdefault(int(r['q']), []).append(r)
    counts = {}
    for rs in rows.values():
        for r in rs:
            counts[r['mistake_type']] = counts.get(r['mistake_type'], 0) + 1
    out = []
    for n, q in enumerate(paper['questions'], 1):
        if q.get('exclude') or q.get('answer') is None:
            out.append(f'<section><h2>Q{n} · {q["subject"]} · ID {q["id"]}</h2><p class="miss">Left out of the bank: '
                       f'{html.escape(q.get("exclude") or "no answer in the final key")} (NTA).</p></section>')
            continue
        mcq = q['type'] == 'MCQ'
        key = q['answer'] + 1 if mcq else q['answer']
        opts = ''.join(f'<div class="opt{" key" if k == key else ""}"><b>({k})</b> <img src="{html.escape(p)}"></div>'
                       for k, p in enumerate(q.get('option_images', []), 1)) if mcq else ''
        trs = ''
        for r in sorted(rows.get(n, []), key=lambda r: float(r['option'])):
            none = r['mistake_type'] == 'none'
            trs += (f'<tr class="{"none" if none else ""}"><td><b>{"(" + r["option"] + ")" if mcq else html.escape(r["option"])}</b></td>'
                    f'<td>{rich(r["trap"])}' + (f'<div class="note">Note: {rich(r["note"])}</div>' if r['note'].strip() else '')
                    + f'</td><td>{MISTAKE_TYPES.get(r["mistake_type"], r["mistake_type"])}</td>'
                    f'<td class="chk">{"–" if none else CHECK.get(r["check"], r["check"])}</td></tr>')
        if trs:
            body = (f'<table><tr><th>{"Option" if mcq else "Trap value"}</th><th>Mistake that leads there</th>'
                    f'<th>Type</th><th>Check</th></tr>{trs}</table>')
        else:
            body = f'<p class="meta">{"No trap rows." if mcq else "No well-known slip value recorded for this numerical."}</p>'
        out.append(f'<section><h2>Q{n} · {q["subject"]} · {"MCQ" if mcq else "Numerical"} · ID {q["id"]} · '
                   f'NTA final key: {key}</h2><img class="q" src="{html.escape(q["image"])}">{opts}{body}</section>')
    summary = ', '.join(f'{MISTAKE_TYPES.get(k, k)}: {v}' for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
    page = f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trap review: {html.escape(paper["source"])}</title>
<style>body{{font:15px/1.5 system-ui,sans-serif;max-width:900px;margin:20px auto;padding:0 16px;color:#1d2733;background:#fff}}
section{{border-top:2px solid #d5dce6;padding:10px 0 18px}}h2{{font-size:15px;color:#40506a}}img.q{{max-width:100%}}
.opt{{display:inline-block;margin:4px 16px 4px 0;padding:2px 6px;border-radius:4px}}.opt img{{max-width:100%}}
.opt.key{{background:#e3f4e1;outline:1px solid #8fca88}}
table{{border-collapse:collapse;width:100%;margin-top:8px;font-size:14px}}td,th{{border:1px solid #d5dce6;padding:4px 8px;vertical-align:top;text-align:left}}
th{{background:#f0f3f8}}tr.none td{{color:#7a8594}}.chk{{font-size:12px;color:#5a6676}}.meta{{font-size:13px;color:#5a6676}}
.note{{font-size:12px;color:#7a5a12;font-style:italic}}.miss{{color:#b00020}}.label{{background:#fff8e6;border-left:3px solid #e2b33b;padding:6px 10px}}</style>
<h1>{html.escape(paper["source"])}: trap analysis for review</h1>
<p class="label"><b>{LABEL}</b> It is not NTA’s. Questions and options are NTA’s own images; the green option is NTA’s
final key. For each wrong option the row names the specific mistake that lands on it. “No clear mistake path” means
Claude found no real route to that option and did not invent one. Please mark any trap that is wrong or far-fetched.</p>
<p class="meta">{sum(len(v) for v in rows.values())} rows · {summary}</p>
{"".join(out)}'''
    path = os.path.join(folder, 'traps_review.html')
    open(path, 'w', encoding='utf-8').write(page)
    print(path)


if __name__ == '__main__':
    main()
