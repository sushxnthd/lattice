# Run525: Exact calibration and pseudoreplication stress test

Executed a synthetic, finite sharp-null sign-flip experiment with 50 configurations (1–10 independent repositories, 1/2/4/8/16 perfectly correlated issue wins per repository) and 120 exact superuniformity checks for the cluster randomization test (all passed). This is NOT empirical repair-model evidence.

Counterexample: one repository containing sixteen concordant wins produces naive issue-level exact McNemar p=0.000030517578125, but repository-level randomization p=1.0. Eight independently randomized repositories each containing one win produce p=0.0078125 for both methods. The cluster randomization test is exactly calibrated under independent randomized repository-level assignments and a sharp null with a fixed statistic; observational cluster labels alone do not justify it.

Local execution produced 50 raw JSON records and 120 passed calibration assertions. Local SHA256: experiment.py d2a94f144f76348026a2b7e2b4590109c014fcce8763d86fb305ea548f4e4984; results.json 9ab72a37c789d720f0b78d587c7628e91b78cbb4fcbe1c016808a6d2419d0dcc; stdout.txt 43d8c79f038be736fe538db7e0ce1d9e4b76232c2a111c3e7e84de63ccb3b162. GitHub script is a compact independently runnable equivalent, not byte-identical to the local script.

This test does not qualify any new real production task, run a coding model, establish IR superiority, or license a claim of statistical power. Two qualified repairs remain; 89 reserved issues remain sealed. Prioritize actual prospectively frozen repair tasks and paired coding-model trials rather than additional synthetic statistical exercises.
