# Run453 — exact cluster randomization audit

2026-11-03. This is a constructed statistical counterexample, **not** new coding-model evidence or a newly qualified repair.

## Independently executed local result

An independent CPython standard-library implementation completed 84 assertions. For six independent repositories with three perfectly correlated discordant issues per repository, all favoring IR, the repository-level exact one-sided sign-flip p-value is 1/64 (0.015625), while treating 18 issues as independent gives 1/262144 (0.000003814697265625). The false issue-level p-value is 4096 times smaller.

For six repositories, four favoring IR and two favoring Python, each containing ten perfectly correlated discordant issues, the repository-level sign-flip p-value is 11/32 (0.34375), versus naive issue-level P(Binomial(60,0.5)>=40) = 3888024206162357/576460752303423488 (~0.00674). Thus a nominally significant issue-level result can be nonsignificant at the repository level.

## Scope

This randomization test assumes independent exchangeable repository clusters under a sharp null. It is not automatically valid under arbitrary cross-repository dependence or heterogeneous effects. No prospective real paired model outcomes were acquired. No claim of IR superiority is warranted. The primary powered multi-repository benchmark remains incomplete; only Flask PR6096 and urllib3 PR5071 are independently qualified. Do not promote previously failed Werkzeug candidates.

## Reproducibility

The executable is `run453_cluster_randomization.py`; run with `python run453_cluster_randomization.py`. Local implementation executed successfully. The GitHub copy implements the same exact fractions and checks. Local independently generated outputs were SHA-256 hashed, but are not yet mirrored to GitHub. No untrusted model code was executed.

## Next

Prioritize new prospectively frozen two-production-source repair qualification and actual paired open-model functional completions. Preserve all 89 sealed boundary issues. Keep one K-SYNTH-1 kernel, branch `research/exp003-context-order`, and draft PR #9 unmerged.
