# PR-CAL target-journal empirical claim-strength corpus

**Corpus version:** v1.0  
**Sample count:** 64 experimental studies  
**Journal balance:** 16 The ISME Journal; 16 Environmental Science & Technology; 16 Water Research; 16 Nature Portfolio comparators (15 Nature Communications + 1 Nature Microbiology).

## Purpose

This corpus is a calibration library for `PR-CAL`. It is not a list of papers to imitate. It records how comparable experimental papers convert different evidence architectures into published claim strength.

The operative question is:

> Given an evidence package similar to the manuscript under review, what level of scientific claim is routinely accepted in the target journal while preserving narrower unresolved boundaries?

The bar is therefore empirical and evidence-architecture matched. It is not set by the boldest paper, by the most cautious paper, or by a generic model preference for hedging.

## Coding

Evidence architecture codes are compact descriptors rather than statistical weights.

- `COC`: defined coculture or synthetic consortium
- `PROC`: reactor/process performance
- `PERT`: selective perturbation or intervention
- `GEN`: genetic manipulation
- `ISO`: isotope tracing / SIP
- `OM`: omics
- `ELEC`: electrochemistry / measured current
- `CHEM`: metabolites / biochemical measurements
- `IMG`: microscopy / spatial evidence
- `MAT`: material-property characterization
- `MODEL`: mechanistic/model support
- `ENV`: field/environmental observations
- `SC`: single-cell evidence
- `PROT`: proteomics
- other labels are self-explanatory extensions

Published claim bands:

- `D` — **direct/high-strength**: the paper uses show/demonstrate/establish/confirm-level language for the coded claim layer because the key proposition is directly isolated or strongly intervened on.
- `S` — **strong convergent**: supports/indicates/promotes/facilitates/drives-level mechanism language is used from convergent functional, molecular, chemical or perturbation evidence.
- `Q` — **qualified**: suggests/proposes/could/may/potential-level interpretation because important alternatives or route details remain unresolved.
- `M` — **mixed-layer**: the paper is strong for one layer (phenomenon/system function) while deliberately qualifying a narrower route, species attribution, or exact mechanism.

## Corpus

