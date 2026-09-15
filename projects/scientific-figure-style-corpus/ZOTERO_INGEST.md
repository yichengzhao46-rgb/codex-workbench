# Zotero figure ingestion into the unified library

## Purpose

Import high-value scientific figures from PDFs in the user's Zotero library into the **Unified Scientific Figure Library**.

Zotero figures are the `reference` tier of the same logical library used by the validated active figures. Physical storage stays separate for provenance; retrieval does not.

## Current imported reference tier

- **139 source rows**;
- **104 unique source articles**;
- **33 visual-QA complete**;
- **106 pending manual visual QA**.

Reference status controls QA/active eligibility. It does not prevent a scientifically relevant record from being returned as a design reference.

## Authoritative files

- source manifest: `manifests/zotero-private-manifest.csv`
- assets: `assets/zotero/`
- master registry: `manifests/library-registry.json`
- materialized unified index: `manifests/unified-library-index.csv`
- builder/validator: `scripts/unified_library.py`
- Router adapter: `scripts/router_reference_query.py`

## Ingestion

Main importer:

`projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py`

The importer is local/provenance-aware:

- Zotero is read-only;
- PDFs are never modified;
- source item/attachment metadata are retained;
- extracted figures carry SHA-256 checksums;
- visual QA and active eligibility remain explicit fields.

Typical run from repository root:

```bash
python -m pip install -r projects/scientific-figure-style-corpus/scripts/requirements.txt
python projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py \
  --repo-root . \
  --max-per-article 2
```

If Zotero cannot be located automatically:

```bash
python projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py \
  --repo-root . \
  --zotero-root "C:/Users/<USER>/Zotero"
```

Use `--allow-other-journals` only when relevant papers outside the normal journal set should be considered.

## Rebuild the unified index

After any source-manifest or ingestion change:

```bash
python projects/scientific-figure-style-corpus/scripts/unified_library.py \
  --project-root projects/scientific-figure-style-corpus \
  build
```

Then validate the generated index against the canonical Router schema, current snapshot, stored files, and SHA-256 values:

```bash
python projects/scientific-figure-style-corpus/scripts/unified_library.py \
  --project-root projects/scientific-figure-style-corpus \
  validate \
  --check-assets \
  --strict-snapshot
```

The current snapshot is **235 source rows**. Exact deduplication identifies one active alias, so the canonical retrieval surface contains **234 unique records = 95 active + 139 reference** while preserving all 235 source rows for provenance.

## Query through the Router adapter

Normal figure-design retrieval should use the read-only adapter:

```bash
python projects/scientific-figure-style-corpus/scripts/router_reference_query.py \
  --text "methane electron transfer mineral interface" \
  --limit 8
```

Structured filters are available for canonical Router fields such as `--purpose`, `--layout`, `--style-family`, `--density`, `--topic`, and `--tier`.

The query adapter never rebuilds or overwrites the index.

## Selection logic

High-value captions are prioritized for:

- schematic / conceptual overview;
- mechanism / pathway;
- microbial interaction / syntrophy;
- EET / EEU / DIET;
- material–microbe / mineral / electrode / conductive interfaces;
- methane oxidation / methanotrophy;
- dark or inorganic carbon fixation;
- oxygen limitation / microoxic–anoxic / redox gradients;
- experimental design and workflow.

Routine quantitative plots are down-weighted.

## Promotion rule

A Zotero-derived record remains `reference` until the project-defined active gates are satisfied. Relevance in a Router query does not by itself promote the record.

Promotion and retrieval are deliberately separate concepts:

- **retrieval** asks whether the figure is useful for the current design problem;
- **promotion** asks whether its QA/classification/provenance state is strong enough for the validated active tier.

## Manual QA

Automated PDF crop extraction is only the first pass. Retained records should be reviewed for:

1. crop completeness;
2. figure/caption pairing;
3. visual relevance;
4. exact and near-duplicate panels;
5. third-party reproduced material;
6. suitability for 2D/2.5D style learning;
7. checksum consistency;
8. canonical purpose/style/layout annotation quality.

## Design principle

There is **one scientific figure library with record-level tiers**. Do not query `assets/zotero/` as a separate database and do not use the old pilot `corpus-index.csv` as the authoritative retrieval index. The materialized `unified-library-index.csv` is the runtime retrieval surface.
