# K-SYNTH-1 Run370 — PRE-REFERENCE PROSPECTIVE FREEZE
Date: 2026-10-30 UTC. Status: **FROZEN BEFORE INSPECTING FIX PR OR PATCH**.

## Candidate and provenance
- Public issue: encode/httpcore#550, "Request errors on overloaded systems may poison the connection pool", https://github.com/encode/httpcore/issues/550
- Reported affected release: httpcore 0.14.7; report independently describes both sync and async failures, a maximum-one-connection pool, a request timing out after assignment, and a persistent CONNECTING entry.
- Pre-fix source ref: `0.14.7`; pre-fix Git blob `httpcore/_sync/connection_pool.py` = `32bc77895191c35e0f155c913462395f1b2067d6`; `httpcore/_async/connection_pool.py` = `ae3854b1815540625c1dffa1b8503fd9b9f07f44`. Both identities obtained directly from repository contents before fix lookup.
- Independent new issue identifier: `encode/httpcore#550`. Not in nine qualified PRs or named historical failures in the available ledger. A full ledger deduplication is required before promotion.
- No reference patch, reference changed-file list, or reference PR has been read before this freeze. The two-file hypothesis comes from the **issue's explicit sync/async report**, not from reference localization.

## Fixed scope and adjudication
Only the two predeclared pool production modules may be edited for the model comparison; if the eventual upstream reference requires additional files, report a scope mismatch, never widen scope after outcome. A full historical 2x2 uses baseline, sync-only, async-only, and both-reference variants, all based on the same immutable pre-fix tree. Source importability and functional behavior are separate outcomes. A pre-oracle import failure is INCONCLUSIVE, not FAIL or zero.

### Six target assertions, frozen before fix inspection
- T-S1: sync: after connection assignment followed by a forced pool-wait timeout, the pool does not strand an unavailable connecting entry indefinitely.
- T-S2: sync: a subsequent independent request can acquire a connection when max_connections=1 and the earlier assigned request timed out.
- T-S3: sync: after timeout and cleanup, tracked live connections do not exceed the configured maximum.
- T-A1/T-A2/T-A3: the corresponding async assertions, including cancellation at the same assignment/wait boundary.
Each target must be tested with a deterministic scheduling hook, bounded wall clock, no external network and explicit raw state traces. If the hook cannot be implemented without changing the target production semantics, mark NOT_EXECUTED rather than changing the target.

### Eight controls
- C-S1/C-A1: normal successful acquisition and release preserve functionality.
- C-S2/C-A2: timeout while still unassigned leaves no queued request.
- C-S3/C-A3: a healthy idle connection remains eligible for reuse.
- C-S4/C-A4: cleanup does not close an actively owned connection from an unrelated request.
Control outcomes must be checked on the baseline before any historical qualification. A baseline control failure is FAIL, not retunable.

## Qualification rule
A task qualifies only if (i) exact pinned upstream source trees are executed in isolated, unprivileged, network-disabled or loopback-only environments; (ii) all four arms import and execute all 14 frozen cases; (iii) baseline passes all 8 controls and fails at least one target in each backend; (iv) full reference passes all 6 targets and all 8 controls; (v) each one-file partial fails at least one target or control; (vi) no target/controls are changed after this freeze; (vii) the candidate is independently deduplicated; and (viii) an independent verifier checks hashes and raw traces. Source-only reconstructions and synthetic models are diagnostics, not qualification.

## Mechanism and model comparison
Separately report per-case factorial interactions; aggregate all-pass interaction does not imply cross-file semantic dependence. Run369 MAY graph may certify only accepted pure acyclic fragments; these real dynamic modules must be UNKNOWN until proven otherwise. A paired IR-vs-Python/AST trial requires equal issue facts, pre-fix source, allowed edits, edit compiler, verifier, oracle, actual model SHA, token counts, raw outputs, and randomized arm order. No reference-derived localization or paid model. A reference-informed qualification does not count as a blinded model success.

## Failure discipline
No retroactive criteria edits; no promotion on import failures, missing raw model completions, synthetic-only evidence, or post-outcome adapters. Keep all 89 boundary issues sealed; sole branch `research/exp003-context-order`, sole PR #9 open/draft/unmerged. GitHub failures must be logged and must not stop substantive local research.
