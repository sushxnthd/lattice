# K-SYNTH-1 Run350 — exact clustered-McNemar falsifier and prospective inference guard

Date: 2026-10-29 UTC / 2026-10-30 IST. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole open/draft/unmerged PR #9. All 89 reserved boundary issues SEALED. This run adds **new statistical research**, not a new coding-model completion, production-repair qualification, or semantic-IR superiority claim.

## Why this matters

The Lattice primary target is a powered, real-repository, paired semantic-IR versus information-equivalent Python/AST-action comparison. Earlier nominal two-sided exact McNemar planning gives n=306 optimistic or n=681 moderate **if discordant issues are independent**. Multiple issues from the same repository can share conventions, APIs, dependencies, model behavior and patch difficulty. Treating them as independent can produce false discoveries even with correctly computed issue-level exact p-values.

## Exact finite-sample counterexample, not a Monte Carlo estimate

Construct eight independent repositories with four discordant issues each. Under the null, each repository independently chooses one fair sign; all four issues within that repository have that sign (perfect within-repository correlation). Enumerate **all 2^8 = 256 equally likely null assignments**. The issue-level two-sided exact McNemar test rejects at alpha .05 in **74/256 = 28.90625%** of null assignments. An exact two-sided repository sign-flip test rejects in **2/256 = 0.78125%**. This is a complete null enumeration, not a fitted or estimated effect. A single repository with eight all-IR-win issues yields issue-level p=0.0078125 but repository sign-flip p=1.0.

**Proof of resolution floor.** With K nonzero independent repository scores and an exact two-sided sign-flip test, the most extreme attainable event consists of the two sign vectors yielding maximal positive and negative absolute sums, giving minimum p = 2/2^K = 2^(1-K). Consequently K<=5 informative repositories cannot produce a two-sided p<.05 under this test, regardless of the number of duplicated issues within each repository. This is a necessary condition, not a sufficient condition for adequate power. If repository effects are not sign-exchangeable under the null, even the cluster sign-flip p-value is not guaranteed valid.

## Frozen beta-binomial null simulation

Pre-registered 12 cells: repositories R=8/16/32, four discordant issues per repository, within-repository sign ICC rho=0/0.1/0.3/1.0, 2,000 deterministic-seed trials per cell, 24,000 raw trials total. Marginal IR/Python win probabilities are each 0.5, with independent repositories. For 0<rho<1, latent repository win probabilities are Beta(a,a), a=(1-rho)/(2rho); rho=0 is independent fair signs and rho=1 is one shared fair sign per repository.

| Repositories | ICC | Issue-level exact McNemar false-positive rate | Cluster sign-flip false-positive rate |
|---:|---:|---:|---:|
| 8 | 0.0 | 2.15% | 0.80% |
| 8 | 0.1 | 4.60% | 1.25% |
| 8 | 0.3 | 9.10% | 2.15% |
| 8 | 1.0 | 28.75% | 1.15% |
| 16 | 0.3 | 13.40% | 4.00% |
| 32 | 0.0 | 3.80% | 3.10% |
| 32 | 0.1 | 7.95% | 3.95% |
| 32 | 0.3 | 13.85% | 3.65% |
| 32 | 1.0 | 38.90% | 1.55% |

The complete 12-cell table and Wilson 95% intervals are in the local `RUN350_SUMMARY.json`; every trial and p-value is in `RUN350_RAW_NULL_TRIALS.jsonl`. Discreteness explains conservative cluster rejection rates. These ICCs are **hypothetical**, not estimated from Lattice outcomes; the simulations do not imply a real IR effect or a measured type-I rate on production issues.

## Independent audit and falsification

Independent SciPy binomial p-values and NumPy generating-function cluster p-values exactly reproduced **48,000 recorded p-values** across all 24,000 trials, all 12 aggregate cells, and the 256-vector exact null. Parent Run349 original ZIP passed 11/11 SHA-256 entries. Thirteen tests passed; three adversarial raw-data mutations (issue p, cluster p, and repository score) were rejected. The frozen protocol predates the simulations.

## Design consequence and immediate next work

Preserve repository IDs, report discordant pair outcomes by repository, preregister repository-aware inference and sensitivity to issue correlation, and power by independent repositories rather than treating all issue pairs as iid. The historical cohort remains **eight reference-qualified PRs across seven repositories**, with no powered model comparison. Next run must prioritize a genuine no-cost Qwen paired pilot on frozen Jinja #1242 and HTTPcore #882 using Run348 verified local-dataflow facts, explicit UNKNOWN runtime edges, an information-equivalent Python/AST arm, actual tokenizer counts, shared atomic compiler and isolated functional oracle. Do not count this statistical calibration as a model outcome or use it to claim semantic-IR superiority.

Raw local ZIP includes the exact enumerator, frozen protocol, complete simulation, independent auditor, all tests, source provenance and the original parent archive. Full historical GitHub ZIP mirroring remains incomplete. Do not modify the 89 sealed issues or merge PR #9.
