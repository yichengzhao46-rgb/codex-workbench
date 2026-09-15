#!/usr/bin/env python3
"""Ingest figure candidates from a local Zotero library into the scientific figure corpus.

Design goals
------------
1. Read Zotero's local SQLite database and storage tree without modifying Zotero.
2. Select papers from accepted/high-value journals, with topic-aware scoring.
3. Locate Figure/Fig. captions in attached PDFs and render figure-region crops.
4. Keep publisher-copyright figures private/local by default.
5. Append provenance-rich records to a local Zotero manifest compatible with the
   workbench corpus model. Public redistribution is never assumed.

This script is meant to run locally (for example from Codex/Desktop) because the
Zotero database and attachment files normally live on the user's computer.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import fitz  # PyMuPDF

PROJECT_REL = Path("projects/scientific-figure-style-corpus")

CORE_JOURNALS = {
    "the isme journal",
    "isme journal",
    "nature communications",
    "environmental science & technology",
    "environmental science and technology",
    "water research",
}

SECONDARY_JOURNALS = {
    "nature microbiology",
    "science advances",
    "nature water",
    "energy & environmental science",
    "energy and environmental science",
    "environmental science & technology letters",
    "environmental science and technology letters",
    "environmental science & ecotechnology",
    "environmental science and ecotechnology",
    "microbiome",
    "mbio",
    "mBio",
    "applied and environmental microbiology",
    "biotechnology for biofuels and bioproducts",
    "bioresource technology",
    "journal of hazardous materials",
    "chemical engineering journal",
    "environment international",
    "environmental microbiome",
}

TOPIC_TERMS = {
    "methane": 6,
    "methanotroph": 9,
    "methanotrophic": 9,
    "methylococcus": 10,
    "rhodopseudomonas": 10,
    "palustris": 8,
    "cross-feeding": 9,
    "cross feeding": 9,
    "interspecies": 8,
    "syntroph": 8,
    "electron transfer": 10,
    "extracellular electron": 10,
    "direct interspecies electron": 10,
    "diet": 7,
    "eet": 7,
    "eeu": 7,
    "conductive": 7,
    "biochar": 5,
    "granular activated carbon": 8,
    "gac": 5,
    "electrode": 7,
    "mineral": 6,
    "selen": 7,
    "semiconductor": 8,
    "biohybrid": 9,
    "carbon fixation": 9,
    "inorganic carbon": 7,
    "dark carbon": 10,
    "microoxic": 8,
    "hypoxi": 7,
    "anoxic": 6,
    "oxygen limitation": 8,
    "redox": 6,
    "riboflavin": 8,
    "formate": 6,
    "acetate": 5,
    "hydrogen": 4,
}

CAPTION_TERMS = {
    "schematic": 10,
    "scheme": 8,
    "conceptual": 9,
    "mechanism": 9,
    "model": 5,
    "pathway": 8,
    "metabolic": 7,
    "metabolism": 6,
    "electron transfer": 10,
    "interaction": 7,
    "cross-feeding": 9,
    "interspecies": 8,
    "interface": 8,
    "mineral": 6,
    "electrode": 7,
    "conductive": 7,
    "aggregate": 5,
    "biofilm": 5,
    "gradient": 7,
    "oxic": 5,
    "anoxic": 5,
    "microoxic": 8,
    "methane": 6,
    "carbon fixation": 8,
    "experimental design": 9,
    "workflow": 6,
    "overview": 6,
    "proposed": 5,
    "illustration": 6,
    "diagram": 8,
}

DATA_FIGURE_TERMS = {
    "heatmap": -5,
    "volcano": -8,
    "principal component": -6,
    "pca": -5,
    "boxplot": -5,
    "box plot": -5,
    "rarefaction": -8,
    "phylogenetic tree": -6,
    "scatter plot": -4,
    "regression": -3,
}

FIGURE_RE = re.compile(
    r"^\s*(?:figure|fig\.?)[\s\u00a0]*([0-9]+[A-Za-z]?)(?:\s*[.:\-–—]|\s+)",
    re.IGNORECASE,
)

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)


@dataclass
class ZoteroItem:
    item_id: int
    item_key: str
    title: str
    journal: str
    year: str
    doi: str
    pdf_path: Path
    attachment_key: str


@dataclass
class FigureCandidate:
    item: ZoteroItem
    page_number: int
    figure_label: str
    caption: str
    crop: fitz.Rect
    score: int


def norm(s: str) -> str:
    return " ".join((s or "").split())


def norm_journal(s: str) -> str:
    return norm(s).lower().replace("the ", "", 1).strip()


def accepted_journal(journal: str, allow_other: bool) -> tuple[bool, str]:
    j = norm(journal).lower()
    j_no_the = norm_journal(journal)
    core_norm = {norm_journal(x) for x in CORE_JOURNALS}
    secondary_norm = {norm_journal(x) for x in SECONDARY_JOURNALS}
    if j_no_the in core_norm:
        return True, "core"
    if j_no_the in secondary_norm:
        return True, "secondary"
    return (allow_other, "other" if allow_other else "rejected")


def score_text(text: str, weights: dict[str, int]) -> int:
    t = text.lower()
    return sum(weight for term, weight in weights.items() if term in t)


def discover_zotero_root(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(p)
        return p

    candidates: list[Path] = []
    home = Path.home()
    if sys.platform.startswith("win"):
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidates.append(Path(appdata) / "Zotero" / "Zotero" / "Profiles")
        candidates += [home / "Zotero", home / "Documents" / "Zotero"]
    elif sys.platform == "darwin":
        candidates += [
            home / "Zotero",
            home / "Library" / "Application Support" / "Zotero",
        ]
    else:
        candidates += [home / "Zotero", home / ".zotero" / "zotero"]

    # Most current Zotero installs put zotero.sqlite directly in the data directory.
    for c in candidates:
        if (c / "zotero.sqlite").exists():
            return c.resolve()

    # Search a shallow set of likely roots rather than crawling the entire disk.
    for root in candidates:
        if not root.exists():
            continue
        hits = list(root.glob("**/zotero.sqlite"))[:5]
        if hits:
            return hits[0].parent.resolve()

    raise FileNotFoundError(
        "Could not locate Zotero data directory automatically. Pass --zotero-root."
    )


def open_zotero_db_readonly(db_path: Path) -> sqlite3.Connection:
    # Copy first so Zotero can remain open and SQLite WAL locking does not interfere.
    td = tempfile.mkdtemp(prefix="zotero-corpus-")
    copy_path = Path(td) / "zotero.sqlite"
    shutil.copy2(db_path, copy_path)
    for suffix in ("-wal", "-shm"):
        src = Path(str(db_path) + suffix)
        if src.exists():
            shutil.copy2(src, Path(str(copy_path) + suffix))
    conn = sqlite3.connect(str(copy_path))
    conn.row_factory = sqlite3.Row
    return conn


def field_id(conn: sqlite3.Connection, name: str) -> int | None:
    row = conn.execute("SELECT fieldID FROM fields WHERE fieldName=?", (name,)).fetchone()
    return int(row[0]) if row else None


def get_field_map(conn: sqlite3.Connection, item_ids: list[int]) -> dict[int, dict[str, str]]:
    if not item_ids:
        return {}
    placeholders = ",".join("?" for _ in item_ids)
    sql = f"""
        SELECT idv.itemID, f.fieldName, v.value
        FROM itemData idv
        JOIN fields f ON f.fieldID=idv.fieldID
        JOIN itemDataValues v ON v.valueID=idv.valueID
        WHERE idv.itemID IN ({placeholders})
    """
    out: dict[int, dict[str, str]] = {i: {} for i in item_ids}
    for row in conn.execute(sql, item_ids):
        out[int(row["itemID"])][str(row["fieldName"])] = str(row["value"] or "")
    return out


def parse_year(s: str) -> str:
    m = re.search(r"(?:19|20)\d{2}", s or "")
    return m.group(0) if m else ""


def enumerate_pdf_items(conn: sqlite3.Connection, zotero_root: Path) -> list[ZoteroItem]:
    # Attachment rows link to bibliographic parent items. We avoid deleted items.
    rows = conn.execute(
        """
        SELECT ia.itemID AS attachmentItemID,
               ia.parentItemID AS parentItemID,
               ia.path AS attachmentPath,
               att.key AS attachmentKey,
               parent.key AS parentKey
        FROM itemAttachments ia
        JOIN items att ON att.itemID=ia.itemID
        JOIN items parent ON parent.itemID=ia.parentItemID
        LEFT JOIN deletedItems d1 ON d1.itemID=ia.itemID
        LEFT JOIN deletedItems d2 ON d2.itemID=ia.parentItemID
        WHERE ia.parentItemID IS NOT NULL
          AND d1.itemID IS NULL
          AND d2.itemID IS NULL
        """
    ).fetchall()

    parent_ids = sorted({int(r["parentItemID"]) for r in rows})
    fields = get_field_map(conn, parent_ids)
    items: list[ZoteroItem] = []

    for r in rows:
        attachment_path = str(r["attachmentPath"] or "")
        if not attachment_path.lower().endswith(".pdf"):
            continue

        if attachment_path.startswith("storage:"):
            rel = attachment_path.split(":", 1)[1]
            pdf = zotero_root / "storage" / str(r["attachmentKey"]) / rel
        else:
            pdf = Path(attachment_path.replace("attachments:", "")).expanduser()

        if not pdf.exists() or not pdf.is_file():
            continue

        pid = int(r["parentItemID"])
        fm = fields.get(pid, {})
        title = fm.get("title", "")
        journal = (
            fm.get("publicationTitle", "")
            or fm.get("journalAbbreviation", "")
            or fm.get("proceedingsTitle", "")
        )
        doi = fm.get("DOI", "")
        date = fm.get("date", "")
        if not doi:
            extra = fm.get("extra", "")
            m = DOI_RE.search(extra)
            doi = m.group(0) if m else ""

        items.append(
            ZoteroItem(
                item_id=pid,
                item_key=str(r["parentKey"]),
                title=title,
                journal=journal,
                year=parse_year(date),
                doi=doi,
                pdf_path=pdf,
                attachment_key=str(r["attachmentKey"]),
            )
        )
    return items


def text_blocks(page: fitz.Page):
    return sorted(page.get_text("blocks"), key=lambda b: (round(b[1], 1), b[0]))


def caption_blocks(page: fitz.Page) -> list[tuple[fitz.Rect, str, str]]:
    out = []
    for b in text_blocks(page):
        rect = fitz.Rect(b[:4])
        text = norm(str(b[4]))
        m = FIGURE_RE.match(text)
        if m:
            out.append((rect, text, m.group(1)))
    return out


def choose_crop(page: fitz.Page, caption_rect: fitz.Rect, all_caps: list[tuple[fitz.Rect, str, str]]) -> fitz.Rect:
    page_rect = page.rect
    # Most journal figures sit above their captions. Use previous caption as a hard
    # upper boundary and then search local layout blocks for a whitespace break.
    previous_bottom = page_rect.y0 + 18
    for r, _, _ in all_caps:
        if r.y1 < caption_rect.y0 and r.y1 > previous_bottom:
            previous_bottom = r.y1 + 8

    top = previous_bottom
    bottom = max(top + 72, caption_rect.y0 - 4)

    # If that is too tall, prefer the final ~58% of available vertical space above
    # the caption; this reduces surrounding article prose while preserving multi-panel figures.
    available = bottom - top
    max_h = page_rect.height * 0.58
    if available > max_h:
        top = bottom - max_h

    # Use nearly full text width; journal PDFs frequently place labels at the edges.
    margin_x = page_rect.width * 0.035
    crop = fitz.Rect(page_rect.x0 + margin_x, top, page_rect.x1 - margin_x, bottom)
    return crop & page_rect


def figure_candidates(item: ZoteroItem, min_caption_score: int) -> list[FigureCandidate]:
    doc = fitz.open(item.pdf_path)
    candidates: list[FigureCandidate] = []
    try:
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            caps = caption_blocks(page)
            for rect, caption, label in caps:
                score = score_text(caption, CAPTION_TERMS) + score_text(caption, DATA_FIGURE_TERMS)
                score += score_text(item.title, TOPIC_TERMS) // 2
                if score < min_caption_score:
                    continue
                candidates.append(
                    FigureCandidate(
                        item=item,
                        page_number=page_idx + 1,
                        figure_label=label,
                        caption=caption,
                        crop=choose_crop(page, rect, caps),
                        score=score,
                    )
                )
    finally:
        doc.close()
    return sorted(candidates, key=lambda x: x.score, reverse=True)


def render_candidate(candidate: FigureCandidate, out_path: Path, dpi: int) -> tuple[str, int, int]:
    doc = fitz.open(candidate.item.pdf_path)
    try:
        page = doc[candidate.page_number - 1]
        pix = page.get_pixmap(clip=candidate.crop, dpi=dpi, alpha=False)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        pix.save(out_path)
        data = out_path.read_bytes()
        return hashlib.sha256(data).hexdigest(), pix.width, pix.height
    finally:
        doc.close()


def infer_purpose(caption: str) -> str:
    t = caption.lower()
    checks = [
        ("electron_transfer", ("electron transfer", "electron transport", "eet", "eeu", "diet")),
        ("material_microbe_interface", ("mineral", "electrode", "biochar", "conductive", "semiconductor")),
        ("microbial_interaction", ("interaction", "cross-feeding", "interspecies", "syntroph")),
        ("metabolic_pathway", ("metabolic", "metabolism", "pathway")),
        ("comparative_perturbation", ("comparison", "versus", "vs.", "oxygen", "oxic", "anoxic")),
        ("experimental_design", ("experimental design", "workflow", "setup", "reactor configuration")),
        ("environmental_process", ("gradient", "environment", "biogeochemical", "sediment", "wetland")),
        ("integrated_mechanism", ("mechanism", "proposed model", "conceptual model")),
        ("conceptual_overview", ("schematic", "scheme", "overview", "conceptual")),
    ]
    for purpose, terms in checks:
        if any(term in t for term in terms):
            return purpose
    return "conceptual_overview"


def write_manifest(rows: list[dict[str, str]], manifest: Path) -> None:
    fields = [
        "sample_id",
        "source_type",
        "zotero_item_key",
        "attachment_key",
        "journal",
        "journal_tier",
        "article_title",
        "year",
        "doi",
        "figure_id",
        "pdf_page",
        "caption",
        "relevance_score",
        "target_primary_purpose",
        "asset_visibility",
        "asset_path",
        "pixel_width",
        "pixel_height",
        "sha256",
        "license_status",
        "redistribution_allowed",
        "counted_toward_private_100",
        "visual_inspection_status",
        "notes",
    ]
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def build(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    project_root = repo_root / PROJECT_REL
    zotero_root = discover_zotero_root(args.zotero_root)
    db_path = zotero_root / "zotero.sqlite"
    if not db_path.exists():
        raise FileNotFoundError(db_path)

    private_root = Path(args.private_assets).expanduser().resolve()
    manifest = Path(args.manifest).expanduser().resolve() if args.manifest else (
        project_root / "manifests" / "zotero-private-manifest.csv"
    )

    conn = open_zotero_db_readonly(db_path)
    try:
        items = enumerate_pdf_items(conn, zotero_root)
    finally:
        conn.close()

    selected_items: list[tuple[ZoteroItem, str, int]] = []
    for item in items:
        ok, tier = accepted_journal(item.journal, args.allow_other_journals)
        if not ok:
            continue
        article_score = score_text(f"{item.title} {item.journal}", TOPIC_TERMS)
        # Core/secondary journals are eligible even if title is not topic-rich; other
        # journals must be strongly relevant to the project.
        if tier == "other" and article_score < args.min_article_score:
            continue
        selected_items.append((item, tier, article_score))

    selected_items.sort(key=lambda x: (x[2], x[1] == "core"), reverse=True)

    rows: list[dict[str, str]] = []
    total = 0
    distinct_articles = 0
    for item, tier, article_score in selected_items:
        if total >= args.max_figures:
            break
        cands = figure_candidates(item, args.min_caption_score)
        if not cands:
            continue
        used = 0
        for cand in cands:
            if used >= args.max_per_article or total >= args.max_figures:
                break
            sample_id = f"ZOT-{item.item_key}-FIG{cand.figure_label}-P{cand.page_number}"
            out_path = private_root / safe_component(item.journal or "unknown-journal") / f"{sample_id}.png"
            if out_path.exists() and not args.overwrite:
                data = out_path.read_bytes()
                sha = hashlib.sha256(data).hexdigest()
                with fitz.open(out_path) as imgdoc:
                    page = imgdoc[0]
                    width = int(page.rect.width)
                    height = int(page.rect.height)
            else:
                sha, width, height = render_candidate(cand, out_path, args.dpi)

            rows.append(
                {
                    "sample_id": sample_id,
                    "source_type": "zotero_pdf",
                    "zotero_item_key": item.item_key,
                    "attachment_key": item.attachment_key,
                    "journal": item.journal,
                    "journal_tier": tier,
                    "article_title": item.title,
                    "year": item.year,
                    "doi": item.doi,
                    "figure_id": f"Figure {cand.figure_label}",
                    "pdf_page": str(cand.page_number),
                    "caption": cand.caption,
                    "relevance_score": str(article_score + cand.score),
                    "target_primary_purpose": infer_purpose(cand.caption),
                    "asset_visibility": "private_local",
                    "asset_path": str(out_path),
                    "pixel_width": str(width),
                    "pixel_height": str(height),
                    "sha256": sha,
                    "license_status": "not_verified_private_reference_only",
                    "redistribution_allowed": "false",
                    "counted_toward_private_100": "true",
                    "visual_inspection_status": "pending_manual_qa",
                    "notes": "Rendered from legally available local Zotero PDF; do not publish asset without separate license verification.",
                }
            )
            used += 1
            total += 1
        if used:
            distinct_articles += 1

    write_manifest(rows, manifest)
    print(f"Zotero root: {zotero_root}")
    print(f"Eligible PDF attachments: {len(selected_items)}")
    print(f"Figures ingested: {len(rows)}")
    print(f"Distinct source articles: {distinct_articles}")
    print(f"Private assets: {private_root}")
    print(f"Manifest: {manifest}")
    if len(rows) < args.min_required:
        print(
            f"WARNING: only {len(rows)} figures were ingested; minimum requested was {args.min_required}.",
            file=sys.stderr,
        )
        return 2
    return 0


def safe_component(s: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", norm(s)).strip("-")
    return cleaned[:100] or "unknown"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ingest high-value figures from a local Zotero PDF library")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--zotero-root", default=None, help="Zotero data directory containing zotero.sqlite and storage/")
    p.add_argument(
        "--private-assets",
        default=str(Path.home() / "scientific-figure-corpus-private" / "zotero"),
        help="Private local asset directory; keep outside public Git by default",
    )
    p.add_argument("--manifest", default=None)
    p.add_argument("--max-figures", type=int, default=100)
    p.add_argument("--max-per-article", type=int, default=3)
    p.add_argument("--min-required", type=int, default=1)
    p.add_argument("--min-article-score", type=int, default=6)
    p.add_argument("--min-caption-score", type=int, default=3)
    p.add_argument("--dpi", type=int, default=220)
    p.add_argument("--allow-other-journals", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    sys.exit(build(parse_args()))
