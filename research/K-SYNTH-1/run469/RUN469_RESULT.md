# Run469: exact cluster allocation counterexample

UTC date: 2026-11-03. Synthetic, not production-model evidence.

With 120 discordant issues across 12 repositories (10 each), both constructions have 90 IR wins and 30 Python wins. Exact two-sided issue-binomial p = 3.772753306355308e-08 in both.

Allocation A: nine repositories have +10 and three have -10. Exact exhaustive repository-sign-flip p = 0.14599609375.

Allocation B: nine repositories have +6 (8 wins/2 losses) and three have +2 (6 wins/4 losses). Exact exhaustive repository-sign-flip p = 0.00048828125.

Both enumerate all 4096 repository sign vectors; the issue-level pooled outcome is insufficient to determine cluster-aware inference. The sign-flip test requires cluster-level sign symmetry under the null, not automatically guaranteed by observational benchmark assignment. This is a finite counterexample, not an empirical IR advantage or a power estimate.

Reproduction: Python 3 standard library, enumerate product((-1,1), repeat=12); count absolute signed sums >= observed absolute sum, divide by 4096. Issue p is twice the upper binomial tail P[Binom(120,.5)>=90]. The original executable and raw JSON are locally archived, GitHub mirroring pending.

No additional real qualified tasks, no new model outputs, all 89 reserved issues sealed.