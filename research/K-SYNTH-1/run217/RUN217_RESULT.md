# Run217 — independently audited model outputs and evaluator counterexample

Date: 2026-10-24. Branch: `research/exp003-context-order`. This run does **not** claim semantic-IR superiority.

Recovered all four original Run216 artifacts from GitHub Actions runs 40076030462 and 40076071851, covering 16 raw Qwen2.5-Coder-7B-Instruct completions (two tasks × four arms × two runs). An independent local executable verified frozen prompts, hashes, model IDs, seeds, token usage, strict JSON schema, compiler acceptance, edit traces and saved networkless Docker verifier outcomes.

| Arm | Accepted (unique tasks) | Docker functional | AST rename contract | Completion tokens |
| --- | ---: | ---: | ---: | ---: |
| Semantic operation | 2/2 | 1/2 | 1/2 | 100 |
| Python semantic tool (same edit authority) | 1/2 | 1/2 | 1/2 | 106 |
| Python exact-line | 2/2 | 0/2 | 0/2 | 858 |
| Python short-ID | 1/2 | 1/2 | **0/2** | 854 |

**All eight repeat task-arm completions were byte-identical** across the two runs; the repeats are not independent replications. Exact two-sided paired McNemar p-values were 1.0 for semantic operation versus each baseline. Two closely related synthetic tasks provide no representation-science evidence.

**New evaluator counterexample:** The Python short-ID patch that passed Docker tests in task 1 retained unreachable `return validate_payload(y)` after an earlier `return check_payload(y)`. It passes the original return-value tests but violates the stronger reference-cleanliness contract. The original primary result is unchanged; the stricter AST check is a clearly labelled retrospective diagnostic. Added a reusable independent static evaluator and regression tests for stale references, wrong public names, imports and attributes. This static oracle supplements, but cannot replace, functional evaluation.

A new locally frozen real-repository matched-view pilot uses two prospectively selected discovery issues (`googlefonts__ufo2ft-930`, `spikeinterface__spikeinterface-2775`). It uses losslessly equivalent typed semantic-node JSON and annotated Python source views, identical compiler and exact-text edit authority, and a shared gold-blind retriever. Source code, tests, freeze manifests and complete original model artifacts are preserved in the Run217 reproducibility archive. The real-issue pilot has **not yet produced model outputs or independent functional resolutions**; no superiority claim is made. Its runner and workflow still require GitHub persistence.

The prior assumption-dependent sample-size target remains ~686 paired real issues under repository ICC 0.5, 30% discordance and 65% IR wins among discordances; only 391 discovery issues are frozen. Next: persist and execute the real-issue runner, recover raw outputs, integrate independent functional issue evaluation, and freeze unseen-boundary predictions.
