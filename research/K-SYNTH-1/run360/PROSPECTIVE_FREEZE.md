# Run360 prospective Jinja PR1242 source-ablation freeze (2026-10-30 UTC)

This is a **new prospective qualification attempt**, not a completed qualification, independent new cohort member, coding-model comparison, or IR superiority claim. Do not retrospectively change the rules after seeing outcomes.

Public PR: https://github.com/pallets/jinja/pull/1242. Historical base commit `94ccd028ef1f3cd9eaec862d6a1d646d02a242bc`, PR-head commit `f524bcce0cf295941fe665cbcb6846e7e9f39df5`. Exact Git blob IDs:

| Source | Historical base | PR head |
|---|---|---|
| src/jinja2/compiler.py | df6fa372e60182cbadabd437a538f3c3997d102e | 50f98f1a9c064e3f270eed5ae547b1138584bce0 |
| src/jinja2/runtime.py | a05b196118bc355c10f1cfff245a958c1089e968 | 4a3c36eeaf5a480b824e6c01f4ac6034e4d9e65a |

Prospectively frozen 2x2 source configurations: base, compiler-only, runtime-only, full reference. Same 12-case public API oracle in every arm: 4 PR-inspired public targets, 2 independently written heldout targets, 6 nonregression controls. All expected outputs, template SHA-256s, exceptions, source blobs and case outcomes must be preserved. No reference-derived model localization. Modern Jinja 3.1.6 preflight was 12/12, **not historical evidence**.

Qualification requires full reference 6/6 targets and 6/6 controls, baseline at least one target failure and 6/6 controls preserved, and each partial component at least one target or control failure. Report target and control factorial interactions separately. If full reference or any predeclared criterion fails, **FAILED**; no retroactive repair. This tests joint target-plus-control component necessity, not necessarily target-only interaction.

Use Python 3.9, MarkupSafe 2.0.1, no-network read-only nonroot Docker for historical source execution. Independent read-only auditor verifies all four source SHA combinations, template/expected invariance, outcomes and complete cases. All failures and raw results preserved. Jinja PR1242 may already be in the historical cohort: do not double-count without deduplication. All 89 reserved issues remain sealed. Sole PR #9 stays open/draft/unmerged on `research/exp003-context-order`.