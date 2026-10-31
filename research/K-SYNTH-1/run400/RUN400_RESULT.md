# K-SYNTH-1 Run400 — weak-null validity and new issue-first oracle

Date: 2026-11-01 IST. Sole K-SYNTH-1 kernel, canonical branch, draft/open/unmerged PR #9; 89 reserved boundary issues sealed.

## Finite-sample weak-null theorem

For independent repository clusters with prospectively fixed nonnegative weights summing to 1, each bounded repository mean `X_r ∈ [-1,1]`, and estimand `mu = sum(w_r E[X_r])`, Hoeffding gives `P(sum(w_r X_r)-mu >= t) <= exp(-t²/(2 sum(w_r²)))`. Thus a conservative two-sided p-value for the **weak average-effect null** is `min(1, 2 exp(-D²/(2 sum(w_r²))))`, with `D=sum(w_r X_r)`. This does **not** require conditional sign symmetry, but it **does** require independent repositories and a valid sampling/randomization design. It is not automatically meaningful on a handpicked deterministic benchmark.

Run392's exact independent-repository zero-mean counterexample has 20 repository totals +5 with probability 1/6 and -1 with probability 5/6. Exact enumeration shows that a sign-flip test wrongly applied to the weak null rejects **13.3261882%** at nominal 5%. Normalizing each cluster to bounded means +1/-0.2, the Hoeffding test rejects **0.0000179765%**, an extremely conservative but valid result. Executable: [run400_weak_null_exact.py](run400_weak_null_exact.py).

A fresh deterministic beta-mixture simulation with 6,000 trials (four 1,500-trial scenarios, discordance .30, sign ICC .30, eight issues/repo) produced **zero Hoeffding rejections** at 60 repos / 480 issues under p=.50 or p=.65 and at 135 repos / 1080 issues under p=.50 or p=.60. The 95% half-width is 0.3507 at 60 repositories and 0.2338 at 135, compared with expected advantages 0.09 and 0.06. **This is a validity backstop, not a practically powered primary test.** Independent read-only auditor: **36,109 checks**, all 6,000 original trials, zero disagreement. **12/12** regression/adversarial tests passed.

## Issue-first real-library candidate

Froze [pytest issue #14942](https://github.com/pytest-dev/pytest/issues/14942) before reading comments or reference fixes. Reporter described ~10x slower collection on 9.1.1 versus 9.0.3, with many class fixtures. Exact upstream release commits are recorded in [prospective protocol](PROTOCOL_PYTEST14942_PRE_REFERENCE.md). Implemented deterministic source-hashed class-fixture workload and a 2 Python × 2 pytest version no-cost [GitHub Actions workflow](https://github.com/sushxnthd/lattice/actions/runs/41252417259).

Local preflight on installed **pytest 9.0.2 only** collected 160/160 and 640/640 tests, with median times 1.170s and 1.418s over two repeats. This does **not** test the claimed 9.0.3-versus-9.1.1 regression. Original four-matrix workflow was queued at report time. Candidate **NOT QUALIFIED**: no reference repair, source ablations, baseline-passing nonregression matrix or joint behavioral necessity.

## Reproducibility and limits

Local clean-extraction archive SHA-256 `5c34bfb89a6c56996c7904d8aa4c1d607594ea882de1bacbb59bff1e8daa39ea` contains 15 SHA-verified payloads, original 6,000 trial repository totals, exact enumeration, independent auditor, tests, functional preflight and frozen protocol. No new model inference, powered semantic-IR advantage, or qualified production repair. Next priority: recover original performance artifacts, reject nonreproducing candidates without retuning, and conduct genuine information-equivalent semantic/dataflow IR versus ordinary Python/AST-action model repairs with shared isolated oracle.