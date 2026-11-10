# Run620: cluster-sensitivity audit (not model evidence)

The existing n=306/681 McNemar planning values assume independent paired observations. Repeated issues from one repository can violate that assumption.

An executable 72-scenario sensitivity model uses the design effect `1+(n/R-1)*rho` for exchangeable discordant-sign correlation and a normal-approximation two-sided power curve, with assumed discordance 0.30 and conditional IR win rates 0.60/0.65. The within-repository ICC rho is hypothetical, not measured.

At rho=0.10, conditional win=0.65: n=306, R=100 yields effective n=253.7 and approximate power 0.783; n=681, R=100 yields effective n=430.7 and approximate power 0.947. These are sensitivity values, not empirical results.

Counterexample: if all discordant outcomes within each repository share a single Bernoulli sign, n=681 issues from 100 repositories supply at most 100 independent sign observations. Therefore nominal paired-task sample size alone cannot certify power or coverage.

Decision: freeze repository-aware recruitment and uncertainty estimation before model outcomes; preserve per-repository paired discordance, and report cluster-aware uncertainty. No new production repair qualified, no model inference executed, and no IR superiority claim. Werkzeug PR3339 remains unqualified; it is a heterogeneous WSGI cleanup, not proven causally coupled repair. All 89 reserved boundary issues sealed.

Full local SHA-verified reproducibility archive: lattice_run620.zip, SHA256 95bf875e76b9b7a6f438a6ceeeb01091f61fa3258cdf3ee546a375839c03a40e.
