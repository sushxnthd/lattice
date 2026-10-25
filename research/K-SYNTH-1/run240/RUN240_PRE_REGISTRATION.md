# Run240 prospective protocol — qualified CrossGL three-file model comparison

Frozen on 2026-10-25, before new inference. **No result is known at freeze.**

Task: CrossGL/crosstl issue #41 at commit `d456c2b5f509104dd97b74ce40c597531784e2ca`. Run239 independently qualified the issue (baseline 3/5, reference 5/5, three one-component defect controls 3/5). The calibration reference is never included in model prompts. The 89 reserved boundary issues remain sealed.

Conditions: `semantic_ir_json` versus `ordinary_python_source`, using the same seven exact source blocks (three editable: lexer TOKENS, parser parse_if_statement, generator generate_if_statement; four read-only: parser parse_block/parse_statement, generator generate_function_body, AST IfNode). Both views are lossless renderings of the same source bytes, selectors, hashes, target information and edit authority. The IR uses structured JSON; the Python condition shows ordinary source with selector comments.

Both arms use the identical action schema, transactional replacement compiler, symbol/decorator/signature preservation, Git patch validator and frozen five-case Run239 functional oracle. Primary endpoint: all five checks pass. Secondary: checks passed, compiler acceptance, failure type, number of files edited, token counts. One paired issue cannot establish superiority.

Model: Qwen2.5-Coder-7B-Instruct Q4_K_M, GGUF SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; llama.cpp v0.7.0 commit `620d2225cc436ab0b001e3200e590e3b286ef9ab`; seed 24041, temperature 0, 3072 completion tokens, context 16384. The deterministic pre-inference stage freezes full requests and their hashes; the cloud run retains raw responses, usage, patches, independent oracle traces and failures.

Power analysis under *hypothetical* 30% discordance and 65% conditional IR wins: 258 independent pairs give 72.3023% exact two-sided McNemar power; 306 give 80.0367%. Under 60% conditional IR wins, 681 independent pairs are needed for 80%. Clustering by repository increases requirements. No claimed empirical effect.

Decision: if both arms fail, prioritize reasoning/context and verified transactional editing, not syntax cosmetics. A representation advantage requires an adequately powered, multi-repository, prospectively frozen functional comparison, followed by mechanism ablation and unseen-boundary validation.
