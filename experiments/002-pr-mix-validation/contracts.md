# Atomic producer-consumer contract migration

## Data contract (`PR-DATA`)

### Before

```text
field: normalized_response
unit: fraction
formula: response / reference
missing values: propagate as missing
```

### After

```text
field: normalized_response_pct
unit: percent
formula: (response / reference) * 100
missing values: propagate as missing
```

### Required validation

- Confirm the numerator and denominator remain unchanged.
- Confirm the only mathematical transformation is multiplication by 100.
- Confirm unit changes from fraction to percent.
- Confirm missing values remain missing rather than being silently imputed.
- Confirm downstream consumers use the new field name and unit.
- Record the formula so the transformation is deterministic and reproducible.

## Figure contract (`PR-FIG`)

### Before

```text
source field: normalized_response
axis label: Normalized response
reference threshold: 0.80
threshold annotation: 0.80
```

### After

```text
source field: normalized_response_pct
axis label: Normalized response (%)
reference threshold: 80
threshold annotation: 80%
```

### Required validation

- Confirm the figure consumes `normalized_response_pct`.
- Confirm axis semantics explicitly indicate percent.
- Confirm the threshold maps from 0.80 to 80 without changing its meaning.
- Confirm annotation text matches the new unit.
- Confirm any exported figure would remain semantically consistent with the data contract.

## Atomicity check

The migration is atomic because the producer schema and consumer schema are version-coupled. A merge containing only one side creates an invalid interface:

| Intermediate state | Result |
| --- | --- |
| New data contract + old figure contract | Figure requests missing `normalized_response` field. |
| Old data contract + new figure contract | Figure requests unavailable `normalized_response_pct` field. |
| Both updated together | Producer-consumer schema remains valid. |

Therefore the authoritative changed objects span both `PR-DATA` and `PR-FIG`, and the combined migration qualifies for `PR-MIX`.

## Negative control — must NOT use PR-MIX

Scenario: the data formula remains unchanged, while an independent figure-only request moves the legend and changes font size.

Changed objects:

- data logic: no substantive change;
- figure layout/style: changed.

Expected routing: `PR-FIG`, not `PR-MIX`.

A second negative-control scenario is a data normalization fix plus an unrelated figure color preference. Even though two files may change in the same working session, they have independent validation and rollback paths and should be split into `PR-DATA` and `PR-FIG` changes rather than packaged as `PR-MIX`.
