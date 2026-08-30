# Evaluation — Experiment 004

## Trigger result

**PASS**

The positive and negative cases separate correctly.

### Positive case

- Request type: design a new reusable Skill / workflow.
- Primary PR class: `PR-OPS`.
- External benchmark: triggered before design.
- Local evidence inspected first: current task-routing policy, research PR taxonomy, PR-MIX anti-abuse rule, and external-benchmark Draft PR #5.
- Result: external ideas were used only as design principles and adapted to local usage.

### Negative control

- Request type: one-time execution of existing `PR-RSCH`.
- Primary PR class: `PR-RSCH` if packaged.
- External benchmark: not triggered.
- Reason: no reusable method, Skill, routing rule, validation gate, or prompt framework changes.

## Traceable external benchmark

The positive case was checked against concrete public implementations and reviews before the local Skill design was finalized.

| Source | Concrete reference | Similar function | Decision | Local adaptation |
| --- | --- | --- | --- | --- |
| CASCADE — Cumulative Agentic Skill Creation through Autonomous Development and Evolution | GitHub: https://github.com/CederGroupHub/CASCADE ; paper: https://arxiv.org/abs/2512.23880 | Agents acquire reusable scientific skills from external tools and web/code knowledge, then accumulate and evolve those skills | **Adapt** | Keep the idea of reusable procedural knowledge and learning from external evidence, but do not allow runtime discoveries to rewrite the stable playbook automatically; promotion remains PR-reviewed and validation-gated |
| AgentAda — Skill-Adaptive Data Analytics for Tailored Insight Discovery | GitHub: https://github.com/ServiceNow/AgentAda ; paper: https://arxiv.org/abs/2504.07421 | Generates analysis questions, matches analytical skills, and produces executable analyses for insight discovery | **Adapt** | Replace automatic skill selection/execution with a recommendation-first interaction: generate 3–5 literature-supported directions, let the user choose, then produce an execution plan |
| Large Language Model-based Data Science Agent: A Survey | arXiv: https://arxiv.org/abs/2508.02744 ; TMLR/OpenReview publication: https://openreview.net/forum?id=ZT5SJQNOCS | Frames data-science agents around roles, execution, knowledge, reflection, preprocessing, modeling, evaluation, and visualization | **Adopt** | Preserve staged separation between problem understanding, analysis execution, interpretation, and validation; route those stages through the existing ChatGPT/Codex task-routing policy rather than importing a new multi-agent architecture |
| A Survey on Large Language Model-based Agents for Statistics and Data Science | https://doi.org/10.1080/00031305.2025.2561140 | Reviews planning, reasoning, reflection, collaboration, knowledge integration, and system design for data agents | **Adopt selectively** | Use it as supporting evidence that analysis planning and execution should be separated; reject extra agent orchestration unless it solves a demonstrated local problem |

### Why these references were useful

The external sources cover three different layers rather than repeating one architecture:

1. **Skill acquisition/evolution** — CASCADE.
2. **Data-analysis skill matching and question generation** — AgentAda.
3. **General data-science-agent workflow decomposition** — the survey literature.

This combination is more useful locally than copying one system wholesale because the intended Skill is not an autonomous analytics agent. Its job is to advise the user on scientifically defensible next analysis directions before execution begins.

## Adopt / Adapt / Reject summary for the positive case

### Adopt

- Separate problem understanding from execution.
- Use literature search to derive candidate analysis hypotheses/directions rather than relying only on generic statistical recipes.
- Keep explicit evidence and applicability conditions for each recommendation.
- Require a user selection gate before detailed execution planning when several scientifically plausible directions exist.
- Preserve explicit interpretation and validation stages after quantitative execution.

### Adapt

- AgentAda-style automated analysis selection is changed into a recommendation-first interaction: generate 3–5 candidate directions, then let the user choose.
- CASCADE-style skill evolution is changed into review-gated playbook evolution: successful usage can inform future updates, but runtime discoveries do not automatically rewrite the Skill.
- Data-science agent execution loops are split according to local task routing: ChatGPT handles literature synthesis and scientific framing; Codex becomes relevant only if the selected direction requires deterministic data processing, scripting, repeated execution, or reproducible validation.
- Literature similarity is judged by scientific question, experimental design, measured object, and data structure rather than merely by use of the same statistical test.

### Reject

- Automatically executing every suggested analysis before the user chooses a direction.
- Treating literature frequency or popularity as proof that a method fits the user's experimental design.
- Auto-promoting runtime-generated procedures into the stable Skill without PR review and validation.
- Copying CASCADE or AgentAda architecture wholesale when the local requirement is advisory rather than autonomous execution.
- Adding extra planner/executor/reviewer agents when the existing ChatGPT/Codex routing already covers the required separation.
- Using `PR-MIX` merely because the Skill touches literature, research interpretation, and data analysis; the Skill itself is the single authoritative changed object.

## Local-experience evidence

The adapted design addresses recurring local failure modes:

1. Scientific interpretation must consider converging evidence rather than escalate severity from one isolated signal.
2. Quantitative representation must be checked before declaring conflicts, as shown by isotope examples involving `δ13C`, `atom% 13C`, and absolute `13C excess`.
3. Recommendations should distinguish observation, interpretation, literature context, analogy, and unresolved inference.
4. The user benefits from choosing among analysis directions before computation begins, avoiding unnecessary analyses and over-automation.
5. ChatGPT/Codex routing should change only when execution and verification needs change.
6. External precedent should improve the local workflow, not override successful local practice merely because a public system is more complex or popular.

## Outcome

The automatic benchmark rule behaves as intended for its first real design task and its specified negative control.

Promotion recommendation for `codex-playbook` Draft PR #5: **validated once; suitable to promote from experimental to stable core trigger with bounded evidence scope**.

## Evidence boundary

Directly validated:

- new reusable Skill design triggers external benchmark;
- one-time existing `PR-RSCH` execution does not;
- concrete public implementations/reviews can be checked and recorded before local design;
- external patterns can be adapted without forcing a copied architecture;
- single-authoritative-object classification remains `PR-OPS`.

Not yet validated:

- every possible reusable workflow category;
- cases with no meaningful public analogue;
- cases where external convention conflicts with safety or correctness requirements;
- fully automated plugin/Skill installation behavior.
