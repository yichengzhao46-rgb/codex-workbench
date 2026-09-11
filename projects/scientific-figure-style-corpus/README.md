# 2D/2.5D Scientific Figure Style Corpus

## Objective

Build a source-backed visual corpus for the experimental `scientific-figure-style-router` defined in `codex-playbook` PR #23.

The project now follows a strict **raw images first** architecture:

> **≥100 real source images → figure-level annotation → reusable element extraction → Style Router validation**

The original 20-record batch remains a useful schema/source-discovery pilot, but it is no longer treated as a sufficient foundation corpus.

## Stage 0 — 100-image raw corpus gate

Before expanding the element library, collect at least **100 legally mirrorable, provenance-checked, visually inspected source images**.

Initial target allocation:

- The ISME Journal: 30
- Nature Communications: 30
- Environmental Science & Technology: 20
- Water Research: 20

See `RAW_CORPUS_POLICY.md` for the full acceptance gate, diversity requirements, rights rules, and anti-bias constraints.

A record counts toward 100 only when the actual image file is stored in an allowed asset location and has verified source metadata, redistribution rights, checksum, and completed visual inspection. Metadata-only references do not count.

## Rights-aware mirror design

`codex-workbench` is public. Full publisher/source images may therefore be committed only when their license or explicit permission allows redistribution. Open-access status alone is not enough: the exact Creative Commons/public-use license and any third-party exclusions must be checked.

For non-mirrorable figures, store an index-only source record with DOI, figure locator, source URL, rights note, and derived visual observations; do not commit the original image.

This design preserves the user's requirement for a genuine original-image learning corpus without turning the repository into an unauthorized publisher mirror.

## Stage 1 — figure-level annotation

After raw acquisition, annotate each figure using the playbook schema:

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

Element extraction is **blocked until Stage 0 passes**. See:

`derived-elements/BLOCKED_UNTIL_RAW_CORPUS_100.md`

Only after the raw corpus reaches the gate should recurring cells, materials, arrows, molecules, gradients, zoom boxes, typography, and composition archetypes be promoted into a reusable element library.

## Stage 3 — Style Router

The Style Router remains experimental until it is validated against the ≥100-image corpus. The target workflow is:

`task → figure purpose → information structure → layout → style family → evidence grammar → reusable elements → final image`

## Current files

```text
projects/scientific-figure-style-corpus/
├── README.md
├── RAW_CORPUS_POLICY.md
├── ANNOTATION_QA.md
├── corpus-index.csv
├── manifests/
│   └── raw-image-manifest.csv       # 100 acquisition slots
├── corpus/
│   ├── isme.yaml
│   ├── nature-communications.yaml
│   ├── water-research.yaml
│   └── est.yaml
├── derived-elements/
│   └── BLOCKED_UNTIL_RAW_CORPUS_100.md
└── validation/
    └── router-validation.md
```

## Current status

- existing pilot: 20 source/annotation records;
- raw-image acquisition target: 100;
- element extraction: blocked;
- Style Router: experimental;
- publisher image mirroring: allowed only for assets with verified redistribution rights.

## Key quality principle

The goal is not to imitate journal branding. The corpus should be large and heterogeneous enough to learn **which visual language works for which scientific job**. Journal/source family is a retrieval filter after purpose and information structure, not the primary style label.
