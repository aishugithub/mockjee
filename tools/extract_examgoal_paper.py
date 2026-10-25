"""
Extract one ExamGOAL question-paper PDF (pdf.questions.examgoal.com) into the same per-shift format as
tools/extract_nta_paper.py, for years NTA does not publish openly (owner's decision, 2026-10-25:
2025, 2022, 2021).

These questions are ExamGOAL's retyped copies with ExamGOAL's answer key, NOT NTA's own paper or
final key. Every record says so: source_kind = "examgoal" and the source line ends "(ExamGOAL)".

What it does
  - cuts each question stem and each option out of the PDF as an image (ExamGOAL's repeating
    background watermark tiles are removed first; logos printed inside figures stay)
  - reads ExamGOAL's answer key on the last pages ("C, D" and "4 or 3.5" become `accept`;
    BONUS and "Scan QR" questions are left out of mocks)
  - reads each question's chapter from the title of its ExamSIDE page (the QR link beside it),
    cached in sources/<year>/examside_titles.json; that chapter is the `topic`, and its NTA unit
    comes from tools/examgoal_chapters.py
  - questions ExamGOAL lists under "Out of syllabus" get chapter "Not in current syllabus"

Usage:  python tools/extract_examgoal_paper.py <paper.pdf> <out_dir> "<source label>" <year>
Writes <out_dir>/img/*.png, questions.json, review.csv
"""
import csv, html, io, json, os, re, ssl, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

import pymupdf
from PIL import Image, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapters import CODES, OUTSIDE
from examgoal_chapters import unit_for

SUBJECTS = ('Chemistry', 'Mathematics', 'Physics')
RIGHT = 505          # the QR code and "Open solution" sit right of this
DPI = 200
PALE = 175     # pixels lighter than this in every channel are watermark/background
HEADER = re.compile(r'^Q(\d+)\.$')
OPT = re.compile(r'^\(([ABCD])\)')


def strip_tiles(pdf):
    """Remove the faint repeating 'ExamGOAL' watermark tiles (one image placed many times per page)."""
    for page in pdf:
        for img in page.get_images(full=True):
            xref = img[0]
            rects = page.get_image_rects(xref)
            if len(rects) >= 3 and all(round(r.width) in (225, 145) or r.width > 140 for r in rects):
                page.delete_image(xref)


def lines_of(page):
    out = []
    for b in page.get_text('dict', flags=pymupdf.TEXTFLAGS_TEXT)['blocks']:   # text only: skip the many tile images
        if b['type'] != 0:
            continue
        for l in b['lines']:
            t = ''.join(s['text'] for s in l['spans']).strip()
            if t:
                out.append({'t': t, 'bbox': pymupdf.Rect(l['bbox'])})
    return sorted(out, key=lambda l: (round(l['bbox'].y0), l['bbox'].x0))


def footer_top(page, lines):
    for l in lines:
        if l['t'].startswith('Keep practising on the ExamGOAL app'):
            return l['bbox'].y0 - 18
    return page.rect.height - 80


_PAGE_CACHE = {}


def page_shapes(page):
    """Image rects and drawing rects of a page, read once (get_drawings is slow on maths-heavy pages)."""
    k = page.number
    if k not in _PAGE_CACHE:
        imgs = [r for img in page.get_images(full=True) for r in page.get_image_rects(img[0])]
        draws = [dr['rect'] for dr in page.get_drawings()]
        _PAGE_CACHE[k] = (imgs, draws)
    return _PAGE_CACHE[k]


def content_bottom(page, lines, y0, y1):
    """Lowest content (text, figure, vector drawing) between y0 and y1, left of the QR column."""
    bottom = y0
    imgs, draws = page_shapes(page)
    for l in lines:
        r = l['bbox']
        if r.y0 >= y0 and r.y1 <= y1 + 1 and r.x0 < RIGHT:
            bottom = max(bottom, r.y1)
    for r in imgs:
        if r.y0 >= y0 - 2 and r.y1 <= y1 + 2 and r.x0 < RIGHT and r.x1 <= RIGHT + 10:
            bottom = max(bottom, r.y1)
    for r in draws:
        if r.y0 >= y0 and r.y1 <= y1 and r.x1 < RIGHT and r.height < 300:
            bottom = max(bottom, r.y1)
    return bottom


