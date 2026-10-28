# K-SYNTH-1 Run315 result

**Decision: PASS, bounded synthetic compiler engineering validation only.** No new production repair qualification, no coding-model inference, no IR superiority or breakthrough.

Prospective frozen protocol commit: `c0310d70bae18e59e052d39315919cf8c08b8308` (before primary execution). The four source/fixture hashes in that protocol matched the executed local files.

## Results
- 384 correlated synthetic cases, three trusted Python modules per case, six edits per case.
- 384/384 byte-identical semantic-IR vs literal Python `ast.Constant(value=INTEGER)` action outputs, identical facts, source/node SHA preconditions, byte spans, authority and shared compiler.
- 2,304/2,304 edit spans independently reconstructed; 384/384 isolated trusted functional case replays passed.
- 384/384 injected failures before pointer publication preserved the previous snapshot.
- 11/11 malformed, stale, unauthorized or overlapping negative controls rejected.
- Independent auditor: zero discrepancies.

## Critical limitation
Multiple unrelated filesystem paths cannot generally be overwritten atomically. The compiler returns a complete snapshot; the prototype writes content-addressed files then replaces one CURRENT pointer. Only readers resolving CURRENT once get snapshot consistency. No proof of crash consistency, concurrent writers or power-loss durability. This is not yet a production-ready filesystem transaction manager.

## Production expressibility
The bounded compiler only edits canonical integer constants and **cannot express** the historical h11 PR #115 reference, which changes function calls, control flow and buffer logic. Its patch was inspected only to assess expressibility, not to supply model localization hints. No model repair inference or production oracle was run in this experiment.

## Evidence
Complete SHA-verified local reproducibility ZIP: `lattice_run315_multifile_atomic_snapshot_parity.zip`, SHA-256 `e89b60173ff5627add1899b85000be980065dd44ca8a21ac0c492d6d15fdac2a`. Twelve evidence payloads plus manifest. Raw trace SHA-256 `7ff47a0cf51ca7a3ca0cb8269d2b976f91c4b6d6c7219dbd730df13e8bbfde3e`. The complete archive is local; this report does not assert that the ZIP has been mirrored to GitHub.

Six previously qualified historical repairs remain six. All 89 reserved boundary issues untouched. No historical frozen criteria modified.