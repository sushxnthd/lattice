# K-SYNTH-1 Run446 frozen mechanism protocol

Freeze date: 2026-11-03. Canonical branch `research/exp003-context-order`, single draft PR #9, 89 reserved issues sealed.

## Fixed provenance
Original Run445 real Flask Actions 41522993332 artifact SHA-256 `5cca13b9d9e6c781f187282c75f8cf3480207ba2ad8e2ce57e2d0aa3febf8ef0`; original 128-case list SHA-256 `b04edef3965002c27c5194ae4b4ca7bf5464ad7bfd757d4e39d987b09d84c3b3`. Historical Flask parent `514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b`, reference `7203feabf723edae0286ae5dc64fec8ac4c91735`, parent testing.py SHA-256 `60c60294d716a6102e9993ad8f14930ad421fde322d8d3b54c7be642acbad560`. The only testing.py reference change is cookie host extraction; app.py remains at parent in both conditions.

## Prospectively frozen questions and disconfirmation
The four baseline-only DNS explicit-port-zero session failures were `dns_with_port_01/09/17/25`; all four reference session round-trips passed. On raw input authority `nodeN.example.test:0`, `partition(':')[0]` and `urlsplit('http://'+authority+'/').hostname` agree. **This does not establish equality on actual Flask request properties.**

H1: `ctx.request.host` and `ctx.request.host_url` differ in a way that changes the two actual extraction results on these four inputs. Reject H1 if the two recorded extractions agree in every case.

H2: reference and parent `_update_cookies_from_response` receive different domains or store cookies under different keys. Reject H2 if the captured domains and cookie-jar keys agree on all four cases.

H3: the four-case outcome persists under a fresh isolated, exact-parent checkout with a pinned Werkzeug version. Reject H3 if baseline and reference no longer differ; label the original mechanism **environment-dependent/unresolved** rather than rewriting original results.

Run all 128 original frozen authorities in both conditions, in fresh processes; record `request.host`, `request.host_url`, old/new extractions, cookie domain, cookie jar keys, response, errors, Python and dependency versions, source SHA, and raw traces. Do not adjust cases after results.

The run is **post-qualification mechanism analysis**, not a new independent task, not a powered model comparison, and not a third qualified repair. No model-generated code executes on host. All failures retained; no retroactive benchmark promotion.
