# Run543: prospective clustered paired-power stress test

Executed 96,000 synthetic paired experiments (3 conditional win probabilities × 4 sample designs × 4 repository ICCs × 2,000 replicates), seed 54320261107. This is statistical planning, **not** coding-model evidence.

Each repository receives a latent beta-distributed conditional IR win probability; issue discordance is 0.30. Compared naive issue-level McNemar asymptotic z rejection with repository-cluster-score studentized normal rejection (threshold 1.96).

| Conditional IR win | issues/repos | repo ICC | naive rejection | cluster-score rejection |
|---|---|---|---|---|
| .50 | 306/102 | .30 | .071 | .050 |
| .60 | 306/102 | .30 | .486 | .430 |
| .60 | 681/227 | .30 | .802 | .756 |
| .65 | 306/102 | .30 | .820 | .772 |
| .65 | 681/227 | .30 | .988 | .983 |

**Finding:** With repository ICC .30, the optimistic n306 and moderate n681 designs fall below 80% cluster-aware power; naive issue-level testing can inflate type-I error. These are model-dependent Monte Carlo estimates, not empirical ICC estimates or exact tests. Freeze repository-aware inference and assess ICC sensitivity before a powered study.

Locally executed reproducibility archive SHA256: `8ddc322e112c6a8fd784a11f4759d5ad67ee37c33f4a446ff6890e452efc1251`. Includes Python source, all 48 raw result cells, stdout, report, SHA manifest. Full artifact GitHub mirroring pending.

No new real production repair, model inference, or IR superiority. Two qualified repairs; all 89 reserved issues sealed.