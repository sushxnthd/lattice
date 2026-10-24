# K-SYNTH-1 Run229: actual Qwen2.5-Coder-7B inference audit

Independent audit of GitHub Actions run 40126724353, artifact 12573013765 (artifact SHA-256 3e4a7208bd50741f01d9739f2629a3248d0ed4bd6c97e857d38e64a8f0a18c45). The run completed successfully and generated TWO genuine completions. Raw requests, responses, model provenance, and usage were retrieved and SHA-256 verified.

## Frozen primary endpoint

| Arm | Prompt tokens | Completion tokens | Compiler accepted | 16-case functional score | Complete repair |
| --- | ---: | ---: | --- | ---: | --- |
| Semantic-IR JSON | 942 | 800 | No | 0/16 | No |
| Annotated Python | 888 | 492 | No | 0/16 | No |

Both arms incorrectly wrote the target ID to `replacement` and proposed code to `content`, despite explicit instructions to put a complete replacement method in `replacement` and leave `content` empty. The common compiler rejected both: `Rejected: nonempty unused or missing replace field`. Primary paired outcome is 0/1 complete repair for each arm; one issue provides no useful superiority estimate.

Pinned model: Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M, SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. Seed `1560714227`, temperature 0, max output 4096 tokens. Both finish reasons: stop. All six independent audit regression tests passed.

## Post-hoc diagnostic only (NOT valid experimental successes)

- Swapping the two wrongly filled fields makes the semantic-IR output compile but passes **7/16** cases. The code constructs a plot before the solved check, and fails to reject empty/partially solved BatchStudy collections.
- Swapping the Python fields alone fails because its generated code is a method body, not the complete method. Reconstructing the header and docstring from the frozen fixture makes it compile and pass **8/16** cases. The BatchStudy guard still accepts empty and partially solved collections.
- These two salvage interventions are *different*, unregistered, and cannot be compared as evidence that Python beats IR. Neither repair resolves the issue.

## Mechanism and decision

A shared action-schema failure is a plausible interface bottleneck, not a representation result. Prospectively test a five-field, replace-only grammar with no unused `content` field and otherwise matched model, source information, compiler, authority, and 16-case evaluator. Do not reclassify the Run228 outputs. This remains a single two-file, method-only feasibility study; a powered, multi-repository functional comparison and distinct semantic-operation baseline are still missing.

Full local reproducibility bundle: `lattice_run229_actual_qwen_independent_audit.zip` (raw Qwen completions, exact requests, inference records, 16-case evaluator, independent audit script, 6 passing tests, traces, SHA-256 manifest). The full archive is preserved as a conversation artifact; GitHub stores this compact report until artifact upload is available.
