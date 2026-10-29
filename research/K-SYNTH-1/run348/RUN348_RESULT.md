# K-SYNTH-1 Run348 — branch-aware local dataflow, negative/soundness-scoped result

Date 2026-10-29 UTC / 2026-10-30 IST. One K-SYNTH-1 kernel. All 89 boundary issues SEALED. No model-authored code executed, no personal spending or user-device access.

## Intervention

Extended Run347's straight-line, bytecode-checked local reaching-definition analysis to nested if/else, conditional branch joins, return-terminated paths and explicit UNBOUND uncertainty. Certificates are MUST_UNIQUE_ON_REACH or MAY_SET_ON_REACH; dynamic callees remain UNKNOWN. The only positive soundness statement is conditional on standard CPython local semantics, original function execution and no external frame-local mutation. Loops, comprehensions, walrus, try, match, nonlocal mutation and other unsupported control are refused.

## Results

On the same pinned two historical HTTPX source files, eligible functions increased from 39/78 to 47/78, and conditional local-binding facts increased from 307 to 365: 362 unique MUST and 3 MAY. Of 365 facts, 336 are parameter bindings, 26 unique assignment bindings and 3 MAY assignment sets; 65 call candidates remain runtime UNKNOWN. Source SHA-256: _api.py 81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe; _client.py 6b223a7a32afcbaf4e1a9a83f6d34caf8f66a31d740a1ac511df678463ecd8a2.

A seeded deterministic generator produced 4,096 function instances (324 unique source hashes), each tested on all eight Boolean inputs: 32,768 functional traces. Among the instances, 276 had unique-MUST return definitions, 1,596 had MAY sets, and 2,224 were UNKNOWN; 8,042 runtime unbound/name errors occurred only in UNKNOWN instances. Zero observed mismatches for certified runtime-origin membership. The 4,096 draws are NOT independent observations. An independent read-only auditor verified all 365 production facts against source SHA, AST positions and CPython 3.13 load/store sites, plus 32,768 trace records. 14 local tests passed including mutated source hash, read position, modality, graph and AST metadata.

Both graph IR and ordinary Python/AST-action presentations were independently reconstructed to the same fact hashes. However the presentations are NOT model-token matched: _api.py 37,398 IR vs 33,405 Python bytes; _client.py 141,756 vs 128,910 bytes. No model inference, compiler repair, real-issue success, powered significance, cross-file semantic edge, or breakthrough is claimed.

The historical cohort remains 8 reference-qualified PRs across 7 repositories. The source files are historical diagnostics, not a new prospective repair. Full code, test outputs, synthetic functional traces, independent auditor, paired presentations and SHA manifest are preserved in the local Run348 reproducibility archive; full historical GitHub ZIP mirroring remains incomplete.

Next: freeze outcome-blind Jinja #1242 and HTTPcore #882 paired real-model tasks, actual tokenizer/model SHA and length balance, shared atomic compiler and isolated oracle. Include verified-edge ablation, ABI negative controls and independent evaluator. Do not promote previously failed qualifications.