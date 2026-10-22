# Run180 — alias-sensitive contextual equivalence

Status: soundness counterexample, not a novel representation breakthrough. K-SYNTH-1 remains the only active research kernel.

**Theorem (restricted Boolean heap):** For finitely many named roots referencing mutable Boolean cells, with arbitrary `read(root)` and `write(root, bit)` operations, two states are contextually equivalent iff their initial root values and root alias equivalence relations coincide. If alias partitions differ, write the opposite of the initial value of `j` through root `i` for a pair `(i,j)` aliased in exactly one state; reading `j` distinguishes the states. The converse follows by induction on action sequences.

**Executed:** Exhaustively enumerated root partitions and Boolean assignments for 2–5 roots. For every pair of states with equal visible root values but different alias partitions, a one-write/one-read distinguishing witness exists: 4,956/4,956 pairs. A separately implemented mutable-object heap verified 9,912 witness executions. Four-file CPython demo confirmed that mutation and rebinding have different alias effects.

**Consequence:** Canonical Lattice semantic state must include versioned heap-object identity/alias classes and edit-effect types (mutate vs rebind), not merely root values or dependencies. Information-equivalent Python must expose the same alias facts. This is established prior art in alias analysis/separation logic (Reynolds LICS 2002; Landi/Ryder PLDI 1992), not new field-level theory.

**Representation claim:** no capable-model inference occurred, no new realistic 258-task set was frozen, no IR advantage demonstrated. Run179's old synthetic 258-task benchmark is invalid for product-scale claims. Under prespecified McNemar discordance probabilities p10=.14, p01=.06, exact two-sided alpha=.05 80%-power minimum remains 258 independent task pairs. Mechanism prediction to freeze before holdout: if structural grouping helps, the advantage increases with cross-file mutable alias classes and disappears with zero mutable cross-file aliases, matched for depth and tokens.

**Next decisive action:** prospective capable >=7B open/no-additional-cost coding-model comparison against executable Python SSA plus identical alias manifest; identical compiler, patch grammar, edit authority, verifier and token budget; independently sealed heterogeneous multi-file tasks; mechanistic ablation and unseen-condition test. No further CI polish counted as research.

**Provenance:** The complete executable archive with raw enumerations, independent CPython traces, and power calculation was generated outside GitHub in this automation run. Repository write-through is only complete if these files can be committed on this isolated branch. No force-push or auto-merge.
