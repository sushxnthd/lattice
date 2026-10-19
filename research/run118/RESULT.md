# Run118: module-qualified capture counterexample

Status: EXACT_BOUNDED_COUNTEREXAMPLE; no capable-model inference; no representation-specific breakthrough.

Two modules export identically named `helper` symbols. A third module imports the lexical alias `helper` from one or the other. Source-only unqualified references cannot identify the target without resolved import identity. In the finite test with helpers drawn from {x, not x, y, not y}, 12/16 helper pairs yield different public outputs under swapped imports. Across 256 executable Python-lowering/independent-oracle checks there were zero disagreements; seven unit tests passed. Editing an internal helper preserved protected public outputs through immutable historical captures.

System consequence: stable module-qualified IDs, import-resolution commitments, separate editable definitions and public outputs, and immutable capture authority. Indexed ordinary Python receives the identical facts and compiler. This is established namespace/versioning semantics, not novel mathematics.

Only active research kernel: K-SYNTH-1. Frozen capable-model experiment remains outstanding. Model Qwen2.5-Coder-7B-Instruct Q4_K_M, independent realistic multi-file tasks >=161 under optimistic exact McNemar assumptions, first-attempt exact repair success, graph vs indexed Python with same compiler/verifier/authority/patch grammar and token budget. The 161 synthetic correlated fixtures are not adequate product-scale evidence. Mechanism ablation and prospective depth>=5 vs <=2 prediction remain mandatory. No model inference in Run118.

Local evidence package: lattice_run118_module_identity.zip (src/lattice/module_ir.py, tests/test_module_ir.py, research/run118/experiment.py, results.json, PROTOCOL.md, SHA256_MANIFEST.json). This commit is only a result pointer if code writes are unavailable. No force-push/auto-merge.
