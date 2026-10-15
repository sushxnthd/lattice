# Run 52: independent bounded lowering audit

## SCIENCE
Active kernel: Does semantic IR reduce repair complexity beyond identical Python facts and identical compiler/verifier? The primary model experiment remains UNTESTED. The strongest control is ordinary Python with the same frame/compiler. No model-gain claim is supported by this run.

### Frozen earlier representation evidence inspected
Successful structured-topology control at commit 60e2c906d9db6a2c4379310ebb76c2bf93830895, GitHub Actions run 38458512860, artifact 11843859936, zip SHA256 2f057f77aeb40115f1998d2980861e461256e305c829bd3779c17c54e2ccb809.
Dev: neutral partition 60/72 (83.33%) vs strong prose 33/72 (45.83%).
Fresh holdout: neutral partition 60/72 (83.33%) vs strong prose 19/72 (26.39%), a 56.94-point difference. Both conditions: zero perfect programs on holdout. Mean holdout prompt tokens: neutral 249.67, prose 245.17 (within 5%). This is a positive representation-format foothold on six synthetic domains, NOT evidence of an IR-specific causal advantage over identical Python plus verifier and NOT a breakthrough.

Original workflow run 38458205402 failed its pre-generation token budget gate (211 versus 252); no model output on that attempt. The permitted prose-only token correction preceded run 38458512860. Do not treat opened holdout as fresh again.

### Interpretation
Hypothesis: structured action partitions improve small function generation versus prose at approximately matched tokens.
Prediction: neutral partition > prose on a new six-domain holdout.
Observed: +56.94 percentage points on 72 correlated hidden cases; no perfect programs.
Surprise: effect exceeds the earlier violation-normal comparison, weakening any claim that negative-polarity constraints are uniquely responsible.
Alternative explanations: generic table formatting, action partition, model-specific training distribution, small synthetic tasks, generated code truncation, and correlated tests.
Uncertainty: six independent domains, one model, no independent artifact-level rescoring yet; 72 test cases are NOT 72 independent tasks.
Next discriminator: identical verifier/compiler Python-versus-IR multi-turn repair on realistic tasks, matched facts and tokens.
Belief: KNOWN (frozen run result); ANOMALOUS (magnitude); UNTESTED (generalization and IR-specific effect).

## SYSTEM
Added src/lattice/lowering_audit.py, an independent AST-based interpreter for emitted bounded Boolean Python plus exhaustive frame checks. It records changed output/input pairs (semantic churn), protected regressions, lowering mismatches, and first witness without executing the emitted code. This is CAPABILITY-BUILDING, not scientific validation. The production frame/compiler remains available to ordinary Python control arms.

### Limitations
Finite Boolean functions only; default maximum 12 inputs; independent lowering interpreter but not independent target oracle; audit does not establish user intent, model effectiveness, or arbitrary Python safety.

### Next
Verify new audit in CI, test intentionally corrupted lowering, and integrate it as an identical post-generation measurement in both Python and IR arms. Preserve all prior frozen artifacts and nulls.
