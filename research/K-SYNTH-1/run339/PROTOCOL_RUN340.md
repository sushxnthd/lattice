# K-SYNTH-1 Run340: prospective HTTPcore #882 qualification freeze

Frozen 2026-10-29 UTC before reference patch inspection. Candidate: [encode/httpcore PR #882](https://github.com/encode/httpcore/pull/882), issue [#872](https://github.com/encode/httpcore/issues/872). Public issue states that h11 trailing_data after CONNECT or Upgrade should be returned by the public response.extensions["network_stream"] before later stream data. Public issue hints are common task facts for every model arm.

Historical baseline commit `c46802478cdd8a82ee8cb333420080fab1aed00b`; reference PR head `c617b700fe0b06b33af8a604d3c8d6e1fbbe806c`. Baseline blob SHA1: `httpcore/_sync/http11.py` `e108f88b124043b05258f6d98363119b79f92d88`; `httpcore/_async/http11.py` `a5eb480840dd4eae73bc8285c9d374a09a0bd44c`. Exactly these two production files may be independently substituted; everything else remains baseline.

## Predeclared isolated public-API cases

Use ConnectionPool and AsyncConnectionPool against deterministic in-memory NetworkBackend/NetworkStream fakes, recording raw read/write/close traces, with no live network.

Targets (all must pass): (1) sync CONNECT 200, (2) async CONNECT 200, (3) sync Upgrade 101 with valid Connection/Upgrade headers, (4) async Upgrade 101. In each, first mock read contains complete HTTP headers followed by b"HELLO", second mock read yields b"WORLD"; first public response.extensions["network_stream"].read() must yield exactly HELLO, second exactly WORLD, without loss/duplication/reordering.

Controls (all must pass): (5) sync GET 200 Content-Length:5 with body HELLO, (6) async GET same, (7) sync CONNECT with no trailing bytes in header read and next read WORLD, (8) async CONNECT same, (9) sync Upgrade with no trailing bytes and next read WORLD, (10) async Upgrade same. Correct status parsing and no invented empty payload required. Public API only: if tests require private state, candidate NOT QUALIFIED.

## Frozen decision

Four source arms: base/base, ref-sync/base-async, base-sync/ref-async, ref/ref. Baseline passes all controls but fails >=1 target; full reference passes all 4 targets and all 6 controls; each single-source arm fails >=1 target belonging to its unrepaired implementation while passing every control. An ABI-only exception is not valid semantic necessity; run a compatibility-only negative control, and if any arm is ABI-confounded reject qualification. Any violation -> NOT QUALIFIED, preserve all outcomes without retuning. Independently verify source SHA, frozen cases, functional traces, and decision. Reference-derived localization forbidden in later model comparison. No superiority claim.

The expanded local freeze artifact is SHA256 `e69c059ea8a333d2b9564bcc9661ff456665a9f73fb3e0ea236885cd9f642428` (`PROTOCOL_RUN340_HTTPcore_882.md`). This commit is the online authoritative freeze. Rich #3180 remains failed. Three qualified historical repos unchanged. All 89 reserved issues SEALED. Only one K-SYNTH-1 kernel, branch research/exp003-context-order, draft PR #9.