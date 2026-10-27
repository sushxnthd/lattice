# K-SYNTH-1 Run300 — Original Qwen completions, contract incompatibility, upstream reachability

UTC 2026-10-27 / IST 2026-10-28. **Genuine completed inference, but no original accepted model edits or oracle evaluations. No representation superiority.**

## Independently verified originals
- [Run299 original Actions 40579703051](https://github.com/sushxnthd/lattice/actions/runs/40579703051), artifact 12769333311, original ZIP SHA256 `6747c86eb257cb6b389ad525e7b0f8eef51eb6c1b1111105d26d47fbb0cf2b83`. All **33/33** manifest entries independently SHA-verified.
- Qwen2.5-Coder-7B Q4_K_M model SHA256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, seed 299001, temperature 0. IR 4209 prompt/211 completion tokens, 389.546 s; Python/AST 4233 prompt/211 completion tokens, 378.087 s. Both `finish_reason=stop`.
- The **two raw completions are byte-for-byte identical**, SHA256 `e00ede49af816cf9ff7ca9679fffd25cdbeeb7e80d5d0bfe64a0da919d40a6f4`. Both contain fenced old/new JSON. **Frozen compiler: INVALID_JSON for both; frozen oracle: NO_ORACLE for both.** Neither outcome may be retroactively changed.
- Independently recovered corrected full-context [Run298 Actions 40573706957](https://github.com/sushxnthd/lattice/actions/runs/40573706957), artifact 12770922114, original ZIP SHA256 `3a56256e01cd62854adc2dc985a66e590c03f2adf4d86ce68c6074cf0e9339c8`. All **20/20** original manifest entries verified. Both requests timed out before completion (900.116 and 900.069 s); these are not model failures.

## Decisive experimental-contract defect
The Run299 prompt prescribed a JSON object containing only `edits` with `path,old,new` records. The shared Run295 compiler strictly requires top-level `representation,edits,assumptions` and, per edit, IR byte offsets/file+span SHA fields or the different Python/AST-action fields. Therefore a completion complying with the *specified* Run299 output grammar **cannot** pass the actual compiler, even without fences. This is a protocol defect, not evidence about IR.

Raw fenced responses fail `INVALID_JSON`. Retrospectively stripping fences still fails `SCHEMA`. A **posthoc diagnostic-only** strict unique-preimage adapter successfully staged the same edit in both compiler views, with identical canonical/staged hashes and no original source mutations; **11/11** local contract tests passed. This does not promote Run299.

## Bounded source-level functional counterexample
Both completions insert `if lines[0].endswith(b'\\n'): lines[0]=lines[0][:-1]` *after* `buf.maybe_extract_lines()`. The pinned historical buffer extractor requires `b'\\r\\n\\r\\n'` before returning lines. A normal LF-only request cannot reach the added branch; a valid CRLF request line is returned with its delimiter removed, making the branch false. The patched file passed **syntax compilation only**; no model code was executed on the host. A separately authored, AST-checked trusted buffer specification produced **512** deterministic fragmentation traces (256 LF-only upstream-blocked, 256 valid CRLF branch-false). These are correlated functional-model traces, **not** an isolated oracle or independent repair issues.

## Research status
**Five** qualified independent real repair issues, one completed paired model pilot, **zero original accepted transactions**, **zero original oracle runs**, no sixth qualification, no powered IR advantage or breakthrough. All 89 reserved boundary issues sealed. Historical GitHub ZIP mirroring incomplete. Full 61-entry SHA-verified local reproducibility archive: SHA256 `0cd02d095825fbd2d5009980e766570ef26dd495d71ca8ae9748570290d56126` (attached to the automation result).

Run301 must freeze an output grammar that actually passes the shared compiler in *both* arms on synthetic preflight transactions **before** any model inference. Keep identical task facts, source, authority, compiler, verifier and isolated oracle; retain all raw failures and do not retune Run299.
