# K-SYNTH-1 Run371: exact paired-test power and repository clustering

Date: 2026-10-30 UTC. This is a **statistical methodology result**, not a new model inference, production-repair qualification, or semantic-IR superiority claim.

## Independent-outcome verification

Let D~Bin(n,p) be the number of discordant repairs and W|D~Bin(D,q) the IR-only wins. The two-sided exact conditional McNemar rejection event has probability integrated over D and W. The portable executable `run371_exact_power_portable.py` computes:

| n | p | q | Exact power |
|---:|---:|---:|---:|
| 306 | .30 | .65 | .800367 |
| 681 | .30 | .60 | .800498 |
| 400 | .30 | .60 | .558530 |
| 800 | .30 | .60 | .862140 |
| 681 | .20 | .60 | .618009 |
| 681 | .40 | .60 | .903352 |

The **minimum** n for 80% independent-issue power is 306 at (p=.30,q=.65), 681 at (.30,.60), 1021 at (.20,.60), and 510 at (.40,.60). The original n306/n681 plans are mathematically sound under their stated assumptions, not guaranteed when issues cluster by repository.

## Reproducible clustered sensitivity experiment

A separately executed local simulation used D_j~Bin(m_j,p), latent q_j~Beta(q*k,(1-q)*k) with k=1/rho-1, and W_j|D_j,q_j~Bin(D_j,q_j). The 18 scenarios used 1,200 replicates each, seed 37120261030, 399 whole-repository sign flips per replicate. This is **synthetic sensitivity analysis**, not empirical model outcomes.

At n=681, p=.30, eight issues/repository and within-repo discordant-direction rho=.35:

- Under alternative q=.60: naive issue-level exact McNemar rejects **75.08%**, repository sign-flip rejects **56.50%** (MC Wilson 95% interval 53.68–59.28%).
- Under null q=.50: naive exact McNemar rejects **12.08%** (MC Wilson 95% 10.36–14.05%), repository sign-flip rejects **3.67%** (MC Wilson 95% 2.74–4.89%).
- Under null q=.50, the signed discordant score X_i in {-1,0,+1} has Var(X_i)=p and Cov(X_i,X_k)=p²rho within a repository, so equal-size null variance inflation is **1+(m-1)p*rho = 1.735**, not 1+(m-1)rho.

An independent auditor recomputed **21,600** simulated replicate decisions using `scipy.stats.binomtest`; all 18 scenario summaries matched. Six tests passed, including exhaustive finite trinomial enumeration and null sign-flip symmetry. Full local reproducibility archive: `lattice_run371_clustered_mcnemar_power_and_raw_traces.zip`, SHA-256 `9a1d7823083e12460344813b6194638462b8fd20d2bcd7e4583880d1d08a3155`. It contains all raw records, full simulation source, independent audit, tests, report and SHA manifest. The archive is retained outside GitHub until mirrored; do not claim it is already uploaded there.

## Decision and limitations

Use a repository-aware preregistered primary analysis and estimate discordance, effect size, and repository heterogeneity in a blinded pilot. Naive McNemar remains a sensitivity analysis. Cluster sign-flip validity requires repository-level sign symmetry; this simulation does not establish empirical rho or real IR-vs-Python success. Historical cohort remains **9 qualified unique PRs across 7 repositories**, not a powered paired-model cohort. All 89 reserved boundary issues remain SEALED. Sole PR #9 must remain OPEN/DRAFT/UNMERGED on `research/exp003-context-order`.
