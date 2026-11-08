# K-SYNTH-1 Run591: repository-level precision feasibility

Executed an exact algebraic Hoeffding calculation for independent bounded repository-level paired effects X in [-1,1]. The two-sided 95% halfwidth is sqrt(2 ln(40)/R). Excluding zero for observed effects of 0.05, 0.10, 0.15, 0.20, 0.30 requires respectively at least 2952, 738, 328, 185, 82 independent repositories under this conservative bound. These are sufficient precision thresholds, NOT power calculations or necessary sample sizes.

At R=120 the halfwidth is approximately 0.248, so observed advantage 0.1 cannot exclude zero using this bound. Constructed two-repository counterexample: 100 IR-only wins in repository A and 1 Python-only win in B produce issue-weighted advantage 99/101, while equal-repository mean advantage is zero.

No real coding-model inference, production qualification or repair evaluation was performed. Independence and boundedness are assumptions. Do not interpret Hoeffding as power. All 89 reserved boundary issues remain sealed. Reproduction script and raw results are in the SHA-verified local Run591 archive.