#!/usr/bin/env python3
"""Build a rights-aware raw scientific-figure corpus from PMC.

This script is intentionally conservative. A figure counts only if:
- the article is discoverable in PMC;
- the article exposes an allowed redistribution license (CC BY or CC0);
- the figure caption does not contain obvious third-party reuse language;
- the actual image bytes are downloaded successfully;
- provenance and sha256 are recorded.

The script prefers figure captions relevant to mechanistic scientific illustration,
but will fall back to other original article figures when needed to fill the raw corpus.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

NCBI_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PMC_ARTICLE = "https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"

USER_AGENT = (
    "codex-workbench-scientific-figure-corpus/0.2 "
    "(noncommercial research corpus builder; contact via repository owner)"
)

TARGETS = {
    "isme": {
        "journal_label": "The ISME Journal",
        "journal_query": '"ISME J"[jour]',
        "quota": 30,
    },
    "nature-communications": {
        "journal_label": "Nature Communications",
        "journal_query": '"Nat Commun"[jour]',
        "quota": 30,
    },
    "est": {
        "journal_label": "Environmental Science & Technology",
        "journal_query": '"Environ Sci Technol"[jour]',
        "quota": 20,
    },
    "water-research": {
        "journal_label": "Water Research",
        "journal_query": '"Water Res"[jour]',
        "quota": 20,
    },
}

POSITIVE_TERMS = {
    # mechanism / process
    "schematic": 9,
    "scheme": 7,
    "conceptual": 8,
    "model": 5,
    "mechanism": 8,
    "pathway": 7,
    "metabolic": 6,
    "metabolism": 6,
    "electron transfer": 10,
    "electron transport": 8,
    "extracellular electron": 10,
    "interspecies": 8,
    "syntroph": 8,
    "cross-feeding": 9,
    "interaction": 6,
    "interface": 7,
    "biofilm": 5,
    "aggregate": 5,
    "mineral": 6,
    "conductive": 7,
    "electrode": 7,
    "redox": 6,
    "oxygen": 4,
    "oxic": 5,
    "anoxic": 5,
    "microoxic": 7,
    "methane": 6,
    "methanotroph": 8,
    "carbon fixation": 8,
    "carbon cycle": 6,
    "biogeochemical": 5,
    "environmental gradient": 7,
    "experimental design": 8,
    "workflow": 6,
    "overview": 5,
    "proposed": 5,
    "illustration": 6,
    "diagram": 7,
}

NEGATIVE_TERMS = {
    # data-heavy figures are still allowed as fallback but scored lower
    "boxplot": -5,
    "box plot": -5,
    "volcano plot": -7,
    "heatmap": -4,
    "principal component": -5,
    "pca": -4,
    "rarefaction": -6,
    "phylogenetic tree": -4,
    "bar chart": -4,
    "bar graph": -4,
    "scatter": -3,
    "regression": -3,
}

THIRD_PARTY_RISK_TERMS = (
    "reproduced from",
    "adapted from",
    "modified from",
    "reprinted from",
    "with permission",
    "permission from",
    "copyright ",
    "© ",
    "credit:",
    "courtesy of",
)

ALLOWED_LICENSE_PATTERNS = (
    re.compile(r"creativecommons\.org/licenses/by/(?:[0-9.]+/)?", re.I),
    re.compile(r"creative commons attribution(?: [0-9.]+)?", re.I),
    re.compile(r"\bcc[- ]?by\b", re.I),
    re.compile(r"creativecommons\.org/publicdomain/zero/", re.I),
    re.compile(r"\bcc0\b", re.I),
)

DISALLOWED_LICENSE_MARKERS = (
    "by-nc",
    "by-nd",
    "by-nc-nd",
    "noncommercial",
    "no derivatives",
    "no-derivatives",
)

IMAGE_EXT_BY_CT = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/tiff": ".tif",
    "image/webp": ".webp",
}


@dataclass
class FigureCandidate:
    journal_slug: str
    journal_label: str
    pmcid: str
    doi: str
    article_title: str
    publication_year: str
    article_url: str
    figure_id: str
    caption: str
    image_url: str
    license_name: str
    license_url: str
    score: int
    third_party_risk: str


def http_get(session: requests.Session, url: str, **kwargs) -> requests.Response:
    last_exc = None
    for attempt in range(4):
        try:
            r = session.get(url, timeout=45, **kwargs)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(1.5 * (attempt + 1))
                continue
            r.raise_for_status()
            return r
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after retries: {url}: {last_exc}")


def esearch(session: requests.Session, journal_query: str, retmax: int = 250) -> list[str]:
    params = {
        "db": "pmc",
        "term": journal_query,
        "retmax": str(retmax),
        "retmode": "json",
        "sort": "pub date",
    }
    r = http_get(session, NCBI_ESEARCH, params=params)
    data = r.json()
    ids = data.get("esearchresult", {}).get("idlist", [])
    return [f"PMC{x}" if not str(x).upper().startswith("PMC") else str(x) for x in ids]


def text_or_empty(node) -> str:
    if not node:
        return ""
    return " ".join(node.get_text(" ", strip=True).split())


def find_meta(soup: BeautifulSoup, name: str) -> str:
    tag = soup.find("meta", attrs={"name": name})
    if tag and tag.get("content"):
        return str(tag["content"]).strip()
    return ""


def detect_license(soup: BeautifulSoup) -> tuple[bool, str, str]:
    page_text = " ".join(soup.stripped_strings)
    lower = page_text.lower()
    for marker in DISALLOWED_LICENSE_MARKERS:
        if marker in lower:
            # A page can mention multiple licenses in references. We therefore still inspect
            # explicit CC links before rejecting globally.
            pass

    cc_links = []
    for a in soup.find_all("a", href=True):
        href = str(a["href"])
        text = text_or_empty(a)
        if "creativecommons.org/" in href.lower():
            cc_links.append((href, text))

    # Prefer explicit CC BY / CC0 links and reject NC/ND variants.
    for href, text in cc_links:
        h = href.lower()
        if any(x in h for x in ("by-nc", "by-nd", "by-nc-nd")):
            continue
        if "/licenses/by/" in h:
            return True, text or "CC BY", href
        if "/publicdomain/zero/" in h:
            return True, text or "CC0", href

    # Fallback to page wording only when it explicitly names Attribution and does not
    # pair that wording with noncommercial/no-derivatives markers nearby.
    for pat in ALLOWED_LICENSE_PATTERNS:
        m = pat.search(page_text)
        if m:
            window = page_text[max(0, m.start() - 120): m.end() + 180].lower()
            if any(x in window for x in DISALLOWED_LICENSE_MARKERS):
                continue
            return True, m.group(0), ""
    return False, "", ""


def figure_score(caption: str) -> int:
    t = caption.lower()
    score = 0
    for term, weight in POSITIVE_TERMS.items():
        if term in t:
            score += weight
    for term, weight in NEGATIVE_TERMS.items():
        if term in t:
            score += weight
    if len(caption) > 120:
        score += 1
    if len(caption) > 350:
        score += 1
    return score


def has_third_party_risk(caption: str) -> str:
    lower = caption.lower()
    hits = [term for term in THIRD_PARTY_RISK_TERMS if term in lower]
    return "; ".join(hits)


def pick_image_url(fig, article_url: str) -> str:
    # PMC often wraps a thumbnail in a link to a larger media file. Prefer that link.
    anchors = fig.find_all("a", href=True)
    for a in anchors:
        href = str(a["href"])
        if re.search(r"\.(?:png|jpe?g|gif|tiff?|webp)(?:\?|$)", href, re.I):
            return urljoin(article_url, href)

    img = fig.find("img")
    if not img:
        return ""
    for attr in ("data-src", "src"):
        value = img.get(attr)
        if value:
            return urljoin(article_url, str(value))
    return ""


def extract_figures(
    soup: BeautifulSoup,
    journal_slug: str,
    journal_label: str,
    pmcid: str,
    article_url: str,
    license_name: str,
    license_url: str,
) -> list[FigureCandidate]:
    title = find_meta(soup, "citation_title") or text_or_empty(soup.find("h1"))
    doi = find_meta(soup, "citation_doi")
    pub_date = find_meta(soup, "citation_publication_date") or find_meta(soup, "citation_date")
    year_match = re.search(r"(19|20)\d{2}", pub_date)
    year = year_match.group(0) if year_match else ""

    figures = []
    # Current PMC pages use semantic <figure>; legacy pages may use div.fig.
    nodes = list(soup.find_all("figure"))
    if not nodes:
        nodes = list(soup.find_all("div", class_=re.compile(r"\bfig\b", re.I)))

    for idx, fig in enumerate(nodes, 1):
        cap_node = fig.find("figcaption") or fig.find(class_=re.compile("caption", re.I))
        caption = text_or_empty(cap_node)
        if not caption:
            continue
        image_url = pick_image_url(fig, article_url)
        if not image_url:
            continue
        fig_id = str(fig.get("id") or f"fig{idx}")
        risk = has_third_party_risk(caption)
        figures.append(
            FigureCandidate(
                journal_slug=journal_slug,
                journal_label=journal_label,
                pmcid=pmcid,
                doi=doi,
                article_title=title,
                publication_year=year,
                article_url=article_url,
                figure_id=fig_id,
                caption=caption,
                image_url=image_url,
                license_name=license_name,
                license_url=license_url,
                score=figure_score(caption),
                third_party_risk=risk,
            )
        )
    return figures


def safe_slug(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s[:120] or "figure"


def ext_from_response(url: str, content_type: str) -> str:
    ctype = content_type.split(";", 1)[0].strip().lower()
    if ctype in IMAGE_EXT_BY_CT:
        return IMAGE_EXT_BY_CT[ctype]
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    return ".img"


def download_figure(
    session: requests.Session,
    fig: FigureCandidate,
    assets_root: Path,
    ordinal: int,
    max_bytes: int,
) -> tuple[Path, str, int, str]:
    r = http_get(session, fig.image_url, stream=True)
    ctype = r.headers.get("content-type", "")
    if not ctype.lower().startswith("image/"):
        raise RuntimeError(f"not image content-type: {ctype} from {fig.image_url}")

    chunks = []
    total = 0
    for chunk in r.iter_content(chunk_size=65536):
        if not chunk:
            continue
        total += len(chunk)
        if total > max_bytes:
            raise RuntimeError(f"image too large ({total} bytes > {max_bytes})")
        chunks.append(chunk)
    data = b"".join(chunks)
    if len(data) < 5_000:
        raise RuntimeError(f"image unexpectedly small: {len(data)} bytes")

    ext = ext_from_response(fig.image_url, ctype)
    sample_id = f"{fig.journal_slug}-{ordinal:03d}-{safe_slug(fig.pmcid)}-{safe_slug(fig.figure_id)}"
    out_dir = assets_root / fig.journal_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{sample_id}{ext}"
    out_path.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    return out_path, sha, len(data), ctype.split(";", 1)[0]


def iter_ranked(figs: list[FigureCandidate]) -> Iterable[FigureCandidate]:
    # Keep original-article diversity by taking strongest figures first.
    return iter(sorted(figs, key=lambda x: (x.score, len(x.caption)), reverse=True))


def build(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    assets_root = root / "assets" / "raw"
    manifest_path = root / "manifests" / "raw-image-manifest.csv"
    report_path = root / "validation" / "raw-corpus-build-report.json"
    assets_root.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.8"})

    rows: list[dict[str, str]] = []
    report: dict[str, object] = {"target_total": 0, "journals": {}, "errors": []}

    global_article_count: dict[str, int] = defaultdict(int)

    for journal_slug, cfg in TARGETS.items():
        quota = int(cfg["quota"])
        report["target_total"] = int(report["target_total"]) + quota
        journal_report = {
            "target": quota,
            "downloaded": 0,
            "articles_examined": 0,
            "license_rejected": 0,
            "third_party_rejected": 0,
            "download_failed": 0,
        }
        report["journals"][journal_slug] = journal_report

        try:
            pmcids = esearch(session, str(cfg["journal_query"]), retmax=args.retmax)
        except Exception as exc:  # noqa: BLE001
            report["errors"].append(f"{journal_slug}: esearch failed: {exc}")
            continue

        downloaded_for_journal = 0
        ordinal = 0

        for pmcid in pmcids:
            if downloaded_for_journal >= quota:
                break
            if global_article_count[pmcid] >= args.max_per_article:
                continue

            article_url = PMC_ARTICLE.format(pmcid=pmcid)
            try:
                html = http_get(session, article_url).text
            except Exception as exc:  # noqa: BLE001
                report["errors"].append(f"{pmcid}: article fetch failed: {exc}")
                continue
            journal_report["articles_examined"] += 1
            soup = BeautifulSoup(html, "html.parser")
            allowed, license_name, license_url = detect_license(soup)
            if not allowed:
                journal_report["license_rejected"] += 1
                time.sleep(args.polite_delay)
                continue

            figs = extract_figures(
                soup,
                journal_slug=journal_slug,
                journal_label=str(cfg["journal_label"]),
                pmcid=pmcid,
                article_url=article_url,
                license_name=license_name,
                license_url=license_url,
            )
            if not figs:
                time.sleep(args.polite_delay)
                continue

            selected_from_article = 0
            for fig in iter_ranked(figs):
                if downloaded_for_journal >= quota:
                    break
                if selected_from_article >= args.max_per_article:
                    break
                if fig.third_party_risk:
                    journal_report["third_party_rejected"] += 1
                    continue
                # Strongly prefer mechanistic/style-relevant figures; allow lower scores only
                # once we are struggling to fill the journal quota.
                remaining_articles = max(1, len(pmcids) - journal_report["articles_examined"])
                remaining_needed = quota - downloaded_for_journal
                strict_phase = remaining_articles > remaining_needed * 2
                if strict_phase and fig.score < args.min_score:
                    continue

                ordinal += 1
                try:
                    out_path, sha, size_bytes, content_type = download_figure(
                        session,
                        fig,
                        assets_root=assets_root,
                        ordinal=ordinal,
                        max_bytes=args.max_image_bytes,
                    )
                except Exception as exc:  # noqa: BLE001
                    journal_report["download_failed"] += 1
                    report["errors"].append(
                        f"{pmcid} {fig.figure_id}: download failed: {exc}"
                    )
                    continue

                downloaded_for_journal += 1
                selected_from_article += 1
                global_article_count[pmcid] += 1
                journal_report["downloaded"] = downloaded_for_journal

                rows.append(
                    {
                        "sample_id": out_path.stem,
                        "journal": fig.journal_label,
                        "journal_slug": journal_slug,
                        "year": fig.publication_year,
                        "article_title": fig.article_title,
                        "doi": fig.doi,
                        "pmcid": fig.pmcid,
                        "figure_id": fig.figure_id,
                        "article_url": fig.article_url,
                        "source_image_url": fig.image_url,
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
                    }
                )
                print(
                    f"[{journal_slug}] {downloaded_for_journal}/{quota} "
                    f"{pmcid} {fig.figure_id} score={fig.score} -> {out_path.name}",
                    flush=True,
                )
                time.sleep(args.polite_delay)

            time.sleep(args.polite_delay)

    fields = [
        "sample_id",
        "journal",
        "journal_slug",
        "year",
        "article_title",
        "doi",
        "pmcid",
        "figure_id",
        "article_url",
        "source_image_url",
        "license",
        "license_url",
        "rights_status",
        "third_party_review",
        "caption_score",
        "caption",
        "asset_path",
        "content_type",
        "size_bytes",
        "sha256",
        "inspection_status",
    ]
    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    report["downloaded_total"] = len(rows)
    report["distinct_articles"] = len({r["pmcid"] for r in rows})
    report["manifest"] = str(manifest_path.relative_to(root))
    report["assets_root"] = str(assets_root.relative_to(root))
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if len(rows) >= int(report["target_total"]) else 2


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--project-root",
        default="projects/scientific-figure-style-corpus",
        help="Project root directory",
    )
    p.add_argument("--retmax", type=int, default=250)
    p.add_argument("--max-per-article", type=int, default=2)
    p.add_argument("--min-score", type=int, default=4)
    p.add_argument("--polite-delay", type=float, default=0.18)
    p.add_argument("--max-image-bytes", type=int, default=8_000_000)
    return p.parse_args()


if __name__ == "__main__":
    sys.exit(build(parse_args()))
