#!/usr/bin/env python3
"""Harvest manually screened Stage 1.5 figures from redistribution-compatible PMC articles.

The selection manifest is human/visual-QA driven. This script only mirrors rows
marked public_mirror=true, re-checks article-level CC licensing and caption-level
third-party/BioRender risk, resolves the original image bytes, computes SHA256,
and writes a harvest manifest plus status report.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import build_raw_corpus as b  # noqa: E402

EXTRA_THIRD_PARTY_TERMS = (
    "biorender",
    "created with biorender",
    "reproduced with permission",
    "adapted with permission",
)

OUTPUT_FIELDS = [
    "candidate_id", "year", "journal", "article_url", "figure_number",
    "style_learning_tier", "primary_purpose", "style_family", "layout_archetype",
    "domain_relevance_to_bath_rp", "license", "license_url", "figure_id",
    "caption", "source_image_url", "resolved_image_url", "asset_path",
    "content_type", "size_bytes", "sha256", "inspection_status",
]


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def caption_text(fig) -> str:
    node = fig.find("figcaption") or fig.find(class_=re.compile("caption", re.I))
    return b.text_or_empty(node)


def find_figure(soup: BeautifulSoup, figure_number: int):
    figures = list(soup.find_all("figure"))
    patterns = [
        re.compile(rf"^\s*Fig(?:ure)?\.?\s*{figure_number}\b", re.I),
        re.compile(rf"^\s*Figure\s*{figure_number}\b", re.I),
    ]
    for fig in figures:
        cap = caption_text(fig)
        if any(p.search(cap) for p in patterns):
            return fig
        fid = str(fig.get("id") or "").lower().replace("-", "")
        if fid in {f"fig{figure_number}", f"f{figure_number}"}:
            return fig
    # Last-resort ordinal fallback is acceptable only for PMC main-text figures.
    if 1 <= figure_number <= len(figures):
        return figures[figure_number - 1]
    return None


def third_party_reason(caption: str) -> str:
    reasons = []
    base = b.has_third_party_risk(caption)
    if base:
        reasons.append(base)
    low = caption.lower()
    for term in EXTRA_THIRD_PARTY_TERMS:
        if term in low and term not in reasons:
            reasons.append(term)
    return "; ".join(reasons)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default="projects/scientific-figure-style-corpus")
    ap.add_argument(
        "--selection",
        default="projects/scientific-figure-style-corpus/annotations/stage1_5_wave1_figure_screening.csv",
    )
    ap.add_argument("--max-image-bytes", type=int, default=15_000_000)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    selection = Path(args.selection).resolve()
    assets_root = root / "assets" / "stage1_5"
    out_manifest = root / "manifests" / "stage1_5_harvested_figures.csv"
    report_path = root / "validation" / "stage1_5_harvest_report.json"
    status_path = root / "validation" / "stage1_5_status.json"
    assets_root.mkdir(parents=True, exist_ok=True)
    out_manifest.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with selection.open(encoding="utf-8", newline="") as f:
        screened = list(csv.DictReader(f))
    mirror_rows = [r for r in screened if truthy(r.get("public_mirror", ""))]

    session = requests.Session()
    session.headers.update({
        "User-Agent": b.USER_AGENT,
        "Accept-Language": "en-US,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,image/webp,image/png,image/jpeg,*/*;q=0.8",
    })

    harvested: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []

    for row in mirror_rows:
        cid = row["candidate_id"]
        url = row["article_url"]
        fnum = int(row["figure_number"])
        try:
            if "pmc.ncbi.nlm.nih.gov/articles/" not in url:
                raise RuntimeError("public mirroring currently requires a PMC full-text URL")
            html = b.http_get(session, url).text
            soup = BeautifulSoup(html, "html.parser")
            allowed, license_name, license_url = b.detect_license(soup)
            if not allowed:
                raise RuntimeError("article does not expose an allowed CC BY/CC0 licence")

            fig = find_figure(soup, fnum)
            if fig is None:
                raise RuntimeError(f"figure {fnum} not found")
            caption = caption_text(fig)
            if not caption:
                raise RuntimeError("figure caption is empty")
            risk = third_party_reason(caption)
            if risk:
                raise RuntimeError(f"caption third-party/tool-asset risk: {risk}")

            article_id_match = re.search(r"/articles/(PMC\d+)/", url, re.I)
            pmcid = article_id_match.group(1).upper() if article_id_match else ""
            image_url = b.pick_image_url(fig, url)
            if not image_url:
                raise RuntimeError("no image URL exposed by figure node")
            fig_id = str(fig.get("id") or f"fig{fnum}")
            figure_page = urljoin(url, f"figure/{fig_id}/")
            initial_urls = [image_url, figure_page]
            filename = b.wrapper_filename(image_url)
            if filename and pmcid:
                initial_urls = b.direct_pmc_bin_candidates(pmcid, filename) + initial_urls
            data, resolved_url, ctype = b.resolve_image_bytes(
                session, initial_urls, pmcid, args.max_image_bytes
            )
            ext = b.ext_from_response(resolved_url, ctype)
            out_dir = assets_root / cid
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{cid}_fig{fnum}{ext}"
            out_path.write_bytes(data)
            sha = hashlib.sha256(data).hexdigest()

            harvested.append({
                "candidate_id": cid,
                "year": row["year"],
                "journal": row["journal"],
                "article_url": url,
                "figure_number": str(fnum),
                "style_learning_tier": row["style_learning_tier"],
                "primary_purpose": row["primary_purpose"],
                "style_family": row["style_family"],
                "layout_archetype": row["layout_archetype"],
                "domain_relevance_to_bath_rp": row["domain_relevance_to_bath_rp"],
                "license": license_name,
                "license_url": license_url,
                "figure_id": fig_id,
                "caption": caption,
                "source_image_url": image_url,
                "resolved_image_url": resolved_url,
                "asset_path": str(out_path.relative_to(root)),
                "content_type": ctype,
                "size_bytes": str(len(data)),
                "sha256": sha,
                "inspection_status": "screened_then_harvested",
            })
            print(f"HARVESTED {cid} Fig.{fnum} -> {out_path.name}", flush=True)
        except Exception as exc:  # noqa: BLE001
            failures.append({
                "candidate_id": cid,
                "figure_number": str(fnum),
                "article_url": url,
                "error": str(exc),
            })
            print(f"SKIPPED {cid} Fig.{fnum}: {exc}", flush=True)

    with out_manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        w.writeheader()
        w.writerows(harvested)

    tier_counts = Counter(r["style_learning_tier"] for r in harvested)
    journal_counts = Counter(r["journal"] for r in harvested)
    active_added = sum(
        1 for r in harvested if r["style_learning_tier"] in {"A_style_reference", "B_style_reference"}
    )
    report = {
        "screened_figure_rows": len(screened),
        "public_mirror_requested": len(mirror_rows),
        "harvested_assets": len(harvested),
        "failed_or_rejected": len(failures),
        "tier_counts": dict(tier_counts),
        "journal_counts": dict(journal_counts),
        "failures": failures,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    status = {
        "stage": "1.5_recent_targeted_refinement",
        "verified_candidate_articles_wave1": 9,
        "screened_figure_rows_wave1": len(screened),
        "public_assets_wave1": len(harvested),
        "wave1_active_ab_added": active_added,
        "stage1_ab_baseline": 42,
        "current_ab_after_wave1": 42 + active_added,
        "target_ab_range": [80, 100],
        "target_new_figures_range": [40, 60],
        "next_action": "expand and screen wave2 recent OA candidates",
    }
    status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)

    # A zero-asset result almost certainly means the harvester is broken.
    return 0 if harvested else 2


if __name__ == "__main__":
    raise SystemExit(main())
