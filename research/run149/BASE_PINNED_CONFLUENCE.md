# K-SYNTH-1 Run149 — base-pinned transaction confluence

**Status:** local source-faithful bounded-Boolean counterexample and proof. This is a semantic-system design correction, not a novel database theorem, not a capable-model comparison, and not a representation breakthrough.

## Failure of naive latest-root captures

Take immutable base roots `a=x`, `b=y`, and protected `sealed=a_old and b_old`. Two authorized transactions write disjoint roots:

- A: `a := not x`.
- B: `b := a and y`.

If B implicitly captures whichever `a` is latest when applied, A then B yields `b=(not x) and y`, while B then A yields `b=x and y`. They differ for both assignments with `y=True`, although A and B write different roots. `sealed` is preserved in both orders. Thus disjoint write authority does **not** imply commutative semantic edits under implicit latest-root reads.

## Base-pinned read theorem (bounded immutable DAG)

Let S be an immutable acyclic graph of pure total Boolean expressions with inputs X, owner-qualified immutable node versions, and named mutable root pointers. Let transactions A and B have disjoint root write sets. Each transaction is prospectively frozen against the **same authenticated base snapshot** and each dependency in each newly written expression is bound to a specific immutable base node ID, including historical self-captures. The only changes made by a transaction are appending new immutable nodes and replacing its own root pointers. Require exact ancestry of the frozen base and reject overlapping writes.

Then applying A followed by B and B followed by A yields the same extensional mapping from every input assignment to every named output, although appended node IDs and graph serialization can differ.

**Proof:** Every newly created node is a pure expression of the same inputs and the same immutable base-version values in both orders. The base nodes cannot change. Structural induction on each transaction's acyclic new-node dependency order gives identical values for each transaction's written roots in either order. Since write sets are disjoint, their root-pointer replacements commute. Untouched roots continue pointing to their original immutable nodes, so protected outputs are unchanged. This is extensional confluence, not byte-for-byte graph identity.

The assumptions matter: `latest` or head-relative reads invalidate the conclusion; shared write targets are conflicts; impure expressions, mutable aliases, external state and open-world registry effects are outside the finite-Boolean theorem.

## Executable local discriminator

A source-faithful local reconstruction of `src/lattice/framed_edits.py` and the unintegrated Run148 `OwnedFrame` extension was used. Run149 adds an opt-in `BasePinnedTransaction` carrying base hash, base owner ledger, base root IDs, explicit read-version map, and disjoint write conflict rejection. Results: 13/13 tests passed including Run148 regressions, 16 pairs of edit forms over all four Boolean inputs, naive nonconfluence witness, authenticated-ancestry rejection, authorization rejection and self-capture. **This was not tested against the live GitHub compiler.**

## System consequence

Semantic transactions must distinguish (i) trusted write authority, (ii) intended rebinding, and (iii) immutable base-version reads. Use base-pinned read sets by default for independently authored/concurrent edits; require explicit new-version captures when causal dependence on another transaction is intended. Canonical version IDs are needed only if physical graph equality is required.

Both graph and ordinary-Python control must receive exactly these same transaction facts and compiler; this theorem cannot establish graph superiority.

## Sole research kernel K-SYNTH-1

1. **Intervention:** explicit owner/version/guard graph with base-pinned read and edit-intent commitments.
2. **Control:** ordinary Python SSA encoding identical versions and commitments; identical compiler, verifier, patch grammar, authority and token budget.
3. **Models:** capable free/open coder at least 7B, second model if compute permits; none run here.
4. **Tasks:** independently sourced, prospectively frozen realistic multi-file repairs with nontrivial protected dependency cuts.
5. **Primary scalar:** within-task first-attempt exact semantic repair success difference (graph minus Python).
6. **Alternative:** visual indexing, tokenization, ordering or salience rather than structural commitments.
7. **Falsification:** powered Python control matches/beats graph or advantage vanishes under information-preserving adjacency ablation.
8. **Unseen prediction:** representation effect, if any, strengthens with cross-file protected dependency-cut complexity and disappears for isolated leaf edits; freeze before holdout.
9. **Publication threshold:** prior-art audit, powered realistic tasks, independent evaluator, capable model replication, ablation, unseen prediction, uncertainty, adversarial cases and clean reproduction.
10. **System consequence:** snapshot-qualified semantic edits with explicit capture/rebind intent and conflict checks, available to both arms.

**Smallest supported claim:** implicit latest-root captures make disjoint edits order-dependent; base-pinned explicit immutable reads restore extensional confluence in the pure finite-Boolean DAG model.

**Unresolved:** realistic powered capable-model experiment and live compiler integration. Preserve Run136/143 synthetic-task failure and Run146 realism falsification. No syntax-only progress counted.
