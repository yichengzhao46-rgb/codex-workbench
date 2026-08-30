# Reusable Quantitative Data Validation Checklist

Use this checklist before packaging a quantitative research-data change.

## Source and structure

- [ ] Record the input file names and sheet/table names.
- [ ] Confirm the authoritative columns and units.
- [ ] Preserve biological replicate structure.
- [ ] Distinguish biological from technical replicates.
- [ ] Record missing values explicitly; do not silently drop them.

## Calculations

- [ ] Document normalization and unit-conversion formulas.
- [ ] Check denominator choice and sample-volume assumptions.
- [ ] Verify that aggregation occurs at the intended replicate level.
- [ ] Recalculate at least one representative row independently.

## Statistics

- [ ] State the statistical test, pairing, sidedness, and correction method.
- [ ] Check that sample size matches the intended biological replicate count.
- [ ] Separate descriptive summaries from inferential statistics.

## Reproducibility

- [ ] Keep raw inputs unchanged.
- [ ] Record software/script version when applicable.
- [ ] Ensure processed outputs can be regenerated from documented inputs and logic.
- [ ] Report unresolved assumptions or validation gaps in the PR.
