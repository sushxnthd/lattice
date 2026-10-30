# K-SYNTH-1 Run357 — prospective real HTTPcore Qwen comparison

**2026-10-30 UTC.** Frozen, locally verified, deployed to canonical branch. **No Run357 model completion or functional repair has been recovered yet.** This is not evidence of IR superiority or a new qualified repair.

Historical issue HTTPcore #872 / PR #882; pinned base `c46802478cdd8a82ee8cb333420080fab1aed00b`. Two authorized production Git blobs: sync `e108f88b124043b05258f6d98363119b79f92d88`; async `a5eb480840dd4eae73bc8285c9d374a09a0bd44c`. Both match independently reconstructed original source.

Built a bounded, reference-blind source-derived ledger of **48 conditional local-binding facts, 50 explicit UNKNOWN records, 14 lexical call records** (112 total). An independent bytecode/AST auditor verified all 48 binding certificates and reconstructed identical facts from a typed semantic graph and ordinary Python/AST-location maps. All **16/16 local tests pass**; four frozen payload SHA entries verified. Calls remain runtime UNKNOWN; no unconditional MUST assertion.

IR prompt SHA-256 `e6f75e8b9e594d21c198e36c8c50ad4d8f3b7a6b50b5d3737856ff556dcd8dcd`; Python/AST prompt SHA-256 `184a9b7e7207a4694e7cdb706ce6f58aa7d9b2ac0b23521bf65fdd060c127fbd`; fact-ledger SHA-256 `bd3c22686e5499429badccb2f15b1375e7a530ffb01f606f92776f3b9daff4e8`. The cloud workflow checks all three before inference.

Both arms use the same original source and issue, edit authority, **Run356 atomic line editor**, isolated 10-case Docker oracle, model Qwen2.5-Coder-7B-Instruct Q4_K_M SHA `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, seed 3572026, temperature 0, completion budget 3500. Historical baseline 6/10, not re-executed locally in this run; cloud must independently confirm. Untrusted model code is never executed on the host.

The dedicated Actions workflow `.github/workflows/lattice-k-synth-1-run357-httpcore-line-graph.yml` and SHA-pinned compressed runner are committed to the canonical branch, within **one open/draft/unmerged PR #9**. Deployed runner blob `f0b9f225014f6ee0fdefcc8e5ed104402e1b42d8`; workflow blob `3e186b26631a1b4cdbd1fd2b88288ecf6e0e30a2`. A workflow commit is **not** evidence of a completed model experiment.

**Limitations:** actual tokenizer counts, raw completions, compiler acceptance and candidate oracle outcomes are pending. Token length may differ; report it as a confound, not token matching. One historical task cannot support a powered claim. No new independent two-production-source qualification, no model success, no breakthrough. All **89 reserved issues remain SEALED**.

Next: recover original Run357 cloud artifact, independently audit every stage, then qualify a NEW independent real two-production-source public-repo repair and expand a clustered paired pilot.