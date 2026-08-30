# PR Auto-Router Forward Validation

## Objective

Validate that the proposed automatic PR validation router can infer the correct task-level validation profile from ordinary user task descriptions without requiring explicit PR labels.

## Source under test

`codex-playbook` Draft PR #11 — `Add automatic PR validation router`.

## Acceptance criteria

The router should:

1. infer one primary PR class from the authoritative object;
2. add specialist/secondary checklists only when materially triggered;
3. keep ChatGPT/Codex/Mixed execution routing independent from PR classification;
4. avoid creating `PR-MIX` for merely multi-artifact work;
5. avoid classifying by file extension alone;
6. allow direct simple questions without surfacing PR terminology;
7. not require the user to name a PR class.

## Test cases

### Case A — Near-final research DOCX

User task:

> Check this near-final confirmation-report DOCX. It contains results, figures and data. Review scientific logic, claim-evidence strength, writing quality and AI-like/formulaic language. Do not rewrite everything automatically.

Expected:
- Primary: `PR-RSCH`
- Specialist: `PR-AUTH`
- Secondary: `PR-DOC` only if native document structure/render/cross-reference QA is also performed
- Execution: ChatGPT-led or Mixed
- Not `PR-MIX`

### Case B — Quantitative isotope recalculation

User task:

> Recalculate background-corrected 13C excess from the raw spreadsheet, verify units and formulas, and update the analysis script.

Expected:
- Primary: `PR-DATA`
- Execution: Codex-heavy or Mixed
- No `PR-RSCH` merely because results belong to a manuscript

### Case C — Reusable skill creation

User task:

> Create a reusable Codex skill for Zotero tag cleanup and validate its trigger behavior.

Expected:
- Primary: `PR-OPS`
- Specialist: skill lifecycle when approved/present
- Execution: Codex-heavy with review
- Not `PR-LIT` because the authoritative changed object is the reusable skill, not the Zotero library

### Case D — DOCX formatting only

User task:

> Keep all scientific wording unchanged. Fix page breaks, caption placement, tracked changes and heading structure in this DOCX.

Expected:
- Primary: `PR-DOC`
- No `PR-RSCH` unless substantive manuscript content changes

### Case E — Figure embedded in manuscript, prose only

User task:

> Rewrite the Results paragraph describing Fig. 3.2, but do not change the figure or its source data.

Expected:
- Primary: `PR-RSCH`
- Not `PR-FIG`

### Case F — Approved skill used on data task

User task:

> Use the existing approved analysis skill to calculate qPCR copies/L from my spreadsheet.

Expected:
- Primary: `PR-DATA`
- Not `PR-OPS`; use of a skill does not make the skill the authoritative changed object

### Case G — Unrelated data + figure preference

User task:

> Fix one statistical calculation and separately change a figure color preference.

Expected:
- Split `PR-DATA` and `PR-FIG` work units if both changes are persisted
- Not `PR-MIX` because there is no atomic dependency

### Case H — Simple factual question

User task:

> What does NADH/NAD+ indicate biologically?

Expected:
- Direct answer
- No surfaced PR workflow required
