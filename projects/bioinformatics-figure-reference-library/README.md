# Bioinformatics Figure Reference Library

This library contains figures explicitly selected by the user as references for **bioinformatics result visualization**. It is maintained independently from PR20's mechanism / scientific visual-learning corpus so that result-plot retrieval and mechanism-figure retrieval do not contaminate each other.

## Canonical numbering

- Canonical IDs: `BI001`–`BI022`.
- Next available ID: `BI023`.
- Old `R*`, `S*`, `Z*`, and `B*` identifiers are retained only as `legacy_id` provenance aliases.
- Canonical catalog: `reference-catalog.csv`.

Physical asset paths are intentionally not renamed during canonical renumbering so historical manifests, SHA validation and source provenance remain intact.

## Current set

- 22 references total.
- 15 locally mirrored assets.
- 5 restricted external references.
- 2 open-access external metadata-only references.

The first 13 canonical records (`BI001`–`BI013`) are the user-selected bioinformatics references split from the original manually curated corpus. `BI014` onward are manually added article figures selected after the split.

## PR21 objective

PR21 converts the current reference set into a dedicated **RNA-seq / bioinformatics visual-reference system**.

The next step is not broad corpus expansion. The required workflow is:

1. **BI001–BI022 visual-role decomposition**
2. **Map each reference against the planned WP3–WP8 bioinformatics outputs**
3. **Detect missing plot types / visual roles**
4. **Supplement only the gaps with ~6–10 high-quality pure bioinformatics-result figures**
5. **Run human visual selection / QA before promotion**

The priority gap categories are:

- PCA / sample separation
- volcano / DEG overview
- pathway enrichment and GSEA
- key-gene heatmap
- species-resolved transcriptomics
- integrated QC → DE → pathway → mechanism multipanel layouts

A reference does **not** need to match the Bath–RP biological topic exactly. For PR21, visual quality, information organization, and transferability to the planned transcriptomics outputs are more important than mechanistic-topic similarity.

## Intended use

Use this library for result-oriented bioinformatics figure design: PCA, differential-expression summaries, enrichment/GSEA, gene-level heatmaps, species-resolved transcriptomics, genome/MAG-resolved result panels, correlation/network analysis, and integrated transcriptomic multipanels.

Mechanism / conceptual illustration references remain the responsibility of PR20.

See `reference-catalog.csv` for the canonical current set, `manifest.csv` for locally mirrored assets, `restricted-references.csv` for restricted external references, `open-access-references.csv` for open-access provenance, `final_split.csv` for the original split decisions, and `split_report.json` for split validation.
