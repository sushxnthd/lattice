# Run384 bounded exact input-indexed causal support

Let `F_i(t)` be the Boolean output of the admitted pure consumer's target at input index `i` under a four-bit producer truth table `t`. The analyzer returns UNKNOWN if source parsing fails or any of the 64 evaluations does not terminate.

For producer-input bit `j`, define `S[i,j]=1` exactly when some `t` with bit `j` zero satisfies `F_i(t) != F_i(t XOR (1<<j))`.

**Theorem:** For admitted total sources, exhaustive checking of all eight four-dimensional hypercube edges in dimension `j` computes each `S[i,j]` exactly. Positive entries have a directly checkable single-bit intervention witness. Negative entries certify invariance to producer bit `j` for target input `i` under every assignment of the other three bits. All 16 entries zero iff the target is globally producer-independent.

**Proof:** Run383's restricted interpreter is extensionally equal to CPython for terminating programs in the admitted grammar. The eight hypercube edges enumerate every possible one-bit change at fixed other producer bits. Each witness is a differing edge. If no edge differs along a dimension, the output is invariant along that dimension. Hypercube connectivity means invariance in all four dimensions implies constant output over all 16 truth tables, for each target input.

**Cross-input counterexample:** `target(x,y): return produce(y,x)` yields support rows `1000,0010,0100,0001`, where target input `01` depends on producer input `10`. Same-input-only analysis is unsound.

**Scope:** exact only for strict pure Boolean AST grammar, all-total interventions and two Boolean parameters. Not unrestricted Python, actual fixed-producer behavior, production repair, or model superiority.
