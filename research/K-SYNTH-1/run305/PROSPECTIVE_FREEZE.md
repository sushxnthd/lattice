# K-SYNTH-1 Run305 prospective freeze

Run304 is retained unchanged. Before executing any trusted CPython functional
witness, freeze 16 distinct syntactic function-annotation templates with 64
correlated variants each, 1,024 total. Predictions are explicit in the frozen
manifest. The primary endpoint is whether the analyzer's **MAY_TARGET** calls
cover actual CPython builtins `len`/`sum` calls at module function definition
time; record both false omissions and controls. Old Run304 analyzer is a fixed
negative comparator. Corrected analyzer visits positional-only, positional,
keyword-only, vararg, varkw and return annotations; `from __future__ import
annotations` must suppress annotation evaluation, while defaults still execute.
No arbitrary model code or third-party source is executed.

The test is scoped to trusted module-level function definitions and direct
builtin calls, not arbitrary Python soundness. The 1,024 variants are **not**
independent issue-level evidence. Preserve failures; never modify the frozen
expected outcomes to force a pass. The sixth real repository qualification and
paired capable-model comparison remain pending and are not claimed here.
