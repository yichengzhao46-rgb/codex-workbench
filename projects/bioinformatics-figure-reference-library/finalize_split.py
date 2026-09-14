#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / 'scientific-figure-style-corpus'
BIO = ROOT / 'bioinformatics-figure-reference-library'
SPLIT = BIO / 'final_split.csv'
MAIN_MANIFEST = MAIN / 'manifests' / 'manual-kept-library.csv'
BIO_MANIFEST = BIO / 'manifest.csv'
REPORT = BIO / 'split_report.json'


def read_csv(path: Path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


split_rows = read_csv(SPLIT)
target = {r['id']: r['target_library'] for r in split_rows}
bio_ids = {k for k, v in target.items() if v == 'bioinformatics'}
main_ids = {k for k, v in target.items() if v == 'main'}
assert len(split_rows) == 27
assert len(bio_ids) == 13
assert len(main_ids) == 14

main_rows = read_csv(MAIN_MANIFEST)
existing_bio_rows = read_csv(BIO_MANIFEST) if BIO_MANIFEST.exists() else []
bio_by_id = {r['id']: r for r in existing_bio_rows}

moved_now = []
source_paths = {}
for r in list(main_rows):
    rid = r['id']
    if rid not in bio_ids:
        continue
    src_rel = r['asset_path']
    src = MAIN / src_rel
    dst_rel = f"assets/{rid}/{Path(src_rel).name}"
    dst = BIO / dst_rel
    source_paths[rid] = src_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.move(str(src), str(dst))
        moved_now.append(rid)
    elif not dst.exists():
        raise FileNotFoundError(f'{rid}: neither source nor destination exists')
    bio_by_id[rid] = {
        'id': rid,
        'source_group': r['source_group'],
        'asset_path': dst_rel,
        'origin_library': 'scientific-figure-style-corpus',
        'origin_asset_path': src_rel,
        'selection_role': 'bioinformatics_analysis_visual_reference',
        'size_bytes': r['size_bytes'],
        'sha256': r['sha256'],
    }

# Recover origin paths for previously moved seed entries.
for rid, r in bio_by_id.items():
    if rid in bio_ids:
        source_paths[rid] = r['origin_asset_path']

# Main active manifest: exactly the 14 user-retained IDs.
main_rows_final = [r for r in main_rows if r['id'] in main_ids]
missing_main_ids = sorted(main_ids - {r['id'] for r in main_rows_final})
if missing_main_ids:
    raise RuntimeError(f'missing main manifest IDs: {missing_main_ids}')
write_csv(MAIN_MANIFEST, main_rows_final, ['id','source_group','asset_path','size_bytes','sha256'])

# Bioinformatics manifest: exactly the 13 transferred IDs.
bio_rows_final = [bio_by_id[rid] for rid in sorted(bio_ids)]
missing_bio_ids = sorted(bio_ids - set(bio_by_id))
if missing_bio_ids:
    raise RuntimeError(f'missing bioinformatics IDs: {missing_bio_ids}')
write_csv(BIO_MANIFEST, bio_rows_final, ['id','source_group','asset_path','origin_library','origin_asset_path','selection_role','size_bytes','sha256'])

# Remove transferred assets from active/source CSV indexes while preserving manual/audit decisions.
old_paths = set(source_paths.values())
filtered = {}
for path in MAIN.rglob('*.csv'):
    rel = path.relative_to(MAIN)
    rel_s = str(rel)
    if rel_s.startswith('annotations/manual') or rel_s.startswith('validation/manual_curation'):
        continue
    if path == MAIN_MANIFEST:
        continue
    try:
        rows = read_csv(path)
    except Exception:
        continue
    if not rows:
        continue
    fieldnames = list(rows[0].keys())
    kept = []
    removed = 0
    for row in rows:
        if any((v or '').strip() in old_paths for v in row.values()):
            removed += 1
        else:
            kept.append(row)
    if removed:
        write_csv(path, kept, fieldnames)
        filtered[rel_s] = removed

# Validate physical separation.
missing_main_assets = []
for r in main_rows_final:
    if not (MAIN / r['asset_path']).exists():
        missing_main_assets.append(r['id'])
missing_bio_assets = []
for r in bio_rows_final:
    if not (BIO / r['asset_path']).exists():
        missing_bio_assets.append(r['id'])
residual_old_assets = [rid for rid, p in source_paths.items() if (MAIN / p).exists()]

status = 'PASS' if not (missing_main_assets or missing_bio_assets or residual_old_assets) else 'FAIL'
report = {
    'main_count': len(main_rows_final),
    'bioinformatics_count': len(bio_rows_final),
    'moved_now': sorted(moved_now),
    'filtered_csv_files': filtered,
    'missing_main_assets': missing_main_assets,
    'missing_bioinformatics_assets': missing_bio_assets,
    'residual_old_assets': residual_old_assets,
    'validation': status,
}
REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
if status != 'PASS':
    raise SystemExit(1)
