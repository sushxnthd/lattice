# K-SYNTH-1 Run355 prospective model freeze

Committed before any Run355 model inference. This is a previously qualified real HTTPcore issue, not a new independently qualified task or powered sample.

- Historical task: encode/httpcore PR #882, based on original issue #872 (2024-01-24), https://github.com/encode/httpcore/issues/872. The model receives the issue summary and two original source files, no reference diff or oracle cases. Manual source-file selection based on the issue topic is a retrieval limitation.
- Base commit c46802478cdd8a82ee8cb333420080fab1aed00b. Pinned blobs: httpcore/_sync/http11.py e108f88b124043b05258f6d98363119b79f92d88; httpcore/_async/http11.py a5eb480840dd4eae73bc8285c9d374a09a0bd44c.
- Two representations of exactly the same verified AST declaration/call fact ledger: SEMANTIC_IR JSON and PYTHON_AST_FACTS Python literal. Runtime targets explicitly UNKNOWN. This is syntactic/lexical information, not a certified runtime-MUST dataflow graph, and cannot establish a substantive semantic-IR advantage.
- Both receive identical original source, issue facts, edit authority, atomic compiler, oracle, seed and output budget. Token lengths are measured, not silently padded. Qwen2.5-Coder-7B-Instruct Q4_K_M SHA256 509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c; llama.cpp v0.7.0 commit 620d2225cc436ab0b001e3200e590e3b286ef9ab; seed 3552026, temperature 0, max 2300 completion tokens, context 16384.
- Shared compiler: 1–6 exact unique nonoverlapping replacements, max 3 per authorized file, reject no-ops, syntax errors, unauthorized files, ambiguous preimages; atomic staging. Reference-gold expressibility is not yet proven and must be independently checked.
- Isolated immutable Run340 public API oracle: four target cases (sync/async CONNECT and Upgrade with buffered trailing data), six controls. Baseline target 0/4, control 6/6. Success requires 4/4 target and 6/6 control. Docker no network, read-only filesystem, nonroot, cap drop, bounded resources.
- Preserve frozen requests, exact raw model responses, prompt/response tokens, source hashes, compiler receipts, all functional traces and failures, SHA manifest. No positive-control gate in this exploratory pilot. Output-schema failures do not prove semantic inferiority.
- Do not touch the 89 reserved issues. Sole open/draft/unmerged PR #9. Historical eight qualified tasks remain unchanged. No model success or superiority is claimed until original artifacts are independently recovered.

Runner source is the SHA-pinned zlib/base64 file in this directory, decompressed by the workflow to SHA256 676dd0792964aea7e7a0f5cb8cc8947e60c003bfe007cf7149f66b7d458d828e. Local original source, tests, and evidence archive are separately SHA-verified.
