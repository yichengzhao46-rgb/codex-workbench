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

## Migration and retrieval

`id-map.csv` is the authoritative crosswalk from canonical IDs to legacy IDs and physical/source locations. New discussion, retrieval, style analysis, and figure-generation tasks should use the canonical IDs. Legacy IDs should only be used when tracing the original curation history or source manifests.

## Scope

The main library is for general scientific visual language: mechanism schematics, environmental-process overviews, material/microbe interfaces, perturbation comparisons, biohybrid systems, graphical abstracts, and related composition.

The bioinformatics library is for omics and analysis-led visual language: phylogeny, pathway reconstruction, gene-expression overlays, transcriptomics/proteomics, enrichment, correlation/network analysis, genome/MAG-resolved figures, and evidence-to-mechanism integration.
