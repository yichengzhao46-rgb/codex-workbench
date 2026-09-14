# Human-Curated Scientific Visual Learning System

> **Current curated reference layer:** the user-selected main library uses canonical IDs `M001`–`M021`; the separate bioinformatics library uses `BI001`–`BI022`. The larger historical harvest/unified corpus is retained for provenance, rights tracking, source discovery, and auditability rather than as the default aesthetic reference set.

## Objective

PR20 converts **user-approved real published figures** into reusable visual knowledge for scientific figure generation.

The system does **not** decide which figures are aesthetically worth learning from: that judgment is made manually by the user before a figure enters the curated reference set. PR20 instead learns how the approved references solve visual communication problems and transfers those solutions to new scientific figures.

The division of responsibility is:

> **You decide what PR20 learns from. We decide what the figure needs to say. PR20 decides how it should look.**

Scientific logic, evidence boundaries, mechanism structure, established versus candidate pathways, and figure content are defined first through user + ChatGPT discussion. PR20 then addresses the complementary visual problem: composition, layout, hierarchy, cell/material rendering, connector grammar, palette, typography, information density, whitespace, dimensionality, lighting, transparency, and reusable graphical elements.

For the full bilingual design specification and workflow, see [`VISUAL-LEARNING-WORKFLOW.md`](VISUAL-LEARNING-WORKFLOW.md).

## Core design principles

1. **Human-approved corpus is the source of truth.** Every figure retained by the user is a valid visual-learning reference.
2. **Learn visual grammar, not complete figures.** Decompose references into transferable components and rules rather than treating any published figure as a template to copy.
3. **Visual suitability outranks topical similarity.** Scientific relevance is a compatibility constraint; it should not dominate aesthetic reference retrieval.
4. **Multi-reference synthesis is the default.** Different references may supply composition, cell rendering, materials, arrows, palette, typography, density, or depth.
5. **2D, 2.5D, 3D, and hybrid references are all valid.** User-approved 3D references should be learned through geometry, perspective, depth, lighting, surface treatment, translucency, and spatial relationships. Those principles may be used directly or translated into restrained 2.5D when appropriate.
6. **The main intermediate output is a structured Style Recipe.** Retrieval should culminate in task-specific guidance before figure generation.
7. **The long-term goal is not one fixed house style.** PR20 should support multiple task-specific scientific visual languages under a coherent user-curated aesthetic direction.

## Canonical workflow

```text
REAL PUBLISHED FIGURES
        ↓
USER MANUAL SELECTION / APPROVAL
        ↓
APPROVED PR20 REFERENCE CORPUS
        ↓
VISUAL DECOMPOSITION
        ↓
VISUAL GRAMMAR ANNOTATION
        ↓
REUSABLE VISUAL KNOWLEDGE
        ↓

NEW SCIENTIFIC FIGURE TASK
        ↓
USER + CHATGPT DEFINE SCIENTIFIC LOGIC
        ↓
PR20 IDENTIFIES REQUIRED VISUAL ROLES
        ↓
TASK-SPECIFIC REFERENCE RETRIEVAL
        ↓
MULTI-REFERENCE VISUAL SYNTHESIS
        ↓
STRUCTURED STYLE RECIPE
        ↓
SCIENTIFIC FIGURE GENERATION
        ↓
USER REVIEW
        ↓
REFINEMENT / FEEDBACK ACCUMULATION
```

Typical visual roles include:

- overall composition / layout
- visual hierarchy
- cell rendering
- membrane / intracellular rendering
- material / mineral / electrode rendering
- molecule / metabolite representation
- arrow and connector grammar
- palette and accent strategy
- typography and label placement
- whitespace and information density
- depth / perspective / lighting
- evidence-to-mechanism integration

## Current curated reference sets

### Main scientific visual-learning library

- **21 references total**
- **14 locally mirrored assets**
- **7 restricted/reference-only external figures**
- canonical IDs: `M001`–`M021`
- next ID: `M022`
- canonical catalog: `manifests/main-reference-catalog.csv`
- curated-set note: `CURATED-REFERENCE-SET.md`

This is the authoritative aesthetic reference set for mechanisms, environmental-process overviews, microbial interaction, material/microbe interfaces, perturbation comparisons, biohybrid systems, graphical abstracts, and general scientific visual-language decisions.

