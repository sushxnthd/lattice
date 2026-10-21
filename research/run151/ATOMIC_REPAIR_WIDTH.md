# Run151 — atomic repair width (K-SYNTH-1)

Status: bounded semantic-system theorem and local executable tests. NOT a representation breakthrough or capable-model experiment.

## Counterexample
For Boolean input x, roots a=x and b=x satisfy the trusted live invariant a==b. A protected historical output sealed captures a_old and b_old. The target a'=not x, b'=not x also satisfies the live invariant and preserves sealed.

Either one-root edit alone violates the live invariant for both values of x. An atomic two-root transaction succeeds. Therefore a compiler that checks live invariants after every separately committed single-root edit cannot realize this valid repair.

## General result
For n>=2 roots all initially computing f(x), with invariant all roots equal, and target all computing g(x), where f(x*)!=g(x*) at some input x*, every nonempty proper subset of direct f->g replacements violates the invariant at x*. Hence the specified direct repair path has minimum atomic root-edit width n.

Proof: at x*, a proper subset computes g(x*) and its complement computes f(x*), contradicting equality. The full set computes g everywhere and satisfies equality. Immutable historical captures remain unchanged. QED.

This is a familiar transactional-atomicity phenomenon; no claim of novel mathematics. It implies that the Lattice semantic representation must have first-class multi-root atomic transactions, explicit per-edge historical capture, and trusted live-invariant hyperedges. Validate the proposed merged state before publishing any root pointer. Both graph and Python representation arms must use the same compiler/verifier.

## Local evidence and limitations
23 local tests passed, including 2- and 3-root exhaustive subset checks, mixed captures, invariant witnesses and rollback. The implementation is in a local package, not integrated into the live compiler. No capable-model inference, realistic-task study, or representation-specific effect occurred.

## Research kernel
K-SYNTH-1 remains the sole kernel. Structural graph vs information-equivalent indexed Python SSA; same facts, edit authority, patch grammar, compiler/verifier, token budget. Primary endpoint: paired first-attempt exact semantic repair success difference. Hypothesized boundary: stronger effect on cross-file protected dependency cuts, absent on leaf edits. Falsify via powered matched capable-model experiment and mechanism ablation.

Exact two-sided McNemar power under P(graph-only)=0.20, P(Python-only)=0.10, alpha=.05 requires 249 independent paired tasks for >=80% power. Run143's 168 synthetic twin clusters cannot establish product-scale claims. No model outcomes inspected.

No force push or merge. Preserve failures.
