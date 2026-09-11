# 2D/2.5D Scientific Figure Style Corpus — v0.1

## Objective

Build the first real reference corpus for the experimental `scientific-figure-style-router` defined in `codex-playbook` PR #23.

This project does **not** mirror publisher figures. It stores source metadata, figure/panel locators, structured design annotations, reusable principles, inspection confidence, and copyright/provenance notes so the router can learn from real published figures without turning the repository into an image archive.

## v0.1 scope

Initial target: **20 real samples**, five from each of four primary source journals:

- The ISME Journal
- Nature Communications
- Water Research
- Environmental Science & Technology

The batch is intentionally heterogeneous. It includes:

- microbial cross-feeding and two-organism interaction;
- MIET vs DIET comparison;
- cell–material and electrode interfaces;
- biohybrid / semiconductor interfaces;
- environmental redox gradients;
- methane oxidation and methane-driven environmental processes;
- conductive-material-facilitated interspecies transfer;
- experimental-design schematics;
- graphical / visual abstracts.

## Relationship to playbook

Canonical schema source:

`codex-playbook/skills/scientific-figure-style-router/references/sample-schema.md`

Current workbench branch intentionally allows one experimental extension block:

```yaml
annotation_qc:
  inspection_level: direct_figure_page | caption_plus_page | graphical_abstract_metadata
  annotation_confidence: high | medium | low
  direct_pixel_qa: complete | pending
  notes: ""
```

This block exists so publisher-access limitations are explicit rather than silently converted into invented visual details. If useful after validation, the block can later be proposed back to the playbook schema.

## Corpus status logic

### `active`

Use only when the figure/panel itself is exposed on the publisher/full-text page with enough visual/caption context to support the functional and design annotation.

### `candidate`

Use when the article and figure/graphical-abstract locator are verified but pixel-level visual inspection is incomplete. Candidate records may still be used for source discovery, but should not drive fine palette, texture, or typography transfer until promoted.

### `rejected`

Use when a real figure is scientifically relevant but visually redundant, too data-heavy for the router task, or unsuitable for transferable design learning.

## Copyright / provenance policy

- No publisher image asset is stored in this repository in v0.1.
- Every record points back to the article DOI or publisher page.
- `rights_or_license` states either the known open-access state or that reuse rights were not independently verified.
- Design principles must be abstractions across samples, not tracing instructions for a single published figure.
- If a local image is ever stored in a later iteration, its license and provenance must be explicit.

## Files

```text
projects/scientific-figure-style-corpus/
├── README.md
├── ANNOTATION_QA.md
├── corpus-index.csv
├── corpus/
│   ├── isme.yaml
│   ├── nature-communications.yaml
│   ├── water-research.yaml
│   └── est.yaml
└── validation/
    └── router-validation.md
```

## v0.1 success criteria

The batch is successful if it can support at least these retrieval routes without defaulting to journal-name imitation:

1. `microbial_interaction + two_organism_interaction + flat_2d_mechanism`
2. `electron_transfer + mirrored_comparison`
3. `material_microbe_interface + zoom_in_multiscale + soft_2_5d_schematic`
4. `environmental_process + layered_gradient`
5. `experimental_design + linear_flow`
6. `graphical_abstract + editorial_2d_overview`

It must also expose where the current router lacks enough samples, especially high-O2 vs low-O2 perturbation figures and restrained 2.5D mineral–microbe interface figures.