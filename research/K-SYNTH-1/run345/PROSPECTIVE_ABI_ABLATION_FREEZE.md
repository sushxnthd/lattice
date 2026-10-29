# K-SYNTH-1 Run345 pre-execution freeze — historical Jinja ABI-only ablation

Date: 2026-10-29 UTC. This is a **post-Run344-outcome, prospective-to-Run345-adapter-execution** mechanism ablation, NOT a new independently qualified task and NOT a model repair.

Parent: original Run344 Jinja PR1242 source qualification (8th PR, 7th repository). Preserve all 56 original observations, original oracle SHA-256 `4d121eb18d8071eacbf5967c7fa62e458f3bcad140b85be1f2398c163e37d5f0`, base commit `94ccd028ef1f3cd9eaec862d6a1d646d02a242bc`, reference `f71f5ebab2e76c5ee6f5f705a2703f3891e762bc`, exact Git blob identities from Run344.

**One fixed adapter intervention:** on the BASELINE `src/jinja2/runtime.py` only, in `Context.call`, insert `kwargs.pop("_loop_vars", None)` and `kwargs.pop("_block_vars", None)` immediately before the existing `try: return __obj(*args, **kwargs)`. No context derivation, value transfer, compiler changes, test modifications, or reference-source edits. Fail closed if the source anchor is not unique or Git blob hash differs.

Run in isolated GitHub Actions environment with disposable historical checkout. For `00A` use base compiler + adapter runtime; `10A` use reference compiler + adapter runtime; for `01A` and `11A` use unmodified reference runtime and the respective base/reference compiler. Preserve original `00,10,01,11` records separately and do not overwrite them.

**Predeclared prediction** for `10A`: targets T03,T04 pass; T01,T02,T05,T06 fail by missing dynamic context; all C01–C08 pass. Counts 2/6 targets and 8/8 controls. For `00A`, baseline 1/6 targets, 8/8 controls; `01A` remains 1/6 and 8/8; `11A` remains 6/6 and 8/8. Expected casewise interaction positive on T01,T02,T05,T06, zero on T03,T04 and controls. If not observed, record failure and investigate without changing this prediction.

Evidence: exact source blob SHA-1, SHA-256 for all overlays, adapter diff and SHA, raw per-case outputs/errors, stdout/stderr/exit codes, oracle/runner SHA, reproducible manifest and independent replay/audit. Keep all 89 boundary issues SEALED. One K-SYNTH-1 kernel; branch `research/exp003-context-order`; only PR #9 open/draft/unmerged. No IR superiority or breakthrough claim.
