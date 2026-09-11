# Raw Scientific Figure Corpus Policy

## Core rule

The style system must be built in this order:

1. **Stage 0 — raw image corpus:** acquire and provenance-check at least **100 real source images**.
2. **Stage 1 — figure-level annotation:** annotate scientific purpose, information structure, layout, dimensionality, palette, connector grammar, density, evidence coding, and reusable principles.
3. **Stage 2 — element library:** only after the raw corpus gate is met, extract recurring cell, material, molecule, arrow, gradient, zoom, and label patterns.
4. **Stage 3 — Style Router:** train/validate routing from task → purpose → layout → style family → elements.

Element extraction is therefore blocked until the Stage 0 acceptance gate is satisfied.

## What counts toward the 100-image gate

A record counts as a **mirrored image** only if all of the following are true:

- the actual source figure/panel image file is stored locally in this project or in an explicitly linked asset store;
- the figure comes from a real published article;
- article, journal, year, DOI/URL, figure/panel locator, and source image URL are recorded;
- the reuse license or permission status is verified;
- the stored image is permitted to be redistributed in the repository where it is stored;
- a checksum is recorded;
- the image has been opened and visually inspected;
- the image is useful for scientific-figure design learning rather than being included only to increase sample count.

A metadata-only record, inaccessible publisher image, graphical-abstract locator, thumbnail without reuse permission, or unverified screenshot does **not** count toward the mirrored-image threshold.

## Public-repository rights rule

`codex-workbench` is currently public. Therefore full source-image files may be committed here only when reuse/redistribution is clearly allowed, for example:

- CC BY;
- CC0 / public domain;
- another explicit open license compatible with redistribution;
- explicit publisher/rights-holder permission.

For figures whose reuse rights are unclear or restrictive, retain an **index-only record** with source URL, DOI, figure number, rights note, and derived visual observations. Do not upload the source image to this public repository.

Third-party material embedded inside an otherwise open-access article must be checked separately; an article-level CC license does not automatically relicense excluded third-party content.

## Initial source quota

The first 100 mirrored images should target:

| Source family | Target | Rationale |
|---|---:|---|
| The ISME Journal | 30 | highest relevance to microbial interaction and environmental microbiology; 2024+ articles are fully OA under CC BY by journal policy, subject to third-party exceptions |
| Nature Communications | 30 | strong source for polished mechanism, biohybrid, interface, multiscale, and editorial scientific schematics; verify license article by article |
| Environmental Science & Technology | 20 | high relevance to environmental engineering, EET, materials, methane, redox, and graphical abstracts; mirror only OA/licensed figures |
| Water Research | 20 | high relevance to engineered microbial systems, conductive materials, DIET, treatment systems, and perturbation comparisons; mirror only OA/licensed figures |
| **Total** | **100** | minimum gate |

The quota may be rebalanced if a journal does not provide enough legally mirrorable images, but all four source families must remain represented.

## Diversity constraints

The corpus is not allowed to reach 100 by repeating one visual genre.

Recommended minimum coverage across the 100-image set:

- conceptual overview: ≥8
- microbial interaction / cross-feeding: ≥12
- mechanistic pathway: ≥12
- metabolic pathway: ≥8
- electron-transfer mechanism: ≥12
- material–microbe interface: ≥12
- environmental process / redox gradient: ≥8
- experimental design: ≥8
- comparative perturbation: ≥8
- integrated mechanism / evidence-to-model: ≥6
- graphical abstract: ≥10
- multiscale / zoom-in schematic: ≥8

One image may satisfy more than one functional tag, but its `primary_purpose` must be unique.

## Anti-bias constraints

- Prefer at least **60 unique articles** across the first 100 mirrored images.
- Normally no article should contribute more than **2 images**; maximum **3** when panels serve genuinely different design functions.
- No single laboratory/research group should dominate a style class.
- Journal prestige must not override functional relevance.
- Data-only plots, microscopy-only panels, and routine heatmaps do not count unless they contribute a reusable evidence-to-model or multiscale composition pattern.
- The corpus should favor 2D and restrained light-2.5D scientific schematics; realistic glossy 3D is excluded from the active style-learning set.

## Raw asset layout

```text
projects/scientific-figure-style-corpus/
├── assets/
│   ├── isme/
│   ├── nature-communications/
│   ├── est/
│   └── water-research/
├── manifests/
│   ├── raw-image-manifest.csv
│   └── index-only-sources.csv
├── corpus/
│   └── ... figure-level annotations ...
└── derived-elements/
    └── BLOCKED_UNTIL_RAW_CORPUS_100.md
```

Recommended asset filename:

`<sample_id>__<journal>__<year>__fig<figure>[_panel-<panel>].<ext>`

Do not use article titles as filenames.

## Required raw-image manifest fields

- `sample_id`
- `journal`
- `year`
- `article_title`
- `doi`
- `article_url`
- `figure_id`
- `panel_id`
- `source_image_url`
- `asset_path`
- `file_format`
- `pixel_width`
- `pixel_height`
- `sha256`
- `license`
- `license_url`
- `third_party_material_checked`
- `redistribution_allowed`
- `downloaded_at`
- `visual_inspection_status`
- `primary_purpose`
- `secondary_purposes`
- `style_family`
- `layout`
- `notes`

## Stage 0 acceptance gate

Stage 0 passes only when:

- mirrored image count ≥100;
- all counted assets pass provenance and rights checks;
- all counted assets have checksums and visual inspection complete;
- all four journal families are represented;
- diversity constraints are substantially met;
- duplicate/perceptually duplicate images have been removed;
- at least 60 unique source articles are represented;
- no unresolved copyright flag exists among counted mirrored assets.

Until this gate passes, `derived-elements/` remains blocked and Style Router outputs are considered experimental only.

## Relationship to the existing 20-record pilot

The original 20-record v0.1 batch remains useful as a **source-discovery and schema pilot**, but it is not the foundation corpus and does not satisfy Stage 0. Existing `active`/`candidate` annotations should be migrated into the raw-image workflow. Only records with an actual legally stored and inspected image may contribute to the ≥100 mirror count.
