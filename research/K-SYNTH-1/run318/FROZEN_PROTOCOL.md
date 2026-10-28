# K-SYNTH-1 Run318 prospective production structural-expressibility protocol

Frozen 2026-10-28 UTC before running the production-source structural compiler on pinned urllib3 PR #5071. This is **gold-only reference-patch expressibility calibration**. No model receives reference-derived locations or code. It is not a new repair qualification, model inference or representation-superiority test.

Executable SHA-256: `a24d444271fea99c3cf360ef3002b6c824d944ca245e5fe58584ff9923081884` (`run318_real_structural_expressibility.py`). Original shared compiler is unchanged Run316 source SHA-256 `005fb330be56bc94ba4e7c8c400a609092e6aa9452a2089e8218f13b7601331f`. No reference patch or baseline code will be executed, only parsed and compiled.

Repository: `urllib3/urllib3`, historical base `f4e4bc31f40f8c94c6a1f1685df28f97ff48c305`, historical head `8b6b36f57e139755356074908abbcb0b07732d6d`. Three production files: `src/urllib3/connectionpool.py` (2 If.test expression replacements), `src/urllib3/poolmanager.py` (2), and `src/urllib3/util/url.py` (1). Source and reference Git blob SHA-1 IDs are pinned in the executable. Every AST If.test target must be unique and verified by exact source SHA-256 and AST-node SHA-256. All five actions must compile atomically through the **unchanged** shared Run316 structural compiler. Primary pass requires all three output files to match the exact historical reference bytes and Git blob hashes. A single mismatch is a failure. Do not change criteria or widen authority post hoc.

Execution: isolated no-cost GitHub Actions checkout, fetch pinned public upstream Git objects, Python 3.13, save original raw JSON results and logs as artifacts; no untrusted model code executed. Source, workflow and logs must be independently verified. Failure due to unavailable upstream Git objects or infrastructure is not a compiler failure; record and retry without changing science.

All 89 reserved issues remain sealed. Six historical qualified repairs remain six. PR #9 stays open/draft/unmerged on `research/exp003-context-order`. Adequately powered paired capable-model functional evidence remains outstanding.
