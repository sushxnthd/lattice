# K-SYNTH-1 Run199 — 480 real multi-file issues prospectively frozen

**2026-10-23. This is a sampling and power result, not a capable-model inference result.**

## Actual cloud execution

The first strict 4-per-repository design yielded **188 eligible issues from 47 repositories**, so it was correctly marked **underpowered**. All 188 public and evaluator-only records were retrieved, independently hashed, and verified. A separate outcome-blind availability audit showed that the same eligibility predicate supports 196 repositories with >=1 issue, 119 with >=2, 74 with >=3, and 47 with >=4.

**Before any model inference on these real tasks**, the preregistered variable-cluster v2 selector kept the same eligibility rules, seed and pinned dataset revision, but allocated issues round-robin across repositories (maximum six per repository). The completed no-cost cloud run froze **480 real Python multi-file repair issues from 196 independent repositories**, including **391 discovery issues and 89 boundary issues** from 39 held-out repositories. The actual repository cluster sizes are 77×1, 45×2, 27×3, 11×4, 28×5 and 8×6. This is a realistic sampling frame, not a claim that a model can solve the issues.

Pinned source: `PrimeIntellect/SWE-rebench-V2`, immutable revision `8851474cc41be8bce981362d1363d9f92e247b4b`.

**Independently verified SHA-256:** public tasks `f615b8c5f4f7e4b1996992105515b3e15e9678fb57a3cc0cff5cf1aef64641f2`; sealed evaluator records `cb25318456e4264ac2d8890df0b4f73d7ebe8d407e2ef64919390267c5d695f2`. Both archives were downloaded and independently checked. Public tasks contain no gold patch, test patch, gold-derived file localization, or FAIL_TO_PASS/PASS_TO_PASS IDs; no repository appears in both splits.

Cloud v1: https://github.com/sushxnthd/lattice/actions/runs/39970961944

Cloud v2: https://github.com/sushxnthd/lattice/actions/runs/39971628595

## Empirical power sensitivity on actual unequal cluster sizes

A separately implemented, **20,000-replication**, outcome-blind simulation using the observed 196 repository sizes, 30% paired discordance, beta-distributed repository directional ICC=0.5, and a two-sided repository-level t test at alpha=.05 gave:

- Null rejection: **0.0486** (MC SE 0.00152).
- Power if P(IR wins | discordance)=0.65: **0.8139** (MC SE 0.00275).
- Power if P(IR wins | discordance)=0.60: **0.47435** (MC SE 0.00353).

The design reaches 80% power **only for the specified large hypothetical advantage**. It is not adequately powered for smaller effects, and no empirical representation effect has been observed. The cluster-aware analysis is mandatory; a naive 480-independent-issue McNemar test is invalid.

## What remains missing

**No model completion has been generated on these 480 tasks.** The current Lattice compiler handles bounded Boolean DAGs, not general Python multi-file edits. The next decisive run must implement and validate a common multi-file edit compiler/verifier, construct lossless information-equivalent IR/Python presentations and a conventional AST-action baseline, establish model positive controls, freeze prompts and inference settings, then execute the paired no-cost open-coding-model comparison. Capture all raw outputs, seeds, token counts, traces, failures, and uncertainty. Mechanism ablation and a frozen unseen-boundary prediction follow only after credible model performance.

This v2 revision was made after observing **task availability only**, not any real-task model outcome. The original 188-task v1 artifact remains unchanged and available. No breakthrough or representation-superiority claim is made.
