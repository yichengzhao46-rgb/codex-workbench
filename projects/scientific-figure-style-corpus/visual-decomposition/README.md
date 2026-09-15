# Phase 2 — Main-Library Visual Decomposition

PR20 has completed user-led aesthetic screening and has formally entered the **visual decomposition / visual grammar learning** phase for the 21-reference main library (`M001`–`M021`).

## Objective

Convert each approved published figure into reusable visual knowledge rather than treating any figure as a template to imitate.

The decomposition asks how each reference solves specific visual problems:

- overall composition and reading order;
- visual hierarchy;
- cell, membrane, material and molecular rendering;
- arrow / connector grammar;
- palette, typography and whitespace;
- information density;
- dimensionality, perspective, lighting and transparency;
- evidence-to-mechanism integration;
- reusable motifs and failure modes.

## Authoritative files

- canonical main-library catalog: `../manifests/main-reference-catalog.csv`
- Batch-1 structured grammar in the main matrix: `../annotations/main-reference-visual-grammar.csv`
- Batch-2 structured grammar fragment: `manifests/batch2-visual-grammar.csv`
- Phase-2 worklist: `manifests/main-library-decomposition-worklist.csv`
- reusable element inventory: `manifests/style-element-inventory.csv`
- decomposition schema: `schema/visual-decomposition-schema.md`
- controlled vocabularies: `schema/controlled-vocabularies.json`
- per-reference notes: `notes/M###.md`
- status: `reports/phase2-status.json`

## Current execution state

**15 / 21 references are now complete.**

Batch 1 completed `M015`–`M021`, covering environmental multiscale mechanism, mirrored perturbation, rhizosphere zoom, soft-2.5D condition comparison, membrane EET cutaway, synthesis-to-function graphical abstract, and methanotroph biohybrid storytelling.

Batch 2 completed `M003`, `M004`, `M005`, `M006`, `M011`, `M012`, `M013`, and `M014`. This batch adds mechanism-plus-evidence composition, central material–microbe hero objects, conductive-carrier/redox-ladder logic, data-to-mechanism stacking, environmental-stress storytelling, omics-to-mechanism layout, alternative-mechanism comparison, and membrane-to-carbon methanotroph metabolism.

The remaining queued references are `M001`, `M002`, and `M007`–`M010`. They should be decomposed only after direct visual inspection; PR20 must not infer detailed aesthetics from captions or topical metadata alone.

Batch-2 structured rows are stored as a fragment and will be consolidated with Batch 3 into `main-reference-visual-grammar.csv` at Phase-2 closeout, so the final matrix has one clean authoritative row per `M###` reference.

## Completion gate

Phase 2 is complete only when:

1. all 21 references have a completed decomposition;
2. every completed note has a corresponding structured grammar row;
3. Batch-2/Batch-3 grammar rows have been consolidated into `main-reference-visual-grammar.csv`;
4. reusable elements have been consolidated into the element inventory;
5. recurring visual grammars have been summarized without collapsing the corpus into a single house style;
6. the resulting knowledge can support task-specific multi-reference Style Recipes.

## Core rule

> Learn visual components and rules; do not copy complete published figures.
