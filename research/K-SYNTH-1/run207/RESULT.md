# K-SYNTH-1 Run207 — repository-wide transaction science (2026-10-24)

## Completed local experiment
A new common compiler implements exact-content, SHA-256-guarded multi-file replacement, creation and deletion across tracked text files, not just Python. It rejects path traversal, symlinks, stale versions, ambiguous anchors, overlapping edits, Python syntax errors, no-ops and removal of leading legal headers. Its in-memory compilation is transactional; filesystem publication is **not** crash-atomic and is restricted to disposable worktrees.

**Executed locally:** 22 regression tests passed; 2,000 independently generated cases were replayed under each of three action representations (6,000 compilations), plus 2,000 non-Python transactions, with zero disagreements against the independent string-replacement oracle. These are compiler-parity tests, **not capable-model results**.

A prospective two-issue pilot has been frozen from the Run201 discovery list: `zulip__zulip-terminal-1463` and `quansight__ragna-426`. The three arms are bounded semantic-node IR, ordinary Python exact-text patches, and Python patches with the same short structural IDs. All share issue facts, target tables, a single gold-blind retrieval stage, identical repository-wide authority and the same compiler. The short-ID Python arm controls for address-copy length. The Qwen2.5-Coder-7B-Instruct Q4_K_M model SHA is `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, with temperature 0, 2,048 output tokens, and deterministic issue-derived seeds.

**Important:** this pilot has not yet run model inference. Compiler acceptance is not functional issue resolution. The AST-node interface is not a full semantic programming language. The 89 held-out boundary issues remain untouched.

## Persistence and next action
Full source, independent oracle, tests, 8,000 local compiler traces, frozen manifest, workflow and checksums are in the Run207 reproducibility archive produced in this automation. The GitHub connector cannot directly read local container files; source-bundle upload is pending and must be retried without pausing research. Next: persist and execute the frozen open-model pilot, then build a sealed independent functional evaluator before the adequately powered study.

Previous cluster-power sensitivity: 391 discovery issues / 157 repositories had ~73.4% modeled power for a specified large effect; ~468 / 187 was the earlier 80% planning estimate. These are assumptions, not observations, and must be recalculated once functional outcomes and pilot discordance are available.
