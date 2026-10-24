# Run216: independent Run215 model audit and prospective transport correction

Date: 2026-10-24. K-SYNTH-1. Run215 inference jobs completed successfully (GitHub Actions run 40071460612; artifact IDs 12551752162 and 12551890752). Six Qwen2.5-Coder-7B-Instruct completions and all exact requests, prompts, seeds, model IDs, token counts and verifier traces were recovered.

| Arm | Strict compiler acceptance | Strict independent Docker functional success | Completion tokens |
| --- | ---: | ---: | ---: |
| Semantic rename operation | 2/2 | 1/2 | 57 |
| Python exact-line | 0/2 | 0/2 | 565 |
| Python short-ID | 0/2 | 0/2 | 1008 |

The accepted semantic task-0 repair chose an incorrect new name; task 1 passed. Python outputs exhibited raw control characters inside doubly encoded JSON strings. Post-hoc lenient decoding recovered one compiler-accepted Python exact-line edit, but it omitted a required reference. This is a retrospective diagnostic, NOT a rescore of frozen primary results.

The two synthetic four-module fixtures are not independent real-repository tasks. The semantic arm has a high-level rename primitive while Python arms must enumerate line edits; authority and action granularity differ. The exact paired McNemar p-value is 1.0. **No representation superiority is established.**

Run216 prospectively introduces identical direct JSON schema for all conditions, including a fourth ordinary-Python semantic-tool control with identical rename authority. All conditions retain common source facts, pinned Qwen 7B, frozen seeds, transactional compiler and networkless Docker functional evaluator. The pilot is a transport and action-granularity diagnostic, not a powered real-repository comparison.

The previous conditional cluster-adjusted planning target remains approximately 686 paired realistic issues, assuming the previously specified effect and intrarepository correlation. No result from two synthetic fixtures can validate those assumptions. A genuinely distinct semantic IR versus Python representation, with identical action authority and independent functional evaluation, remains the decisive missing study.

Full source, independently decoded raw inference, audit code, JSON records, prospective runner/tests, freeze manifests and SHA-256 manifest are preserved in the Run216 local reproducibility archive.
