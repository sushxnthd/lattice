# K-SYNTH-1 Run349 — two-file causal-mechanism calibration

Date: 2026-10-29 UTC / 2026-10-30 IST. One K-SYNTH-1 kernel; 89 boundary issues SEALED.

## Experiment
Executed fixed, trusted synthetic two-file Python programs in 17 isolated `python -I -S` processes. Recorded 168 functional observations and 800 `sys.setprofile` call/return events, with source and runner SHA-256. Three predeclared families were: (1) ABI-compatible semantic conjunction, (2) parallel independent repair, and (3) ABI-confounded repair with a separate ABI-only compatibility adapter. Each family used four 2x2 source configurations, and eight input values per entry point. A separate runtime-rebinding negative control kept the same two source hashes.

## Observed casewise factorial results
- **Semantic conjunction:** four positive target interactions (+1) and four zero-interaction controls. Both versions preserve the tuple return shape and call signature.
- **Parallel repair:** all 16 casewise interactions zero, despite both files being needed to repair the combined task.
- **ABI confound:** four positive control interactions and four zero target interactions. The compatibility-only adapter removes all eight interactions.
- **Runtime rebinding:** with identical source hashes, rebinding the imported function eliminates observed producer-module calls and changes eight outputs to `x+100`. A lexical cross-file edge is not a universal runtime-MUST target.
- Independent truth-table auditor verified 168 records, 800 profile events, frozen source hashes and identities. Eleven tests passed, including eight corruption/omission tests.

## Scientific decision
These are **synthetic mechanism controls**, not a new independently qualified public-repository repair, no real coding-model inference, no semantic-IR advantage and no breakthrough. A dynamic call edge is `OBSERVED_ON_THIS_EXECUTION`, not an unconditional runtime-MUST. Historical cohort remains **eight source-qualified PRs across seven repositories**. The full local SHA-256-verified reproducibility archive includes raw traces, executable Python runner, independent auditor, tests, and source hashes; complete ZIP mirroring to GitHub is still pending.

The immediate blocker to the primary real-task paired pilot is no-cost capable-model execution with pinned model/tokenizer SHA and isolated oracle. The Run349 calibration does not replace that pilot. Next: Jinja #1242 and HTTPcore #882 with shared compiler, matched IR/Python-AST facts, exact tokenization, ABI controls, blind task localization, raw model completions and independent evaluator. No untrusted model code executed on host.
