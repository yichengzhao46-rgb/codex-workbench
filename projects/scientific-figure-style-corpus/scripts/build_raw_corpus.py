#!/usr/bin/env python3
"""Build a rights-aware raw scientific-figure corpus from PMC.

A figure counts only when:
- the article is available in PMC;
- the article exposes an allowed redistribution license (CC BY or CC0);
- the caption does not show obvious third-party reuse language;
- the actual image bytes are downloaded successfully;
- provenance and SHA256 are recorded.

The builder prioritizes the four core journal families, but it can fill the
100-image gate from other high-level journals in scope when Water Research,
ES&T, or another source family does not expose enough legally mirrorable images.

PMC figure links sometimes point to an HTML zoom/tileshop wrapper rather than to
the underlying JPG/PNG/WebP. This builder resolves those wrappers recursively and
also tries the legacy /articles/<PMCID>/bin/<filename> path when a wrapper query
contains an image id.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html as html_lib
import json
import re
import sys
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

NCBI_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PMC_ARTICLE = "https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"

USER_AGENT = (
    "codex-workbench-scientific-figure-corpus/0.3 "
    "(noncommercial research corpus builder; contact via repository owner)"
)

SOURCES = [
    {"slug": "isme", "journal_label": "The ISME Journal", "journal_query": '"ISME J"[jour]', "tier": "core", "first_pass_cap": 20, "max_cap": 30},
    {"slug": "nature-communications", "journal_label": "Nature Communications", "journal_query": '"Nat Commun"[jour]', "tier": "core", "first_pass_cap": 20, "max_cap": 30},
    {"slug": "est", "journal_label": "Environmental Science & Technology", "journal_query": '"Environ Sci Technol"[jour]', "tier": "core", "first_pass_cap": 15, "max_cap": 25},
    {"slug": "water-research", "journal_label": "Water Research", "journal_query": '"Water Res"[jour]', "tier": "core", "first_pass_cap": 10, "max_cap": 20},
    {"slug": "nature-microbiology", "journal_label": "Nature Microbiology", "journal_query": '"Nat Microbiol"[jour]', "tier": "scope-high", "first_pass_cap": 8, "max_cap": 15},
    {"slug": "nature-water", "journal_label": "Nature Water", "journal_query": '"Nat Water"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "science-advances", "journal_label": "Science Advances", "journal_query": '"Sci Adv"[jour]', "tier": "scope-high", "first_pass_cap": 8, "max_cap": 15},
    {"slug": "ees", "journal_label": "Energy & Environmental Science", "journal_query": '"Energy Environ Sci"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "est-letters", "journal_label": "Environmental Science & Technology Letters", "journal_query": '"Environ Sci Technol Lett"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "ese", "journal_label": "Environmental Science & Ecotechnology", "journal_query": '"Environ Sci Ecotechnol"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "microbiome", "journal_label": "Microbiome", "journal_query": '"Microbiome"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "mbio", "journal_label": "mBio", "journal_query": '"mBio"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "isme-communications", "journal_label": "ISME Communications", "journal_query": '"ISME Commun"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "npj-biofilms-microbiomes", "journal_label": "npj Biofilms and Microbiomes", "journal_query": '"NPJ Biofilms Microbiomes"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "communications-biology", "journal_label": "Communications Biology", "journal_query": '"Commun Biol"[jour]', "tier": "scope-high", "first_pass_cap": 6, "max_cap": 12},
    {"slug": "water-research-x", "journal_label": "Water Research X", "journal_query": '"Water Res X"[jour]', "tier": "scope-high", "first_pass_cap": 5, "max_cap": 10},
    {"slug": "environmental-microbiome", "journal_label": "Environmental Microbiome", "journal_query": '"Environ Microbiome"[jour]', "tier": "scope-high", "first_pass_cap": 5, "max_cap": 10},
]

POSITIVE_TERMS = {
    "schematic": 9, "scheme": 7, "conceptual": 8, "model": 5, "mechanism": 8,
    "pathway": 7, "metabolic": 6, "metabolism": 6, "electron transfer": 10,
    "electron transport": 8, "extracellular electron": 10, "interspecies": 8,
    "syntroph": 8, "cross-feeding": 9, "interaction": 6, "interface": 7,
    "biofilm": 5, "aggregate": 5, "mineral": 6, "conductive": 7, "electrode": 7,
    "redox": 6, "oxygen": 4, "oxic": 5, "anoxic": 5, "microoxic": 7,
    "methane": 6, "methanotroph": 8, "carbon fixation": 8, "carbon cycle": 6,
    "biogeochemical": 5, "environmental gradient": 7, "experimental design": 8,
    "workflow": 6, "overview": 5, "proposed": 5, "illustration": 6, "diagram": 7,
    "biohybrid": 8, "semiconductor": 7, "direct interspecies electron": 10,
    "eet": 5, "eeu": 5, "diet": 5, "riboflavin": 6, "formate": 5, "acetate": 4,
}

NEGATIVE_TERMS = {
    "boxplot": -5, "box plot": -5, "volcano plot": -7, "heatmap": -4,
    "principal component": -5, "pca": -4, "rarefaction": -6,
    "phylogenetic tree": -4, "bar chart": -4, "bar graph": -4,
    "scatter": -3, "regression": -3,
}

THIRD_PARTY_RISK_TERMS = (
    "reproduced from", "adapted from", "modified from", "reprinted from",
    "with permission", "permission from", "copyright ", "© ", "credit:", "courtesy of",
)

ALLOWED_LICENSE_PATTERNS = (
    re.compile(r"creativecommons\.org/licenses/by/(?:[0-9.]+/)?", re.I),
    re.compile(r"creative commons attribution(?: [0-9.]+)?", re.I),
    re.compile(r"\bcc[- ]?by\b", re.I),
    re.compile(r"creativecommons\.org/publicdomain/zero/", re.I),
    re.compile(r"\bcc0\b", re.I),
)

DISALLOWED_LICENSE_MARKERS = (
    "by-nc", "by-nd", "by-nc-nd", "noncommercial", "no derivatives", "no-derivatives",
)

IMAGE_EXT_BY_CT = {
    "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/png": ".png",
    "image/gif": ".gif", "image/tiff": ".tif", "image/webp": ".webp",
}

IMAGE_URL_RE = re.compile(
    r'''(?P<url>https?://[^\s"'<>\\]+?\.(?:png|jpe?g|gif|tiff?|webp)(?:\?[^\s"'<>\\]*)?|/[^\s"'<>\\]+?\.(?:png|jpe?g|gif|tiff?|webp)(?:\?[^\s"'<>\\]*)?)''',
    re.I,
)


@dataclass
class FigureCandidate:
    journal_slug: str
    journal_label: str
    source_tier: str
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
            r = session.get(url, timeout=45, allow_redirects=True, **kwargs)
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
    params = {"db": "pmc", "term": journal_query, "retmax": str(retmax), "retmode": "json", "sort": "pub date"}
    r = http_get(session, NCBI_ESEARCH, params=params)
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    return [f"PMC{x}" if not str(x).upper().startswith("PMC") else str(x) for x in ids]


def text_or_empty(node) -> str:
    if not node:
        return ""
    return " ".join(node.get_text(" ", strip=True).split())


def find_meta(soup: BeautifulSoup, name: str) -> str:
    tag = soup.find("meta", attrs={"name": name})
    return str(tag["content"]).strip() if tag and tag.get("content") else ""


def detect_license(soup: BeautifulSoup) -> tuple[bool, str, str]:
    page_text = " ".join(soup.stripped_strings)
    cc_links = []
    for a in soup.find_all("a", href=True):
        href = str(a["href"])
        if "creativecommons.org/" in href.lower():
            cc_links.append((href, text_or_empty(a)))
    for href, text in cc_links:
        h = href.lower()
        if any(x in h for x in ("by-nc", "by-nd", "by-nc-nd")):
            continue
        if "/licenses/by/" in h:
            return True, text or "CC BY", href
        if "/publicdomain/zero/" in h:
            return True, text or "CC0", href
    for pat in ALLOWED_LICENSE_PATTERNS:
        m = pat.search(page_text)
        if m:
            window = page_text[max(0, m.start() - 120):m.end() + 180].lower()
            if any(x in window for x in DISALLOWED_LICENSE_MARKERS):
                continue
            return True, m.group(0), ""
    return False, "", ""


def figure_score(caption: str) -> int:
    t = caption.lower()
    score = sum(weight for term, weight in POSITIVE_TERMS.items() if term in t)
    score += sum(weight for term, weight in NEGATIVE_TERMS.items() if term in t)
    if len(caption) > 120:
        score += 1
    if len(caption) > 350:
        score += 1
    return score


def has_third_party_risk(caption: str) -> str:
    lower = caption.lower()
    return "; ".join(term for term in THIRD_PARTY_RISK_TERMS if term in lower)


def _srcset_urls(value: str) -> list[str]:
    return [part.strip().split(" ", 1)[0] for part in value.split(",") if part.strip()]


def html_image_candidates(html_text: str, base_url: str, preferred_filename: str = "") -> list[str]:
    soup = BeautifulSoup(html_text, "html.parser")
    candidates: list[str] = []
    for attrs in ({"property": "og:image"}, {"name": "twitter:image"}, {"name": "citation_image"}):
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            candidates.append(urljoin(base_url, str(tag["content"])))
    for link in soup.find_all("link", href=True):
        rel = " ".join(link.get("rel") or []).lower()
        if "image_src" in rel or "preload" in rel:
            candidates.append(urljoin(base_url, str(link["href"])))
    for tag in soup.find_all(["img", "source"]):
        for attr in ("data-src", "data-original", "data-full-src", "data-image-src", "src"):
            value = tag.get(attr)
            if value:
                candidates.append(urljoin(base_url, str(value)))
        for attr in ("srcset", "data-srcset"):
            value = tag.get(attr)
            if value:
                candidates.extend(urljoin(base_url, u) for u in _srcset_urls(str(value)))
    for a in soup.find_all("a", href=True):
        href = str(a["href"])
        if re.search(r"\.(?:png|jpe?g|gif|tiff?|webp)(?:\?|$)", href, re.I):
            candidates.append(urljoin(base_url, href))
    decoded = html_lib.unescape(html_text).replace("\\/", "/")
    for match in IMAGE_URL_RE.finditer(decoded):
        candidates.append(urljoin(base_url, unquote(match.group("url"))))
    seen: set[str] = set()
    unique: list[str] = []
    for url in candidates:
        if url and url not in seen:
            seen.add(url)
            unique.append(url)
    if preferred_filename:
        p = preferred_filename.lower()
        unique.sort(key=lambda u: (p not in unquote(u).lower(), len(u)))
    return unique


def wrapper_filename(url: str) -> str:
    values = parse_qs(urlparse(url).query).get("id", [])
    if not values:
        return ""
    value = Path(unquote(values[0])).name
    return value if re.search(r"\.(?:png|jpe?g|gif|tiff?|webp)$", value, re.I) else ""


def direct_pmc_bin_candidates(pmcid: str, filename: str) -> list[str]:
    if not filename:
        return []
    return [
        f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/bin/{filename}",
        f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/bin/{filename}",
    ]


def pick_image_url(fig, article_url: str) -> str:
    for a in fig.find_all("a", href=True):
        href = str(a["href"])
        lower = href.lower()
        if re.search(r"\.(?:png|jpe?g|gif|tiff?|webp)(?:\?|$)", href, re.I) or "tileshop_pmc" in lower or "inline.html" in lower:
            return urljoin(article_url, href)
    img = fig.find("img")
    if not img:
        return ""
    for attr in ("data-src", "data-original", "data-full-src", "src"):
        value = img.get(attr)
        if value:
            return urljoin(article_url, str(value))
    return ""


def extract_figures(soup: BeautifulSoup, journal_slug: str, journal_label: str, source_tier: str, pmcid: str, article_url: str, license_name: str, license_url: str) -> list[FigureCandidate]:
    title = find_meta(soup, "citation_title") or text_or_empty(soup.find("h1"))
    doi = find_meta(soup, "citation_doi")
    pub_date = find_meta(soup, "citation_publication_date") or find_meta(soup, "citation_date")
    year_match = re.search(r"(19|20)\d{2}", pub_date)
    year = year_match.group(0) if year_match else ""
    nodes = list(soup.find_all("figure")) or list(soup.find_all("div", class_=re.compile(r"\bfig\b", re.I)))
    figures = []
    for idx, fig in enumerate(nodes, 1):
        cap_node = fig.find("figcaption") or fig.find(class_=re.compile("caption", re.I))
        caption = text_or_empty(cap_node)
        if not caption:
            continue
        image_url = pick_image_url(fig, article_url)
        if not image_url:
            continue
        figures.append(FigureCandidate(
            journal_slug=journal_slug,
            journal_label=journal_label,
            source_tier=source_tier,
            pmcid=pmcid,
            doi=doi,
            article_title=title,
            publication_year=year,
            article_url=article_url,
            figure_id=str(fig.get("id") or f"fig{idx}"),
            caption=caption,
            image_url=image_url,
            license_name=license_name,
            license_url=license_url,
            score=figure_score(caption),
            third_party_risk=has_third_party_risk(caption),
        ))
    return figures


def safe_slug(s: str) -> str:
    return (re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")[:120] or "figure")


def ext_from_response(url: str, content_type: str) -> str:
    ctype = content_type.split(";", 1)[0].strip().lower()
    if ctype in IMAGE_EXT_BY_CT:
        return IMAGE_EXT_BY_CT[ctype]
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    return ".img"


def resolve_image_bytes(session: requests.Session, initial_urls: list[str], pmcid: str, max_bytes: int, max_hops: int = 3) -> tuple[bytes, str, str]:
    queue: deque[tuple[str, int, str]] = deque()
    for url in initial_urls:
        if url:
            queue.append((url, 0, wrapper_filename(url)))
    seen: set[str] = set()
    last_errors: list[str] = []
    while queue:
        url, depth, preferred_filename = queue.popleft()
        if not url or url in seen or depth > max_hops:
            continue
        seen.add(url)
        if preferred_filename:
            for candidate in direct_pmc_bin_candidates(pmcid, preferred_filename):
                if candidate not in seen:
                    queue.appendleft((candidate, depth + 1, preferred_filename))
        try:
            r = http_get(session, url, stream=True)
        except Exception as exc:  # noqa: BLE001
            last_errors.append(f"{url}: {exc}")
            continue
        ctype = r.headers.get("content-type", "").split(";", 1)[0].strip().lower()
        if ctype.startswith("image/"):
            parts = []
            total = 0
            for chunk in r.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                total += len(chunk)
                if total > max_bytes:
                    raise RuntimeError(f"image too large ({total} bytes > {max_bytes})")
                parts.append(chunk)
            data = b"".join(parts)
            if len(data) < 5_000:
                last_errors.append(f"{url}: image unexpectedly small ({len(data)} bytes)")
                continue
            return data, r.url, ctype
        if "html" not in ctype and not ctype.startswith("text/"):
            last_errors.append(f"{url}: unsupported content-type {ctype}")
            continue
        if depth >= max_hops:
            last_errors.append(f"{url}: wrapper depth exceeded")
            continue
        body = r.content[:2_000_000].decode(r.encoding or "utf-8", errors="replace")
        filename = preferred_filename or wrapper_filename(r.url)
        for candidate in html_image_candidates(body, r.url, filename)[:30]:
            if candidate not in seen:
                queue.append((candidate, depth + 1, filename))
    raise RuntimeError("could not resolve image bytes: " + " | ".join(last_errors[-5:]))


def download_figure(session: requests.Session, fig: FigureCandidate, assets_root: Path, ordinal: int, max_bytes: int) -> tuple[Path, str, int, str, str]:
    figure_page = urljoin(fig.article_url, f"figure/{fig.figure_id}/")
    initial_urls = [fig.image_url, figure_page]
    filename = wrapper_filename(fig.image_url)
    if filename:
        initial_urls = direct_pmc_bin_candidates(fig.pmcid, filename) + initial_urls
    data, resolved_url, content_type = resolve_image_bytes(session, initial_urls, fig.pmcid, max_bytes)
    ext = ext_from_response(resolved_url, content_type)
    sample_id = f"{fig.journal_slug}-{ordinal:03d}-{safe_slug(fig.pmcid)}-{safe_slug(fig.figure_id)}"
    out_dir = assets_root / fig.journal_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{sample_id}{ext}"
    out_path.write_bytes(data)
    return out_path, hashlib.sha256(data).hexdigest(), len(data), content_type, resolved_url


def iter_ranked(figs: list[FigureCandidate]) -> Iterable[FigureCandidate]:
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
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8",
    })

    rows: list[dict[str, str]] = []
    report: dict[str, object] = {
        "target_total": args.target_total,
        "journals": {},
        "errors": [],
        "source_policy": {"core_journals_prioritized": True, "fixed_water_research_quota": False, "scope_high_fill_allowed": True},
    }
    global_article_count: dict[str, int] = defaultdict(int)
    seen_figures: set[tuple[str, str]] = set()
    journal_ordinals: dict[str, int] = defaultdict(int)
    source_cache: dict[str, list[str]] = {}

    for source in SOURCES:
        report["journals"][source["slug"]] = {
            "tier": source["tier"], "first_pass_cap": source["first_pass_cap"], "max_cap": source["max_cap"],
            "downloaded": 0, "articles_examined": 0, "license_rejected": 0,
            "third_party_rejected": 0, "download_failed": 0,
        }

    def process_source(source: dict[str, object], cap: int) -> None:
        if len(rows) >= args.target_total:
            return
        slug = str(source["slug"])
        cfg_report = report["journals"][slug]
        if int(cfg_report["downloaded"]) >= cap:
            return
        if slug not in source_cache:
            try:
                source_cache[slug] = esearch(session, str(source["journal_query"]), retmax=args.retmax)
            except Exception as exc:  # noqa: BLE001
                report["errors"].append(f"{slug}: esearch failed: {exc}")
                source_cache[slug] = []
                return
        pmcids = source_cache[slug]
        for pmcid in pmcids:
            if len(rows) >= args.target_total or int(cfg_report["downloaded"]) >= cap:
                break
            if global_article_count[pmcid] >= args.max_per_article:
                continue
            article_url = PMC_ARTICLE.format(pmcid=pmcid)
            try:
                html = http_get(session, article_url).text
            except Exception as exc:  # noqa: BLE001
                report["errors"].append(f"{pmcid}: article fetch failed: {exc}")
                continue
            cfg_report["articles_examined"] = int(cfg_report["articles_examined"]) + 1
            soup = BeautifulSoup(html, "html.parser")
            allowed, license_name, license_url = detect_license(soup)
            if not allowed:
                cfg_report["license_rejected"] = int(cfg_report["license_rejected"]) + 1
                time.sleep(args.polite_delay)
                continue
            figs = extract_figures(
                soup, slug, str(source["journal_label"]), str(source["tier"]), pmcid,
                article_url, license_name, license_url,
            )
            if not figs:
                time.sleep(args.polite_delay)
                continue
            selected_from_article = global_article_count[pmcid]
            for fig in iter_ranked(figs):
                if len(rows) >= args.target_total or int(cfg_report["downloaded"]) >= cap or selected_from_article >= args.max_per_article:
                    break
                key = (fig.pmcid, fig.figure_id)
                if key in seen_figures:
                    continue
                if fig.third_party_risk:
                    cfg_report["third_party_rejected"] = int(cfg_report["third_party_rejected"]) + 1
                    continue
                remaining_needed = args.target_total - len(rows)
                remaining_articles = max(1, len(pmcids) - int(cfg_report["articles_examined"]))
                if remaining_articles > remaining_needed and fig.score < args.min_score:
                    continue
                journal_ordinals[slug] += 1
                try:
                    out_path, sha, size_bytes, content_type, resolved_url = download_figure(
                        session, fig, assets_root, journal_ordinals[slug], args.max_image_bytes,
                    )
                except Exception as exc:  # noqa: BLE001
                    cfg_report["download_failed"] = int(cfg_report["download_failed"]) + 1
                    report["errors"].append(f"{pmcid} {fig.figure_id}: download failed: {exc}")
                    continue
                cfg_report["downloaded"] = int(cfg_report["downloaded"]) + 1
                selected_from_article += 1
                global_article_count[pmcid] += 1
                seen_figures.add(key)
                rows.append({
                    "sample_id": out_path.stem,
                    "journal": fig.journal_label,
                    "journal_slug": slug,
                    "source_tier": fig.source_tier,
                    "year": fig.publication_year,
                    "article_title": fig.article_title,
                    "doi": fig.doi,
                    "pmcid": fig.pmcid,
                    "figure_id": fig.figure_id,
                    "article_url": fig.article_url,
                    "source_image_url": fig.image_url,
                    "resolved_image_url": resolved_url,
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
                })
                print(f"[{slug}] {cfg_report['downloaded']}/{cap} overall={len(rows)}/{args.target_total} {pmcid} {fig.figure_id} score={fig.score} -> {out_path.name}", flush=True)
                time.sleep(args.polite_delay)
            time.sleep(args.polite_delay)

    for source in SOURCES:
        process_source(source, int(source["first_pass_cap"]))
        if len(rows) >= args.target_total:
            break
    if len(rows) < args.target_total:
        for source in SOURCES:
            process_source(source, int(source["max_cap"]))
            if len(rows) >= args.target_total:
                break

    fields = [
        "sample_id", "journal", "journal_slug", "source_tier", "year", "article_title", "doi", "pmcid",
        "figure_id", "article_url", "source_image_url", "resolved_image_url", "license", "license_url",
        "rights_status", "third_party_review", "caption_score", "caption", "asset_path", "content_type",
        "size_bytes", "sha256", "inspection_status",
    ]
    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    report["downloaded_total"] = len(rows)
    report["distinct_articles"] = len({r["pmcid"] for r in rows})
    report["represented_journals"] = sorted({r["journal_slug"] for r in rows})
    report["core_images"] = sum(1 for r in rows if r["source_tier"] == "core")
    report["scope_high_images"] = sum(1 for r in rows if r["source_tier"] == "scope-high")
    report["manifest"] = str(manifest_path.relative_to(root))
    report["assets_root"] = str(assets_root.relative_to(root))
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if len(rows) >= args.target_total else 2


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", default="projects/scientific-figure-style-corpus")
    p.add_argument("--target-total", type=int, default=100)
    p.add_argument("--retmax", type=int, default=400)
    p.add_argument("--max-per-article", type=int, default=2)
    p.add_argument("--min-score", type=int, default=4)
    p.add_argument("--polite-delay", type=float, default=0.14)
    p.add_argument("--max-image-bytes", type=int, default=12_000_000)
    return p.parse_args()


if __name__ == "__main__":
    sys.exit(build(parse_args()))
