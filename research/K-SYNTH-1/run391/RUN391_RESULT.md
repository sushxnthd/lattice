# K-SYNTH-1 Run391 — repository-clustered McNemar power falsification

2026-10-31 UTC. Canonical branch `research/exp003-context-order`, one draft PR #9. All 89 reserved boundary issues sealed.

**Scope:** methodological simulation and exact finite counterexample, **not** new model completions, production repairs, or semantic-IR superiority evidence.

The original independent-issue exact McNemar planning assumptions are verified: n=306, discordance .30, conditional IR win .65 gives exact power **0.8003672484**; n=681, discordance .30, conditional IR win .60 gives **0.8004984160**.

We generated 360,000 original paired-outcome trials across 36 scenarios, with 10,000 replicates per scenario. Independent repositories draw latent conditional IR win probabilities from a Beta mixture; issues within repositories share the latent parameter, with specified conditional sign ICC. Every issue has a discordance indicator and signed IR-only/Python-only outcome. A separately implemented auditor recomputed all original trial p-values and aggregate rejection rates, passing 1,803,564 checks. Ten tests passed. The local archive contains 36 full raw NPZ datasets, code, independent auditor, tests, SHA-256 manifest, and clean-extraction verification.

| Scenario | Naive issue-level McNemar rejection | Cluster-aware repository t rejection |
|---|---:|---:|
| n306, iid null | .0397 | .0512 |
| n306, 8 issues/repo, sign ICC .30, null | **.1034** | .0475 |
| n306, iid p=.65 | .7992 | .8273 |
| n306, 8 issues/repo, ICC .30, p=.65 | .7448 | **.6040** |
| n681, 8 issues/repo, ICC .30, null | **.1110** | .0497 |
| n681, iid p=.60 | .8027 | .8218 |
| n681, 8 issues/repo, ICC .30, p=.60 | .7425 | **.6063** |

The assumed balanced-cluster design effect for eight issues/repository and ICC .30 is 1.589 (optimistic) or 1.612 (moderate). On this specific model, cluster-aware power first exceeded .80 among tested grid points at n480/60 repos for the optimistic effect and n1080/135 repos for the moderate effect. These are illustrative, not universal sample-size minima.

**Exact counterexample:** two independent repositories, each with eight perfectly correlated IR-only wins, yield naive exact McNemar p=3.0517578125e-05, while exact repository sign-flip p=.5. Apparent overwhelming issue-level significance can be pseudoreplication.

**Decision:** n306/681 are not automatically 80%-powered for clustered real-repository tasks. Before a confirmatory paired-model comparison, preregister repository-clustered inference and pilot ICC sensitivity, account for task-family and shared-dependency correlation, and avoid counting multiple issues in one repo as independent. The Beta-mixture is hypothetical, not an empirical ICC estimate; the cluster t procedure also has assumptions and is not universally exact.

Local archive SHA-256: `aa156ca332075f749369660a5a65b9bccedcfb0642743181516a857484761636`. Full GitHub executable/raw mirroring remains incomplete. No new production task qualified and no superiority claim.
