# K-SYNTH-1 Run296: prospective qualification protocol

Freeze time: 2026-10-27 UTC, before execution of the frozen Click oracle on the upstream base/reference configurations.

Candidate: pallets/click PR #2956, merged 2025-07-01. This candidate was selected by inspecting its upstream patch and observing two production source files. This is **not** gold-blind task selection, nor an unseen model task. The public API oracle below was specified independently from upstream test files and frozen before measuring any of the four configurations.

Pinned upstream base commit: `5c1239b0116b66492cdd0848144ab3c78a04495a`
Pinned upstream PR head commit: `9caedb9206103dfb5465e1916bc2f13b9c10c0e4`
Production files: `src/click/core.py`, `src/click/types.py`.
Original and reference Git blob SHAs are embedded in the executable and asserted before any oracle run.

**Frozen executable:** `run296_qualification.py`, SHA-256 `1ff64feb64067c430c12c48645ee1f360b3eb68443bbf6b948a1ebe0fb2f8883`, Git blob `a9f6cb6a1defb5ad6f874ff7cebebaf3b7ab4cfd`.

Four source configurations: base, core-only, types-only, full reference. Each configuration gets the same ten public-API cases: three targets and seven controls. Exact input, expected result, and error classifications are frozen as `CASES` in the executable. All cases run under clean Python subprocesses on ephemeral GitHub-hosted CI, with no model-generated code executed.

Qualification requires: (i) full reference passes all ten target/control cases; (ii) base passes all seven controls but fails at least one target; (iii) core-only and types-only each fail at least one target or control. If any fails, candidate is **NOT QUALIFIED**, even if another post-hoc oracle would rescue it. No retroactive retuning or replacement of cases. Preserve raw functional traces, process errors, source SHAs, and failures.

Scientific interpretation: a successful qualification adds one independent upstream PR (not ten independent repairs), selected with patch awareness. It does **not** establish semantic IR superiority or a model repair. This prospective oracle is a screening gate for a later gold-blind paired model experiment. No reserved boundary issues are accessed.

Run296 must not modify, merge, or close draft PR #9 or touch the 89 sealed boundary issues. The primary powered real-repair comparison remains outstanding.