# PR-CAL Forward Validation

## Objective

Validate the proposed `PR-CAL` specialist workflow for `PR-RSCH` so that scientific review avoids both overclaiming and reflexive over-conservatism.

The tested behavior is: select the **strongest defensible claim** after considering the full evidence set, its independence, material alternatives, and the remaining evidence boundary.

## Case 1 — Convergent evidence without one fully isolating assay

### Scenario

A defined coculture study reports:

- community-level inorganic-carbon incorporation by bulk isotope analysis;
- physiological maintenance/growth of the partner under coculture conditions;
- candidate diffusible metabolite production/turnover patterns;
- partner substrate-utilization controls for relevant metabolites;
- a donor-availability perturbation that preserves methane oxidation but weakens transferable reduced-product patterns and the coupled partner-associated response.

No species-resolved isotope measurement directly quantifies partner-specific bicarbonate incorporation.

### Incorrect over-conservative outcome

`The mechanism is unsupported and no conclusion about metabolic coupling can be drawn because the isotope measurement is not species-resolved.`

### Expected PR-CAL outcome

- Do **not** claim direct partner-specific isotope incorporation.
- Retain the direct community-level inorganic-carbon-incorporation conclusion.
- Recognize the orthogonal physiological, metabolite, substrate-use, and perturbation evidence as convergent support for a bounded metabolic-coupling interpretation.
- Allow wording such as `The combined evidence supports a model in which diffusible metabolic exchange contributes to the coupled response`, while preserving the unresolved species-specific flux boundary.

### Result

**PASS** — the claim corridor separates the unsupported species-specific statement from the stronger but defensible system-level/mechanism-consistent interpretation.

## Case 2 — Pseudo-triangulation from one measurement

### Scenario

A manuscript treats the following as three independent lines of evidence:

- concentration change;
- percent change calculated from the same concentration data;
- fold change calculated from the same concentration data.

### Expected PR-CAL outcome

- Identify these as dependent representations of one underlying signal.
- Do not upgrade evidence strength by counting them as three independent observations.
- Keep the claim at the evidence tier warranted by the original measurement and any genuine controls.

### Result

**PASS** — the independence gate blocks artificial evidence inflation.

## Case 3 — Genuine evidence insufficiency

### Scenario

A conductive material increases one bulk response endpoint, but there is no conductive-interface evidence, no selective perturbation, no exclusion of soluble mediators, and no species-resolved electron-transfer evidence.

### Incorrect over-positive outcome

`The result demonstrates DIET.`

### Expected PR-CAL outcome

- Reject direct DIET language.
- Permit only a bounded statement such as `the response is consistent with a possible conductive-material-associated interaction` if scientifically useful.
- Identify the missing discriminating evidence.

### Result

**PASS** — the upper-bound gate preserves conservative wording where the evidence really is weak.

## Case 4 — Limitation should bound, not erase, a supported conclusion

### Scenario

A claim is directly supported at community scale but cannot be resolved to one species.

### Expected PR-CAL outcome

Prefer:

`The experiment demonstrates increased community-level inorganic-carbon incorporation, while the bulk measurement does not resolve the species-specific contribution.`

Over:

`Because species-specific incorporation cannot be resolved, no conclusion can be drawn from the isotope experiment.`

### Result

**PASS** — the limitation is retained without negating the valid direct conclusion.

## Case 5 — Severity calibration

### Scenario

A manuscript uses `supports a model in which` for a mechanism backed by several orthogonal observations but lacking one definitive direct flux assay.

### Expected PR-CAL outcome

- Do not label the passage P0 solely because the direct flux assay is absent.
- Evaluate independence, alternative explanations, and exact wording first.
- Use P1 only if the claim still materially exceeds or understates the evidence corridor; otherwise P2/P3 or retain.

### Result

**PASS** — severity is tied to actual incompatibility with evidence rather than directness alone.

## Overall result

**PASS**

The proposed workflow behaves symmetrically:

- prevents unsupported causal/species-specific/mechanistic inflation;
- prevents single-assay vetoes from erasing convergent evidence;
- rejects pseudo-triangulation;
- treats limitations as boundaries rather than automatic nullifiers;
- calibrates review severity to the size of the evidence mismatch.

## Evidence boundary

This is controlled instruction-level forward validation. It does not prove that every future scientific judgment will be calibrated correctly. Ambiguous real manuscripts should be added as regression cases, particularly when evidence streams share hidden dependencies or alternative explanations are difficult to rank.

## Promotion recommendation

Suitable for adoption as a `PR-RSCH` specialist overlay, with real-manuscript use monitored for both false strengthening and false weakening.
