#!/usr/bin/env python3
"""Build and query the unified scientific figure library.

The unified library has one retrieval surface with two provenance/eligibility tiers:
- active: validated Stage 1.5 A/B assets
- reference: Codex/Zotero reference assets

Physical asset locations remain unchanged. This script normalizes both sources into a
single row-level index while preserving rights, QA, provenance, and promotion gates.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path, PureWindowsPath
from typing import Iterable

PROJECT_DEFAULT = Path("projects/scientific-figure-style-corpus")
UNIFIED_FIELDS = [
    "record_id",
    "canonical_record_id",
    "duplicate_of",
    "library_tier",
    "source_manifest",
    "source_record_id",
    "source_type",
    "journal",
    "year",
    "article_title",
    "doi",
    "article_url",
    "figure_id",
    "primary_purpose",
    "style_family",
    "layout",
    "topics",
    "asset_path",
    "sha256",
    "rights_status",
    "redistribution_allowed",
    "visual_qa_status",
    "active_eligible",
    "retrieval_enabled",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def first(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def bool_text(value: str | bool, default: bool = False) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    v = (value or "").strip().lower()
    if v in {"1", "true", "yes", "y"}:
        return "true"
    if v in {"0", "false", "no", "n"}:
        return "false"
    return "true" if default else "false"


def normalize_zotero_asset_path(raw: str, sample_id: str) -> str:
    raw = (raw or "").strip()
    if raw:
        parts = list(PureWindowsPath(raw).parts)
        lower = [p.lower() for p in parts]
        if "zotero" in lower:
            idx = lower.index("zotero")
            suffix = parts[idx + 1 :]
            if suffix:
                return Path("assets", "zotero", *suffix).as_posix()
    return f"assets/zotero/__unresolved__/{sample_id}.png"


def active_manifest_paths(project: Path) -> list[Path]:
    manifests = project / "manifests"
    paths = sorted(manifests.glob("stage1_5*_harvested_figures.csv"))
    return paths


def baseline_active_rows(project: Path) -> list[dict[str, str]]:
    raw_path = project / "manifests" / "raw-image-manifest.csv"
    cls_path = project / "annotations" / "figure-level-classification-v0.1.csv"
    raw = {first(r, "sample_id"): r for r in read_csv(raw_path)}
    out = []
    for c in read_csv(cls_path):
        if first(c, "style_learning_tier") not in {"A_style_reference", "B_style_reference"}:
            continue
        sid = first(c, "sample_id")
        r = raw.get(sid)
        if not r:
            raise SystemExit(f"Baseline active record missing from raw manifest: {sid}")
        out.append({**r, **{f"classification__{k}": v for k, v in c.items()}})
    return out


def normalize_baseline(row: dict[str, str]) -> dict[str, str]:
    rid = first(row, "sample_id")
    purpose = first(row, "classification__primary_purpose")
    tier = first(row, "classification__style_learning_tier")
    return {
        "record_id": f"ACTIVE::{rid}::baseline",
        "canonical_record_id": "",
        "duplicate_of": "",
        "library_tier": "active",
        "source_manifest": "manifests/raw-image-manifest.csv + annotations/figure-level-classification-v0.1.csv",
        "source_record_id": rid,
        "source_type": "stage1_baseline_raw_corpus",
        "journal": first(row, "journal"),
        "year": first(row, "year"),
        "article_title": first(row, "article_title"),
        "doi": first(row, "doi"),
        "article_url": first(row, "article_url"),
        "figure_id": first(row, "figure_id"),
        "primary_purpose": purpose,
        "style_family": first(row, "classification__style_family"),
        "layout": first(row, "classification__layout"),
        "topics": first(row, "classification__domain_relevance_to_bath_rp"),
        "asset_path": first(row, "asset_path"),
        "sha256": first(row, "sha256").lower(),
        "rights_status": first(row, "rights_status", "license"),
        "redistribution_allowed": "true",
        "visual_qa_status": first(row, "inspection_status") or "classified",
        "active_eligible": "true",
        "retrieval_enabled": "true",
        "notes": ";".join(x for x in [tier, first(row, "classification__qa_caveats"), first(row, "caption")] if x),
    }


def normalize_active(row: dict[str, str], source: Path) -> dict[str, str]:
    rid = first(row, "sample_id", "candidate_id", "figure_id")
    if not rid:
        rid = Path(first(row, "asset_path") or "unknown").stem
    figure = first(row, "figure_number", "figure_id")
    if figure and not figure.lower().startswith("fig") and figure.isdigit():
        figure = f"Figure {figure}"
    return {
        "record_id": f"ACTIVE::{rid}::{figure or 'figure'}",
        "canonical_record_id": "",
        "duplicate_of": "",
        "library_tier": "active",
        "source_manifest": source.as_posix(),
        "source_record_id": rid,
        "source_type": first(row, "source_type") or "stage1_5_public_harvest",
        "journal": first(row, "journal"),
        "year": first(row, "year"),
        "article_title": first(row, "article_title", "title"),
        "doi": first(row, "doi"),
        "article_url": first(row, "article_url"),
        "figure_id": figure,
        "primary_purpose": first(row, "primary_purpose"),
        "style_family": first(row, "style_family"),
        "layout": first(row, "layout_archetype", "layout"),
        "topics": first(row, "topics", "domain_relevance_to_bath_rp"),
        "asset_path": first(row, "asset_path"),
        "sha256": first(row, "sha256").lower(),
        "rights_status": first(row, "rights_status", "license"),
        "redistribution_allowed": "true",
        "visual_qa_status": first(row, "visual_qa", "inspection_status") or "validated",
        "active_eligible": "true",
        "retrieval_enabled": "true",
        "notes": first(row, "notes", "caption"),
    }


def normalize_zotero(row: dict[str, str], source: Path) -> dict[str, str]:
    rid = first(row, "sample_id")
    return {
        "record_id": f"ZOTERO::{rid}",
        "canonical_record_id": "",
        "duplicate_of": "",
        "library_tier": "reference",
        "source_manifest": source.as_posix(),
        "source_record_id": rid,
        "source_type": first(row, "source_type") or "zotero_pdf",
        "journal": first(row, "journal"),
        "year": first(row, "year"),
        "article_title": first(row, "article_title"),
        "doi": first(row, "doi"),
        "article_url": "",
        "figure_id": first(row, "figure_id"),
        "primary_purpose": first(row, "target_primary_purpose"),
        "style_family": "",
        "layout": "",
        "topics": first(row, "topics"),
        "asset_path": normalize_zotero_asset_path(first(row, "asset_path"), rid),
        "sha256": first(row, "sha256").lower(),
        "rights_status": first(row, "license_status") or "reference_only",
        "redistribution_allowed": bool_text(first(row, "redistribution_allowed"), default=False),
        "visual_qa_status": first(row, "visual_inspection_status") or "pending",
        "active_eligible": "false",
        "retrieval_enabled": "true",
        "notes": first(row, "notes", "caption"),
    }


def dedupe(records: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    """Mark exact duplicates without discarding provenance rows.

    Prefer active records as canonical when an exact SHA appears in both tiers.
    Otherwise preserve first deterministic occurrence.
    """
    ordered = sorted(records, key=lambda r: (0 if r["library_tier"] == "active" else 1, r["record_id"]))
    by_sha: dict[str, str] = {}
    by_asset: dict[str, str] = {}
    duplicates = 0
    for row in ordered:
        key_sha = row["sha256"]
        key_asset = row["asset_path"]
        canonical = ""
        if key_sha and key_sha in by_sha:
            canonical = by_sha[key_sha]
        elif key_asset and key_asset in by_asset:
            canonical = by_asset[key_asset]
        if canonical:
            row["duplicate_of"] = canonical
            row["canonical_record_id"] = canonical
            duplicates += 1
        else:
            row["canonical_record_id"] = row["record_id"]
            if key_sha:
                by_sha[key_sha] = row["record_id"]
            if key_asset:
                by_asset[key_asset] = row["record_id"]
    return sorted(ordered, key=lambda r: (r["library_tier"], r["record_id"])), duplicates


def build(project: Path) -> tuple[list[dict[str, str]], dict]:
    records: list[dict[str, str]] = []
    baseline_rows = baseline_active_rows(project)
    for row in baseline_rows:
        records.append(normalize_baseline(row))

    active_sources = active_manifest_paths(project)
    for source in active_sources:
        for row in read_csv(source):
            records.append(normalize_active(row, source.relative_to(project)))

    zotero_source = project / "manifests" / "zotero-private-manifest.csv"
    zotero_rows = read_csv(zotero_source)
    for row in zotero_rows:
        records.append(normalize_zotero(row, zotero_source.relative_to(project)))

    records, duplicate_rows = dedupe(records)
    canonical = [r for r in records if not r["duplicate_of"]]
    active = [r for r in canonical if r["library_tier"] == "active"]
    reference = [r for r in canonical if r["library_tier"] == "reference"]

    qa = Counter(r["visual_qa_status"] or "unspecified" for r in reference)
    summary = {
        "schema_version": 1,
        "library": "unified_scientific_figure_library",
        "row_count_with_provenance_aliases": len(records),
        "canonical_record_count_exact_dedup": len(canonical),
        "exact_duplicate_alias_rows": duplicate_rows,
        "active_canonical_records": len(active),
        "reference_canonical_records": len(reference),
        "baseline_active_records": len(baseline_rows),
        "expected_baseline_active_records": 42,
        "expected_active_records": 96,
        "expected_zotero_source_rows": 139,
        "zotero_source_rows": len(zotero_rows),
        "reference_visual_qa_status_counts": dict(sorted(qa.items())),
        "cross_pool_perceptual_deduplication": "not_run",
        "retrieval_surface": "unified",
        "promotion_rule": "reference records require figure-level rights verification and completed visual QA before active promotion",
    }
    if len(baseline_rows) != 42:
        raise SystemExit(f"Expected 42 baseline active records, found {len(baseline_rows)}")
    if len(zotero_rows) != 139:
        raise SystemExit(f"Expected 139 Zotero rows, found {len(zotero_rows)}")
    if len(active) != 96:
        raise SystemExit(
            f"Expected 96 canonical active records, found {len(active)}. "
            "Review Stage 1.5 manifest overlap/dedup keys before accepting the unified index."
        )
    return records, summary


def write_outputs(project: Path, records: list[dict[str, str]], summary: dict) -> None:
    manifests = project / "manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    index_path = manifests / "unified-library-index.csv"
    with index_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=UNIFIED_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    (manifests / "unified-library-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def query(records: Iterable[dict[str, str]], text: str, include_reference: bool = True) -> list[dict[str, str]]:
    terms = [t.lower() for t in text.split() if t.strip()]
    ranked = []
    for row in records:
        if not include_reference and row["library_tier"] != "active":
            continue
        hay = " ".join(
            row.get(k, "")
            for k in ("journal", "article_title", "primary_purpose", "style_family", "layout", "topics", "notes")
        ).lower()
        score = sum(1 for term in terms if term in hay)
        if score:
            ranked.append((score, 1 if row["library_tier"] == "active" else 0, row))
    ranked.sort(key=lambda x: (-x[0], -x[1], x[2]["record_id"]))
    return [r for _, _, r in ranked]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=PROJECT_DEFAULT)
    ap.add_argument("--query", default="")
    ap.add_argument("--active-only", action="store_true")
    ap.add_argument("--limit", type=int, default=20)
    args = ap.parse_args()

    records, summary = build(args.project_root)
    write_outputs(args.project_root, records, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.query:
        hits = query(records, args.query, include_reference=not args.active_only)[: args.limit]
        print(json.dumps(hits, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
