# Human-Curated Scientific Visual Learning System

> **Current curated reference layer:** the user-selected PR20 main library uses canonical IDs `M001`–`M022`. The separate bioinformatics result-visualization library is owned by PR21 and should not contaminate PR20 mechanism/conceptual retrieval. The larger historical harvest/unified corpus is retained for provenance, rights tracking, source discovery, and auditability rather than as the default aesthetic reference set.

## Objective

PR20 converts **user-approved real published figures and user-approved visual references** into reusable visual knowledge for scientific figure generation.

The system does **not** decide which figures are aesthetically worth learning from: that judgment is made manually by the user before a figure enters the curated reference set. PR20 instead learns how the approved references solve visual communication problems and transfers those solutions to new scientific figures.

The division of responsibility is:

> **You decide what PR20 learns from. We decide what the figure needs to say. PR20 decides how it should look.**

Scientific logic, evidence boundaries, mechanism structure, established versus candidate pathways, and figure content are defined first through user + ChatGPT discussion. PR20 then addresses the complementary visual problem: composition, layout, hierarchy, cell/material rendering, connector grammar, palette, typography, information density, whitespace, dimensionality, lighting, transparency, and reusable graphical elements.

PR20 now also controls the transition from an AI-generated draft to a publication-facing scientific illustration through a dedicated [`ANTI-AI-LOOK-PASS.md`](ANTI-AI-LOOK-PASS.md).

For the full bilingual visual-learning specification, see [`VISUAL-LEARNING-WORKFLOW.md`](VISUAL-LEARNING-WORKFLOW.md).

## Core design principles

1. **Human-approved corpus is the source of truth.** Every figure retained by the user is a valid visual-learning reference.
2. **Learn visual grammar, not complete figures.** Decompose references into transferable components and rules rather than treating any published figure as a template to copy.
3. **Visual suitability outranks topical similarity.** Scientific relevance is a compatibility constraint; it should not dominate aesthetic reference retrieval.
4. **Multi-reference synthesis is the default.** Different references may supply composition, cell rendering, materials, arrows, palette, typography, density, or depth.
5. **2D, 2.5D, 3D, and hybrid references are all valid.** User-approved 3D references should be learned through geometry, perspective, depth, lighting, surface treatment, translucency, and spatial relationships. Those principles may be used directly or translated into restrained 2.5D when appropriate.
6. **The main intermediate output is a structured Style Recipe.** Retrieval should culminate in task-specific generation guidance before rendering.
7. **AI is a rendering assistant, not the scientific figure designer.** Scientific logic, evidence semantics, final typography, connector meaning, spacing, and publication-facing hierarchy remain controlled.
8. **Asset-first generation is preferred.** Generate difficult visual elements individually when practical; assemble the figure under explicit layout and semantic rules.
9. **Anti-AI cleanup is mandatory for publication-facing output.** Rendering intensity, AI-flavor anti-patterns, subtraction, typography replacement, connector reconstruction, and final QA are part of the default workflow.
10. **The long-term goal is not one fixed house style.** PR20 should support multiple task-specific scientific visual languages under a coherent user-curated aesthetic direction.

## Canonical workflow

```text
REAL PUBLISHED FIGURES / USER-APPROVED VISUAL REFERENCES
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
SCIENCE LOCK
        ↓
PR20 IDENTIFIES REQUIRED VISUAL ROLES
        ↓
TASK-SPECIFIC REFERENCE RETRIEVAL
        ↓
MULTI-REFERENCE VISUAL SYNTHESIS
        ↓
STRUCTURED STYLE RECIPE
        ↓
ASSET-FIRST / CONTROLLED FIGURE GENERATION
        ↓
MANUAL / VECTOR ASSEMBLY WHERE APPROPRIATE
        ↓
ANTI-AI-LOOK PASS
        ↓
SCIENTIFIC + VISUAL + AI-FLAVOR QA
        ↓
USER REVIEW
        ↓
REFINEMENT / FEEDBACK ACCUMULATION
```

Typical visual roles include:

- overall composition / layout;
- visual hierarchy;
- cell rendering;
- membrane / intracellular rendering;
- material / mineral / electrode rendering;
- molecule / metabolite representation;
- arrow and connector grammar;
- palette and accent strategy;
- typography and label placement;
- whitespace and information density;
- depth / perspective / lighting;
- evidence-to-mechanism integration.

## Current curated reference set

### Main scientific visual-learning library

- **22 references total**;
- **14 locally mirrored assets**;
- **8 restricted/reference-only external figures**;
- canonical IDs: `M001`–`M022`;
- next ID: `M023`;
- canonical catalog: `manifests/main-reference-catalog.csv`;
- curated-set note: `CURATED-REFERENCE-SET.md`.

This is the authoritative aesthetic reference set for mechanisms, environmental-process overviews, microbial interaction, material/microbe interfaces, perturbation comparisons, biohybrid systems, graphical abstracts, and other mechanism-oriented visual-language decisions.

### PR21 boundary

