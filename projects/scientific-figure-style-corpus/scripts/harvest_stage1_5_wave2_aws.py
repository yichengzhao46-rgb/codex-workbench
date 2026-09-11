#!/usr/bin/env python3
"""Harvest visually screened Stage 1.5 wave-2 figures from the official PMC AWS dataset."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import scan_stage1_5_wave2_oa_package as aws  # noqa: E402

FIELDS = [
    "candidate_id", "year", "journal", "article_url", "figure_number",
    "style_learning_tier", "primary_purpose", "style_family", "layout_archetype",
    "domain_relevance_to_bath_rp", "rights_status", "license", "cloud_version",
    "figure_id", "caption", "source_media_url", "asset_path", "content_type",
    "size_bytes", "sha256", "inspection_status",
]


def truthy(v: str) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y"}


def active_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return sum(1 for r in rows if r.get("style_learning_tier") in {"A_style_reference", "B_style_reference"})


def mime_from_suffix(suffix: str) -> str:
    return {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".webp": "image/webp", ".gif": "image/gif", ".tif": "image/tiff", ".tiff": "image/tiff",
    }.get(suffix.lower(), "application/octet-stream")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default="projects/scientific-figure-style-corpus")
    ap.add_argument("--selection", default="projects/scientific-figure-style-corpus/annotations/stage1_5_wave2_figure_screening.csv")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    selection = Path(args.selection).resolve()
    assets_root = root / "assets" / "stage1_5"
    manifest = root / "manifests" / "stage1_5_wave2_harvested_figures.csv"
    report_path = root / "validation" / "stage1_5_wave2_harvest_report.json"
    status_path = root / "validation" / "stage1_5_status.json"
    assets_root.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with selection.open(encoding="utf-8", newline="") as f:
        all_rows = list(csv.DictReader(f))
    selected = [r for r in all_rows if truthy(r.get("public_mirror", ""))]

    session = requests.Session()
    session.headers.update({"User-Agent": "codex-workbench-stage1.5-harvest/0.3", "Accept-Language": "en-US,en;q=0.8"})

    harvested = []
    failures = []
    cache: dict[str, tuple[str, dict, ET.Element, dict[str, str], str]] = {}

    for row in selected:
        cid = row["candidate_id"]
        fnum = int(row["figure_number"])
        url = row["article_url"]
        try:
            if row.get("rights_status") != "public_mirror_allowed_cc_by":
                raise RuntimeError("selection row is not public-mirror compatible")
            m = re.search(r"(PMC\d+)", url, re.I)
            if not m:
                raise RuntimeError("selected row lacks PMCID")
            pmcid = m.group(1).upper()

            if pmcid not in cache:
                version, meta = aws.choose_version(session, pmcid)
                allowed, lic = aws.allowed_license(meta)
                if not allowed:
                    raise RuntimeError(f"AWS license not public-mirror compatible: {lic}")
                xml_url = aws.as_https(str(meta.get("xml_url") or ""))
                if not xml_url:
                    raise RuntimeError("AWS metadata has no xml_url")
                xr = session.get(xml_url, timeout=60)
                xr.raise_for_status()
                article = ET.fromstring(xr.content)
                mmap = aws.media_map(meta)
                cache[pmcid] = (version, meta, article, mmap, lic)
            version, meta, article, mmap, lic = cache[pmcid]

            target = None
            for ordinal, fig in enumerate(article.findall(".//fig"), 1):
                label = aws.txt(fig.find("label"))
                nm = re.search(r"(\d+)", label)
                num = int(nm.group(1)) if nm else ordinal
                if num == fnum:
                    target = fig
                    break
            if target is None:
                raise RuntimeError(f"figure {fnum} not found in JATS XML")

            caption = aws.txt(target.find("caption"))
            if not caption:
                raise RuntimeError("empty figure caption")
            third = aws.risk(caption)
            if third:
                raise RuntimeError(f"third-party/tool-asset risk: {third}")
            graphic = target.find("graphic")
            href = graphic.attrib.get(aws.XLINK, "") if graphic is not None else ""
            media_url = aws.find_media(mmap, href)
            if not media_url:
                raise RuntimeError(f"no media URL matched JATS graphic href={href!r}")

            ir = session.get(media_url, timeout=60)
            ir.raise_for_status()
            data = ir.content
            if not data:
                raise RuntimeError("empty media response")
            suffix = PurePosixPath(urlparse(media_url).path).suffix.lower() or ".img"
            out_dir = assets_root / cid
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{cid}_fig{fnum}{suffix}"
            out_path.write_bytes(data)
            digest = hashlib.sha256(data).hexdigest()

            harvested.append({
                "candidate_id": cid, "year": row["year"], "journal": row["journal"],
                "article_url": url, "figure_number": str(fnum),
                "style_learning_tier": row["style_learning_tier"],
                "primary_purpose": row["primary_purpose"], "style_family": row["style_family"],
                "layout_archetype": row["layout_archetype"],
                "domain_relevance_to_bath_rp": row["domain_relevance_to_bath_rp"],
                "rights_status": row["rights_status"], "license": lic, "cloud_version": version,
                "figure_id": target.attrib.get("id", f"fig{fnum}"), "caption": caption,
                "source_media_url": media_url, "asset_path": str(out_path.relative_to(root)),
                "content_type": ir.headers.get("Content-Type", "") or mime_from_suffix(suffix),
                "size_bytes": str(len(data)), "sha256": digest,
                "inspection_status": "direct_contact_sheet_screened_then_aws_harvested",
            })
            print(f"HARVESTED {cid} Fig.{fnum} -> {out_path.name}", flush=True)
        except Exception as exc:  # noqa: BLE001
            failures.append({"candidate_id": cid, "figure_number": str(fnum), "error": str(exc)})
            print(f"SKIPPED {cid} Fig.{fnum}: {exc}", flush=True)

    with manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(harvested)

    tier_counts = Counter(r["style_learning_tier"] for r in harvested)
    active_added = sum(1 for r in harvested if r["style_learning_tier"] in {"A_style_reference", "B_style_reference"})
    report = {
        "wave": 2,
        "screened_figure_rows": len(all_rows),
        "public_mirror_selected": len(selected),
        "harvested_assets": len(harvested),
        "failed_or_rejected": len(failures),
        "tier_counts": dict(tier_counts),
        "journal_counts": dict(Counter(r["journal"] for r in harvested)),
        "failures": failures,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    wave1_active = active_count(root / "manifests" / "stage1_5_harvested_figures.csv")
    wave2_active = active_count(manifest)
    status = {
        "stage": "1.5_recent_targeted_refinement",
        "stage1_ab_baseline": 42,
        "wave1_active_ab_added": wave1_active,
        "wave2_active_ab_added": wave2_active,
        "current_ab_after_wave2": 42 + wave1_active + wave2_active,
        "target_ab_range": [80, 100],
        "target_new_figures_range": [40, 60],
        "wave2_screened_figures": len(all_rows),
        "wave2_public_assets": len(harvested),
        "next_action": "expand wave3 recent OA candidates and prioritize mechanism/material-interface/environmental-gradient gaps",
    }
    status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
    print(json.dumps(status, indent=2, ensure_ascii=False), flush=True)
    return 0 if harvested else 2


if __name__ == "__main__":
    raise SystemExit(main())
