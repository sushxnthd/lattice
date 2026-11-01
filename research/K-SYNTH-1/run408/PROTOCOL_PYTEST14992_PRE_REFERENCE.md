# K-SYNTH-1 Run408: prospective pytest #14992 issue-first oracle

Frozen on 2026-11-01 IST before inspecting any reference patch, fixing PR, changed-file list, or reference behavior for issue https://github.com/pytest-dev/pytest/issues/14992.

Original control source: pytest 9.0.3 commit a7d58d7a21b78581e636bbbdea13c66ad1657c1e.
Original regression source: pytest 9.1.1 commit cf470ec0bf7eb89cd97dd56df4859eae5db46447.

Immutable 12-case oracle in the SHA-verified Run408 archive: 3 public target variants, 3 heldout target variants, 6 nonregression controls. Target: an explicit pytest_generate_tests hook moves the autouse fixture name to the end, and a class usefixtures guard must run before the autouse fixture's dependency subtree. Controls check fixture presence. All 12 must pass on control; all 6 targets must fail on regression while 6 controls pass. The six variants are one structural family, not six independent tasks.

Require exact installed source SHA, isolated environment, raw stdout/stderr, source hashes, exit codes, artifact SHA manifest, and an independent evaluator. The local pytest 9.0.2 preflight is NOT a pinned baseline comparison.

Before any promotion to a real multi-production-source repair, require genuine fixing reference success on all 12 cases; at least two distinct changed production .py files; and two independent behavioral leave-one-production-file-out necessities under joint target-plus-control oracle. Import errors, signature mismatches and harness failures do not count. Never retune the frozen cases or use reference-derived localization in model prompts. Preserve all 89 sealed issues and the sole draft PR #9.