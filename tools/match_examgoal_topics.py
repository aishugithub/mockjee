"""
Give each question of an NTA shift (pyq/<year>/<shift>) its ExamGOAL chapter ("topic"), by finding the
same question in ExamGOAL's copy of that paper. NTA's question images are read with the Windows OCR
engine (tools/win_ocr.ps1) and matched by text to ExamGOAL's question stems, one-to-one within a
subject and question type. Each match is then checked by its answer:
  - numerical: ExamGOAL's key must equal NTA's final key
  - MCQ: ExamGOAL's letter must equal NTA's option position (ExamGOAL usually keeps NTA's option order)
A match is kept only if the text match is good and both texts are 40+ characters, or the answer agrees and
the match is fair, or the question was the only one left in its subject and type (a figure with little text)
and the answer agrees. An MCQ answer agreement only counts where ExamGOAL keeps NTA's option order.

Writes pyq/<year>/<shift>/topics.csv: q,topic,examside_id,match,answer_check
build_pyq_bank.py adds `topic` from it. Rows with an empty topic were not matched confidently.

Usage:  python tools/match_examgoal_topics.py pyq/<year>/<shift> <examgoal paper.pdf>
"""
import csv, difflib, json, os, re, subprocess, sys, tempfile, shutil

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_examgoal_paper import fetch_titles, parse_key
from examgoal_chapters import unit_for
from chapters import CODES

SUBJECTS = ('Chemistry', 'Mathematics', 'Physics')
GOOD, FAIR = 0.60, 0.35


def norm(t):
    return re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()


def examgoal_questions(pdf):
    """[(num, subject, type, stem text, examside id)] from an ExamGOAL paper."""
    out, subject = [], None
    for page in pdf:
        links = [(k['from'].y0, re.search(r'/question/([A-Za-z0-9]+)', k['uri']).group(1)) for k in page.get_links()
                 if 'examside.com' in k.get('uri', '') and 'utm_medium' not in k['uri']]
        blocks = page.get_text('dict', flags=pymupdf.TEXTFLAGS_TEXT)['blocks']
        lines = sorted(((l['bbox'][1], l['bbox'][0], ''.join(s['text'] for s in l['spans']).strip())
                        for b in blocks for l in b['lines']), key=lambda x: (round(x[0]), x[1]))
        cur = None
        for y, x, t in lines:
            if t in SUBJECTS and x < 60:
                subject = t
            m = re.match(r'^Q(\d+)\.$', t)
            if m and x < 60:
                lid = min(links, key=lambda k: abs(k[0] - y), default=(0, None))
                cur = {'num': int(m.group(1)), 'subject': subject, 'text': [], 'type': None,
                       'qid': lid[1] if abs(lid[0] - y) < 60 else None, 'y': y}
                out.append(cur); continue
            if cur is None or x > 505:
                continue
            if cur['type'] is None and abs(y - cur['y']) < 4:
                cur['type'] = 'NUM' if 'Numerical' in t else 'MCQ'
                sm = re.search(r'·\s*(Chemistry|Mathematics|Physics)', t)
                if sm: cur['subject'] = sm.group(1)
                continue
            if re.match(r'^\(A\)', t):
                cur['stop'] = True
            if not cur.get('stop') and not t.startswith('Keep practising') and 'pdf.questions.examgoal.com' not in t:
                cur['text'].append(t)
    for q in out:
        q['text'] = norm(' '.join(q['text']))
    return out


def ocr_images(paths):
    tmp = tempfile.mkdtemp(prefix='ntaq')
    for p in paths:
        shutil.copy(p, os.path.join(tmp, os.path.basename(p)))
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                    os.path.join(os.path.dirname(__file__), 'win_ocr.ps1'), '-Folder', tmp], check=True, capture_output=True)
    out = {}
    for p in paths:
        j = os.path.join(tmp, os.path.basename(p)[:-4] + '.json')
        lines = json.load(open(j, encoding='utf-8-sig')) or []
        out[p] = norm(' '.join(l['text'] for l in lines))
    shutil.rmtree(tmp, ignore_errors=True)
    return out


