# K-SYNTH-1 / Run140 — negative dependency counterexample

**Status:** verified semantic-representation boundary; NOT a capable-model experiment, NOT a representation advantage, NOT a new theorem in incremental computation.

## Claim and assumptions
A positive-value dependency graph (only values actually selected by a dynamic lookup) cannot soundly certify noninterference of key insertions in an open-world registry. The limitation applies when registry membership may change without freezing the registry snapshot. It does not describe a demonstrated defect in Lattice's existing pure finite-Boolean FramedProgram.

Let f(R,x) = R[k](x) when k is present in registry R, otherwise b(x). Take R0 = {}, b(x) = "fallback:" + x, and h(x) = "plugin:" + x. On R0, the positive-value trace contains b but no R[k]. The edit R1 = R0 union {k -> h} changes f(R1,x) from b(x) to h(x) although the positive trace has no edge to the edited key. An unrelated insertion {j -> h} with j != k preserves f. Thus a checker using only the positive trace cannot safely classify key insertion as noninterfering.

## Proof
At R0, k is absent, so f(R0,x)=b(x). By construction h(x) != b(x). At R1, k is present, so f(R1,x)=h(x) != f(R0,x). Yet the initial positive-value provenance contains only b. A noninterference rule based solely on absence of a positive dependency from the protected output to R[k] incorrectly accepts this change. The missing dependency is the negative observation absent(R,k).

## Minimal representation consequence
An effect-aware semantic graph must record key-presence/absence guards (including object identity, key and epoch or immutable snapshot) alongside positive value dependencies. A write to the same registry/key invalidates an absence guard. For arbitrary Python with dynamic keys or aliasing, either prove conservative read/write summaries, anchor reads to immutable snapshots, or reject edits whose effects cannot be established. Both graph and Python experimental arms must receive the identical guard facts, compiler/verifier and patch authority.

## Executable witness
A three-module Python example (registry.py, fallback.py, router.py) plus a deterministic test compares insertion at key dispatch against unrelated key audit. Four tests passed locally on 2026-10-20. Result: relevant insertion changes protected output despite no positive dependency; unrelated insertion does not. The guard distinguishes the two.

## Single active kernel: K-SYNTH-1
1. **Intervention:** owner-qualified immutable graph with explicit dependency, state and guard commitments.
2. **Control:** information-equivalent ordinary Python SSA with explicit corresponding guard facts, identical compiler, verifier, patch grammar, authority and token budget.
3. **Model:** Qwen2.5-Coder-7B-Instruct on free public compute; second capable model if available. None run in Run140.
4. **Tasks:** prospectively frozen independently sourced realistic multi-file repair tasks; no correlated synthetic twins counted as independent product-scale units.
5. **Primary scalar:** within-task first-attempt exact semantic repair success difference (graph minus Python).
6. **Alternative:** formatting/indexing or salience, not semantic structure.
7. **Falsification:** matched Python meets or beats graph at useful paired power, or advantage disappears under information-preserving indexing ablation.
8. **Unseen prediction:** any genuine graph effect strengthens with cross-file conditional registry coupling and edit radius; disappears when dependency and guard information is locally explicit. Freeze before holdout.
9. **Publication threshold:** prior-art audit, powered realistic tasks, same compiler, capable model, independent evaluation, ablation, unseen prediction, uncertainty, adversarial cases, clean reproduction and direct system consequence.
10. **System consequence:** keep pure Boolean versioned semantics; require negative guards or conservative effects before supporting dynamic registries. No new syntax counted as research progress.

## Preserved failures and limitations
Run132 and Run135 shortcuts; Run131/132 contaminated holdouts; Run136 synthetic-only; Run137 operational inequivalence of eager control; Run138 direct-construction owner provenance; Run139 Shannon information invariance. Run140 proves no graph-vs-Python model-performance difference. No capable-model inference, realistic powered task study, or breakthrough occurred.

**Smallest supported claim:** positive-value provenance alone cannot soundly certify frame preservation under insertion into a dynamic registry; a guard/absence commitment or conservative alternative is necessary.
