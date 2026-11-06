# Run544 — exact clustered sign-flip counterexample

This run constructs eight synthetic repositories with four perfectly correlated paired outcomes per repository. Exact repository-level sign-flip inference is compared with an invalid issue-independent sign-flip analysis.

With seven positive repositories and one negative repository, naive issue-level two-sided p is below 0.05 while exact repository-level p exceeds 0.05. Duplicating each repository's outcomes 1, 2, 4, or 10 times leaves the exact cluster p unchanged. This is a finite counterexample to treating duplicated issue outcomes as independent evidence. No production task qualified; no coding-model inference; no IR superiority claim. The 89 reserved issues remain sealed.

Reproduce: `python research/K-SYNTH-1/run544/experiment.py`. Synthetic design and tests only; neither a calibrated cluster bootstrap nor a powered evaluation.
