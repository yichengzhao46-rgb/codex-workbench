# Curated Figure Reference Libraries

This directory defines the canonical IDs for the two user-curated figure reference libraries used after the 2026-09-14 manual screening and split.

## Canonical IDs

- Main scientific figure style library: `M001` onward.
- Bioinformatics figure reference library: `BI001` onward.
- Old `R*`, `S*`, `Z*`, `U*`, and `B*` identifiers are retained only as `legacy_id` provenance.
- Physical asset paths are intentionally not renamed. Renaming the underlying files would break historical manifests, SHA-based validation, and source provenance.

## Current snapshot

### Main library

- 21 references total.
- 14 locally mirrored assets.
- 7 restricted/reference-only external figures.
- Canonical catalog: `projects/scientific-figure-style-corpus/manifests/main-reference-catalog.csv`.
- Current range: `M001`–`M021`; next ID: `M022`.

### Bioinformatics library

- 22 references total.
- 15 locally mirrored assets.
- 5 restricted external references.
- 2 open-access metadata-only references.
- Canonical catalog: `projects/bioinformatics-figure-reference-library/reference-catalog.csv`.
- Current range: `BI001`–`BI022`; next ID: `BI023`.

## Numbering order

Canonical numbering preserves the user's curation chronology rather than grouping by journal or topic. This keeps IDs stable as the libraries grow. Scientific function is stored separately in catalog fields such as `primary_purpose`, `style_family`, and `layout`.

For the main library, `M001`–`M014` are the surviving local figures from the manual screening and `M015`–`M021` are later user-added reference-only figures.

For the bioinformatics library, `BI001`–`BI013` are the figures moved out of the original curated set and `BI014`–`BI022` are later user-added bioinformatics references.

## Migration and retrieval

`id-map.csv` is the authoritative crosswalk from canonical IDs to legacy IDs and physical/source locations. New discussion, retrieval, style analysis, and figure-generation tasks should use the canonical IDs. Legacy IDs should only be used when tracing the original curation history or source manifests.

## Scope

The main library is for general scientific visual language: mechanism schematics, environmental-process overviews, material/microbe interfaces, perturbation comparisons, biohybrid systems, graphical abstracts, and related composition.

The bioinformatics library is for omics and analysis-led visual language: phylogeny, pathway reconstruction, gene-expression overlays, transcriptomics/proteomics, enrichment, correlation/network analysis, genome/MAG-resolved figures, and evidence-to-mechanism integration.
