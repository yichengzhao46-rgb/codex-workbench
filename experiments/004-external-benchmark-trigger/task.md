# Experiment 004 — External Workflow Benchmark Trigger Validation

## Objective

Forward-validate the automatic trigger proposed in `codex-playbook` Draft PR #5 for the External Workflow Benchmark and Local Adaptation workflow.

The test must distinguish a reusable method-design task that should trigger external benchmarking from a one-off execution of an existing approved research workflow that should not.

## Positive case — should trigger

User request:

> Design a new reusable research Skill/PR called “Literature-guided Data Analysis Advisor”. It should read user data and trends, search published literature for how comparable data are interpreted, extract analysis and attribution frameworks, generate 3–5 candidate analysis directions with literature support and applicability conditions, and after the user selects one direction provide a detailed execution plan.

### Expected classification

- Project key: `CODEX` / research-method context
- Authoritative changed object: reusable Skill / workflow
- Primary PR class: `PR-OPS`
- Secondary validation lenses: `PR-RSCH` and `PR-DATA`
- Task route: ChatGPT-first because external research, methodological synthesis, and workflow design dominate; executable implementation is not yet required.
- External benchmark trigger: **YES**

### Expected benchmark behavior

Before designing the Skill:

1. inspect the local playbook and existing routing/PR rules;
2. search public references for similar agent skills/workflows and data-science agent designs;
3. classify useful external patterns as Adopt / Adapt / Reject / Unresolved;
4. tie each adopted or adapted pattern to a demonstrated local need;
5. design the smallest local Skill that fits the existing playbook;
6. define positive/non-trigger cases and evidence boundaries.

## Negative control — should NOT trigger

User request:

> Apply the existing `PR-RSCH` workflow once to review a confirmation-report paragraph for claim-evidence alignment and revise the wording. Do not change any reusable workflow, Skill, router, prompt framework, validation gate, or operating rule.

### Expected classification

- Authoritative changed object: manuscript paragraph / academic argument
- Primary PR class if packaged: `PR-RSCH`
- Task route: ChatGPT
- External benchmark trigger: **NO**

### Reason

This is ordinary one-off execution of an already approved workflow. Searching GitHub for alternative agent architectures would add overhead without changing the reusable method.

## Acceptance criteria

- [ ] Positive case triggers external benchmarking before Skill design.
- [ ] Positive case records external principles and local adaptation rather than copying a public workflow.
- [ ] Positive case remains `PR-OPS`, not `PR-MIX`, because the reusable Skill is the single authoritative changed object.
- [ ] `PR-RSCH` and `PR-DATA` are used only as validation lenses for scientific and quantitative correctness.
- [ ] Negative control does not trigger external benchmarking.
- [ ] Negative control remains ordinary `PR-RSCH` execution.
- [ ] Trigger decision is based on reusable operating behavior, not topic, repository location, or assumed permissions.
