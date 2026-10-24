# K-SYNTH-1 Run215 — semantic-operation versus Python capable-model pilot

Date: 2026-10-24. Canonical repo `sushxnthd/lattice`, branch `research/exp003-context-order`, draft PR #9. **Controlled-fixture feasibility pilot, not an adequately powered real-repository result.**

## Frozen capable-model experiment

Launched Qwen2.5-Coder-7B-Instruct Q4_K_M (SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`) on two four-module Python refactoring fixtures with three conditions:

- `semantic_operation`: one high-level rename lowered by the conservative Run214 semantic compiler.
- `python_text`: ordinary Python exact-line replacements.
- `python_short_id`: ordinary Python line replacements using identical precomputed short IDs.

All arms see identical task information, source, hashes, line IDs, authorized files, seed, model, outer JSON schema, and final transaction compiler/verifier. The evaluator executes candidate code only in restricted networkless Docker, with a read-only mount, dropped capabilities, no-new-privileges, and memory/process limits. Exact prompts, raw completions, usage, compiler and functional traces, errors, seeds and model identity are retained as GitHub Actions artifacts.

**Causal limitation:** The semantic arm has a high-level action primitive whereas Python emits explicit patches. This isolates an action-granularity advantage, not intrinsic representational superiority under identical action languages. The two synthetic tasks share one import topology and differ in names/behavior; they are neither realistic SWE-rebench issues nor independent samples.

## Executed validation

Five new unit tests passed. Two trusted reference refactors compiled through both semantic and ordinary Python paths to byte-identical four-module outputs. Both trusted reference outputs passed independent CPython smoke tests, generating 12 backend replacement traces and 10 dependency edges. These are compiler and trusted-reference tests, **not** coding-model success rates.

GitHub Actions run `40071460612` started two jobs. At the initial check, both passed SHA-verified source restoration, regression tests, prospective freeze, and independent evaluator preparation; model engine compilation was ongoing. **No capable-model outputs or functional outcomes are claimed yet.**

## Next science gate

Independently audit all six actual model outputs. Move immediately to a prospectively frozen realistic multi-file cohort with independent issue-resolution tests, genuinely information-equivalent semantic IR and ordinary Python conditions, shared editing authority, and a justified paired sample size. The prior 686-pair estimate is assumption-dependent prospective planning, not observed evidence. Preserve the 89 unseen boundary issues. If Python matches/beats IR in two controlled reformulations, pivot to a rigorous negative result rather than cosmetic syntax changes.
