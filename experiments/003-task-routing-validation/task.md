# Experiment 003 — ChatGPT/Codex Task Routing Validation

## Objective

Forward-validate the `TASK_ROUTING.md` policy proposed in `codex-playbook` PR #3 using a realistic research task where the PR class and the preferred execution environment are not the same concept.

## Primary scenario

Project context: `POLYU` research work.

User request:

> Review a confirmation-report paragraph that interprets coculture 13C-bicarbonate tracing together with heat-killed controls, qPCR, metabolite dynamics, and physiological evidence. Decide whether the wording overstates species-specific carbon fixation, and revise the claim so it reflects the combined evidence without treating bulk EA-IRMS as RP-specific. No raw-data recalculation, plotting, or repository-wide mechanical edit is requested.

### Relevant properties

- The authoritative changed object is scientific interpretation / manuscript wording.
- The main difficulty is evidence synthesis and claim-strength judgment.
- Multiple lines of evidence must be considered jointly.
- The task does not require code execution, tests, builds, or an edit-run-debug loop.
- A wrong result would most likely arise from reasoning or evidence-boundary errors rather than implementation errors.

## Expected routing

```text
Route: ChatGPT
Task class: research / review
Project key: POLYU
Primary PR class if packaged: PR-RSCH
Reason: scientific reasoning and evidence-boundary judgment dominate; executable validation is not required.
ChatGPT role: synthesize evidence, judge claim strength, revise wording.
Codex role: none by default.
GitHub output: none unless the revised method/wording is being committed as a reusable or repository-tracked artifact.
Acceptance check: community-level versus species-specific attribution is preserved; converging evidence is considered; no unsupported causal or species-specific claim is introduced.
Escalate if: raw isotope data must be deterministically recalculated, a reusable analysis script must change, or the task becomes a multi-file mechanical implementation.
```

## Negative control A — same scientific topic, executable data task

User request:

> Recalculate atom% 13C and background-corrected absolute 13C excess for all samples from the raw workbook, verify units and formulas, regenerate the summary table, and update the plotting script.

Expected route:

- `Mixed` overall.
- ChatGPT frames the scientific definition, calculation basis, and acceptance criteria if ambiguity remains.
- Codex performs deterministic recalculation, script changes, and executable verification.
- Primary PR class: `PR-DATA`; add `PR-FIG` only if figure semantics/source contracts change atomically.

## Negative control B — approved prose, repository-scale mechanical application

User request:

> The scientific wording has already been approved. Apply the exact terminology replacement and section-link update consistently across 18 repository Markdown files and verify no old term remains.

Expected route:

- `Codex`.
- Task class: bounded multi-file implementation / verification.
- The difficult part is repository-wide mechanical execution and verification, not scientific judgment.

## Acceptance criteria

1. The primary scenario routes to ChatGPT despite being a POLYU/GitHub-adjacent research task.
2. `PR-RSCH` is kept separate from the tool route; PR class does not imply Codex execution.
3. Negative control A escalates to Mixed/Codex when deterministic data execution is introduced.
4. Negative control B routes to Codex when the scientific decision is already locked and multi-file mechanical work dominates.
5. No route is selected based on assumed exclusive permissions.
6. The escalation condition is explicit and would change the route when task nature changes.
