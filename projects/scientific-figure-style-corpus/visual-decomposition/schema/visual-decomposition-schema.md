# Visual Decomposition Schema

This schema defines the structured visual analysis used for the user-curated PR20 main library.

## 1. Identity and status

- `canonical_id`: stable `M###` identifier.
- `legacy_id`: provenance alias only.
- `visual_analysis_status`: `pending_visual_decomposition | in_progress | completed_batch1 | completed`.
- `note_file`: path to the detailed per-reference note when completed.

## 2. Dimensionality and composition

- `dimensionality`: `flat_2d | editorial_2d | soft_2_5d | full_3d | hybrid_2d_3d`.
- `overall_composition`: free-text description of the large-scale spatial organization.
- `layout_archetype`: controlled layout family.
- `reading_direction`: dominant intended reading order.
- `panel_structure`: single or multi-panel organization.
- `visual_hierarchy`: what is noticed first, second and third.

## 3. Object rendering

- `cell_rendering`: geometry, morphology specificity, outline, fill, surface and internal detail.
- `membrane_intracellular_rendering`: membrane layers, organelles/proteins/pathways and cutaway logic.
- `material_rendering`: minerals, GAC, electrodes, semiconductors, nanoparticles and interfaces.
- `molecule_metabolite_rendering`: gases, metabolites, ions, electrons and molecular structures.

For 2.5D/3D references also record geometry, perspective, light direction, shadow softness, surface treatment, translucency and depth separation.

## 4. Arrow and connector grammar

Analyze arrows as a visual language, not decoration. Distinguish when visible:

- metabolic / material flow;
- electron flow;
- carbon flow;
- gas exchange;
- causal or state-transition arrows;
- bidirectional exchange;
- inhibitory or blocking marks;
- dashed / speculative / candidate pathways;
- established versus hypothetical relationships;
- color, line weight and arrowhead semantics.

## 5. Palette and typography

- `palette`: dominant hues, temperature, saturation and accent logic.
- `typography_labeling`: hierarchy, label placement, font scale, contrast and dependency on caption text.
- `whitespace`: sparse / balanced / dense and how empty space separates information classes.

## 6. Density, depth and evidence integration

- `information_density`: `low | medium | medium-high | high`.
- `perspective_camera`: flat, cutaway, oblique, isometric or scene perspective.
- `lighting_shadow`: semantic lighting versus volumetric rendering.
- `transparency_depth`: layering, alpha, glow, foreground/background separation.
- `evidence_integration`: how data, mechanism, environmental context or thermodynamic context are combined.

## 7. Transferable knowledge

- `reusable_motifs`: visual components worth reusing.
- `best_visual_roles`: presentation problems this reference solves especially well.
- `avoid_transfer`: features that should not be copied or that fail at typical journal/PPT scale.
- `notes`: concise overall judgment.

## 8. Per-reference note structure

Each completed `notes/M###.md` should contain:

1. Figure identity
2. Functional role
3. Layout and reading logic
4. Cell / object rendering
5. Arrow grammar
6. Palette / outline / typography
7. Information density and evidence style
8. Best reusable elements
9. Suitable future use cases in the Bath–RP / Bath–Bio-Se project
10. Weaknesses / what not to imitate

## 9. Evidence rule

Detailed visual fields must come from direct inspection of the actual figure. Caption-only or topic-only inference is not sufficient for `completed` status.
