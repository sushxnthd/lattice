# K-SYNTH-1 Run323: repository-clustered paired-power calibration

Date: 2026-10-28 UTC. Pre-execution protocol commit `086c6cf59fdf197c718de5cdb196da4c3fe0ae5d`. Exactly one open/draft/unmerged PR #9. All 89 reserved issues sealed. Six previously qualified historical production repairs unchanged. **No coding-model inference was performed.**

## Frozen design

The existing optimistic McNemar plan assumes 306 independent issue pairs (discordance .30, conditional IR win .65); the moderate plan assumes 681 (.30, .60). We simulated repository-dependent signs of discordant pairs, with per-repository conditional win probabilities q_r ~ Beta(qk,(1-q)k), k=1/rho-1, or constant q at rho=0. Repository sizes balanced; 1200 PCG64-seeded replicates per cell; seed 3232026; two-sided alpha .05. Primary issue-weighted paired difference tested using repository-cluster-robust t statistic with m-1 degrees of freedom. Comparator is naive issue-independent exact McNemar. **This is an assumed sensitivity model, not estimated real-repository ICC.**

| Design | Conditional sign ICC | Cluster-aware power | Naive alternative rejection | Cluster-aware null rejection | Naive null rejection |
|---|---:|---:|---:|---:|---:|
| 306 issues / 102 repos, q=.65 | 0 | 82.9% | 80.3% | 4.8% | 3.8% |
| 306 / 102, q=.65 | .10 | 80.7% | 80.3% | 4.9% | 3.9% |
| 306 / 102, q=.65 | .30 | 75.8% | 78.3% | 4.7% | 5.2% |
| 681 / 170, q=.60 | 0 | 79.4% | 77.3% | 4.9% | 3.7% |
| 681 / 170, q=.60 | .10 | 76.9% | 78.1% | 5.9% | 5.8% |
| 681 / 170, q=.60 | .30 | 71.0% | 75.8% | 4.1% | 6.8% |
| 800 / 200, q=.60 | 0 | 86.8% | 86.0% | 5.2% | 4.8% |
| 800 / 200, q=.60 | .10 | 83.0% | 83.3% | 5.0% | 5.4% |
| 800 / 200, q=.60 | .30 | 75.8% | 81.7% | 6.1% | 9.5% |

At n=800, rho=.30, cluster-aware power was 75.8% (Wilson 95% Monte Carlo interval 73.3–78.2%), while the naive test rejected 81.7% under the alternative **but also 9.5% under the null** (95% interval 8.0–11.3%). The cluster-aware null rate 6.1% has interval 4.9–7.6%; exact 5% calibration is not established. The moderate 681/170 design at rho=.30 had 71.0% cluster-aware power (95% interval 68.4–73.5%). Neither original n is universally sufficient.

## Analytical mechanism

For D=+1 (IR-only), -1 (Python-only), 0 (concordant), with discordance p=.30, mean conditional IR win q, and Beta conditional-sign ICC rho:

- E[D]=p(2q-1)
- Var(D)=p-p²(2q-1)²
- Cov(D_i,D_j)=4p²q(1-q)rho within repository.

At the null q=.5, Corr(D_i,D_j)=p*rho, so rho=.30 implies unconditional paired-effect ICC=.09. Four issues per repository give approximate design effect 1+3(.09)=1.27; n=800 corresponds to roughly 630 independent-issue variance equivalents. This is model-specific, not a universal power theorem.

## Evidence and decision

**21,600 raw synthetic replicates** across 18 cells. An independently implemented auditor recomputed repository scores, exact binomial p-values, cluster t p-values and all aggregate counts with **zero discrepancies**. Raw JSONL SHA-256: `f67848358b004f64bdd39a90a490694b23c1b4666e58ff0159f0afb1d4960bd4`. Full raw traces and independent auditor are retained in the SHA-verified local Run323 archive.

Limitations: balanced cluster sizes, independent discordance indicators, hypothetical Beta heterogeneity, no issue-difficulty dependence or informative cluster sizes. Monte Carlo uncertainty matters. Do not pool these synthetic replicates with real model repairs or claim semantic-IR superiority.

Next: freeze a real paired capable-model pilot to estimate discordance and repository dependence before declaring the full study powered. Identical facts/source/authority/compiler/oracle for semantic IR and ordinary Python/AST. Preserve model SHA, prompts, seeds, raw completions, refusals and failures; do not give gold-derived localization. Recruit an independent seventh qualified multi-production-source public repair.