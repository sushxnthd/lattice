# K-SYNTH-1 Run330 prospective frozen protocol (2026-10-29 UTC)

Canonical sushxnthd/lattice, branch research/exp003-context-order, one OPEN/DRAFT/UNMERGED PR #9. All 89 reserved boundary issues SEALED.

## Real issue and pinned source
Only HTTPX issue https://github.com/encode/httpx/issues/1146, filed 2020-08-07, with its original pre-fix wording and normalized line endings. Baseline 891d865044d27c229278f0fa20d84ba4007cb289; _api.py blob a300f633e7ace1d0876a39735bf9af0c7ac64336; _client.py blob e3b2f5b31913f210491a6c5fc2bff1c454833440. Frozen independent Run328 nine-case oracle SHA256 51cefba11ede1692bf543500f410fcf3406f95705f6b5876af886893574394f7. Baseline must reproduce 0/3 targets and 6/6 controls; model success requires 9/9. No reference source or diff accessible to model runner.

## Predeclared discovery and arms
Scan ALL baseline httpx/**/*.py functions with a defaulted allow_redirects parameter whose AST default is a boolean literal. Assign SHA-derived IDs from baseline path and qualified function name. No reference-derived changed-line localization. Identical eligible targets, issue facts, source hashes, action IDs, edit authority, strict JSON output schema, model and seed in both arms. Arm IR renders source-derived IR_DEFAULT and syntactic MAY_FORWARD with UNKNOWN callee/runtime effects. Arm PYTHON_AST renders ordinary ast.FunctionDef.args.defaults and ast.Call.keywords with the SAME underlying facts and UNKNOWN. Different prompt lengths and syntax are confounds. This is NOT a certified semantic/dataflow IR.

## Model, positive-control gate, compiler and isolated oracle
Qwen2.5-Coder-7B-Instruct Q4_K_M SHA256 509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c; llama.cpp v0.7.0 commit 620d2225cc436ab0b001e3200e590e3b286ef9ab; seed 3302026, temperature 0, 512 output tokens, identical json_schema-constrained decoding. Freeze exact four requests/hashes before inference. First, each arm must produce an accepted model edit changing def probe(flag: bool=False) to default True. If either gate fails or precompletion errors occur, SKIP both real requests. Otherwise run one genuine completion per arm on HTTPX. Never posthoc salvage malformed JSON as frozen success.

Same Run329 postfreeze boolean-literal guard and atomic SHA-preconditioned AST-congruent compiler for both arms. Reject non-literal defaults, stale source, unknown IDs, malformed schema and empty edits. Untrusted model code is never imported or executed on host. Oracle runs in networkless read-only, no-new-privileges, capability-dropped, PID/CPU/memory-limited Docker. Preserve raw requests, completions, usage, model/engine SHA, compiler traces, oracle outcomes, failures and SHA256 manifest.

## Claim boundary
This is one previously qualified production issue, not a new independent repair, not a powered superiority test, and not general semantic soundness. Do not promote failed Werkzeug PR2535/PR2860 or urllib3 PR2482. Keep all 89 sealed. Future study requires independently qualified multi-repo issues, soundness-scoped IR, strong equivalent Python/AST baseline, cluster-aware power, mechanism ablation, unseen prediction and independent evaluator. No superiority/breakthrough claim from this pilot.

Frozen local runner SHA256 b83c99edc91320663ff8dcd99242df4ab83ea6a74717adcbba18765c3964d633; workflow SHA256 e56068fca0ea5b626e50606d3084405b802134a8443179e42987b15c5082e358.
