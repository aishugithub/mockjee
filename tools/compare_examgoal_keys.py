"""
Compare ExamGOAL's answer key with NTA's final key, question by question, for an NTA shift we also
have from ExamGOAL (sources/examgoal_nta/). The question pairs come from topics.csv
(tools/match_examgoal_topics.py).

MCQs: where ExamGOAL keeps NTA's option order in a paper (its key letter is at NTA's key position for
90%+ of 20+ MCQs; a shuffled candidate copy manages about 25%), positions are compared directly.
Otherwise the options are compared by CONTENT: both sides' option images are read with the Windows OCR
engine (tools/win_ocr.ps1, images enlarged 3x first) and matched by text. A pairing counts only when both
texts have 5+ characters and the match is clear (ratio >= 0.95 and at least 0.3 better than any other
option), and only if at least two options of the question pair; with three paired the fourth follows.
An MCQ whose keyed option cannot be paired is "not compared". Numericals are compared by value
("x or y" keys accept either).
OCR drops +/- signs and mangles formulas, so this is only a first pass: every "differs" must be checked
by eye (the `checked` column) before the app shows it.

Writes pyq/<year>/<shift>/key_compare.csv: q,type,examside_id,nta_key,examgoal_key,status,how,checked
  nta_key / examgoal_key: MCQ option numbers as NTA prints them (1-4), or the numerical value
  status: agree | differs | not compared
  checked: the by-eye verdict on a "differs" row (both images side by side), kept when the script is rerun:
    confirmed = same question, the keys really differ | wrong_pair = not the same question |
    wrong_mapping = ExamGOAL's keyed option is in fact NTA's key | text_differs = ExamGOAL's copy changed the question
build_pyq_bank.py adds `examgoal_key_differs` only where status is "differs" AND checked is "confirmed"; the app shows it
in the answer review. NTA's final key stays the answer; a difference only means "look again".

Usage:  python tools/compare_examgoal_keys.py pyq/<year>/<shift> sources/examgoal_nta/<slug>.pdf [folder to keep ExamGOAL's images]
Every "differs" must be checked by eye (both images side by side) before it is shown: a wrong pairing gives a false difference.
"""
import csv, difflib, itertools, json, os, re, shutil, subprocess, sys, tempfile

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SURE, MARGIN = 0.95, 0.3   # strict: OCR drops +/- signs and mangles superscripts, so near-identical options must not pair


def norm(t):
    return re.sub(r'[^a-z0-9]+', '', t.lower())


def ocr(paths):
    """{path: normalised text} for images, enlarged 3x with a white border (small option images read badly otherwise)."""
    tmp = tempfile.mkdtemp(prefix='optocr')
    names = {}
    for i, p in enumerate(paths):
        im = Image.open(p).convert('L')
        im = ImageOps.expand(im.resize((im.width * 3, im.height * 3), Image.LANCZOS), 60, fill=255)
        im.save(os.path.join(tmp, f'{i}.png')); names[p] = i
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', os.path.join(HERE, 'win_ocr.ps1'),
                    '-Folder', tmp], check=True, capture_output=True)
    out = {}
    for p, i in names.items():
        lines = json.load(open(os.path.join(tmp, f'{i}.json'), encoding='utf-8-sig')) or []
        out[p] = norm(' '.join(l['text'] for l in lines))
    shutil.rmtree(tmp, ignore_errors=True)
    return out


def pair_options(eg_txt, nta_txt):
    """{examgoal option index: NTA option index} for the options whose text clearly matches."""
    # short strings (OCR often keeps only part of a formula, e.g. "24" of 5π/24) cannot be told apart reliably
    sim = [[difflib.SequenceMatcher(None, a, b).ratio() if len(a) >= 5 and len(b) >= 5 else 0 for b in nta_txt] for a in eg_txt]
    m = {}
    for i in range(4):
        j = max(range(4), key=lambda j: sim[i][j])
        others = [sim[i][k] for k in range(4) if k != j] + [sim[k][j] for k in range(4) if k != i]
        if sim[i][j] >= SURE and sim[i][j] - max(others) >= MARGIN:
            m[i] = j
    if len(set(m.values())) != len(m) or len(m) < 2:      # one lone pairing may be a coincidence
        return {}
    if len(m) == 3:
        m[({0, 1, 2, 3} - set(m)).pop()] = ({0, 1, 2, 3} - set(m.values())).pop()
    return m


