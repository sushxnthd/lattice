# K-SYNTH-1 Run384: exact input-indexed semantic influence

**Date:** 2026-10-31 UTC. **Branch:** `research/exp003-context-order`. **PR:** #9 open/draft/unmerged. **Boundary:** 89 reserved issues sealed.

Run383 established global producer dependence in a bounded pure Boolean Python grammar but could not identify which producer **input** affects which consumer **input**. Run384 computes a 4-by-4 exact influence-support matrix. Each positive entry includes a *single-bit* counterfactual intervention witness. Each negative entry certifies finite-domain invariance to that producer bit, conditional on the strict admitted grammar and termination of all 64 interventions.

**Counterexample:** `target(x,y): return produce(y,x)` gives a non-diagonal support matrix: target input `01` depends on producer input `10`. Same-input-only dataflow analysis misses this influence.

### Original frozen corpus
1,100 original programs and 70,400 previously independently replayed CPython observations were SHA-verified. All support classifications agreed with independent reconstruction from original traces. 374 NO_DEPENDENCE, 165 DEPENDENCE_CERTIFIED, 561 UNKNOWN. The 165 dependent programs have 649 support entries, all diagonal; this reflects original-corpus coverage, not a universal property.

### Fresh cross-input stress
A deterministic new 768-program synthetic corpus (seed 3842026) was generated with helper calls, swapped producer arguments, short-circuit Boolean operators and conditionals. **49,152 original CPython observations** were independently re-executed as **49,152 fresh CPython observations** using a separate AST whitelist, importer and bit-vector support algorithm. Zero trace or support mismatches. All 768 source hashes and 12,288 support cells agreed. Twenty adversarial and regression tests passed.

364/768 programs have influence; 197/768 exhibit cross-input influence; 324 cross-input plus 889 diagonal entries (1,213 total) were verified. Four programs exhibit cross-input influence without diagonal influence.

**Limitations:** This is a bounded finite-domain theorem and synthetic exploratory corpus, not a real-repository repair comparison, model advantage or powered result. No new model inference or qualified production bug repair occurred. Ordinary Python/AST must receive the same derived support and witnesses in any matched experiment.

### Evidence
Local SHA-verified reproducibility ZIP: `lattice_run384_exact_input_indexed_causal_support_and_independent_cpython.zip`; archive SHA-256 `c18ae8bc80c86d7fe8afeeb12bea9894194f6a4ca5aa3d2b9beaeb151c97ecd0`. It contains 15 manifest-verified payloads plus manifest, including executable analyzer, two independent experiments, original corpus, 768 fresh synthetic programs, 49,152 original and 49,152 independent CPython traces, tests, theorem and next protocol. Full raw data is preserved locally, not mirrored to GitHub.

Next: genuinely unseen, independently qualified multi-production-source bug repair and matched model inference with a shared AST-span compiler, isolated oracle, and issue-level clustered analysis. No breakthrough or IR superiority claimed.
