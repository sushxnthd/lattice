# Run239 — prospective real multi-file functional qualification

**2026-10-25. Status at freeze: NO model inference.** Run234's 12-repository pilot produced no accepted multi-file transactions and no complete issue-level functional endpoint. Run239 therefore qualifies a fresh **discovery** task before another model comparison. The reserved 89 boundary issues remain sealed.

## Frozen task and provenance

- Instance `crossgl__crosstl-41`, repository `CrossGL/crosstl`, immutable base commit `d456c2b5f509104dd97b74ce40c597531784e2ca` from the existing Run199 480-issue discovery pool. Not among Run234's 12 pilot tasks.
- Issue: implement `else if` support in the DirectX lexer, parser, and CrossGL generator. It explicitly identifies three files and is therefore a realistic cross-component multi-file target.
- Authorized reference files: `crosstl/src/backend/DirectX/DirectxLexer.py`, `DirectxParser.py`, and `DirectxCrossGLCodeGen.py`. The AST classes and package initializer are read-only in the positive control.
- Five frozen evaluator cases: multi-branch else-if chain, newline-separated else-if, plain if/else, explicitly nested `else { if ... }`, and if-only. Checks lexer tokens, parsed AST structure, branch execution via an independent restricted interpreter, and emitted CrossGL syntax. Executes pinned upstream modules without third-party packages.
- Independently authored reference control adds a lexer token, recursive parser tail with `is_elif` marker, and marker-aware generator emission. It changes **three files**. Three seeded defective controls each omit one component edit. These are not model completions or upstream gold patches.
- Qualification requires both issue-specific baseline checks to fail, all five reference checks to pass, at least two defective controls to fail issue checks, and at least two distinct reference-edited files. Failure is retained as a negative artifact; no post-hoc oracle edits without a separately named revision.

## Execution and evidence

`qualify_crossgl.py` is stored as a zlib+base64 reproducibility payload, decoded source SHA-256 `232aaedbc91e279e77de2da68f7a303305054d5e8823329d1a569b7b523f5795`, with plain-text source in the downloadable local archive. Workflow checks out the exact upstream commit, verifies evaluator hash, executes baseline, reference and defect controls, and uploads per-case traces even if qualification fails. **No model calls occur.** Local structural tests are not pinned-upstream execution.

## Interpretation and next gate

Passing establishes one executable multi-file calibration task, **not** model advantage, full HLSL execution, or adequate power. Next: freeze diversified tasks with independent functional oracles, matched ordinary-Python and semantic-IR edit authority, identical compiler/verifier, prospective prompt hashes, and cluster-aware paired sample size. Include an AST-action baseline for claims beyond source-presentation effects. Do not unseal reserved boundary tasks without a frozen mechanism prediction.
