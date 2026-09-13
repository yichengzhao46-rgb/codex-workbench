# Zotero figure ingestion into the unified library

## Purpose

Import high-value scientific figures from PDFs already downloaded in the user's local Zotero library into the **Unified Scientific Figure Library**.

Zotero-derived figures are no longer treated as a separate database. They enter the same logical library as the validated Stage 1.5 records, but retain the `reference` tier until their rights and visual-QA requirements are satisfied.

The importer remains deliberately local and provenance-aware:

- Zotero is read-only;
- PDFs are never modified;
- extracted figures preserve source item/attachment metadata;
- every record keeps a SHA-256 checksum;
- rights, QA state and active eligibility are record-level fields;
- a reference-tier record may be retrieved for style/mechanism comparison without being silently promoted to active.

## Unified-library relationship

Master registry:

`projects/scientific-figure-style-corpus/manifests/library-registry.json`

Unified loader/index builder:

`projects/scientific-figure-style-corpus/scripts/unified_library.py`

Zotero source manifest:

`projects/scientific-figure-style-corpus/manifests/zotero-private-manifest.csv`

Physical asset root:

`projects/scientific-figure-style-corpus/assets/zotero/`

The physical folder remains separate only for provenance and auditability. Retrieval is unified.

## Script

`projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py`

## Default selection logic

### Core journals

- The ISME Journal
- Nature Communications
- Environmental Science & Technology
- Water Research

### Secondary accepted journals

Includes high-value related sources such as Nature Microbiology, Science Advances, Nature Water, Energy & Environmental Science, ES&T Letters, Environmental Science & Ecotechnology, Microbiome, mBio, Applied and Environmental Microbiology, and selected environmental-engineering journals.

Other journals can be admitted with `--allow-other-journals`, but they must pass the project-topic relevance threshold.

### Figure priority

The importer scores captions for:

- schematic / conceptual overview;
- mechanism / pathway;
- microbial interaction / syntrophy;
- EET / EEU / DIET / electron transfer;
- material–microbe / mineral / electrode / conductive interface;
- methane oxidation / methanotrophy;
- dark or inorganic carbon fixation;
- oxygen limitation / microoxic–anoxic / redox gradients;
- experimental design and workflow.

Routine quantitative plots are down-weighted.

## Current reference tier

The currently imported Zotero collection contains:

- **139 figure records**;
- **104 unique source articles**;
- **33 records with completed visual QA**;
- **106 records pending manual visual QA**.

These 139 records are part of the unified library's retrieval surface. They are not automatically active-eligible.

## Run

From the repository root:

```bash
python -m pip install pymupdf
python projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py \
  --repo-root . \
  --max-figures 100 \
  --max-per-article 2
```

The script attempts to locate the Zotero data directory automatically. If needed, pass it explicitly:

```bash
python projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py \
  --repo-root . \
  --zotero-root "C:/Users/<USER>/Zotero"
```

To include strongly relevant papers outside the accepted journal list:

```bash
python projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py \
  --repo-root . \
  --allow-other-journals
```

## Unified indexing

After ingestion or manifest changes, rebuild the unified row-level index with:

```bash
python projects/scientific-figure-style-corpus/scripts/unified_library.py
```

This normalizes the 42 baseline active records, Wave 1–7 additions, and Zotero reference records into one retrieval schema and performs exact SHA-256 / asset-path duplicate marking while preserving provenance aliases.

Example retrieval:

```bash
python projects/scientific-figure-style-corpus/scripts/unified_library.py \
  --query "methane electron transfer mineral interface" \
  --limit 20
```

Use `--active-only` when only validated active records are permitted.

## Promotion rule

A Zotero-derived figure starts in the `reference` tier. Promotion to `active` requires the project-defined figure-level rights verification and completed visual QA.

Until promotion, it can still contribute to:

- source discovery;
- comparison of mechanism/layout grammar;
- retrieval of relevant visual precedents;
- corpus gap analysis;
- style-routing context.

It must not silently inherit active/public reuse status.

## Manual QA

Automated PDF crop extraction is a first-pass ingestion step. Retained figures should be checked for:

1. crop completeness;
2. correct figure/caption pairing;
3. actual visual relevance;
4. duplicate or near-duplicate panels;
5. third-party reproduced material;
6. suitability for 2D/2.5D style learning;
7. consistency between the stored SHA-256 and the reviewed image.

## Design principle

There is now **one scientific figure library with record-level tiers**, not an active library plus a separate Zotero library. Physical storage may remain separated for provenance, but task retrieval should use the unified interface by default.
