#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

import requests
from PIL import Image, ImageDraw

S3_BASE = "https://pmc-oa-opendata.s3.amazonaws.com"
XLINK = "{http://www.w3.org/1999/xlink}href"

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
    "micrograph": -3, "sem": -2, "tem": -2, "phylogen": -4,
}
RISK_TERMS = (
    "biorender", "created with biorender", "created in biorender",
    "reproduced from", "adapted from", "modified from", "reprinted from",
    "with permission", "permission from", "copyright ", "© ", "credit:", "courtesy of",
)
FIELDS = [
    "candidate_id", "year", "journal", "article_title", "article_url", "figure_number",
    "figure_id", "caption_score", "caption", "third_party_risk", "license",
    "license_url", "image_resolved", "preview_path", "preliminary_rank", "cloud_version"
]


def txt(node) -> str:
    if node is None:
        return ""
    return " ".join("".join(node.itertext()).split())


def score_caption(text: str) -> int:
    low = text.lower()
    return sum(w for t, w in POSITIVE.items() if t in low) + sum(w for t, w in NEGATIVE.items() if t in low)


def risk(text: str) -> str:
    low = text.lower()
    return "; ".join(t for t in RISK_TERMS if t in low)


def as_https(url: str) -> str:
    if not url:
        return ""
    if url.startswith("s3://pmc-oa-opendata/"):
        return f"{S3_BASE}/" + url[len("s3://pmc-oa-opendata/"):]
    return url


def list_versions(session: requests.Session, pmcid: str) -> list[str]:
    r = session.get(S3_BASE + "/", params={"list-type": "2", "prefix": pmcid + ".", "delimiter": "/"}, timeout=45)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    versions = []
    for el in root.iter():
        if el.tag.endswith("Prefix") and el.text and el.text.startswith(pmcid + "."):
            versions.append(el.text.rstrip("/"))
    return sorted(set(versions), key=lambda x: int(x.rsplit(".", 1)[-1]), reverse=True)


def load_metadata(session: requests.Session, version: str) -> dict:
    url = f"{S3_BASE}/{version}/{version}.json"
    r = session.get(url, timeout=45)
    r.raise_for_status()
    return r.json()


def choose_version(session: requests.Session, pmcid: str) -> tuple[str, dict]:
    versions = list_versions(session, pmcid)
    if not versions:
        raise RuntimeError("PMCID not found in PMC AWS Cloud dataset")
    candidates = []
    for v in versions:
        try:
            meta = load_metadata(session, v)
            candidates.append((v, meta))
        except Exception:
            continue
    if not candidates:
        raise RuntimeError("no readable AWS metadata object")
    # Prefer final published version over author manuscript, then newest version number.
    candidates.sort(key=lambda vm: (str(vm[1].get("is_manuscript", "")).lower() in {"yes", "true", "1"}, -int(vm[0].rsplit(".", 1)[-1])))
    return candidates[0]


def allowed_license(meta: dict) -> tuple[bool, str]:
    code = str(meta.get("license_code") or "").strip().lower().replace("_", "-")
    norm = re.sub(r"\s+", "-", code)
    if norm in {"cc-by", "ccby", "by", "cc-0", "cc0"} or norm.startswith("cc-by-") and all(x not in norm for x in ("-nc", "-nd", "-sa")):
        return True, str(meta.get("license_code") or "CC BY")
    return False, str(meta.get("license_code") or "")


def media_map(meta: dict) -> dict[str, str]:
    result = {}
    for item in meta.get("media_urls") or []:
        if isinstance(item, dict):
            url = as_https(str(item.get("url") or item.get("href") or ""))
        else:
            url = as_https(str(item))
        if not url:
            continue
        path = urlparse(url).path
        base = PurePosixPath(path).name
        result[base] = url
        result[PurePosixPath(base).stem] = url
    return result


