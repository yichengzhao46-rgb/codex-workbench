# PR-CAL out-of-sample holdout validation

## Purpose

Validate `PR-CAL` against experimental papers that were **not included in the 64-study calibration corpus** when the rules were designed. These papers remain outside the training/calibration corpus for this test.

The validation question is not whether PR-CAL reproduces every author's exact wording. It asks whether PR-CAL would place the focal claim in the same defensible strength region without systematically downgrading already-published mechanisms or licensing unsupported specificity.

## Holdout set

### H1 — The ISME Journal
**Walker et al. (2020), _Syntrophus conductive pili demonstrate that common hydrogen-donating syntrophs can have a direct electron transfer option_.**

Source: https://academic.oup.com/ismej/article/14/3/837/7474816

Evidence architecture:
- native conductive pili measured by conductive AFM;
- heterologous expression of the pilin gene and current-production tests;
- defined coculture with an electron-accepting partner;
- critical incapacity control: partner strain unable to consume H2 or formate;
- growth/stoichiometry persisted when DIET was the remaining feasible interspecies transfer route.

Published claim pattern:
- direct/high-strength for the tested organism's ability to grow via DIET;
- broader ecological prevalence remains framed as likely/should be reconsidered rather than directly quantified.

PR-CAL prediction:
- `D` for organism-level DIET capability because the incapacity control isolates the route sufficiently;
- `Q/S` for how widespread DIET is in environmental communities.

**Result: PASS.** PR-CAL preserves the strong direct claim while bounding the broader extrapolation.

### H2 — The ISME Journal
**Lerminiaux et al. (2025), _Lysis of Escherichia coli by colicin Ib contributes to bacterial cross-feeding by releasing active β-galactosidase_.**

Source: https://academic.oup.com/ismej/article/19/1/wraf032/8024246

Evidence architecture:
- defined E. coli–Salmonella system;
- toxin-mediated lysis;
- released active β-galactosidase;
- galactose-uptake response and spent-medium growth benefit;
- transcriptional response;
- explicit limitation: exclusive monosaccharide-only cross-feeding conditions could not be established.

Published claim pattern:
- direct discovery language for lysis releasing active enzyme and supporting the recipient;
- bounded mechanism language because cross-feeding could not be isolated exclusively to the monosaccharide route.

PR-CAL prediction:
- `M`: strong system-level cross-feeding mechanism, narrower route-exclusivity unresolved.

**Result: PASS.** The limitation narrows exclusivity rather than erasing the positive mechanism claim.

### H3 — Environmental Science & Technology
**Zhao et al. (2025), _Mutualistic Cross Feeding Mediated by Metabolic Intermediates and Siderophores Enhances Dibenzo-p-dioxin Removal_.**

Source: https://pubs.acs.org/doi/10.1021/acs.est.4c11857

Evidence architecture:
- bottom-up defined synthetic consortium;
- identified released catechol/intermediates;
- recipient use of cytotoxic metabolite;
- siderophore secretion and increased iron availability;
- transcriptional responses for catabolism and siderophore synthesis/transport;
- improved consortium function.

Published claim pattern:
- authors state that a mutualistic metabolic cross-feeding relationship is established from the reciprocal metabolite/siderophore exchange package.

PR-CAL prediction:
- `D/S` for reciprocal cross-feeding relationship at consortium level;
- no need to downgrade the entire mechanism because each individual molecular exchange is not tracked continuously in real time.

**Result: PASS.** PR-CAL permits strong positive mechanism language for a defined, experimentally resolved reciprocal exchange package.

### H4 — Environmental Science & Technology
**Magnetite Alters the Metabolic Interaction between Methanogens and Sulfate-Reducing Bacteria (2023).**

Source: https://pubs.acs.org/doi/10.1021/acs.est.3c05948

Evidence architecture:
- magnetite perturbation;
- methane/H2S and VFA process responses;
- genome-centric metagenomics;
- methanogenic-group-specific abundance changes;
- positive correlations between candidate syntrophic partners.

Published claim pattern:
- competition/cooperation between methanogens and sulfate reducers is stated positively;
- specific DIET-based interactions are introduced as suggested by correlation/community evidence, while the concluding synthesis uses stronger `fostering DIET-based syntrophic interactions` language.

PR-CAL prediction:
- `M`: strong for altered metabolic interaction and magnetite-associated syntrophy;
- `Q/S` for exact DIET partner route because the route is not isolated by a direct incapacity/flux test.

**Result: PASS.** PR-CAL reproduces the paper's internal layer separation instead of forcing either full agnosticism or unqualified DIET proof.

### H5 — Water Research
**Electric syntrophy-driven modulation of Fe0-dependent microbial denitrification (2025).**

Source: https://www.sciencedirect.com/science/article/pii/S004313542401621X

Evidence architecture:
- model consortium of Shewanella oneidensis and Pseudomonas aeruginosa;
- Fe0-dependent denitrification;
- explicit electron-transfer system between Fe0, the electroactive donor and denitrifier;
- membrane-bound CymA–OmcA–MtrC complexes linked to electron generation/transfer/consumption;
- electron-donor contribution analysis and downstream denitrification responses.

Published claim pattern:
- authors report a previously unidentified Fe0-dependent denitrification mode driven by electro-syntrophic interaction;
- recipient electron acceptance and protein-complex role are stated positively.

PR-CAL prediction:
- `D/S` for existence of the electro-syntrophic system and electron-dependent functional coupling;
- exact molecular causality should track the strength of the protein-complex perturbation evidence rather than being automatically downgraded because electrons are not individually traced between every cell.

**Result: PASS.** The global envelope appropriately allows strong mechanism-level wording for a defined functional electron-transfer system.

### H6 — Water Research
**Interspecies cooperation-driven photogenerated electron transfer processes and efficient multi-pathway nitrogen removal in the g-C3N4-anammox consortia biohybrid system (2024).**

Source: https://www.sciencedirect.com/science/article/pii/S0043135424004342

Evidence architecture:
- photocatalyst–microbial biohybrid system;
- community-resolved functional analysis;
- cytochrome c/flavin carrier attribution to associated bacteria;
- regulatory/electron-transfer proteins;
- carbon-fixation pathway reconstruction;
- nitrogen-removal performance.

Published claim pattern:
- interspecies photogenerated-electron cooperation is described as deciphered;
- anammox bacteria are identified as the primary photogenerated-electron sink;
- associated bacteria are stated to provide key extracellular carriers;
- pathway-level mechanistic interpretation is strongly affirmative.

PR-CAL prediction:
- `S` for the integrated photogenerated-electron cooperation mechanism when supported by convergent functional and molecular evidence;
- any exact species-resolved electron flux quantity would remain outside the claim unless directly measured.

**Result: PASS.** This is a strong holdout against excessive conservatism: Water Research accepts mechanism-level electron-transfer attribution from a multi-evidence package without requiring single-electron tracking.

### H7 — Nature Communications
**Electron shuttling promotes denitrification and mitigates nitrous oxide emissions in lakes (2025).**

Source: https://www.nature.com/articles/s41467-025-63601-0

Evidence architecture:
- field investigation;
- laboratory 15N isotope experiments;
- humic-substance manipulation;
- outer-membrane c-type cytochrome response;
- denitrification/N2O outcome;
- ecological context dependence on native humic-substance levels.

Published claim pattern:
- authors use reveal/enhances/mitigates-level language for HS-mediated electron shuttling and denitrification;
- environmental context is retained as a boundary rather than nullifying the mechanism.

PR-CAL prediction:
- `D/S` for the experimentally perturbed system-level effect;
- narrower molecular exclusivity remains bounded if cytochrome involvement is not the only possible pathway.

**Result: PASS.** Strong system-level language is appropriate with isotope + perturbation + molecular convergence.

### H8 — Nature Communications
**Cable bacteria with electric connection to oxygen attract flocks of diverse bacteria (2023).**

Source: https://www.nature.com/articles/s41467-023-37272-8

Evidence architecture:
- direct observation of bacterial flocking around cable bacteria;
- laser disruption of the cable's oxygen connection causing immediate dispersal;
- Raman redox-state measurements showing stronger oxidation near cable bacteria;
- rare/brief physical contact.

Published claim pattern:
- dependence of flocking on the cable-bacteria oxygen connection is reported strongly;
- the actual electron-transfer route is kept qualified: observations suggest potential transfer through unidentified soluble intermediates.

PR-CAL prediction:
- `D` for connection-dependent flocking/redox association;
- `Q` for the exact soluble electron-transfer mechanism.

**Result: PASS.** This is a clean mixed-layer case: a strong causal perturbation at one layer coexists with explicitly qualified route identity.

## Aggregate result

**8/8 PASS.**

The holdout set supports the current PR-CAL architecture:

1. published papers often make strong positive claims at the phenomenon/system/mechanism layer when multiple functional evidence streams converge;
2. the same papers frequently retain caution only at the narrower route, species, exclusivity or exact-flux layer;
3. direct incapacity/genetic/physical perturbation controls justify `show/demonstrate/establish`-level wording for the layer they isolate;
4. community/process + omics/metabolite evidence can justify `support/indicate/facilitate/drive`-level mechanism language without single-cell flux tracing;
5. a limitation is commonly written as a boundary on one layer, not as a reason to erase the entire mechanistic interpretation.

## Falsification check

No holdout paper required broadening the PR-CAL global mechanism envelope beyond the existing 64-study corpus. More importantly, none exposed a systematic false-positive tendency in which PR-CAL would license the paper's narrowest route/species/flux claim despite weaker evidence.

The most important stress cases were H4, H6 and H8:
- H4 shows strong process/syntrophy language coexisting with weaker DIET-route evidence;
- H6 shows that a high-level engineering journal accepts strong integrated electron-transfer mechanism language from convergent community/molecular evidence;
- H8 shows that even Nature Communications separates a demonstrated functional dependency from a merely suggested electron-transfer route.

## Validation boundary

This remains a small out-of-sample set, not statistical proof of universal calibration. Keep these eight papers outside the 64-study calibration corpus unless a future corpus version is rebuilt with a separate held-out set. Future PR-CAL changes should be rechecked against both the fixed holdout set and new unseen papers to reduce circular validation.