def main():
    folder, eg_pdf = sys.argv[1], sys.argv[2]
    qs = json.load(open(os.path.join(folder, 'questions.json'), encoding='utf-8'))['questions']
    pairs = [r for r in csv.DictReader(open(os.path.join(folder, 'topics.csv'), encoding='utf-8'))
             if r['examside_id'] and (r['topic'] or float(r['match']) >= 0.35)]
    keep = sys.argv[3] if len(sys.argv) > 3 else None     # optional: keep ExamGOAL's cut images here for checking by eye
    tmp = keep or tempfile.mkdtemp(prefix='egcopy')
    if not (keep and os.path.exists(os.path.join(tmp, 'questions.json'))):      # a kept copy is reused
        subprocess.run([sys.executable, os.path.join(HERE, 'extract_examgoal_paper.py'), eg_pdf, tmp, '', str(qs[0]['year'])],
                       check=True, capture_output=True)
    eg = {q['id'][3:]: q for q in json.load(open(os.path.join(tmp, 'questions.json'), encoding='utf-8'))['questions']}

    work = []
    for r in pairs:
        q, e = qs[int(r['q']) - 1], eg.get(r['examside_id'])
        if e and q.get('answer') is not None and not q.get('exclude') and q['type'] == e['type'] == 'MCQ' \
                and len(q.get('option_images', [])) == 4 and len(e.get('option_images', [])) == 4:
            work.append((r, q, e))
    imgs = [os.path.join(folder, p) for _, q, _ in work for p in q['option_images']] + \
           [os.path.join(tmp, p) for _, _, e in work for p in e['option_images']]
    txt = ocr(imgs)
    maps = {}
    for r, q, e in work:
        maps[r['q']] = pair_options([txt[os.path.join(tmp, p)] for p in e['option_images']],
                                    [txt[os.path.join(folder, p)] for p in q['option_images']])
    # Does ExamGOAL keep NTA's option order in this paper? Then its key letter sits at NTA's key position for
    # nearly every MCQ (a shuffled copy agrees by position only about a quarter of the time).
    pos = [bool(({e['answer']} | set(e.get('accept', []))) & ({q['answer']} | set(q.get('accept', []))))
           for _, q, e in work if e.get('answer') is not None and not e.get('exclude')]
    same_order = len(pos) >= 20 and sum(pos) / len(pos) >= 0.9

    rows = []
    for r in pairs:
        q, e = qs[int(r['q']) - 1], eg.get(r['examside_id'])
        row = {'q': r['q'], 'type': q['type'], 'examside_id': r['examside_id'], 'nta_key': '', 'examgoal_key': '',
               'status': 'not compared', 'how': ''}
        if q.get('answer') is None or q.get('exclude'):
            row['how'] = 'no NTA answer'; rows.append(row); continue
        if not e or e.get('answer') is None or e.get('exclude'):
            row['how'] = 'no usable ExamGOAL key'; rows.append(row); continue
        if q['type'] == 'NUM':
            nta = [q['answer']] + list(q.get('accept', [])); egk = [e['answer']] + list(e.get('accept', []))
            row.update(nta_key=' or '.join(f'{v:g}' for v in nta), examgoal_key=' or '.join(f'{v:g}' for v in egk), how='numerical value',
                       status='agree' if any(abs(a - b) < 1e-6 for a in nta for b in egk) else 'differs')
            rows.append(row); continue
        nta = {q['answer']} | set(q.get('accept', []))
        egk = {e['answer']} | set(e.get('accept', []))
        m = maps.get(r['q'], {})
        if same_order:
            mapped, how = egk, "ExamGOAL keeps NTA's option order in this paper"
        elif egk <= set(m):
            mapped, how = {m[i] for i in egk}, 'options paired by text'
        else:
            row.update(nta_key=','.join(str(a + 1) for a in sorted(nta)), how='options could not be paired')
            rows.append(row); continue
        row.update(nta_key=','.join(str(a + 1) for a in sorted(nta)), examgoal_key=','.join(str(a + 1) for a in sorted(mapped)),
                   how=how, status='agree' if mapped & nta else 'differs')
        rows.append(row)
    if not keep:
        shutil.rmtree(tmp, ignore_errors=True)

    path = os.path.join(folder, 'key_compare.csv')
    prev = list(csv.DictReader(open(path, encoding='utf-8'))) if os.path.exists(path) else []
    old = {(r['q'], r['examside_id'], r['nta_key'], r['examgoal_key']): r.get('checked', '') for r in prev}
    for r in rows:
        r['checked'] = old.get((r['q'], r['examside_id'], r['nta_key'], r['examgoal_key']), '') if r['status'] == 'differs' else ''
    # a difference confirmed by eye stays even if this (stricter) run can no longer pair the options itself
    sure = {(r['q'], r['examside_id']): r for r in prev if r['status'] == 'differs' and r.get('checked') == 'confirmed'}
    rows = [dict(sure[(r['q'], r['examside_id'])]) if r['status'] == 'not compared' and (r['q'], r['examside_id']) in sure
            else r for r in rows]
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    c = {s: sum(r['status'] == s for r in rows) for s in ('agree', 'differs', 'not compared')}
    print(f"{folder}: agree {c['agree']}, differs {c['differs']}, not compared {c['not compared']}"
          f"{' (same option order)' if same_order else ''}")
    for r in rows:
        if r['status'] == 'differs':
            print(f"    Q{r['q']} {r['type']}: NTA {r['nta_key']}, ExamGOAL {r['examgoal_key']} ({r['how']}) {r['checked'] or 'NOT CHECKED BY EYE YET'}")


if __name__ == '__main__':
    main()
