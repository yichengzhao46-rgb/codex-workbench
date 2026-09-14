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
- structured grammar matrix: `../annotations/main-reference-visual-grammar.csv`
- Phase-2 worklist: `manifests/main-library-decomposition-worklist.csv`
- reusable element inventory: `manifests/style-element-inventory.csv`
- decomposition schema: `schema/visual-decomposition-schema.md`
- controlled vocabularies: `schema/controlled-vocabularies.json`
- per-reference notes: `notes/M###.md`
- status: `reports/phase2-status.json`

## Current execution state

Batch 1 is complete for the seven high-value recent references `M015`–`M021`. These cover environmental multiscale mechanism, mirrored perturbation, rhizosphere zoom, soft-2.5D condition comparison, membrane EET cutaway, synthesis-to-function graphical abstract, and methanotroph biohybrid storytelling.

`M001`–`M014` remain queued. They should be decomposed only after direct visual inspection; PR20 must not infer detailed aesthetics from captions or topical metadata alone.

## Completion gate

Phase 2 is complete only when:

1. all 21 references have a completed decomposition;
2. every completed note has a corresponding structured row in `main-reference-visual-grammar.csv`;
3. reusable elements have been consolidated into the element inventory;
4. recurring visual grammars have been summarized without collapsing the corpus into a single house style;
5. the resulting knowledge can support task-specific multi-reference Style Recipes.

## Core rule

> Learn visual components and rules; do not copy complete published figures.
