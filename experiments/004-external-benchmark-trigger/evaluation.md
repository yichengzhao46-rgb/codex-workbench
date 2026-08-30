# Evaluation — Experiment 004

## Trigger result

**PASS**

The positive and negative cases separate correctly.

### Positive case

- Request type: design a new reusable Skill / workflow.
- Primary PR class: `PR-OPS`.
- External benchmark: triggered before design.
- Local evidence inspected first: current task-routing policy, research PR taxonomy, PR-MIX anti-abuse rule, and external-benchmark Draft PR #5.
- Public patterns reviewed: CASCADE-style skill evolution, AgentAda-style adaptive data-analysis skills, data-science agent survey patterns, and public agent/workflow repositories.
- Result: external ideas were used only as design principles and adapted to local usage.

### Negative control

- Request type: one-time execution of existing `PR-RSCH`.
- Primary PR class: `PR-RSCH` if packaged.
- External benchmark: not triggered.
- Reason: no reusable method, Skill, routing rule, validation gate, or prompt framework changes.

## Adopt / Adapt / Reject summary for the positive case

### Adopt

- Separate problem understanding from execution.
- Use literature search to derive candidate analysis hypotheses/directions rather than relying only on generic statistical recipes.
- Keep explicit evidence and applicability conditions for each recommendation.
- Require a user selection gate before detailed execution planning when several scientifically plausible directions exist.

### Adapt

- AgentAda-style automated analysis selection is changed into a recommendation-first interaction: generate 3–5 candidate directions, then let the user choose.
- CASCADE-style skill evolution is changed into review-gated playbook evolution: successful usage can inform future updates, but runtime discoveries do not automatically rewrite the Skill.
- Data-science agent execution loops are split according to local task routing: ChatGPT handles literature synthesis and scientific framing; Codex becomes relevant only if the selected direction requires deterministic data processing, scripting, repeated execution, or reproducible validation.

### Reject

- Automatically executing every suggested analysis before the user chooses a direction.
- Treating literature frequency or popularity as proof that a method fits the user's experimental design.
- Auto-promoting runtime-generated procedures into the stable Skill without PR review and validation.
- Using `PR-MIX` merely because the Skill touches literature, research interpretation, and data analysis; the Skill itself is the single authoritative changed object.

## Local-experience evidence

The adapted design addresses recurring local failure modes:

1. Scientific interpretation must consider converging evidence rather than escalate severity from one isolated signal.
2. Quantitative representation must be checked before declaring conflicts, as shown by isotope examples involving `δ13C`, `atom% 13C`, and absolute `13C excess`.
3. Recommendations should distinguish observation, interpretation, and unresolved inference.
4. The user benefits from choosing among analysis directions before computation begins, avoiding unnecessary analyses and over-automation.
5. ChatGPT/Codex routing should change only when execution and verification needs change.

## Outcome

The automatic benchmark rule behaves as intended for its first real design task and its specified negative control.

Promotion recommendation for `codex-playbook` Draft PR #5: **validated once; suitable to promote from experimental to stable core trigger with bounded evidence scope**.

## Evidence boundary

Directly validated:

- new reusable Skill design triggers external benchmark;
- one-time existing `PR-RSCH` execution does not;
- external patterns can be adapted without forcing a copied architecture;
- single-authoritative-object classification remains `PR-OPS`.

Not yet validated:

- every possible reusable workflow category;
- cases with no meaningful public analogue;
- cases where external convention conflicts with safety or correctness requirements;
- fully automated plugin/Skill installation behavior.
