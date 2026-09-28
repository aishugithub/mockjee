"""
Extract questions from an official NTA JEE Main question-paper PDF and match
them to NTA's FINAL answer key by question ID.

NTA papers print every question and option as a picture; only the question IDs
and option IDs are text. So this script does not try to read the questions: it
saves NTA's own embedded images unchanged (native pixels) and records which
option ID is correct according to the final key.

Usage:
  python tools/extract_nta_paper.py <paper.pdf> <final_key.pdf> <out_dir> "<source label>" <year>

Writes into <out_dir>:
  img/<qid>.png, img/<qid>_o1.png .. _o4.png   question and option images
  questions.json                               records for the app (see README)
  review.csv                                   one row per question for the owner's check
"""
import csv, io, json, os, re, sys

import pymupdf
from PIL import Image

HEADER = re.compile(r'Question Number : (\d+) Question Id : (\d+) Question Type : (\w+)')
SECTION = re.compile(r'(Mathematics|Physics|Chemistry) Section ([AB])\b')
OPTION_ID = re.compile(r'^(\d{6,})\.$')


OCR_DPI = 200


def ocr_pages(pdf):
    """OCR text lines for papers saved with "Print to PDF" (no text layer; the question and
    option pictures are still NTA's embedded images). Uses the Windows OCR engine via
    win_ocr.ps1. Returns {page_no: [(text, bbox in PDF points)]}, or {} if the PDF has text."""
    if any(p.get_text().strip() for p in pdf):
        return {}
    import subprocess, tempfile
    tmp = tempfile.mkdtemp(prefix='ntaocr')
    for pno, page in enumerate(pdf):
        page.get_pixmap(dpi=OCR_DPI).save(os.path.join(tmp, f'p{pno:04d}.png'))
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                    os.path.join(os.path.dirname(__file__), 'win_ocr.ps1'), '-Folder', tmp], check=True)
    s = 72 / OCR_DPI
    out = {}
    for pno in range(len(pdf)):
        with open(os.path.join(tmp, f'p{pno:04d}.json'), encoding='utf-8-sig') as f:
            lines = json.load(f) or []
        out[pno] = []
        for l in lines:
            t = l['text'].replace('Question ld', 'Question Id')
            t = re.sub(r'(?<=\d)[Oo]|[Oo](?=\d)', '0', t)          # O read for 0 inside numbers
            t = re.sub(r'Instruction Time : [Oo]\b', 'Instruction Time : 0', t)
            bb = (l['x'] * s, l['y'] * s, (l['x'] + l['w']) * s, (l['y'] + l['h']) * s)
            label = re.match(r'(\d[\d ]{8,}\d)\s*(?:\.|(?=\s|$))', t)
            if label and bb[0] < 40:   # option-ID label: OCR may drop the ".", split digits, or run on into the option's text
                t = label.group(1).replace(' ', '') + '.'
            out[pno].append((t, bb))
        # OCR sometimes splits a question header into pieces on one line: join them back
        heads = [x for x in out[pno] if x[0].startswith('Question Number')]
        for h in heads:
            parts = sorted((x for x in out[pno] if abs(x[1][1] - h[1][1]) < 4), key=lambda x: x[1][0])
            if len(parts) > 1:
                bb = (parts[0][1][0], min(p[1][1] for p in parts), parts[-1][1][2], max(p[1][3] for p in parts))
                out[pno] = [x for x in out[pno] if x not in parts] + [(' '.join(p[0] for p in parts), bb)]
        fixed = []
        for t, bb in out[pno]:
            if t.startswith('Question Number'):
                t = re.sub(r'[^\x20-\x7e]', ' ', t)
                t = re.sub(r'(Number|Id|Type)\s*[.:]+\s*', r'\1 : ', t)
                t = re.sub(r'Number : ([0-9IlO]+)', lambda m: 'Number : ' + m.group(1).translate(str.maketrans('IlO', '110')), t)
                t = re.sub(r'\s+', ' ', t)
            fixed.append((t, bb))
        out[pno] = fixed
    return out


