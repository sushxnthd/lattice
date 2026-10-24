# K-SYNTH-1 Run209 — independent Run208 audit and single-selector pilot

Date: 2026-10-24. Active branch: `research/exp003-context-order`. Draft PR: #9.

## Independently recovered capable-model evidence

Run208 GitHub Actions run 40038183894 completed successfully and uploaded job artifacts 12537984137 and 12538715155. All six Qwen2.5-Coder-7B-Instruct Q4_K_M positive-control completions were independently replayed against the frozen common compiler.

| Arm | Job 0 | Job 1 | Post-hoc one-selector replay |
| --- | --- | --- | --- |
| semantic_node_ir | rejected | rejected | correct edit both |
| python_text | rejected | rejected | correct edit both |
| python_short_id | rejected | rejected | invalid syntax both |

**0/6 prospective controls accepted; 0 real-repository completions.** All six raw actions incorrectly populated BOTH `old_text` and `target_id`, violating Run208's required empty unused field. A *post-hoc diagnostic only* removed the redundant address and renamed the chosen address `selector`: 4/6 then correctly compiled; the two Python-short-ID outputs targeted an entire function with an indented return-statement replacement, triggering `unexpected indent`. This establishes two distinct failure modes: redundant-output-field contamination and target-scope confusion. Post-hoc results are not confirmatory evidence. Both jobs produced the same outputs under different seeds. Exact requests, model IDs, tokens, seeds, responses and traces are retained in the original GitHub artifacts and the local reproducibility archive.

## Prospective Run209 correction

The new six-string-field schema is identical for all three conditions: `op,path,file_sha256,selector,replacement,content`. The arm-specific selector is resolved into the SAME trusted compiler. The prompt explicitly distinguishes replacing a full function versus one return statement. The same model checksum, common source/target facts, repository-wide authority, shared retrieval, verifier and previously frozen two discovery issues remain in force. The 89 held-out boundary issues remain unused.

Unlike Run208, Run209 will collect **exploratory** real-task outputs even if controls fail; those outputs must not enter a confirmatory comparison. The patched source and workflow were committed to this branch. Local verification: **29 unit tests passed**; patch replay reproduced the intended runner byte-for-byte. Run209 patch SHA-256: `5c48a26ad2070aea7958f85641242962580863d7e719b0c10f9eb9a06cb91338`.

## Identification and limitations

The semantic-node-IR and Python-short-ID arms share the same target IDs, target facts, output schema and compiler. Their operational difference is prompt wording, **not an actual semantic-IR representation**. Any difference between them measures instruction framing rather than intrinsic representation quality.

No functional issue resolution or adequately powered model comparison is established. Previous planning estimated ~73.4% power for 391 discovery issues / 157 repositories under a hypothetical large effect, versus ~80% for approximately 468 discovery issues / 187 repositories; recalculate using actual paired functional discordance and repository correlation. A true semantic IR, independent functional evaluator, mechanism ablations, adversarial tasks, and unseen-boundary prediction remain necessary.

## Reproduce

Source: `research/K-SYNTH-1/run207` restored with the frozen Run208 and Run209 patches. Run209 workflow: `.github/workflows/lattice-k-synth-1-run209-single-selector-pilot.yml`. Original model data: GitHub Actions run 40038183894, artifacts 12537984137 and 12538715155. Independent audit, exact raw outputs, tests, checksum manifest and full local runner are in the Run209 reproducibility archive.
