# Run239 — pinned CrossGL three-file functional qualification: PASSED

**2026-10-25.** GitHub Actions [run 40164605118](https://github.com/sushxnthd/lattice/actions/runs/40164605118) completed successfully at Lattice commit `d3a180732099e3a04803873d6bb44eed46680625`. Original [artifact 12587786353](https://github.com/sushxnthd/lattice/actions/runs/40164605118/artifacts/12587786353) contains the full machine-readable per-case traces and hashes. Its contents were downloaded and independently audited. **No model inference was performed.**

Pinned public discovery task: `crossgl__crosstl-41` at `CrossGL/crosstl@d456c2b5f509104dd97b74ce40c597531784e2ca`, not one of the preceding 12 pilot issues. The upstream request concerns `else if` support across DirectX lexer, parser, and code generator. An independently authored calibration reference changes exactly these three files.

| Executed condition | Checks passed | Chain / multiline issue tests |
|---|---:|---|
| Original pinned upstream | 3/5 | both fail: parser expects LBRACE, sees IF |
| Three-file reference control | **5/5** | both pass |
| Reference omitting lexer change | 3/5 | both fail |
| Reference omitting parser change | 3/5 | both fail |
| Reference omitting generator change | 3/5 | both fail |

The three non-issue regression cases (plain if/else, nested else with if, and if-only) pass on baseline and reference. Checks include lexer tokens, AST structure, branch semantics via a restricted independent interpreter, and emitted CrossGL syntax. Four additional local structural tests passed in the cloud. Frozen evaluator and tests were verified against SHA-256 digests before execution.

**Prospective qualification passed**: baseline red on issue-specific checks, reference green on all five checks, three seeded defect controls red on issue-specific checks, and a positive-control edit changing three distinct files. The reference is not the upstream gold patch or a model response. The oracle does not execute CrossGL in a shader runtime; a different valid solution could use fewer than three files. This is one qualified calibration task, not an adequately powered functional study.

**Next scientific step:** freeze and execute a matched semantic-IR versus ordinary Python-source capable-model comparison on this qualified issue, with identical compiler/verifier/edit authority/task information/model/seeds/token budget and the frozen oracle. Do not reveal the calibration reference to the model. Expand to independent repositories for a cluster-aware adequately powered sample. The prior exact planning estimate of 306 independent pairs for 80% power applies only to assumed discordance .30 and conditional IR win .65; repository clustering can require many more. The 89 reserved boundary issues remain sealed.

**No representation advantage, mechanism attribution, unseen-boundary validation, or completion claim.** Full plain-text source, original cloud artifact, independent audit and SHA-256 manifest are preserved in the local Run239 reproducibility archive.
