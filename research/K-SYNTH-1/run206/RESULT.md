# K-SYNTH-1 Run206: independent replay of Run204

Date: 2026-10-24. Existing branch `research/exp003-context-order`; draft PR #9.

## Recovered real capable-model inference

Both Run204 jobs completed and uploaded original raw model artifacts (GitHub Actions run 40011951251, artifact IDs 12530087118 and 12529523586). Qwen2.5-Coder-7B-Instruct Q4_K_M was pinned to SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. Temperature 0, max completion 1536 tokens.

An independent local script reconstructed all 16 prompts from the original requests, rechecked source and prompt hashes, seeds, model IDs, usage and raw responses, and replayed all 16 verifier outcomes with zero disagreements.

| Measure | Observed |
| --- | ---: |
| Positive controls accepted | 8/8 |
| Real issues | 2 |
| Real completions | 8 |
| Compiler accepted | **1/8** |
| Structural-ID accepted | 1/4 |
| Text-anchor accepted | 0/4 |
| Real failures | 4 no-op, 2 truncated JSON, 1 unknown/ambiguous address |
| Functional resolution | **NOT EVALUATED** |

## Important newly discovered false positive

The only compiler-accepted real completion (Nox issue `wntrblm__nox-933`, source-first/structural-ID) changed the bytes of three files but changed **no Python AST** under `ast.parse(..., type_comments=True)` in any file. It stripped the existing copyright/Apache license headers from all three files and added only commented-out code. Syntactic acceptance was not a meaningful code repair. AST equality does not prove full behavioral equivalence in the presence of source introspection or line-number-sensitive behavior.

A separately executed, **post-hoc** common safety gate rejects license-header removal and can optionally require an AST delta for code-changing tasks. This is diagnostic only; it must not retroactively redefine the frozen original endpoint. The local Run206 archive contains the independent replay script, per-completion audit JSON, post-hoc gate source, 15 passing tests, and both original inference artifact ZIPs.

## Interpretation and next gate

Run204 compared structural addresses with exact-text anchors and context order, **not full semantic IR vs ordinary Python**. Two issues and four correlated arms per issue do not support a representation superiority claim. Run205 also established that a three-Python-file edit restriction excludes reproduction of many reference patches; do not condition the primary cohort on gold metadata.

Next freeze and execute a powered genuine semantic-IR vs ordinary Python vs Python-with-matched-short-IDs comparison, using identical repository-wide edit authority (including non-Python files), model budget, compiler, verifier and independent functional issue evaluation. Earlier cluster-power sensitivity suggested ~468 discovery issues across ~187 repositories for 80% power under the large-effect assumption; this is not yet a finalized sample. The 89 held-out boundary issues remain unused for model inference.

**Conclusion:** 1/8 syntactic acceptance, 0/8 demonstrated AST-changing repairs, and 0 functional resolutions measured. Representation superiority unproven.

Original artifacts: https://github.com/sushxnthd/lattice/actions/runs/40011951251