def stream(pdf, ocr=None):
    """All text/image blocks of the paper, in reading order, across pages."""
    for pno, page in enumerate(pdf):
        blocks = page.get_text('dict')['blocks']
        if ocr:
            imgs = [b['bbox'] for b in blocks if b['type'] == 1]
            inside = lambda r: any(r[0] >= i[0] - 2 and r[2] <= i[2] + 2 and r[1] >= i[1] - 2 and r[3] <= i[3] + 2 for i in imgs)
            blocks = [b for b in blocks if b['type'] == 1] + [
                {'type': 0, 'bbox': bb, 'lines': [{'spans': [{'text': t}]}]}
                for t, bb in ocr.get(pno, []) if not inside(bb)]   # skip text read off NTA's images
        for b in sorted(blocks, key=lambda b: (round(b['bbox'][1]), b['bbox'][0])):
            if b['type'] == 0:
                text = ' '.join(s['text'] for l in b['lines'] for s in l['spans']).strip()
                if text:
                    yield {'kind': 'text', 'text': text, 'page': pno, 'bbox': b['bbox']}
            else:
                yield {'kind': 'image', 'data': b['image'], 'ext': b.get('ext', 'png'),
                       'page': pno, 'bbox': b['bbox']}


def parse_paper(path):
    pdf = pymupdf.open(path)
    ocr = ocr_pages(pdf)
    meta = {'ocr': bool(ocr)}
    first = '\n'.join(t for t, _ in ocr[0]) if ocr else pdf[0].get_text()
    m = re.search(r'Question Paper Name :\s*(.+)', first)
    meta['paper_name'] = m.group(1).strip() if m else ''
    questions, cur, subject, section = [], None, None, None
    seen, copies = set(), {}   # 2023/2024 papers print each question twice (English, then Hindi); keep the first copy
    for b in stream(pdf, ocr):
        if b['kind'] == 'text':
            t = b['text']
            s = SECTION.search(t)
            if s:
                subject, section = s.group(1), s.group(2)
                continue
            h = HEADER.search(t)
            if h:
                copies[h.group(2)] = copies.get(h.group(2), 0) + 1
                if h.group(2) in seen:
                    cur = None; continue
                seen.add(h.group(2))
                cur = {'num': int(h.group(1)), 'qid': h.group(2), 'nta_type': h.group(3),
                       'subject': subject, 'section': section,
                       'q_imgs': [], 'opt_items': [], 'in_options': False, 'notes': []}
                questions.append(cur)
                continue
            if cur is None:
                continue
            if cur['in_options'] and re.match(r'(Correct Marks|Question Mandatory|Instruction Time)', t):
                cur = None; continue      # a question header was missed (OCR); don't run on into it
            if t.startswith('Options :'):
                cur['in_options'] = True
                continue
            o = OPTION_ID.match(t)
            if o and cur['in_options']:
                cur['opt_items'].append({'kind': 'label', 'oid': o.group(1), 'page': b['page'], 'bbox': b['bbox']})
        elif cur is not None:
            (cur['opt_items'] if cur['in_options'] else cur['q_imgs']).append(b)
    for q in questions:
        q['options'] = assign_options(q)
        if ocr and copies.get(q['qid']) != 2:
            q['notes'].append(f'OCR found {copies.get(q["qid"])} copies of this question (expected English + Hindi); check it is the English one')
    return meta, questions


def assign_options(q):
    """Pair each option-ID label with its image.

    Short options: the image sits on the same line as the label (a little above it).
    Long options: the label comes first and a full-width image follows below it.
    """
    items = q['opt_items']
    labels = [i for i in items if i['kind'] == 'label']
    imgs = [i for i in items if i['kind'] == 'image']
    opts = [{'oid': l['oid'], 'imgs': []} for l in labels]
    used = set()
    for n, l in enumerate(labels):
        y0, y1 = l['bbox'][1], l['bbox'][3]
        for k, im in enumerate(imgs):
            if k not in used and im['page'] == l['page'] and im['bbox'][3] >= y0 - 2 and im['bbox'][1] <= y1 + 2:
                opts[n]['imgs'].append(im); used.add(k)
    # leftover images belong to the closest label before them that still has no image
    pos = {id(x): i for i, x in enumerate(items)}
    for k, im in enumerate(imgs):
        if k in used:
            continue
        before = [n for n, l in enumerate(labels) if pos[id(l)] < pos[id(im)] and not opts[n]['imgs']]
        if before:
            opts[before[-1]]['imgs'].append(im); used.add(k)
            q['notes'].append(f'option {before[-1] + 1}: long option, image placed below its label (check)')
        else:
            q['notes'].append('an option image could not be matched to a label')
    return opts


