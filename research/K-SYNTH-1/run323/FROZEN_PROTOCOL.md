# K-SYNTH-1 Run323 prospective clustered paired-power diagnostic

Status: PRE-EXECUTION, frozen before primary simulation (2026-10-28 UTC).

Question: Do issue-independent McNemar sample-size calculations remain calibrated when paired repair outcomes share repository-level dependence? This is a synthetic statistical-design diagnostic, not coding-model inference or real repair evidence.

Estimand: issue-weighted mean D = E[Y_IR - Y_Python], D in {-1,0,+1}. Each issue discordant independently with probability p_d=0.30. Conditional on discordance, IR-only win probability q_r is shared within repository r: q_r ~ Beta(q*k,(1-q)*k), k=1/rho-1; for rho=0 use fixed q. This gives mean q and within-repository conditional-sign ICC rho. It is an assumed sensitivity model, not a measured ICC.

Three designs (issues n, independent repositories m, alternative q): optimistic (306,102,.65), moderate (681,170,.60), expanded (800,200,.60). Allocate n as evenly as possible across m. Test rho in {0,.10,.30}; null q=.50. For each design x rho x null/alternative cell, run 1200 independent Monte Carlo replicates with numpy PCG64 seed 3232026. Two-sided alpha=.05.

Primary cluster-aware t test: repository score S_r=sum_i D_ri; n_r issues; mu=sum_r S_r/n; SE^2=(m/(m-1))*sum_r(S_r-n_r*mu)^2/n^2; p=2*t.sf(abs(mu/SE),df=m-1). If SE=0, p=1 when mu=0, otherwise p=0. Secondary comparator: issue-independent exact two-sided McNemar p=min(1,2*BinomCDF(min(IRonly,Pythononly),discordant,.5)). The latter is not cluster-valid.

Report empirical power and type-I rejection for both tests, Wilson 95% Monte Carlo intervals, discordance and cluster summaries. Preserve raw per-repository scores/discordance counts and all p-values in JSONL; independently recompute p-values and aggregate results without importing the primary implementation. Do not infer 80% power without evidence. Do not pool synthetic cases with model runs.

All 89 reserved boundary issues SEALED; six historical repairs unchanged. Canonical branch research/exp003-context-order, exactly one open/draft/unmerged PR #9. No model inference, reference-derived localization, or superiority claim.
