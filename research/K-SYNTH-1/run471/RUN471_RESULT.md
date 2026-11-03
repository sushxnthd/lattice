# Run471: effective discordant repository count (2026-11-03 UTC)

Exact finite enumeration (not model inference). A two-sided repository-level sign-flip test with K nonzero cluster margins has minimum attainable p-value 2^(1-K), attained when all nonzero margins have the same sign. Zero-margin repositories contribute no independent sign information; counting them toward effective K falsely inflates apparent precision.

Verified deterministic cases (exact fractions):
- 12 repositories, 2 nonzero margins [10,10]: p=1/2, K=2.
- 12 repositories, 6 nonzero margins [1]*6: p=1/32, K=6.
- 12 repositories, 12 nonzero margins [1]*12: p=1/2048, K=12.
- Dominant cluster [100]+[-1]*11: p=1 despite 12 active clusters.
- Balanced [1,-1]*6: p=1.

For alpha .05, at least 6 active repositories are needed even for the most extreme possible two-sided result (K=5 gives minimum 1/16). This is a necessary, not sufficient, condition. The exact sign-flip test remains conditional on cluster sign symmetry and a prospectively specified estimand. These results are synthetic mathematical counterexamples and do not validate semantic IR or real repair superiority. Benchmark still has only two qualified repairs. 89 sealed issues untouched.

Executable and raw local artifact: run471.py and raw.json, with SHA-256 provenance retained separately. GitHub mirroring of executable/raw is pending.