def parse_key(path, exam_date, shift):
    """Return {qid: answer} for the India page of one date/shift of the final key.

    2026 keys have separate India / outside-India pages; 2023/2024 keys have one page per shift,
    print the date as DD.MM.YYYY or DD-MM-YYYY, and may write "Shift :First" and bare subject names."""
    pdf = pymupdf.open(path)
    dates = (f'Exam Date : {exam_date}', f'Exam Date : {exam_date.replace(".", "-")}')
    pages = [p.get_text() for p in pdf]
    pages = [t for t in pages if any(d in t for d in dates) and re.search(rf'Shift\s*:\s*{shift}\b', t)]
    if len(pages) > 1:
        pages = [t for t in pages if 'Centers in India' in t]
    if len(pages) != 1:
        raise SystemExit(f'Expected one India key page for {exam_date} / {shift}, found {len(pages)}')
    lines = [l.strip() for l in pages[0].splitlines() if l.strip()]
    subject = lambda l: l.startswith('( ') or l in ('Mathematics', 'Physics', 'Chemistry')
    start = next(i for i, l in enumerate(lines) if subject(l))
    key, subj = {}, None
    body = lines[start:]
    j = 0
    while j < len(body):
        l = body[j]
        if subject(l):
            subj = l.strip('() ').title(); j += 1; continue
        one = re.fullmatch(r'(\d{7,})\s+(\S.*)', l)   # some pages print "qid answer" on one line
        if one:
            ans = one.group(2)
            if ans.count('(') > ans.count(')') and j + 1 < len(body) and body[j + 1].endswith(')'):
                ans += ' ' + body[j + 1]; j += 1   # a note in brackets wrapped onto the next line
            key[one.group(1)] = {'answer': ans, 'subject': subj}
            j += 1; continue
        if re.fullmatch(r'\d{7,}', l) and j + 1 < len(body):
            key[l] = {'answer': body[j + 1], 'subject': subj}
            j += 2; continue
        j += 1
    return key


def stack(images, path):
    """Save one or more image blocks as a single PNG (stacked vertically)."""
    pics = [Image.open(io.BytesIO(i['data'])).convert('RGB') for i in images]
    if len(pics) == 1:
        pics[0].save(path, optimize=True); return
    w = max(p.width for p in pics); h = sum(p.height for p in pics) + 8 * (len(pics) - 1)
    out = Image.new('RGB', (w, h), 'white'); y = 0
    for p in pics:
        out.paste(p, (0, y)); y += p.height + 8
    out.save(path, optimize=True)


