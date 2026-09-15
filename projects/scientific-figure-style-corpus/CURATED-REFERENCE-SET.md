# Curated Main Scientific Visual-Learning Reference Set

This is the current **user-curated main scientific visual-learning library**. It is distinct from the larger historical harvest/unified corpus retained in this project for provenance, rights tracking, source discovery, and auditability.

## Core rule

Every figure retained in this curated set has already passed **user manual visual approval** and is therefore considered worth learning from.

PR20 should not run a second automatic aesthetic gate over these references. Its job is to analyze what each approved figure does well, decompose that into reusable visual grammar, and retrieve the most useful visual roles for new scientific-figure tasks.

Scientific topic similarity is a compatibility constraint, not the primary aesthetic ranking principle.

## Canonical numbering

- Canonical IDs: `M001`–`M021`.
- Next available ID: `M022`.
- `R*`, `S*`, `Z*`, and `U*` identifiers are legacy provenance aliases only.
- Canonical catalog: `manifests/main-reference-catalog.csv`.
- Cross-library migration map: `../figure-reference-libraries/id-map.csv`.

## Current composition

- **21 references total**.
- **14 locally mirrored assets** selected from the earlier corpus.
- **7 restricted/reference-only external figures** added manually after screening.

The current set is intentionally small and curated. Corpus quality and transferable visual knowledge matter more than raw image count.

## What should be learned from each reference

Approved references should be decomposed across reusable visual dimensions such as:

- composition and layout;
- visual hierarchy;
- cell and membrane rendering;
- material / mineral / electrode / particle rendering;
- metabolite, molecule, gas and electron representation;
- arrow / connector grammar;
- palette and accent strategy;
- typography and label placement;
- whitespace and information density;
- panel organization;
- depth, perspective, lighting and transparency when relevant;
- evidence-to-mechanism integration;
- reusable graphical motifs.

A reference does not need to be copied as a whole. Different parts of different approved references may be combined in a new Style Recipe.

## Dimensionality policy

The curated visual-learning system is **not restricted to 2D**.

User-approved references may be:

- 2D;
- restrained 2.5D;
- full 3D;
- hybrid 2D–3D.

For 3D references, PR20 should learn geometry, perspective, camera angle, depth hierarchy, lighting, shadow, surface/material treatment, translucency, and spatial relationships. These principles may be used directly in a 3D/hybrid task or translated into restrained 2.5D when that better serves scientific clarity.

## Intended use

Use this library for visual decisions in:

- mechanism schematics;
- microbial interaction and cross-feeding;
- environmental-process overviews;
- material/microbe interfaces;
- perturbation comparisons;
- biohybrid systems;
- EET / EEU / DIET concepts;
- graphical abstracts;
- general scientific visual-language decisions.

For each task, the preferred workflow is:

```text
scientific logic defined by user + ChatGPT
        ↓
identify required visual roles
        ↓
retrieve complementary M### references
        ↓
multi-reference synthesis
        ↓
structured Style Recipe
        ↓
figure generation
```

Physical assets are not renamed during canonical renumbering. This preserves historical manifests, checksums, source provenance, and auditability while allowing future discussion and retrieval to use stable `M###` identifiers.

See `VISUAL-LEARNING-WORKFLOW.md` for the full bilingual PR20 design specification.
