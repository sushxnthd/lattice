# K-SYNTH-1 Run258 — source-exact compiler positive control and verified import edge

Executed a separate **source-exact format-control** diagnostic on the previously qualified real two-production-file Flask PR6096. This is **not** a new independent issue and **not** a semantic-IR versus ordinary-Python result.

## Scientific findings

- Replaced dedented AST method presentation with original-line source windows preserving indentation and added source-exact import context. The earlier AST extractor stripped declaration indentation, but this alone does not prove literal-match failure; the actual previous model patch had zero exact matches.
- Verified one narrow cross-file binding by AST: `Flask.test_client` in `src/flask/app.py` imports `FlaskClient` from `src/flask/testing.py`, where the target class exists. A target-class mutation fails closed. Dynamic `test_client_class` overrides mean **no definite runtime invocation is claimed**.
- Constructed five real reference-patch transactions across the two source files. The **unchanged strict compiler accepted all five** and reconstructed both upstream reference files byte-for-byte. This is an executable compiler positive control, **not a model-generated repair or functional-oracle result**.
- **10/10 local regression tests passed**, including a stubbed inference-runner integration test. Stubbed responses are not model evidence.
- Frozen two prospectively distinct source-exact prompts, JSON facts **3,954 UTF-8 bytes**, Python-comment facts **3,967 bytes**; identical source, facts, public task, edit scope, two format examples and planned oracles. Intended pinned Qwen2.5-Coder-7B-Instruct Q4_K_M SHA256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, seed 258001, temperature 0, max output 2048. **No actual new model inference, token counts, or functional model results yet.** This remains a fact-encoding contrast only.

## Independent candidate screening

- `pallets/werkzeug` PR3308 (merge `830d4b3957e9532be5f510e499dd797964d064d6`) changes eight production files but is a broad API refactor. **Candidate only; no executable qualification.**
- `pallets/werkzeug` PR3238 (merge `3474ff43371fdb7d9c129d9a13021fda38812f2d`) changes two production files, but the matcher edit appears to change exception chaining rather than the targeted 404-versus-500 behavior. **Not counted as a proven two-source repair task** without ablation.

## Evidence and next gate

Full **22-entry SHA-256-verified local archive** `lattice_run258_source_exact_binding_positive_control.zip` SHA256 `08b4041f45eaeeb1f5704fcdf29570b34ece55798bfabee842c760478699ba1e`. It includes source code, tests, frozen request files and hashes, exact pinned Flask baseline/reference snapshots, original prior cloud artifact, and candidate screening. Complete code mirroring remains outstanding if connector writes block.

Next: execute the frozen Qwen diagnostic without changing its requests, independently audit raw completions/strict compiler/functional oracle; qualify additional genuine multi-source public issues; implement a verified cross-file semantic/dataflow IR and information-equivalent ordinary Python comparator. Preserve prior negative outcomes and all 89 sealed boundary issues. No representation superiority or significance claimed.
