# Unified 2D/2.5D Scientific Figure Library

## Objective

Build one source-backed scientific figure library for the experimental `scientific-figure-style-router` defined in `codex-playbook` PR #23.

The project follows a strict **raw images first** architecture:

> **real source images → figure-level annotation → reusable element extraction → Style Router validation**

## One unified library

The corpus is now exposed as a single **Unified Scientific Figure Library** rather than two separate libraries.

Current registered content:

- **235 records total** before cross-tier perceptual deduplication;
- **96 active records** — validated A/B style-learning assets from Stage 1.5;
- **139 reference records** — Codex/Zotero-derived figures from 104 articles;
- Zotero visual QA: **33 complete**, **106 pending**.

The distinction between `active` and `reference` is now a **tier inside one library**, not a separate database boundary.

The single registry is:

`manifests/library-registry.json`

The unified row-level loader/index builder is:

`scripts/unified_library.py`

It normalizes all Stage 1.5 harvested manifests plus `zotero-private-manifest.csv` into:

- `manifests/unified-library-index.csv`
- `manifests/unified-library-summary.json`

The builder preserves provenance, exact-hash duplicate aliases, QA state, rights status, active eligibility and retrieval eligibility.

## Retrieval policy

All figure-discovery and style-learning queries should use the **unified library** by default.

Retrieval behavior:

1. search both tiers;
2. rank relevance first;
3. prefer `active` records when relevance is otherwise comparable;
4. use `reference` records for visual/mechanistic inspiration and comparison;
5. restrict public reuse to records whose rights status permits it;
6. do not promote a reference record to active until figure-level rights verification and visual QA are complete.

For Bath/RP/MOB/EET/DIET/material-interface/environmental-gradient tasks, both tiers are searchable through the same interface.

Example:

```bash
python projects/scientific-figure-style-corpus/scripts/unified_library.py \
  --query "methane EET material microbe interface" \
  --limit 20
```

Use `--active-only` when a task specifically requires only validated active records.

## Physical storage vs logical library

The logical library is unified, while physical assets remain in provenance-preserving locations:

```text
projects/scientific-figure-style-corpus/
├── assets/
│   ├── stage1_5/                  # active tier, 96
│   └── zotero/                    # reference tier, 139
├── manifests/
│   ├── library-registry.json      # single master registry
│   ├── unified-library-index.csv  # generated unified row-level index
│   ├── unified-library-summary.json
│   ├── zotero-private-manifest.csv
│   └── stage1_5*_harvested_figures.csv
├── scripts/
│   └── unified_library.py
├── corpus/
├── derived-elements/
└── validation/
```

Physical separation is retained only to preserve provenance, auditability and rights controls. It no longer represents two independent libraries.

## Stage 0 / rights boundary

See `RAW_CORPUS_POLICY.md` for provenance, diversity, rights and anti-bias requirements.

A record is `active` only when its source metadata, stored asset, checksum, redistribution status and visual QA satisfy the project gate. Reference-tier records remain searchable even when they are not active-eligible.

`codex-workbench` is public. Therefore public reuse and redistribution remain governed by the rights field on each record. A reference record does not become redistribution-safe merely because it is searchable in the unified library.

## Figure-level annotation

The unified index carries or links the following design dimensions where available:

- scientific purpose;
- information type and density;
- 2D / light-2.5D style family;
- layout/composition;
- cell/material/molecule rendering;
- arrow/connector grammar;
- palette and outline strategy;
- evidence-state coding;
- reusable principles;
- limitations and unsuitable transfer cases;
- topics and domain relevance;
- QA state;
- rights and active eligibility.

## Exact vs perceptual deduplication

`unified_library.py` performs exact deduplication using SHA-256 and asset path while retaining alias/provenance rows.

Cross-tier **perceptual** duplicate detection remains a separate corpus-level QA task because Zotero figures can be re-rendered/cropped versions of the same published figure and therefore may have different byte hashes.

## Current status

- unified registered records: **235**;
- active tier: **96**;
- reference tier: **139** from **104** articles;
- reference visual QA: **33 complete**, **106 pending**;
- exact deduplication: supported by unified builder;
- cross-tier perceptual deduplication: **pending**;
- Style Router: continues to treat active eligibility and rights as explicit fields, not as separate-library boundaries.

## Key quality principle

The goal is not to imitate journal branding. The unified library should be large and heterogeneous enough to learn **which visual language works for which scientific job**. Scientific purpose and information structure lead retrieval; journal/source family is a secondary filter.
