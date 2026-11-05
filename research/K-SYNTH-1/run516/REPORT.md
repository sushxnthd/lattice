# Run516: independently cross-checkable cluster sign-flip implementation
Date: 2026-11-05 UTC. Research branch only; all 89 reserved issues sealed.

Added `exact_cluster_oracle.py` with two independently implemented exact distributions: direct enumeration of all repository sign vectors, and a subset-sum dynamic-programming counting oracle. Includes 880 deterministic seeded cross-check cases (11 sizes × 80), and three directed adversarial configurations.

**Analytical results (not presented as executed CI evidence):**
- Eight wins from a single repository: cluster exact two-sided p=1, naive issue-level p=2/256=0.0078125.
- Eight wins from eight independent repositories: cluster p=2/256=0.0078125.
- Seven +1 repository totals and one -10 total: observed sum=-3, and every possible sign combination has magnitude at least 3; cluster p=1.
These calculations assume exchangeable independent repository signs under a sharp null. The latter counterexample illustrates why raw positive-repository counts do not determine the weighted statistic's significance.

**Execution status:** source persisted on GitHub, but local Python execution and SHA archive creation were blocked by runtime errors (SessionLimitReachedError, redis ResponseError). Assertions and 880 cross-checks are *specified*, not claimed as run. Next eligible run must execute them, preserve raw output and independently verify SHA before promoting the artifact as validated. No production repairs or coding-model completions this run; two qualified real repairs only. All 89 issues remain sealed. PR #9 was verified OPEN/DRAFT/UNMERGED on the correct branch at start of run. Do not infer IR superiority.
