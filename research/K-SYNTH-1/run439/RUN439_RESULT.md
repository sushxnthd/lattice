# K-SYNTH-1 Run439 — Two real issue-first rejections and recovery-race counterexample

## Real public-repository screening (prospectively frozen)

Both candidate issues were registered on this branch **before** inspecting fixing references. All frozen target/control cases remain unchanged.

| Issue | Original frozen register | Merged reference | Changed production Python files | Decision |
|---|---|---|---|---|
| [Flask #4834](https://github.com/pallets/flask/issues/4834) | `1975c0bd6f50d19153343b451efc7e4db7549846` | [PR #4935](https://github.com/pallets/flask/pull/4935), merged 2023-01-04 | `src/flask/blueprints.py` only | REJECT |
| [urllib3 #3352](https://github.com/urllib3/urllib3/issues/3352) | `d9aa57b5a1d7f783aa7d31eacb78fe3a410f6e55` | [PR #4952](https://github.com/urllib3/urllib3/pull/4952), merged 2026-04-04 | `src/urllib3/connectionpool.py` only | REJECT |

The Flask 8-case historical oracle was frozen but not executed. urllib3 2.7.0 executed **8/8 real loopback HTTP requests** preserving raw request-target bytes, with 8/8 independent stdlib HTTP-server replays. These modern-version observations are **not** historical qualification evidence.

## Executed new counterexamples

Run438's original `recover()` does not acquire the same advisory lock as `commit_locked()`. In **32/32 real forked writer-process trials**, recovery removed an active stage and the writer subsequently raised `FileNotFoundError`. With new `recover_locked()`, **32/32** analogous transactions committed successfully. All 64 observed snapshots were internally consistent.

The original `read_snapshot()` blocks on a generation-source symlink to a FIFO because the symlink check follows the blocking read. A new descriptor-relative bounded reader uses `O_NOFOLLOW | O_NONBLOCK`, regular-file checks, size caps and generation digest verification. It rejected the FIFO fixture in **0.000444 s** in the recorded run. No hostile concurrent writer, mount-race, or power-loss security claim.

Independent auditor reconstructed all 64 original/new source digests and content-addressed generation IDs, and replayed the 8 HTTP cases using a different HTTP server: **452 checks, zero disagreements**. **13/13** adversarial/regression tests passed. Clean-extraction replay passed.

## Reproducibility

Local archive: `lattice_run439_issue_first_rejections_and_recovery_race.zip`; ZIP SHA-256 `d02d125857c6c1f0c1389e2d6ff326bfac9605dfba6c5eecfb096308f3cd15d1`; **20 entries, 19 SHA-256-verified payloads**, including complete original raw receipts, frozen issue-first executable oracles, source code, independent audit, tests and next protocol. Full ZIP not yet mirrored to GitHub.

**Scientific status:** Two qualified real multi-production-source repairs, unchanged (Flask PR6096 and urllib3 PR5071). No new coding-model completions, powered IR-vs-AST-action superiority, or breakthrough. All 89 reserved boundary issues SEALED. One K-SYNTH-1 kernel, canonical branch, one draft/unmerged PR #9. Next: matched functional open-model inference on the two qualified tasks and third independent real qualification.
