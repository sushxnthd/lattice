# K-SYNTH-1 / Run195: format-controlled diagnostic (prospective freeze)

Frozen 2026-10-23, after observing Run194 failures. **This is a new protocol, not a blinded rerun of Run193 and not a real-repository experiment.**

## Hypothesis and controls
Qwen2.5-Coder-7B-Instruct Q4_K_M may fail because it cannot produce the requested JSON patch, not because of semantic inability. Both IR and Python SSA get identical natural-language tasks, a format-only example, edit authority, patch schema, compiler, 64-case exhaustive verifier, and decoding parameters. The only arm-specific input is the semantic graph versus Python SSA view of the same immutable policy. Strict JSON-schema constrained decoding requests exactly `{"edits":{"gate":"<Boolean expression>"}}`. The compiler is unchanged; the gate-only schema is the same for both arms. No second attempt or repair loop.

Two simple positive controls, "set gate to a and b" and "set gate to a or b", must pass **both arms** before any 16-task pilot is run. The controls are independently reference-verified; failures remain evidence. Each of two CPU shards repeats all four controls, so a shard failing controls skips its main pilot. Main pilot task IDs are policy-000 through policy-015 (8 per shard), selected and frozen before inference. The task set has four families, so no confirmatory independence or unseen-condition claim is permitted.

### Frozen identifiers
- Original synthetic task SHA256: `f54d4c05b5176f18ecf187d57c144de3ec03b56fa80e7d3077517788f5eb06f7`
- New Run195 prompt manifest SHA256: `1e87c431e73c79ecf975ace9e406a44a7ba6e3ff920300df024030a4fd4dea98`
- Run195 runner SHA256 (uncompressed): `e2cb8f93c5613c95385a4dacf5eaa5af112e2816614c7dbb2017649655710085`
- Pinned model GGUF SHA256: `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`
- Model ID: `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M`; llama.cpp tag `v0.7.0`.
- Temperature 0, seed derived deterministically from `1952317` and each task seed, max 384 tokens.
- Raw requests, model responses, usage, format verdicts, compiler and independent CPython verifier results, errors, and server logs must be retained as workflow artifacts.

## Power and inference boundaries
Run193's 258 synthetic seeds are not independent issues. An exact two-sided McNemar power sensitivity calculation (alpha 0.05, assumed discordance 0.30 and conditional IR win probability 0.65) gives **306 independent paired issue clusters** for at least 80% power, versus **72.3% power at 258**. With three tasks per issue and assumed ICC 0.1, a design-effect approximation gives 368 tasks across about 123 independent clusters, but this is NOT a validated cluster-aware power calculation. At conditional win 0.60 the independent-cluster requirement rises to 681. These are assumptions, not empirical estimates; real-repository task sampling and hierarchical simulation must precede the confirmatory study.

Run195 answers only whether constrained JSON and elementary positive controls restore measurement validity. Even a perfect 16-task result cannot prove IR superiority. If the controls fail, preserve artifacts and prioritize improving the common task interface before any full-scale comparison. If controls pass, inspect pilot failure mechanisms, then preregister independently sampled real multi-file issues and an unseen depth/coupling boundary. Never pool Run193 and Run195 results as if protocol-identical.
