# K-SYNTH-1 Run368 — ninth unique historical reference-qualified PR, no cross-file case interaction

**2026-10-30 UTC.** Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole OPEN/DRAFT/UNMERGED PR #9; all 89 reserved boundary issues SEALED.

## Original prospective freeze and upstream identity

New distinct [encode/httpx PR #1532](https://github.com/encode/httpx/pull/1532), merged 2021-03-24. The [prospective freeze](PROSPECTIVE_FREEZE.md) was committed `bc2286926494d07185abaf01cad5d0d22a6ca875` **before historical execution**. The upstream PR patch was inspected before freeze: this is **reference-informed** historical qualification, NOT a reference-blind model benchmark.

Exact baseline `ea5ffce14f6a1430a3cb89eae573b388047f3f2c`, reference merge `6cb1672459b0c1386cb36b89a92b87419fdc478c`. Only `httpx/_client.py` and `httpx/_models.py` changed between the four source arms. All eight source-file Git blob selections verified.

Original successful [GitHub Actions run 41080279172](https://github.com/sushxnthd/lattice/actions/runs/41080279172), artifact **12989112370**, ZIP SHA256 `8b978bce7febd8c869bd18b432d7dd54f0cda1c32210fd3b667c2577800e311b`, exactly matching GitHub artifact digest. All **7/7 original manifest entries** SHA-256 verified. The frozen 13-case oracle executed **52/52** public API outcomes in no-network, read-only, unprivileged Python 3.10 containers, with HTTPcore 0.12.3 and RFC3986 1.4.0.

| Historical source arm | Public targets /3 | Heldout targets /3 | Controls /7 |
|---|---:|---:|---:|
| baseline client + baseline models | 1 | 0 | 7 |
| reference client + baseline models | 2 | 1 | 7 |
| baseline client + reference models | 2 | 2 | 7 |
| reference client + reference models | 3 | 3 | 7 |

**Original prospectively frozen qualification: PASS.** Baseline preserves controls but fails five targets. Each one-file reference arm leaves targets unrepaired. Full reference repairs all six targets and preserves all seven controls. No import/ABI failure. An independent read-only verifier checked original ZIP SHA, manifest, source Git blobs, and all 52 case classifications. Seven local unit tests passed, including adversarial provenance and score-tampering tests.

## Negative mechanism result

All **13/13 individual casewise factorial interactions are zero**. `URL.join` cases respond to `_models.py`; `Client.build_request` cases respond to `_client.py` on this finite oracle. Yet the nonlinear aggregate `ALL tests pass` has interaction **+1**. Thus aggregate two-file necessity does **not** certify semantic/dataflow interaction. This is a concrete real-production corroboration of the separately [preregistered constructive counterexample](AGGREGATE_INTERACTION_THEOREM.md). It is not a proof of universal source independence.

## Cohort and limits

Run343 reconciled seven unique qualified PRs in six repositories; Run344 Jinja #1242 was eighth in seven. HTTPX #1532 is distinct from the already counted HTTPX #1183, giving **nine unique reference-qualified PRs across seven repositories**, not eight repositories. Source qualification is not model-generated repair success. No new model inference, powered IR-vs-Python/AST advantage or breakthrough is claimed.

Modern HTTPX 0.28.1 preflight passed 13/13; independent local tests 7/7. Original cloud artifact, raw outcomes, independent auditors, tests and 13-entry SHA-256 local archive are preserved. Next: [Run369 protocol](PROTOCOL_RUN369.md) for genuinely reference-blind issue recruitment and paired capable-model feasibility, with equal task facts/source/edit authority/compiler/oracle/token budget. All 89 boundary issues remain SEALED.
