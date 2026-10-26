# K-SYNTH-1 Run265: bounded cross-file provenance IR and frozen paired feasibility pilot (2026-10-26)

## Scientific result
Implemented a source-SHA-verified cross-file MAY provenance graph (local `bounded_provenance_ir.py`) with verified *syntactic candidate* import edges, simple alias propagation, if/else joins, and explicit UNKNOWN for open-world runtime resolution and unsupported constructs. This is not a sound general-Python semantic IR. Both graph-anchored actions and ordinary Python byte-span actions lower through the identical Run264 v4 atomic compiler and edit authority.

Constructive counterexample: `fn=lambda:1; if (fn := (lambda:2)): pass; return fn()` returns 2, but a naive branch may-def analysis identifies only the first lambda. Corrected conservative analyzer includes UNKNOWN. Reproducible trace in local `walrus_unsound_trace.json`.

Validation: **63/63 inherited and new tests passed**, including 12 Run265-specific tests. Deterministic 512/512 generated import/alias/if programs (seed 2652026) had the observed controlled runtime callee among source candidates (zero observed misses; not a general proof). On real pinned Flask PR6096 baseline, graph SHA256 `b51913f505276f7a32c0a2600159ddda49ce1f13d46cf584d62856ddaae4dc11` includes 3 source-verified cross-file import candidates, 179 static call sites, 33 explicit unknown events; NO guaranteed runtime bindings. Five upstream reference edits reconstruct both source files byte-for-byte under graph-anchor and Python byte-span normalization using the same v4 compiler.

## Frozen matched pilot, not model evidence
Constructed an explicitly **oracle-localized** pilot using only OLD edit spans selected by upstream reference diff, without intentionally including replacement text. This is privileged localization, NOT blind issue solving. Both arms receive identical task, source snippets, pinned hashes, provenance graph facts, candidate spans, compiler contract and edit authority; only action encoding differs. Pinned model Qwen2.5-Coder-7B-Instruct Q4_K_M SHA256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, seed 265001, temp 0, max output 2048.

Flask PR6096 semantic-IR arm request SHA256 `78ff43535bc34734355723a4b6725cbd9fa6758159bca526c6cacb686f78408e`, prompt SHA256 `9bc3b0caf29547c92fc259e58ae6e2b1a8ee7a2bb19dbb5304642b7f661e4141`, 14009 UTF-8 bytes.
Python span arm request SHA256 `75e33fd5270e45f461819898f1733dcf7d4b81d17800e94095d01b4745ad96c5`, prompt SHA256 `6fe5ee6048c953ecd377e8021e1c0a57a92a1cdeb6b982ead39ba3873c306fcc`, 13993 bytes. Both include five OLD spans. This is the SAME Flask issue, not a new independent sample.

**No new model inference, tokenizer counts or model-patch functional oracle results were obtained in Run265.** Local environment has no Qwen model; no new cloud inference run was confirmed launched. urllib3 PR5071 remains second independently qualified task from Run264, but its Run265 prompts have not yet been frozen. No superiority, significance or breakthrough claims.

## Persistence
Complete local 65-entry SHA256-verified ZIP `/mnt/data/lattice_run265/lattice_run265_bounded_provenance_ir_and_frozen_pilot.zip` SHA256 `396086e3184b8687cb6459d4335e71410c235bcb82079ccbebbf3ae9f732dff5` contains full source, tests, frozen prompts, witness, prior evidence and manifest. **Full code/ZIP not yet mirrored to GitHub; retry without blocking science.** 89 boundary issues remain sealed.

## Next
Mirror full code and frozen requests; freeze urllib3 paired prompts; launch actual pinned Qwen inference on both qualified issues and run strict shared compiler plus independent isolated public/heldout/nonregression oracles. Treat these as feasibility pilots, not powered evidence. Continue qualifying independent multi-source real issues; retain one kernel/branch/draft PR #9.
