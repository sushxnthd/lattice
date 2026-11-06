# K-SYNTH-1 Run524: qualification estimand separation

Executed exhaustive enumeration of 16,384 Boolean outcome matrices with two targets, two baseline-passing controls, and four arms (base, A-only, B-only, full). Full must pass all four; baseline must fail at least one target.

- Joint necessity: 675 matrices.
- Target-only necessity: 432 matrices.
- Joint necessary but not target-only: 243 matrices (36% of joint-qualified).
- Target-only qualified is a strict subset of joint qualified.

The 243 cases demonstrate selection bias from requiring both components to be target-essential: one component can instead be necessary to preserve nonregression controls. Report target-repair and control-preservation strata separately, prospectively. This is exact combinatorial evidence, NOT prevalence in real repositories, not a new qualified repair, and not evidence of IR superiority. All 89 reserved issues remain sealed.

Reproduction: run524.py and raw.json in local SHA-verified archive. ZIP SHA256 a3355b9f138d0fb2440f0cd25a4e607687b7875f9a399cf1c8334c65c7832060. GitHub mirroring of raw archive pending.