def main():
    paper, keyfile, out, source, year = sys.argv[1:6]
    meta, qs = parse_paper(paper)
    if len(sys.argv) > 7:   # optional override: <DD.MM.YYYY> <shift 1|2>, for papers named differently
        exam_date, shift_no = sys.argv[6], sys.argv[7]
    else:
        m = re.search(r'(\d+)(?:st|nd|rd|th) (\w{3})\w* (\d{4}),? Shift[- ]?0?(\d)', meta['paper_name'])
        months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        if not m:
            raise SystemExit(f'Cannot read date/shift from paper name "{meta["paper_name"]}"; pass <DD.MM.YYYY> <shift>')
        exam_date = f'{int(m.group(1)):02d}.{months[m.group(2)]}.{m.group(3)}'
        shift_no = m.group(4)
    shift = {'1': 'First', '2': 'Second'}[shift_no]
    key = parse_key(keyfile, exam_date, shift)

    if meta['ocr'] and [q['qid'] for q in qs] != list(key):
        print('WARNING: OCR question IDs do not follow the final key order; check review.csv')
    os.makedirs(os.path.join(out, 'img'), exist_ok=True)
    records, review = [], []
    for q in qs:
        flags = list(q['notes'])
        qid = q['qid']
        k = key.get(qid)
        rec = {'id': qid, 'subject': q['subject'], 'chapter': 'Not tagged yet', 'year': int(year),
               'type': 'MCQ' if q['nta_type'] == 'MCQ' else 'NUM',
               'source': f'{source}, Q.{q["num"]} (Question ID {qid})',
               'question': '', 'solution': ''}     # the question is the NTA image
        if not q['q_imgs']:
            flags.append('no question image found')
        else:
            rel = f'img/{qid}.png'; stack(q['q_imgs'], os.path.join(out, rel)); rec['image'] = rel
            if len(q['q_imgs']) > 1:
                flags.append(f'question built from {len(q["q_imgs"])} image pieces (check nothing is cut)')
            if len({i['page'] for i in q['q_imgs']}) > 1:
                flags.append('question runs across a page break')
        if k is None:
            flags.append('question ID not in final key'); ans = ''
        else:
            ans = k['answer']
            if k['subject'] and k['subject'] != q['subject']:
                flags.append(f'key lists it under {k["subject"]}')
        if rec['type'] == 'MCQ':
            if meta['ocr']:   # IDs were read by OCR: NTA option IDs are always 4 consecutive numbers
                o = [int(x['oid']) for x in q['options']]
                if o != list(range(o[0], o[0] + 4)) if o else True:
                    flags.append(f'OCR option IDs not 4 consecutive numbers: {o}')
            if len(q['options']) != 4:
                flags.append(f'{len(q["options"])} options found, expected 4')
            rec['options'], rec['option_images'] = [], []
            for n, o in enumerate(q['options'], 1):
                rec['options'].append(f'[option image {n}]')
                if o['imgs']:
                    rel = f'img/{qid}_o{n}.png'; stack(o['imgs'], os.path.join(out, rel)); rec['option_images'].append(rel)
                else:
                    rec['option_images'].append(''); flags.append(f'option {n} has no image')
            oids = [o['oid'] for o in q['options']]
            lang = re.fullmatch(r'(\d+)\s*\((\d+) for\s*(\w*)\)?', ans)
            if lang:   # e.g. "68019154398 (68019154395 for Gujarati)": the other ID is for a regional-language paper
                flags.append(f'final key: {lang.group(2)} for the {lang.group(3) or "regional-language"} paper; '
                             f'{lang.group(1)} used for this English/Hindi paper')
                ans = lang.group(1)
            multi = [a.strip() for a in ans.split(',')]
            if ans in oids:
                rec['answer'] = oids.index(ans)
            elif ans.lower() in ('dropped', 'drop'):
                rec['exclude'] = 'dropped'; rec['answer'] = None; flags.append('NTA DROPPED this question (final key); left out of mocks')
            elif len(multi) > 1 and all(a in oids for a in multi):
                rec['accept'] = [oids.index(a) for a in multi]; rec['answer'] = rec['accept'][0]
                flags.append('final key accepts more than one option: ' + ', '.join(str(i + 1) for i in rec['accept']))
            else:
                rec['answer'] = None; flags.append(f'key answer "{ans}" is not one of the option IDs')
        else:
            num = r'-?\d+(?:\.\d+)?'
            lang = re.fullmatch(rf'({num})\s*\((DROP|Dropped) for (\w+) Medium\)', ans, re.I)
            if lang:   # e.g. "11 (DROP for Hindi Medium)": dropped only for that medium; this is the English copy
                flags.append(f'final key: dropped for {lang.group(3)} medium only; {lang.group(1)} used for the English question')
                ans = lang.group(1)
            alts = re.fullmatch(rf'({num})\s*(?:\s+or\s+|,)\s*({num})', ans, re.I)
            if re.fullmatch(num, ans):
                rec['answer'] = float(ans) if '.' in ans else int(ans)
            elif alts:
                rec['accept'] = [float(v) if '.' in v else int(v) for v in alts.groups()]; rec['answer'] = rec['accept'][0]
                flags.append('final key accepts either ' + ' or '.join(alts.groups()))
            elif ans.lower() in ('dropped', 'drop'):
                rec['exclude'] = 'dropped'; rec['answer'] = None; flags.append('NTA DROPPED this question (final key); left out of mocks')
            else:
                rec['exclude'] = 'special key'; rec['answer'] = None
                flags.append(f'final key says "{ans}"; left out of mocks')
        if not q['q_imgs'] or any(not x for x in rec.get('option_images', [])):
            rec['exclude'] = 'incomplete in NTA paper'
            flags.append("NTA's paper is missing the question or an option image; left out of mocks")
        rec['nta_key'] = ans
        rec['review_flags'] = flags
        records.append(rec)
        review.append({'Q.No': q['num'], 'Question ID': qid, 'Subject': q['subject'], 'Type': rec['type'],
                       'Final key (NTA)': ans,
                       'Answer as option no.': (rec['answer'] + 1) if rec['type'] == 'MCQ' and rec.get('answer') is not None else '',
                       'Flags': '; '.join(flags)})

    missing = set(key) - {q['qid'] for q in qs}
    with open(os.path.join(out, 'questions.json'), 'w', encoding='utf-8') as f:
        json.dump({'paper': meta['paper_name'], 'source': source, 'exam_date': exam_date, 'shift': shift,
                   'key_ids_not_in_paper': sorted(missing), 'questions': records}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(out, 'review.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(review[0])); w.writeheader(); w.writerows(review)
    by = {}
    for r in records: by[r['subject']] = by.get(r['subject'], 0) + 1
    print(f"{meta['paper_name']}: {len(records)} questions {by}; key entries {len(key)}; "
          f"flagged {sum(1 for r in records if r['review_flags'])}; key IDs missing from paper {len(missing)}")


if __name__ == '__main__':
    main()
