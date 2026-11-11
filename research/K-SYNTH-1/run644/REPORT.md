# Run644 — Exact repository-level sign-flip sensitivity

Executed exhaustive sign flips across four synthetic scenarios (reproducibility archive retained locally, SHA256 74beff0ec8fa9b4e4e501c54df82a9b7d14f3cf253511818cb6d1ae317a4a5c4).

For repository differences [10,10,10,-10], issue-level McNemar compares 30 IR-only and 10 Python-only discordances (p < 0.01), while exhaustive repository-label sign flipping yields p=0.625 (16 assignments). With four unanimous winning repositories, minimum two-sided sign-flip p=0.125. Six nonzero independently exchangeable unanimous repositories are needed to reach p=0.03125.

The sign-flip test requires joint within-repository method-label exchangeability under a sharp symmetry null, not an arbitrary heterogeneous population-average null. Results are synthetic methodological sensitivity, not production repair or model evidence. All 89 boundary issues sealed. Qualified real tasks remain two. Exact source and raw outputs in local archive pending GitHub mirroring.