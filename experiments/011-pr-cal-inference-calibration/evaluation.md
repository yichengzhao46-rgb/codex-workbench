# PR-CAL Forward Validation

## Objective

Validate the proposed `PR-CAL` specialist workflow for `PR-RSCH` so that scientific review avoids both overclaiming and reflexive over-conservatism.

The tested behavior is: use the **full active journal corpus as the outer empirical mechanism envelope**, then place each manuscript claim inside that envelope according to the manuscript's own evidence.

This deliberately rejects two failure modes:

1. an exact same-system / same-journal / nearest-neighbour precedent is treated as mandatory before a mechanism claim is allowed; and
2. the existence of one strong published claim is treated as automatic permission to use the same verb with weaker local evidence.

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
- Recognize that bounded system-level metabolic-coupling claims occur within the global published mechanism envelope even when a narrower species-specific flux remains unresolved.
- Allow wording such as `The combined evidence supports a model in which diffusible metabolic exchange contributes to the coupled response`, while preserving the unresolved species-specific flux boundary.

### Result

**PASS** — the global corpus does not impose a single-assay veto, while local evidence still prevents species-specific over-attribution.

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
- Do not use strong examples elsewhere in the global corpus to compensate for weak local independence.

### Result

**PASS** — global corpus membership does not override the local independence requirement.

## Case 3 — Genuine evidence insufficiency inside a broad global envelope

### Scenario

The active corpus contains multiple published DIET mechanism papers, including studies with direct incapacity controls, genetic or electrochemical interventions, and strongly convergent process/molecular evidence.

A new manuscript reports only that a conductive material increases one bulk response endpoint. It has no conductive-interface evidence, no selective perturbation, no exclusion of soluble mediators, and no species-resolved electron-transfer evidence.

### Incorrect corpus-permission outcome

`DIET is demonstrated because DIET claims exist within the benchmark corpus.`

### Expected PR-CAL outcome

- Recognize that DIET is a mechanism layer represented within the global corpus envelope.
- Reject direct DIET wording for this manuscript because its local evidence does not place it at the direct/strong DIET position within that envelope.
- Permit only a bounded statement such as `the response is consistent with a possible conductive-material-associated interaction` if scientifically useful.
- Identify the missing discriminating evidence.

### Result

**PASS** — the global envelope defines what mechanism layers are publishable, while local evidence controls exact wording and specificity.

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

## Case 5 — Severity calibration without exact-precedent requirement

### Scenario

A manuscript uses `supports a model in which` for a mechanism backed by several orthogonal observations but lacking one definitive direct flux assay. No paper in the corpus has exactly the same organism pair and assay combination, but comparable mechanism layers are represented across the corpus.

### Expected PR-CAL outcome

- Do not require an exact same-system or same-journal precedent before allowing the bounded mechanism claim.
- Do not label the passage P0 solely because the direct flux assay is absent.
- Evaluate local independence, alternatives, and exact wording first.
- Use P1 only if the claim still materially exceeds or understates the manuscript's defensible local position within the global corpus envelope; otherwise P2/P3 or retain.

### Result

**PASS** — exact-precedent absence is not used to create an artificial conservative ceiling.

## Case 6 — Same mechanism layer, different local verb strength

### Scenario

The corpus contains papers using `demonstrates`, `supports`, `indicates`, `promotes`, and `suggests` for different DIET/EET/metabolic-coupling layers under evidence packages of different strength.

Two manuscripts make the same broad mechanism claim:

- Manuscript A has genetic incapacity control + isotope tracing + functional perturbation.
- Manuscript B has phenotype + metabolites + time course + one pathway-relevant perturbation, but no direct isolation of the exact flux step.

### Expected PR-CAL outcome

- Both may remain inside the same **global mechanism layer** represented in the corpus.
- Manuscript A may justify `shows/demonstrates` for the isolated layer.
- Manuscript B may justify `supports/indicates` for the bounded mechanism layer.
- Do not force Manuscript B down to purely agnostic language merely because it lacks Manuscript A's strongest assay.

### Result

**PASS** — corpus-wide mechanism admissibility and local verb calibration remain separate.

## Overall result

**PASS**

The revised workflow behaves symmetrically:

- uses the full active corpus as the outer empirical mechanism boundary;
- does not impose mandatory same-journal or nearest-neighbour matching;
- prevents unsupported causal/species-specific/mechanistic inflation;
- prevents single-assay vetoes from erasing convergent evidence;
- prevents corpus membership from becoming automatic permission to borrow stronger wording;
- rejects pseudo-triangulation;
- treats limitations as boundaries rather than automatic nullifiers;
- calibrates review severity to the actual local evidence mismatch inside the global published envelope.

## Evidence boundary

This is controlled instruction-level forward validation. It does not prove that every future scientific judgment will be calibrated correctly. Ambiguous real manuscripts should be added as regression cases, particularly when evidence streams share hidden dependencies, the corpus contains heterogeneous mechanism definitions, or alternative explanations are difficult to rank.

## Promotion recommendation

Suitable for adoption as a `PR-RSCH` specialist overlay, with real-manuscript use monitored for both false strengthening and false weakening.
