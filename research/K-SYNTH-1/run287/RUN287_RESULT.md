# K-SYNTH-1 Run287: original Run285 recovery and binding counterexample

Date: 2026-10-27 IST. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, one open/draft/unmerged PR #9. All 89 reserved boundary issues remain SEALED.

## Recovered original GitHub evidence

Original [Run285 Actions 40460886503](https://github.com/sushxnthd/lattice/actions/runs/40460886503) completed successfully; artifact ID `12717163598`, ZIP SHA-256 `8486f65cf7731a73a08a6a09c190ef5b39fbcfd6cfe09ea09279ef5090b215c7`. Independently checked 3/3 original manifest entries and every raw outcome against unchanged prospectively frozen `FROZEN_RUN285.json` SHA-256 `811e33423dc734ab5d0fbe72de4e9c5277b68bed86315b9e7373c01b157be571`.

**Result: 120/120 executed public-API observations match the frozen predictions, 0 censored, 0 disagreements**, across baseline, sync-only, async-only and full-reference (30 each). This recomputes the outcomes rather than trusting the artifact's success flag. Source SHA-256 declarations match the freeze, but the four upstream source files were **not independently downloaded and rehashed** in this run. The independent cloud oracle is not byte-identical to the original local generated oracle. The local generator's oracle SHA-256 `6cdaf1ec4b19e03cd1c3288410f0cf417ea92ede826822288c5ae7a0b509dffe` was separately reproduced.

This is an additional within-issue holdout for already qualified HTTPcore PR1000, **not a fifth independent issue**. Preserve Run283's 8/32 failed predictions and Run284's 72/72 successful predictions unchanged.

## New executable identifiability counterexample

The exact same two expression texts/ASTs, `len([connection.is_idle() for connection in connections]) > threshold` and `sum(connection.is_idle() for connection in connections) > threshold`, produce opposite comparison outcomes under different runtime environments. With two exact Boolean `True` values and threshold 1, ordinary builtins yield old=True/new=True; shadowing `len` to return zero yields old=False/new=True. With integer-returning predicates `2,2` and threshold 3, old=False/new=True, violating the exact-Boolean theorem if its type assumptions are omitted.

Thus **expression-only AST/source cannot identify exact runtime behavior across arbitrary bindings**. This is not an impossibility theorem for verified whole-program semantics. Run286's bounded IR must continue returning `UNKNOWN` without trusted builtin binding, pure exact-Boolean predicate, stable iteration and integer threshold evidence. Independently tested 5,000 exact-Boolean random cases: 0 theorem mismatches; 9/9 local tests passed.

## Limitations and next step

Four independently qualified real issues, no new coding-model completions or functional model repairs, no powered IR-versus-Python advantage, and no breakthrough. Full historical GitHub ZIP mirroring remains incomplete; original SHA-verified artifacts are preserved locally. Next: genuine gold-blind paired capable-model IR/Python repair with common atomic compiler and isolated oracle, additional independent repository clusters, and binding provenance tests. All 89 sealed issues untouched.
