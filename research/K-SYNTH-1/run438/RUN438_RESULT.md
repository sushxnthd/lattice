# K-SYNTH-1 Run438 — POSIX snapshot publication and fault-injection audit

## Finding
Run437's lossless two-file compiler returned an in-memory transaction but did not provide an atomic on-disk multi-file update. Run438 implements a **trusted, content-addressed generation store**: both verified files are staged, fsynced and published in one immutable generation, followed by a single atomic HEAD replacement. Readers must resolve HEAD once and verify both source hashes. An advisory single-writer lock rejects stale concurrent actions.

## Executed evidence
- **2,048 actual filesystem transactions** from 128 deterministic fixtures × 2 information-equivalent IR/AST action modes × 8 normal/injected conditions.
- **1,792 injected failures**, with **1,280 old** and **768 new** complete snapshots visible, **zero mixed generations**. 512 injected failures occurred after the HEAD publication point: exceptions do **not** necessarily mean rollback.
- **25/25 regression tests passed**, including corrupted-source rejection, stale SHA, lock serialization, seven failure checkpoints and recovery.
- Independent replay audited all **2,048 receipts** and ran **256 fresh locked commits**, **8,192 actual CPython function calls**, **8,192 functional checks**, **1,024 source checks**, zero disagreements.
- Executable counterexample: direct provider-first in-place writes expose intermediate output **30**, between old **22** and new **42**; verified snapshot readers observe only 22 or 42.

## Scope
This is a POSIX, single-cooperative-writer, snapshot-reader, trusted-affine-grammar result. The linearization point is os.replace(HEAD.tmp, HEAD). No physical power-loss simulation, general Python editing, arbitrary filesystem security, distributed transaction, or adversarial-symlink guarantee is claimed. fsync improves durability but does not prove it. Historical generations are retained; no garbage collection is attempted.

## Real task and model evidence
Strict independent qualified real multi-production-source repair count remains **two** (Flask PR6096, urllib3 PR5071). Flask #4297 historical workflow artifact was not verified; its post-reference oracle cannot qualify it prospectively. No new coding-model completions, powered IR superiority evidence, or breakthrough. All 89 reserved issues remain sealed.

Complete raw evidence, implementation, independent auditor and SHA-256 manifest: local Run438 reproducibility archive, SHA-256 `b5b0048c5a5b2d6e8b601cb4611b99198172911ef9053fc6edb9f0163d1a5b49`. GitHub code mirroring may lag the local verified archive.