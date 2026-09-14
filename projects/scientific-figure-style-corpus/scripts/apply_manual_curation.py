#!/usr/bin/env python3
"""Apply the user-approved final manual aesthetic curation to the figure corpus.

The authoritative source is annotations/manual_curation_final.csv. The script is
idempotent: assets already deleted in earlier batches are simply skipped.
"""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "annotations" / "manual_curation_final.csv"
REPORT_DIR = ROOT / "reports"
KEPT_MANIFEST = ROOT / "manifests" / "manual-kept-library.csv"
PROJECT_PREFIX = "projects/scientific-figure-style-corpus/"


def norm(value: str) -> str:
    return (value or "").strip().replace("\\", "/")


with DECISIONS.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

required = {"id", "source_group", "asset_path", "decision"}
if not rows or not required.issubset(rows[0]):
    raise SystemExit(f"invalid final decision file; required columns: {sorted(required)}")

ids = [norm(r["id"]) for r in rows]
if len(ids) != len(set(ids)):
    dupes = [k for k, v in Counter(ids).items() if v > 1]
    raise SystemExit(f"duplicate manual IDs in final decisions: {dupes}")

bad_decisions = [r for r in rows if norm(r["decision"]).lower() not in {"keep", "delete"}]
if bad_decisions:
    raise SystemExit(f"invalid decision values: {bad_decisions[:5]}")

keeps = [r for r in rows if norm(r["decision"]).lower() == "keep"]
deletes = [r for r in rows if norm(r["decision"]).lower() == "delete"]
keep_paths = {norm(r["asset_path"]) for r in keeps}
delete_paths = {norm(r["asset_path"]) for r in deletes}

if keep_paths & delete_paths:
    raise SystemExit("an asset path is marked both keep and delete")

# The completed manual review covered exactly 293 displayed assets.
if len(rows) != 293 or len(keeps) != 27 or len(deletes) != 266:
    raise SystemExit(
        f"unexpected final counts: total={len(rows)} keep={len(keeps)} delete={len(deletes)}"
    )

# Remove binaries. Missing delete targets are expected when an earlier batch already
# deleted them; this makes the operation safe to rerun.
deleted_now = []
already_absent = []
for rel in sorted(delete_paths):
    p = ROOT / rel
    if p.exists():
        if not p.is_file():
            raise SystemExit(f"delete target is not a file: {rel}")
        p.unlink()
        deleted_now.append(rel)
        print("deleted asset", rel)
    else:
        already_absent.append(rel)

# Remove now-empty asset directories, but never remove one that still contains a keep.
assets_root = ROOT / "assets"
for d in sorted((p for p in assets_root.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
    try:
        d.rmdir()
    except OSError:
        pass

# Build path/stem matchers for stale CSV references.
delete_full_paths = {PROJECT_PREFIX + p for p in delete_paths}
delete_stems = {Path(p).stem for p in delete_paths}
path_field_hints = {
    "asset_path",
    "image_path",
    "preview_path",
    "local_path",
    "file_path",
    "source_asset_path",
}
id_field_hints = {"sample_id", "asset_id", "image_id"}


def cell_matches_deleted(value: str) -> bool:
    v = norm(value)
    return v in delete_paths or v in delete_full_paths


def row_matches_deleted(row: dict) -> bool:
    # Exact asset-path matches anywhere in the row.
    if any(cell_matches_deleted(v) for v in row.values()):
        return True
    # Known path fields may contain an absolute/repo-prefixed form.
    for key, value in row.items():
        k = (key or "").strip().lower()
        v = norm(value)
        if k in path_field_hints and v:
            if any(v.endswith("/" + p) or v == p for p in delete_paths):
                return True
        if k in id_field_hints and v in delete_stems:
            return True
    return False


# Filter every corpus CSV that can hold asset references. Historical/manual decision
# records are intentionally retained as the audit trail.
filtered_files = {}
csv_candidates = []
for base in (ROOT / "manifests", ROOT / "annotations"):
    if base.exists():
        csv_candidates.extend(base.glob("*.csv"))
if (ROOT / "corpus-index.csv").exists():
    csv_candidates.append(ROOT / "corpus-index.csv")

for path in sorted(set(csv_candidates)):
    if path.name.startswith("manual_curation") or path.name.startswith("manual-curation"):
        continue
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        data = list(reader)
    if not fieldnames:
        continue
    kept_rows = [r for r in data if not row_matches_deleted(r)]
    removed = len(data) - len(kept_rows)
    if removed:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(kept_rows)
        filtered_files[str(path.relative_to(ROOT))] = removed
        print("filtered", path.relative_to(ROOT), removed)

# Validate the 27 selected references physically exist.
missing_keeps = sorted(p for p in keep_paths if not (ROOT / p).is_file())
remaining_deletes = sorted(p for p in delete_paths if (ROOT / p).exists())
if missing_keeps:
    raise SystemExit(f"kept assets missing after cleanup: {missing_keeps}")
if remaining_deletes:
    raise SystemExit(f"delete-marked assets still present: {remaining_deletes}")

# Re-scan non-audit CSVs for stale references.
stale_csv_refs = []
for path in sorted(set(csv_candidates)):
    if path.name.startswith("manual_curation") or path.name.startswith("manual-curation"):
        continue
    if not path.exists():
        continue
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            if row_matches_deleted(row):
                stale_csv_refs.append(f"{path.relative_to(ROOT)}:{line_no}")
                if len(stale_csv_refs) >= 20:
                    break
if stale_csv_refs:
    raise SystemExit(f"stale deleted-asset CSV references remain: {stale_csv_refs}")

# Rebuild a compact canonical manifest for the user-approved aesthetic library.
kept_records = []
for r in keeps:
    rel = norm(r["asset_path"])
    p = ROOT / rel
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    kept_records.append(
        {
            "id": norm(r["id"]),
            "source_group": norm(r["source_group"]),
            "asset_path": rel,
            "size_bytes": p.stat().st_size,
            "sha256": digest,
        }
    )

KEPT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
with KEPT_MANIFEST.open("w", encoding="utf-8", newline="") as f:
    fieldnames = ["id", "source_group", "asset_path", "size_bytes", "sha256"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(kept_records)

hash_counts = Counter(r["sha256"] for r in kept_records)
duplicate_hashes = sorted(h for h, n in hash_counts.items() if n > 1)

REPORT_DIR.mkdir(parents=True, exist_ok=True)
report = {
    "decision_source": str(DECISIONS.relative_to(ROOT)),
    "reviewed_total": len(rows),
    "keep_total": len(keeps),
    "delete_total": len(deletes),
    "deleted_in_this_run": len(deleted_now),
    "already_absent_before_run": len(already_absent),
    "filtered_csv_files": filtered_files,
    "missing_keep_assets": missing_keeps,
    "remaining_delete_assets": remaining_deletes,
    "duplicate_sha256_among_kept": duplicate_hashes,
    "validation": "PASS",
}
(REPORT_DIR / "manual_curation_apply_report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)

print(json.dumps(report, indent=2, ensure_ascii=False))
