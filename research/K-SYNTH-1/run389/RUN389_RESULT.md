# Run389: optional-subset editor fairness and frozen Rich pilot

Date 2026-10-31 UTC. Single K-SYNTH-1 kernel, branch `research/exp003-context-order`, sole draft PR #9; 89 reserved boundary issues untouched.

## Identified confound
Run388's exact-authority editor required one edit in **each** of the two authorized files. This rejected valid one-file solutions and embedded a reference-known two-function localization. The corrected shared compiler permits 0/1/2 edits, at most one unique undecorated top-level function per authorized source file, and leaves all eight Rich base-source functions selectable. It pins source SHA-256, checks edit identity, syntax and bytecode, and never executes model code on host. Empty edits represent abstention.

## Original deterministic evidence
On the two original Rich #3176 sources: 600/600 valid one-file transactions accepted, 600/600 valid two-file transactions accepted, and 300/300 invalid transactions rejected (60 each: unauthorized path, duplicate path, unknown function, malformed replacement, changed function identity). An independent AST-span auditor reconstructed all 1,200 accepted output SHA pairs and all 300 rejection classes, zero disagreements. Six local unit tests passed. A concrete valid one-file edit is rejected by the previous editor and accepted by the corrected one, preserving the other source byte-for-byte.

## Frozen model pilot
Four exact requests prepared for Qwen2.5-Coder-7B Q4_K_M (SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`): syntactic IR-like NODE/MAY_CALL vs ordinary Python/AST inventory, crossed with source-first/facts-first. Both have identical issue, full source, function/call-name facts, schema and 0/1/2-file edit authority. MAY_CALL is syntax only, runtime resolution UNKNOWN. Frozen request JSON SHA-256 `93edec22fb4c5a22fe558954bc5b53ef14e29ca94b3b023a9866ce291c0cccf3`. Source SHA-256: _wrap `c5f57ff6dd1283aaf38a69ab0ebbbc7c25665256a56007072c37eb2599db6f04`, cells `eb6ef3b49b3dcce2fedfc1c9ee45c17ab47e813f0a05f602f14cc4c0c243618a`.

This is historical reference-known exploratory evidence, **not** a blinded or genuinely semantic/dataflow superiority comparison. No new model completions, functional model repairs, powered statistics, or breakthrough claimed. Original Run387 oracle outcomes and all 89 sealed issues remain unchanged. Local 14-entry SHA-verified reproducibility archive: `lattice_run389_subset_editor_fairness_and_frozen_rich_pilot.zip`, SHA-256 `989b01280d12841c3a5c00814d4acbf2233c0da7878888bb6cdca179ff5ac889`. Full ZIP GitHub mirroring remains incomplete.

Next: exact model inference and isolated oracle, plus independently frozen unseen multi-source repairs.
