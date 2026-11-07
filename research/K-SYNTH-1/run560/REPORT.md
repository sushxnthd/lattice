# Run560 — synthetic cluster-null calibration

This is a reproducible methodological simulation, not observed coding-model evidence or production qualification.

Synthetic exchangeable null: 100 repositories × 6 paired issues; 30% discordance; 300 replicates per rho; seed 56020261107. Repository-common discordant orientation probability rho. Exact two-sided issue-level McNemar versus 512-flip repository-level sign randomization with plus-one correction.

| rho | McNemar false rejections | Cluster false rejections |
|---|---:|---:|
| 0 | 8/300 | 10/300 |
| .25 | 11/300 | 9/300 |
| .5 | 30/300 | 16/300 |
| .75 | 37/300 | 12/300 |
| 1 | 60/300 | 10/300 |

At rho=1, naive issue-level testing rejected the true null 20% of the time in this finite synthetic simulation, while the repository randomization rejected 3.33%. These are simulation-specific results, not universal Type-I error estimates. Original n306/n681 issue-level planning is insufficient without cluster-aware inference.

The locally executed code, raw JSON, stdout and SHA manifest are in archive lattice_run560.zip (SHA256 9310169de2c2e05ff8e974d8645397717bfe42cf52378a8132b5068e8806f33e). Full GitHub source/raw mirroring remains outstanding. No new real repairs or model inference; two qualified repairs remain, 89 sealed issues untouched.