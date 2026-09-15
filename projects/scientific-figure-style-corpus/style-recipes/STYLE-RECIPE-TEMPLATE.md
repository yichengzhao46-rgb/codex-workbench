# Style Recipe Template

## A. Science lock

- Scientific task:
- Core claim:
- Evidence boundary:
- Established relationships:
- Candidate / unresolved relationships:
- Required objects/modules:
- Forbidden inventions / unsupported content:

## B. Reference roles

- Composition references:
- Cell rendering references:
- Material/interface references:
- Connector references:
- Palette references:
- Typography/whitespace references:
- Density/hierarchy references:
- Depth/lighting references when relevant:

Use multiple approved references by role. Do not copy one complete published figure.

## C. Visual architecture

- Layout family:
- Reading order:
- Visual hierarchy:
- Main focal object:
- Secondary modules:
- Context/background elements:
- Target density:
- Whitespace strategy:
- Dimensionality:
- Perspective / camera angle:

## D. Rendering rules

- Rendering intensity (1-5; default 2):
- Cell rendering:
- Material rendering:
- Molecular representation:
- Surface treatment:
- Outline treatment:
- Shading:
- Texture:
- Reflection:
- Glow:
- Background:

## E. Semantic visual grammar

- Palette:
- Accent strategy:
- Electron-flow style:
- Metabolite-flow style:
- Condition-comparison style:
- Confirmed-process connector:
- Candidate/unresolved connector:
- Alternative-route connector:
- Typography:
- Reusable motifs:

## F. Generation strategy

- Generation mode: asset-first / whole-figure draft / hybrid
- Assets to generate individually:
- Transparent-background assets required:
- Elements to assemble manually:
- Text to add after generation:
- Connectors to redraw after generation:
- Vector-edit requirements:

Default rule: use AI primarily to render difficult visual assets; use controlled assembly for layout, typography, arrows, evidence semantics, and final spacing.

## G. Anti-AI-look constraints

- Elements to avoid:
- Negative-style vocabulary:
- Maximum palette complexity:
- Secondary-object simplification:
- Lighting consistency rule:
- Perspective consistency rule:
- AI-specific artifact risks for this task:

Default avoid list unless a user-approved reference justifies an exception:

```text
no glossy plastic rendering
no neon cyan-purple gradient aesthetic
no glow or glowing arrows
no cinematic / volumetric lighting
no decorative floating particles
no toy-like microbial cells
no excessive rounded geometry
no hyper-detailed pseudo-biology
no advertising-render aesthetics
no unnecessary background texture
```

## H. Post-generation reconstruction

- Replace all generated text: yes / no
- Redraw arrows/connectors: yes / no
- Normalize palette: yes / no
- Normalize stroke weights: yes / no
- Normalize lighting/shading: yes / no
- Run subtraction pass: yes / no

Subtraction targets:

- meaningless particles;
- redundant highlights;
- unnecessary gradients/shadows;
- non-informative background texture;
- repeated molecules/icons;
- duplicate arrows;
- decorative effects without communication value.

## I. QA

- Scientific fidelity: pass / fail
- Visual hierarchy: pass / revise
- Readability: pass / revise
- Aesthetic quality: pass / revise
- Style consistency: pass / revise
- Editability: pass / revise
- AI Flavor Score (0-10):
- AI Flavor disposition: acceptable / polish / major revision / reconstruct

Scientific fidelity is a hard gate. If it fails, reject regardless of aesthetic quality.

See [`../ANTI-AI-LOOK-PASS.md`](../ANTI-AI-LOOK-PASS.md) and [`../validation/anti-ai-look-checklist.json`](../validation/anti-ai-look-checklist.json).

## J. Final generation brief

- Final generation brief:
- Final assembly instructions:
- Final human-review focus:
