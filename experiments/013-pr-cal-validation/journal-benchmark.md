# Target-journal claim-strength benchmark for PR-CAL

This benchmark calibrates PR-CAL against published experimental writing in journals relevant to environmental microbiology and engineering. The purpose is not to copy the boldest wording from any one article, but to infer the mainstream accepted claim-strength envelope for comparable evidence architectures.

## Benchmark cohort

### The ISME Journal

1. Huang et al. (2022), *Light-driven carbon dioxide reduction to methane by Methanosarcina barkeri in an electric syntrophic coculture*.
   - Evidence architecture: defined coculture, light dependence, monoculture/heat-killed controls, 13C-bicarbonate to methane, electrochemistry, physical separation, FISH, transcriptomics/redox mediator analyses.
   - Wording pattern: strong system-level statements (`demonstrate` / direct functional role) coexist with more bounded route-specific wording (`suggesting direct interspecies electron transfer`, `possibility of indirect interspecies electron transfer`).
   - Calibration lesson: direct process evidence can justify strong system-level wording even when a narrower route remains qualified.

2. *Single-cell assembled genomes predict enhanced bacterial metabolic cross-feeding potential in carbon-enriched soils* (ISME J, 2026).
   - Evidence architecture: model predictions plus coculture and metabolomics.
   - Wording pattern: model-only predictions are explicitly not treated as direct evidence; experimental consistency is used to `support the hypothesis`, while further in situ validation remains necessary.
   - Calibration lesson: distinguish model-supported mechanism from experimentally observed interaction; do not collapse all layers to the weakest wording.

### Environmental Science & Technology

3. *Quorum Sensing Enhances Direct Interspecies Electron Transfer in Anaerobic Methane Production* (2024).
   - Evidence architecture: long-term process performance, conductive-pili/cytochrome gene expression, ATPase expression, functional-guild enrichment, carbon-reduction/alcohol-dehydrogenation genes.
   - Wording pattern: stronger DIET is described as being `supported by` convergent molecular and community evidence; the integrated study `indicates` positive effects on DIET.
   - Calibration lesson: ES&T accepts bounded mechanism-level inference from convergent process + molecular evidence without requiring direct electron-by-electron tracing.

4. *Enhanced Anaerobic Wastewater Treatment by a Binary Electroactive Material: Pseudocapacitance/Conductance-Mediated Microbial Interspecies Electron Transfer* (2023).
   - Evidence architecture: material conductance/pseudocapacitance, NADH/NAD+ response, ATP/cofactor response, methane performance and community-scale mechanistic interpretation.
   - Wording pattern: the material is described as helping establish DIET and directing electrons to methanogens.
   - Calibration lesson: engineering journals may use stronger mechanism verbs when material properties, process response and biological readouts converge; PR-CAL should not automatically downgrade such claims to `speculative` solely because single-cell flux was not measured.

### Water Research

5. Zheng et al. (2021), *Desulfovibrio feeding Methanobacterium with electrons in conductive methanogenic aggregates from coastal zones*.
   - Evidence architecture: metagenomics, metatranscriptomics, electroactive aggregates, isolate conductivity, defined coculture tests and comparison with an H2/formate-incompetent methanogen.
   - Wording pattern: direct transfer to Methanothrix is stated strongly where the control permits it, while Methanobacterium is phrased as `might directly accept electrons`.
   - Calibration lesson: wording is calibrated to partner-specific evidence depth within the same study rather than applying one conservative level to the whole mechanism.

6. *A novel green composite conductive material enhancing anaerobic digestion of waste activated sludge via improving electron transfer and metabolic activity* (2022).
   - Evidence architecture: VFA/methane response, electron-transfer-system activity, hydrogenase, Cyt-C, sludge electron-transfer capacity, enzyme activity and microbial community.
   - Wording pattern: authors state that the material enhanced intracellular electron transfer and changed the extracellular pathway from IHT to DIET, while some downstream responsibility statements remain conditional.
   - Calibration lesson: WR commonly permits a mechanism-level conclusion from convergent functional and biochemical evidence even without direct species-resolved electron flux.

7. *Material and microbial perspectives on understanding the role of biochar in mitigating ammonia inhibition during anaerobic digestion* (2024).
   - Evidence architecture: performance, material characteristics, EPS, electroactive-guild abundance and metatranscriptomic pili/cytochrome genes.
   - Wording pattern: biochar is stated to promote/facilitate DIET, with the mechanism explicitly described as `evidenced by` convergent observations.
   - Calibration lesson: `promotes/facilitates` is an accepted mechanism-level verb when multiple independent functional and molecular indicators align.

### Nature-family comparator

8. Guzman et al. (2019), *Phototrophic extracellular electron uptake is linked to carbon dioxide fixation in Rhodopseudomonas palustris*, Nature Communications.
   - Evidence architecture: bioelectrochemistry, intracellular redox measurements, transcriptomics, 13CO2 incorporation and RuBisCO double-mutant perturbation.
   - Wording pattern: `show` and `demonstrate` are used for EEU–CO2-fixation linkage and major electron-sink attribution because orthogonal evidence includes a strong genetic perturbation.
   - Calibration lesson: strong causal/mechanistic verbs are appropriate when an intervention directly disrupts the proposed pathway.

9. Ha et al. (2017), *Syntrophic anaerobic photosynthesis via direct interspecies electron transfer*, Nature Communications.
   - Evidence architecture: defined coculture, growth dependence, electrode electron uptake, light dependence and a donor mutant defective in a required electron-transfer complex.
   - Wording pattern: the authors state that photoautotrophy can be driven by DIET and name the new metabolism.
   - Calibration lesson: a mechanistically isolating mutant/control allows high-strength wording and illustrates the upper end of the journal-calibrated corridor.

## Cross-journal empirical rules

The cohort supports the following calibration rules:

1. **Calibrate by evidence architecture, not by one missing assay.** A system-level mechanism can be strongly supported by convergent process, perturbation, molecular and physiological evidence even when a narrower species/flux step is unresolved.
2. **Calibrate each layer separately.** The observed phenomenon, system-level mechanism, route identity, species attribution and exact flux may legitimately use different verbs in the same paragraph.
3. **No single-assay veto.** Missing an ideal species-resolved or flux-resolved assay limits the narrow claim that requires it; it does not automatically invalidate broader mechanism-supported interpretation.
4. **No pseudo-triangulation.** Multiple transformations of one signal do not justify stronger language.
5. **Interventions move the bar upward.** Gene knockout, inhibitor/rescue, separation, donor/recipient incapacity controls, isotope tracing and selective perturbations justify stronger causal/mechanistic wording when they isolate the proposition.
6. **Process + molecular convergence can justify `supports`, `indicates`, `promotes`, or `facilitates`.** This is routine in ES&T and Water Research and also appears in ISME/Nature-family papers when appropriately bounded.
7. **`demonstrates` / `shows` should be attached to the layer directly established.** A paper can demonstrate a system-level functional process while only suggesting the exact interspecies route.
8. **Use the mainstream accepted envelope, not the boldest outlier.** When a target journal is known, benchmark at least several comparable papers and choose wording typical of the evidence package, with Nature-family comparators serving as a high-specificity reference rather than a universal minimum.

## Implication for PR-CAL

PR-CAL should target the strongest defensible wording that falls inside the empirical claim-strength envelope of the target journal for a comparable evidence package. It should flag both wording that exceeds this envelope and wording that falls materially below it.
