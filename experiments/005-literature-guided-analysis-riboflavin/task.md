# Experiment 005 — Literature-guided Data Analysis Advisor validation on Chapter 3 riboflavin data

## Objective

Forward-validate `codex-playbook` Draft PR #6 (`Literature-guided Data Analysis Advisor`) against a representative real research case from the user's Confirmation Report Chapter 3.

The validation question is not whether riboflavin is already proven to mediate Bath-to-RP electron transfer. It is whether the Skill can:

1. understand the actual data structure before recommending analyses;
2. search literature that matches the biological system, measurement, perturbation and mechanistic question;
3. extract transferable analysis/attribution logic rather than merely list citations;
4. generate 3–5 genuinely distinct directions;
5. distinguish analyses possible with current data from experiments/new measurements required for stronger mechanistic claims;
6. preserve community-level and causal evidence boundaries;
7. stop at the recommendation gate before quantitative execution.

## User case

Dataset/context: Chapter 3 Bath–RP coculture riboflavin result in `Confirmation Report-2(1)_riboflavin_revised_v2.docx`.

Observed data include:

- extracellular riboflavin in RP, Bath and Bath–RP coculture at 24 and 140 h;
- a high-O2 (25% O2) coculture perturbation, with extracellular riboflavin increasing from 7.95 ± 2.65 μg L-1 at 24 h to 15.15 ± 3.05 μg L-1 at 140 h while remaining below the standard coculture;
- formate, acetate and H2 dynamics;
- EEM P1–P3 redistribution;
- community ATP and NADH/NAD+ responses;
- RP qPCR/physiological maintenance;
- community-level 13C bicarbonate incorporation;
- high-O2 Bath monoculture evidence showing methane oxidation remained active while formate/acetate/H2 donor output contracted.

Current working interpretation: riboflavin is positioned as a **candidate soluble electron shuttle / third candidate MIET route**, not as directly demonstrated Bath-to-RP electron flux.

## Expected Skill behavior

### Step 1
Build a data-understanding card and preserve the distinction between:

- extracellular riboflavin concentration;
- riboflavin production/release rate;
- riboflavin redox state/speciation;
- riboflavin-mediated electron-transfer flux.

### Step 2
Search literature across at least these query families:

- direct system match: `Methylococcus capsulatus Bath` extracellular flavins;
- recipient/system analogy: `Rhodopseudomonas palustris` dark IET and riboflavin;
- functional mechanism match: riboflavin/flavin electron shuttle and EET;
- perturbation/pattern match: shuttle present while overall phenotype or donor pool changes;
- analytical-method match: DPV/CV, LC-MS/HPLC, add-back/depletion, normalization to biomass/growth state;
- measurement limitation: flavin fluorescence and redox-state dependence.

### Step 3
Extract transferable reasoning frameworks such as:

- detection + chemical identity + electrochemical redox signature + functional perturbation/add-back;
- normalization of extracellular flavin abundance to cell biomass/physiological state;
- distinction between shuttle abundance and actual electron-transfer flux;
- coexistence of multiple IET routes rather than a single-carrier model.

### Step 4
Generate 3–5 analytically distinct directions, with priority, literature support, required inputs, expected outputs, applicability and what each cannot establish.

The preferred output should distinguish:

- **current-data analysis** directions;
- **new-measurement / experimental validation** directions.

### Step 5
Do not execute a selected direction because the user has not selected one in this validation run.

## Acceptance criteria

- [ ] Skill triggers correctly for this real analysis-choice case.
- [ ] Data are read before literature search.
- [ ] Literature includes direct Bath flavin evidence plus mechanistically relevant IET/EET analogues.
- [ ] Recommendations are not generic statistical tests.
- [ ] At least three distinct directions are produced.
- [ ] At least one direction is executable using current data only.
- [ ] At least one direction identifies stronger new evidence needed to test the shuttle mechanism.
- [ ] Recommendations explicitly distinguish abundance/availability from electron-transfer flux.
- [ ] Community ATP/NADH and bulk 13C remain community-level.
- [ ] Riboflavin is not upgraded from candidate shuttle to demonstrated Bath-to-RP MIET.
- [ ] User-choice gate is preserved before execution.
- [ ] Validation identifies any improvement needed in the Skill itself.
