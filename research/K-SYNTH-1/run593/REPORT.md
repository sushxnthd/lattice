# Run593: optional-stopping counterexample for fixed-n Hoeffding intervals

Executed exact absorbing binomial dynamic programming under independent fair Rademacher repository-level paired effects (mean 0). At checkpoints n=20,40,...,2000, reject when the fixed-n two-sided Hoeffding interval (radius sqrt(2 log(40)/n) for effects in [-1,1]) excludes zero, then stop. Exact integer path counts and rational cumulative probabilities were maintained; floating point only determines the strict rejection boundary.

- First checkpoint exceeding 5% cumulative false positives: **n=700**, probability **0.050449375**.
- At n=2000: cumulative false-positive probability **0.071539094** versus nominal 0.05.
- This does not invalidate fixed-n Hoeffding coverage; it demonstrates that repeatedly inspecting fixed-n intervals and stopping on significance is not generally anytime-valid.
- Repair: freeze sample size and analysis in advance, or use a proven confidence sequence / alpha-spending protocol; do not claim these particular thresholds are power estimates.

All data are synthetic exact null calculations. No new real repair, model inference, or evidence of IR superiority. The 89 reserved issues remain sealed.
