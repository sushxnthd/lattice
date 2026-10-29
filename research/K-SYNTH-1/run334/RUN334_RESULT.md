# K-SYNTH-1 Run334: original Run333 recovery and truncation mechanism

## Original evidence, independently audited

Recovered [GitHub Actions Run333](https://github.com/sushxnthd/lattice/actions/runs/40822825928), original artifact 12876087310, ZIP SHA-256 `b5a03afa3f020d0f1fbed023b6180fbfede43d606a3add0fb5fc4dd7cec25d0b`. Workflow completed successfully. A read-only independent audit verified all **39/39** manifest entries, the pinned historical HTTPX base `891d865044d27c229278f0fa20d84ba4007cb289`, both production-source SHA-256 values, the frozen Qwen2.5-Coder-7B Q4_K_M model SHA `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, all **31** information-matched candidate rows and **18** original oracle case records. Ten adversarial mutations, with their manifest hashes recalculated, were independently detected. Original completions were never corrected or rescored.

Both original two-action gates passed (2/2 edits each). On the real HTTPX issue, **IR reached the 768-token limit and emitted unterminated JSON**; the original compiler rejected it and no IR oracle ran. **Python/AST generated one valid, accepted `_api.py:head` default edit** (46 tokens); the isolated oracle improved from **0/3 targets + 6/6 controls** to **1/3 targets + 6/6 controls**, or 7/9. **Full repair success was 0/1 in both arms.**

## New descriptive mechanism finding

The original IR text contains **25 complete unique authorized edit objects** and an incomplete 26th. The 25 complete objects copy candidate IDs in exact consecutive order, positions **1–25** of 0–30, all with `new_expr=True`. **22/25 are no-op True-to-True edits**, while three are actual False-to-True changes, covering the three frozen HEAD defaults. This is a candidate-enumeration/output-budget failure in the observed text, **not** a successful IR repair: the partial output must never be auto-closed, compiled or scored as valid.

Both presentations contain the same issue facts, candidate IDs, old defaults and MAY_FORWARD facts. Their different surface labels and AST-slot syntax do not isolate an information advantage of semantic IR. The synthetic gate also did not predict real repair success. Run333 itself was an exploratory post-Run332 gate reformulation; these results are not a powered comparison or a breakthrough.

## Next prospective exploratory experiment

Run335 applies an **identical, pre-inference minimal-delta instruction suffix** to both real model prompts: do not output no-op edits, do not enumerate authorized candidates, use at most four edits and return complete JSON. The generic bound four is not an exact reference edit count. The frozen original issue, 31 source-derived candidates, edit authority, model, positive-control gate, shared compiler and isolated oracle remain unchanged. New completions and functional traces must be preserved independently; Run333 outcomes stay immutable. A local independent freeze/audit of the two transformed requests passed. **No Run335 model success is claimed yet.**

Three independently qualified historical production issues remain (Flask PR6096, urllib3 PR5071, HTTPX PR1183). All 89 reserved issues remain sealed. Maintain the single K-SYNTH-1 kernel, branch `research/exp003-context-order`, and open/draft/unmerged PR #9.
