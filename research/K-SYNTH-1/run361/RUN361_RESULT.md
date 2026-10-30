# K-SYNTH-1 Run361 — original Jinja #1242 factorial recovered

2026-10-30 UTC. Canonical branch `research/exp003-context-order`; one open/draft/unmerged PR #9. All 89 reserved boundary issues remain sealed.

## Original cloud artifact and independent verification

The ORIGINAL [Run360 GitHub Actions run](https://github.com/sushxnthd/lattice/actions/runs/41021665305) completed successfully at commit `25ad051df89dc97adc43437d303d8a2ce1b697f9`. Its source verification, four isolated no-network historical Jinja executions and original independent auditor all passed.

Original artifact ID `12961542894`, ZIP SHA-256 `7ecb8086ae37194a9b7b05b2d90b0913e6c0556d7dfb2c4bd2d4182d1bd6d376`, matching the GitHub-reported artifact digest. All 8 original manifest entries were independently verified. A new read-only auditor independently verified 8 historical source Git blob identities, 48 case template/expected-value identities against the separately frozen literal oracle, source variant matrix, Python/Jinja versions, statuses, original matrix and SHA manifest. Fourteen local tests passed, including thirteen adversarial evidence-corruption tests.

## Frozen public-API factorial

| Variant | Targets passed (6) | Controls passed (6) | Total |
|---|---:|---:|---:|
| Original compiler + original runtime | 1 | 6 | 7 |
| Repaired compiler only | 1 | 4 | 5 |
| Repaired runtime only | 1 | 6 | 7 |
| Both repaired production files | 6 | 6 | 12 |

**The exact prospectively frozen joint target-plus-control qualification passes.** The compiler-only variant regresses two ordinary-function-call controls because it emits `_loop_vars`/`_block_vars` that the old runtime does not accept. The complete compiler/runtime pair repairs all six targets while preserving all six controls. Casewise factorial correctness interaction is +5 across targets and +2 across controls. One target already passed at baseline; do not claim every target needs both files.

This is a finite, source-pinned historical functional necessity result, not a general Jinja theorem, unique causal-mechanism identification, or a coding-model representation comparison. The twelve cases are not independent samples for significance testing. The reference diff was used for qualification only, never for model localization. The separately authored local Run360 oracle code differs in implementation from the authoritative GitHub oracle, though its twelve frozen templates and expected outputs agree.

## Scientific status

**No new Qwen inference, model-generated repair or IR superiority claim.** **Deduplication completed:** the original Run344 cohort ledger already lists `pallets/jinja` PR #1242 as its eighth qualified PR. Run361 does not increase the cohort: eight PRs across seven repositories. The Run360 oracle was frozen before its own four-variant execution, but after earlier Jinja #1242 research, so it is not a genuinely unseen independent issue. No post-outcome retuning. Full SHA-verified local Run361 reproducibility ZIP retains the original cloud artifact, independent verifier, 14-test adversarial suite, raw matrix, report and protocol. Historical ZIP mirroring to GitHub remains incomplete.

Next: deduplicate the cohort; then prospectively freeze a tokenizer-controlled, gold-blind Jinja IR-versus-ordinary-Python/AST pilot using identical source facts, two-file authority, atomic compiler, Qwen model, isolated functional oracle, raw completion capture and independent verifier. Continue multi-repository sampling toward cluster-aware power. No changes to the 89 sealed issues.

## Run361 independent cloud replay and cohort deduplication addendum

The new [Run361 independent GitHub Actions replay](https://github.com/sushxnthd/lattice/actions/runs/41029860157) completed **SUCCESS** on commit `0487a8be4f62b185df4cc9c06155f2d197d44c83`. It downloaded the original Run360 ZIP, SHA-checked the exact original bytes, ran a separate portable verifier, and preserved its results. Original Run361 replay artifact ID `12964793846`, ZIP SHA-256 `c1c8798a405fe6f4bba4f7587be7f59ed2a38a70a9346c38cf60649a4fb602f5`; its independent gate reproduced counts 7/5/7/12 and interaction +5 targets/+2 controls.

**Independent cohort lookup resolved.** [Run344's canonical cohort ledger](../run344/COHORT_LEDGER_RUN344.json), Git blob `0731549b1455b087d20d508336b51ba9932475ff`, explicitly lists `pallets/jinja` PR #1242 as the eighth unique PR. The prior [Run344 qualification](../run344/RUN344_RESULT.md) used 6 targets and 8 controls, with 1/1/1/6 target passes and 8/8/8/8 control passes across the 2×2 arms. Run360 used a distinct 6-target/6-control oracle, and compiler-only regressed two of its new ordinary-call controls. Different control sets explain the different control outcomes; neither oracle replaces the other. Run344's reference merge commit `f71f5ebab2e76c5ee6f5f705a2703f3891e762bc` and Run360's PR head `f524bcce0cf295941fe665cbcb6846e7e9f39df5` must not be represented as the same commit. Prior Run344/345 analysis also identified ABI confounding; this remains unresolved as a general semantic-mechanism attribution. PR #1242's implementation hints were previously exposed and must be excluded from gold-blind model prompts.

**Correct cohort remains eight qualified PRs across seven repositories, zero established model repair successes from this qualification, and no representation superiority.**
