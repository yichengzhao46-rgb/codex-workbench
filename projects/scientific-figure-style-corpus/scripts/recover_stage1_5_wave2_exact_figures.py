#!/usr/bin/env python3
"""Recover selected wave-2 figures whose numeric label collides with nested JATS figures."""
from __future__ import annotations

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

TARGETS = {("S15-015", "1"): "f1", ("S15-017", "1"): "f1"}


def truthy(v: str) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y"}


def active_count(path: Path) -> int:
    if not path.exists():
        return 0
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    return sum(1 for r in rows if r.get("style_learning_tier") in {"A_style_reference", "B_style_reference"})


def main() -> int:
    root = Path("projects/scientific-figure-style-corpus").resolve()
    screening = root / "annotations/stage1_5_wave2_figure_screening.csv"
    manifest = root / "manifests/stage1_5_wave2_harvested_figures.csv"
    report_path = root / "validation/stage1_5_wave2_harvest_report.json"
    status_path = root / "validation/stage1_5_status.json"
    fields = [
        "candidate_id", "year", "journal", "article_url", "figure_number",
        "style_learning_tier", "primary_purpose", "style_family", "layout_archetype",
        "domain_relevance_to_bath_rp", "rights_status", "license", "cloud_version",
        "figure_id", "caption", "source_media_url", "asset_path", "content_type",
        "size_bytes", "sha256", "inspection_status",
    ]

    selected = [r for r in csv.DictReader(screening.open(encoding="utf-8", newline="")) if truthy(r.get("public_mirror", ""))]
    existing = list(csv.DictReader(manifest.open(encoding="utf-8", newline=""))) if manifest.exists() else []
    existing_keys = {(r["candidate_id"], r["figure_number"]) for r in existing}

    session = requests.Session()
    session.headers.update({"User-Agent": "codex-workbench-stage1.5-recovery/0.1", "Accept-Language": "en-US,en;q=0.8"})
    failures = []

    for row in selected:
        key = (row["candidate_id"], row["figure_number"])
        if key not in TARGETS or key in existing_keys:
            continue
        try:
            m = re.search(r"(PMC\d+)", row["article_url"], re.I)
            if not m:
                raise RuntimeError("missing PMCID")
            pmcid = m.group(1).upper()
            version, meta = aws.choose_version(session, pmcid)
            allowed, lic = aws.allowed_license(meta)
            if not allowed:
                raise RuntimeError(f"AWS license not public-mirror compatible: {lic}")
            xml_url = aws.as_https(str(meta.get("xml_url") or ""))
            xr = session.get(xml_url, timeout=60); xr.raise_for_status()
            article = ET.fromstring(xr.content)
            wanted_id = TARGETS[key]
            target = next((f for f in article.findall(".//fig") if f.attrib.get("id") == wanted_id and aws.txt(f.find("caption"))), None)
            if target is None:
                raise RuntimeError(f"exact JATS figure id {wanted_id!r} with caption not found")
            caption = aws.txt(target.find("caption"))
            third = aws.risk(caption)
            if third:
                raise RuntimeError(f"third-party/tool-asset risk: {third}")
            graphic = target.find("graphic")
            href = graphic.attrib.get(aws.XLINK, "") if graphic is not None else ""
            mmap = aws.media_map(meta)
            media_url = aws.find_media(mmap, href)
            if not media_url:
                raise RuntimeError(f"no media URL matched href={href!r}")
            ir = session.get(media_url, timeout=60); ir.raise_for_status()
            data = ir.content
            suffix = PurePosixPath(urlparse(media_url).path).suffix.lower() or ".img"
            out_dir = root / "assets" / "stage1_5" / row["candidate_id"]
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{row['candidate_id']}_fig{row['figure_number']}{suffix}"
            out_path.write_bytes(data)
            existing.append({
                "candidate_id": row["candidate_id"], "year": row["year"], "journal": row["journal"],
                "article_url": row["article_url"], "figure_number": row["figure_number"],
                "style_learning_tier": row["style_learning_tier"], "primary_purpose": row["primary_purpose"],
                "style_family": row["style_family"], "layout_archetype": row["layout_archetype"],
                "domain_relevance_to_bath_rp": row["domain_relevance_to_bath_rp"], "rights_status": row["rights_status"],
                "license": lic, "cloud_version": version, "figure_id": wanted_id, "caption": caption,
                "source_media_url": media_url, "asset_path": str(out_path.relative_to(root)),
                "content_type": ir.headers.get("Content-Type", ""), "size_bytes": str(len(data)),
                "sha256": hashlib.sha256(data).hexdigest(),
                "inspection_status": "direct_contact_sheet_screened_then_exact_jats_aws_harvested",
            })
            existing_keys.add(key)
            print(f"RECOVERED {row['candidate_id']} Fig.{row['figure_number']} -> {out_path.name}")
        except Exception as exc:  # noqa: BLE001
            failures.append({"candidate_id": row["candidate_id"], "figure_number": row["figure_number"], "error": str(exc)})
            print(f"FAILED {row['candidate_id']} Fig.{row['figure_number']}: {exc}")

    existing.sort(key=lambda r: (r["candidate_id"], int(r["figure_number"])))
    with manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(existing)

    report = {
        "wave": 2,
        "screened_figure_rows": sum(1 for _ in csv.DictReader(screening.open(encoding="utf-8", newline=""))),
        "public_mirror_selected": len(selected),
        "harvested_assets": len(existing),
        "failed_or_rejected": len(failures),
        "tier_counts": dict(Counter(r["style_learning_tier"] for r in existing)),
        "journal_counts": dict(Counter(r["journal"] for r in existing)),
        "failures": failures,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    wave1 = active_count(root / "manifests/stage1_5_harvested_figures.csv")
    wave2 = active_count(manifest)
    status = {
        "stage": "1.5_recent_targeted_refinement", "stage1_ab_baseline": 42,
        "wave1_active_ab_added": wave1, "wave2_active_ab_added": wave2,
        "current_ab_after_wave2": 42 + wave1 + wave2,
        "target_ab_range": [80, 100], "target_new_figures_range": [40, 60],
        "wave2_screened_figures": report["screened_figure_rows"], "wave2_public_assets": len(existing),
        "next_action": "expand wave3 recent OA candidates and prioritize mechanism/material-interface/environmental-gradient gaps",
    }
    status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(status, indent=2, ensure_ascii=False))
    return 0 if len(existing) == len(selected) and not failures else 2

if __name__ == "__main__":
    raise SystemExit(main())
