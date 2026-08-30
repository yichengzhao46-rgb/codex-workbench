# Evaluation — Experiment 001

## Routing decision

- Project key: `POLYU`
- Scenario: reusable quantitative research-data validation method
- Authoritative changed object: data-analysis validation logic
- Primary PR class: `PR-DATA`
- Secondary checklist: none
- Split or combined: combined as one atomic data-method experiment

## Why this classification is correct

The project context suggests research writing by default, but the changed object is not manuscript prose. It is reusable logic for validating quantitative data processing. Under the routing precedence defined in `codex-playbook` PR #1, the authoritative changed object determines the primary PR class. Therefore `PR-DATA` correctly overrides the `POLYU` profile's default `PR-RSCH` suggestion.

## Validation performed

- Dedicated branch used: `codex/validate-research-pr-routing`.
- Raw/source experimental data were not added or modified.
- The checklist explicitly preserves biological replicate structure.
- Missing values are required to remain explicit rather than being silently removed.
- Unit conversion, normalization, denominator choice, replicate aggregation, statistical test definition, and reproducibility are all represented.
- The experiment output is isolated under `experiments/001-research-pr-routing-validation/`.

## Outcome

**PASS for routing precedence.**

The generic PR taxonomy and personal project profile can coexist without ambiguity in this test case. The project key provides context, while the authoritative object controls class selection.

## Limitation

This validates a single cross-signal case (`POLYU` context → `PR-DATA`). It does not yet validate every PR class or `PR-MIX` behavior.

## Promotion recommendation

The routing-precedence rule is suitable to be marked as forward-validated once this experiment is reviewed through a Draft PR. Broader class coverage should remain experimental until additional cases are exercised.
