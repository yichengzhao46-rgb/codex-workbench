# Experiment 002 — PR-MIX Validation

## Objective

Test whether the `PR-MIX` class is used only for a genuinely atomic cross-boundary change rather than as a catch-all for any task touching multiple areas.

## Scenario

Project context: `POLYU`.

A reusable analysis contract defines a derived metric called `normalized_response`. A paired figure contract consumes that exact field and requires a visual threshold annotation tied to the same metric definition.

The proposed change renames and redefines the derived metric to `normalized_response_pct` and simultaneously updates the figure contract to consume the new field and display the corresponding percentage threshold. Shipping either side alone would break the producer-consumer contract:

- data side only: the figure contract references a removed field and becomes invalid;
- figure side only: the figure contract expects a field the data contract does not produce.

The two authoritative objects are therefore:

1. a quantitative data-analysis contract (`PR-DATA`), and
2. a figure semantics/annotation contract (`PR-FIG`).

## Expected routing

- Project key: `POLYU`
- Primary PR class: `PR-MIX`
- Constituent classes: `PR-DATA` + `PR-FIG`
- Split or combined: combined

## Why this should qualify as PR-MIX

This is one atomic interface migration. The data producer and figure consumer must move together to preserve a valid shared schema. Splitting the change would leave one side unusable at the merge boundary.

## Anti-abuse condition

Merely touching both data and figure files is insufficient. `PR-MIX` passes only if:

- multiple authoritative objects are identified;
- their dependency is explicit;
- splitting would create an invalid intermediate state;
- the validation gates for every constituent class are applied.

## Acceptance criteria

- [ ] `PR-MIX` is selected for the atomic migration.
- [ ] `PR-DATA` and `PR-FIG` are both named as constituent classes.
- [ ] The reason splitting is not viable is documented.
- [ ] Data validation checks the metric definition, units, inputs, missing-value behavior, and reproducibility.
- [ ] Figure validation checks the consumed field, annotation semantics, threshold mapping, and export expectations.
- [ ] A negative-control scenario is evaluated to show when the same two classes should be split instead of using PR-MIX.
- [ ] No raw research data, credentials, or private material are added.
