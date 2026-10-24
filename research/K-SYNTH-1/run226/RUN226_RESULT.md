# K-SYNTH-1 Run226 — repository-clustered power sensitivity

Date: 2026-10-24. **Scientific status: statistical planning, not a new capable-model experiment.** This work does not demonstrate an IR advantage.

## Experiment

Executable `cluster_power.py` simulates paired functional successes on four issues per repository. The paired difference is +1 for IR-only success, -1 for Python-only success, and zero otherwise. Discordance is Bernoulli(q); the probability of IR winning a discordant issue varies by repository according to a beta distribution with mean p and latent correlation parameter rho. A two-sided t-test across repository means avoids treating four issues from one repository as four independent units. A fixed seed makes the Monte Carlo replicable.

With q=0.30, p=0.60, 5,000 replicates per setting:

| Paired issues | Independent repository draws (rho=0) | Latent rho=0.3 | Latent rho=0.6 |
| --- | ---: | ---: | ---: |
| 260 | 0.416 | 0.347 | 0.302 |
| 688 | 0.812 | 0.731 | 0.652 |
| 1,024 | 0.941 | 0.874 | 0.813 |
| 1,500 | 0.989 | 0.966 | 0.925 |

At rho=0.3 the induced *issue-level* ICC is approximately 0.087 (design effect 1.26); at rho=0.6 the induced issue ICC is approximately 0.175 (design effect 1.52). These are explicit hypothetical assumptions, **not** estimates from Lattice data. The Monte Carlo standard error is at most 0.0071 at 5,000 replicates (95% Monte Carlo margin at most 0.014). Values are approximate, not minimum sample sizes.

**Conclusion:** The Run225 independent-pair 681/686 planning direction achieves approximately 80% power only in the zero-clustering scenario for q=0.30, p=0.60. Under moderate repository heterogeneity, approximately 688 pairs produce only 73% power; stronger heterogeneity produces approximately 65%. A realistic prospective design must estimate clustering from a functional pilot and freeze the powered analysis before confirmatory inference. It cannot claim 258 or 686 pairs are universally adequate.

## Reproducibility

`python -m unittest -v test_cluster_power` (5 tests passed locally). `python cluster_power.py --replicates 5000 --output cluster_power_results.json` produces 48 complete scenario rows with per-row deterministic seeds, induced ICC, design effect, power and Monte Carlo uncertainty. The local archive also preserves the previously frozen Run225 inference runner, fixture, 11 regression tests, oracle, compiler and checksums.

**Inference limitation:** No new open-model completions were executed in this run. The frozen Run225 runner has not yet been published to the repository; that is the immediate next persistence and experiment priority. No reserved boundary issue was used.
