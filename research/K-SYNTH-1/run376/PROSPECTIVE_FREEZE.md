# K-SYNTH-1 Run376: prospective reference-blind issue freeze

Frozen before inspecting any fixing commit, pull-request diff, or later-version behavior.

## Issue and immutable baseline
- Public issue: https://github.com/encode/httpcore/issues/670 (2023-04-18), reported `ValueError: list.remove(x): x not in list` on cancellation of a queued async request.
- Baseline commit **5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e** is linked directly in the issue. Never substitute a later base.
- Source Git blobs at that commit: `httpcore/_async/connection_pool.py` **e6c4ef66312d4d6f31fcbfc417905ae329ef5885**, `httpcore/_sync/connection_pool.py` **53536d05e8c3d127b466e44dcf20e9f028aadab0**, `httpcore/_synchronization.py` **be3dcfda72158d1430c34c0387988eacac3452b8**.
- The source contains unconditional `self._requests.remove(status)` in the async and sync wait-exception handlers, while pool close methods clear `self._requests`. This is source inspection, **not** reference-patch inspection.

## Independently frozen test contract (no external network)
Use isolated, bounded subprocesses and public `httpcore` Request/Pool APIs, with max_connections=0 to guarantee a queued request. Explicitly distinguish original exception class from replacement exception class. All outcomes and timeouts recorded as raw JSON. No monkeypatching upstream methods.

**Public targets**
T1: async queued request, wait until pending, pool.aclose(), cancel task: cancellation must remain cancellation, not ValueError from stale queue removal.
T2: sync queued request in thread, wait until pending, pool.close(), let pool timeout: original PoolTimeout must propagate, not ValueError.

**Public controls**
C1: async queued request without pool close and with pool timeout -> PoolTimeout.
C2: sync queued request without pool close and with pool timeout -> PoolTimeout.
C3: async empty pool aclose idempotent.
C4: sync empty pool close idempotent.
C5: unsupported URL scheme rejected before queue mutation, async.
C6: unsupported URL scheme rejected before queue mutation, sync.

**Heldout targets** (sealed until public oracle works)
H1: async two pending tasks, close pool then cancel both; neither raises ValueError and no stale requests.
H2: sync two pending threads, close pool then timeout; neither raises ValueError and no stale requests.
H3: async cancellation before close, preserving ordinary cancellation.
H4: sync ordinary timeout before close, preserving PoolTimeout.

**Nonregression**: no network calls; all controls must pass on baseline and reference; source-blob identity and test-contract SHA must match; no timeout is counted as pass.

## Qualification gates
A) original baseline must fail at least one public target and pass all six controls.
B) the exact historical reference (if found only **after** this freeze) must pass both public targets and all six controls, plus all four heldouts.
C) source-level factorial arms: async-only, sync-only, full, none; full must pass all targets/controls and each one-component arm must fail at least one target or control. Report individual casewise interactions, not only aggregate all-pass synergy.
D) reference must actually change **at least two production files**, independently confirmed. A one-file fix is a prospective failure even if a two-file hypothetical repair can be constructed.
E) reference patch must apply cleanly to the pinned issue base; otherwise fail without retuning.
F) this is a recruitment/qualification experiment, **not** coding-model evidence. No representation advantage is inferred.

## Model comparison, if candidate qualifies
Freeze source/task facts before any model request. Semantic IR and Python/AST-action receive identical information, edit authority, compiler, isolated oracle, model ID/weight SHA, seed, output format, token budget, and retry policy. Record raw completions and all infrastructure errors. Reference-derived localization is forbidden.

## Integrity and guardrails
One K-SYNTH-1 kernel; only branch `research/exp003-context-order`; only PR #9, open/draft/unmerged. 89 reserved boundary issues remain sealed. No untrusted model code on host. No personal spend or laptop access.