#!/usr/bin/env python3
"""Resume the rights-aware scientific-figure corpus from committed checkpoints.

Unlike build_raw_corpus.py, this entry point loads an existing manifest/assets tree,
keeps valid rows, and only downloads figures needed to reach an absolute target.
It is designed for GitHub Actions batch checkpoints (for example 10 images per
batch) so a timeout or cancellation loses at most the current small batch.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Importing the scoped wrapper mutates build_raw_corpus.SOURCES to the curated
# allow-list used by this project, including the selected Nature/Science/Cell pool.
import run_raw_corpus_scoped as scoped  # noqa: F401
import build_raw_corpus as b

FIELDS = [
    "sample_id", "journal", "journal_slug", "source_tier", "year", "article_title", "doi", "pmcid",
    "figure_id", "article_url", "source_image_url", "resolved_image_url", "license", "license_url",
    "rights_status", "third_party_review", "caption_score", "caption", "asset_path", "content_type",
    "size_bytes", "sha256", "inspection_status",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", default="projects/scientific-figure-style-corpus")
    p.add_argument("--target-total", type=int, required=True, help="Absolute corpus size to reach in this batch")
    p.add_argument("--retmax", type=int, default=400)
    p.add_argument("--max-per-article", type=int, default=2)
    p.add_argument("--min-score", type=int, default=4)
    p.add_argument("--polite-delay", type=float, default=0.14)
    p.add_argument("--max-image-bytes", type=int, default=12_000_000)
    return p.parse_args()


def valid_existing_rows(root: Path, manifest_path: Path) -> list[dict[str, str]]:
    if not manifest_path.exists():
        return []
    with manifest_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    valid: list[dict[str, str]] = []
    for row in rows:
        rel = row.get("asset_path", "")
        sha = row.get("sha256", "")
        if not rel or not sha:
            continue
        path = root / rel
        if not path.exists() or not path.is_file():
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
            continue
        if row.get("rights_status") != "mirror_allowed_ccby_or_cc0":
            continue
        valid.append(row)
    return valid


def max_ordinal(rows: list[dict[str, str]], slug: str) -> int:
    pat = re.compile(rf"^{re.escape(slug)}-(\d+)-")
    values = []
    for row in rows:
        m = pat.match(row.get("sample_id", ""))
        if m:
            values.append(int(m.group(1)))
    return max(values, default=0)


def write_state(root: Path, rows: list[dict[str, str]], report: dict[str, object], target: int, start_count: int) -> None:
    manifest_path = root / "manifests" / "raw-image-manifest.csv"
    report_path = root / "validation" / "raw-corpus-build-report.json"
    progress_path = root / "validation" / "raw-corpus-progress.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    by_journal = Counter(r.get("journal_slug", "") for r in rows)
    report["downloaded_total"] = len(rows)
    report["downloaded_new_this_batch"] = max(0, len(rows) - start_count)
    report["distinct_articles"] = len({r.get("pmcid", "") for r in rows if r.get("pmcid")})
    report["represented_journals"] = sorted(k for k in by_journal if k)
    report["core_images"] = sum(1 for r in rows if r.get("source_tier") == "core")
    report["manifest"] = str(manifest_path.relative_to(root))
    report["assets_root"] = "assets/raw"
    report["checkpoint_target"] = target
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    progress = {
        "count": len(rows),
        "target": 100,
        "batch_target": target,
        "batch_start_count": start_count,
        "new_this_batch": max(0, len(rows) - start_count),
        "distinct_articles": report["distinct_articles"],
        "core_images": report["core_images"],
        "journals": dict(sorted(by_journal.items())),
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    progress_path.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")


def build(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    assets_root = root / "assets" / "raw"
    manifest_path = root / "manifests" / "raw-image-manifest.csv"
    assets_root.mkdir(parents=True, exist_ok=True)

    rows = valid_existing_rows(root, manifest_path)
    start_count = len(rows)
    if start_count >= args.target_total:
        print(f"checkpoint already satisfied: {start_count}/{args.target_total}", flush=True)
        return 0

    session = b.requests.Session()
    session.headers.update({
        "User-Agent": b.USER_AGENT,
        "Accept-Language": "en-US,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8",
    })

    by_slug = Counter(r.get("journal_slug", "") for r in rows)
    report: dict[str, object] = {
        "target_total": args.target_total,
        "resume_start_count": start_count,
        "journals": {},
        "errors": [],
        "source_policy": {
            "core_journals_prioritized": True,
            "fixed_water_research_quota": False,
            "scope_high_fill_allowed": True,
            "resumable_checkpoint_build": True,
        },
    }

    global_article_count: dict[str, int] = defaultdict(int)
    seen_figures: set[tuple[str, str]] = set()
    journal_ordinals: dict[str, int] = defaultdict(int)
    for row in rows:
        pmcid = row.get("pmcid", "")
        figid = row.get("figure_id", "")
        if pmcid:
            global_article_count[pmcid] += 1
        if pmcid and figid:
            seen_figures.add((pmcid, figid))
    for source in b.SOURCES:
        slug = str(source.get("slug", ""))
        journal_ordinals[slug] = max_ordinal(rows, slug)
        report["journals"][slug] = {
            "tier": source["tier"],
            "first_pass_cap": source["first_pass_cap"],
            "max_cap": source["max_cap"],
            "downloaded": int(by_slug.get(slug, 0)),
            "articles_examined": 0,
            "license_rejected": 0,
            "third_party_rejected": 0,
            "download_failed": 0,
        }

    source_cache: dict[str, list[str]] = {}

    def process_source(source: dict[str, object], cap: int) -> None:
        if len(rows) >= args.target_total:
            return
        slug = str(source["slug"])
        cfg = report["journals"][slug]
        if int(cfg["downloaded"]) >= cap:
            return
        if slug not in source_cache:
            try:
                source_cache[slug] = b.esearch(session, str(source["journal_query"]), retmax=args.retmax)
            except Exception as exc:  # noqa: BLE001
                report["errors"].append(f"{slug}: esearch failed: {exc}")
                source_cache[slug] = []
                return

        pmcids = source_cache[slug]
        for pmcid in pmcids:
            if len(rows) >= args.target_total or int(cfg["downloaded"]) >= cap:
                break
            if global_article_count[pmcid] >= args.max_per_article:
                continue
            article_url = b.PMC_ARTICLE.format(pmcid=pmcid)
            try:
                html = b.http_get(session, article_url).text
            except Exception as exc:  # noqa: BLE001
                report["errors"].append(f"{pmcid}: article fetch failed: {exc}")
                continue
            cfg["articles_examined"] = int(cfg["articles_examined"]) + 1
            soup = b.BeautifulSoup(html, "html.parser")
            allowed, license_name, license_url = b.detect_license(soup)
            if not allowed:
                cfg["license_rejected"] = int(cfg["license_rejected"]) + 1
                time.sleep(args.polite_delay)
                continue
            figs = b.extract_figures(
                soup, slug, str(source["journal_label"]), str(source["tier"]), pmcid,
                article_url, license_name, license_url,
            )
            if not figs:
                time.sleep(args.polite_delay)
                continue

            selected_from_article = global_article_count[pmcid]
            for fig in b.iter_ranked(figs):
                if len(rows) >= args.target_total or int(cfg["downloaded"]) >= cap or selected_from_article >= args.max_per_article:
                    break
                key = (fig.pmcid, fig.figure_id)
                if key in seen_figures:
                    continue
                if fig.third_party_risk:
                    cfg["third_party_rejected"] = int(cfg["third_party_rejected"]) + 1
                    continue
                remaining_needed = args.target_total - len(rows)
                remaining_articles = max(1, len(pmcids) - int(cfg["articles_examined"]))
                if remaining_articles > remaining_needed and fig.score < args.min_score:
                    continue
                journal_ordinals[slug] += 1
                try:
                    out_path, sha, size_bytes, content_type, resolved_url = b.download_figure(
                        session, fig, assets_root, journal_ordinals[slug], args.max_image_bytes,
                    )
                except Exception as exc:  # noqa: BLE001
                    cfg["download_failed"] = int(cfg["download_failed"]) + 1
                    report["errors"].append(f"{pmcid} {fig.figure_id}: download failed: {exc}")
                    continue

                cfg["downloaded"] = int(cfg["downloaded"]) + 1
                selected_from_article += 1
                global_article_count[pmcid] += 1
                seen_figures.add(key)
                rows.append({
                    "sample_id": out_path.stem,
                    "journal": fig.journal_label,
                    "journal_slug": slug,
                    "source_tier": fig.source_tier,
                    "year": fig.publication_year,
                    "article_title": fig.article_title,
                    "doi": fig.doi,
                    "pmcid": fig.pmcid,
                    "figure_id": fig.figure_id,
                    "article_url": fig.article_url,
                    "source_image_url": fig.image_url,
                    "resolved_image_url": resolved_url,
                    "license": fig.license_name,
                    "license_url": fig.license_url,
                    "rights_status": "mirror_allowed_ccby_or_cc0",
                    "third_party_review": "caption_screen_pass",
                    "caption_score": str(fig.score),
                    "caption": fig.caption,
                    "asset_path": str(out_path.relative_to(root)),
                    "content_type": content_type,
                    "size_bytes": str(size_bytes),
                    "sha256": sha,
                    "inspection_status": "downloaded_unannotated",
                })
                # Keep local state current after every successful image. The
                # workflow commits it after each batch checkpoint.
                write_state(root, rows, report, args.target_total, start_count)
                print(
                    f"[{slug}] checkpoint-build overall={len(rows)}/{args.target_total} "
                    f"global_target=100 {pmcid} {fig.figure_id} score={fig.score} -> {out_path.name}",
                    flush=True,
                )
                time.sleep(args.polite_delay)
            time.sleep(args.polite_delay)

    for source in b.SOURCES:
        process_source(source, int(source["first_pass_cap"]))
        if len(rows) >= args.target_total:
            break
    if len(rows) < args.target_total:
        for source in b.SOURCES:
            process_source(source, int(source["max_cap"]))
            if len(rows) >= args.target_total:
                break

    write_state(root, rows, report, args.target_total, start_count)
    print(
        json.dumps({
            "checkpoint_start": start_count,
            "checkpoint_end": len(rows),
            "checkpoint_target": args.target_total,
            "distinct_articles": len({r.get('pmcid', '') for r in rows if r.get('pmcid')}),
        }, indent=2),
        flush=True,
    )
    return 0 if len(rows) >= args.target_total else 2


if __name__ == "__main__":
    sys.exit(build(parse_args()))
