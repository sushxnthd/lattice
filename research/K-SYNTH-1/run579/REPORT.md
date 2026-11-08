# Run579 — Repository clustering invalidates issue-independent McNemar inference

Executed exact exhaustive sign-flip randomization (4096 assignments) over 12 synthetic repository clusters, 20 perfectly dependent issues per cluster.

- Balanced: six IR-only and six Python-only repositories, b=c=120, issue-level exact McNemar p=1, cluster p=1.
- Nine versus three: b=180,c=60, issue-independent exact McNemar p=4.0990161694649685e-15, repository-cluster exact sign-flip p=0.14599609375.

This is a counterexample to interpreting issue-level significance as robust when within-repository dependence is extreme. The cluster sign-flip null assumes exchangeable signs of independent repository-level paired effects; it is not automatically valid for observational or nonrandomized samples.

Implication: preregister repository-cluster inference and report both issue-level and cluster-level uncertainty; recruit independent repositories, not just issues. Reproducibility archive SHA-256 f0af42ab2157a2a0fecc209c0ef807a07e3fba3b4d5559197b653d0eb468e6f9.

No real model inference, no newly qualified repair, no semantic-IR claim. All 89 reserved issues untouched.