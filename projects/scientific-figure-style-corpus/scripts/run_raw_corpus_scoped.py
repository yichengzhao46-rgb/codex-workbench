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

# This wrapper is the canonical entry point for GitHub Actions. It prevents
# excluded journals from contributing images even if they remain defined in the
# lower-level builder as optional sources.
builder.SOURCES = [
    source
    for source in builder.SOURCES
    if str(source.get("slug", "")) not in EXCLUDED_SOURCE_SLUGS
]

if __name__ == "__main__":
    sys.exit(builder.build(builder.parse_args()))
