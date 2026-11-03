# Run456: exact paired-power audit (2026-11-03 UTC)

This is a prospective *planning calculation*, not empirical model evidence. Exact two-sided conditional McNemar/sign rejection thresholds were integrated over D ~ Binomial(n, 0.30) discordant issues, with IR wins conditional on discordance p. Independent issues assumed.

| n | p=.60 power | p=.65 power |
|---:|---:|---:|
| 306 | 0.443609 | 0.800367 |
| 400 | 0.558519 | 0.898777 |
| 681 | 0.800498 | 0.989749 |
| 800 | 0.862140 | 0.996393 |

Executable `run456_power.py` uses scipy.stats.binom.sf and binom.pmf, checks 40 rejection thresholds and design-effect identity. Local full-length reference calculation executed successfully; these figures are not real repair outcomes.

**Scope:** With repository clustering, these independent-issue powers are invalid as confirmatory design guarantees. A rough equal-cluster design effect 1+(m-1)rho is sensitivity analysis, not a valid substitute for cluster-level simulation or hierarchical inference. No new qualified repair, model completion, or semantic-IR advantage. All 89 boundary issues remain sealed. Preserve one draft PR #9.
