#!/usr/bin/env python3
"""Run the raw corpus builder with the curated journal scope for this project."""

from __future__ import annotations

import sys

import build_raw_corpus as builder

EXCLUDED_SOURCE_SLUGS = {
    "est-letters",
    "microbiome",
    "mbio",
    "npj-biofilms-microbiomes",
    "communications-biology",
    "water-research-x",
    "environmental-microbiome",
}

# Additional high-level journals allowed as fill sources. They do not bypass
# the topic/figure-quality/license filters in build_raw_corpus.py.
ELITE_SCOPE_SOURCES = [
    # Flagship journals
    {"slug": "nature", "journal_label": "Nature", "journal_query": '"Nature"[jour]', "tier": "elite-general", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "science", "journal_label": "Science", "journal_query": '"Science"[jour]', "tier": "elite-general", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "cell", "journal_label": "Cell", "journal_query": '"Cell"[jour]', "tier": "elite-general", "first_pass_cap": 4, "max_cap": 8},

    # Nature Portfolio — selected for relevance to environmental microbiology,
    # biohybrids, carbon cycling, materials and mechanistic illustration.
    {"slug": "nature-ecology-evolution", "journal_label": "Nature Ecology & Evolution", "journal_query": '"Nat Ecol Evol"[jour]', "tier": "elite-scope", "first_pass_cap": 5, "max_cap": 10},
    {"slug": "nature-biotechnology", "journal_label": "Nature Biotechnology", "journal_query": '"Nat Biotechnol"[jour]', "tier": "elite-scope", "first_pass_cap": 5, "max_cap": 10},
    {"slug": "nature-chemical-biology", "journal_label": "Nature Chemical Biology", "journal_query": '"Nat Chem Biol"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "nature-energy", "journal_label": "Nature Energy", "journal_query": '"Nat Energy"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "nature-catalysis", "journal_label": "Nature Catalysis", "journal_query": '"Nat Catal"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "nature-sustainability", "journal_label": "Nature Sustainability", "journal_query": '"Nat Sustain"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},

    # Science family: Science Advances is already defined in the base builder.
    # Other Science specialty journals are intentionally not added unless they
    # become clearly relevant to the corpus scope.

    # Cell Press — selected for systems microbiology, host/microbe interaction,
    # environmental/energy materials, and polished mechanistic schematics.
    {"slug": "cell-host-microbe", "journal_label": "Cell Host & Microbe", "journal_query": '"Cell Host Microbe"[jour]', "tier": "elite-scope", "first_pass_cap": 5, "max_cap": 10},
    {"slug": "cell-systems", "journal_label": "Cell Systems", "journal_query": '"Cell Syst"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "joule", "journal_label": "Joule", "journal_query": '"Joule"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "one-earth", "journal_label": "One Earth", "journal_query": '"One Earth"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "matter", "journal_label": "Matter", "journal_query": '"Matter"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "chem", "journal_label": "Chem", "journal_query": '"Chem"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
    {"slug": "cell-reports-physical-science", "journal_label": "Cell Reports Physical Science", "journal_query": '"Cell Rep Phys Sci"[jour]', "tier": "elite-scope", "first_pass_cap": 4, "max_cap": 8},
]

# This wrapper is the canonical entry point for GitHub Actions. It prevents
# excluded journals from contributing images even if they remain defined in the
# lower-level builder as optional sources, then appends the curated elite pool.
base_sources = [
    source
    for source in builder.SOURCES
    if str(source.get("slug", "")) not in EXCLUDED_SOURCE_SLUGS
]

existing = {str(source.get("slug", "")) for source in base_sources}
for source in ELITE_SCOPE_SOURCES:
    if str(source.get("slug", "")) not in existing:
        base_sources.append(source)
        existing.add(str(source.get("slug", "")))

builder.SOURCES = base_sources

if __name__ == "__main__":
    sys.exit(builder.build(builder.parse_args()))