def render(page, rect, path):
    pix = page.get_pixmap(clip=rect, dpi=DPI)
    im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    # ExamGOAL's watermarks (diagonal background text, faint grid in figures) are very pale; the question
    # itself is dark ink. Whiten every pixel whose darkest channel is still light.
    r, g, b = im.split()
    pale = ImageChops.darker(ImageChops.darker(r, g), b).point(lambda v: 255 if v > PALE else 0)
    im.paste((255, 255, 255), mask=pale)
    box = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).point(lambda v: 255 if v > 18 else 0).getbbox()
    if box:
        pad = 6
        im = im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad)))
    im.save(path, optimize=True)
    return bool(box)


def parse_key(pdf):
    text = ''.join(p.get_text() for p in pdf)
    body = text[text.rfind('Answer Key'):]
    key, subj = {}, None
    for line in body.splitlines():
        line = line.strip()
        if line in SUBJECTS + ('Out of syllabus',):
            subj = line; continue
        m = re.fullmatch(r'(\d+)\.\s*(.+)', line)
        if m and subj:
            key[int(m.group(1))] = m.group(2).strip()
    return key


def fetch_titles(ids, cache_path):
    cache = json.load(open(cache_path, encoding='utf-8')) if os.path.exists(cache_path) else {}
    todo = [i for i in ids if i not in cache]

    ctx = ssl.create_default_context()          # built once: loading the Windows certificate store is slow

    def get(qid):
        url = f'https://questions.examside.com/past-years/jee/question/{qid}'
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                body = urllib.request.urlopen(req, timeout=60, context=ctx).read().decode('utf-8', 'replace')
                m = re.search(r'<title>([^<]*)</title>', body)
                return qid, (html.unescape(m.group(1)) if m else '')
            except Exception:
                time.sleep(2 + attempt * 3)
        return qid, ''
    with ThreadPoolExecutor(4) as ex:
        for qid, title in ex.map(get, todo):
            if title:
                cache[qid] = title
    json.dump(cache, open(cache_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    return cache


def main():
    paper, out, source, year = sys.argv[1:5]
    pdf = pymupdf.open(paper)
    title = pdf.metadata.get('title', '').split(' — ')[0].strip()
    strip_tiles(pdf)
    key = parse_key(pdf)
    key_page = next(i for i in range(len(pdf) - 1, -1, -1) if 'Answer Key' in pdf[i].get_text())
    os.makedirs(os.path.join(out, 'img'), exist_ok=True)

    # 1. find every question block
    blocks, subject, oos = [], None, False
    for pno in range(1, key_page):
        page = pdf[pno]
        L = lines_of(page)
        foot = footer_top(page, L)
        heads = []
        for i, l in enumerate(L):
            if l['t'] in SUBJECTS + ('Out of syllabus',) and l['bbox'].x0 < 60 and any(
                    re.fullmatch(r'\d+ questions?', m['t']) and abs(m['bbox'].y0 - l['bbox'].y0) < 6 for m in L):
                heads.append(('section', l['bbox'].y0, l['t']))
            m = HEADER.match(l['t'])
            if m and l['bbox'].x0 < 60:
                same = ' '.join(x['t'] for x in L if abs(x['bbox'].y0 - l['bbox'].y0) < 4 and x is not l and x['bbox'].x0 < RIGHT)
                heads.append(('q', l['bbox'].y0, (int(m.group(1)), same, l['bbox'])))
        heads.sort(key=lambda h: h[1])
        links = [(pymupdf.Rect(k['from']), k['uri']) for k in page.get_links()
                 if 'examside.com' in k.get('uri', '') and 'utm_medium' not in k['uri']]
        for j, h in enumerate(heads):
            if h[0] == 'section':
                subject = h[2] if h[2] != 'Out of syllabus' else subject
                oos = h[2] == 'Out of syllabus'
                continue
            num, typ, hb = h[2]
            nxt = heads[j + 1][1] if j + 1 < len(heads) else foot
            y_end = min(nxt, foot) - 2
            subj = subject
            if oos:
                sm = re.search(r'·\s*(Chemistry|Mathematics|Physics)', typ)
                subj = sm.group(1) if sm else subject
            link = min(links, key=lambda k: abs(k[0].y0 - hb.y0), default=None)
            qid = re.search(r'/question/([a-z0-9]+)', link[1]).group(1) if link and abs(link[0].y0 - hb.y0) < 60 else None
            blocks.append(dict(num=num, typ=typ, page=pno, hb=hb, y_end=y_end, subject=subj, oos=oos, qid=qid, lines=L))

    # 2. chapters from ExamSIDE page titles
    cache = fetch_titles([b['qid'] for b in blocks if b['qid']], os.path.join(os.path.dirname(paper), 'examside_titles.json'))

    records, review = [], []
    for b in blocks:
        flags = []
        page = pdf[b['page']]
        L = b['lines']
        top = b['hb'].y1 + 1
        bottom = content_bottom(page, L, top, b['y_end'])
        is_mcq = b['typ'].startswith('MCQ')
        qid = b['qid'] or f"{os.path.basename(out)}_q{b['num']}"
        if not b['qid']:
            flags.append('no ExamSIDE link found')
        rid = f'eg_{qid}'
        rec = {'id': rid, 'subject': b['subject'], 'year': int(year), 'type': 'MCQ' if is_mcq else 'NUM',
               'source': f"{source}, Q.{b['num']} (ExamGOAL)", 'source_kind': 'examgoal',
               'origin_url': f'https://questions.examside.com/past-years/jee/question/{qid}' if b['qid'] else '',
               'question': '', 'solution': ''}
        if 'Multiple Correct' in b['typ']:
            flags.append('multiple-correct MCQ')

        # chapter / topic
        t = html.unescape(cache.get(b['qid'] or '', ''))
        parts = [p.strip() for p in t.split('|')]
        topic = re.sub(r'\s+Question\s+\d+$', '', parts[1]) if len(parts) >= 3 else ''
        if not topic:
            flags.append('chapter not found on ExamSIDE'); rec['chapter'] = 'Not tagged yet'
        else:
            if parts[2] != b['subject']:
                flags.append(f'ExamSIDE lists the subject as {parts[2]}')
            if title and parts[0] != title:
                flags.append(f'ExamSIDE page belongs to "{parts[0]}"')
            rec['topic'] = topic
            try:
                code, amb = unit_for(b['subject'], topic)
                rec['chapter'] = CODES[code][1]
                rec['tag_confidence'] = 'low' if amb else 'high'
                if amb:
                    flags.append(f'NTA unit inferred from ExamGOAL chapter "{topic}" (spans two units)')
            except KeyError:
                rec['chapter'] = 'Not tagged yet'; flags.append(f'unknown ExamGOAL chapter "{topic}"')
        if b['oos']:
            rec['chapter'] = OUTSIDE
            rec['out_of_syllabus'] = 'examgoal'

        # options: the LAST (A) in the block and the B, C, D after it (earlier (A)-(D) are lists in the stem)
        opts = [l for l in L if OPT.match(l['t']) and top <= l['bbox'].y0 <= b['y_end'] and l['bbox'].x0 < RIGHT - 60]
        chosen = []
        if is_mcq:
            a_idx = max((i for i, l in enumerate(opts) if l['t'].startswith('(A)')), default=None)
            if a_idx is not None:
                a_y = opts[a_idx]['bbox'].y0           # labels on the same row can sit a point higher than (A)
                seq = [l for l in opts if l['bbox'].y0 >= a_y - 4]
                for letter in 'ABCD':
                    hit = next((l for l in seq if l['t'].startswith(f'({letter})') and l not in chosen), None)
                    if hit: chosen.append(hit)
            if len(chosen) != 4:
                flags.append(f'{len(chosen)} option labels found, expected 4')
        stem_bottom = (min(l['bbox'].y0 for l in chosen) - 3) if chosen else bottom + 3
        stem = pymupdf.Rect(28, top, RIGHT, stem_bottom)
        if stem.height < 4 or not render(page, stem, os.path.join(out, 'img', f'{rid}.png')):
            flags.append('empty question image')
        rec['image'] = f'img/{rid}.png'
        if is_mcq and len(chosen) == 4:
            rows = sorted({round(l['bbox'].y0) for l in chosen})
            rows_m = []                                  # merge rows a few points apart
            for y in rows:
                if rows_m and y - rows_m[-1] < 5: continue
                rows_m.append(y)
            rec['options'], rec['option_images'] = [], []
            for n, l in enumerate(chosen, 1):
                r = l['bbox']
                ri = max(i for i, y in enumerate(rows_m) if y <= round(r.y0) + 4)
                y0 = rows_m[ri] - 4
                y1 = (rows_m[ri + 1] - 4) if ri + 1 < len(rows_m) else bottom + 3
                same_row = sorted(x['bbox'].x0 for x in chosen if abs(round(x['bbox'].y0) - rows_m[ri]) < 5)
                right = next((x for x in same_row if x > r.x0 + 5), RIGHT) - 4
                rect = pymupdf.Rect(r.x0 + 14.5, y0, right, max(y1, r.y1 + 1))   # skip the "(A)" label itself
                rel = f'img/{rid}_o{n}.png'
                ok = render(page, rect, os.path.join(out, rel))
                rec['options'].append(f'[option image {n}]'); rec['option_images'].append(rel)
                if not ok: flags.append(f'option {n} image is empty')

        # answer from ExamGOAL's key
        ans = key.get(b['num'], '')
        rec['examgoal_key'] = ans
        num = r'-?\d+(?:\.\d+)?'
        if ans.upper() == 'BONUS':
            rec['exclude'] = 'bonus (ExamGOAL key)'; rec['answer'] = None
        elif ans in ('', 'Scan QR'):
            rec['exclude'] = 'no answer in ExamGOAL key'; rec['answer'] = None
        elif is_mcq:
            letters = [x.strip() for x in ans.split(',')]
            if all(x in 'ABCD' and x for x in letters) and len(chosen) == 4:
                idx = ['ABCD'.index(x) for x in letters]
                rec['answer'] = idx[0]
                if len(idx) > 1:
                    rec['accept'] = idx; flags.append('ExamGOAL key accepts ' + ans)
            else:
                rec['exclude'] = f'key "{ans}" not usable'; rec['answer'] = None
        else:
            alts = re.fullmatch(rf'({num})\s+or\s+({num})', ans)
            rng = re.fullmatch(rf'({num})\s*(?:-|to)\s*({num})', ans)
            if re.fullmatch(num, ans):
                rec['answer'] = float(ans) if '.' in ans else int(ans)
            elif alts:
                rec['accept'] = [float(v) if '.' in v else int(v) for v in alts.groups()]; rec['answer'] = rec['accept'][0]
                flags.append('ExamGOAL key accepts ' + ans)
            elif rng:
                rec['answer'] = ans; flags.append('range answer ' + ans)
            else:
                rec['exclude'] = f'key "{ans}" not usable'; rec['answer'] = None
        if rec.get('exclude'):
            flags.append('left out of mocks: ' + rec['exclude'])
        rec['review_flags'] = flags
        records.append(rec)
        review.append({'Q.No': b['num'], 'ExamSIDE id': qid, 'Subject': b['subject'], 'Topic': rec.get('topic', ''),
                       'NTA unit': rec.get('chapter', ''), 'Type': rec['type'], 'ExamGOAL key': ans, 'Flags': '; '.join(flags)})

    with open(os.path.join(out, 'questions.json'), 'w', encoding='utf-8') as f:
        json.dump({'paper': title, 'source': source, 'source_kind': 'examgoal', 'pdf': os.path.basename(paper),
                   'questions': records}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(out, 'review.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(review[0])); w.writeheader(); w.writerows(review)
    by = {}
    for r in records: by[r['subject']] = by.get(r['subject'], 0) + 1
    print(f"{title}: {len(records)} questions {by}; key entries {len(key)}; flagged {sum(1 for r in records if r['review_flags'])}")


if __name__ == '__main__':
    main()
