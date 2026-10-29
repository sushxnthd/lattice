# K-SYNTH-1 Run351 — provenance correction and frozen paired-model launch

Date: 2026-10-29 UTC / 2026-10-30 IST. Kernel: K-SYNTH-1. Canonical PR: #9, draft/unmerged. All 89 reserved boundary issues remain sealed.

## Critical source-provenance correction

Run348 described two HTTPX files as the pinned pre-repair baseline. An independent source SHA check during Run351 found that its `_api.py` actually came from **Run335's model-edited stage** (both model arms had changed `httpx/_api.py:head` from `allow_redirects=False` to `True`). The stage's SHA-256 is `81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe`, Git blob `71712bffd015d3687a715fa65ca1f785ea16a90d`. The genuine historical baseline at commit `891d865044d27c229278f0fa20d84ba4007cb289` is SHA-256 `bd646bd7bfddd75eba6687bef45b52f5c9e1b7634d680fbcbfaf16304b618f5d`, Git blob `a300f633e7ace1d0876a39735bf9af0c7ac64336`. The other file `_client.py` is genuinely baseline: SHA-256 `6b223a7a32afcbaf4e1a9a83f6d34caf8f66a31d740a1ac511df678463ecd8a2`, Git blob `e3b2f5b31913f210491a6c5fc2bff1c454833440`.

The true `_api.py` baseline was reconstructed by reverting the sole model edit and independently matched against the pinned Git blob and cloud checkout. The Run348 source-provenance description is **incorrect** and must be amended; do not silently rewrite its frozen evidence. Re-running the unchanged Run348 analyzer on the genuine baseline yielded the same 93 `_api.py` local-binding certificates, unknowns, and call records; `_client.py` remains 272. Thus the **365 abstract fact records are invariant under this single signature-default change**, but the old source identity claim is not valid.

## New verified source-only evidence

Run351 independently checked 31 Boolean `allow_redirects` signature defaults on the genuine baseline (28 True, 3 False). A safe reconstructed-signature CPython probe checked omitted/default, explicit True and explicit False binding for each, totaling 93 functional observations. A separate AST auditor validated signature locations, default literals, pinned source identities and 23 relevant local reaching-definition facts, with all runtime callees explicitly `UNKNOWN`. Local test suite: 19/19 PASS, including adversarial mutations.

The 23 facts were frozen into two information-equivalent, read-only presentations: graph IR edges versus ordinary Python/AST binding literals. No reference patch or model output was used to choose them. Both prompts retain the original public HTTPX #1146 issue text, 31 candidate edit slots, identical shared compiler, model, seed, schema and isolated functional oracle. This is a **narrow test of verified lexical-dataflow presentation**, not a test of globally sound cross-file runtime semantics.

Frozen fact SHA-256: `46aabe8c411a73c3d4888b11d3c09531e771ef54ba9e58739448dab110400910`.
Augmented IR prompt SHA-256: `cb856af412a241b8de8d6ac2088292921c9a695fbb0415820a71c2bb7f7195f3`.
Augmented Python/AST prompt SHA-256: `c80c32f016a677799c8627ee67bbdce546df53469d264835a2a5d402aa71b517`.
Prompt lengths: 17,136 and 17,502 UTF-8 bytes respectively. Actual model-token counts are measured by the pinned llama.cpp tokenizer in the cloud run, **not inferred from byte lengths**.

## Genuine model inference

A new no-cost GitHub Actions workflow was committed and triggered:
[Run351 paired Qwen workflow](https://github.com/sushxnthd/lattice/actions/workflows/lattice-k-synth-1-run351-dataflow-pilot.yml).
Pinned model: Qwen2.5-Coder-7B-Instruct Q4_K_M, SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. The existing Run335 gate, common compiler and Docker-isolated oracle are reused, with new prospectively frozen dataflow facts. Source-provenance and escaped-newline failures in initial workflow attempts were recorded and corrected; the corrected run ID is `40965977369`. No completion or model success is claimed before the raw artifacts are independently retrieved and audited.

## Limitations

This is one historically qualified repository, not the primary powered multi-repository study. Run348's source-identity correction must be propagated to documentation. The source-only signature probes are **not** production repair outcomes. Historical qualified cohort remains eight PRs across seven repositories. Full historical ZIP mirroring remains incomplete. No IR superiority, causal mechanism or breakthrough is claimed.
