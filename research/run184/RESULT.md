# Run184 — authorized-edit congruence of semantic representations

Scientific status: finite-state theorem/counterexample and exhaustive validation; not a novel theorem, not capable-model inference, and not evidence of IR superiority. Sole kernel: K-SYNTH-1.

## Exact theorem

Let S be finite concrete states, O:S→V protected observations, and T_a:S→S the deterministic semantics of each currently authorized edit a∈A. A compressed representation R:S→Q has exact induced observations and transitions if and only if:

1. R(s)=R(t) ⇒ O(s)=O(t).
2. R(s)=R(t) ⇒ R(T_a(s))=R(T_a(t)) for every a∈A.

Necessity follows by applying the induced readout/transition to equal abstract states. Sufficiency follows by defining readout([s])=O(s) and transition_a([s])=[T_a(s)]. By induction all authorized edit sequences preserve observations.

The coarsest sound equivalence is s~t iff O(T_w(s))=O(T_w(t)) for every finite authorized edit word w. This is classical Moore-machine/Myhill–Nerode minimization, not new mathematical theory. Expanding the authorized edit alphabet can only refine, never coarsen, the minimal sound quotient.

## Constructive counterexample

Four states have observations [0,0,1,1]. Authorized advance transition is [2,1,2,3] and reset is [0,1,0,1]. States 0 and 1 have equal current observation 0 but after advance have observations 1 and 0. Therefore collapsing states solely on current observations is unsound for edits. Exact partition refinement separates all four states.

## Executed exhaustive experiment

The executable local evidence bundle enumerates all 5,832 deterministic three-state, two-edit Moore systems with binary observations (2^3×(3^3)^2). A separate shortest-distinguishing-word BFS verifies each partition; 542,376 concrete-vs-quotient traces of edit-word length ≤4 agree with zero mismatches. 3,024/5,832 systems have observation-only partitions unsound under edits. Adding the second authorized edit forces a finer exact quotient in 1,080/5,832 systems. These are exact counts for the small universe, not statistical generalization to Python.

## Direct semantic-system consequence

Lattice must version the edit authority alphabet and represent transition/effect distinctions, not only present-value dependencies and protected output snapshots. A semantic quotient must be certified edit-congruent or conservatively retain state distinctions. Expanding edit authority invalidates the abstraction certificate until rechecked. Both graph and executable indexed-Python views must share this canonical semantic core and compiler. Unsupported effects must fail closed.

## Only active representation kernel K-SYNTH-1

1. Intervention: explicit versioned dependency/state graph with commitments and edit-congruent transition/effect structure.
2. Control: executable indexed Python SSA encoding identical facts; same patch grammar, compiler, verifier, edit authority, token budget.
3. Models: planned Qwen2.5-Coder-7B-Instruct and second >=7B open model only if free compute exists; no inference this run.
4. Tasks: >=258 independent realistic prospectively frozen multi-file repairs; prior Run177/179 synthetic corpus invalid. Not yet frozen.
5. Primary scalar: paired first-attempt fully verified repair success, graph minus Python.
6. Alternative: layout/localization/tokenization or unequal retrieval affordance.
7. Falsification: Python equals/beats graph at useful effect, or graph win disappears with equal localization; pivot after two sound matched reformulations.
8. Unseen prediction: graph advantage grows with cross-file branching at fixed frontier and vanishes with equally prelocalized dependency cones; freeze before inference.
9. Publication threshold: powered capable-model prospective result, independent evaluator, ablation, holdout, uncertainty, counterexamples, clean reproduction. Not met.
10. System consequence: authority-sensitive edit-congruent semantic core independent of both text views.

Power plan retained from Run183: n=258 independent pairs for assumed graph-only discordance 0.14, Python-only 0.06, exact two-sided McNemar alpha .05, target power .80. Assumption-dependent, not achieved.

Prior art: https://en.wikipedia.org/wiki/Myhill%E2%80%93Nerode_theorem ; https://doi.org/10.1017/S0960129514000358 ; https://doi.org/10.1145/2951913.2951941

Reproduction evidence: local run184 bundle with executable edit_congruence.py, results.json, stdout.txt, PROTOCOL.json and SHA256SUMS. GitHub executable-write status is recorded separately; no model transcripts/token counts exist.

Smallest supported claim: current-observation equivalence is insufficient for a sound editable IR, and edit-authority expansion can require strictly finer semantic state distinctions. No representation-specific causal advantage established.
