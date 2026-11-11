# Run645 — exact null calibration under repository clustering

Reproducible local exact enumeration of a null model: R independent fair repository signs, m perfectly correlated discordant issues per repository. Enumerate all R+1 repository win counts with exact binomial weights and apply issue-level two-sided exact McNemar at p<0.05.

Exact null rejection probabilities:
- R=100, m=1: 0.0352; R=100, m=4: 0.2713; R=100, m=8: 0.4841.
- R=20, m=8: 0.5034.
- R=4, m=8: 0.625.

A 30-vs-10 issue-level result with four repositories (3 vs 1) has issue-level p<0.01 but repository sign-test p=0.625.

This is a deliberately extreme cluster-dependence counterexample, not an estimate of actual ICC or model performance. The prospective experiment must preregister repository-level estimands and cluster-aware inference. No upstream production oracle or model comparison was run; qualified production repairs remain two. All 89 reserved issues remain sealed.

Local reproducibility artifact: lattice_run645.zip, SHA256 c507ca4dd73d637628f9fcf80915d6922696ea24e359adb069923d23248d6b01. Contains reproduce.py, raw.json, REPORT.md and SHA256SUMS. Executable/raw GitHub mirroring pending.