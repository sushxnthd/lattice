# K-SYNTH-1 Run367: exact historical HTTPcore factorial, independent audit

Date: 2026-10-30 UTC. Canonical branch `research/exp003-context-order`, sole draft PR #9. All 89 reserved boundary issues remain SEALED.

## Original evidence and provenance

Initial [Actions run 41069900235](https://github.com/sushxnthd/lattice/actions/runs/41069900235) failed **before testing** because the previously local-only Run366 oracle was missing from the GitHub branch. This is an infrastructure failure, not a model or oracle failure. The oracle was then committed **byte-identically** at `research/K-SYNTH-1/run367/run366_historical_oracle.py`, SHA-256 `1889d4e0b71610018b94fa87084199de280323cedf3133eeac7588025ff30797`, Git blob `ef84547431fdb455597cceb576d8883e44a2575c`.

Corrected [Actions run 41070045920](https://github.com/sushxnthd/lattice/actions/runs/41070045920) completed **SUCCESS**. Original artifact **12983813500**, ZIP SHA-256 `f36bc1a83bfd54dc340abedeb180bc303307a9011071cc362239a908ff07501e`. All **18/18** original SHA-256 manifest entries independently verified.

The workflow cloned exact historical HTTPcore base `5974b03c7df89d3ee4e23779900d5349d550753c` and PR #1000 head `7fb20526175e2300185ce2b472a97acca95b2525`. All four historical Git blobs were verified before execution. The unchanged frozen 36-case oracle ran against four complete historical source combinations in no-network, read-only, unprivileged Python 3.11 containers with pinned `h11==0.16.0` and `certifi==2025.1.31`. **144/144 historical functional observations executed**, without pre-oracle errors.

## Exact historical functional matrix

| Historical source | Sync targets | Async targets | Sync controls | Async controls |
| --- | ---: | ---: | ---: | ---: |
| Baseline/baseline | 0/8 | 0/8 | 9/10 | 9/10 |
| Repaired sync only | 8/8 | 0/8 | 10/10 | 9/10 |
| Repaired async only | 0/8 | 8/8 | 9/10 | 10/10 |
| Both repaired | 8/8 | 8/8 | 10/10 | 10/10 |

**Prospective qualification FAIL.** The original baseline already fails the frozen `busy_idle_closed` control in each backend. Both repaired files pass all finite targets and controls, but baseline control preservation was required prospectively. Do not retrospectively remove or reclassify failed controls.

**Mechanism result:** All **36/36 individual case-level factorial interactions equal zero**, even though the nonlinear `ALL tests pass` aggregate has positive interaction. This establishes that aggregate two-file necessity can arise from two independent mirrored-backend repairs without case-level cross-file semantic coupling.

## Independent exact-history versus modern-package proxy audit

Independently compared the 144 exact historical rows against the previous Run366 modern HTTPcore 1.0.9 source-normalized reconstruction. **144/144** agree on backend, case, group, input states, cap, pass, expected and actual retention/closure, and error. Only environment/path metadata differs. This does not retroactively turn the proxy into a historical run.

An independent read-only auditor verified 144 rows, source Git blob IDs, the original oracle SHA, independent expected-state transitions, counts and 36 interactions. Eight local adversarial auditor tests passed. The original cloud auditor and independent local replay agree on all scientific fields; only an explanatory note string differs.

## Scientific limits and next action

This is **not** a ninth qualified PR. Cohort remains **eight qualified PRs across seven repositories**. No new Qwen inference, powered IR superiority, or breakthrough is claimed. Next recruit a genuinely independent, reference-blind, multi-production-file issue with clean frozen baseline controls and heldout oracle, then run matched semantic/dataflow IR versus ordinary Python/AST-action real-model repairs with identical source facts, authority, compiler, isolated oracle, and tokenizer-measured budgets. All 89 reserved boundary issues remain sealed.