def find_media(meta_map: dict[str, str], href: str) -> str:
    if not href:
        return ""
    base = PurePosixPath(href).name
    return meta_map.get(base) or meta_map.get(PurePosixPath(base).stem) or ""


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
    ap.add_argument("--candidates", default="projects/scientific-figure-style-corpus/manifests/stage1_5_wave2_candidates.csv")
    args = ap.parse_args()
    root_dir = Path(args.project_root).resolve()
    scan_dir = root_dir / "validation" / "stage1_5_wave2_package_scan"
    preview_root = scan_dir / "previews"
    contact_root = scan_dir / "contact_sheets"
    preview_root.mkdir(parents=True, exist_ok=True)
    contact_root.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(Path(args.candidates).open(encoding="utf-8", newline="")))
    session = requests.Session()
    session.headers.update({"User-Agent": "codex-workbench-stage1.5/0.3", "Accept-Language": "en-US,en;q=0.8"})
    scanned = []
    summary = {"articles_total": len(rows), "articles_scanned": 0, "figures_scanned": 0, "previews_resolved": 0, "metadata_only": 0, "article_failures": []}

    for row in rows:
        cid = row["candidate_id"]
        m = re.search(r"(PMC\d+)", row["url"], re.I)
        if not m:
            summary["metadata_only"] += 1
            continue
        pmcid = m.group(1).upper()
        try:
            version, meta = choose_version(session, pmcid)
            allowed, lic = allowed_license(meta)
            xml_url = as_https(str(meta.get("xml_url") or ""))
            if not xml_url:
                raise RuntimeError("AWS metadata has no xml_url")
            xr = session.get(xml_url, timeout=60)
            xr.raise_for_status()
            article = ET.fromstring(xr.content)
            mmap = media_map(meta)
            figs = article.findall(".//fig")
            article_previews = []
            article_count = 0
            for ordinal, fig in enumerate(figs, 1):
                cap = txt(fig.find("caption"))
                if not cap:
                    continue
                article_count += 1
                label = txt(fig.find("label"))
                nm = re.search(r"(\d+)", label)
                fnum = int(nm.group(1)) if nm else ordinal
                third = risk(cap)
                score = score_caption(cap)
                graphic = fig.find("graphic")
                href = graphic.attrib.get(XLINK, "") if graphic is not None else ""
                media_url = find_media(mmap, href)
                resolved = False
                preview_rel = ""
                if allowed and not third and media_url:
                    ir = session.get(media_url, timeout=60)
                    ir.raise_for_status()
                    suffix = PurePosixPath(urlparse(media_url).path).suffix.lower() or ".img"
                    out_dir = preview_root / cid
                    out_dir.mkdir(parents=True, exist_ok=True)
                    p = out_dir / f"{cid}_fig{fnum}{suffix}"
                    p.write_bytes(ir.content)
                    resolved = True
                    preview_rel = str(p.relative_to(root_dir))
                    article_previews.append((p, f"{cid} Fig.{fnum} score={score}"))
                    summary["previews_resolved"] += 1
                scanned.append({
                    "candidate_id": cid, "year": row["year"], "journal": row["journal"],
                    "article_title": row["article_title"], "article_url": row["url"],
                    "figure_number": str(fnum), "figure_id": fig.attrib.get("id", f"fig{fnum}"),
                    "caption_score": str(score), "caption": cap, "third_party_risk": third,
                    "license": lic if allowed else (lic or "not-public-mirror-compatible"), "license_url": "",
                    "image_resolved": str(resolved).lower(), "preview_path": preview_rel,
                    "preliminary_rank": "high" if score >= 8 else "medium" if score >= 3 else "low",
                    "cloud_version": version,
                })
            if article_previews:
                make_contact_sheet(article_previews, contact_root / f"{cid}_contact.jpg")
            summary["articles_scanned"] += 1
            summary["figures_scanned"] += article_count
        except Exception as exc:
            summary["article_failures"].append({"candidate_id": cid, "pmcid": pmcid, "error": str(exc)})

    csv_out = scan_dir / "stage1_5_wave2_all_figures.csv"
    with csv_out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(scanned)
    (scan_dir / "stage1_5_wave2_scan_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["articles_scanned"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
