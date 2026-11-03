# Run452: exact clustered-null counterexample for paired repair studies

## Result

Constructed an executable finite enumeration proving that an issue-level exact sign test can report a nominal one-sided p=1/256 when the correct repository-cluster null gives p=1/16 for the *same eight observed IR wins*. Four independent repositories each supply two perfectly correlated repair issues. Under the null, each repository independently favors IR or Python with probability 1/2. The eight issue-level outcomes therefore contain only four independent signs.

The complete null distribution of IR issue wins is 0:1/16, 2:4/16, 4:6/16, 6:4/16, 8:1/16. The event of eight wins has probability 1/16, **not** 1/256. The naive issue-level tail is artificially 16 times smaller. The general construction for r repositories with m perfectly correlated issues per repository gives correct all-win probability 2^(-r) and naive probability 2^(-rm), inflation factor 2^(r(m-1)).

## Executable artifact

`run452_cluster_null.py` uses only CPython standard-library `itertools` and `fractions`, enumerates all repo-level sign assignments, and includes exact rational assertions plus a 1..8 repo by 1..4 issue parameter sweep (32 cases). Reproduce with `python3 research/K-SYNTH-1/run452/run452_cluster_null.py`.

## Interpretation

This is a **constructed mathematical counterexample**, not empirical Lattice model output, a third qualified production repair, or evidence of IR superiority. The perfect-correlation construction is deliberately extreme but suffices to disprove automatic issue-level independence. Repo-cluster-aware design and analysis must be specified prospectively; the intended 400–800 issues across 100–200 repos are not 400–800 independent samples without assumptions. An exact repo-level sign test itself requires independent and suitably exchangeable repo signs; heterogeneous, unbalanced clusters require more careful randomization or hierarchical inference.

## Next decisive experiment

Prioritize a new independently qualified real two-production-source public PR with frozen heldout/nonregression tests, and genuinely paired capable-model repairs with shared isolated oracle, equal task facts, actual distinct semantic/dataflow IR versus Python/AST actions, and raw outputs. Do not use reference-derived localization. Preserve all 89 sealed issues. Existing two qualified tasks unchanged. No claim of breakthrough.

## Infrastructure

GitHub-only source artifact and report on canonical branch; local container was unavailable during this run, so code was not executed in a local CPython runtime and no SHA-verified local archive is claimed. The mathematical distribution was derived exactly in the report and encoded as assertions. No inference was run.
