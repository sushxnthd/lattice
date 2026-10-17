# Run82 SCIENCE / SYSTEM ledger — 2026-10-17

## SCIENCE — evidence, not syntax progress
- **Active kernel:** whether semantic IR reduces capable-model repair complexity beyond Python with the identical frame compiler, verifier, semantic facts, and token budget. The current Run79 treatment only changes output notation.
- **New exact counterexample (synthetic):** for all six frozen development tasks, give both arms the identical correct assignment. The native IR parser accepts 6/6; the native Python-dictionary parser accepts 0/6. Yet an arm-blind format-normalized diagnostic verifies the same correct semantic content in 6/6 for both. Apparent native difference = +100 percentage points; normalized difference = 0. The exact two-sided paired discordance p-value for the synthetic native contrast is 0.03125. This is an *identification counterexample*, not a model result.
- **Evidence artifact:** `research/run82/synthetic_counterexample.json`; tested in `tests/test_run82_format_confound.py` and `tests/test_run82_format_diagnostic.py`.
- **Limitations:** no capable-model inference, no model transcripts, no new frozen holdout use, no unseen multi-file tasks, no representation superiority. Normalized scoring is observational and cannot replay a counterfactual repair-feedback trajectory.
- **Smallest supported claim:** Run79's raw endpoint cannot, by itself, identify a semantic-representation causal effect; output-format compliance can fully explain a large arm difference even when semantic content is identical.
- **Kill/reformulate trigger:** after three actual capable-model comparisons without a surviving format-normalized or structural effect, pivot to semantic compiler/editing product. No infrastructure attempt counts as a scientific failure.

## SYSTEM — capability and validation
- Added `research/run82/format_diagnostic.py`: arm-blind parser classification, trusted-scope check, production `FramedProgram.edit` and independent oracle scoring through the frozen Run79 evaluator, and reanalysis of raw model transcripts when available.
- Added six tests in default CI (two format-confound tests, four diagnostics tests). CI on commit `f4cc7aae8399bc9aa2ff7c4df8a2a5ebbddcfcce`: **63 passed** in run 39056126909, up from the Run81 branch's 57.
- No new DSL syntax or claimed model performance. The diagnostic can prevent agent-repair reports from confusing parser failure with incorrect semantics; that is a real evaluator capability, not yet a demonstrated end-user performance gain.

## Execution / reproducibility
- Isolated branch: `research/run82-capable-model-execution-20261017`.
- Parent: `research/run81-paired-repair-inference-20261017` at `427a4aa2e632775e154a0abc56fca866cb6fd643`.
- Attempted `.github/workflows/run82-paired-repair.yml` to execute frozen Run79 7B protocol; GitHub connector safety checks blocked workflow-file creation. A longer diagnostic write and a separate paired-statistics write were also rejected; the smaller diagnostic implementation and CI tests were committed successfully.
- Frozen prompts/model identifiers remain in `research/run79/prompts.py`, `research/run79/model_pilot.py`, and `research/run79/KERNEL.md`. Model planned: Qwen2.5-Coder-7B-Instruct-GGUF Q4_K_M, pinned llama.cpp, seed 271828, two calls; **not run**. Raw model transcript: **none**.
- No force push, merge, user laptop, paid API, or holdout access.

## Next highest-information discriminator
Run the preregistered capable-model pilot on no-cost compute when a permitted workflow/inference path is available. Report both the original native endpoint and post-hoc format-normalized endpoint, then freeze a genuinely structural IR-versus-Python same-compiler test on realistic multi-file tasks. If capable-model execution remains blocked, continue concrete compiler/repair-diagnostic integration rather than adding cosmetic notation.
