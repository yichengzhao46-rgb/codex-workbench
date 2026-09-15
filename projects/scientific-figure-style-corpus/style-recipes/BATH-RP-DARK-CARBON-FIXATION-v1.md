# Bath–RP Dark Carbon Fixation — Style Recipe v1

## Scientific task
Create a mechanism-summary figure for a defined Bath–RP coculture under dark microoxic conditions. The figure should communicate methane oxidation by Bath as the upstream process, diffusible metabolic support across the extracellular space, maintenance of RP-associated physiology, and enhanced community-level inorganic-carbon incorporation.

Do not imply species-specific isotope incorporation, a dominant carrier, direct cell-to-cell electron transfer, or a quantified flux through any single transfer route.

## Reference assignment
- Overall two-partner composition: M001
- Bath membrane / carbon-allocation logic: M014
- Soft cell-volume rendering: M018
- Candidate-route line grammar and electron semantics: M019
- Condition-comparison grammar for the high-O2 variant: M016 + M018
- Staged explanation if a graphical-abstract version is needed: M021

## Layout
Use a horizontal two-organism composition with Bath on the left and RP on the right. Keep a broad extracellular exchange zone in the center. The center should remain visually open and should contain only the candidate diffusible resources and a small number of directional cues.

Suggested reading order:
1. CH4 + controlled O2 enter Bath.
2. Bath oxidation / redox module generates transferable products.
3. H2, formate, acetate and riboflavin occupy the shared extracellular zone.
4. Candidate uptake / use by RP supports energy-redox maintenance and carbon-assimilation capacity.
5. Bottom-level output: enhanced community-level inorganic-carbon incorporation.

## Cell rendering
Bath: spherical or coccoid, cool low-saturation blue, restrained 2.5D volume, simple outer envelope, no glossy 3D.

RP: rod-shaped, restrained warm red, similar visual weight to Bath. Keep morphology different but rendering language matched.

Do not use generic identical cells for the two species.

## Intracellular detail
Bath should contain only three compact modules:
- methane oxidation / carbon entry;
- respiratory energy-redox node;
- donor-product release node.

RP should contain only:
- dark respiration / energy-redox node;
- simplified CBB-related carbon-assimilation node;
- maintenance / biomass outcome.

Avoid enzyme-by-enzyme pathway density in the main mechanism figure.

## Extracellular exchange zone
Use four separate small labels or compact molecular icons:
- H2
- formate
- acetate
- riboflavin

Do not merge them into one large arrow. Their visual grammar should preserve the fact that several candidate support routes coexist.

## Connector grammar
- Solid neutral arrow: directly observed process or established intracellular transformation.
- Dashed colored arrow: candidate interspecies transfer / use inferred from combined evidence but not directly flux-resolved.
- Electron-specific arrow: one consistent accent color with an explicit e− cue only where an electron route must be highlighted.
- Carbon / metabolite arrows: separate color from electron arrows.
- Candidate riboflavin shuttle: dashed line; never present it as the dominant route.
- Acetate: show as carbon/energy cross-feeding, not as an electron-shuttle equivalent.

## Isotope / inorganic-carbon representation
Do not draw 13C-HCO3− entering RP alone. Use a shared lower output such as:

**Enhanced community-level inorganic-carbon incorporation**

If a bicarbonate icon is shown, connect it to the coculture-level output or shared biomass region rather than assigning it exclusively to one species.

## Palette
- Bath: #0A65B8 family, reduced saturation for fills.
- RP: #C43E3E family, reduced saturation for fills.
- Shared coculture / integration accent: #7A3EB1 used sparingly.
- Extracellular background: off-white or very pale neutral blue-gray.
- Electron accent: one consistent warm or deep-blue accent distinct from organism colors.
- Candidate routes: lower saturation and/or dashed line treatment.

Avoid rainbow coding.

## Typography
Use short labels. Prefer pathway/module names over sentences. RP species name may be italicized where full taxonomic naming is used; Bath can remain non-italic in the established project style.

