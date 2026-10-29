# K-SYNTH-1 Run332: corrected AST and two-action competence gate

**Status 2026-10-29 UTC:** Frozen model experiment and cloud workflow committed; no original cloud model outputs have yet been recovered. No new model-generated repair or superiority claim.

## Scientific correction

Run330 incorrectly represented 29/31 keyword-only defaults as positional `args.defaults`. Run332 independently checks 31/31 candidates against pinned historical HTTPX source: 29 `ast.arguments.kw_defaults`, 2 `ast.arguments.defaults`. Both arms receive identical 31 candidate IDs, old values, MAY_FORWARD/UNKNOWN facts, source/edit authority, original issue #1146, JSON schema, shared atomic compiler, and isolated nine-case oracle. Local real prompt characters: 9,783 IR vs 10,453 Python/AST. Actual model token counts await cloud execution; length is a disclosed confound.

A **two-action competence gate** now requires model-generated changes in separate files: `probe_a.flag False→True` and `probe_b.flag True→False`. Both arms must pass before real inference. If either gate fails, the real task is not attempted; do not misclassify this as a failed repair.

## Reproducible pre-inference evidence

- Independent read-only audit: 31/31 source AST candidates and 4/4 frozen requests correct.
- Deterministic adversarial gate contract: 11/11 tests passed (2 valid accepted, 9 invalid rejected).
- Seeded property test: **1,024/1,024** expected decisions, 65 valid accepted and 959 invalid rejected, zero discrepancies.
- Both trusted two-action payloads compiled atomically to identical output SHA-256 across both files. **These are synthetic trusted compiler tests, not coding-model completions.**
- Source SHA-256: `httpx/_api.py bd646bd7bfddd75eba6687bef45b52f5c9e1b7634d680fbcbfaf16304b618f5d`, `httpx/_client.py 6b223a7a32afcbaf4e1a9a83f6d34caf8f66a31d740a1ac511df678463ecd8a2`.
- Runner SHA-256 `0b8eeba574bb589457ed026aec6bcf3ae8048065362c63754d4c933fceabd73c`; independent auditor SHA-256 `648d54480f5fc1a0714f3f1e1c83abc2e4082bd3ac9769f2055a110113aa1085`.

## Cloud execution

Workflow: [Run332 paired Qwen](https://github.com/sushxnthd/lattice/actions/workflows/lattice-k-synth-1-run332-httpx-paired.yml). Model Qwen2.5-Coder-7B Q4_K_M SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, seed 3322026, temperature 0, max completion 768, context 16,384. Model and llama.cpp source pinned; SHA-check before use. Preserve original requests, raw responses, compiler outcomes, oracle traces, failures and artifact manifest.

Original Run330 remains **7/9 IR and 7/9 Python/AST**, not rescored. Three independent historical production issues remain qualified (Flask, urllib3, HTTPX). No powered significance or breakthrough. All 89 reserved boundary issues sealed; PR #9 must remain open, draft, unmerged. Full historical ZIP mirroring incomplete.

**Next:** Recover the original Run332 Actions artifact and independently audit model gate responses, request hashes, source, compiler and nine-case oracle; then advance independent repository recruitment.
