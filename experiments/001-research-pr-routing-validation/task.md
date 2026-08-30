# Experiment 001 — Research PR Routing Validation

## Objective

Forward-validate the classified research PR workflow proposed in `codex-playbook` PR #1.

## Test case

Scenario context: `POLYU` research work.

Authoritative changed object: a reusable data-analysis validation checklist for qPCR-style quantitative workflows.

Expected routing result:

- Project key: `POLYU`
- Primary PR class: `PR-DATA`
- Rationale: the authoritative changed object is data-analysis logic, so the generic PR class must override the project's default `PR-RSCH` suggestion.

## Acceptance criteria

1. The task is isolated on a dedicated branch.
2. The output records project context separately from PR class.
3. The primary class is `PR-DATA`, not `PR-RSCH`.
4. Validation follows data-oriented checks rather than manuscript-writing checks.
5. A Draft PR is created and left unmerged.
6. The result is documented sufficiently to decide whether the routing method should be promoted as forward-validated.
