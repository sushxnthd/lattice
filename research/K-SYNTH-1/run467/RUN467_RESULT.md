# Run467 — repository clustering falsifies naive McNemar calibration

Synthetic reproducible null simulation (NOT model evidence): 100 repositories × 6 issues, 3,000 independent simulated experiments, seed 467, per-issue discordance probability 0.30. Each repository draws a symmetric null sign; each discordant issue copies that sign with probability rho and otherwise draws an independent fair sign. Thus each marginal issue is null-balanced.

| rho | Exact unclustered McNemar p<0.05 rejection | Mean discordant issues |
|---|---:|---:|
| 0 | 0.044333 | 180.125 |
| 0.5 | 0.087667 | 180.052 |
| 1 | 0.207333 | 179.851 |

The same marginal null and nominal n=600 can yield 20.7% false positives under shared repository direction. This is a simulation counterexample, not a finding that semantic IR works. Freeze repository-aware primary inference before collecting powered outcomes; preserve repository identifiers and report cluster-robust or repository-level sensitivity analyses. Code, raw JSON and SHA-256 archive are preserved locally for mirroring. Existing two qualified tasks unchanged; 89 reserved boundary issues untouched. No new model completions.