Pure bioinformatics result visualization is intentionally separated from PR20.

PR20 does **not** own:

- PCA;
- volcano plots;
- enrichment / GSEA plots;
- transcriptomic heatmaps;
- species-resolved RNA-seq result presentation;
- other pure bioinformatics-result visualization.

Those belong to PR21. PR20 may still learn general composition principles from a user-approved reference when the role is genuinely mechanism/conceptual rather than result-plot imitation.

## Manual curation history

The reference layer has completed direct user-led screening. Historical curation decisions remain available in `annotations/manual_curation_final.csv` and provenance manifests.

Canonical numbering is separated from legacy provenance aliases. Old `R*`, `S*`, `Z*`, `U*`, and `B*` identifiers remain available only for traceability.

## Historical corpus / provenance layer

The earlier harvest remains intentionally preserved. It supports provenance, rights, source discovery, reproducibility, and historical validation, but it is **not** the default aesthetic reference surface after manual curation.

Historical runtime files include:

- `manifests/library-registry.json`;
- `manifests/unified-library-index.csv`;
- `manifests/unified-library-summary.json`;
- `scripts/unified_library.py`;
- `scripts/router_reference_query.py`;
- `validation/router-retrieval-test-cases.json`.

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

These inputs are synthesized into a **task-specific Style Recipe** rather than copied from one figure.

## Structured Style Recipe

The canonical template is [`style-recipes/STYLE-RECIPE-TEMPLATE.md`](style-recipes/STYLE-RECIPE-TEMPLATE.md).

A publication-facing Style Recipe should define:

```text
science lock and evidence boundary
reference roles
layout / composition
visual hierarchy
cell / material / molecular rendering
arrow / connector grammar
palette and accent strategy
typography and whitespace
information density
dimensionality and depth
rendering intensity
generation mode
asset-level generation plan
manual assembly requirements
negative-style vocabulary
post-generation reconstruction
subtraction pass
AI Flavor Score
scientific + visual QA
```

The recipe is not just a natural-language image prompt. It is the control layer between the visual reference library and generation.

## Anti-AI-Look production policy

The default publication-facing goal is **not** to make an AI render look more elaborate. It is to remove generic AI visual signatures and recover intentional scientific design.

Core defaults:

- rendering intensity around `2/5` for mechanism/conceptual figures;
- restrained 2D–2.5D unless a task-specific approved reference justifies otherwise;
- matte surfaces;
- low texture;
- low gradient use;
- minimal shadow;
- no glow by default;
- small semantic palette;
- white or near-white background;
- controlled visual hierarchy;
- publication text added after image generation;
- arrows/connectors redrawn or checked after generation;
- explicit subtraction pass;
- final AI-flavor QA.

Default anti-patterns include glossy plastic rendering, neon cyan-purple gradients, glowing arrows, cinematic/volumetric lighting, decorative floating particles, toy-like microbial cells, pseudo-biological detail, excessive rounded geometry, generic futuristic infographic aesthetics, and unnecessary background texture.

See [`ANTI-AI-LOOK-PASS.md`](ANTI-AI-LOOK-PASS.md) for the full policy and [`validation/anti-ai-look-checklist.json`](validation/anti-ai-look-checklist.json) for the machine-readable QA checklist.

## AI Flavor Score

PR20 uses a simple `0–10` warning score based on materially present AI-style anti-patterns.

```text
0–2  acceptable
3–4  polish required
5–6  major revision
7–10 regenerate or reconstruct
```

This score does not replace scientific QA. **Scientific fidelity is always a hard gate.**

## What PR20 should not do

PR20 should not:

- automatically decide which published figures are aesthetically good;
- define the scientific mechanism or evidence boundary;
- rank references mainly by topical similarity;
- force all outputs into flat 2D;
- imitate one published figure wholesale;
- optimize primarily for corpus size;
- let the image model invent scientific content;
- accept generated text as publication typography;
- accept generated arrows merely because they look plausible;
- add random imperfections or noise to simulate a human-made appearance.

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
├── style-recipes/
│   └── STYLE-RECIPE-TEMPLATE.md
├── validation/
│   └── anti-ai-look-checklist.json
├── ANTI-AI-LOOK-PASS.md
├── CURATED-REFERENCE-SET.md
├── VISUAL-LEARNING-WORKFLOW.md
├── scripts/
└── validation/
```

Restricted external references may guide style and composition but are not mirrored into the public repository unless redistribution rights are verified. Existing provenance, rights status, SHA/path history, and source metadata remain authoritative.

## Success criteria

PR20 succeeds when it can reliably answer four questions:

1. **What visual principles should be learned from the approved corpus?**
2. **Which approved references best solve the current presentation problem, and which visual role should each reference serve?**
3. **How should those visual principles be recombined into a new, scientifically correct, original, and aesthetically mature figure?**
4. **How should AI-generated assets be constrained and reconstructed so the final illustration looks intentionally designed rather than generically AI-generated?**

The quality of visual knowledge, transfer, and publication-facing control is more important than the raw number of stored images.
