# K-SYNTH-1 Run311: clustered paired-repair power audit

**2026-10-28. Prospective protocol committed first:** [PROTOCOL_RUN311_CLUSTER_POWER.md](PROTOCOL_RUN311_CLUSTER_POWER.md), commit `24934720d333918ae57cb6b34a763a385cf767af`. This is statistical design evidence, not a real-repository repair or model completion.

63 frozen cells = seven repository/issue designs × p=.50/.60/.65 × intrarepository winner ICC rho=0/.05/.15. Discordance q=.30; 4,000 Monte Carlo replicates per cell (252,000 total); seed 31120261028. Rejection compared two-sided naive McNemar with a repository-cluster score t test. Independent auditor rederived every rejection decision, all 63 counts and closed-form variances from the original 252,000 per-replicate repository-score vectors; **zero discrepancies**.

| Design | p | rho | Naive rejection | Cluster-aware rejection |
|---|---:|---:|---:|---:|
| 306 issues / 102 repos | .65 | 0 | 83.4% | 82.6% |
| 306 issues / 102 repos | .65 | .15 | 82.3% | **79.4%** (MC 95% CI 78.2–80.7%) |
| 681 issues / 227 repos | .60 | 0 | 82.1% | 82.3% |
| 681 issues / 227 repos | .60 | .15 | 79.9% | **77.7%** (76.4–79.0%) |
| 800 issues / 100 repos | .60 | .15 | 84.8% | **77.2%** (75.8–78.5%) |
| 800 issues / 200 repos | .60 | .15 | 85.6% | **82.7%** (81.5–83.8%) |
| 1200 issues / 200 repos | .60 | .15 | 94.8% | **92.5%** (91.7–93.3%) |

Under the rho=.15 null, naive McNemar rejected **8.7%** of the time for 1600 issues / 200 repos versus **4.9%** for the cluster-aware test (nominal 5%). At p=.60, rho=.15, 800 issues concentrated in 100 repos were below 80% simulated power; the same 800 issues distributed across 200 repos exceeded 80%.

**Assumptions and limitations:** beta-binomial repo-level winner probabilities; independent discordance indicators; equal repo sizes; ICC fixed at the frozen values; asymptotic tests. The MC intervals quantify simulation noise, not uncertainty about these assumptions. No powered IR-vs-Python claim follows. The unclustered n306/n681 targets are not unconditional guarantees.

Independent raw audit: 252,000 records, 63 cells, zero discrepancies. Raw JSONL gzip SHA256 `7c27e27e4d86f328631d7c3080b74be97935b4dda61066f59b06691172ae56ba`; summary SHA256 `620ce3da1c88e98df1bd1e052c895a25bf1038277d3ad0632d4d722f2d938933`. Full raw evidence and runnable code are in the local Run311 reproducibility archive; historical large-artifact GitHub mirroring is incomplete.

Candidate screened only: [python-hyper/h11 PR #115](https://github.com/python-hyper/h11/pull/115), merged, three relevant production files, **NOT QUALIFIED** (no frozen oracle). Prior wsproto PR #6 failure remains unchanged.

**Status:** five previously reported independently qualified real repairs; no sixth qualification, no new model inference, no IR advantage or breakthrough. One K-SYNTH-1 kernel; branch `research/exp003-context-order`; PR #9 open/draft/unmerged; all 89 boundary issues sealed.