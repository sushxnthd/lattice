# Run110 — Repair sufficiency within the single K-SYNTH-1 kernel

**Status:** exact bounded counterexample; no capable-model inference; no representation win. Run108's synthetic 161-task benchmark remains retired as a primary discriminator.

## Theorem (fixed contract and patch grammar)
Let S be semantic states, P permitted patch expressions, A trusted authority, T a target contract, and Accept(s,T,A,p) the independent verifier. Define the repair signature R(s) = (Accept(s,T,A,p)) for every p in P. A view V(s) is sufficient for deciding patch admissibility **if and only if** V(s)=V(t) implies R(s)=R(t). Proof: the implication makes R a well-defined function of V; a counterexample pair forces any view-only decision rule to err on at least one state.

For injective semantic graph and indexed Python views of the same state, both have identical optimal decision accuracy and conditional entropy. Invertible recoding cannot reduce Shannon conditional entropy. Any capable-model advantage must be resource-bounded search/attention/layout, not extra information.

## Executed exact counterexample
Enumerated 16 Boolean functions of two inputs for each of two historical versions and a target, with three nonempty trusted capture scopes: 16^3 * 3 = **12,288 states**. Shared patch grammar: capture(v0) or capture(v1); a patch succeeds iff the version is authorized and its function equals the target.

- Full semantic graph: 12,288 view classes, 0 ambiguous, 100% Bayes-optimal repair-signature accuracy.
- Fully indexed Python: identical.
- Omit historical node: 512 ambiguous classes, 512 Bayes-optimal errors.
- Omit capture authority: 496 ambiguous classes, 512 errors.
- Extensional deduplication of historical versions: 720 ambiguous classes, 720 errors.
- Omit target commitment: 768 ambiguous classes, 1008 errors.

Minimal historical witness: states (v0=0000,v1=0001,target=0000,scope={v0}) and (v0=0010,v1=0001,target=0000,scope={v0}) share current version, target and scope but differ in permitted successful capture. Authority witness: v0=v1=target=0011 with scope {v0} versus {v1} has the same function but different permitted version ID.

These are fixed finite Boolean witnesses, not independent realistic repository tasks, and do not show model superiority. Four local tests passed. The result is an application of established observational-equivalence reasoning, not a novel general theorem.

## Exactly one active causal kernel: K-SYNTH-1
1. Intervention: explicit versioned graph with exact function-level commitments, captures and trusted authority.
2. Control: indexed SSA Python with identical versions, commitments, facts, authority, compiler/verifier and JSON patch grammar.
3. Capable model: Qwen2.5-Coder-7B-Instruct on no-cost public compute; second model if possible. **Not run here.**
4. Tasks: prospectively frozen independent realistic multi-file repairs. **Not yet frozen.** Synthetic Run108 tasks excluded.
5. Scalar: paired first-attempt independently verified target repair success, IR minus Python.
6. Alternative: salience/indexing/token truncation/unequal facts.
7. Falsification: Python matches or beats graph at useful-effect precision, or layout-only ablation eliminates gain; after two matched reformulations pivot to semantic compiler/editor.
8. Unseen prediction (before any holdout): graph advantage, if any, grows with functionally equivalent historical aliases under narrow capture scope; disappears with unique versions and unrestricted captures.
9. Publication: powered real tasks, independent verifier, two capable models, mechanism ablation, unseen prediction, uncertainty, adversarial controls, reproduction and primary prior art. **Not met.**
10. System consequence: preserve historical version IDs, full function commitments and trusted authority. Never collapse equal-function historical nodes when capture rights differ. Measure bounded search cost, not Shannon entropy.

Power before inference: two-sided exact McNemar alpha=.05, assumed P(IR-only)=.20, P(Python-only)=.08, independent pairs, 80% power requires **n=161** (computed power 0.8016). Correlated synthetic variants do not count. No powered inference performed.

Prior art: Gaifman & Shapiro, POPL 1989 (DOI:10.1145/75277.75289), observational/full abstraction; information-theoretic invertible data-processing equality; Jimenez et al., SWE-bench, ICLR 2024 (arXiv:2310.06770) for realistic repository repair.

Smallest supported claim: exact capture-patch admissibility requires retaining version identity, function commitments, target and trusted authority in this bounded model. Lossless graph and indexed Python are information-equivalent. No representation-specific performance result.
