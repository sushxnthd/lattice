# Run171 proof: restricted semantic repair is NP-complete

Decision problem: given a finite, side-effect-free, acyclic multi-file Python project with editable Boolean-constant root functions, immutable protected outputs, and a requested change to a target Boolean root, decide whether an atomic authorized patch can satisfy the target while preserving all protected outputs.

NP membership: a certificate gives one Boolean literal for each editable root. The acyclic Boolean program and protected outputs are evaluable in polynomial time.

Reduction from 3SAT: for each variable x_i create a separate editable module with a Boolean-returning value() function. For each clause C_j create a fixed guard module with protected() returning goal() or C_j(values). Initially goal() returns True, so every guard is True. Require an authorized patch making goal() False while preserving every guard. This patch exists exactly when all clauses can simultaneously be satisfied. The construction is polynomial, acyclic, and has fixed edit grammar and authority. Therefore the restricted repair-feasibility problem is NP-complete.

This is a standard application of SAT complexity, not a novel theorem. Consequence: dependency reachability and per-root influence alone cannot decide joint repair feasibility. Lattice needs constraint scopes/hyperedges over editable roots. Standard treewidth-bounded CSP dynamic programming gives tractable subclasses when a width-w decomposition is available, with complexity polynomial in project size and exponential in w.

Validation: 500 randomly generated 3CNF formulas with exhaustive assignment checks, zero mismatches; 16 independently executed isolated CPython multi-file before/after programs matched the clause evaluator. Explicit satisfiable and unsatisfiable cases passed. Full reproducible script, traces summary, and hash manifest are in the Run171 evidence archive, but executable files could not be committed through the repository connector.

Primary sources: Cook (1971) SAT NP-completeness; Karp (1972) polynomial reductions; Freuder (1990) bounded-treewidth CSP algorithms.

No capable-model inference or IR/Python comparison occurred. Smallest supported claim: a sound semantic editor must preserve relational joint constraints; no representation advantage is established.
