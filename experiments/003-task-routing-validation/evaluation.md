# Evaluation — Experiment 003

## Routing results

### Primary scenario — evidence synthesis and manuscript claim review

**Result: PASS**

- Route: `ChatGPT`
- Task class: research / review
- Project key: `POLYU`
- Primary PR class if packaged: `PR-RSCH`
- Codex participation: not required by default

### Why

The task's failure mode is interpretive: overclaiming species-specific carbon fixation, ignoring converging evidence, or confusing community-level EA-IRMS with organism-specific incorporation. No executable validation is required to answer the stated request. The routing policy therefore correctly prioritizes ChatGPT despite the task being research- and repository-adjacent.

This also validates the separation between two dimensions:

- PR class answers **what authoritative object is being changed** (`PR-RSCH`).
- task route answers **which environment can complete and verify the difficult part most efficiently** (`ChatGPT`).

## Negative control A — raw isotope recalculation + plotting script

**Result: PASS**

- Route: `Mixed`, becoming Codex-heavy during execution.
- Primary PR class: `PR-DATA`.
- ChatGPT role: resolve scientific definitions and calculation basis if ambiguous; define acceptance criteria.
- Codex role: deterministic workbook calculation, script modification, reproducibility checks, and executable validation.

The route changes because the main completion evidence now includes deterministic recalculation and executable verification. Scientific topic alone does not keep the task in ChatGPT.

## Negative control B — approved terminology across 18 files

**Result: PASS**

- Route: `Codex`.
- Task class: bounded multi-file implementation / verification.
- Scientific interpretation is already locked.
- Completion requires repository-wide search, mechanical edits, and verification that no stale term remains.

The policy correctly routes this to Codex even though the changed content is prose.

## Acceptance-criteria check

- [x] Primary research reasoning task routes to ChatGPT.
- [x] `PR-RSCH` does not imply Codex execution.
- [x] Adding deterministic data work changes the route to Mixed/Codex-heavy.
- [x] Locking the reasoning and expanding mechanical repository work changes the route to Codex.
- [x] No case depends on exclusive permission assumptions.
- [x] Escalation conditions are explicit and behaviorally meaningful.

## What this test validates

The policy successfully distinguishes:

1. **authoritative object classification** from **execution-environment routing**;
2. scientific reasoning from deterministic implementation;
3. direct execution from justified handoff;
4. topic identity from task mechanics.

These are the main ambiguities the routing policy was intended to resolve.

## Limitation

This experiment validates one research/review scenario plus two controlled route-changing variants. It does not yet prove every task class or every high-risk override. In particular, security-sensitive operations, destructive repository changes, and large architectural code changes remain untested.

## Promotion recommendation

**Promote with one structural change.**

`TASK_ROUTING.md` is mature enough to become stable routing policy, but it should not be the only formal workflow artifact. Keep it as the canonical policy/rule, and add a short executable workflow under `workflows/` that tells an agent how to apply the policy at task intake.

Recommended formal structure:

- `TASK_ROUTING.md` — stable policy and decision model.
- `workflows/task-routing-workflow.md` — compact intake procedure: classify → route → build handoff if needed → record escalation condition.
- optional `templates/task-envelope.md` — copy-ready handoff contract for Mixed tasks.

Status recommendation: mark the core routing rule as **forward-validated in one controlled research scenario with two negative controls**, not universally validated.
