# K-SYNTH-1 Run354 — historical HTTPX dispatch factorial

**Classification:** new SHA-pinned source-extracted CPython functional traces, independent auditor and a negative mechanism result. Not a new independent repair, full HTTPX runtime/network oracle, coding-model inference, or representation superiority.

## Original sources and method

Post-outcome diagnostic on historical HTTPX baseline `891d865044d27c229278f0fa20d84ba4007cb289`, extending Run353's three manually specified HEAD default edits. Original SHA-256: `httpx/_api.py` `bd646bd7bfddd75eba6687bef45b52f5c9e1b7634d680fbcbfaf16304b618f5d`, `httpx/_client.py` `6b223a7a32afcbaf4e1a9a83f6d34caf8f66a31d740a1ac511df678463ecd8a2`. Reconstructed stage SHA-256: `81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe`, `97f9ba016b14033c347a398444662e795e02e0118729d67ecbfbfa0192a0bd60`.

A bounded AST guard extracts the original module-level `head`, `Client.head`, and `AsyncClient.head` bodies and enforces a single HEAD call-through with explicit `allow_redirects` forwarding. Under CPython with instrumented request spies, four source combinations (baseline, API-only, client-only, both) each ran six cases on three entry points. **72 real source-extracted dispatch observations**, all verified. Independent read-only auditor reconstructed the source edits without importing the compiler, verified every trace and source identity. **12/12 tests passed**, including six evidence mutations; synthetic forwarding hardcoding rejected before execution.

| Configuration | Omitted HEAD calls forwarding True | Other cases |
| --- | ---: | ---: |
| Baseline | 0/3 | 15/15 verified |
| API only | 1/3 | 15/15 verified |
| Client only | 2/3 | 15/15 verified |
| Both | 3/3 | 15/15 verified |

**Casewise factorial interaction is zero on all three entry points.** Two production files require edits to cover all three entry points, but the observed forwarding behavior is parallel/independent, not a cross-file semantic conjunction. This falsifies any inference that merely touching multiple production files proves a semantic interaction.

The edited source retains **five potentially stale documentation fragments** (three inline comments and two docstring lines). This is a release-review obligation.

## Limitations and status

The CPython bodies were extracted from pinned historical source, with annotations removed and request calls instrumented. **Not** a full historical HTTPX package run, network redirect test, complete nonregression oracle, prospective qualification or new model inference. The source is trusted historical code, not model-authored code. The historical cohort remains **8 reference-qualified PRs across 7 repositories**. No IR superiority or breakthrough claim. All 89 reserved issues remain sealed. Full raw evidence, tests, auditor, and 15 SHA-verified payloads preserved in local archive `lattice_run354_httpx_real_dispatch_factorial.zip`, SHA-256 `160f9e6e9723f5c3f6aa5424a3715c4c1dcfc27a56d468a621c09535897bd097`; historical GitHub ZIP mirroring remains incomplete.
