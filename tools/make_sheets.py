"""
Contact sheets for chapter tagging: stacks NTA's question images (with the question
number, subject and type written above each) into tall PNGs so several questions can
be read at once. Sheets are a working aid only and are not part of the app.

Usage: python tools/make_sheets.py <pyq/<year>/<shift>> <out_dir> [max_height]
"""
import json, os, sys

from PIL import Image, ImageDraw, ImageFont

WIDTH = 900


def main():
    folder, out = sys.argv[1], sys.argv[2]
    max_h = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    os.makedirs(out, exist_ok=True)
    qs = json.load(open(os.path.join(folder, 'questions.json'), encoding='utf-8'))['questions']
    try:
        font = ImageFont.truetype('arial.ttf', 22)
    except OSError:
        font = ImageFont.load_default()
    tiles = []
    for n, q in enumerate(qs, 1):
        head = f"Q{n}  {q['subject']}  {q['type']}" + ('  [left out: ' + q['exclude'] + ']' if q.get('exclude') else '')
        parts = [Image.open(os.path.join(folder, q['image'])).convert('RGB')] if q.get('image') else []
        if q['type'] == 'MCQ':   # options side by side, small, to help when the stem alone is ambiguous
            opts = [Image.open(os.path.join(folder, p)).convert('RGB') for p in q.get('option_images', []) if p]
            if opts:
                h = max(o.height for o in opts); w = sum(o.width for o in opts) + 30 * len(opts)
                row = Image.new('RGB', (w, h), 'white'); x = 0
                for o in opts:
                    row.paste(o, (x, 0)); x += o.width + 30
                parts.append(row)
        body = [p.resize((WIDTH, max(1, round(p.height * WIDTH / p.width)))) if p.width > WIDTH else p for p in parts]
        h = 34 + sum(p.height + 6 for p in body)
        tile = Image.new('RGB', (WIDTH, h), 'white')
        d = ImageDraw.Draw(tile)
        d.rectangle([0, 0, WIDTH, 30], fill=(225, 235, 255)); d.text((6, 3), head, fill='black', font=font)
        y = 34
        for p in body:
            tile.paste(p, (0, y)); y += p.height + 6
        tiles.append(tile)
    sheets, cur = [], []
    for t in tiles:
        if cur and sum(x.height for x in cur) + t.height > max_h:
            sheets.append(cur); cur = []
        cur.append(t)
    if cur:
        sheets.append(cur)
    for i, s in enumerate(sheets, 1):
        img = Image.new('RGB', (WIDTH, sum(t.height + 4 for t in s)), (160, 160, 160)); y = 0
        for t in s:
            img.paste(t, (0, y)); y += t.height + 4
        img.save(os.path.join(out, f'sheet{i:02d}.png'))
    print(f'{len(qs)} questions -> {len(sheets)} sheets in {out}')


if __name__ == '__main__':
    main()
