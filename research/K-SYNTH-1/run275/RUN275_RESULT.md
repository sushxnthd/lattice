# K-SYNTH-1 Run275: original blind-Qwen failure audit and post-hoc compact-context feasibility

Date: 2026-10-26 UTC / 2026-10-27 IST. Canonical branch `research/exp003-context-order`, one draft PR #9. All 89 boundary issues remain sealed.

## Decisive recovered result (unchanged Run271 experiment)

The original Run271 GitHub Actions run `40357685395` completed with workflow status SUCCESS. **This does not mean model inference succeeded.** Independently downloaded original artifact `12681398014`, ZIP SHA256 `f4cac01fa8d6f4d674ed87d6c493a99f7fdb889913f9158d556e790e9626e29b` matching GitHub's artifact digest. All **27 original manifest entries** verify. Both four-arm prospective freezes, prompt/request/fact hashes, declared model SHA, seeds, temperatures, and information-equivalent JSON/Python presentations verify.

**Eight of eight model requests failed without a completion:** six client read timeouts after 1,800 seconds each, and two HTTP 400 responses. Original server log confirms two 34,942-token requests exceed the 32,768-token context window, and six other requests were canceled after the 1,800-second timeout while still processing prompt tokens. The HTTP-400 pair are the urllib3 Python-literal arms. There are **ZERO raw completions**, **ZERO model patch transactions**, and **ZERO functional model-patch oracle runs**. These are compute/transport-censored outcomes, NOT model abstentions or unsuccessful functional repairs. Do not compare arm performance, claim semantic parity, or merge with Run270's eight genuine abstentions.

Run271's original requests and scores are immutable. The source candidate authority was gold-expressible in both tasks under separately labeled post-freeze positive controls (Runs272/273); this does not rescue inference measurement validity.

## New executable science: resource-aware candidate projection (EXPLORATORY, post-hoc)

Implemented `compact_projection.py` on frozen, baseline-source-only Run271 facts. It selects 12 high-scoring candidates per authorized production file plus issue-lexical fallbacks. These fallbacks were devised **after examining the two known gold repairs**, so the projection is NOT a prospectively blind localization study and cannot validate generalization. It changes candidate authority and task information compared with Run271; no frozen historical results are rescored or pooled.

| Task | Original AST candidates | Compact AST candidates | Serialized facts reduction | Post-hoc gold edit nodes retained |
| --- | ---: | ---: | ---: | ---: |
| Flask PR6096 | 141 | 29 | 79.09% | 5/5 |
| urllib3 PR5071 | 192 | 27 | 80.52% | 3/3 |

All retained candidates preserve exact original source hashes, AST IDs, preimage hashes, offsets and replacement authority. Both compact fact dictionaries round-trip exactly through JSON and Python literals. The unchanged v4 atomic compiler reconstructed both original upstream reference files **byte-for-byte** from the compact authorized candidate sets for each task, using explicitly reference-derived positive-control replacements. No model generated these replacements; no functional model patch was executed.

A separate independent read-only replay of the original Run274 Werkzeug negative artifact confirms the same one prospectively frozen discordance (`full`/`toggle_on`: expected REDIRECT, observed NOT_FOUND) among 28 source-ablation outcomes. Werkzeug PR2860 remains unqualified, and the qualified real issue count stays TWO.

## New model experiment

Launched a **separate exploratory** four-arm-per-task Qwen7B run, GitHub Actions `40397730600`, using SHA-pinned Run268 transport, Run271 baseline AST retrieval, and the new compact projection. The workflow freezes eight matched requests *before inference*, checks source/model/engine SHA and JSON/Python fact bijection, verifies actual model token budget, captures raw responses and failures, and retains original artifacts. It is a feasibility diagnostic, not the primary powered IR-versus-Python experiment. The same source-verified graph facts appear in both presentations; intrinsic semantic IR benefit remains unidentified. At report time, the new run is queued, and NO new model completion is claimed.

## Verification and limitations

Five new local tests passed. Original Run271 artifact manifest 27/27 verified. Exact source-verified compiler reference controls passed for both real tasks. No production patch was merged, no untrusted model source executed on the host, and no new independent issue qualified. This does not establish general Python semantic soundness, representation superiority, significance, or a breakthrough. Full historical executable mirroring remains incomplete.
