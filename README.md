# Lattice

Lattice is a research project investigating a simple question:

> If AI writes most of the software, is conventional source code still the right primary representation for software?

The working hypothesis is that coding agents are bottlenecked not only by model capability, but by the representation they are forced to reason through. Conventional code records implementation well, but often scatters or loses product intent, visual structure, state, permissions, architectural rationale, invariants, and optimization constraints.

Lattice explores an AI-native software representation that preserves those semantics explicitly, with conventional code as a compilation/lowering target.

## Research model

```text
human intent
    ↓
Lattice representation
    ↓
AI reasoning + deterministic verification/optimization
    ↓
React / TypeScript / backend / native / other targets
```

The project is empirical. The goal is not to assume a new language is better, but to test whether the same underlying coding model performs better through Lattice than through direct source-code generation or ordinary spec-first planning.

## Primary questions

1. Does an AI-native representation improve long-horizon software evolution?
2. Does it preserve requirements, architecture, security invariants, design intent, and state more reliably?
3. Does semantic locality reduce context, repo navigation, repair loops, and code churn?
4. Can explicit optimization intent produce more efficient implementations?
5. Which representation primitives actually cause gains?
6. If a simpler project-state/specification layer performs just as well, does that falsify the need for a new language?

## Research principles

- same-model, equal-budget controls
- strong direct-code and spec/planning baselines
- frozen tasks and held-out evaluation
- explicit ablations
- preserve negative results
- distinguish authoring efficiency from runtime efficiency
- do not claim a breakthrough from a visually impressive demo

See `docs/RESEARCH_AGENDA.md` for the current bottleneck map.
