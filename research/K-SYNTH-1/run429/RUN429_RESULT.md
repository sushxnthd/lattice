# K-SYNTH-1 Run429 — production HTTP clients become indistinguishable under a lossy oracle

**Scientific decision:** Exploratory oracle-validity result and post-hoc mechanism ablation, not a new qualified multi-production-source repair or an IR superiority claim. Run428's frozen oracle and rejected qualification are unchanged; all 89 reserved boundary issues remain sealed.

## Experimental contract

Three real installed clients (urllib3 2.7.0, Requests 2.32.5, HTTPX 0.28.1) sent 80 deterministic loopback HTTP paths each. The corpus crosses 1–5 leading slashes with 16 suffixes involving colons, queries, fragments, percent encoding and nested slashes. A single `BaseHTTPRequestHandler` captures both the raw request line and the parsed `.path` from **the same request**, avoiding Run428's cross-request comparison. No proxies, redirects, or external network.

All 240/240 client requests succeeded. The server reported **identical paths for all three clients in all 80 cases**, but Requests differed from urllib3 and HTTPX at the wire in 64/80 cases. The latter two matched at the wire in all 80.

| Client | Wire preserves input path (fragment removed) | Handler appears to preserve | Wire vs handler differs |
|---|---:|---:|---:|
| urllib3 | 80/80 | 16/80 | 64/80 |
| HTTPX | 80/80 | 16/80 | 64/80 |
| Requests | 16/80 | 16/80 | 0/80 |

The server-only score collapses the real 80/80 vs 16/80 difference into a three-way 16/80 tie. This is a finite, constructed-corpus measurement result, not a general claim of library superiority.

## Mechanism and ablation

For input `//v:h`, Requests sends `GET /v:h HTTP/1.1`; urllib3 sends `GET //v:h HTTP/1.1`; the handler reports `/v:h` for both. Installed Requests `HTTPAdapter.request_url` explicitly removes repeated leading slashes; CPython `BaseHTTPRequestHandler.parse_request` also normalizes them before setting `.path`. Source SHA-256 values are in the local reproducibility archive.

A post-hoc Requests adapter override returning the unchanged `PreparedRequest.path_url` was evaluated on 80 matched cases (160 additional actual requests). Prepared paths remained identical, raw targets changed in exactly 64 cases, raw preservation rose from 16/80 to 80/80, and **zero** server-observed paths changed. This isolates the bounded client-side mechanism; removing the production safeguard is not recommended.

An independent auditor replayed all 240 original wire targets using raw stdlib sockets and checked 1,440 predicates with zero disagreements. A second auditor replayed all 160 ablation targets and checked 720 predicates with zero disagreements. **400 client requests + 400 independent socket replays = 800 real HTTP observations.** Thirteen adversarial/regression tests passed. Clean-extraction replay of the local SHA-verified archive passed.

## Finite theorem

Let `H` be the server-only observation and `F` a wire-level predicate. If `H(w1)=H(w2)` but `F(w1)!=F(w2)`, then no function `G` of `H` alone can satisfy `G(H(w))=F(w)` on both inputs. The `//v:h` and `/v:h` pair is a concrete witness. Therefore a server-only repair oracle cannot distinguish some genuine wire-level behavioral differences.

## Limits and status

The 80 paths are curated deterministic cases; no population prevalence, McNemar p-value or confidence interval is justified. The experiment does not decide which client's behavior is normatively correct. Future HTTP qualification must freeze raw-wire oracles *before* examining post-fix sources. The Run428 historical Actions matrix artifact IDs remain unverified and are not counted.

Strictly qualified independent real multi-source repairs: **2** (Flask PR6096, urllib3 PR5071). New coding-model completions: **0**. Powered IR superiority: **none**. Run430 resumes prospective real qualification and matched functional open-model inference.

**Local archive SHA-256:** `44c8a732bfd1c08262439d4e5568d8c9a0dbec7e78bbfd1e5f020279d2da5137`. Contains raw JSONL observations, source provenance, both independent auditors, adapter-ablation receipts, 13 tests, executable witness, full report, next protocol and preceding Run428 archive.
