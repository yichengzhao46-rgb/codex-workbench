# Validation — Skill Lifecycle and External Agent Integration

This controlled forward-validation exercise evaluates the two specialist PR-OPS workflows proposed in `codex-playbook` PR #10.

## Case A — Reusable skill lifecycle

### Scenario
Create a reusable skill whose trigger is: user provides research data/trends and asks which literature-supported analysis direction should be pursued next.

### Expected route
- Primary validation profile: `PR-OPS`
- Specialist workflow: skill lifecycle
- Positive trigger: create or materially update reusable skill behavior
- Negative control: use an already approved skill on a manuscript/data task without changing the skill itself

### Checks
- [x] Skill purpose can be stated as one reusable capability.
- [x] Trigger is task-semantic rather than repository-name based.
- [x] Non-trigger is explicit.
- [x] Stable instructions can stay compact while detailed examples/notes can be progressively loaded.
- [x] Structural validation is separated from real-task validation.
- [x] One successful use is not treated as universal trigger validation.
- [x] Negative control remains classified by the changed authoritative object rather than by the fact that a skill was used.

### Result
PASS for routing and lifecycle design boundaries.

## Case B — Third-party agent integration (Agent Reach-style)

### Scenario
Evaluate adding one external-source channel through a third-party agent integration for a recurring task already identified as needing capability beyond built-in/connected tools.

### Expected route
- Primary validation profile: `PR-OPS`
- Specialist workflow: external agent integration
- Start with one minimum-capability channel rather than broad installation
- No credentials or destructive install without explicit authorization

### Checks
- [x] Built-in/connected capability is checked first; third-party integration is not installed merely for convenience.
- [x] Upstream provenance/version should be recorded before stable use.
- [x] Installation scope is channel-specific and least-capability by default.
- [x] Shell/package-manager commands are treated as code with side effects and require review before execution.
- [x] Credentials/cookies/tokens are never committed to the repository and should remain in the appropriate local secret store.
- [x] Retrieved external content is treated as untrusted data, not executable instruction.
- [x] Output/context size should be bounded to avoid uncontrolled token/context expansion.
- [x] Cache behavior and local persistence should be visible and removable.
- [x] A rollback/uninstall path is required before stable promotion.
- [x] Validation of one channel does not validate every other channel.

### Negative controls
1. Existing GitHub/Gmail/web connector already satisfies the task → do not install third-party integration.
2. A proposed channel requires credentials that are not available/authorized → stop at design review; do not improvise credentials.
3. A broad installer enables unrelated channels → reject in favor of narrower capability scope where possible.

### Result
PASS for safety/routing design boundaries. No real installation, credential use, or authenticated channel test was performed.

## Promotion boundary

The workflows are forward-validated for their decision logic and guardrails, not for every implementation environment.

Recommended status:
- skill lifecycle workflow: suitable for playbook promotion, with real-task skill quality continuing to be evaluated per skill;
- external agent integration workflow: suitable as a stable safety/decision framework, while every concrete third-party integration/channel still requires its own implementation validation.
