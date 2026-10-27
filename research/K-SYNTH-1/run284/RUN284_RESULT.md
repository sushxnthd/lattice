# K-SYNTH-1 Run284: prospective HTTPcore phase holdout passes

Date: 2026-10-27 IST. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, ONE open/draft/unmerged PR #9. All 89 reserved boundary issues SEALED.

## Prospectively frozen third holdout, independently audited

Run283's original frozen HTTPcore holdout **FAILED scientifically** (8/32 predictions wrong). After observing that negative result, Run283 developed a posthoc cleanup-before-create phase model. Run284 tested this model on NEW cases prospectively frozen BEFORE execution. Frozen GitHub commit: `e409c101ac1e325043d858c90d9dfc288de29f91`. Frozen JSON SHA256: `6a0c19792707d58271bd0fbf40bbd5900203437b0a120560ae9a70bc170f79cb`. Original pinned Run279 oracle SHA256: `6d1fbb5d18aa7b58da802fb34f43ec6a5efcfc7a3842049df2fb02f18d2e2e96`. New frozen oracle SHA256: `b6f53c1c99fadc5a4767b0dd0ceedf5725b8b947d75d122739ee74ab7eb97892`.

The 18 new mode/case combinations were sync and async for `(limit, active)` pairs `(2,1),(2,2),(2,4),(4,3),(4,4),(4,5),(5,4),(5,5),(5,6)`. Four source arms (baseline, sync-only, async-only, complete reference) share the same upstream source and MockBackend public-API oracle. Each of the **72 frozen predictions** included exact `before`, `during` idle counts and Boolean pass, not merely aggregate success. Expected success counts were **12/18, 15/18, 15/18, 18/18**.

[Original Actions run 40453471542](https://github.com/sushxnthd/lattice/actions/runs/40453471542) COMPLETED SUCCESS. Original artifact ID `12711536031`, ZIP SHA256 `499cce75d66bb4a57f7b5dc7182cdeca563b1ac5a9d61ae661b1f6df91d9cf02`, matching GitHub's digest. Independent read-only auditor verified **all five original manifest payload hashes**, pinned frozen spec/oracle hashes, exact case ordering, 72 raw observations, four zero-exit subprocesses, zero censored cases, and zero per-case disagreements. All 72 predictions matched, with the exact frozen per-arm counts.

This is **successful prospective unseen-boundary prediction of a previously posthoc-derived temporal mechanism**, strictly within the same HTTPcore issue, source, MockBackend and public-API family. The 72 correlated source-arm observations are NOT independent repair issues or powered model evidence. The original failed Run283 holdout remains FAILED without retroactive changes.

## Independent scoped event-order theorem

Under attested finite stable collections, exact-Boolean pure idle predicates, one initial idle, distinct-origin/no reuse, no expiry, positive stable integer limit, trusted event order and no other pool limits, the original guard retains idle after `cleanup_before_create` iff `q <= k`; after counterfactual `cleanup_after_create` iff `q < k` (for q>=1). The repaired guard retains idle in both. Thus event order alone changes predictions at q=k, the previously missed boundary.

An independent step interpreter and closed-form certificate agreed on **16,640 evaluations**, with zero mismatches and **64 event-order-sensitive witnesses**. Six deliberately unsupported cases returned `UNKNOWN`. These are scoped abstract-state results, not full Python/HTTPcore soundness, not model repairs and not an intrinsic IR advantage.

## Integrity and limits

Pinned base `5974b03c7df89d3ee4e23779900d5349d550753c`, source-identical direct-child ref alias `10a658221deb38a4c5b16db55ab554b0bf731707`, both production file SHA pairs in frozen JSON. GitHub commits: freeze `e409c101`, executable cloud runner `74bb2672`, workflow `ab3bc6a0`, launch `fe8d0344`. Cloud original code blob matches GitHub `910978826ea1cd06aa750d73f4eaed1bb34fad4b`. Full original ZIP, independent audit, 16,640-row trace, local tests, and previous Run283 archive are preserved in SHA-verified local reproducibility bundle.

The qualified cohort remains **FOUR independent real issues** (Flask PR6096, urllib3 PR5071, Werkzeug PR3136, HTTPcore PR1000). Run284 is not a fifth issue. No new coding-model inference, accepted model patch, powered IR-vs-Python comparison, or breakthrough. Historical GitHub ZIP mirroring Runs265–283 remains incomplete. All 89 sealed issues untouched.
