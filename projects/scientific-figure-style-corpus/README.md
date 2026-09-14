# Unified 2D/2.5D Scientific Figure Library

> **Current curated reference layer:** the user-selected main library now uses canonical IDs `M001`–`M021`; the separate bioinformatics library uses `BI001`–`BI022`. For current style work, use `manifests/main-reference-catalog.csv`, `../bioinformatics-figure-reference-library/reference-catalog.csv`, and `../figure-reference-libraries/registry.json`. The larger unified corpus described below is retained as the historical harvest/provenance layer.

## Objective

Build one source-backed scientific figure library for the experimental `scientific-figure-style-router` in `codex-playbook` PR #23.

The architecture is:

> **real source images → figure-level annotation → unified index → Router retrieval → reusable visual decisions**

## Current snapshot

The library has one logical retrieval surface with two provenance tiers:

- **235 source rows** total;
- **96 active source rows** from the validated baseline + Stage 1.5 refinement;
- **139 reference source rows** from 104 Zotero/Codex articles;
- exact SHA/path deduplication identifies **1 active alias**, leaving **234 canonical unique records = 95 active + 139 reference**;
- Zotero visual QA: **33 complete**, **106 pending**.

The duplicate alias is retained for provenance and excluded from normal retrieval. `active` and `reference` are tiers inside one library, not separate databases.

## Authoritative runtime files

- current curated main catalog: `manifests/main-reference-catalog.csv`
- current curated main-set note: `CURATED-REFERENCE-SET.md`
- cross-library canonical-ID registry: `../figure-reference-libraries/registry.json`
- historical registry: `manifests/library-registry.json`
- historical materialized index: `manifests/unified-library-index.csv`
- generated summary: `manifests/unified-library-summary.json`
- builder / validator / low-level query: `scripts/unified_library.py`
- Router-facing query adapter: `scripts/router_reference_query.py`
- end-to-end retrieval validation: `scripts/validate_router_retrieval.py`
- real-task validation cases: `validation/router-retrieval-test-cases.json`

## Build, validate, query

From the repository root:

```bash
python projects/scientific-figure-style-corpus/scripts/unified_library.py \
  --project-root projects/scientific-figure-style-corpus \
  build
```

Validate the materialized index, canonical taxonomy, current snapshot, asset presence, and every stored SHA-256:

```bash
python projects/scientific-figure-style-corpus/scripts/unified_library.py \
  --project-root projects/scientific-figure-style-corpus \
  validate \
  --check-assets \
  --strict-snapshot
```

Router-style retrieval is read-only and should normally use the adapter:

```bash
python projects/scientific-figure-style-corpus/scripts/router_reference_query.py \
  --text "methane EET material microbe interface" \
  --limit 8
```

The query command does **not** rebuild or rewrite the index.

## Canonical Router schema

The unified builder preserves source text while normalizing records to the Router contract.

Primary purpose:

`conceptual_overview | microbial_interaction | mechanistic_pathway | metabolic_pathway | electron_transfer | material_microbe_interface | environmental_process | experimental_design | comparative_perturbation | integrated_mechanism | graphical_abstract | multiscale_zoom`

Style family:

`flat_2d_mechanism | soft_2_5d_schematic | pathway_cutaway_2d | editorial_2d_overview`

Layout:

`linear_flow | two_organism_interaction | central_hub | mirrored_comparison | zoom_in_multiscale | circular_pathway | layered_gradient | evidence_to_model | other`

Information density:

`low | medium | high`

Original free-text labels remain in `*_raw` fields so normalization remains auditable.

## Retrieval policy

For current user-selected style work, use the curated `M###` / `BI###` catalogs first. The historical unified index remains available as a broader provenance/research surface.

Historical retrieval defaults:

1. search both tiers through the materialized unified index;
2. rank scientific relevance first;
3. use active status only as a small tie-break preference;
4. exclude exact duplicate aliases (`duplicate_of`) from normal results;
5. preserve QA, provenance, rights, and active eligibility on every row;
6. do not promote a reference record to active merely because it is relevant.

## Physical storage

Physical locations remain provenance-preserving. Canonical renumbering does **not** rename binaries, because doing so would break historical manifests, checksums, and source traceability.

```text
projects/scientific-figure-style-corpus/
├── assets/
│   ├── raw/
│   ├── stage1_5/
│   └── zotero/
├── manifests/
│   ├── main-reference-catalog.csv      # current curated M### IDs
│   ├── library-registry.json
│   ├── unified-library-index.csv
│   ├── unified-library-summary.json
│   ├── raw-image-manifest.csv
│   ├── zotero-private-manifest.csv
│   └── stage1_5*_harvested_figures.csv
├── CURATED-REFERENCE-SET.md
├── scripts/
└── validation/
```

## Validation

The historical corpus workflow performs raw-image validation, unified-index materialization, schema/snapshot/asset/SHA validation, and Router retrieval testing. The current curated layer is separately tracked by canonical catalogs and the cross-library migration map.

## Key quality principle

The goal is not to imitate journal branding. Scientific purpose and information structure lead retrieval; journal/source family is a secondary filter. The system should learn **which visual language works for which scientific job** while preserving evidence boundaries and provenance.
