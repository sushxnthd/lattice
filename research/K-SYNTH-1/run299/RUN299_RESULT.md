# Lattice K-SYNTH-1 Run299: original inference failure audit and compact paired launch

UTC 2026-10-27 / IST 2026-10-28. **No model-generated repair, powered representation advantage or breakthrough.**

## Original Run298: verified precompletion failure

- Original workflow [40573648036](https://github.com/sushxnthd/lattice/actions/runs/40573648036) completed **SUCCESS as infrastructure**, not as a model repair.
- Original artifact 12768591944, ZIP SHA-256 `d1b8226a9b2b42fd3269c80a8f91292539f3e714d3194e359782a8388e21eeac`. Independent read-only audit verified **20/20** manifest entries, exact prompts and zero preflight disagreements.
- Genuine Qwen requests: IR **14,731 input tokens**; Python/AST **16,224**. Both timed out at **900 seconds before completing prefill**. **Zero model responses, zero completions, zero candidate compiles and zero oracle runs.** Do not count these as model abstentions or repair failures.
- Original llama logs: 10,240 tokens of the first prompt processed after 853.5 seconds. A 900-second limit was insufficient even before generation.
- Corrected 24,576-context Run298 [40573706957](https://github.com/sushxnthd/lattice/actions/runs/40573706957) was still in progress at latest verification; must audit separately.

## Prospectively frozen Run299

- [Protocol](PROTOCOL_RUN299.md) committed at `99865112ba38bbfea012483be78d3a198741e881` **before** model inference and postfreeze reference-patch inspection.
- Exact compact selector source SHA-256 `2c0b38d27897567ee920120216188de9bf3ecebbd8049d2e8c5c8d4438ced797`; verified remote blob SHA `06e65f4941060965384c19d013dc1e036af73f41`.
- Original historical h11 baseline SHA pinned; four modules, **12 source-exact windows**, **15,895** source characters. Both arms have identical source snippets, task facts, SHA-pinned edit authority, shared compiler and isolated oracle. IR prompt **17,103** characters; Python/AST **17,179**. Exact tokenizer counts pending.
- Compact context SHA-256 `1a68ad280455912ee21703543d2282a36fc81a976b36c6215349b6ec6e656c59`; request SHA-256 IR `66fe3c17da322cbf7c6e817999cf3d409dd7c03e498ad088d0d2053a7cdfb7f3`; Python/AST `89d2dd72941f8ba98f04366f92c60b92d0ef6788ada1bab8930929e570376843`.
- Pinned Qwen2.5-Coder-7B Q4_K_M model SHA, seed 299001, temperature 0, max 768 output tokens; 900-second timeout per arm. Same Run295 v2 exact-preimage compiler and Run297 5-target/5-control isolated oracle.
- [Original Run299 workflow](https://github.com/sushxnthd/lattice/actions/runs/40579703051) launched; restore and freeze succeeded. **Model completions not yet verified.**

## Executed science and limitations

- Independent source audit: **12/12** windows verified against historical source bytes; both prompt hashes and all 20 original cloud payload hashes matched.
- **128 real paired compiler transactions** on historical h11 source: **96/96** trusted synthetic comment edits accepted in both representations, **32/32** deliberately stale span hashes rejected in both, **zero arm disagreements**, **zero source snapshot mutations**. Independently read-only audited. These are *not* model-generated repairs.
- Postfreeze inspection of h11 PR115 showed the compact windows include changed methods in all three production files but omit a module-level import and regex declaration from the reference patch. This is a source-localization limitation. **Do not retune the frozen context.**
- Local failure ledger: first selector failed to select any `_abnf.py` top-level definition; corrected before freeze by deterministic prefix fallback and nested-method extraction. First independent audit assertion mishandled a first window beginning on line 1; corrected before final read-only audit.
- This is a presentation-only pilot with shared JSON edit grammar, **not** a verified semantic/dataflow-IR editing-language superiority comparison. Five qualified independent real tasks remain, far below powered targets. Historical ZIP mirroring incomplete.
- Canonical branch `research/exp003-context-order`, [one draft open unmerged PR #9](https://github.com/sushxnthd/lattice/pull/9), all 89 reserved boundary issues SEALED.

Full SHA-verified local reproducibility archive contains the original cloud artifact, raw paired compiler outcomes, compact frozen prompts, auditors and failure ledger; see automation run artifact.
