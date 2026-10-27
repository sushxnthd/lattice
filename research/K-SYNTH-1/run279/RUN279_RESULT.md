# K-SYNTH-1 Run279 | Prospective HTTPcore repair and bounded cardinality IR

Date: 2026-10-27 IST. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole open/draft/unmerged PR #9. All 89 reserved boundary issues SEALED.

## Independent new repository-cluster candidate

Identified merged [encode/httpcore PR1000](https://github.com/encode/httpcore/pull/1000). Verified its direct-parent base `5974b03c7df89d3ee4e23779900d5349d550753c` and direct-child reference `7fb20526175e2300185ce2b472a97acca95b2525`. The two production files are `httpcore/_sync/connection_pool.py` and `httpcore/_async/connection_pool.py`. Both upstream corrections replace `len([connection.is_idle() for connection in self._connections])` with `sum(connection.is_idle() for connection in self._connections)`.

Before any source ablation, froze an independent network-disabled public-API 4x10 qualification: two sync targets, two async targets, and six controls (zero keepalive, one idle, reuse for both modes). Four configurations: baseline, sync-only, async-only, complete reference. Frozen target/control pass counts required: baseline 0/4+6/6; sync-only 2/4+6/6; async-only 2/4+6/6; full reference 4/4+6/6. The ten named tests, SHA-pinned source commits, direct-parent assertion and strict qualification criteria cannot be retuned.

Committed the SHA-verified compressed source/test/freeze transport and [workflow](../../../../.github/workflows/lattice-k-synth-1-run279-httpcore.yml), then launched [Actions 40428602984](https://github.com/sushxnthd/lattice/actions/runs/40428602984) with commit `83464485d90a68b9e9314a729c227dc68ba3c570`. At the last check the workflow was QUEUED; no original functional outcomes or artifact recovered. **PR1000 is NOT qualified yet**. The qualified cohort remains three distinct issues: Flask PR6096, urllib3 PR5071, Werkzeug PR3136.

## Soundness-scoped semantic mechanism

Implemented a conditional exact cardinality/dataflow transfer. Under a finite stable exact list/tuple, pure deterministic exact-bool predicate and no name rebinding, `len([p(x) for x in C])` counts all elements, whereas `sum(p(x) for x in C)` counts only true predicates. Constructive witness: one idle and two active connections, limit one: baseline 3>1 closes an idle connection, corrected 1>1 does not.

**Source AST recognition is only CANDIDATE_UNVERIFIED**, not a runtime binding/purity certificate. Unverified contracts and unsupported constructs return explicit UNKNOWN. A separately implemented trusted CPython expression oracle agreed with the transfer on **8,191 exhaustive Boolean vectors (length 0–12) and 4,096 seeded vectors (12,287 total, zero mismatches)**. Raw trace SHA256 `d33319ab411a1a87a4fbf0e210af6db524cfbc048d15bf738d0489a114d2a172`. All 12 local IR/freeze tests passed. This is a restricted theorem and counterexample, **not general sound Python IR** or evidence of representation superiority.

Independent read-only re-audits of Run278 recovered and verified all 40 original qualification outcomes and all 24 frozen holdout predictions, with unchanged SHA digests.

## Limits and Run280

No new coding-model inference or accepted patch transaction. HTTPcore qualification pending. Three qualified issues are not powered; no significance or breakthrough. Complete historical GitHub ZIP mirroring remains incomplete. Next recover original Actions 40428602984 artifact and audit all 40 frozen outcomes without post-hoc modifications; promote only if the exact frozen criteria pass. Then advance cross-file binding/effect analysis, blind capable-model paired functional evidence and SHA mirroring. All 89 boundary issues remain SEALED.
