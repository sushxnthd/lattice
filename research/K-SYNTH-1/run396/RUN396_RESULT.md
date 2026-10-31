# K-SYNTH-1 Run396 — factorial qualification false positives

Date: 2026-10-31 UTC / 2026-11-01 IST. Methodology result, not new production-repair evidence.

Executed five deterministic, two-module CPython scenario families, 96 parameterizations per family, four baseline/reference source combinations each, for 1,920 isolated `python -I -S` subprocesses and 9,600 frozen-case observations. The original Run395 gate returned `ELIGIBLE_BOUNDED` for all 480 constructed scenarios.

| Family (96 each) | Original eligible | Common target fails both ablations | Nonzero primitive interaction | Nonzero public interaction |
|---|---:|---:|---:|---:|
| Independent split-target repairs | 96 | 0 | 0 | 0 |
| Independent conjunction | 96 | 96 | 0 | 0 |
| Unused import decoy | 96 | 96 | 0 | 0 |
| Independent product observer | 96 | 96 | 0 | 96 |
| Actual generated cross-file dataflow | 96 | 96 | 96 | 96 |

**Finding:** Failure on some target in each single-source ablation does not establish a common target requiring both modules. A conjunctive Boolean oracle can exhibit interaction even when primitive module outputs are separable. An unused import does not prove dataflow. A derived product observer creates an interaction from two independent outputs. A generated true cross-file call provides a positive bounded witness.

The conservative screen rejects 96 split cases for no common target, returns `UNKNOWN` on 288 independent cases without primitive interaction, and identifies 96 generated dataflow witnesses with primitive interaction. These are finite, coordinate-dependent checks, not a universal coupling criterion.

An independent arithmetic auditor checked 67,680 values, statuses and interaction terms with zero disagreement; 11/11 regression and adversarial tests passed. The Run395 gate accepts a fabricated 64-hex-character shim-evidence hash when `verified=True`; hash shape does not verify semantic neutrality.

The first experiment process timed out after 456 completed scenarios. Its raw records were preserved; the remaining 24 scenarios were executed without modifying the design. The final 480 unique records were verified.

Complete SHA-verified local archive: `lattice_run396_factorial_causal_qualification_counterexamples.zip`, SHA-256 `98843327ac756e525206e85fbbe71e6955f383a22fe78b63ac718c0fb583d413` (16 manifest payloads). Full raw evidence is in the local archive; GitHub raw-archive mirroring remains incomplete.

**Limitations:** 480 parameterizations of five constructed templates, not independent real repairs; no new model inference, powered IR superiority evidence or production-task qualification. All 89 reserved boundary issues remain sealed. Next: freeze an unseen issue-first real repair and test a matched semantic/dataflow IR versus Python/AST coding-model comparison with independently verified oracle and edit authority.
