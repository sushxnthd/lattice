# K-SYNTH-1 Run428: raw-wire versus server-observation counterexample

**Decision: REJECT** urllib3/urllib3#3352 as an independent multi-production-source repair. The 89 reserved issues remain sealed.

The 14-case issue-first oracle was frozen at commit 29c211c85eb68e6156cd8d6df7fd98bbfbef0259 **before inspecting the fixing PR**. However, installed urllib3 2.7.0 had already been used to calibrate the oracle, so the candidate is explicitly excluded from the strictly independent prospective cohort.

The fixing PR https://github.com/urllib3/urllib3/pull/4952 has head 02d3a75e8f91d59493806782611257dceec1966e and parent 166f66faa5ef23e255f654e8c6b66ad8590fe630. It changes one production Python file (connectionpool.py), one test and one changelog. It therefore fails the >=2 production-source qualification gate. Its test requires preservation of leading // at the lower-level HTTPConnectionPool request boundary.

## Functional evidence

The frozen loopback oracle observed Python BaseHTTPRequestHandler.path, not the actual outgoing HTTP request-target. Installed urllib3 2.7.0 passed 14/14 frozen cases (6 targets, 8 controls). A separately implemented raw TCP server captured the actual request lines: 7/14 raw targets differed from the standard server observation, including **all 6/6 positive targets** and 1/8 controls. Only 7/14 frozen expected paths matched raw-wire observations. The 14 raw-wire and 14 standard-server requests were genuine loopback HTTP executions.

An independent socket replay executed another 14 requests, checked 98 receipt predicates and found the same seven normalizations with zero disagreements. Eleven adversarial/regression tests passed, including a tampered-receipt rejection.

**Executable counterexample:** distinct raw request-targets "//v:h" and "/v:h" both yield BaseHTTPRequestHandler.path == "/v:h". This observation function is not injective, so any oracle restricted to it cannot tell a client that preserves repeated leading slashes from one that collapses them. The installed client **preserves** the raw leading slashes; the standard server normalizes them.

## Historical-source replay

A three-way GitHub Actions matrix was committed at .github/workflows/lattice_run428_historical.yml, pinning issue-base d4ffa29ee1862b3d1afe584efb57d489a7659dac, PR-parent 166f66faa5ef23e255f654e8c6b66ad8590fe630, and PR head 02d3a75e8f91d59493806782611257dceec1966e. It uses python -S, an import-provenance assertion, and raw artifact retention. **Its execution outcome was not verified at reporting time.**

The candidate remains rejected on independent grounds: single-production-file reference, post-release calibration exposure, and a frozen oracle that cannot identify the target behavior. No retrospective changes to the frozen oracle or acceptance criteria are permitted.

**Status:** Two previously qualified independent multi-source repairs; zero new model inference, no powered IR superiority, no breakthrough. Complete local SHA-256 evidence archive available separately; GitHub mirroring of raw artifacts remains incomplete.
