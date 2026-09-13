# Unified 2D/2.5D Scientific Figure Library

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

The duplicate alias is retained for provenance but excluded from normal retrieval. `active` and `reference` are tiers inside one library, not separate databases.

## Authoritative runtime files

- registry: `manifests/library-registry.json`
- materialized index: `manifests/unified-library-index.csv`
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

Default figure-design retrieval:

1. search both tiers through the materialized unified index;
2. rank scientific relevance first;
3. use active status only as a small tie-break preference;
4. exclude exact duplicate aliases (`duplicate_of`) from normal results;
5. preserve QA, provenance, rights, and active eligibility on every row;
6. do not promote a reference record to active merely because it is relevant.

This is important for tasks where the reference tier contains the strongest precedent—for example methanotroph biohybrids or graphical abstracts. The Router should not insert a less relevant active record simply to force tier balance.

## Physical storage

Physical locations remain provenance-preserving:

```text
projects/scientific-figure-style-corpus/
├── assets/
│   ├── raw/                       # baseline raw corpus; 42 A/B source rows selected from it
│   ├── stage1_5/                  # Wave 1–7 active additions
│   └── zotero/                    # 139 reference assets
├── manifests/
│   ├── library-registry.json
│   ├── unified-library-index.csv
│   ├── unified-library-summary.json
│   ├── raw-image-manifest.csv
│   ├── zotero-private-manifest.csv
│   └── stage1_5*_harvested_figures.csv
├── scripts/
│   ├── unified_library.py
│   ├── router_reference_query.py
│   └── validate_router_retrieval.py
└── validation/
```

Physical separation is for provenance and auditability only; retrieval is unified.

## Validation

The main corpus workflow now performs, in order:

1. raw 100-image validation;
2. unified-index materialization;
3. strict unified schema/snapshot/asset/SHA validation;
4. Router retrieval validation against eight real drawing tasks;
5. commit of the generated index and validation reports only after the gates pass.

The eight task families cover Bath–RP dark carbon fixation, Bath–Bio-Se, oxygen perturbation, GAC/potential DIET, membrane EET, environmental redox gradients, a graphical abstract, and Objective 3 experimental design.

## Remaining QA

- cross-tier **perceptual** duplicate detection is still pending; exact SHA/path deduplication is implemented;
- 106 Zotero/reference figures still require manual visual QA;
- reference records inferred from captions should be promoted to higher-confidence style/layout annotations as they are visually reviewed.

## Key quality principle

The goal is not to imitate journal branding. Scientific purpose and information structure lead retrieval; journal/source family is a secondary filter. The system should learn **which visual language works for which scientific job** while preserving evidence boundaries and provenance.