| ID | Journal | Year | Study | Evidence architecture | Claim band | Published calibration pattern |
|---|---|---:|---|---|:---:|---|
| I01 | The ISME Journal | 2022 | [Light-driven carbon dioxide reduction to methane by Methanosarcina barkeri in an electric syntrophic coculture](https://academic.oup.com/ismej/article/16/2/370/7474266) | `COC+ISO+ELEC+IMG+OM+PERT` | **M** | System-level light-driven electron donation/methanogenesis stated strongly; exact direct vs shuttle route remains layered/qualified. |
| I02 | The ISME Journal | 2015 | [Privatization of cooperative benefits stabilizes mutualistic cross-feeding interactions in spatially structured environments](https://academic.oup.com/ismej/article/10/6/1413/7538204) | `COC+PERT+IMG+MODEL` | **D** | Engineered reciprocal cross-feeding and spatial manipulation support direct mechanism claims; ecological generality remains broader inference. |
| I03 | The ISME Journal | 2017 | [Microbial mutualism dynamics governed by dose-dependent toxicity of cross-fed nutrients](https://academic.oup.com/ismej/article/11/2/337/7538044) | `COC+PERT+CHEM+MODEL` | **D** | Genetic tuning of ammonium exchange and reciprocal metabolite response allow strong causal statements about mutualism dynamics. |
| I04 | The ISME Journal | 2014 | [Fitness and stability of obligate cross-feeding interactions that emerge upon gene loss in bacteria](https://academic.oup.com/ismej/article/8/5/953/7582416) | `COC+GEN+PERT+FITNESS` | **D** | Engineered auxotrophies and competition tests support direct claims about division of metabolic labour and stability. |
| I05 | The ISME Journal | 2016 | [Segregating metabolic processes into different microbial cells accelerates the consumption of inhibitory substrates](https://academic.oup.com/ismej/article/10/7/1568/7538207) | `COC+PERT+CHEM+MODEL` | **D** | Experimentally varied cross-feeding architecture supports demonstrate-level claims about substrate consumption and inhibition. |
| I06 | The ISME Journal | 2016 | [A stable genetic polymorphism underpinning microbial syntrophy](https://academic.oup.com/ismej/article/10/12/2844/7538087) | `COC+GEN+PERT+PHYS` | **D** | Genotype-specific syntrophy and energetic physiology support a direct genetic-basis claim. |
| I07 | The ISME Journal | 2018 | [Syntrophic pathways for microbial mercury methylation](https://academic.oup.com/ismej/article/12/7/1826/7475495) | `COC+CHEM+THERMO` | **M** | Enhanced methylation under defined syntrophies is shown; extrapolation to major environmental source is proposed/likely. |
| I08 | The ISME Journal | 2018 | [Metabolite toxicity slows local diversity loss during expansion of a microbial cross-feeding community](https://academic.oup.com/ismej/article/12/1/136/7501454) | `COC+PERT+IMG+MODEL` | **D** | Direct experimental manipulation of metabolite toxicity supports demonstrate-level ecological mechanism claims. |
| I09 | The ISME Journal | 2018 | [Cross-feeding modulates antibiotic tolerance in bacterial communities](https://academic.oup.com/ismej/article/12/11/2723/7475398) | `COC+PERT+MIC` | **S** | Cross-feeding dependence and antibiotic-response experiments support mechanism-level effects; exact generality remains bounded. |
| I10 | The ISME Journal | 2021 | [Flow-through stable isotope probing (Flow-SIP) minimizes cross-feeding in complex microbial communities](https://academic.oup.com/ismej/article/15/1/348/7474396) | `ISO+PERT+COMMUNITY` | **D** | Method intervention directly demonstrates reduced cross-feeding relative to conventional SIP in tested systems. |
| I11 | The ISME Journal | 2022 | [In vitro interaction network of a synthetic gut bacterial community](https://academic.oup.com/ismej/article/16/4/1095/7474305) | `COC+METABOLOMICS+MODEL` | **M** | Pairwise/community experiments demonstrate interaction patterns; metabolic-network explanations are supported rather than fully causal. |
| I12 | The ISME Journal | 2022 | [Sulfate differentially stimulates but is not respired by diverse anaerobic methanotrophic archaea](https://academic.oup.com/ismej/article/16/1/168/7474152) | `ENRICH+PERT+ISO/ACTIVITY+OM` | **M** | Physiological response to sulfate is directly observed; syntrophy mechanism differences remain partly unresolved. |
| I13 | The ISME Journal | 2015 | [Methane-fed microbial microcosms show differential community dynamics and pinpoint taxa involved in communal response](https://academic.oup.com/ismej/article/9/5/1119/7558022) | `MICROCOSM+OM+ENV` | **S** | Community convergence and taxon dynamics support cooperative carbon-sharing interpretation but stop short of a unique exchanged metabolite. |
| I14 | The ISME Journal | 2016 | [Identification of syntrophic acetate-oxidizing bacteria in anaerobic digesters by combined protein-based stable isotope probing and metagenomics](https://academic.oup.com/ismej/article/10/10/2405/7538079) | `PROT-SIP+OM+COMMUNITY` | **M** | Active acetate users are identified; candidate SAO identity/pathway is phrased as possible where function is not isolated. |
| I15 | The ISME Journal | 2024 | [Emergent antibiotic persistence in a spatially structured synthetic microbial mutualism](https://academic.oup.com/ismej/article/18/1/wrae075/7660941) | `COC+PERT+IMG+TIME` | **D** | Spatially resolved perturbation supports a direct emergent-mechanism conclusion. |
| I16 | The ISME Journal | 2016 | [Peat: home to novel syntrophic species that feed acetate- and hydrogen-scavenging methanogens](https://academic.oup.com/ismej/article/10/8/1954/7538281) | `MICROCOSM+SUBSTRATE+OM` | **S** | Substrate turnover and community evidence support syntrophic-consortium interpretation; exact partner flux remains bounded. |
| E01 | Environmental Science & Technology | 2020 | [Methanobacterium Capable of Direct Interspecies Electron Transfer](https://pubs.acs.org/doi/10.1021/acs.est.0c05525) | `COC+PERT+IMG+GAC` | **D** | Defined coculture and inability/compatibility controls justify direct DIET capability claims. |
| E02 | Environmental Science & Technology | 2023 | [Enhanced Anaerobic Wastewater Treatment by a Binary Electroactive Material: Pseudocapacitance/Conductance-Mediated Microbial Interspecies Electron Transfer](https://pubs.acs.org/doi/10.1021/acs.est.3c01986) | `PROC+MAT+REDOX+ENERGY+COMMUNITY` | **S** | Material properties plus NADH/cofactor/process convergence support establish/direct-electron-routing language at reactor level. |
| E03 | Environmental Science & Technology | 2018 | [Biochar Modulates Methanogenesis through Electron Syntrophy of Microorganisms with Ethanol as a Substrate](https://pubs.acs.org/doi/10.1021/acs.est.8b04121) | `PROC+MAT+ELEC+qPCR+COMMUNITY` | **S** | Authors state biochar stimulates methanogenesis by facilitating DIET from convergent material/process/community evidence. |
| E04 | Environmental Science & Technology | 2024 | [Quorum Sensing Enhances Direct Interspecies Electron Transfer in Anaerobic Methane Production](https://pubs.acs.org/doi/10.1021/acs.est.3c08503) | `PROC+OM+ENERGY+COMMUNITY` | **S** | Stronger DIET is explicitly supported by expression and process evidence; energy explanation retains probabilistic wording. |
| E05 | Environmental Science & Technology | 2023 | [Metabolite Cross-Feeding Promoting NADH Production and Electron Transfer during Efficient SMX Biodegradation by a Denitrifier and Shewanella oneidensis MR-1](https://pubs.acs.org/doi/10.1021/acs.est.2c09341) | `COC+PROT+CHEM+CHEMOTAXIS+VALIDATION` | **D** | Identified metabolite exchanges plus validation coculture support direct cross-feeding-mechanism language. |
| E06 | Environmental Science & Technology | 2018 | [Magnetite Triggering Enhanced Direct Interspecies Electron Transfer: A Scavenger for the Blockage of Electron Transfer in Anaerobic Digestion of High-Solids Sewage Sludge](https://pubs.acs.org/doi/10.1021/acs.est.8b00891) | `PROC+ISO+SUBSTRATE+OM+ENZYME` | **S** | Combined isotope, pathway substrates and metatranscriptomics are described as jointly proving/enhancing DIET at system level. |
| E07 | Environmental Science & Technology | 2021 | [Genome-Centric Metatranscriptomics Analysis Reveals the Role of Hydrochar in Anaerobic Digestion of Waste Activated Sludge](https://pubs.acs.org/doi/10.1021/acs.est.1c01995) | `PROC+MAG+OM+PATHWAY` | **Q** | Genome-resolved expression supports a DIET interpretation; wording remains 'suggesting' for partner electron exchange. |
| E08 | Environmental Science & Technology | 2019 | [Biochar-Mediated Anaerobic Oxidation of Methane](https://pubs.acs.org/doi/10.1021/acs.est.9b01345) | `ENRICH+PERT+CH4/CO2+COMMUNITY` | **M** | Biochar-stimulated AOM is shown directly; environmental mitigation mechanism is presented as an additional plausible mechanism. |
| E09 | Environmental Science & Technology | 2020 | [Hydrochar-Facilitated Anaerobic Digestion: Evidence for Direct Interspecies Electron Transfer Mediated through Surface Oxygen-Containing Functional Groups](https://pubs.acs.org/doi/10.1021/acs.est.0c00112) | `PROC+SUBSTRATE+PROT+MAT` | **Q** | Hydrochar response and proteomics support DIET as a plausible cause rather than unequivocal proof. |
| E10 | Environmental Science & Technology | 2020 | [Enhanced Current Production by Exogenous Electron Mediators via Synergy of Promoting Biofilm Formation and the Electron Shuttling Process](https://pubs.acs.org/doi/10.1021/acs.est.0c00141) | `BES+PERT+BIOFILM+ELEC` | **D** | Mediator addition and electrochemical/biofilm measurements support direct synergy claims. |
| E11 | Environmental Science & Technology | 2012 | [Soluble Electron Shuttles Can Mediate Energy Taxis toward Insoluble Electron Acceptors](https://pubs.acs.org/doi/10.1021/es204302w) | `PERT+CHEM+MODEL+MOTILITY` | **S** | Experiments plus model are presented to support the proposed riboflavin-mediated energy-taxis mechanism. |
| E12 | Environmental Science & Technology | 2017 | [Enhancing Extracellular Electron Transfer of Shewanella oneidensis MR-1 through Coupling Improved Flavin Synthesis and Metal-Reducing Conduit for Pollutant Degradation](https://pubs.acs.org/doi/10.1021/acs.est.6b04640) | `GEN+ELEC+POLLUTANT` | **D** | Targeted genetic engineering with electrochemical response supports direct causal enhancement of EET. |
| E13 | Environmental Science & Technology | 2023 | [Conductive Materials on Biocathodes Altered the Electron-Transfer Paths and Modulated γ-HCH Dechlorination and CH4 Production in Microbial Electrochemical Systems](https://pubs.acs.org/doi/10.1021/acs.est.2c06097) | `BES+MAT+PROC+COMMUNITY` | **S** | Contrasting conductive/anti-conductive treatments support electron-partition/pathway claims at system level. |
| E14 | Environmental Science & Technology | 2019 | [Diffusion-Based Recycling of Flavins Allows Shewanella oneidensis MR-1 To Yield Energy from Metal Reduction Across Physical Separations](https://pubs.acs.org/doi/10.1021/acs.est.8b04718) | `MICROFLUIDIC+SEPARATION+FLUX+ENERGY` | **D** | Physical separation and real-time flux directly establish long-range flavin-mediated electron transfer and recycling. |
| E15 | Environmental Science & Technology | 2023 | [Novel Role of Hematite in Anaerobic Digestion: Manipulating Membrane-Bound Electron Transport Chain by the Construction of Biological Capacitors with Humic Acid](https://pubs.acs.org/doi/10.1021/acs.est.3c01867) | `PROC+MAT+ELECTRON-BALANCE+COMMUNITY` | **S** | Electron partition and mineral comparisons support capacitor-mediated methanogenesis mechanism claims. |
| E16 | Environmental Science & Technology | 2026 | [Visualizing Microbial Indirect Extracellular Electron Transfer](https://pubs.acs.org/doi/10.1021/acs.est.6c00304) | `SPATIAL+ELECTRON-TRAP+PERT` | **D** | Direct spatial visualization supports demonstrate-level centimeter-scale IEET claims. |
| W01 | Water Research | 2024 | [Zero-valent iron enhanced methane production of anaerobic digestion by reinforcing microbial electron bifurcation coupled with direct inter-species electron transfer](https://www.sciencedirect.com/science/article/pii/S0043135424003300) | `PROC+MAT+ENZYME+ENERGY+COMMUNITY` | **Q** | Authors frame EB-coupled DIET as a potential micro-energetic strategy while strongly reporting process enhancement. |
| W02 | Water Research | 2023 | [Long-term transformation of nanoscale zero-valent iron explains its biological effects in anaerobic digestion: From ferroptosis-like death to magnetite-enhanced direct electron transfer networks](https://www.sciencedirect.com/science/article/pii/S0043135423005511) | `LONGTERM+MAT+CELL-DEATH+COMMUNITY` | **S** | Time-resolved material transformation and biological responses support magnetite-enhanced DIET cooperation. |
| W03 | Water Research | 2019 | [Response of syntrophic aggregates to the magnetite loss in continuous anaerobic bioreactor](https://www.sciencedirect.com/science/article/pii/S0043135419306992) | `CONTINUOUS+PERT+EPS+COMMUNITY` | **S** | Magnetite addition/loss and aggregate conductivity support DIET-favoring interpretation. |
| W04 | Water Research | 2020 | [Direct interspecies electron transfer can be suppressed under ammonia-stressed condition – Reevaluate the role of conductive materials](https://www.sciencedirect.com/science/article/pii/S004313542030631X) | `PROC+STRESS+MAT+PATHWAY` | **S** | Stress-dependent divergence is used to argue DIET formation is conditionally suppressed, not universally promoted by conductors. |
| W05 | Water Research | 2024 | [Neglected role of iron redox cycle in direct interspecies electron transfer in anaerobic methanogenesis: Inspired from biogeochemical processes](https://www.sciencedirect.com/science/article/pii/S004313542401025X) | `PROC+IRON-REDOX+CAPACITANCE+OM` | **M** | Pathway redirection to robust DIET is strongly claimed; exact conductive matrix composition is explicitly conjectured. |
| W06 | Water Research | 2024 | [Magnetite encapsulated in carbon shell particles to boost anaerobic methanogenesis of chloramphenicol wastewater](https://www.sciencedirect.com/science/article/pii/S0043135424010212) | `PROC+MAT+COMMUNITY+PATHWAY` | **S** | Material treatment is stated to strengthen hydrogenotrophic methanogenesis and DIET processes. |
| W07 | Water Research | 2024 | [Enhancing proton-coupled electron transfer drives efficient methanogenesis in anaerobic digestion](https://www.sciencedirect.com/science/article/pii/S0043135424012302) | `PROC+ENERGY+SYNTHROPHY+PERT` | **S** | Integrated energetic evidence supports an identified PCET principle driving methanogenesis. |
| W08 | Water Research | 2024 | [Insights into feasibility and microbial characterizations on simultaneous elimination of dissolved methane and nitrate/nitrite reduction with magnetite](https://www.sciencedirect.com/science/article/pii/S004313542400469X) | `PROC+CH4+N+MAT+COMMUNITY` | **S** | Coupled AOM-denitrification and magnetite-facilitated syntrophic electron exchange are stated as occurred/facilitated. |
| W09 | Water Research | 2026 | [Electrical stimulation-induced π-π stacking drives sludge humification to enhance direct interspecies electron transfer and methanogenesis](https://www.sciencedirect.com/science/article/pii/S0043135426003787) | `E-STIM+HUMICS+DFT+PROC` | **S** | Field-induced conductive-network formation is used to support enhanced DIET/methanogenesis mechanism. |
| W10 | Water Research | 2025 | [A novel strategy for high efficiency anaerobic digestion of waste activated sludge using Fe-Cu microelectrolysis: performance, electron transfer, key enzymes and microbial community](https://www.sciencedirect.com/science/article/pii/S004313542501228X) | `PROC+MICROCURRENT+ENZYME+COMMUNITY` | **S** | Fe-Cu is reported to combine microcurrent stimulation and DIET with multi-layer functional evidence. |
| W11 | Water Research | 2024 | [Magnetite-mediated shifts in denitrifying consortia in bioelectrochemical system: Insights into species selection and metabolic dynamics](https://www.sciencedirect.com/science/article/pii/S0043135424010315) | `BES+MAT+OM+COMMUNITY` | **S** | Magnetite is stated to enhance interspecies cooperation and consortium functionalization from species/metabolic evidence. |
| W12 | Water Research | 2023 | [Potential bacterial isolation by dosing metabolites in cross-feedings](https://www.sciencedirect.com/science/article/pii/S0043135423000258) | `METABOLITE-ADD+ANAMMOX+GROWTH` | **M** | Specific folate/gluconate support is inferred from symbiont/metabolite rescue; broader isolation strategy remains proposed. |
| W13 | Water Research | 2026 | [Biomass ratio regulates methane conversion and carbon fixation in a methanotrophs-microalgae symbiotic system](https://www.sciencedirect.com/science/article/pii/S0043135425019190) | `COC+RATIO-PERT+CLSM+CARBON-FLOW` | **S** | Biomass-ratio intervention and aggregation/carbon-flow data support co-metabolism mechanism claims. |
| W14 | Water Research | 2022 | [A novel green composite conductive material enhancing anaerobic digestion of waste activated sludge via improving electron transfer and metabolic activity](https://www.sciencedirect.com/science/article/pii/S0043135422006406) | `PROC+MAT+ETS+ENZYME+COMMUNITY` | **S** | Intra/extracellular ET and DIET enhancement are stated directly from convergent process/biochemical/community data. |
| W15 | Water Research | 2024 | [Material and microbial perspectives on understanding the role of biochar in mitigating ammonia inhibition during anaerobic digestion](https://www.sciencedirect.com/science/article/pii/S0043135424004056) | `PROC+MAT+EPS+OM` | **S** | Biochar is stated to facilitate DIET, evidenced by material, guild and metatranscriptomic responses. |
| W16 | Water Research | 2011 | [A sustainable, carbon neutral methane oxidation by a partnership of methane oxidizing communities and microalgae](https://www.sciencedirect.com/science/article/pii/S0043135411001163) | `COC+PROC+O2-BALANCE+BIOMASS` | **S** | Coculture performance supports a functional partnership claim while detailed exchanged currencies remain less resolved. |
| N01 | Nature Communications | 2013 | [Characterization and modelling of interspecies electron transfer mechanisms and microbial community dynamics of a syntrophic association](https://www.nature.com/articles/ncomms3809) | `COC+OM+MODEL+PHYS` | **S** | Multi-omic/model convergence supports mechanistic electron-flow interpretation without treating modeling alone as direct proof. |
| N02 | Nature Communications | 2022 | [Design of stable and self-regulated microbial consortia for chemical synthesis](https://www.nature.com/articles/s41467-022-29215-6) | `ENGINEERED-COC+MULTI-CROSSFEED+BIOSENSOR` | **D** | Designed metabolite dependencies and feedback control support direct design-rule claims. |
| N03 | Nature Communications | 2016 | [Conventional methanotrophs are responsible for atmospheric methane oxidation in paddy soils](https://www.nature.com/articles/ncomms11728) | `ENV+SIP+COMMUNITY+FUNCTION` | **D** | Stable-isotope/function evidence supports strong attribution of atmospheric methane oxidation to conventional methanotrophs. |
| N04 | Nature Communications | 2017 | [Syntrophic anaerobic photosynthesis via direct interspecies electron transfer](https://www.nature.com/articles/ncomms13924) | `COC+ELECTRODE+LIGHT+MUTANT` | **D** | Defined coculture plus donor electron-transfer mutant/electrode controls justify a named DIET-driven metabolism. |
| N05 | Nature Communications | 2019 | [Phototrophic extracellular electron uptake is linked to carbon dioxide fixation in Rhodopseudomonas palustris](https://www.nature.com/articles/s41467-019-09377-6) | `ELEC+REDOX+OM+13CO2+RUBISCO-MUTANT` | **D** | Genetic perturbation causing ~90% EEU loss supports show-level linkage and primary electron-sink attribution. |
| N06 | Nature Communications | 2023 | [Stress-induced metabolic exchanges between complementary bacterial types underly a dynamic mechanism of inter-species stress resistance](https://www.nature.com/articles/s41467-023-38913-8) | `COC+STRESS+METABOLOMICS+PHYS` | **D** | Stress-triggered excretion and reciprocal physiology support an established collaborative stress-resistance mechanism. |
| N07 | Nature Communications | 2024 | [Mechanisms of extracellular electron transfer in anaerobic methanotrophic archaea](https://www.nature.com/articles/s41467-024-45758-2) | `BES+CH4-CURRENT+OM+TEM` | **M** | Methane-dependent current is directly observed; specific protein-complex/nanowire mechanism remains suggested/possible. |
| N08 | Nature Microbiology | 2022 | [Methanotrophy by a Mycobacterium species that dominates a cave microbial ecosystem](https://www.nature.com/articles/s41564-022-01252-3) | `ENRICH+CULTURE+GENOME+PROT+13CH4` | **D** | Growth plus 13CH4 incorporation confirm methane as sole carbon/energy source and extend methanotrophy phylogeny. |
| N09 | Nature Communications | 2015 | [Nutritional stress induces exchange of cell material and energetic coupling between bacterial species](https://www.nature.com/articles/ncomms7283) | `COC+CONTACT+STRESS+ENERGY` | **D** | Physical interaction and physiological measurements support direct emergent energetic-coupling claims. |
| N10 | Nature Communications | 2024 | [Enhanced metabolic entanglement emerges during the evolution of an interkingdom microbial community](https://www.nature.com/articles/s41467-024-51702-1) | `EVOLUTION+COC+CROSSFEED+PHYS` | **S** | Serial evolution and dependency changes support increased metabolic entanglement; specific exchanged routes are layer-specific. |
| N11 | Nature Communications | 2024 | [Electrochemically coupled CH4 and CO2 consumption driven by microbial processes](https://www.nature.com/articles/s41467-024-47445-8) | `MICROCOSM+IRON-REDOX+ELEC+OM` | **S** | Mineral-mediated coupling and electron flow are stated strongly at system level; energy metabolism is predicted at genetic level. |
| N12 | Nature Communications | 2020 | [Genomic and enzymatic evidence of acetogenesis by anaerobic methanotrophic archaea](https://www.nature.com/articles/s41467-020-17860-8) | `HIGH-P+13C+GENOME+ENZYME` | **D** | 13C methane-to-acetate plus enzyme activity justify direct acetogenic-capacity claims. |
| N13 | Nature Communications | 2024 | [Metabolic coupling between soil aerobic methanotrophs and denitrifiers in rice paddy fields](https://www.nature.com/articles/s41467-024-47827-y) | `FIELD+13CH4-DNA-SIP+FUNCTION+GENES` | **S** | Field correlations plus SIP support coupling between aerobic methane oxidation and denitrification; precise metabolite currency remains broader inference. |
| N14 | Nature Communications | 2024 | [Persistent activity of aerobic methane-oxidizing bacteria in anoxic lake waters due to metabolic versatility](https://www.nature.com/articles/s41467-024-49602-5) | `RATE+NANOSIMS+OM+ENV` | **D** | Single-cell isotope and multi-omics link anoxic methane oxidation activity to Methylococcales with strong functional attribution. |
| N15 | Nature Communications | 2018 | [A biochemical framework for anaerobic oxidation of methane driven by Fe(III)-dependent respiration](https://www.nature.com/articles/s41467-018-04097-9) | `BIOCHEM+ENRICH+RESPIRATION+MODEL` | **M** | Biochemical evidence supports an Fe(III)-respiration framework; broader pathway model remains framework-level rather than fully isolated. |
| N16 | Nature Communications | 2017 | [Electricity from methane by reversing methanogenesis](https://www.nature.com/articles/ncomms15419) | `ENGINEERED-CONSORTIUM+MFC+SHUTTLE-REPLACEMENT+PROC` | **D** | Constructed consortium and component substitutions support direct methane-to-electricity functional claims. |

## Corpus-level observations

Across this v1.0 corpus:

- 24/64 samples fall in the direct/high-strength band (`D`).
- 27/64 fall in strong convergent mechanism language (`S`).
- 10/64 are explicitly mixed-layer (`M`): strong at the phenomenon/system level while narrower route or species claims remain qualified.
- 3/64 are primarily qualified (`Q`) for the focal mechanistic layer.

The distribution itself is **not** a target proportion for manuscripts. It shows that high-impact environmental microbiology and engineering journals routinely publish strong positive mechanism language when the evidence architecture warrants it, while simultaneously preserving narrower unresolved boundaries.

## Retrieval rule for manuscript review

Do not average all 64 papers. For each disputed central claim:

1. identify the claim layer: phenomenon, system-level function, mechanism, route identity, species attribution, or exact flux/causal step;
2. encode the manuscript evidence architecture;
3. retrieve the closest empirical neighbors, prioritizing:
   - same target journal;
   - similar biological/engineering system;
   - similar intervention strength;
   - similar evidence independence;
   - similar claim layer;
4. use at least **5 close analogues** when practical for a disputed central mechanism claim, with at least **3 from the exact target journal** when suitable samples exist;
5. inspect both the strongest published layer and the narrower boundary retained by those papers;
6. set the manuscript claim corridor from the mainstream neighbor envelope, not from one outlier.

## Anti-bias rules

- A published overclaim is not permission to repeat it.
- A highly conservative paper is not a universal minimum.
- Topic similarity is weaker than evidence-architecture similarity.
- Omics abundance alone does not equal direct function.
- Repeated transformations of one assay are not independent evidence.
- A missing species-resolved or flux-resolved assay constrains the claim layer that requires it; it does not automatically erase broader system-level support.
- Genetic, inhibitor/rescue, incapacity controls, isotope tracing, physical separation and selective perturbations can legitimately move the claim corridor upward when they isolate the proposition.
- The corpus should be expanded with real misclassification cases and new target-journal papers rather than changing the evidence bar ad hoc.

## Maintenance

Maintain at least **50 active, relevant experimental samples**. The preferred baseline is 60+ so that removal of weak or outdated analogues does not collapse coverage.

When adding samples, record:
- journal/year;
- evidence architecture;
- focal claim layer;
- published claim strength;
- narrower boundary retained;
- why the sample is transferable to PR-CAL.

When a real manuscript review produces a disputed calibration decision, add that case to Workbench regression validation if it reveals a reusable failure mode.