### Bioinformatics figure reference library

- **22 references total**
- **15 locally mirrored assets**
- **5 restricted external references**
- **2 open-access metadata-only references**
- canonical IDs: `BI001`–`BI022`
- next ID: `BI023`
- canonical catalog: `../bioinformatics-figure-reference-library/reference-catalog.csv`

This library is reserved for phylogeny, pathway reconstruction, genome/MAG-resolved figures, transcriptomics/proteomics, gene-level expression overlays, enrichment, correlation/network analysis, and evidence-to-mechanism composition.

## Manual curation history

The current reference layer has completed direct user-led screening:

- **293 displayed figures reviewed**
- **27 original aesthetic KEEP**
- **266 DELETE**
- historical decisions: `annotations/manual_curation_final.csv`

Canonical numbering is separated from legacy provenance aliases. Old `R*`, `S*`, `Z*`, `U*`, and `B*` identifiers remain available only for traceability.

Cross-library mapping and registry:

- `../figure-reference-libraries/id-map.csv`
- `../figure-reference-libraries/registry.json`

## Historical corpus / provenance layer

The earlier harvest remains intentionally preserved. It supports provenance, rights, source discovery, reproducibility, and historical validation, but it is **not** the default aesthetic reference surface after manual curation.

Historical runtime files include:

- `manifests/library-registry.json`
- `manifests/unified-library-index.csv`
- `manifests/unified-library-summary.json`
- `scripts/unified_library.py`
- `scripts/router_reference_query.py`
- `validation/router-retrieval-test-cases.json`

The older retrieval rule of ranking scientific relevance first should be treated as **legacy behavior for the historical corpus**, not as the design principle of the curated visual-learning system.

## Retrieval policy for the curated system

Reference retrieval should answer **which approved visual solutions best serve the current figure**, not which figures share the most scientific keywords.

A normal task may deliberately retrieve complementary references such as:

```text
Reference A → overall composition
Reference B → cell rendering
Reference C → material / molecular representation
Reference D → arrow grammar
Reference E → palette
Reference F → typography / whitespace
Reference G → information-density control
```

These inputs are then synthesized into a **task-specific Style Recipe** rather than copied from one figure.

## Structured Style Recipe

A Style Recipe should normally specify:

```text
scientific task
layout / composition
visual hierarchy
cell rendering
material rendering
molecular representation
arrow / connector grammar
palette
accent strategy
typography
whitespace
information density
dimensionality
perspective / lighting when relevant
reusable motifs
elements to avoid
```

## What PR20 should not do

PR20 should not:

- automatically decide which published figures are aesthetically good;
- define the scientific mechanism or evidence boundary;
- rank references mainly by topical similarity;
- force all outputs into flat 2D;
- imitate one published figure wholesale;
- optimize primarily for corpus size.

## Physical storage and provenance

Physical locations remain provenance-preserving. Canonical renumbering does **not** rename binaries because doing so would break historical manifests, checksums, and source traceability.

```text
projects/scientific-figure-style-corpus/
├── assets/
│   ├── raw/
│   ├── stage1_5/
│   └── zotero/
├── manifests/
│   ├── main-reference-catalog.csv
│   ├── library-registry.json
│   ├── unified-library-index.csv
│   ├── unified-library-summary.json
│   ├── raw-image-manifest.csv
│   ├── zotero-private-manifest.csv
│   └── stage1_5*_harvested_figures.csv
├── CURATED-REFERENCE-SET.md
├── VISUAL-LEARNING-WORKFLOW.md
├── scripts/
└── validation/
```

Restricted external references may guide style and composition but are not mirrored into the public repository unless redistribution rights are verified. Existing provenance, rights status, SHA/path history, and source metadata remain authoritative.

## Success criteria

PR20 succeeds when it can reliably answer three questions:

1. **What visual principles should be learned from the approved corpus?**
2. **Which approved references best solve the current presentation problem, and which visual role should each reference serve?**
3. **How should those visual principles be recombined into a new, scientifically correct, original, and aesthetically mature figure?**

The quality of visual knowledge and transfer is therefore more important than the raw number of stored images.
