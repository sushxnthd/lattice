# Run364 prospective historical proxy-origin qualification

Frozen 2026-10-30 UTC, before execution of historical source variants or inspection of PR #5126 reference patch. The public PR description (not patch hunks) was used to specify behavior.

Candidate: https://github.com/urllib3/urllib3/pull/5126. Base e349d97f2bf234b95d5dd9e689d056a521dfc3b0, reference 580df2aab0340c2f81cf2770012875e4530a101d. Two production files:
- src/urllib3/connectionpool.py base Git blob 7556b50f6d685bdb30e7afac11484a05ef07b767; ref 1c8a56597c5728a2a377b3399b427403f753915e
- src/urllib3/poolmanager.py base Git blob 007b31dcfe8aae4f24bebff8bfafa1a06a7bd3eb; ref 1ac39a8d5cb048a2c791f5d757ab6e4602624911

Frozen public-API oracle run364_proxy_redirect_oracle.py SHA256 30896d34a903203c27a5da55275d16faaa6eb9f95879f49d3e1b1968152d5ffb, with seven repair targets and six controls. The cases use loopback HTTP proxy observations for same-origin credential preservation, cross-origin credential removal, proxy-origin redirect classification, Host regeneration, forwarding and unrelated nonregression. No external network or model-generated code.

Frozen 2x2 qualification: run all four source combinations in independent isolated CPython 3.11 containers with exact Git blob verification. All 52 functional cases must be observed. Baseline fails at least one target and passes six controls. Full reference passes seven targets and six controls. Neither one-file variant passes all 13 cases. At least one target exhibits positive casewise two-file factorial interaction. Any pre-oracle failure is UNKNOWN and yields INCONCLUSIVE, never zero functional score. Never retune after results. This is finite reference-source qualification, not semantic mechanism or model success.

Separate modern installed urllib3 2.7.0 smoke test: 2/7 targets, 6/6 controls, not a historical qualification. Model prompts must exclude reference-derived localization; an independent heldout evaluator is still required. All 89 reserved issues sealed; one OPEN/DRAFT/UNMERGED PR #9, canonical research/exp003-context-order branch.