Three text levels only:
1. organism / major process labels;
2. pathway / resource labels;
3. small evidence-boundary qualifier where needed.

## Information density
Target: medium.

The figure should be readable as a mechanism at first glance. Detailed gene names, full metabolite time courses, ATP/NADH plots, and isotope statistics belong in adjacent data panels or the caption, not inside the central mechanism schematic.

## High-O2 variant
For a perturbation version, reuse the exact organism geometry and overall layout. Change only:
- O2 condition cue;
- Bath donor-product output intensity;
- RP energy/redox maintenance state;
- community-level inorganic-carbon incorporation outcome.

This follows the matched-condition grammar from M016 and M018. Do not redesign both sides independently.

## Reusable motifs
- M001 open extracellular exchange zone
- M014 top-to-bottom Bath membrane-to-carbon organization
- M019 dashed candidate connector
- M018 restrained soft cell cutaway
- M016 matched perturbation geometry

## Elements to avoid
- DIET-style direct cell-to-cell arrow
- a single thick arrow implying one dominant carrier
- species-specific 13C assignment
- ATP or NADH labels placed exclusively inside RP unless species-resolved data support that assignment
- decorative glow around every metabolite
- dense protein-level pathway labels
- full 3D cells

## Anti-AI-look production controls

### Rendering intensity

```text
rendering_intensity = 2 / 5
```

Use restrained 2D–2.5D rendering. Cell volume can be indicated by one subtle tonal transition, but surfaces should remain matte and publication-like rather than glossy.

### Generation mode

Default to **asset-first generation + controlled assembly**.

Generate individually when needed:
- Bath cell shell / cutaway;
- RP cell shell / cutaway;
- small methane / oxygen visual motifs if an icon treatment is required.

Do not ask the image model to finalize:
- labels;
- chemical formulas;
- pathway names;
- arrows;
- evidence-status line styles;
- panel letters;
- final alignment.

Transparent-background single-cell assets are preferred.

### Negative-style vocabulary

```text
no glossy plastic cells
no neon blue-purple gradient aesthetic
no glowing arrows
no volumetric or cinematic light
no decorative floating particles
no toy-like cell morphology
no excessive roundness
no hyper-detailed pseudo-cellular structures
no futuristic infographic background
no strong drop shadows
no unnecessary texture
```

### Visual hierarchy

Primary: Bath → shared extracellular exchange → RP coupling logic.

Secondary: simplified intracellular energy/redox and CBB-related modules.

Context: CH4, O2, bicarbonate / inorganic-carbon outcome cues.

Contextual objects should be flatter and quieter than the two cells and the exchange zone.

### Post-generation reconstruction

Required before publication-facing use:

1. replace all generated text with controlled typography;
2. redraw all interspecies and evidence-bearing connectors as vectors;
3. normalize Bath/RP/coculture colors to the project palette;
4. normalize outline and arrow stroke weights;
5. remove non-informative particles, highlights, shadows, textures, and repeated molecular motifs;
6. verify one consistent lighting/shading direction;
7. run the subtraction pass;
8. run AI Flavor QA.

### AI Flavor target

Target score: `0–2 / 10`.

A score of `3–4` requires polish. A score of `5+` means the figure should be substantially reconstructed rather than cosmetically patched.

## Final QA hard gate

Scientific fidelity overrides aesthetic quality.

Reject any version that visually converts candidate diffusible support into proven DIET, assigns community-level isotope incorporation specifically to RP, implies one dominant carrier, or uses connector strength/style to overstate evidence.

Then assess:
- visual hierarchy;
- readability;
- aesthetic quality;
- style consistency;
- editability;
- AI Flavor Score.

## Final visual direction
A clean, publication-grade 2D / restrained-2.5D two-organism mechanism with a wide shared extracellular zone, disciplined arrow semantics, low-saturation Bath/RP colors, and explicit separation between observed processes and candidate interspecies-transfer routes. The figure should look synthesized from several reference grammars rather than copied from any one source, and it should look intentionally designed rather than generically AI-generated.
