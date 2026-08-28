# Codex Workbench

An execution workspace for applying, testing, and validating Codex methods through real tasks, prototypes, agents, automations, integrations, and experiments.

## Purpose

This repository defines **where Codex methods are executed and tested**. Reusable operating methods belong in `codex-playbook`; this repository is for implementation, experimentation, validation, and practical outputs.

## Relationship to codex-playbook

- **codex-playbook** = approved methods, rules, prompts, templates, and standards.
- **codex-workbench** = execution environment for trying those methods in practice.

A successful pattern discovered here should be documented, generalized, and promoted into `codex-playbook` rather than remaining as an undocumented local trick.

## Repository structure

```text
codex-workbench/
├── AGENTS.md
├── projects/
├── prototypes/
├── agents/
├── automations/
├── integrations/
├── experiments/
├── tests/
└── outputs/
```

## Working model

`playbook method → workbench execution → validation → lessons learned → playbook improvement`

## Core principles

1. Keep experiments isolated and reversible.
2. Preserve inputs and provenance.
3. Record enough context to reproduce successful runs.
4. Separate prototypes from stable reusable components.
5. Prefer branch + Draft PR for meaningful changes.
6. Do not treat an experiment as a validated method until it has been reviewed and promoted to `codex-playbook`.
