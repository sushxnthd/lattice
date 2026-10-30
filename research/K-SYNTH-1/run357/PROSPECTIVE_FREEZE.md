# K-SYNTH-1 Run357: prospective HTTPcore #882 paired-model freeze

This new exploratory study does not modify or rescore Run355/Run356. Frozen original HTTPcore base `c46802478cdd8a82ee8cb333420080fab1aed00b`; authorized production Git blobs: sync `e108f88b124043b05258f6d98363119b79f92d88`, async `a5eb480840dd4eae73bc8285c9d374a09a0bd44c`.

Issue facts: original HTTPcore #872; PR #882. Same original source, issue, line-edit compiler, edit authority, seed 3572026, temperature 0, 3500 completion-token budget and Qwen2.5-Coder-7B Q4_K_M SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c` in both arms.

The two pre-inference prompts contain the same 112 independently reconstructible source-derived records (48 conditional local-binding facts, 50 explicit UNKNOWN records, 14 lexical calls). Semantic IR uses a typed edge list; the ordinary Python/AST baseline uses AST-location-indexed binding maps and uncertainty/call lists. Neither prompt contains reference-derived patch locations. The shared atomic line editor and isolated Docker functional oracle are fixed before inference.

Frozen prompt SHA-256: IR `e6f75e8b9e594d21c198e36c8c50ad4d8f3b7a6b50b5d3737856ff556dcd8dcd`; Python/AST `184a9b7e7207a4694e7cdb706ce6f58aa7d9b2ac0b23521bf65fdd060c127fbd`. Actual tokenizer counts must be recorded before inference. Any length imbalance is a confound; report separately, never silently claim token matching.

The predeclared endpoint is full functional success on 10 independent isolated oracle cases with 6/10 historical baseline pass. Candidate failures and missingness are retained by stage. This is a single paired issue, not a powered comparison. All 89 reserved boundary issues remain SEALED. Never execute untrusted model code on the host.