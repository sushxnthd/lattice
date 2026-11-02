# K-SYNTH-1 Run427 — issue-first specification-adjudication failure

**2026-11-02 UTC. Decision: REJECTED.** Independently qualified historical real multi-source repair count remains **two**. No coding-model inference or IR superiority claim.

## Prospective issue-first freeze

Before inspecting the fixing reference, froze [HTTPX issue #1404](https://github.com/encode/httpx/issues/1404), with exact reported-version base commit `92ca4d0cc654859fc2257c492e55d8752370d427` (HTTPX 0.16.1). The 10-case contract requires per-request cookies to survive same-origin 302/307 redirects in sync and async clients, two cross-origin negatives, two direct controls and two no-cookie controls. It also requires >=2 Python production sources and importable source-component ablation necessity.

**Prospective freeze commit:** `5311f3d162a5c9be9f8d3fbef1184ccf84c9b467`. File Git blob `a484c56b366554f0ccdd77973417e6819d8ae9f7`; SHA-256 `065680ec5c9efea8a061b4121127f03c8b9e5c0a91e38b2dbbd5c98d44d7eca1`. Freeze precedes reference inspection and is never revised.

## Postfreeze reference inspection

Merged [HTTPX PR #1574](https://github.com/encode/httpx/pull/1574) resolves the issue by **deprecating per-request cookies**, not implementing the frozen expectation for `Client.get(..., cookies=...)`. It modifies two Python production files (`httpx/_api.py`, `httpx/_client.py`), docs and tests. The top-level convenience API moves cookies to its temporary client; instance-level per-request calls receive a deprecation warning. Maintainer discussion explicitly identifies cookie persistence as an ambiguous API contract.

**REJECTED**: two changed production sources do not compensate for a fixing reference that contradicts the prospectively frozen behavioral specification. No source ablation or historical repair qualification is claimed.

## Executed functional diagnostic, explicitly nonhistorical

Installed HTTPX **0.28.1**, source init SHA-256 `0ac6997bac998f4ac783adf6d8058a587193315afdb718047c3e4fdff46bcfad`. With in-memory `MockTransport`, 20 sync/async scenarios produced **38 real HTTP request observations**. Frozen criteria: **6/10 pass, 4/10 fail** (all four same-origin per-request cookie persistence targets). Client-level cookies persist on same-origin redirects; domain-scoped cookies do not cross origin; explicit `Cookie` headers are stripped on redirects. An independent replay using separate `BaseTransport` and `AsyncBaseTransport` implementations reproduced all **20 cases, 38 request observations and 70 checks** with **zero mismatches**. **21/21** local regression tests passed. No network calls.

These observations use installed 0.28.1, **not** pinned historical 0.16.1. The latter could not be obtained locally due to unavailable network/DNS. The frozen issue remains rejected regardless of modern-version observations. Full raw JSONL, executable original and independent replay, SHA manifest and tests are in the local reproducibility ZIP.

## Scientific interpretation

The original reporter's desired behavior and the maintainer-adopted API contract are not interchangeable. A benchmark must independently adjudicate normative semantics before looking at the reference. Ambiguous policy issues must be excluded, not post-hoc retuned. This is a **specification-identifiability failure**, not a model failure, proof of multi-source minimality, or an IR advantage.

Outstanding: a third genuinely independently qualified real multi-source task; exact historical editor replay; strong open-model paired functional inference; adequately powered cluster-aware comparison; unseen prediction and historical artifact mirroring. All 89 reserved boundary issues remain sealed. Preserve one K-SYNTH-1 kernel, `research/exp003-context-order` and sole OPEN/DRAFT/UNMERGED PR #9.
