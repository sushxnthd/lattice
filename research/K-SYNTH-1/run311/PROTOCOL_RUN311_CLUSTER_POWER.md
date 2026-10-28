# K-SYNTH-1 Run311: prospective clustered paired-repair power audit

Frozen 2026-10-28 before the primary Monte Carlo was run. This is a **statistical design study**, not model evidence and not a new independently qualified repository repair.

## Objective
Audit whether the previously quoted unclustered McNemar sample sizes (n=306 for q=.30, conditional IR win p=.65; n=681 for p=.60) remain adequately powered when repairs are clustered by public repository. A non-result must be reported as such.

## Fixed generative model
- J independent repositories, exactly m issues per repository; n=J*m.
- Per repository j, draw latent conditional IR-win probability P_j ~ Beta(p*(1/rho-1),(1-p)*(1/rho-1)) for rho>0; for rho=0 use P_j=p.
- Each issue discordance D_ji ~ Bernoulli(q=.30), independent of P_j and other D. Conditional on D=1, IR win W_ji ~ Bernoulli(P_j); otherwise tie. This induces intrarepository correlation rho in discordant winner signs, **not** in discordance rates. This simplifying assumption is a limitation.
- Fixed designs (J,m): (102,3), (227,3), (100,4), (100,8), (200,4), (200,6), (200,8).
- Fixed p in {.50,.60,.65}; fixed rho in {0,.05,.15}; 4,000 Monte Carlo replicates per cell, fixed seed 31120261028. All 63 cells reported, including null calibration p=.50.

## Frozen analyses
1. Naive two-sided asymptotic McNemar z=(wins-losses)/sqrt(discordants); reject if abs(z)>normal quantile .975.
2. Cluster-robust repo-score t statistic: U_j=sum_i D_ji*(2W_ji-1); t=sum_j U_j / sqrt(J/(J-1)*sum_j (U_j - mean(U))^2), with t_(J-1) two-sided .05. This is an asymptotic cluster test, not an exact randomization test.
3. For each cell report rejection rate and binomial Monte Carlo SE and 95% simulation CI; for p=.50 report empirical type-I error, otherwise empirical power.
4. Closed-form independent and clustered variance of the signed score: Var(S_i)=q-q^2*(2p-1)^2; Cov(S_ji,S_jk)=4*q^2*p*(1-p)*rho, for distinct issues in same repo. Compare observed variance of summed scores against formula. Do not use the closed-form formula to silently adjust the frozen test.
5. Decision: do not call any scenario adequately powered unless **cluster-robust** estimated power >=.80; note Monte Carlo uncertainty and model dependence.

## Reproducibility and integrity
Run only trusted locally authored statistical Python code, preserve raw per-cell counts and SHA256 manifests. Verify with independent mathematical calculations. No model completions, new repository qualification, or IR advantage can be inferred from this simulation. Keep canonical branch research/exp003-context-order and exactly one open/draft/unmerged PR #9. Do not touch the 89 sealed issues.