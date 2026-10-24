# K-SYNTH-1 Run218 — Target-recall confound isolated

## Frozen Run217 results (independent replay, 2026-10-24)

Both Qwen2.5-Coder-7B-Instruct Q4_K_M real-repository pilot issues completed. Each had two information-equivalent representation conditions and one shared gold-blind file retrieval decision. The frozen compiler-acceptance scores were **semantic-node JSON 0/2 and annotated Python 0/2**. Functional issue resolution was NOT EVALUATED. Exact prompts, raw outputs, model IDs, token usage, seeds, retrieval decisions and compiler failures are in the original GitHub Actions artifacts: https://github.com/sushxnthd/lattice/actions/runs/40077591843

* `googlefonts__ufo2ft-930`: both arms were rejected as unknown/ambiguous targets. The named `_featuresCompatible` function was missing from the five disclosed target records in its source file. At the pinned source commit, the function spans approximately **1,169 characters**, exceeding the 480-character preimage cap; the target selector therefore omitted it even though it was named in the issue. The semantic output hallucinated a replacement preimage; Python emitted the literal placeholder `old_text`.
* `spikeinterface__spikeinterface-2775`: Python emitted the literal instruction `exact old_text from a listed target` as its selector and was rejected. Semantic JSON hit the 2,048-token completion limit, producing truncated JSON. At the pinned source commit, the requested `split` method spans approximately **865 characters**, also exceeding the 480-character cap and absent from the displayed target records.

The four responses do not support an IR superiority, inferiority or equivalence claim. The study failed a **target-availability and action-addressing prerequisite**. Original scores remain unchanged; no post-hoc rescoring is included.

## Prospective Run218 correction

A new two-issue pilot, frozen before inference, holds model, seeds within issue, task text, retrieved files, full editing authority, JSON action grammar and transactional compiler constant. Both representations now expose the **same 24-character target IDs** and full preimages. Named functions explicitly mentioned in the issue receive priority and may exceed the previous 480-character limit (up to 5,500 characters). Information-equivalence of JSON and annotated-Python facts is checked before inference. The frozen shared facts have a 26,000-character budget.

Five preflight tests were implemented for long named-function recall, lossless cross-view facts, shared short-ID compilation, fallback behavior and identical output schema. No new model outcomes are claimed until raw cloud artifacts are retrieved and independently audited.

This remains a **presentation-format feasibility pilot**, not a genuine semantic-operation versus ordinary-Python action-space comparison. It has only two issues, no independent functional SWE-rebench evaluator, no mechanism ablation and no unseen-boundary test. The earlier approximate 686-pair planning figure depends on assumed effect and repository clustering; it is not an observed power result.

## Next decisive decision

First establish that a capable open model can address a relevant source target and produce valid edits in both arms. Then add independent functional issue tests and an equal-authority semantic-operation/Python-tool comparison. Preserve negative results and pivot the thesis if matched Python wins or ties in repeated controlled reformulations.
