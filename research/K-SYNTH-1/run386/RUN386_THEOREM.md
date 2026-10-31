# Run386 bounded effect-trace completeness theorem

For target inputs `i ∈ {00,01,10,11}` and producer interventions `t ∈ {0,...,15}`, let `F_i(t)` be the ordered sequence of trusted `emit(tag,bool)` events followed by a tagged Boolean return or `ValueError(message)` outcome. All admitted programs are loop-free and statically restricted to Boolean expressions, local assignments, conditionals, `p` calls, bounded `emit`, and terminal outcomes. Any unsupported syntax, missing terminal, invalid type or exhausted bound yields `UNKNOWN`.

Let `O` be the deterministically ordered finite alphabet of observed traces. For each input `i` and outcome `o∈O`, define `G_{i,o}(t)=1[F_i(t)=o]`. Encode each 16-element Boolean indicator by its unique GF(2) algebraic normal form. Inverse Möbius transformation reconstructs every indicator. Since indicators are one-hot at every intervention, this reconstructs exactly all 64 `F_i(t)`. Thus equality of full certificates is equivalent to equality of all finite observed trace/outcome pairs in the admitted domain.

**Counterexample:** `a=p(x,y); if a: emit('audit',True); return False` and `return False` have identical Boolean return-only ANFs for all interventions and target inputs, but different event traces whenever the selected producer truth-table bit is true. Return-only semantic equivalence does not imply effect-trace equivalence, even in this deterministic finite grammar.

**Scope:** This is not a theorem for unrestricted Python, dynamic effects, files, networking, timing, concurrency, or producer implementation effects. It does not identify causal effects from observational traces without the stipulated interventions. The synthetic corpus is a test of this bounded theorem, not model utility or production repair performance.
