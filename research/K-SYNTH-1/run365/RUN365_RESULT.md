# K-SYNTH-1 Run365: import-boundary gate and real HTTPcore counterexample

2026-10-30 UTC. One canonical branch, PR #9 open/draft/unmerged, all 89 reserved issues sealed.

Independent audit of ORIGINAL cloud evidence: Flask #5928 artifact SHA256 `deff0b0a86093b6822dbd46b93239a8e3e4a66979948a7d05110f64a75ae111a`, 20/20 inner hashes, 60 observed functional cases, 36 pre-oracle ImportErrors. urllib3 #5126 original inner artifact SHA256 `09a787735ea2689c669002fa002034c8231f74db37203380ccd2b0f7eacb4314`, 12/12 inner hashes, 39 observed, 13 pre-oracle ImportErrors. Neither failed qualification is promoted or retuned.

A conservative AST import-name gate predicts all 12 historical import-failure masks from independently established direct-import facts, and 12/12 isolated self-authored synthetic CPython fixtures agree. A dynamic module `__getattr__` counterexample demonstrates why unsupported constructs must remain UNKNOWN. 12 local unit tests and 12 additional seeded acyclic import fixtures passed. Minimal reconstructed AST witnesses are NOT historical source bytes. `NO_DIRECT_NAME_MISSING` does NOT guarantee runtime import success.

Screened merged [HTTPcore #1000](https://github.com/encode/httpcore/pull/1000), pinned base `5974b03c7df89d3ee4e23779900d5349d550753c`, reference `7fb20526175e2300185ce2b472a97acca95b2525`. Base/reference sync blobs: `9ccfa53e597a29ee387f9d16f3af4f695ac0d33a` / `4b26f9c63032be5c6c932b9d1339c43d4029368e`; async blobs: `96e973d0ce223f6bed9be9e6a6a2f3c01622c611` / `5ef74e6497f1fe44b7be520f8e1502e8786e91fd`.

The original idle-connection predicate counts all connections, not idle connections. For an idle candidate, n total, k idle and cap m, old closes while reference retains iff k <= m < n. Exhaustive n<=10: **188,412** predicate evaluations, **37,886** old-only closures, zero new-only closures. Actual installed HTTPcore 1.0.9 preflight removed an idle connection when one busy + one idle existed with cap=1. This is not a historical pinned factorial or a newly qualified repair; the reference patch was inspected, so #1000 is not a blind model benchmark.

The complete SHA-verified local archive `lattice_run365_import_gate_and_httpcore_counterexample.zip` has 15 evidence payloads, SHA256 `225f60300fb9c64ec898d74c7a96b21543b5d7d6782f7033042550e7d9f70948`. It includes full independent auditors, original evidence ZIPs, exhaustive predicate aggregate and witness traces, functional preflight and tests. **Qualified cohort unchanged: 8 PRs across 7 repos. No Qwen inference or IR superiority.**
