# Task — Validate automatic execution route audit

Validate the proposed `codex-playbook` execution-route audit against representative task-routing cases.

## Case 1 — Scientific manuscript review

User request:

> Review a near-final confirmation-report chapter for scientific logic, evidence strength, academic writing quality, and consistency. Do not edit files yet.

Expected:

- primary PR profile: `PR-RSCH`;
- specialist checks may include `PR-CAL` and `PR-AUTH`;
- initial route: `ChatGPT`;
- dominant difficulty: scientific reasoning / evidence calibration;
- GitHub role: `none` unless later packaging is requested;
- final route: `ChatGPT`;
- receipt remains in task context rather than creating a GitHub artifact solely for logging.

## Case 2 — Approved multi-file mechanical edit

User request:

> The scientific wording is approved. Apply the same approved terminology change across 18 Markdown files and verify that the previous term no longer appears.

Expected:

- initial route: `Codex`;
- dominant difficulty: repeated file implementation and repository-wide verification;
- GitHub may be `branch` / `PR` if the change is meaningful;
- final route: `Codex`;
- receipt persists in the PR/validation record if a PR exists.

## Case 3 — Scientific review escalates to deterministic recalculation

Initial user request:

> Review whether the manuscript's isotope interpretation is scientifically defensible.

During review, a numerical discrepancy can only be resolved by recalculating background-corrected absolute 13C excess from the raw workbook.

Expected:

- initial route: `ChatGPT`;
- initial primary profile: `PR-RSCH` with appropriate scientific overlays;
- reroute: `ChatGPT -> Mixed`;
- trigger: deterministic raw-data recalculation becomes necessary;
- `PR-DATA` is added as a validation requirement for the quantitative finding;
- final route: `Mixed`;
- initial decision is preserved rather than overwritten.

## Negative control 1 — Trivial factual explanation

User request:

> What does MIET stand for?

Expected:

- answer directly;
- no persistent Route Receipt or GitHub artifact required;
- no branch/issue/PR created merely to log routing.

## Negative control 2 — Repository involvement is not Codex routing

User request:

> Read a small policy file in GitHub and tell me whether its scientific wording is too strong. Do not modify it.

Expected:

- route according to reasoning/review difficulty, normally `ChatGPT`;
- GitHub is recorded as `source of truth`, not as an executor;
- repository involvement alone does not force Codex;
- no unnecessary Mixed handoff.

## Acceptance criteria

Pass if all five cases preserve the independence of:

1. PR validation profile;
2. ChatGPT / Codex / Mixed execution route; and
3. GitHub provenance/packaging role.

Additional requirements:

- initial route and final route are distinct fields;
- material reroutes append history instead of rewriting the initial decision;
- chat-only tasks do not create unnecessary GitHub logging artifacts;
- a route audit can be surfaced later without reconstructing a different route from memory;
- no case introduces `GitHub` as a fourth executor.
