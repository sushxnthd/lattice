# Run 79 — prospectively frozen capable-model repair pilot (development only)
Date: 2026-10-17. Parent: Run78 independent-oracle production gate. No prior run79 inference.
## Single active kernel
| Field | Predeclared choice |
|---|---|
| Question | Does explicit semantic-IR edit notation reduce capable-model semantic repair complexity versus ordinary Python dict edits, using exactly the same framed compiler and independent oracle? |
| Current baseline | Python dictionary-of-expressions edit submitted to `parse_python_patch` and `FramedProgram.edit`, with the identical verifier, context and feedback as IR. Previous 7B public-package pilot was unsuccessful for both; not an efficacy baseline. |
| Intervention | Model returns `read = a or b`-style semantic assignment instead of Python `{'read': a or b}` expression dictionary. No extra semantic facts or privileged compiler access. |
| Matched-information control | Same initial rules, task request, trusted scope, previous source and captured-dependency context. Same model, seed, decoding, max completion budget, compiler, oracle, repair feedback and calls. Token gate: initial prompt tokens differ by <=5% of the longer prompt per pair. |
| Primary scalar | Paired difference in proportion of tasks independently correct **after at most two model calls**, fixed 256 new tokens per call. An incomplete/invalid response is a failure, not discarded. |
| Secondary | First-attempt success; calls-to-success; protected-output violations; compiler/oracle mismatches; target truth-table errors; semantic churn (# changed output/input pairs); total prompt/completion tokens; repair recovery; invalid-format rate. |
| Strongest alternative | Representation affects output formatting rather than semantic reasoning; verifier feedback, trivial tasks, model incapacity or prompt length cause apparent gains. |
| Decisive falsification | On solvable unseen multi-file tasks and at least two capable models, no repeatable IR-over-Python gain with equivalent information and identical compiler; or improvement disappears with format normalization. |
| Publishable threshold | Prospective multi-repository holdout, model-scale replication, independently audited evaluator, state-machine and same-compiler controls, bootstrap/paired uncertainty, ablations, prediction and clean reproduction. This pilot cannot reach it. |
| Product threshold | At least 10% relative reduction in median repair calls or 10 percentage-point recovery gain on real repository edits with no added forbidden-state regressions, same tool budget. |
| Kill condition | After three substantive solvable capable-model comparisons without stronger effect/boundary, drop representation-superiority claim and pivot to semantic compiler/editor. |
## Execution freeze
- Development tasks: eight bounded Boolean policy-edit tasks; **not** realistic multi-file tasks or held-out publication evidence. Holdouts untouched.
- Manifest is `research/run79/tasks.json`. Task order fixed, both arms paired on each task, Python first on even-indexed tasks and IR first on odd-indexed tasks. No post-result prompt edits.
- Model: official `Qwen2.5-Coder-7B-Instruct-GGUF` Q4_K_M, two SHA-256 verified GGUF shards, pinned llama.cpp `8bb3cf0d216a5ae48360179f2931daf284be4d01`, CPU-only public GitHub runner, seed 271828, temperature 0, top_p 1.0, 256 max output tokens, 2 turns.
- The common semantic facts and task request are identical text in both prompts; only return-format directions differ. Any token-gate failure aborts before model calls, remains an infrastructure/protocol failure, and is preserved.
- Deterministic optional removal of exactly one surrounding Markdown code fence is permitted **equally in both arms**; other model output is not rewritten. Both raw and parsed strings are preserved.
- Every attempt uses production `FramedProgram.edit`, plus independent `audit_three_way` and exhaustive target truth-table comparison; never `exec` model output. Verifier feedback is a normalized error/witness, not a representation-specific hint.
- Store raw request/response JSON and model/runner/commit/checksum provenance as Actions artifact even on failures. No paid APIs, user laptop, force pushes, merges, or secrets.
- A dry-run/tests CI gate runs before model download. Do not confuse CI success or model availability with scientific success.
## SCIENCE ledger
Run78 only verified that independent oracle tests are discovered by CI (55 passing); no representation-specific model evidence. Run79 tests that distinction prospectively. Negative/invalid responses count in the denominator.
## SYSTEM ledger
The compiler's framed protected-output behavior and independent oracle are available to both representations. This run exercises the real edit path and measures actionable repair diagnostics. It does not add cosmetic syntax.
## Backup kernels (inactive)
1. Verifier-only causal repair benefit: byte-identical Python prompts, feedback enabled versus disabled.
2. Provenance-bound semantic diff: independent source-identity verification before accepting a repaired frame.
## Smallest claim at freeze
An eight-task, two-turn, token-gated paired capable-model development experiment has been specified, not executed.
