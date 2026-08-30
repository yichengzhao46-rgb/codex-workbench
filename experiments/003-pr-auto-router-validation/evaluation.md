# PR Auto-Router Validation Evaluation

## Result

**PASS for all eight defined cases.**

This is a controlled forward-validation of the routing logic proposed in `codex-playbook` Draft PR #11. It validates classification boundaries and anti-overtrigger behavior; it does not validate every future edge case.

## Case results

| Case | Expected | Routed result | Status |
| --- | --- | --- | --- |
| A — near-final research DOCX | `PR-RSCH` + `PR-AUTH`; optional `PR-DOC` | authoritative object is scientific manuscript argument; comprehensive writing/AI-style review triggers `PR-AUTH`; DOCX format alone does not override primary class | PASS |
| B — isotope recalculation | `PR-DATA` | authoritative object is quantitative calculation/script; manuscript context is secondary | PASS |
| C — reusable Zotero cleanup skill | `PR-OPS` + skill lifecycle | authoritative object is reusable Codex skill; Zotero domain does not make it `PR-LIT` | PASS |
| D — DOCX formatting only | `PR-DOC` | native document structure/render behavior is the only changed object | PASS |
| E — prose about figure only | `PR-RSCH` | figure is referenced but not changed | PASS |
| F — approved skill used for qPCR | `PR-DATA` | approved skill is execution mechanism, not changed object | PASS |
| G — unrelated data + color preference | split `PR-DATA` + `PR-FIG`; not `PR-MIX` | no atomic dependency; separate validation/rollback paths | PASS |
| H — factual NADH/NAD+ question | direct answer | trivial/direct question does not require surfaced PR ceremony | PASS |

## Key boundaries validated

### 1. File extension does not control primary classification

A DOCX can route to `PR-RSCH` or `PR-DOC` depending on whether the authoritative object is scientific content or native document behavior.

### 2. Tool use does not control primary classification

Using an approved skill for a quantitative task does not change the task to `PR-OPS`. `PR-OPS` applies when the skill/agent/router/integration itself is the changed object.

### 3. Specialist overlays can auto-trigger without becoming top-level classes

The near-final manuscript case correctly adds `PR-AUTH` beneath `PR-RSCH` without creating a new primary class.

### 4. `PR-MIX` remains restricted

A data fix plus unrelated figure preference does not qualify. Multiple work items alone are insufficient; an inseparable atomic dependency is still required.

### 5. Validation profile and execution route remain separate

- manuscript reasoning can be `PR-RSCH` while ChatGPT-led;
- quantitative recalculation can be `PR-DATA` while Codex-heavy;
- reusable skill creation can be `PR-OPS` while Codex-heavy;
- none of these classifications automatically requires a GitHub Pull Request for the user's substantive task.

## Negative-control assessment

The controls specifically guard against the most likely over-trigger failures:

- classifying by file type instead of changed object;
- classifying by tool used instead of artifact changed;
- treating any multi-artifact task as `PR-MIX`;
- surfacing routing ceremony for simple factual questions.

All defined controls passed under the proposed rules.

## Evidence boundaries

- Directly validated: the eight written routing scenarios and their classification logic.
- Not validated: every combination of specialist overlays, future PR classes, or ambiguous tasks with insufficient user intent.
- Not executable validation: this router is an instruction/routing method rather than a deterministic software classifier, so PASS means the stated rules resolve the controlled cases consistently.
- Future refinement should record real misroutes from normal work and add regression cases only when a concrete failure appears.

## Promotion recommendation

The auto-router is suitable for promotion after human review of `codex-playbook` PR #11.

Recommended stable posture:

- automatic and mostly silent for non-trivial in-scope tasks;
- authoritative-object-first;
- specialist overlays loaded progressively;
- execution route chosen independently;
- GitHub PR creation remains a separate decision;
- new regression cases added from actual misrouting rather than speculative taxonomy expansion.
