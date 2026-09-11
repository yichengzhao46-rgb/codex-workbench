#!/usr/bin/env python3
"""Filter and merge a previous raw-corpus artifact with a fresh incremental build.

This keeps useful downloads from an older GitHub Actions run while enforcing the
current journal scope. Old records are accepted only when the source journal is
still allowed, the asset exists, and its SHA256 matches the manifest. The final
merge de-duplicates by (PMCID, figure_id) and asset hash, prefers core/high-value
sources and mechanistic-caption scores, and writes a clean 100-image corpus.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

import run_raw_corpus_scoped as scoped

ALLOWED_SLUGS = {str(s.get("slug", "")) for s in scoped.builder.SOURCES}
CORE_SLUGS = {str(s.get("slug", "")) for s in scoped.builder.SOURCES if s.get("tier") == "core"}


def locate_project_root(root: Path) -> Path | None:
    direct = root / "manifests" / "raw-image-manifest.csv"
    if direct.exists():
        return root
    hits = list(root.rglob("raw-image-manifest.csv"))
    if not hits:
        return None
    return hits[0].parent.parent


def read_rows(project_root: Path) -> list[dict[str, str]]:
    manifest = project_root / "manifests" / "raw-image-manifest.csv"
    if not manifest.exists():
        return []
    with manifest.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def asset_ok(project_root: Path, row: dict[str, str]) -> bool:
    rel = row.get("asset_path", "")
    sha = row.get("sha256", "")
    if not rel or not sha:
        return False
    path = project_root / rel
    if not path.exists() or not path.is_file():
        return False
    return hashlib.sha256(path.read_bytes()).hexdigest() == sha


def rights_ok(row: dict[str, str]) -> bool:
    rights = row.get("rights_status", "")
    return rights == "mirror_allowed_ccby_or_cc0"


def filter_rows(project_root: Path) -> list[dict[str, str]]:
    out = []
    for row in read_rows(project_root):
        if row.get("journal_slug", "") not in ALLOWED_SLUGS:
            continue
        if not rights_ok(row):
            continue
        if not asset_ok(project_root, row):
            continue
        out.append(row)
    return out


def priority(row: dict[str, str]) -> tuple[int, int, int]:
    slug = row.get("journal_slug", "")
    tier = row.get("source_tier", "")
    if slug in CORE_SLUGS or tier == "core":
        tier_score = 4
    elif tier in {"elite-general", "elite-scope"}:
        tier_score = 3
    elif tier == "scope-high":
        tier_score = 2
    else:
        tier_score = 1
    try:
        caption_score = int(row.get("caption_score", "0") or 0)
    except ValueError:
        caption_score = 0
    try:
        size_score = min(int(row.get("size_bytes", "0") or 0) // 100_000, 20)
    except ValueError:
        size_score = 0
    return tier_score, caption_score, size_score


def copy_selected(source_root: Path, rows: list[dict[str, str]], output_root: Path) -> list[dict[str, str]]:
    copied = []
    for row in rows:
        src = source_root / row["asset_path"]
        dst = output_root / row["asset_path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(dict(row))
    return copied


def write_manifest(output_root: Path, rows: list[dict[str, str]]) -> None:
    manifest = output_root / "manifests" / "raw-image-manifest.csv"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    preferred = [
        "sample_id", "journal", "journal_slug", "source_tier", "year", "article_title", "doi", "pmcid",
        "figure_id", "article_url", "source_image_url", "resolved_image_url", "license", "license_url",
        "rights_status", "third_party_review", "caption_score", "caption", "asset_path", "content_type",
        "size_bytes", "sha256", "inspection_status",
    ]
    extras = sorted({k for row in rows for k in row} - set(preferred))
    fields = preferred + extras
    with manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def cmd_seed(args: argparse.Namespace) -> int:
    artifact_root = Path(args.artifact_root).resolve()
    output_root = Path(args.output_root).resolve()
    project_root = locate_project_root(artifact_root)
    if project_root is None:
        print(json.dumps({"seed_count": 0, "reason": "no manifest found"}))
        return 0
    rows = filter_rows(project_root)
    rows.sort(key=priority, reverse=True)
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    copied = copy_selected(project_root, rows, output_root)
    write_manifest(output_root, copied)
    summary = {
        "seed_count": len(copied),
        "distinct_articles": len({r.get("pmcid", "") for r in copied if r.get("pmcid")}),
        "core_count": sum(1 for r in copied if r.get("journal_slug") in CORE_SLUGS or r.get("source_tier") == "core"),
        "journals": dict(Counter(r.get("journal_slug", "") for r in copied)),
    }
    (output_root / "seed-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))
    return 0


def cmd_merge(args: argparse.Namespace) -> int:
    seed_root = Path(args.seed_root).resolve()
    increment_root = Path(args.increment_root).resolve()
    output_root = Path(args.output_root).resolve()
    target = args.target

    candidates: list[tuple[dict[str, str], Path]] = []
    for root in (seed_root, increment_root):
        if not (root / "manifests" / "raw-image-manifest.csv").exists():
            continue
        for row in filter_rows(root):
            candidates.append((row, root))

    candidates.sort(key=lambda x: priority(x[0]), reverse=True)
    selected: list[tuple[dict[str, str], Path]] = []
    seen_figs: set[tuple[str, str]] = set()
    seen_sha: set[str] = set()
    per_article: Counter[str] = Counter()

    for row, root in candidates:
        key = (row.get("pmcid", ""), row.get("figure_id", ""))
        sha = row.get("sha256", "")
        pmcid = row.get("pmcid", "")
        if key in seen_figs or sha in seen_sha:
            continue
        if pmcid and per_article[pmcid] >= 2:
            continue
        selected.append((row, root))
        seen_figs.add(key)
        seen_sha.add(sha)
        if pmcid:
            per_article[pmcid] += 1
        if len(selected) >= target:
            break

    # If the first pass is short because of the 2/article preference, permit a
    # third image only when needed to reach the raw-image gate.
    if len(selected) < target:
        chosen_ids = {(r.get("pmcid", ""), r.get("figure_id", "")) for r, _ in selected}
        for row, root in candidates:
            key = (row.get("pmcid", ""), row.get("figure_id", ""))
            sha = row.get("sha256", "")
            pmcid = row.get("pmcid", "")
            if key in chosen_ids or sha in seen_sha:
                continue
            if pmcid and per_article[pmcid] >= 3:
                continue
            selected.append((row, root))
            chosen_ids.add(key)
            seen_sha.add(sha)
            if pmcid:
                per_article[pmcid] += 1
            if len(selected) >= target:
                break

    if output_root.exists():
        assets = output_root / "assets" / "raw"
        if assets.exists():
            shutil.rmtree(assets)
    output_root.mkdir(parents=True, exist_ok=True)

    final_rows = []
    for row, root in selected:
        final_rows.extend(copy_selected(root, [row], output_root))
    write_manifest(output_root, final_rows)

    summary = {
        "target": target,
        "selected": len(final_rows),
        "distinct_articles": len({r.get("pmcid", "") for r in final_rows if r.get("pmcid")}),
        "core_count": sum(1 for r in final_rows if r.get("journal_slug") in CORE_SLUGS or r.get("source_tier") == "core"),
        "journals": dict(Counter(r.get("journal_slug", "") for r in final_rows)),
        "seed_candidates": len(filter_rows(seed_root)) if (seed_root / "manifests" / "raw-image-manifest.csv").exists() else 0,
        "increment_candidates": len(filter_rows(increment_root)) if (increment_root / "manifests" / "raw-image-manifest.csv").exists() else 0,
    }
    validation_dir = output_root / "validation"
    validation_dir.mkdir(parents=True, exist_ok=True)
    (validation_dir / "raw-corpus-merge-report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if len(final_rows) >= target else 2


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("seed")
    s.add_argument("--artifact-root", required=True)
    s.add_argument("--output-root", required=True)

    m = sub.add_parser("merge")
    m.add_argument("--seed-root", required=True)
    m.add_argument("--increment-root", required=True)
    m.add_argument("--output-root", required=True)
    m.add_argument("--target", type=int, default=100)
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.command == "seed":
        raise SystemExit(cmd_seed(args))
    raise SystemExit(cmd_merge(args))
