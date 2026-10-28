# Run328 outcome-blind candidate lock: encode/httpx PR1183

Selected after Run327 failed. **No reference diff or reference source body inspected in this selection step**; only original issue text, merged PR title/body, changed filenames, commit ancestry and blob identities were read. Do not claim this candidate qualified yet.

- Different repository: `encode/httpx`.
- Pre-fix issue: [#1146](https://github.com/encode/httpx/issues/1146), created **2020-08-07 15:44 UTC**, asks for consistent default `allow_redirects` on HEAD requests.
- Historical merged PR: [#1183](https://github.com/encode/httpx/pull/1183), merged **2020-08-16 05:33 UTC**.
- Pinned exact parent baseline: `891d865044d27c229278f0fa20d84ba4007cb289`.
- Pinned exact reference commit: `a226c60861f651b9874e31e66b3bb7f0db46c96d`.
- Two production files only: `httpx/_api.py` (base blob `a300f633e7ace1d0876a39735bf9af0c7ac64336`, reference `4c608f0622dd58adc7d533fd16f64710c7a7f0a8`); `httpx/_client.py` (base `e3b2f5b31913f210491a6c5fc2bff1c454833440`, reference `53d52e5123c82e58bb154626619fbf45898bc6d5`).

**Before inspecting reference source or any outcome**, implement and commit a network-isolated functional oracle using a loopback deterministic HTTP redirect server or equivalent verified in-memory transport. Public targets: default `httpx.head(...)` and `httpx.Client().head(...)` follow a single HEAD redirect to final response. Heldout target: two consecutive HEAD redirects. Nonregression: both entrypoints with explicit `allow_redirects=False` stop at 302; GET default behavior unchanged; explicit `allow_redirects=True` remains functional. Check HEAD method preservation and no external network. Use exactly the same frozen oracle across baseline, `_api.py` only, `_client.py` only and full reference. Require baseline target failure with preserved controls, full reference all targets/controls, and each component removal to lose joint target-plus-control correctness. If any part fails, preserve negative and do not promote.

This lock is **selection and outcome design only**, not a frozen executable oracle. Final executable protocol, independent evaluator and environment/dependency pins must be committed before outcomes. Any necessary revisions must be prospectively versioned, not backfilled. All 89 reserved boundary issues remain sealed.
