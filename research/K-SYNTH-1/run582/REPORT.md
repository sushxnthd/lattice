# Run582: exact repository-sign power sensitivity

Executed deterministic Python exact Poisson-binomial dynamic programming for synthetic independent repository-level IR win signs. This is a design counterexample, not empirical repair evidence.

At 20 repositories with identical average IR-win probability 0.65, exact two-sided sign-test power is 0.245706 for homogeneous p=.65, 0.232116 for alternating .8/.5, and 0.180699 for alternating .95/.35. At 40 repositories: 0.440795, 0.435979, 0.412530. At 80: 0.723528, 0.733489, 0.774352. At 120: 0.892429, 0.904263, 0.946345.

Finite-sample power differs despite identical mean win probability. The design assumes independent nonzero repository signs and a specified alternative; it does not justify exchangeability under heterogeneous effects and is not a powered empirical comparison. Reproducibility ZIP locally SHA256 dcf9889fd790ddfe883e8b5708cd8e2a0ff8d57875bad416d9c91fccc5726dde. Two qualified real repairs; 89 reserved issues sealed. No model inference or superiority claim.
