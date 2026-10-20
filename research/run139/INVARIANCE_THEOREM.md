# K-SYNTH-1 / Run139 — representation information-invariance theorem

**Status:** exact mathematical restriction on mechanism claims, not a capable-model experiment or a novel information-theory result.

## Theorem

Let F be the complete task-specific semantic facts (including version ownership, immutable dependency captures, edit authority and verifier contract), Y the correct patch, and G=g(F), P=p(F) be deterministic, lossless graph and Python SSA representations. Assume g and p are injective on the support of F and introduce no task-relevant extra information. Then:

H(Y|G) = H(Y|F) = H(Y|P) and I(Y;G) = I(Y;F) = I(Y;P).

For any fact-defined correct dependency path D, H(D|G) = H(D|P) as well.

**Proof:** F can be recovered deterministically from either G or P, while G and P are deterministic functions of F. Hence all three generate the same sigma-algebra (modulo null events), so their conditional distributions of Y and D coincide. The entropy and mutual-information equalities follow.

**Interpretation:** If Lattice's explicit graph beats an information-equivalent Python control, it cannot have reduced the *Shannon uncertainty* about the correct path. The possible mechanism is bounded-model computation: attention localization, path lookup count, invalid intermediate states, semantic churn, or verifier loops. Measure and ablate those quantities rather than using the term 'reduced dependency-search entropy' without a model-relative definition.

## Counterexample to interpreting a raw graph win

A version graph indexes N immutable nodes by ID. The ordinary Python SSA control represents the same N nodes with _vID assignments. A naive graph algorithm follows d dependency edges in O(d) lookups. A naive Python algorithm repeatedly scanning all N lines may use O(Nd) inspections. But a single O(N) Python indexing pass followed by d O(1) lookups gives O(N+d). This raw gap is attributable to indexing strategy, not stronger semantics or more information. The graph and Python views remain invertible.

## Single active kernel

1. **Intervention:** owner-qualified immutable dependency/state graph with explicit captures.
2. **Strongest control:** ordinary Python SSA with exactly the same facts, edit authority, compiler/verifier, output JSON patch grammar and token budget.
3. **Capable models:** Qwen2.5-Coder-7B-Instruct (or stronger no-cost model), second independent model if public compute permits. No model run occurred here.
4. **Tasks:** prospectively frozen independently sourced realistic multi-file repairs. Correlated synthetic twins are diagnostics, not independent product-scale samples.
5. **Primary scalar:** cluster-mean first-attempt exact semantic repair success difference, graph minus Python.
6. **Strongest alternative:** indexing, ordering, tokenization or visual salience rather than semantic commitments.
7. **Falsification:** Python matches/beats graph with useful paired power; or graph benefit disappears under an information-preserving indexing/adjacency ablation.
8. **Unseen prediction:** graph effect increases with cross-file capture depth and edit radius; disappears for locally explicit shallow single-file captures. Freeze before holdout outcomes.
9. **Publication threshold:** prior-art audit, powered realistic tasks, same compiler, capable model, independent evaluator, mechanism ablation, unseen-condition prediction, uncertainty, adversarial cases, clean reproduction and system consequence.
10. **System consequence:** retain owner-qualified captured semantics and common compiler; instrument actual bounded search costs; do not claim Shannon-entropy reduction or count new syntax as science.

## Preserved failures

Run132 view-free shortcut; Run135 fixed-position shortcut; Run136 synthetic-only/no capable inference; Run137 eager Python control not operationally equivalent for partial expressions; Run138 direct-construction owner-provenance defect. Run131/132 contaminated holdouts remain excluded.

**Smallest supported claim:** lossless representation alone cannot alter task-conditioned Shannon information. This theorem does not establish any Lattice model-performance advantage. Next substantive run must execute capable-model matched inference or identify a new theorem/counterexample that changes the semantic representation, not repeat provenance or CI polishing.

Prepared 2026-10-20.