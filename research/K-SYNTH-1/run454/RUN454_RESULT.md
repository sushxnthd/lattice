# K-SYNTH-1 Run454 — Cluster allocation non-identifiability

2026-11-03 UTC. Constructed mathematical counterexample, not measured Lattice model outcomes.

Both examples have 40 IR-winning and 20 Python-winning discordant issues:
- Six repositories, ten perfectly correlated issues each: deltas [10,10,10,10,-10,-10]; exact repository sign-flip p=11/32=0.34375.
- Twelve repositories, five perfectly correlated issues each: deltas [5,5,5,5,5,5,5,5,-5,-5,-5,-5]; exact p=397/2048=0.19384765625.
- Naive issue-level sign p is identical in both, approximately 0.00674465.

Hence issue-level win/loss totals are insufficient for repository-aware inference. Enumeration assumes a sharp, exchangeable cluster-level null and does not account for between-repository dependence or nonrandom arm assignment.

Prospective protocol must retain repository IDs, issue IDs, paired outcomes, assignment mechanism, model hashes and seeds; predeclare cluster-level estimand and weighting. This is not evidence of IR superiority or a new qualified repair.

The local CPython executable passed deterministic assertions. All 89 reserved issues remain sealed.
