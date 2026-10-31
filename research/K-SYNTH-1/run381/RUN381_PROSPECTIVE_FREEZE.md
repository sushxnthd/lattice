# K-SYNTH-1 Run381 prospective freeze: HTTPcore #724

Freeze recorded before inspecting any subsequent reference repair.

- Public issue: https://github.com/encode/httpcore/issues/724 (2023-06-14).
- Pinned historical base: encode/httpcore commit `eb5957d60b240a0deec503a4acca0e69da2833db`. This commit is a docstring/refactor that explicitly removes an unrelated network_stream change; it is **not** treated as the eventual reference fix.
- Source files authorized: `httpcore/_sync/http2.py` Git blob `5cf43b298e6e8489bcb02d6f46ca897ddfae9afc`; `httpcore/_async/http2.py` Git blob `23701808b55371dda50678641660bcee47e2b95e`.
- Frozen local oracle source SHA-256 `b5524eaed8dfaa3ff4b178b682909af5cfc09a52cfb99307c12377d78b625f2a`. Run this source unmodified in an isolated clean Python environment, against exact base and then reference/one-file factorial arms.
- Oracle uses an in-memory actual hyper-h2 server/client frame exchange with no external network and no monkeypatch of the HTTPcore implementation. The public target is `response.extensions["network_stream"] is original_stream`. Heldout target is `get_extra_info("server_addr") == ("127.0.0.1",443)`. Each applies to both synchronous and asynchronous HTTP/2 public responses. Four nonregression controls per mode: `http_version` and stream_id; HTTP status 201; body `OK` and x-lattice response header; reuse for a second request.
- Prospective 12 case outcome: base must pass 8/8 controls and fail 4/4 targets; full reference must pass all 12; each one-file ablation must fail both target checks in its unmodified mode and preserve 8/8 controls. Require the exact upstream reference to change BOTH named production files; no other production file changes needed for targets. If any criterion fails, mark candidate NOT QUALIFIED. Do not relax after outcome.
- Separate aggregate necessity from casewise interaction; expect independent sync/async branches, no cross-file semantic interaction claim from aggregate pass.
- Exclude reference code from prompts, preserve raw outputs/sha/model provenance, use the same compiler and authority for both representations, and treat public issue links that prelocalize code as task facts rather than independent model discovery.
- Local modern httpcore 1.0.9 smoke test passed 12/12, but is **not** evidence of historical baseline or reference success.
- No historical reserved boundary issue was opened, changed, or unsealed. The 89 remain SEALED. Sole branch `research/exp003-context-order`, one K-SYNTH-1 kernel, one open/draft/unmerged PR #9.
