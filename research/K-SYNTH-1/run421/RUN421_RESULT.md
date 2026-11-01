# K-SYNTH-1 Run421: MAY-effect graph, real-source coverage, and equal-authority test

Date: 2026-11-01 UTC / 2026-11-02 IST. Canonical branch `research/exp003-context-order`, sole draft PR #9. All 89 reserved boundary issues remained sealed.

## Scientific question

Run420's strict exact-integer SSA certificate covered zero eligible edits among 1,700 inspected functions. Can a conservative descriptive MAY-effect/dataflow graph expose useful lexical structure while retaining explicit UNKNOWN for dynamic Python effects and **without restricting ordinary Python/AST editing authority**?

## Implementation and executed evidence

A new source-aligned AST graph records statement reads/writes, branch-insensitive lexical MAY def-use edges, possible UNKNOWN effect couplings and explicit tags for dynamic dispatch, control flow, deferred code, complex targets, imports and unmodeled effects. It grants no edit authority and makes no noninterference or soundness claim. It is **not yet a verified semantic/dataflow action selector**.

Read-only scan of installed urllib3 2.7.0, HTTPX 0.28.1, Requests 2.32.5 and Click 8.1.8:
- 93 Python source files SHA-256 recorded; 1,700 function graphs, 10,328 statement nodes.
- 7,197 lexical MAY def-use edges and 73,490 UNKNOWN possible-effect edges.
- 771 functions with lexical edges; 1,595 with at least one UNKNOWN node.
- 105 functions without a flagged UNKNOWN are **not certified pure**.

304 seeded first-party functional before/after pairs ran in isolated CPython (608 executions): 48 each for overloaded operators, properties, truthiness, iteration and global mutation, plus 64 pure controls. All 240 dynamic-effect pairs changed observable outputs and had UNKNOWN; all 64 pure controls were unchanged. This bounded construction is not a general proof.

128 seeded two-file transactions used the same Run419 atomic compiler, source hashes, authority and graph facts for structural-fingerprint and ordinary AST-index action encodings. All 128 outputs and receipts matched byte-for-byte. The structural fingerprint is **not** a genuine semantic selector; this is transport parity, not model evidence.

Independent read-only auditor re-executed 608 additional CPython subprocesses, rebuilt all 1,700 graphs, rehashed 93 files and replayed all 128 paired transactions: **13,064 checks, zero disagreements**. Twelve adversarial unit tests passed.

## Limitations and status

No new coding-model inference, no new independently qualified real multi-production-source repair, no powered semantic-IR advantage. Qualified count remains **two** (Flask PR6096 and urllib3 PR5071). Installed package snapshots are not pinned historical PR bases. Graph UNKNOWN is a warning against absence inference, not a proof of effect.

Local SHA-verified 24-entry reproducibility archive:
`lattice_run421_may_graph_effects_and_equal_authority.zip`
SHA-256 `bb399cf3419a903bf259325d29e81626ce8062f84c7b76588a350e2b4e9982e3`.
Full raw archive is preserved locally; GitHub ZIP mirroring remains incomplete.

## Next

Reconstruct full pinned historical source and reference trees and test complete reference expressibility through the shared compiler; then implement a genuinely typed semantic/dataflow action selector and run matched functional open-model inference. Prospectively freeze independent real multi-source issues before reference inspection. Keep all 89 sealed, one branch and sole draft PR #9.
