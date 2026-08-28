# Evaluation — Experiment 002

## Routing result

- Project key: `POLYU`
- Primary PR class: `PR-MIX`
- Constituent classes: `PR-DATA` + `PR-FIG`
- Split or combined: combined

## Authoritative objects

1. Quantitative producer contract defining the derived metric name, formula, unit, and missing-value behavior.
2. Figure consumer contract defining the source field, axis semantics, threshold mapping, and annotation text.

## Why splitting is not viable

The two contracts form a version-coupled producer-consumer interface. Updating only one side creates a broken intermediate state because the figure refers to a field schema the data side does not provide. The migration therefore must be reviewed and merged atomically.

## Constituent validation gates

### `PR-DATA`

- [x] Metric formula is explicit and deterministic.
- [x] Numerator and denominator remain unchanged.
- [x] Transformation is limited to fraction → percent by multiplication by 100.
- [x] Unit migration is explicit.
- [x] Missing values remain missing; no silent imputation is introduced.
- [x] Downstream schema dependency is identified.
- [x] Reproducibility information is recorded.

### `PR-FIG`

- [x] Figure source field is updated to the new producer field.
- [x] Axis label reflects percent units.
- [x] Threshold mapping preserves meaning (`0.80` → `80`).
- [x] Annotation text matches the new units.
- [x] Figure semantics remain synchronized with the producer contract.
- [x] Export expectations are stated at the contract level.

## Anti-abuse / negative-control result

Two negative controls were evaluated:

1. Independent figure layout-only changes while data logic is unchanged → route as `PR-FIG`, not `PR-MIX`.
2. A data-normalization fix plus an unrelated figure color preference → split into separate `PR-DATA` and `PR-FIG` changes because validation and rollback paths are independent.

This demonstrates that merely touching multiple areas is not sufficient for `PR-MIX`.

## Outcome

**PASS**

The proposed `PR-MIX` rule behaves as intended for this controlled scenario:

- it recognizes a genuinely inseparable cross-boundary migration;
- it requires the union of constituent validation gates;
- it documents why splitting is invalid;
- it rejects superficially mixed but independently reviewable changes.

## Evidence boundaries

- Directly verified: routing decision, atomic dependency structure, constituent gate coverage, and negative-control classification.
- Not verified: all possible `PR-MIX` combinations beyond `PR-DATA` + `PR-FIG`.
- Not verified: behavior under automated CI or external execution tooling.

## Promotion recommendation

This experiment provides forward-validation evidence supporting the `PR-MIX` rule in `codex-playbook` PR #1. The rule can move from untested design to **validated in one controlled mixed-class scenario**, while broader cross-class coverage should remain experimental until more cases exist.
