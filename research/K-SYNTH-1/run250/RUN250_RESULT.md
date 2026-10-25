# K-SYNTH-1 Run250 — genuine Qwen inference recovered and independently audited

Date: 2026-10-25. Research branch: `research/exp003-context-order`. Draft PR: #9.

## Provenance

The corrected GitHub Actions [Run248 retry #5](https://github.com/sushxnthd/lattice/actions/runs/40207052721) completed successfully at commit `f6b117bb7d2edcb4016f05d2357d255a17100917`. Artifact ID `12604538934` is 132,396 bytes, SHA-256 `8510309dd266d7ba33b37afab3a8275d8aaff55198aa06cd423860ac4fddbf4c`. This is genuine model inference, unlike the earlier pre-inference failures. All three frozen request SHA-256 hashes, raw-response and completion hashes, model ID, seed, token usage, engine and upstream pins, and prompt-component parity were independently verified. Seven local auditor regression tests passed.

Model: Qwen2.5-Coder-7B-Instruct Q4_K_M; GGUF SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; seed 24741; temperature 0; max 3,072 completion tokens. Pinned CrossGL commit: `d456c2b5f509104dd97b74ce40c597531784e2ca`.

| Condition | Prompt content tokens | Reported prompt/completion | Strict format | Compiler | Functional |
|---|---:|---:|---|---|---|
| Syntactic graph first | 8,418 | 8,447 / 931 | Rejected | Not reached | Not evaluated |
| Python first, same graph | 8,418 | 8,447 / 912 | Accepted | Accepted | 3/5 |
| Python source only | 2,281 | 2,310 / 928 | Accepted | Accepted | 3/5 |

The original baseline passed 3/5 and the independently authored reference passed 5/5. No model condition achieved a functional repair.

## Independent mechanism audit

- Graph-first emitted three extra `# FILE ...` lines outside the permitted edit blocks. The common strict parser rejected line 1. A separately labeled **post-hoc header-tolerant parser** recovered all three actions. This is a formatting recovery, **not** a verified compiler or functional pass.
- All three model-generated lexer tables place `ELSE` before `ELSEIF`/`ELSE_IF`. A standalone regex first-match witness confirms that both `else if` and `else\nif` match `ELSE` first. The combined-token patterns also use a literal space and cannot match the newline case.
- All three generated `parse_if_statement` methods fail to build a nested `IfNode` inside the elif loop. The Python-first and Python-only candidates overwrite their original condition and body, losing branch-chain semantics. This is a structural AST witness, not a complete execution proof for the rejected graph-first candidate.

## Scientific decision

This experiment tests **order of identical source + typed syntactic-graph components**, plus a shorter Python-only efficiency baseline. The Python-only arm omits graph annotations and is not information-equivalent to the other arms. The graph is **not** a semantic/dataflow IR. This is one previously studied issue, not an adequately powered multi-repository study. There is no justified representation advantage or boundary prediction.

Next: qualify independent multi-file tasks with executable baseline-negative/reference-positive oracles, construct a true semantic/dataflow representation with information-equivalent Python baseline, and preregister a repository-cluster-aware paired sample size. Previous sensitivity calculations indicated 306 independent pairs under the larger hypothetical effect, but up to 960 issues across 240 repositories under smaller effects and clustering.

**Evidence preservation:** Full original cloud artifact is retained by GitHub Actions for 90 days; complete local reproducibility archive contains the raw requests/responses, compiler/evaluator traces, independent auditor, seven tests, findings and SHA-256 manifest. The complete archive and auditor source have not yet been mirrored to GitHub; retry mirroring without blocking science. Keep existing draft PR and hourly research automation active.
