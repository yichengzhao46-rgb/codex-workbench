# 2D/2.5D Scientific Figure Style Corpus

## Objective

Build a source-backed visual corpus for the experimental `scientific-figure-style-router` defined in `codex-playbook` PR #23.

The project follows a strict **raw images first** architecture:

> **real source images → figure-level annotation → reusable element extraction → Style Router validation**

The corpus now has two explicitly separated pools:

1. **Public active A/B pool** — 96 validated style-learning records in `assets/stage1_5/`.
2. **Zotero reference pool** — 139 Codex-imported records from 104 articles in `assets/zotero/`, indexed by `manifests/zotero-private-manifest.csv` and registered through `manifests/library-registry.json`.

The Zotero pool is available for reference and retrieval, but it is not counted toward the public active A/B total unless a figure receives figure-level rights verification and completed visual QA.

## Stage 0 — raw corpus gate

The public mirrored corpus requires legally mirrorable, provenance-checked, visually inspected source images.

See `RAW_CORPUS_POLICY.md` for the acceptance gate, diversity requirements, rights rules, and anti-bias constraints.

A record counts toward the public mirrored set only when the actual image file is stored in an allowed asset location and has verified source metadata, redistribution rights, checksum, and completed visual inspection. Metadata-only or reference-only records do not count toward that public threshold.

## Rights-aware mirror design

`codex-workbench` is public. Full publisher/source images should therefore be treated as public mirrored assets only when their license or explicit permission allows redistribution. Open-access status alone is not enough: the exact Creative Commons/public-use license and any third-party exclusions must be checked.

The Codex-imported Zotero images are registered as a separate reference pool. Their manifest records retain `redistribution_allowed=false`; they must not be promoted into the public active A/B pool without a rights audit.

## Stage 1 — figure-level annotation

Annotate figures using the playbook schema:

- scientific purpose;
- information type and density;
- 2D / light-2.5D style family;
- layout/composition;
- cell/material/molecule rendering;
- arrow/connector grammar;
- palette and outline strategy;
- evidence-state coding;
- reusable principles;
- limitations and unsuitable transfer cases.

An experimental QC block remains useful:

```yaml
annotation_qc:
  inspection_level: direct_image | direct_figure_page | caption_plus_page | metadata_only
  annotation_confidence: high | medium | low
  direct_pixel_qa: complete | pending
  notes: ""
```

## Stage 2 — element library

Element extraction should use the validated active set first. Reference-only Zotero figures may inform retrieval and comparison, but should not silently bypass rights or QA gates.

## Stage 3 — Style Router

The target workflow is:

`task → figure purpose → information structure → layout → style family → evidence grammar → reusable elements → final image`

For Bath/RP/MOB/EET/material-interface tasks, retrieval should consult both the active pool and the Zotero reference manifest, while preserving their different QA and rights status.

## Current files

```text
projects/scientific-figure-style-corpus/
├── README.md
├── RAW_CORPUS_POLICY.md
├── ANNOTATION_QA.md
├── ZOTERO_INGEST.md
├── corpus-index.csv
├── manifests/
│   ├── raw-image-manifest.csv
│   ├── zotero-private-manifest.csv
│   └── library-registry.json
├── assets/
│   ├── stage1_5/                  # 96 active A/B records
│   └── zotero/                    # 139 reference records
├── corpus/
├── derived-elements/
└── validation/
```

## Current status

- public active A/B set: **96**;
- Codex/Zotero reference records: **139** from **104** articles;
- Zotero visual QA: **33 complete**, **106 pending**;
- total registered records across both pools: **235** before cross-pool perceptual deduplication;
- Zotero reference records counted toward public active A/B: **no**;
- PR remains a workbench validation project rather than a final immutable training standard.

## Key quality principle

The goal is not to imitate journal branding. The corpus should be large and heterogeneous enough to learn **which visual language works for which scientific job**. Journal/source family is a retrieval filter after purpose and information structure, not the primary style label.
