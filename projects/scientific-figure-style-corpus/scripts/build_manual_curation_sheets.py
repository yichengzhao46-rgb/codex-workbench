#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('projects/scientific-figure-style-corpus')
OUT = ROOT / 'validation' / 'manual_curation'
SOURCES = [
    ('R', ROOT / 'assets' / 'raw'),
    ('S', ROOT / 'assets' / 'stage1_5'),
    ('Z', ROOT / 'assets' / 'zotero'),
]
EXTS = {'.jpg', '.jpeg', '.png', '.webp'}
PER_SHEET = 12
COLS = 3
CELL_W = 640
CELL_H = 470
THUMB_W = 610
THUMB_H = 390


def load_font(size: int):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def collect():
    rows = []
    counters = {'R': 0, 'S': 0, 'Z': 0}
    for prefix, base in SOURCES:
        if not base.exists():
            continue
        for path in sorted(p for p in base.rglob('*') if p.is_file() and p.suffix.lower() in EXTS):
            counters[prefix] += 1
            stable_id = f'{prefix}{counters[prefix]:03d}'
            rows.append((stable_id, path))
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.glob('sheet-*.jpg'):
        p.unlink()
    rows = collect()
    mapping = OUT / 'manual_curation_mapping.csv'
    with mapping.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id', 'source_group', 'asset_path'])
        for stable_id, path in rows:
            w.writerow([stable_id, stable_id[0], str(path.relative_to(ROOT))])

    title_font = load_font(24)
    label_font = load_font(18)
    rows_per_sheet = (PER_SHEET + COLS - 1) // COLS
    for sheet_idx in range((len(rows) + PER_SHEET - 1) // PER_SHEET):
        chunk = rows[sheet_idx * PER_SHEET:(sheet_idx + 1) * PER_SHEET]
        canvas = Image.new('RGB', (COLS * CELL_W, rows_per_sheet * CELL_H + 70), 'white')
        draw = ImageDraw.Draw(canvas)
        draw.text((20, 20), f'PR #20 manual curation — batch {sheet_idx + 1:02d}', fill='black', font=title_font)
        for i, (stable_id, path) in enumerate(chunk):
            r, c = divmod(i, COLS)
            x0, y0 = c * CELL_W, 70 + r * CELL_H
            try:
                img = Image.open(path).convert('RGB')
                img.thumbnail((THUMB_W, THUMB_H))
                x = x0 + (CELL_W - img.width) // 2
                y = y0 + 45 + (THUMB_H - img.height) // 2
                canvas.paste(img, (x, y))
            except Exception as exc:
                draw.text((x0 + 20, y0 + 100), f'LOAD ERROR: {exc}', fill='black', font=label_font)
            short = path.name
            if len(short) > 68:
                short = short[:65] + '...'
            draw.rectangle((x0 + 8, y0 + 6, x0 + CELL_W - 8, y0 + 42), outline='black', width=1)
            draw.text((x0 + 14, y0 + 12), f'{stable_id}  {short}', fill='black', font=label_font)
        canvas.save(OUT / f'sheet-{sheet_idx + 1:02d}.jpg', quality=90)

    summary = OUT / 'summary.txt'
    summary.write_text(
        f'total_images={len(rows)}\nraw={sum(1 for x,_ in rows if x.startswith("R"))}\nstage1_5={sum(1 for x,_ in rows if x.startswith("S"))}\nzotero={sum(1 for x,_ in rows if x.startswith("Z"))}\nsheets={(len(rows)+PER_SHEET-1)//PER_SHEET}\n',
        encoding='utf-8'
    )
    print(summary.read_text())

if __name__ == '__main__':
    main()
