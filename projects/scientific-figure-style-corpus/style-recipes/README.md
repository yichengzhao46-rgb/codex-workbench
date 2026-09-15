# PR20 Style Recipe Layer

Each new scientific figure should combine approved references by visual role: composition, rendering, connectors, palette, typography, whitespace, density, depth, and hierarchy. Do not copy one complete source figure.

A Style Recipe now has two responsibilities:

1. **Visual synthesis** — translate the human-curated reference library into a task-specific visual grammar.
2. **Generation control** — constrain AI rendering so the final figure does not retain a generic AI-generated aesthetic.

Every publication-facing recipe should therefore define:

- science lock and evidence boundaries;
- multi-reference roles;
- visual architecture;
- rendering intensity;
- semantic connector grammar;
- asset-first vs whole-figure generation strategy;
- elements that must be added or redrawn after generation;
- anti-AI-look constraints;
- subtraction pass;
- scientific + visual + AI-flavor QA.

Default production preference:

> **Generate difficult visual assets with AI; assemble layout, typography, connectors, evidence semantics, and final spacing under controlled design rules.**

Use [`STYLE-RECIPE-TEMPLATE.md`](STYLE-RECIPE-TEMPLATE.md) for new tasks and [`../ANTI-AI-LOOK-PASS.md`](../ANTI-AI-LOOK-PASS.md) for the publication-facing cleanup pass.
