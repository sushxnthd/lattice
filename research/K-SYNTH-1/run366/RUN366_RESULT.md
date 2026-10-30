# K-SYNTH-1 Run366: HTTPcore mirrored-backend experiment and aggregation counterexample

Date: 2026-10-30 UTC. Canonical branch `research/exp003-context-order`; sole draft PR #9; all 89 reserved issues SEALED.

## Exact historical provenance, local reconstruction scope

Verified upstream HTTPcore PR #1000's four source blobs directly via GitHub: sync base `9ccfa53e597a29ee387f9d16f3af4f695ac0d33a`, sync head `4b26f9c63032be5c6c932b9d1339c43d4029368e`; async base `96e973d0ce223f6bed9be9e6a6a2f3c01622c611`, async head `5ef74e6497f1fe44b7be520f8e1502e8786e91fd`. Base commit `5974b03c7df89d3ee4e23779900d5349d550753c`; PR head `7fb20526175e2300185ce2b472a97acca95b2525`. Both historical method excerpts replace `len([c.is_idle() for c in self._connections])` with `sum(c.is_idle() for c in self._connections)`.

**Executed scope:** source-normalized four-way reconstruction on installed HTTPcore 1.0.9, NOT the complete historical source checkout. No new historical task is qualified. The reference patch was inspected, so this is not a reference-blind model benchmark.

## Frozen local functional oracle

The 36-case oracle was frozen before executing the matrix (SHA-256 `1889d4e0b71610018b94fa87084199de280323cedf3133eeac7588025ff30797`). Eight mixed busy/idle targets and ten cleanup/nonregression controls per backend. Twelve independent unit tests passed. All 144 functional observations executed in separately isolated package-copy subprocesses.

| Source | Sync targets | Async targets | Sync controls | Async controls |
|---|---:|---:|---:|---:|
| Old/old | 0/8 | 0/8 | 9/10 | 9/10 |
| New sync/old async | 8/8 | 0/8 | 10/10 | 9/10 |
| Old sync/new async | 0/8 | 8/8 | 9/10 | 10/10 |
| New/new | 8/8 | 8/8 | 10/10 | 10/10 |

**Prospective qualification FAIL:** baseline violates the predeclared `busy_idle_closed` control in both backends: a later closed connection is still counted when deciding whether to evict an earlier healthy idle connection. Do not relabel/remove this failed control post-outcome. The exact historical-tree factorial is NOT_EXECUTED.

## Exact mechanism counterexample

Across all **36 individual cases**, additive 2x2 interaction is **0**, and each backend's outcome depends only on its own source arm. Yet the nonlinear global endpoint `ALL targets pass` yields interaction **+1** (false in baseline and both single-arm variants, true only in the double-arm variant). `ALL 36 cases pass` also yields +1. Therefore an all-tests-pass interaction alone cannot identify cross-file semantic coupling: an AND of two independently repaired backends creates apparent synergy.

## Separate postfreeze adversarial probe

Actual HTTPcore HTTP/1.1 can have `has_expired()==True` and `is_idle()==True` simultaneously. With a healthy idle connection before an expired idle connection and cap 1, both old and new predicates close both connections; reversing the order preserves the healthy one. Executed for both sync and async. This is a bounded retention-efficiency/order-sensitivity witness, not necessarily protocol incorrectness (the cap is an upper bound). It was NOT used to alter the frozen primary endpoint.

## Scientific status

Cohort unchanged: **8 qualified PRs / 7 repositories**. No new Qwen inference, powered IR advantage, independent historical qualification or breakthrough. The complete 15-payload SHA-verified local ZIP is `lattice_run366_local_httpcore_factorial_and_aggregation_counterexample.zip`, SHA-256 `3f60a9ee5667f34d8cfb2036e3cec705aa739f1a5026686157342bb1b7203696`. The original frozen oracle and all 144 raw observations are in the local archive; not yet fully mirrored to GitHub.

Next: exact historical pinned-tree replay with the unchanged failed control; recruit a new reference-blind multi-file repair; then perform information-equivalent semantic/dataflow IR versus ordinary Python/AST real-model functional comparisons using shared compiler/oracle, full raw outputs, and clustered power planning. All 89 boundary issues remain SEALED.
