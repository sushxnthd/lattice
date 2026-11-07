# Run562 — Unequal repository sizes and estimand divergence

Synthetic exact-enumeration experiment (not coding-model evidence).

Eight repositories have discordant counts [30,30,30,30,30,30,30,2], seven favoring IR, one favoring Python. The 212 issue-level discordances give IR margin +208 and naive exact McNemar p=6.860813572208336e-60. Exhaustive 256 cluster-level sign flips give **issue-weighted cluster p=0.015625** and **equal-repository sign p=0.0703125**. These tests answer different questions; their disagreement is not an implementation bug.

A separate construction with seven single-issue IR-favoring repositories and one 30-issue Python-favoring repository yields issue-weighted margin -23 but equal-repository margin +6. Thus even the direction of the estimand can reverse. Freeze issue-weighted vs repository-weighted estimand, cluster inference and sampling before outcomes. Exchangeability of whole-repository sign flips remains an assumption, not a universal guarantee.

No new production repair, model inference, or IR superiority. Two qualified real repairs; 89 reserved issues sealed. Local source and raw output SHA-verified in archive; GitHub source/raw mirroring pending.
