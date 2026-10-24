# Run222 representation-identifiability proposition

**Proposition.** Let X be a random repair task, F(X) the common disclosed source/task facts, and R1,R2 mutually invertible encodings of those facts. Suppose both arms share authorized actions A, compiler C, and correctness Y(X,C(a)). If all measurable decision policies are admissible and computation is unrestricted, then the supremum of expected correctness over policies observing R1(F(X)) equals that over policies observing R2(F(X)).

**Proof.** For any policy pi1, construct pi2 = pi1 ∘ R1 ∘ inverse(R2). The two policies induce the same action for every task. Their correctness agrees pointwise. Reverse the construction for the opposite inequality. QED.

**Limitation.** A finite-context transformer need not attain the unrestricted optimum. Information equivalence does not imply equal bounded-model accuracy. If Lattice gains an advantage with matched edit authority, the mechanism must involve inductive/computational bias, token placement, dependency locality, intermediate-state validity or verifier-repair behavior, not extra task information. If one arm has a more powerful operation primitive, the matched-action premise fails.

**Exhaustive counterexample (16 tasks).** For four equiprobable binary variables (y,n1,n2,n3), the correct action is y. Encoding IR=(y,n1,n2,n3) and Python=(n1,n2,n3,y) are bijections with identical information. A full four-symbol observer reaches 100% optimal accuracy under either encoding. A one-, two-, or three-symbol prefix observer reaches 100% for IR and 50% for Python. This is an elementary representation-boundary witness, **not** a novel programming-language theorem or a capable-model coding result.

**Unseen prediction, not yet tested:** Counterbalancing dependency-relevant information position should attenuate or reverse a representation advantage if bounded context placement is causal. Measure actual prompt tokens and truncation. Do not attribute representation effects to semantics without such controls.

Local reproducibility: `representation_identifiability.py` and `RUN222_REPRESENTATION_THEOREM_TRACE.json` in the Run222 archive.
