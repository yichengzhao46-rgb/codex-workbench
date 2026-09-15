#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

import requests
from PIL import Image, ImageDraw

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import scan_stage1_5_wave2_oa_package as aws  # noqa: E402

POSITIVE = {
    "schematic": 6, "mechanism": 6, "model": 3, "pathway": 4, "workflow": 5,
    "electron transfer": 6, "extracellular electron transfer": 8, "direct interspecies electron": 8,
    "cross-feeding": 7, "interaction": 4, "interface": 6, "biohybrid": 7,
    "semiconductor": 6, "biochar": 5, "magnetite": 5, "mineral": 4,
    "spatial": 4, "gradient": 5, "stratification": 6, "conceptual": 5,
    "overview": 4, "nanowire": 5, "flavin": 5, "metabolite": 3, "community": 2,
    "electrode": 4, "redox": 4, "hydrogel": 5, "biofilm": 3,
}
NEGATIVE = {
    "heatmap": -5, "principal component": -5, "pca": -5, "volcano": -5,
    "boxplot": -4, "box plot": -4, "western blot": -4, "microscopy": -3,
    "micrograph": -3, "sem image": -3, "tem image": -3, "phylogen": -4,
}
FIELDS = [
    "candidate_id", "year", "journal", "article_title", "article_url", "figure_number",
    "figure_id", "caption_score", "caption", "third_party_risk", "license",
    "image_resolved", "preview_path", "preliminary_rank", "cloud_version",
]


def score_caption(text: str) -> int:
    low = text.lower()
    return sum(w for t, w in POSITIVE.items() if t in low) + sum(w for t, w in NEGATIVE.items() if t in low)


def make_contact_sheet(items: list[tuple[Path, str]], out: Path) -> None:
    if not items:
        return
    cell_w, cell_h, cols = 520, 390, 2
    rows = (len(items) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(canvas)
    for i, (path, label) in enumerate(items):
        try:
            img = Image.open(path).convert("RGB")
        except Exception:
            continue
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
    ap.add_argument("--candidates", default="projects/scientific-figure-style-corpus/manifests/stage1_5_wave3_candidates.csv")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    scan_dir = root / "validation" / "stage1_5_wave3_scan"
    previews = scan_dir / "previews"
    contacts = scan_dir / "contact_sheets"
    previews.mkdir(parents=True, exist_ok=True)
    contacts.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(Path(args.candidates).open(encoding="utf-8", newline="")))
    session = requests.Session()
    session.headers.update({"User-Agent": "codex-workbench-stage1.5-wave3/0.1", "Accept-Language": "en-US,en;q=0.8"})

    scanned = []
    summary = {
        "articles_total": len(rows), "articles_scanned": 0, "figures_scanned": 0,
        "previews_resolved": 0, "public_mirror_compatible_articles": 0,
        "restrictive_or_unknown_articles": 0, "article_failures": [],
    }

    for row in rows:
        cid = row["candidate_id"]
        m = re.search(r"(PMC\d+)", row["url"], re.I)
        if not m:
            summary["article_failures"].append({"candidate_id": cid, "error": "missing PMCID"})
            continue
        pmcid = m.group(1).upper()
        try:
            version, meta = aws.choose_version(session, pmcid)
            allowed, lic = aws.allowed_license(meta)
            if allowed:
                summary["public_mirror_compatible_articles"] += 1
            else:
                summary["restrictive_or_unknown_articles"] += 1
            xml_url = aws.as_https(str(meta.get("xml_url") or ""))
            if not xml_url:
                raise RuntimeError("AWS metadata has no xml_url")
            xr = session.get(xml_url, timeout=60); xr.raise_for_status()
            article = ET.fromstring(xr.content)
            mmap = aws.media_map(meta)
            article_previews = []
            article_count = 0
            for ordinal, fig in enumerate(article.findall(".//fig"), 1):
                cap = aws.txt(fig.find("caption"))
                if not cap:
                    continue
                article_count += 1
                label = aws.txt(fig.find("label"))
                nm = re.search(r"(\d+)", label)
                fnum = int(nm.group(1)) if nm else ordinal
                third = aws.risk(cap)
                score = score_caption(cap)
                graphic = fig.find("graphic")
                href = graphic.attrib.get(aws.XLINK, "") if graphic is not None else ""
                media_url = aws.find_media(mmap, href)
                resolved = False
                rel = ""
                if allowed and not third and media_url:
                    try:
                        ir = session.get(media_url, timeout=60); ir.raise_for_status()
                        suffix = PurePosixPath(urlparse(media_url).path).suffix.lower() or ".img"
                        out_dir = previews / cid
                        out_dir.mkdir(parents=True, exist_ok=True)
                        p = out_dir / f"{cid}_fig{fnum}{suffix}"
                        p.write_bytes(ir.content)
                        resolved = True
                        rel = str(p.relative_to(root))
                        article_previews.append((p, f"{cid} Fig.{fnum} score={score}"))
                        summary["previews_resolved"] += 1
                    except Exception:
                        pass
                scanned.append({
                    "candidate_id": cid, "year": row["year"], "journal": row["journal"],
                    "article_title": row["article_title"], "article_url": row["url"],
                    "figure_number": str(fnum), "figure_id": fig.attrib.get("id", f"fig{fnum}"),
                    "caption_score": str(score), "caption": cap, "third_party_risk": third,
                    "license": lic or "unknown_or_restrictive", "image_resolved": str(resolved).lower(),
                    "preview_path": rel, "preliminary_rank": "high" if score >= 8 else "medium" if score >= 3 else "low",
                    "cloud_version": version,
                })
            if article_previews:
                make_contact_sheet(article_previews, contacts / f"{cid}_contact.jpg")
            summary["articles_scanned"] += 1
            summary["figures_scanned"] += article_count
        except Exception as exc:
            summary["article_failures"].append({"candidate_id": cid, "pmcid": pmcid, "error": str(exc)})

    out_csv = scan_dir / "stage1_5_wave3_all_figures.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(scanned)
    (scan_dir / "stage1_5_wave3_scan_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["articles_scanned"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
