# K-SYNTH-1 Run282: frozen HTTPcore transport recovery and bounded interval IR

Date: 2026-10-27 (IST). Canonical branch `research/exp003-context-order`, one draft PR #9. All 89 reserved boundary issues remain sealed.

## Original experiment and correction

The Run281 frozen HTTPcore replay, GitHub Actions 40438772162, completed **failure before any scientific oracle ran**. Its job log shows the restored Run279 source archive extracted correctly, but the subsequent `sha256sum -c` was executed from inside `research/K-SYNTH-1/run279`, while the original manifest entries were repository-root-relative (`research/K-SYNTH-1/run279/...`). All four source-file checks consequently reported `FAILED open or read`. No artifact or functional observations were generated. This is a working-directory infrastructure failure, **not a negative functional repair result**.

Corrected the workflow in commit `b5ac72a605d86bceb753234a4f9a27f7a189f662` by executing the unchanged manifest from the repository root. Triggered a new run in commit `e97417483088c53377d6518ea60545a4c8d3d712`. Actions **40444443690** was `queued` at the independently retrieved 2026-10-27 03:29:26 UTC snapshot. This is a separately logged replay of the original frozen source, oracle, and criteria; no result is yet claimed. Do not promote HTTPcore until 40 real public-API outcomes are audited. The prior Run280 missing-`certifi` dependency failure remains separately preserved.

## New substantive scientific artifact: cardinality interval abstract interpreter

Implemented `run282_interval_semantic_ir.py`, a bounded source-pattern-checked semantic IR for the HTTPcore PR1000 Boolean counting bug. It recognizes exactly the audited AST transition from `len([connection.is_idle() for ...]) > k` to `sum(connection.is_idle() for ...) > k` and refuses to certify other templates. Inputs are a finite collection size `n`, a sound interval `[lo,hi]` of true Boolean predicate counts, integer threshold `k`, and five externally justified assumptions: finite, stable, pure, Boolean return, and integer threshold. The analyzer does **not** infer those assumptions from Python source.

It returns `MUST_AGREE`, `MUST_DIVERGE`, `MAY_DIVERGE`, or `UNKNOWN`. The proof is elementary: for a stable Boolean sequence of length `n`, the original predicate is `n>k` and the repaired predicate is `i>k` for true count `i` in `[lo,hi]`. If `n<=k`, both are false. Otherwise the guards must diverge when `hi<=k`, must agree when `lo>k`, and may diverge otherwise. Invalid bounds, noninteger inputs, and unproved assumptions yield `UNKNOWN`. This is an exact abstract interpretation of this **fixed expression family**, not a production-wide Python semantic proof.

Independent CPython execution of the two fixed AST expressions checked **6,370 interval/threshold cases** and **26,572 concrete evaluations**, with **zero certificate disagreements**. The outcome counts were 3,640 `MUST_AGREE`, 1,365 `MUST_DIVERGE`, and 1,365 `MAY_DIVERGE`. Nine invalid-assumption/bound controls returned `UNKNOWN`. Eight independent unit tests passed. A non-Boolean predicate return `[2,2]` with threshold 3 gives original false and repaired true, demonstrating the need for the Boolean assumption.

The same exact task facts are also serialized as an ordinary Python dataclass/dictionary view; the IR has **no information or edit-authority advantage**. This work develops a verified mechanism and an explicit soundness boundary. It does not test coding-model performance, provide an independent evaluator for arbitrary Python, or establish a Lattice advantage.

## Integrity and limits

Local archive contains the executable interpreter, unit tests, complete raw interval trace, summary, previous Run281 archive, workflow-failure ledger, and SHA-256 manifest. Historical GitHub source/ZIP mirroring is still incomplete; retry. Three previously qualified independent issues remain Flask PR6096, urllib3 PR5071, and Werkzeug PR3136. HTTPcore is still pending. No powered McNemar comparison, functional coding-model repair, or breakthrough.
