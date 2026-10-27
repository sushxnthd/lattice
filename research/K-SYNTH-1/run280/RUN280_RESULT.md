# K-SYNTH-1 Run280 | HTTPcore source-identical transport recovery and Boolean threshold proof

Date: 2026-10-27 IST. Canonical branch `research/exp003-context-order`, sole open/draft/unmerged PR #9; all 89 boundary issues SEALED.

## Original Run279 failure, preserved

GitHub Actions [40428602984](https://github.com/sushxnthd/lattice/actions/runs/40428602984) failed **before functional evaluation**. All 12 original freeze/IR tests passed; upstream clone failed at `git worktree add` with `fatal: invalid reference: 7fb20526175e2300185ce2b472a97acca95b2525`. No functional outcomes or artifact were produced. This is a transport failure, not a failed scientific qualification or model repair.

The original PR-head SHA was squash-merged into upstream master as reachable direct-child commit `10a658221deb38a4c5b16db55ab554b0bf731707` (parent `5974b03c7df89d3ee4e23779900d5349d550753c`). Independent GitHub file reads confirm both original PR-head and merged commit have the **same exact production Git blobs**:
- `httpcore/_sync/connection_pool.py`: `4b26f9c63032be5c6c932b9d1339c43d4029368e`
- `httpcore/_async/connection_pool.py`: `5ef74e6497f1fe44b7be520f8e1502e8786e91fd`

Run280 is an explicitly separate transport-only replay. The wrapper verifies direct-parent relationship and both original Git blob identities before running the **unchanged** Run279 frozen 4x10 public-API oracle, expected counts and source authority. No Run280 outcomes may be attributed retroactively to Run279.

## Independent semantic mechanism

An exhaustive independent CPython check of exact Boolean vectors of length 0..12 and integer thresholds 0..n+1 completed **106,496 evaluations**, all satisfying the theorem: for n finite stable elements, i true predicates and integer k, `len([p(x) for x in C]) > k` differs from `sum(p(x) for x in C) > k` iff `i <= k < n`. Exactly **45,057 discordances**, all in the predicted direction. Raw trace digest `a7f87a97e4b540c00c05fdc0dd56b04427157054f63b45da4e7dae5828036e95`. A non-Boolean predicate returning integer 2 twice at threshold 3 reverses the direction, demonstrating the scope limitation. This is a bounded mechanism proof, not general sound Python IR.

**15/15 local tests passed** (12 inherited + 3 new). Source code, tests and workflow committed to the canonical branch. [Run280 cloud replay](https://github.com/sushxnthd/lattice/actions/runs/40430591378) was queued at the last check; no functional outcomes or promotion yet. Qualified cohort remains **three** (Flask PR6096, urllib3 PR5071, Werkzeug PR3136). No new capable-model repair, powered significance or representation superiority. Complete historical ZIP mirroring still outstanding.
