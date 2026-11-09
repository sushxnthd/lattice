# Run597: exact cluster sign-flip correction to Runs595–596
2026-11-09 UTC. K-SYNTH-1. Research-only, no production repair.

**Question:** Does unequal issue count itself invalidate a *cluster-aware* issue-weighted randomization test? **No.** Previous Runs595–596 correctly identified the invalidity of treating correlated issues as independent, but did not establish that *all issue-weighted tests* are invalid. Exact sign-flip randomization at the independent-repository level preserves within-repository dependence even when the statistic is issue-weighted. It tests a sharp symmetric sign-flip null, not an arbitrary common-mean null.

Constructed null: each repository has a fair independent sign; all its issue effects share that sign. Repo sizes [100,1,...,1]. Enumerate all 2^R sign vectors, and calculate two-sided exact sign-flip p-values using either issue-weighted sum or equally weighted repository sum. Reject at p<=.05.

| R | issue-weighted exact rejection | equal-repo exact rejection |
|---|---|---|
| 4 | 0 | 0 |
| 6 | 1/32 | 1/32 |
| 8 | 1/128 | 1/128 |
| 10 | 5/256 | 11/512 |

Both tests remain at or below nominal alpha in these exhaustive null experiments; the naive *issue-independent binomial* test in Runs595–596 does not. Different weighting targets different estimands and can change sensitivity. Neither permutation method automatically supplies a confidence interval for a non-sharp population-average effect or controls arbitrary cross-repository dependence.

**Protocol correction:** distinguish (i) naive issue-level independence, (ii) repository-clustered sign-flip inference under its exchangeability/symmetry assumptions, and (iii) equal-repository estimands. Predeclare estimand, cluster, weighting, null, stopping and uncertainty method. Do not claim issue weighting intrinsically inflates type-I error.

Executable reproducibility: reproduce.py, deterministic exhaustive rational arithmetic, no model inference. No new qualified repair; two qualified tasks remain; all 89 reserved issues sealed. PR #9 remains draft and unmerged.
