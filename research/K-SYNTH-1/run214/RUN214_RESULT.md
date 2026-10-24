# K-SYNTH-1 Run214 — CPython observability and unequal-cluster power

Date: 2026-10-24. This is executed compiler science and prospective statistical planning, **not** new coding-model inference or SWE-rebench resolution.

## Six new accepted but behavior-changing renames
The Run213 semantic rename accepted all six CPython witness programs, and independent before/after subprocess execution observed divergent successful results in every case:
1. Decorator registration observes the function representation at definition time.
2. A generator object exposes its originating function name.
3. A returned nested lambda exposes its enclosing function name.
4. An exception traceback exposes the frame's function name.
5. Python logging `%(funcName)s` exposes the frame name.
6. A coroutine object exposes its originating function name.

A conservative Run214 patch rejects all six. **35 regression tests passed**, including previous controls. The patch rejects some safe cases; neither the patch nor closed-world snapshot attestation establishes general Python observational equivalence. External tracing and reflection remain unrestricted counterexamples.

## Recomputed sample size using actual public repository sizes
The 391 discovery issues span 157 repositories, with size histogram `{1:59, 2:35, 3:25, 4:10, 5:21, 6:7}`. Their mean is 2.49045 and coefficient of variation is 0.63061. At assumed ICC 0.5, the unequal-cluster design effect is `1+0.5*(1361/391-1)=2.240409`, versus the Run213 equal-size approximation of 1.745223.

Under the earlier *assumed* effect model (30% discordance, IR wins 65% of discordants, two-sided alpha .05), the previous exact McNemar planning threshold was 306 effective independent pairs. The corresponding unequal-cluster heuristic is **686 nominal paired issues**, not 535. The current discovery split is 295 issues short. The 89 sealed boundary issues must remain untouched.

In a separate 6,000-replicate Dirichlet-multinomial simulation with ICC 0.5 and a repository-cluster t test, prospective power was 59.9% at 391, 70.9% at 535, and 83.4% at 686 (Monte Carlo 95% interval 82.4–84.3%). These are synthetic planning calculations, **not model outcomes**, and depend on strong assumptions.

## Science gate
A genuine semantic-operation IR versus information-equivalent Python baseline, equal edit authority and common compiler/verifier, prospective real multi-file tasks, independent functional tests, open coding model outputs, and mechanism ablation remain missing. Recalculate sample size after actual paired functional discordance is measured.

The local reproducibility archive contains original and patched compiler source, executable witnesses, raw CPython observations, the 391-issue public cohort, 6,000-replicate power code and outputs, test logs, source patch and SHA-256 checksums.