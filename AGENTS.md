# AGENTS.md — Codex Workbench

## Mission

This repository is the execution and validation environment for Codex workflows defined in `codex-playbook`.

## Default behavior

1. Read this file and relevant project context before editing.
2. Keep experiments isolated by folder and, for meaningful work, by branch.
3. Preserve original inputs; do not overwrite source material unless explicitly required.
4. Record assumptions, dependencies, and validation steps for reproducibility.
5. Prefer Draft Pull Requests for non-trivial changes.
6. Do not merge automatically unless explicitly instructed.
7. Review the final diff before completion.
8. Never commit secrets, API keys, tokens, credentials, or private data.

## Repository roles

- `projects/`: bounded execution projects with a clear objective.
- `prototypes/`: early implementations that may be discarded or redesigned.
- `agents/`: executable or testable agent configurations.
- `automations/`: recurring or scripted workflows.
- `integrations/`: MCP, API, GitHub, or external-tool integration experiments.
- `experiments/`: controlled tests of prompts, workflows, models, or configurations.
- `tests/`: shared validation utilities and regression tests.
- `outputs/`: generated non-source outputs that are safe and appropriate to version.

## Promotion rule

A pattern discovered here is not automatically a standard. Promote it to `codex-playbook` only after it is reusable, documented, and sufficiently validated.

## Pull request expectations

Meaningful PRs should include:
- objective
- implementation summary
- validation performed
- evidence of success or failure
- known limitations
- whether any lesson should be promoted to `codex-playbook`
