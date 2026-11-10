# Run618: Werkzeug #3339 pre-oracle candidate audit

Upstream GitHub API inspected 2026-11-10 UTC. Merged PR "more WSGI environ cleanup". Base b73dce5a2ce14f7c7fd645699d1d878de48d2948, head 0d35bad79a9fe713cca19be480286e203adfa499. Changed production Python files: _internal.py 12 lines; exceptions.py 33; http.py 4; test.py 61; wrappers/response.py 74.

**Construct validity:** helper removal, WSGI request adaptation, cookie handling, exception defaults, typing, and documentation are heterogeneous changes, not automatically one causally coupled repair. Do not qualify by file count.

Executable local 16-case synthetic gate audit: 9 joint-gate acceptances, 4 target-necessity acceptances, 5 joint acceptances attributable solely to control regression. The latter are not target mechanism evidence.

**Candidate NOT_QUALIFIED.** Proposed public targets: run_wsgi_app accepts Request and raw environ; HTTPException.code None for uncoded exception. Proposed controls: raw environ behavior, cookie roundtrip, coded HTTP exceptions. These are preliminary ideas, **not** frozen executable tests. Missing: independent authored SHA-frozen heldout/public/control oracle, exact source snapshots, dependency pins, component partition, baseline/full/ablation isolated outcomes. Do not retrospectively freeze after outcomes. No new model inference or qualified repair. Two previously qualified tasks remain; 89 reserved issues untouched.

Local SHA-verified archive: lattice_run618.zip SHA256 675354204679e0c20fd01c21f275690319673154906eec66319068909cac35e2. Local archive includes executable, raw 16-case matrix, candidate JSON and per-file hashes. Complete raw archive not mirrored on GitHub.
