# K-SYNTH-1 Run447: crossed real-Flask reproduction falsifies the simple version/protocol explanations

**Executed 2026-11-02 UTC / 2026-11-03 IST.** Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, exactly one OPEN/DRAFT/UNMERGED PR #9, all 89 reserved boundary issues sealed.

## Frozen history and design

The original [Run445 Actions experiment](https://github.com/sushxnthd/lattice/actions/runs/41522993332) ran on **Python 3.12.15** (verified from original job 125543461677 logs), with baseline session **60/128** and reference **128/128**. Its original artifact ID 13177664423 has ZIP SHA-256 `5cca13b9d9e6c781f187282c75f8cf3480207ba2ad8e2ce57e2d0aa3febf8ef0`. The original oracle ran a mocked `Flask.run` before the session probe and did not record `pip freeze`.

Run446 ran on **Python 3.11.17**, pinned Werkzeug **3.1.3**, with baseline **64/128** and reference **128/128**. Both used the exact same 128-case SHA-256 `b04edef3965002c27c5194ae4b4ca7bf5464ad7bfd757d4e39d987b09d84c3b3`. Four DNS explicit-port-zero cases `dns_with_port_01/09/17/25` accounted for the original disagreement. Python version and oracle protocol had changed together, so neither cause was identifiable from those two historical observations.

**Before cloud execution**, [Run447 prospective protocol](PROTOCOL_RUN447_FROZEN.md) was committed as `328a2fa398c36c71f2a60418c05ad992437857be`. [Run447 Actions 41541062257](https://github.com/sushxnthd/lattice/actions/runs/41541062257) completed **SUCCESS** at 2026-11-02 22:54 UTC on frozen head `261620e3edaedbe1beed9af4985d37946f8a65f4`. It crossed Python **3.11.17 vs 3.12.15** × **original byte-identical Run445 oracle vs canonical Run446 diagnostic** × **exact historical parent vs reference** with 128 unchanged cases and six pinned runtime dependencies.

## Complete real API matrix

| Python | Oracle protocol | Historical parent correct | Reference correct |
|---|---|---:|---:|
| 3.11.17 | Original Run445 | 64/128 | 128/128 |
| 3.11.17 | Run446 diagnostic | 64/128 | 128/128 |
| 3.12.15 | Original Run445 | 64/128 | 128/128 |
| 3.12.15 | Run446 diagnostic | 64/128 | 128/128 |

**All four previously failing DNS port-zero cases now pass in every new cell.** Every parent failure is the same set of 64 IPv6 cases. Zero case-level disagreements between Python versions or protocols; zero difference-in-differences on failures. The reference passes every case. This is **1,024 actual Flask session API transactions**, plus **512 mocked Flask.run probes** from the legacy oracle, not a source-expression surrogate.

Two independent read-only auditors verified both original GitHub artifact ZIPs, **42/42 payload SHA-256 entries**, all **1,024 real API rows**, and **4,096 case invariants**. **15/15 local tests passed**; clean-extraction replay passed. Original artifacts: Python 3.11 ZIP SHA-256 `af46b6e71859678037e5ac1aef9fbfea5143590c9be9ffa144ccc6fd3b723a4f` (artifact 13186917337); Python 3.12 ZIP SHA-256 `d58e2e57494664aa3213ecbf655ba42e5bb54452bc930c3d5608b7ae844a94a9` (artifact 13187052017). The six pinned runtime dependencies matched; `setuptools` appeared only in the Python 3.11 full freeze, so complete environment identity is not claimed.

## Interpretation and next work

This prospectively crossed experiment **does not reproduce** the four original Run445 DNS failures, even with the original byte-identical oracle and Python 3.12.15. It rejects the predeclared Python-only, protocol-only and simple interaction patterns **under the pinned runtime environment**. It **does not identify** the cause of the unpinned original Run445 result. The historical observations are preserved; no retrospective rescoring or new benchmark qualification is permitted.

**Research status remains two independently qualified real multi-source repairs** (Flask PR6096 and urllib3 PR5071). No new coding-model completions, powered McNemar evidence, IR superiority or breakthrough. Historical ZIP mirroring to GitHub remains incomplete.

**Run448 priorities:** genuinely functional paired capable open-model inference on both qualified repairs with semantic/dataflow IR vs information-equivalent ordinary Python/AST-action, shared SHA-pinned source/facts/atomic compiler/isolated oracle, raw model outputs and failure taxonomy; and prospectively qualify independent two-production-source public-repository issues with target, heldout, nonregression and component-necessity checks. If investigating the four historical failures further, vary one runtime dependency at a time while preserving all frozen cases. Keep all 89 reserved issues sealed and PR #9 draft/unmerged.
