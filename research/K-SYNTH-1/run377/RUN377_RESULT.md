# Run377: independent original-artifact factorial mechanism audit

Original source: Run376 four-arm GitHub Actions ZIP SHA-256 `c785739905b89d792f95d1f64d6bad8dabd7ec5812bb141ef3e29e6b029c53eb`. The independent auditor recomputes correctness from observed versus expected exceptions and empty queue, not the prior summary.

## Original functional evidence

48/48 cases parsed and independently checked. Four-arm totals: baseline 8/12, async-only 10/12, sync-only 10/12, both 12/12. Classification: 2 async-only repair cases, 2 sync-only repair cases, 8 invariant cases. All 12 casewise factorial interactions are zero. The all-tests-pass conjunction has factorial interaction +1. Six local verification/adversarial tests passed, including tampered pass labels, duplicate/missing cases and injected interactions.

## Theorem

Let `Y_j(a,s)` be binary correctness for case `j` under async and sync repair toggles `a,s`. If every case depends on at most one toggle, its second-order factorial contrast `I_j = Y_j(1,1) - Y_j(1,0) - Y_j(0,1) + Y_j(0,0)` equals zero. This follows by cancellation for any `Y_j=f_j(a)`, `Y_j=g_j(s)`, or constant `Y_j`.

Yet aggregate all-tests-pass `A(a,s) = product_j Y_j(a,s)` can have nonzero interaction. For example, two independent cases `Y_1=a` and `Y_2=s` yield `A=a*s` and `I_A=1`. Therefore aggregate two-file necessity alone cannot establish semantic cross-file coupling.

This is a casewise correctness theorem and an audit of a historically selected task, not a model advantage, powered result, or proof about all Python behaviors.

## Paired Qwen experiment

The separately frozen Run377 experiment uses original issue #670, SHA-pinned historical HTTPcore baseline `5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e`, two authorized production files, a shared atomic exact-preimage compiler, and a network-disabled historical oracle. Original attempt 41150087160 failed before model inference due to ambiguous AST exception-handler selection. Attempt 41150142389 failed before inference due to tuple-unpacking error. Both are retained as infrastructure failures, not model failures. Corrected attempt: https://github.com/sushxnthd/lattice/actions/runs/41150199531 . Its preflight source verification, prompt freeze, independent fact parity and atomic compiler accept/reject controls passed; model build/inference may still be pending. Do not claim model results until original raw completions and functional traces have been independently audited.

All 89 reserved boundary issues remain sealed. Sole open/draft/unmerged PR #9 on `research/exp003-context-order`.
## Blinding limitation

The issue was prospectively selected and frozen in Run376 before its reference patch was inspected. However, the Run377 prompt/runner was authored after that reference repair became known to the research process. The actual model prompt excludes the reference PR and its patch bytes, but **prompt exclusion is not equivalent to investigator blinding**. Treat this as a reference-excluded exploratory paired pilot, not as independent blinded evidence of IR superiority. The two arm representations also differ in derived control-flow summarization and may differ in token count; both must be audited before causal interpretation.
