# Run312 prospective secondary experiment: informative repository sizes

Frozen before generating any random outcomes. Run311 assumed equal issue counts per repository. Test whether changing the estimand from issue-weighted mean paired outcome to repository-weighted mean paired outcome can reverse its sign when cluster size is informative. This is a **synthetic design counterexample**, not an IR/Python model result.

Two types of independent repositories, 100 of each: small with 2 issues and conditional IR win p=.80; large with 20 issues and p=.40. Per-issue discordance q=.30 in both groups; zero otherwise; independent Bernoulli trials. Seed 31220261028. R=10,000 independent complete simulated studies. Compute:
- issue-weighted paired difference = sum(D_ij)/sum(n_i), D in {-1,0,+1}
- repository-weighted difference = mean_i[(sum_j D_ij)/n_i]
- cluster-aware t statistic on repository score **sums** (issue-weighted null), and on repository score **means** (repo-weighted null), two-sided alpha .05, df=199.
- report empirical rejection directions and a deterministic analytic expectation for both estimands; independently recompute each from raw per-repository score vectors and n_i.

Theoretical expectations: small E[D]=.3*(2*.8-1)=+.18; large E[D]=.3*(2*.4-1)=-.06. Repo-weighted expectation (+.18-.06)/2=+.06. Issue-weighted expectation (2*.18+20*(-.06))/22=-.03818181818. Opposite signs are **by design**, not a discovered model advantage. No post-hoc reweighting of Run311's 63 frozen cells. Original h11 qualification remains primary. All 89 sealed.
