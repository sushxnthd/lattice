# K-SYNTH-1 Run433 — Trace-observational boundary and clustered power

## Scientific result
**Bounded negative theorem; no model-performance or general Python soundness claim.** Run432's conditional pure-int assignment commutation theorem certifies equal final local stores and returns, but does not certify trace equivalence. Two independent assignments over exact built-in integers can be swapped without changing final values, yet CPython `sys.settrace` sees different intermediate local-store sequences.

Minimal witness: `left=x+3; right=x*5; return left-right` versus `right=x*5; left=x+3; return left-right`. Both terminate normally and agree on every exact-int input; their line-event local snapshots differ. The final-store theorem remains intact. A trace-sensitive IR must return `UNKNOWN_TRACE_OBSERVABILITY` rather than promote a final-state certificate to trace preservation.

## Executed evidence
- 256 seeded trusted constructed programs, 1,024 before/after input pairs, 2,048 real CPython executions.
- 1,024/1,024 equal returns; 1,024/1,024 differing intermediate line traces; 256/256 independently disassembled store-order differences.
- Independent auditor checked 12,288 predicates with zero disagreements; 11/11 regression and statistical tests passed.
- Raw JSONL SHA-256: `94ef4659d2f94f68d7611e11f9f6c6f55d37afeb01cce4c80076a96bca4a86d2`.

## Statistical audit
Exact unconditional two-sided McNemar power at alpha=.05 validates the *iid planning assumptions*: n306 with discordance=.30 and conditional IR win=.65 yields power **0.800367**; n681 with discordance=.30 and conditional IR win=.60 yields **0.800498**. These are assumed effects, not measured effects.

In 20,000 simulations per setting, 200 repos × 4 issues with hypothetical beta-binomial repository heterogeneity, null naive McNemar rejection was **.04380/.05430/.06375** at ICC **0/.10/.20**, while a cluster-t on repository signed margins yielded **.05060/.05075/.05110**. Cluster ICC is hypothetical; the cluster-t is sensitivity analysis, not a preregistered confirmatory test. Design must account for clustering and heterogeneous discordance.

## Issue-first candidates
- [HTTPX #2810](https://github.com/encode/httpx/issues/2810): prospective freeze SHA `782014fda46735882aea67a25cab6fa31d3c0ac962aa436bb6ba3d426617372d`. Merged [PR #2999](https://github.com/encode/httpx/pull/2999) changes only one production Python source. Rejected.
- [urllib3 #2936](https://github.com/urllib3/urllib3/issues/2936): prospective freeze SHA `ec41e967086687a39d3bb2ed8fea4ad44b7c1f8408336411bf42cb5c2ee25404`. Merged [PR #5054](https://github.com/urllib3/urllib3/pull/5054) documents that changing class defaults is not the supported contract; other behavior-changing PRs closed unmerged. Rejected.

Neither candidate is promoted. No historical functional replay claimed for these candidates. Historical sealed-issue overlap must be checked against the full ledger before reuse.

## Status
Exactly **two** independently qualified historical multi-production-source repairs (Flask PR6096, urllib3 PR5071). No new coding-model completions, powered semantic-IR superiority, or breakthrough. All 89 reserved boundary issues remain sealed. Full 24-entry SHA-verified local archive (23 payloads) contains raw traces, full code, independent auditor, tests, power calculations, simulation, prospective freezes, and replay receipts. Older GitHub ZIP mirroring remains incomplete.
