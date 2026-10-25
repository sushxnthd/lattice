# K-SYNTH-1 Run249 — failed-inference recovery and independent frozen-request audit

Date: 2026-10-25. Research branch: `research/exp003-context-order`. Draft PR: #9.

## Observed cloud failure (not a model result)

GitHub Actions [Run248](https://github.com/sushxnthd/lattice/actions/runs/40204335375) finished **failure** before inference. The preflight failed with `ModuleNotFoundError: No module named 'typed_representation'`, but `continue-on-error: true` hid it. The workflow built llama.cpp and downloaded a SHA-verified 4.5-GB model, then failed trying to tokenize the missing `graph_first-request.json`. Artifact ID `12603157275` contains failure evidence, not completions. **Zero new model outputs** were observed.

## Repairs committed without modifying frozen requests

- Restored the two missing typed graph dependencies as SHA-pinned compressed sources: `typed_representation.py` (SHA-256 `933fd881df72a527e24e807cb9dc6221ef602bfc02499cfdcd8a694f03656435`) and `typed_representation_v2.py` (SHA-256 `5358242052f2dee3e6f4d2b3163642c8389a49835a55846492d4f3f764d1861d`).
- Updated the workflow to verify those dependencies and **fail fast** if preflight does not complete.
- Corrected a second blocker: the workflow had a truncated 61-character graph-first SHA. The correct original preregistered digest is `2a0dedd8d06bb9edb61f3641ad39eb149a838cecfaa6f469717524e8398490e2`. The actual frozen prompt and model settings were unchanged.

Recovery commits: `8697e523`, `803f372f`, `94d3c9e0`, `f6b117bb`. These changes trigger the existing workflow on branch push. No completed rerun has yet been independently audited.

## New independent construct-validity result

Rebuilt all three requests from frozen seven-block CrossGL facts and checked exact byte equality against the original frozen requests and Run247 manifest. All three hashes matched. **27 local tests passed**, including an intentionally corrupted-request rejection test and compiler tests.

| Arm | Request bytes | Prompt bytes |
|---|---:|---:|
| Graph first | 27,320 | 23,960 |
| Python first | 27,320 | 23,960 |
| Python only | 8,406 | 7,615 |

The graph component is **16,345 bytes** against **5,922 source-component bytes**, a **2.760× byte overhead**, not a model-token count. The verified projection contains 107 AST nodes, 33 syntactic call candidates and 47 syntactic bindings across seven blocks (three editable, four read-only).

Graph-first and Python-first are exactly the same two components in reverse order. The source-only arm intentionally omits redundant structural annotations. Consequently this pilot tests **presentation ordering and annotation overhead**, not the benefit of a genuine semantic/dataflow IR. No performance claim follows from these deterministic checks.

## Outstanding decisive experiment

Recover and independently evaluate actual Qwen2.5-Coder-7B-Instruct completions from the repaired workflow; then qualify multiple real repositories, freeze a matched native-Python vs genuinely semantic-IR comparison, and power for repository clustering. The earlier 306-independent-pair planning number is not sufficient automatically under clustering. Preserve all failures and negative results.

Complete local Run249 archive contains source, exact frozen requests, failure record, independent audit, 27 passing tests and SHA-256 manifest. The archive has not been uploaded to GitHub.
