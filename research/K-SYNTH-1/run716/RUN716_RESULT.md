# Run716 — bounded snapshot comparison

Date: 2026-11-17 UTC. Research branch `research/exp003-context-order`; draft PR #9. All 89 reserved issues remain sealed.

The Run715 alpha `--check` and `--check-api` paths used `Path.read_bytes()` on an arbitrary snapshot file, permitting unbounded memory allocation despite bounded source input. A local candidate patch uses `snapshot_stream.read(len(report.encode('utf-8')) + 1)` to detect exact equality and any oversized mismatch with bounded allocation. Four subprocess checks passed: exact snapshot (exit 0), 4 MB overlong snapshot (exit 4), short mismatch (exit 4), restored exact snapshot (exit 0). `py_compile` passed. Local SHA-verified ZIP `run716.zip` SHA256 `0350abd6ef0ee2e79564a24f46b8767fefb28b764c8b4f027b6ed9611a904945` contains source patch, tests, traces, report, manifest. Full archive not yet mirrored to GitHub.

No new qualified production repair or model comparison; qualified count remains two. No semantic-IR superiority claim. Alpha remains unreleased. Next: mirror patch/test, run CI, publish reviewed alpha, continue prospective paired study.
