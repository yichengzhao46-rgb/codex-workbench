# Evaluation — Experiment 014

## Result

**PASS**

The proposed Route Receipt keeps PR validation, execution routing, and GitHub provenance as separate dimensions and preserves the initial routing decision when a material reroute occurs.

## Case results

### Case 1 — Scientific manuscript review

Observed receipt:

```text
Authoritative object: near-final scientific manuscript
Primary PR profile: PR-RSCH
Secondary / specialist checks: PR-CAL, PR-AUTH
Initial route: ChatGPT
Dominant difficulty: scientific reasoning, evidence calibration, academic review
Required completion evidence: evidence-calibrated findings and writing audit
Primary executor / writer: ChatGPT
GitHub role: none
Escalate / reroute if: deterministic recalculation or multi-file implementation becomes necessary
Reroute history: none
Final route: ChatGPT
Validation performed: scientific/evidence/style review
Persistent record location: chat
```

**PASS** — a DOCX/manuscript review does not route to Codex merely because a file exists, and no GitHub artifact is created solely for the receipt.

### Case 2 — Approved multi-file mechanical edit

Observed receipt:

```text
Authoritative object: approved terminology across repository files
Primary PR profile: PR-RSCH for scientific terminology context
Secondary / specialist checks: none beyond approved meaning lock unless needed
Initial route: Codex
Dominant difficulty: repeated file editing and repository-wide verification
Required completion evidence: all target files updated; old term absent; diff reviewed
Primary executor / writer: Codex
GitHub role: branch / PR when packaged
Escalate / reroute if: implementation encounters an unresolved scientific wording decision
Reroute history: none
Final route: Codex
Validation performed: repository-wide search and diff verification
Persistent record location: PR body/comment when a PR exists
```

**PASS** — execution route follows implementation burden rather than the manuscript/research PR label.

### Case 3 — Scientific review escalates to deterministic recalculation

Observed receipt:

```text
Authoritative object: isotope interpretation, then source-data calculation required for one finding
Primary PR profile: PR-RSCH
Secondary / specialist checks: PR-CAL; PR-DATA added for the quantitative finding
Initial route: ChatGPT
Dominant difficulty: initially scientific interpretation
Required completion evidence: defensible claim plus deterministic recalculation of the disputed quantity
Primary executor / writer: ChatGPT for interpretation; Codex for quantitative execution
GitHub role: source of truth / validation record if files are repository-backed
Escalate / reroute if: raw-data recalculation becomes necessary
Reroute history: ChatGPT -> Mixed because source-data recalculation became necessary
Final route: Mixed
Validation performed: scientific review + reproducible calculation/unit verification
Persistent record location: task/PR/validation record as applicable
```

**PASS** — the initial ChatGPT decision remains visible and the route is appended as a reroute rather than retrospectively rewritten.

### Negative control 1 — Trivial factual explanation

Expected and observed behavior:

- direct ChatGPT answer;
- no persistent Route Receipt requirement;
- no GitHub branch, issue, commit, or PR created solely for routing metadata.

**PASS**

### Negative control 2 — Repository involvement is not Codex routing

Observed receipt:

```text
Authoritative object: policy wording under review
Primary PR profile: determined by policy content
Initial route: ChatGPT
Dominant difficulty: reasoning/review
Primary executor / writer: ChatGPT
GitHub role: source of truth
Reroute history: none
Final route: ChatGPT
```

**PASS** — GitHub is not represented as a fourth executor and repository access alone does not force Codex.

## Key properties validated

- PR profile and execution route remain independent.
- GitHub role is recorded separately from execution route.
- Initial and final routes are distinct fields.
- Evidence-based reroutes append history rather than erase the original decision.
- Chat-only work does not create unnecessary persistent logs.
- Repository-backed work can persist the receipt in an existing PR/validation record.
- Several specialist overlays do not automatically imply a Mixed route.
- The audit adds traceability without requiring extra ChatGPT-Codex handoffs.

## External benchmark adaptation check

The local workflow retains only the useful public patterns:

- separate routing decision from execution outcome;
- keep a compact route receipt for auditability.

It intentionally rejects heavier infrastructure such as a routing database, model-cost ledger, or mandatory persistent log because those would add process overhead without addressing the demonstrated local failure mode.

## Maturity recommendation

The workflow is **forward-validated once** for the intended core scope and is suitable for promotion to stable after the playbook PR is updated with this validation evidence.

## Remaining boundary

Not yet validated for:

- security-sensitive or destructive operations;
- long-running multi-stage implementation with several legitimate reroutes;
- concurrent multiple-writer workflows;
- external integrations that generate their own routing/provenance logs.

These limits do not block stable use for the current core ChatGPT/Codex/Mixed routing scope, but future materially different cases should extend the validation record.
