# Annotation QA

## Purpose

Prevent prestige bias, unsupported visual inference, and accidental copyright drift while building the scientific figure style corpus.

## Admission checks

For every `active` record:

1. Article identity, journal, year, DOI/URL, and figure/panel locator are verified.
2. The actual figure or panel has been directly inspected on a publisher/full-text page.
3. Palette, layout, connector grammar, and element descriptions are based on visible content rather than title/abstract inference.
4. At least one weakness or `not_suitable_for` note is recorded.
5. Evidence semantics are separated from visual style.
6. No image asset is stored unless reuse rights are independently verified.

For every `candidate` record:

1. Article identity and graphical/visual abstract or figure locator are verified.
2. Any uninspected visual fields are explicitly marked `pending`.
3. The record may contribute scientific-purpose and source-discovery metadata, but not pixel-level style transfer.
4. Promotion to `active` requires direct visual QA.

## Evidence-boundary checks

- A solid arrow in the corpus does not automatically mean "experimentally proven" in a new figure.
- A visual abstract may summarize an author's interpretation more strongly than the underlying data; annotations must preserve the paper's evidence limits.
- DIET, EEU, and mineral-mediated transfer must not be generalized across systems without system-specific evidence.
- Community-level measurements must not be converted into species-specific pathway arrows.
- In Bath–RP figures, H2, formate, acetate, and riboflavin remain candidate transferable resources unless separately resolved.
- High-O2 perturbation is a mechanistic comparison, not the primary novelty claim.

## Copyright / provenance checks

- Publisher artwork is not copied into this repository in v0.1.
- `doi_or_url` is the canonical pointer to the original.
- `rights_or_license` records known rights state or says that reuse rights were not independently verified.
- Reusable notes must describe abstractions: layout hierarchy, information density, connector logic, focal-element placement, contrast, and evidence coding.
- Do not write reconstruction instructions that would reproduce one specific published figure nearly identically.

## Promotion checklist

A `candidate` becomes `active` only after:

- direct figure/asset view;
- palette checked;
- outline/shading checked;
- exact layout checked;
- connector semantics checked;
- text density checked;
- evidence coding checked against caption/main text;
- `why_it_works`, `main_weakness`, and transferability fields re-reviewed.

## Current v0.1 state

- ISME: 5/5 directly inspected → active.
- Nature Communications: 5/5 directly inspected → active.
- Water Research: 0/5 direct pixel QA → candidate.
- Environmental Science & Technology: 0/5 direct pixel QA → candidate.

This asymmetry is intentional. It is better to preserve uncertainty than to manufacture complete-looking annotations from metadata-only access.