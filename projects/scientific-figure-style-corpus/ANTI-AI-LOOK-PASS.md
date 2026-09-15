# PR20 Anti-AI-Look Pass

## Purpose

PR20 should use generative image models as **rendering assistants**, not as autonomous scientific figure designers.

The goal of the Anti-AI-Look Pass is to remove the visual signatures that make a scientific illustration look like a generic AI-generated infographic while preserving scientific clarity, originality, and the visual strengths learned from the human-curated published-figure library.

This pass happens **after the scientific logic and Style Recipe are locked** and before final human approval.

> **Core rule:** reduce AI creative freedom as the figure moves from concept to publication-ready output.

---

## 1. Science lock before rendering

Before any image generation, freeze the following:

- scientific claim;
- required objects and modules;
- established / candidate / unresolved relationships;
- arrow semantics;
- reading order;
- visual hierarchy;
- evidence boundaries;
- species / material morphology constraints.

The image model must not invent mechanisms, pathways, structures, labels, or decorative scientific-looking content.

Visual certainty must not exceed evidence certainty.

---

## 2. Asset-first generation is the default

Prefer generating **individual visual assets** and assembling the final scientific figure outside the image model.

Typical AI-generated assets:

- microbial cells;
- minerals / particles;
- GAC / electrodes / membranes;
- environmental objects;
- individual molecular or material motifs when scientifically safe.

Typical elements that should be added or redrawn after generation:

- all publication text;
- chemical formula labels;
- gene / pathway labels;
- panel letters;
- legends;
- quantitative annotations;
- arrows and connector lines;
- evidence-status encoding;
- alignment and spacing.

Transparent-background single-element generation is preferred whenever practical.

Whole-figure generation may be used for composition exploration or early drafts, but it is not the default final-production route.

---

## 3. Rendering-intensity control

Each Style Recipe should declare a `rendering_intensity` from 1 to 5.

Default for mechanism / conceptual figures:

```text
rendering_intensity = 2 / 5
```

Recommended baseline:

```text
dimensionality: restrained 2D–2.5D
texture: low
gradient: low
shadow: very low
reflection: none
glow: none
surface: matte
outline: subtle and consistent
detail: medium-low
background: white or near-white
```

Higher rendering intensity requires a user-approved reference that justifies it.

---

## 4. AI-flavor anti-patterns

The following are warning signs unless directly justified by the Style Recipe:

1. glossy plastic surfaces;
2. excessive gradients;
3. neon cyan / purple palettes;
4. glowing arrows or glowing objects;
5. cinematic or volumetric lighting;
6. decorative floating particles;
7. toy-like or gummy microbial cells;
8. excessive rounded geometry;
9. fake molecular / membrane / cellular detail;
10. inconsistent lighting or perspective;
11. strong drop shadows on every object;
12. over-rendered secondary objects;
13. every object presented as a hero object;
14. decorative depth that does not encode information;
15. dense background texture without scientific function;
16. pseudo-scientific labels or unreadable generated text;
17. malformed arrows / connectors;
18. repeated AI-like texture patterns;
19. unnecessary visual effects that compete with information;
20. color proliferation without semantic purpose.

Default negative-style vocabulary:

```text
avoid glossy 3D
avoid neon cyan-purple gradients
avoid glow
avoid cinematic lighting
avoid volumetric lighting
avoid dramatic shadows
avoid decorative floating particles
avoid toy-like cells
avoid excessive rounded geometry
avoid hyper-detailed pseudo-biology
avoid advertising-render aesthetics
avoid futuristic infographic aesthetics
```

These are defaults, not absolute bans. A user-approved reference may override them for a specific visual role.

---

## 5. Intentional consistency over artificial irregularity

Do **not** attempt to remove AI appearance by adding random noise, fake hand-drawn imperfections, arbitrary asymmetry, or inconsistent textures.

Publication-quality human design usually looks intentional because repeated visual decisions are systematic.

Examples:

- the same entity uses the same color across panels;
- the same evidence status uses the same line style;
- the same interaction type uses the same connector grammar;
- shading direction is consistent;
- outline weight is controlled;
- spacing follows a coherent rhythm;
- visual emphasis reflects scientific importance.

> Human-designed appearance should come from **intentional visual grammar**, not simulated imperfection.

---

## 6. Palette discipline

