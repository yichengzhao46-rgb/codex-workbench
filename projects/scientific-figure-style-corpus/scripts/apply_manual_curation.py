#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / 'annotations' / 'manual-curation-decisions.csv'

with DECISIONS.open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))

deletes = [r for r in rows if (r.get('decision') or '').strip().lower() == 'delete']
asset_paths = {r['asset_path'].strip() for r in deletes}
sample_ids = {Path(p).stem for p in asset_paths}

# Remove binaries.
for rel in sorted(asset_paths):
    p = ROOT / rel
    if p.exists():
        p.unlink()
        print('deleted asset', rel)

# Raw manifest: match asset_path.
def filter_csv(path: Path, predicate):
    if not path.exists():
        return 0
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        data = list(reader)
    kept = [r for r in data if not predicate(r)]
    if len(kept) == len(data):
        return 0
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(kept)
    print('filtered', path.relative_to(ROOT), len(data)-len(kept))
    return len(data)-len(kept)

filter_csv(ROOT/'manifests'/'raw-image-manifest.csv', lambda r: (r.get('asset_path') or '').strip() in asset_paths)
filter_csv(ROOT/'annotations'/'figure-level-classification-v0.1.csv', lambda r: (r.get('sample_id') or '').strip() in sample_ids)
filter_csv(ROOT/'manifests'/'unified-library-index.csv', lambda r: (r.get('asset_path') or '').strip() in asset_paths)

print(f'applied {len(deletes)} manual deletions')