def main():
    folder, eg_pdf = sys.argv[1], sys.argv[2]
    qs = json.load(open(os.path.join(folder, 'questions.json'), encoding='utf-8'))['questions']
    tp = os.path.join(folder, 'tags.csv')      # our own NTA-unit tags, for the cross-check
    if os.path.exists(tp):
        for row in csv.DictReader(open(tp, encoding='utf-8')):
            qs[int(row['q']) - 1]['chapter'] = CODES[row['chapter'].strip()][1]
    pdf = pymupdf.open(eg_pdf)
    eg = examgoal_questions(pdf)
    key = parse_key(pdf)
    texts = ocr_images([os.path.join(folder, q['image']) for q in qs if q.get('image')])
    titles = fetch_titles([e['qid'] for e in eg if e['qid']], os.path.join(os.path.dirname(eg_pdf), 'examside_titles.json'))

    pairs = []
    for i, q in enumerate(qs):
        t = texts.get(os.path.join(folder, q.get('image', '')), '')
        for j, e in enumerate(eg):
            if e['subject'] != q['subject'] or e['type'] != q['type']:
                continue
            pairs.append((difflib.SequenceMatcher(None, t, e['text']).ratio(), i, j))
    pairs.sort(reverse=True)
    took_q, took_e, match = set(), set(), {}
    for r, i, j in pairs:
        if i in took_q or j in took_e:
            continue
        took_q.add(i); took_e.add(j); match[i] = (j, r)

    # does ExamGOAL keep NTA's option order in this paper? (key letter at NTA's key position for 90%+ of MCQs)
    pos = []
    for i, (j, r) in match.items():
        q, k = qs[i], key.get(eg[j]['num'], '')
        if q['type'] == 'MCQ' and q.get('answer') is not None and r >= GOOD:
            pos.append(any('ABCD'.index(x.strip()) in ({q['answer']} | set(q.get('accept', [])))
                           for x in k.split(',') if x.strip() and x.strip() in 'ABCD'))
    same_order = len(pos) >= 20 and sum(pos) / len(pos) >= 0.9

    rows, stats = [], {'kept': 0, 'dropped': 0, 'agree': 0, 'disagree': 0, 'unit_mismatch': []}
    for i, q in enumerate(qs):
        n = i + 1
        if i not in match:
            rows.append({'q': n, 'topic': '', 'examside_id': '', 'match': 0, 'answer_check': 'no candidate'}); stats['dropped'] += 1; continue
        j, r = match[i]
        e = eg[j]
        k = key.get(e['num'], '')
        if q.get('answer') is None:
            check = 'no NTA answer'
        elif q['type'] == 'MCQ':
            right = {q['answer']} | set(q.get('accept', []))
            letters = [x.strip() for x in k.split(',') if x.strip() in 'ABCD' and x.strip()]
            check = 'agree' if letters and any('ABCD'.index(x) in right for x in letters) else f'differs (ExamGOAL {k})'
        else:
            vals = [q['answer']] + list(q.get('accept', []))
            try:
                ek = [float(v) for v in re.split(r'\s+or\s+', k)]
                check = 'agree' if any(abs(float(a) - b) < 1e-6 for a in vals for b in ek) else f'differs (ExamGOAL {k})'
            except ValueError:
                check = f'differs (ExamGOAL {k})'
        stats['agree' if check == 'agree' else 'disagree'] += 1
        title = titles.get(e['qid'] or '', '')
        parts = [p.strip() for p in title.split('|')]
        topic = re.sub(r'\s+Question\s+\d+$', '', parts[1]) if len(parts) >= 3 else ''
        weak_in_group = sum(1 for ii, (jj, rr) in match.items() if rr < FAIR
                            and qs[ii]['subject'] == q['subject'] and qs[ii]['type'] == q['type'])
        forced = r < FAIR and weak_in_group == 1      # the only question left in its subject and type
        if len(parts) >= 3 and parts[2] != q['subject']:
            topic = ''                                # ExamSIDE files it under another subject: not the same question
        # Mostly-formula stems leave little text ("if then is equal to"), and two such scraps can look alike,
        # so a short text never counts as a good match on its own. An answer check is evidence for a numerical,
        # and for an MCQ only where ExamGOAL keeps NTA's option order (shuffled copies agree by chance).
        t = texts.get(os.path.join(folder, q.get('image', '')), '')
        short = min(len(t), len(e['text'])) < 40
        evidence = check == 'agree' and (q['type'] == 'NUM' or same_order)
        keep = topic and ((r >= GOOD and not short) or (r >= FAIR and evidence) or (forced and evidence))
        if keep:
            stats['kept'] += 1
            try:
                code, _ = unit_for(q['subject'], topic)
                if q.get('chapter') not in (CODES[code][1], 'Not in current syllabus'):
                    stats['unit_mismatch'].append(f"Q{n}: our tag {q.get('chapter')!r}, ExamGOAL {topic!r}")
            except KeyError:
                stats['unit_mismatch'].append(f'Q{n}: unknown ExamGOAL chapter {topic!r}')
        else:
            stats['dropped'] += 1
        rows.append({'q': n, 'topic': topic if keep else '', 'examside_id': e['qid'] or '', 'match': round(r, 2), 'answer_check': check})

    with open(os.path.join(folder, 'topics.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['q', 'topic', 'examside_id', 'match', 'answer_check']); w.writeheader(); w.writerows(rows)
    print(f"{'(same option order) ' if same_order else ''}{folder}: topics for {stats['kept']}/{len(qs)}; answers agree {stats['agree']}, differ {stats['disagree']}; "
          f"our NTA-unit tag differs from ExamGOAL's chapter for {len(stats['unit_mismatch'])}")
    for m in stats['unit_mismatch']:
        print('   ', m)


if __name__ == '__main__':
    main()
