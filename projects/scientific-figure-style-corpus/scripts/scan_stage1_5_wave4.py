#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import build_raw_corpus as b
import harvest_stage1_5 as h
import scan_stage1_5_wave2 as base


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default="projects/scientific-figure-style-corpus")
    ap.add_argument("--candidates", default="projects/scientific-figure-style-corpus/manifests/stage1_5_wave4_candidates.csv")
    ap.add_argument("--max-image-bytes", type=int, default=15_000_000)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    candidates = Path(args.candidates).resolve()
    scan_dir = root / "validation" / "stage1_5_wave4_scan"
    preview_root = scan_dir / "previews"
    contact_root = scan_dir / "contact_sheets"
    scan_dir.mkdir(parents=True, exist_ok=True)
    preview_root.mkdir(parents=True, exist_ok=True)
    contact_root.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(candidates.open(encoding="utf-8", newline="")))
    session = requests.Session()
    session.headers.update({"User-Agent": b.USER_AGENT, "Accept-Language": "en-US,en;q=0.8"})

    scanned = []
    summary = {
        "articles_total": len(rows), "articles_scanned": 0, "figures_scanned": 0,
        "previews_resolved": 0, "metadata_only": 0, "article_failures": []
    }

    for row in rows:
        cid = row["candidate_id"]
        url = row["url"]
        if "pmc.ncbi.nlm.nih.gov/articles/" not in url:
            summary["metadata_only"] += 1
            continue
        try:
            html = b.http_get(session, url).text
            soup = BeautifulSoup(html, "html.parser")
            allowed, lic, lic_url = b.detect_license(soup)
            figures = list(soup.find_all("figure")) or list(soup.find_all("div", class_=re.compile(r"\bfig\b", re.I)))
            article_previews = []
            article_count = 0
            for ordinal, fig in enumerate(figures, 1):
                cap = h.caption_text(fig)
                if not cap:
                    continue
                article_count += 1
                fnum = base.figure_number(fig, ordinal)
                risk = h.third_party_reason(cap)
                score = base.score_caption(cap)
                preview_rel = ""
                resolved = False
                if allowed and not risk:
                    pmcid_m = re.search(r"/articles/(PMC\d+)/", url, re.I)
                    pmcid = pmcid_m.group(1).upper() if pmcid_m else ""
                    candidate_urls = h.preferred_image_candidates(fig, url, pmcid)
                    try:
                        data, resolved_url, ctype = b.resolve_image_bytes(session, candidate_urls, pmcid, args.max_image_bytes)
                        ext = b.ext_from_response(resolved_url, ctype)
                        out_dir = preview_root / cid
                        out_dir.mkdir(parents=True, exist_ok=True)
                        p = out_dir / f"{cid}_fig{fnum}{ext}"
                        p.write_bytes(data)
                        preview_rel = str(p.relative_to(root))
                        resolved = True
                        article_previews.append((p, f"{cid} Fig.{fnum} score={score}"))
                        summary["previews_resolved"] += 1
                    except Exception:
                        pass
                prelim = "high" if score >= 8 else "medium" if score >= 3 else "low"
                scanned.append({
                    "candidate_id": cid, "year": row["year"], "journal": row["journal"],
                    "article_title": row["article_title"], "article_url": url,
                    "figure_number": str(fnum), "figure_id": str(fig.get("id") or f"fig{fnum}"),
                    "caption_score": str(score), "caption": cap, "third_party_risk": risk,
                    "license": lic if allowed else "not-confirmed-by-parser", "license_url": lic_url if allowed else "",
                    "image_resolved": str(resolved).lower(), "preview_path": preview_rel,
                    "preliminary_rank": prelim,
                })
            if article_previews:
                base.make_contact_sheet(article_previews, contact_root / f"{cid}_contact.jpg")
            summary["articles_scanned"] += 1
            summary["figures_scanned"] += article_count
        except Exception as exc:
            summary["article_failures"].append({"candidate_id": cid, "error": str(exc)})

    out_csv = scan_dir / "stage1_5_wave4_all_figures.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=base.FIELDS)
        w.writeheader()
        w.writerows(scanned)
    (scan_dir / "stage1_5_wave4_scan_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["articles_scanned"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
