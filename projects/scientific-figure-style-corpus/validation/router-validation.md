# Router Validation — Corpus v0.1

## Goal

Test whether the first real corpus can support task-first retrieval for the user's main figure families without relying on journal-name imitation.

## Test 1 — Bath–RP final integrated mechanism

**Task:** methane-driven dark inorganic carbon fixation in a defined Bath–RP coculture, with diffusible resources shown as candidates and evidence boundaries preserved.

**Recommended retrieval:**

- `ISME-2024-CHUANG-F1A` — two-organism RP cross-feeding grammar
- `NC-2019-NIEHAUS-F1` — chemical mediator nodes + connector semantics
- `ISME-2017-LOVLEY-F3` — evidence-aware interaction-zone hierarchy
- `EST-2023-METHANE-SELENATE-VA` — domain analogue, candidate pending pixel QA

**Router output:**

- purpose: integrated_mechanism / microbial_interaction
- layout: asymmetric two-organism interaction
- style: flat 2D mechanism
- focal hierarchy: CH4 + limited O2 → Bath → candidate diffusible resources → RP physiology/CBB
- evidence encoding: supported system-level phenotype strong; individual candidate carriers visually weaker

**Result:** PASS.

## Test 2 — Bath–Se biohybrid hypothesis

**Task:** Bath surface-associated semiconductor/Se nanostructure, photoelectron-assisted metabolism, no unsupported claim of direct EEU.

**Recommended retrieval:**

- `NC-2025-ZHOU-F2A` — biohybrid interface-centered soft 2.5D
- `NC-2020-YU-F1` — baseline vs engineered cell–material interface
- `EST-2024-FES-CONDUIT-VA` — self-assembled material/membrane zoom, pending pixel QA
- `NC-2019-RP-EEU-F1AB` — apparatus-to-interface scale separation

**Router output:**

- purpose: material_microbe_interface
- layout: zoom_in_multiscale
- style: soft 2.5D at the material only; biological labels remain flat
- focal hierarchy: light/material → interface → candidate electron uptake/support → metabolism/carbon fixation

**Result:** PASS.

## Test 3 — 5% vs 25% O2 perturbation

**Task:** matched comparison showing low-O2 donor output and coculture phenotype vs high-O2 weakening.

**Recommended retrieval:**

- `ISME-2016-STORCK-F1` — hold common elements fixed and vary the mechanism
- `NC-2020-YU-F1` — matched state comparison
- `WR-2025-SHU-WU-GA` — treatment × operating-condition comparison, pending pixel QA

**Router output:**

- purpose: comparative_perturbation
- layout: mirrored_comparison
- style: editorial 2D / flat mechanism hybrid
- constraint: same Bath/RP positions, same visual identities, same scale; vary O2 condition and downstream donor/metabolic state only

**Result:** PARTIAL PASS.

**Gap:** no directly inspected environmental-microbiology sample yet specifically encodes a low-O2 vs high-O2 perturbation with identical biological actors. Add 3–5 such samples in v0.2.

## Test 4 — GAC-facilitated interspecies coupling / potential DIET

**Task:** Bath → GAC → RP as a testable conductive-coupling hypothesis, with soluble-transfer alternative preserved.

**Recommended retrieval:**

- `ISME-2016-STORCK-F1` — distinguish mediated vs direct routes
- `ISME-2017-LOVLEY-F3` — aggregate/conductive transfer zone
- `WR-2021-ZHENG-DIET-GA` — conductive aggregate evidence boundary, pending pixel QA
- `EST-2023-FE3O4-BIOCHAR-VA` — conductive/capacitive material functions, pending pixel QA

**Router output:**

- purpose: electron_transfer + material_microbe_interface
- layout: two-organism interaction with central material hub
- style: flat 2D mechanism with restrained material texture
- evidence encoding: Bath→GAC→RP drawn as candidate/hypothesis until directly resolved; H2/formate/other soluble routes shown separately

**Result:** PASS for logic, PARTIAL for style until candidate material graphics receive pixel QA.

## Test 5 — Membrane-level EET/EEU cutaway

**Task:** cell-envelope-scale mechanism of extracellular electron exchange.

**Recommended retrieval:**

- `NC-2020-YU-F1`
- `EST-2024-FES-CONDUIT-VA`
- `EST-2025-H2O2-EEU-VA`

**Router output:**

- purpose: electron_transfer / material_microbe_interface
- layout: zoom_in_multiscale
- style: pathway cutaway 2D
- rule: electron arrows must cross explicit interface components; mediated routes must include the mediator

**Result:** PASS for structure; pixel styling remains partly pending.

## Test 6 — Environmental microoxic–anoxic gradient

**Task:** background/context schematic showing methane source, O2 penetration, overlap/interface, MOB activity, and downstream partners/minerals.

**Recommended retrieval:**

- `NC-2024-DIRECTIONAL-ET-F1` — layered redox-gradient storytelling
- `WR-2024-TROPICAL-MOX-GA` — methane oxidation environmental context, pending pixel QA

**Router output:**

- purpose: environmental_process
- layout: layered_gradient
- style: editorial 2D overview
- focal hierarchy: environment → CH4/O2 overlap → MOB biofilter → interaction zone

**Result:** PASS, with limited corpus depth.

## Test 7 — Graphical abstract adaptation

**Task:** compress a paper mechanism into one low-density visual story.

**Recommended retrieval:**

- currently uses scientific-purpose signals from 10 Water Research / ES&T graphical/visual abstracts
- pixel-level style transfer is blocked until QA promotion

**Result:** PARTIAL PASS.

**Gap:** add at least 8 directly inspected graphical abstracts across ES&T, Water Research, Nature Communications, and ISME-equivalent papers.

## Test 8 — Negative control: simple quantitative line plot

**Task:** plot CH4 consumption over time.

**Expected router behavior:** do not invoke the scientific-figure schematic corpus; use quantitative visualization standards instead.

**Result:** PASS by scope rule.

---

## v0.1 coverage verdict

The corpus is already strong enough for:

- two-organism microbial interaction;
- MIET/DIET route separation;
- evidence-aware arrow grammar;
- cell–material/biohybrid interfaces;
- multiscale electrode/interface figures;
- environmental redox-gradient framing;
- experimental design schematics.

The next sampling priority should **not** be more generic mechanism figures. It should target the identified gaps:

1. directly inspected low-O2 vs high-O2 matched perturbation graphics;
2. directly inspected graphical abstracts from ES&T and Water Research;
3. mineral/semiconductor–microbe figures using restrained, low-saturation 2.5D rather than glossy 3D;
4. evidence-to-model layouts that combine quantitative panels with a final mechanism without visually overstating causality;
5. methane-oxidizer-specific microbial interaction graphics.

## Promotion implication for playbook PR #23

The first real-corpus test supports the router's core taxonomy and task-first decision chain. However, the new `annotation_qc` block proved necessary in practice and should be considered for promotion into the playbook schema after the v0.2 direct-visual-QA pass.