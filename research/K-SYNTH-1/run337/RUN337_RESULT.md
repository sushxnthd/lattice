# K-SYNTH-1 Run337: cardinality semantics and an explicitly excluded candidate

2026-10-29 UTC. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, PR #9 OPEN/DRAFT/UNMERGED; 89 reserved boundary issues SEALED.

## Source provenance and exclusion

Exploratory historical [httpcore PR #1000](https://github.com/encode/httpcore/pull/1000), pinned base `5974b03c7df89d3ee4e23779900d5349d550753c`, head `7fb20526175e2300185ce2b472a97acca95b2525`. Original source Git blobs: sync pool `9ccfa53e597a29ee387f9d16f3af4f695ac0d33a`, async pool `96e973d0ce223f6bed9be9e6a6a2f3c01622c611`. Each original production method contains one `len([connection.is_idle() for connection in self._connections])` expression. Both interface methods annotate `is_idle() -> bool`, but annotations are not runtime enforcement.

**Not prospectively qualified:** a GitHub commit fetch exposed the reference diff before the experiment was frozen. This study is post-reference-exposure, cannot count as the fourth qualified repair, and is not a model comparison. The full local harness executes a trusted manual transcription of the method bodies, not the entire installed repository.

## Bounded functional result

For each sync and async pool method, enumerate all Boolean idle vectors of length 0–8 and every limit 0–n: **4,097 states per module, 8,194 total**. With no queued requests, the independent oracle preserves active connections and closes only the earliest `max(0, idle_count - limit)` idle connections. The original method deviated on **3,020/4,097 states per module (6,040 total)**; the AST-transformed `sum(...)` method deviated on **0/4,097 per module**. Independent state-transition audit replayed all 8,194 raw trace rows with zero disagreements and no missing/duplicate rows. Four adversarial mutations were rejected even with recomputed trace hashes. The finite experiment is exhaustive for the stated stable-Boolean domain, **not** an estimate of real production failure frequency.

[Minimal executable theorem/replayer](research/K-SYNTH-1/run337/run337_cardinality_minimal.py) verifies the same counts independently. Complete SHA-verified local archive (8 payloads plus manifest) is preserved separately: `lattice_run337_httpcore_cardinality_counterexample.zip`, SHA-256 `57730419158249714ab246d9494fb4e8aaa54bbe08b62af4dc40809141171411`. Raw 8,194 traces and original method-transcription runner are in that archive, not mirrored to GitHub.

## Soundness scope

For finite `X`, `len([p(x) for x in X]) = len(X)` regardless of predicate values; under a stable Boolean-return contract, `sum(p(x) for x in X)` counts true results. But a truthy non-numeric object gives `len([object]) == 1` while `sum([object])` raises `TypeError`. A soundness-scoped semantic/dataflow IR must retain `UNKNOWN` for unverified runtime type/purity and cannot silently auto-rewrite arbitrary Python.

## Next real qualification

[Rich PR #3180 candidate protocol](research/K-SYNTH-1/run337/PROTOCOL_RUN338_RICH3180.md) was committed **before inspecting its reference diff**, commit `5768baf35c3999847c2a7878547374a6a16a4d88`. It pins the pre-fix issue #3176, historical base/head, both production source blobs, public/heldout/control oracle criteria and joint component necessity. **Qualification is not yet executed.** Preserve any failures, including possible whitespace-control overconstraint, without post-outcome retuning.

Primary adequately powered, prospectively frozen IR vs information-equivalent Python/AST comparison remains outstanding. Three independently qualified historical repairs remain Flask #6096, urllib3 #5071, HTTPX #1183. No superiority or breakthrough claim.
