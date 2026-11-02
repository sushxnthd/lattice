# K-SYNTH-1 Run444 — completed paired Qwen IR-vs-AST pilot and bounded negative result

**Date:** 2026-11-02 UTC. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, one open/draft/unmerged PR #9. All 89 reserved boundary issues sealed.

## Completed genuine model inference

[Actions Run444 #41510207507](https://github.com/sushxnthd/lattice/actions/runs/41510207507) finished **SUCCESS** at 19:38:23 UTC. Original artifact **13173530788**, ZIP SHA256 `b58bc45da9e499f2edfeb68189dc7824871c76b62f94661bd44d689b545d18f2`. All **30/30** original artifact members independently verified by SHA and size; independent audit passed **82 checks**, including exact six prospectively frozen prompt hashes, original source facts, raw requests/responses/completions, model SHA `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, llama.cpp engine commit `620d2225cc436ab0b001e3200e590e3b286ef9ab`, seeds and upstream checkouts.

**6/6 genuine Qwen completions** with finish_reason=stop; **6/6** JSON action schemas accepted under the *prospectively frozen* shared plain-or-fenced JSON parser. All six raw completions used Markdown fences. This does **not** retroactively revise Run442's strict-parser failures.

| Task | Semantic IR | Python/AST | Actual verified real repair |
|---|---|---|---|
| Flask PR6096 | AST-parse accepted | AST-parse accepted | **No**. Byte-identical `rpartition` edits regress no-port hosts |
| urllib3 PR5071 | Missing/nonunique preimage | Missing/nonunique preimage | **No**. Neither edit transaction accepted |
| Synthetic two-file control | Exact expected AST | Exact expected AST | **2/2 synthetic control passes only** |

Flask and synthetic control completions were byte-identical between arms; urllib3 completions differed. The urllib3 IR completion copied line-number prefixes (`313:`, `433:`) into old/new source strings, causing nonexistent preimages. The Python/AST completion targeted `if port is not None:` in `util/url.py`, which appears **twice** in the frozen excerpt, violating unique-preimage authority. These are mechanism diagnostics, not causal superiority evidence.

**Chat prompt tokens (IR/AST):** Flask 606/565, urllib3 1359/1259, synthetic control 363/301. The raw tokenize endpoint counted 29 fewer tokens per prompt than chat usage. Unequal token budgets and known-bug-mechanism localization remain confounds.

## Independent functional and formal-scoping evidence

The locally implemented graph IR and conventional Python AST action representation independently decode to identical task facts, source snippets, edit authority and source hashes. Cross-file dataflow is explicitly **UNKNOWN**, not proven. **23/23 tests** passed (15 local compiler/representation plus 8 model-artifact tests); **1,700 independent checks** passed (1,618 local plus 82 original model artifact checks). **1,536 actual CPython calls**: 1,024 trusted synthetic two-file control calls plus 512 isolated subprocess calls.

[Executable counterexample](https://github.com/sushxnthd/lattice/blob/research/exp003-context-order/research/K-SYNTH-1/run444/run444_minimal_unknown_edge_witness.py): identical published excerpts for `a.py` and `b.py` conceal an import binding to `b` versus `c`. Editing `b.py` changes `a.f` by exactly +10 in one world and 0 in the other, across 128 inputs and four child-process conditions. Thus excerpt-only source cannot certify the cross-file dependency; this does **not** refute whole-program analysis.

## Reproducibility and limitations

Complete SHA-verified **21-entry archive** `lattice_run444_completed_qwen_dual_view_and_dataflow_counterexample.zip`, SHA256 **`c112a2f1c9524224ba9236144701ad7139c1aa2035670f2225f47ba2abb1e7f9`**, contains 20 verified payloads, both original model ZIPs, six raw Qwen completions, frozen prompts, independent auditors, 1,536 functional traces, source code, tests, exact SHA manifest and clean-extraction replay. Full historical GitHub ZIP mirroring remains incomplete.

**Scientific status:** Independently qualified real multi-source repair count remains **two**. No new verified real repair, no powered McNemar significance, no IR superiority and no breakthrough. AST-parse acceptance is not a functional repair oracle. Next: independent isolated historical PR-parent public/heldout oracles, genuinely blind issue-first new repair qualification, and prospectively controlled token/line-number reformulations.
