#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

import requests
from PIL import Image, ImageDraw

OA_API = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmcid}"
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
    "license_url", "image_resolved", "preview_path", "preliminary_rank"
]


def txt(node) -> str:
    if node is None:
        return ""
    return " ".join("".join(node.itertext()).split())


def score_caption(text: str) -> int:
    low = text.lower()
    score = sum(w for t, w in POSITIVE.items() if t in low)
    score += sum(w for t, w in NEGATIVE.items() if t in low)
    return score


def risk(text: str) -> str:
    low = text.lower()
    return "; ".join(t for t in RISK_TERMS if t in low)


def detect_license(root: ET.Element) -> tuple[bool, str, str]:
    candidates = []
    for el in root.findall(".//license"):
        href = el.attrib.get(XLINK, "")
        text = txt(el)
        candidates.append((href, text))
    for href, text in candidates:
        blob = f"{href} {text}".lower()
        if any(x in blob for x in ("by-nc", "by-nd", "by-nc-nd", "noncommercial", "no derivatives", "no-derivatives")):
            continue
        if "creativecommons.org/licenses/by/" in blob or re.search(r"\bcc[- ]?by\b", blob):
            return True, text or "CC BY", href
        if "creativecommons.org/publicdomain/zero/" in blob or "cc0" in blob:
            return True, text or "CC0", href
    return False, "", ""


def safe_member_name(name: str) -> bool:
    p = PurePosixPath(name)
    return not p.is_absolute() and ".." not in p.parts


def find_member(tf: tarfile.TarFile, href: str):
    target = PurePosixPath(href).name
    stems = {target, target + ".jpg", target + ".jpeg", target + ".png", target + ".tif", target + ".tiff", target + ".gif", target + ".webp"}
    for member in tf.getmembers():
        if not member.isfile() or not safe_member_name(member.name):
            continue
        base = PurePosixPath(member.name).name
        if base in stems or PurePosixPath(base).stem == PurePosixPath(target).stem:
            return member
    return None


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
    session.headers.update({"User-Agent": "codex-workbench-stage1.5/0.2", "Accept-Language": "en-US,en;q=0.8"})
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
            oa = session.get(OA_API.format(pmcid=pmcid), timeout=45)
            oa.raise_for_status()
            oa_root = ET.fromstring(oa.content)
            links = oa_root.findall(".//link")
            tgz = next((x.attrib.get("href", "") for x in links if x.attrib.get("format") == "tgz"), "")
            if not tgz:
                raise RuntimeError("PMC OA API returned no tgz package")
            if tgz.startswith("ftp://"):
                tgz = "https://" + tgz[len("ftp://"):]
            pkg = session.get(tgz, timeout=90)
            pkg.raise_for_status()
            tf = tarfile.open(fileobj=io.BytesIO(pkg.content), mode="r:gz")
            xml_members = [x for x in tf.getmembers() if x.isfile() and x.name.lower().endswith((".nxml", ".xml")) and safe_member_name(x.name)]
            if not xml_members:
                raise RuntimeError("OA package contains no JATS XML")
            xml_bytes = tf.extractfile(xml_members[0]).read()
            article = ET.fromstring(xml_bytes)
            allowed, lic, lic_url = detect_license(article)
            figs = article.findall(".//fig")
            article_previews = []
            for ordinal, fig in enumerate(figs, 1):
                cap = txt(fig.find("caption"))
                if not cap:
                    continue
                label = txt(fig.find("label"))
                nm = re.search(r"(\d+)", label)
                fnum = int(nm.group(1)) if nm else ordinal
                third = risk(cap)
                score = score_caption(cap)
                graphic = fig.find("graphic")
                href = graphic.attrib.get(XLINK, "") if graphic is not None else ""
                resolved = False
                preview_rel = ""
                if allowed and not third and href:
                    member = find_member(tf, href)
                    if member:
                        data = tf.extractfile(member).read()
                        suffix = PurePosixPath(member.name).suffix.lower() or ".img"
                        out_dir = preview_root / cid
                        out_dir.mkdir(parents=True, exist_ok=True)
                        p = out_dir / f"{cid}_fig{fnum}{suffix}"
                        p.write_bytes(data)
                        resolved = True
                        preview_rel = str(p.relative_to(root_dir))
                        article_previews.append((p, f"{cid} Fig.{fnum} score={score}"))
                        summary["previews_resolved"] += 1
                scanned.append({
                    "candidate_id": cid, "year": row["year"], "journal": row["journal"],
                    "article_title": row["article_title"], "article_url": row["url"],
                    "figure_number": str(fnum), "figure_id": fig.attrib.get("id", f"fig{fnum}"),
                    "caption_score": str(score), "caption": cap, "third_party_risk": third,
                    "license": lic if allowed else "not-public-mirror-compatible", "license_url": lic_url if allowed else "",
                    "image_resolved": str(resolved).lower(), "preview_path": preview_rel,
                    "preliminary_rank": "high" if score >= 8 else "medium" if score >= 3 else "low",
                })
            if article_previews:
                make_contact_sheet(article_previews, contact_root / f"{cid}_contact.jpg")
            summary["articles_scanned"] += 1
            summary["figures_scanned"] += len([x for x in scanned if x["candidate_id"] == cid])
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