Prefer a small semantic palette.

Normal target:

- 2–3 primary semantic colors;
- neutral greys / off-white;
- at most 1 additional accent when needed.

Do not assign a new saturated color to every object.

Color must encode identity, process, condition, or hierarchy rather than decoration.

For the Bath–RP system, existing project colors remain authoritative unless a task-specific Style Recipe explicitly overrides them.

---

## 7. Arrow and connector reconstruction

Generated arrows are treated as disposable draft content.

Publication arrows should normally be redrawn as vectors using the task-specific connector grammar.

A Style Recipe should specify:

- stroke weight;
- arrowhead size;
- curvature;
- color;
- solid / dashed / dotted semantics;
- directionality;
- confirmed / candidate / alternative encoding.

Do not let visual arrow certainty imply stronger mechanistic evidence than the science supports.

---

## 8. Typography replacement

All final scientific text should be added after image generation.

Replace generated text with controlled typography for:

- species names;
- chemical formulas;
- genes;
- pathway names;
- labels;
- legends;
- panel letters;
- annotations.

Do not accept AI-generated text merely because it is visually plausible.

---

## 9. Visual hierarchy normalization

Not every object should receive equal rendering effort.

For every figure, assign:

```text
Primary focal object(s)
Secondary supporting modules
Context / background elements
```

Rendering detail and visual contrast should decrease from primary → secondary → context.

Secondary and contextual elements should often be flatter, quieter, and simpler than the focal mechanism.

---

## 10. Subtraction Pass

After the first assembled draft, perform one explicit subtraction pass.

Ask of every non-essential visual element:

> Does this help explain scientific content, hierarchy, orientation, or identity?

If not, remove it.

Typical deletion targets:

- meaningless particles;
- redundant highlights;
- unnecessary gradients;
- decorative shadows;
- background texture;
- repeated molecules;
- duplicate arrows;
- ornamental lines;
- non-informative icons;
- excessive depth cues.

The purpose is not to hit a fixed deletion percentage. The purpose is to ensure that every retained element has a communication role.

---

## 11. AI Flavor Score

Score the final assembled draft from `0–10`.

Add one point for each materially present category:

1. glossy / plastic rendering;
2. excessive gradients;
3. neon / generic AI palette;
4. glow effects;
5. cinematic lighting;
6. decorative particles;
7. fake or unnecessary depth;
8. over-rounded / toy-like morphology;
9. inconsistent shading / perspective;
10. over-rendered or decorative objects that compete with information.

Interpretation:

```text
0–2  acceptable
3–4  polish required
5–6  clearly AI-flavored; major revision
7–10 regenerate or reconstruct rather than patch
```

The AI Flavor Score is a **visual warning metric**, not a scientific-quality score.

---

## 12. Final output QA

A publication-facing figure must pass all six dimensions:

1. **Scientific fidelity** — hard gate;
2. **Visual hierarchy**;
3. **Readability**;
4. **Aesthetic quality**;
5. **Style consistency**;
6. **Editability**.

Additional AI-artifact checks:

- malformed morphology;
- impossible object overlap;
- inconsistent perspective;
- pseudo-scientific molecular detail;
- gibberish text;
- malformed arrows;
- unexplained glow;
- repeated texture artifacts.

If scientific fidelity fails, reject the figure regardless of aesthetic quality.

---

## 13. Canonical production workflow

```text
USER + CHATGPT DEFINE SCIENTIFIC LOGIC
        ↓
SCIENCE LOCK
        ↓
PR20 VISUAL-ROLE RETRIEVAL
        ↓
MULTI-REFERENCE SYNTHESIS
        ↓
STYLE RECIPE
        ↓
LOW-TO-MODERATE RENDERING BRIEF
        ↓
ASSET-FIRST GENERATION
        ↓
MANUAL / VECTOR ASSEMBLY
        ↓
REPLACE ALL TEXT
        ↓
REDRAW CONNECTORS
        ↓
NORMALIZE PALETTE / STROKE / LIGHTING
        ↓
SUBTRACTION PASS
        ↓
AI FLAVOR QA
        ↓
SCIENTIFIC + VISUAL QA
        ↓
HUMAN APPROVAL
```

## Final principle

> **Use AI to render difficult visual assets; use PR20 and human design decisions to control the figure.**
