# K-SYNTH-1 Run446: historical port-zero session failures fail prospective reproduction

**2026-11-03 IST.** Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, one OPEN/DRAFT/UNMERGED PR #9; all 89 reserved boundary issues sealed.

## Original evidence retained

The unmodified Run445 real Flask Actions 41522993332 artifact SHA-256 `5cca13b9d9e6c781f187282c75f8cf3480207ba2ad8e2ce57e2d0aa3febf8ef0` was independently reaudited: 11/11 original payload SHA-256 entries, 512 API rows, 2,432 invariant checks. The original baseline session round-trip passed 60/128; testing.py reference-only passed 128/128. Four DNS explicit-port-zero cases returned `None` on baseline and `42` on reference.

Run445's source-expression cookie oracle predicted baseline 64/128 versus actual 60/128, with **exactly four false-positive predictions** (dns_with_port_01/09/17/25). No other original baseline source-oracle discrepancies. The raw authority string `nodeN.example.test:0` yields the same hostname under `partition(':')[0]` and `urlsplit('http://'+authority+'/').hostname`, but that is not evidence about actual Flask request properties.

## New preregistered isolated real API execution

Froze H1/H2/H3 in [PROTOCOL_RUN446_FROZEN.md](./PROTOCOL_RUN446_FROZEN.md) before running cloud inference. [GitHub Actions run 41527974055](https://github.com/sushxnthd/lattice/actions/runs/41527974055) completed **SUCCESS**. Original artifact ID `13180756221`, ZIP SHA-256 `eddf9f012646157488504af923cefee0c55286af8c4a59fa42fb697a1a76f060`. Independent auditor verified 11/11 payload hashes, 256 actual Flask session+GET observations, 256 original-versus-new comparisons and 1,152 checks.

Historical parent `514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b`; reference `7203feabf723edae0286ae5dc64fec8ac4c91735`; baseline testing.py SHA-256 `60c60294d716a6102e9993ad8f14930ad421fde322d8d3b54c7be642acbad560`; reference testing.py SHA-256 `629d481658aaec7076a55913eda38c270ec45d430b34b2f9d38b2eec2b0ad3da`. Exact original 128-case SHA-256 `b04edef3965002c27c5194ae4b4ca7bf5464ad7bfd757d4e39d987b09d84c3b3`. Environment: Python 3.11.17, Flask 3.2.0.dev0, Werkzeug **3.1.3**, complete pip freeze in original artifact.

| Condition | Original Run445 | New Run446 pinned runtime |
|---|---:|---:|
| Baseline testing.py session correct /128 | 60 | **64** |
| Reference testing.py session correct /128 | 128 | **128** |
| Four baseline DNS port-zero failures | 4 | **0** |

The only four baseline changes were the original port-zero cases. All 124 other baseline cases and all 128 reference cases matched. For the four cases, both actual Flask extraction expressions were equal, cookie-update domains were identical, cookie-jar keys were identical, and both source variants returned `42`. The prospective persistence hypotheses were rejected.

**Interpretation:** Run445's four historical failures are **not reproduced** under this recorded runtime. The original dependency environment was not fully pinned, and the responsible version or environmental cause is **unknown**. Do not claim a Werkzeug root cause, retroactively erase Run445, or promote this as a new qualified repair.

## Scientific status

Eight local regression/audit tests passed. The local SHA-verified reproducibility archive contains both unmodified original Actions ZIPs, raw traces, independent auditors, tests, frozen case list and environment. Historical GitHub ZIP mirroring remains incomplete.

Still **two** independently qualified real multi-production-source repairs. No new coding-model completions, no powered IR superiority evidence, no new qualification, no breakthrough. Run447 prioritizes functional paired model inference, independent issue-first real repairs, and environment-pinned mechanism ablations.
