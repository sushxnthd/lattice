# K-SYNTH-1 Run392: exact cluster inference, weak-null counterexample, and PR5126 freeze

Date: 2026-10-31 UTC. One kernel, one draft PR #9, 89 reserved boundary issues sealed.

## Verified statistical finding

Run391 showed issue-level McNemar inference becomes anti-conservative under within-repository dependence. Run392 implemented an exact integer-arithmetic repository sign-flip p-value using subset-sum dynamic programming. It requires **independent, fair repository-level arm-label sign flips conditional on observed magnitudes**, a *sharp exchangeability null*, not merely a zero population-average IR-Python advantage. This distinction is decisive.

A fully enumerated **weak-null counterexample** uses 20 independent repositories, each with signed repair total +5 with probability 1/6 and -1 with probability 5/6. The population mean is exactly zero: 5*(1/6)-1*(5/6)=0. Nonetheless, the exact two-sided repository sign-flip test at nominal alpha=.05 rejects with probability **487226555297351/3656158440062976 = 0.13326188218718407**. This is not a simulation estimate. It is an exact rational sum of all 21 possible counts of +5 repositories, weighted by their binomial probabilities. Consequently the cluster sign-flip test must not be called a universally valid test of the weak mean-zero null.

The original Run391 counterexample (two repositories with eight perfectly correlated wins each) is reproduced: issue-level McNemar p=1/32768, exact repository sign-flip p=1/2. Eight independent positive repositories give sign-flip p=1/128.

## Independent verification

Eight regression/adversarial tests passed, including 1,100 deterministic brute-force enumerations of sign patterns (k=0..10), zero and heterogeneous clusters, permutation and sign invariance, and 200-repository integer counting. A separately implemented Counter-based signed-polynomial convolution audited all 21 exact weak-null configurations and 128 frozen original Run391 trials (rows 4, 5, 12, 13, first 32 each) with zero disagreements. Frozen reanalysis rejection counts (exact sign-flip versus cluster t) were 0/32 vs 0/32, 20/32 vs 21/32, 2/32 vs 2/32, and 21/32 vs 22/32 respectively. These are diagnostic subsets of the *same synthetic simulations*, not new model outcomes or general power estimates.

## New real-production candidate: urllib3 PR5126

A prospective oracle protocol was committed **before reading the reference patch** as commit `3b951406391805a2fb8bd95710dc8e0401fe9211`. Candidate: [urllib3 PR #5126](https://github.com/urllib3/urllib3/pull/5126), pinned base `e349d97f2bf234b95d5dd9e689d056a521dfc3b0`, head `580df2aab0340c2f81cf2770012875e4530a101d`; base Git blobs `connectionpool.py` `7556b50f6d685bdb30e7afac11484a05ef07b767` and `poolmanager.py` `007b31dcfe8aae4f24bebff8bfafa1a06a7bd3eb`. The reference patch subsequently showed two production-file changes: it introduces `_is_same_host` in connectionpool and imports/uses it in poolmanager, with a Host recomputation change. This supports a *static cross-file dependency hypothesis* only. The frozen socket-level public/heldout/control oracle and all four source ablations have **not been executed**; candidate is **NOT qualified**. The public PR description itself contains implementation hints, so this candidate is unsuitable for a blind model comparison without an independently prepared reference-excluded issue statement. No source-derived localization may be provided to model arms.

## Decision

The primary study must predeclare its estimand and null: if testing mean repair advantage, use an appropriate independent-repository cluster-robust approach with sufficient repositories, and treat sign-flip as a sharp-null sensitivity analysis unless exchangeability is justified. Do not pool frozen Run391 simulations with model outcomes. No new coding-model inference, real functional repair, qualified task, IR superiority, or breakthrough is claimed. Historical qualified cohort unchanged. Full executable and raw evidence is in the local SHA-verified Run392 archive.
