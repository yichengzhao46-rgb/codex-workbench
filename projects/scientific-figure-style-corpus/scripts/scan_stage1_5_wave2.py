#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, ImageDraw

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import build_raw_corpus as b  # noqa: E402
import harvest_stage1_5 as h  # noqa: E402

POSITIVE = {
    "schematic": 6, "mechanism": 6, "model": 3, "pathway": 4, "workflow": 5,
    "electron transfer": 6, "extracellular electron transfer": 8, "cross-feeding": 8,
    "interaction": 4, "interface": 5, "biohybrid": 6, "spatial": 4,
    "gradient": 4, "conceptual": 5, "illustration": 4, "overview": 4,
    "nanowire": 5, "flavin": 5, "metabolite": 3, "community": 2,
}
NEGATIVE = {
    "heatmap": -5, "principal component": -5, "pca": -5, "volcano": -5,
    "boxplot": -4, "box plot": -4, "western blot": -4, "microscopy": -3,
    "micrograph": -3, "sem image": -3, "tem image": -3, "phylogen": -4,
}

FIELDS = [
    "candidate_id", "year", "journal", "article_title", "article_url", "figure_number",
    "figure_id", "caption_score", "caption", "third_party_risk", "license",
    "license_url", "image_resolved", "preview_path", "preliminary_rank"
]


def score_caption(text: str) -> int:
    low = text.lower()
    score = 0
    for term, weight in POSITIVE.items():
        if term in low:
            score += weight
    for term, weight in NEGATIVE.items():
        if term in low:
            score += weight
    return score


def figure_number(fig, ordinal: int) -> int:
    cap = h.caption_text(fig)
    m = re.search(r"^\s*Fig(?:ure)?\.?\s*(\d+)", cap, re.I)
    if m:
        return int(m.group(1))
    fid = str(fig.get("id") or "")
    m = re.search(r"(\d+)", fid)
    return int(m.group(1)) if m else ordinal


def make_contact_sheet(items: list[tuple[Path, str]], out: Path) -> None:
    if not items:
        return
    cell_w, cell_h = 520, 390
    cols = 2
    rows = (len(items) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(canvas)
    for i, (path, label) in enumerate(items):
        img = Image.open(path).convert("RGB")
        img.thumbnail((cell_w - 20, cell_h - 55))
        x = (i % cols) * cell_w + (cell_w - img.width) // 2
        y = (i // cols) * cell_h + 32
        canvas.paste(img, (x, y))
        draw.text(((i % cols) * cell_w + 10, (i // cols) * cell_h + 8), label, fill="black")
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=90)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default="projects/scientific-figure-style-corpus")
    ap.add_argument("--candidates", default="projects/scientific-figure-style-corpus/manifests/stage1_5_wave2_candidates.csv")
    ap.add_argument("--max-image-bytes", type=int, default=15_000_000)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    candidates = Path(args.candidates).resolve()
    scan_dir = root / "validation" / "stage1_5_wave2_scan"
    preview_root = scan_dir / "previews"
    contact_root = scan_dir / "contact_sheets"
    scan_dir.mkdir(parents=True, exist_ok=True)
    preview_root.mkdir(parents=True, exist_ok=True)
    contact_root.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(candidates.open(encoding="utf-8", newline="")))
    session = requests.Session()
    session.headers.update({"User-Agent": b.USER_AGENT, "Accept-Language": "en-US,en;q=0.8"})

    scanned = []
    summary = {"articles_total": len(rows), "articles_scanned": 0, "figures_scanned": 0, "previews_resolved": 0, "metadata_only": 0, "article_failures": []}

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
            figures = list(soup.find_all("figure"))
            article_previews = []
            for ordinal, fig in enumerate(figures, 1):
                cap = h.caption_text(fig)
                if not cap:
                    continue
                fnum = figure_number(fig, ordinal)
                risk = h.third_party_reason(cap)
                score = score_caption(cap)
                preview_rel = ""
                resolved = False
                # Resolve every main-text figure only when article-level rights are compatible and caption has no third-party warning.
                if allowed and not risk:
                    pmcid_m = re.search(r"/articles/(PMC\d+)/", url, re.I)
                    pmcid = pmcid_m.group(1).upper() if pmcid_m else ""
                    candidates_urls = h.preferred_image_candidates(fig, url, pmcid)
                    try:
                        data, resolved_url, ctype = b.resolve_image_bytes(session, candidates_urls, pmcid, args.max_image_bytes)
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
                make_contact_sheet(article_previews, contact_root / f"{cid}_contact.jpg")
            summary["articles_scanned"] += 1
            summary["figures_scanned"] += sum(1 for r in scanned if r["candidate_id"] == cid)
        except Exception as exc:
            summary["article_failures"].append({"candidate_id": cid, "error": str(exc)})

    out_csv = scan_dir / "stage1_5_wave2_all_figures.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(scanned)
    (scan_dir / "stage1_5_wave2_scan_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["articles_scanned"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
