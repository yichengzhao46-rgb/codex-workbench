# Bioinformatics Figure Reference Library

This library contains figures explicitly selected by the user as references for bioinformatics-analysis figure design.

## Canonical numbering

- Canonical IDs: `BI001`–`BI022`.
- Next available ID: `BI023`.
- Old `R*`, `S*`, `Z*`, and `B*` identifiers are retained only as `legacy_id` provenance aliases.
- Canonical catalog: `reference-catalog.csv`.
- Cross-library migration map: `../figure-reference-libraries/id-map.csv`.

Physical asset paths are intentionally not renamed during canonical renumbering so historical manifests, SHA validation and source provenance remain intact.

## Current set

- 22 references total.
- 15 locally mirrored assets.
- 5 restricted external references.
- 2 open-access external metadata-only references.

The first 13 canonical records (`BI001`–`BI013`) are the user-selected bioinformatics references split from the original manually curated corpus. `BI014` onward are manually added article figures selected after the split.

## Added article references

- `BI014` — Yu et al., Environmental Science & Technology (2025), Figure 4, DOI `10.1021/acs.est.4c11221` — restricted external reference.
- `BI015` — Guzman et al., Nature Communications (2019), Figure 4, DOI `10.1038/s41467-019-09377-6` — locally mirrored, CC BY 4.0.
- `BI016` — Huang et al., The ISME Journal (2022), Figure 5, DOI `10.1038/s41396-021-01078-7` — restricted external reference.
- `BI017` — Yao et al., Environmental Science & Technology (2025), Figure 5, DOI `10.1021/acs.est.5c01275` — restricted external reference.
- `BI018` — Han et al., Environmental Science & Technology (2026), Figure panel e, DOI `10.1021/acs.est.5c17814` — restricted external reference.
- `BI019` — Wang et al., Environmental Science & Technology (2026), Figure 7, DOI `10.1021/acs.est.5c16493` — restricted external reference.
- `BI020` — Tian et al., Advanced Science (2026), Figure 6, DOI `10.1002/advs.202516258` — CC BY 4.0, metadata-only reference pending local mirror.
- `BI021` — Liu et al., Advanced Science (2025), Figure 6, DOI `10.1002/advs.202501376` — locally mirrored, CC BY 4.0.
- `BI022` — Ye et al., Nature Communications (2025), Figure 5, DOI `10.1038/s41467-025-60908-w` — CC BY-NC-ND 4.0, metadata-only under the stricter public-binary policy.

## Intended use

Use this library for phylogeny, metabolic/pathway reconstruction, genome/MAG-resolved figures, transcriptomics/proteomics, gene-level expression overlays, enrichment analysis, correlation/network analysis, and evidence-to-mechanism composition.

See `reference-catalog.csv` for the canonical current set, `manifest.csv` for locally mirrored assets, `restricted-references.csv` for restricted external references, `open-access-references.csv` for open-access provenance, `final_split.csv` for the original split decisions, and `split_report.json` for split validation.
