# K-SYNTH-1 Run308: Python module-binding provenance counterexample

Frozen 2026-10-28 UTC before local functional execution. Scope: CPython 3.13.5 trusted, self-contained module-level sources. No model-generated code. This is a source-analysis soundness test, not an independently qualified repair or representation experiment.

## Question
Can Run307's source-only transfer incorrectly classify `len(...)` as definitely NOT the builtin after a local lambda shadows `len`, followed by a module-level `from builtins import len`, a `del len`, or a rebinding through an imported alias?

## Primary pre-specified endpoints
- At least one independently executed counterexample where the unmodified Run307 analyzer says `NOT_KNOWN_TARGET` but CPython calls the original builtin `len` (observed result 3 on a three-element list).
- A conservative, separately implemented Run308 binding transfer should have zero false-negative `NOT_KNOWN_TARGET` outcomes on the frozen cases, with UNKNOWN allowed and not counted as a proven success for precision.
- Record per-case original and corrected classifications, actual CPython outcome, source SHA-256, return code, stderr, and Python version; compare against an independent subprocess replay with separate source-hash checks.

## Fixtures, frozen before execution
Twelve hand-specified scenarios, 32 deterministic syntactic variants each, 384 correlated cases. Scenarios: direct `from builtins import len`; alias-as-len import; imported-len via intermediary alias; deletion exposing builtin; delete followed by local reshadow; unrelated builtin import control; unrelated builtin alias control; direct lambda control; imported `sum as len` control; imported `len as other` then reshadow; `len` function definition control; explicit `from builtins import *` uncertain. All end in a `len([1,2,3])` observation. The independent oracle uses subprocesses and CPython trace function code identity or output, with exception outcomes preserved rather than silently dropped.

## Soundness assumptions
No user-supplied code, dynamic monkeypatching of `builtins`, hostile import hooks, reflection, concurrency, or side-effecting decorators/defaults. `from builtins import len` is treated as the genuine builtin only under this frozen trusted subset. Unknown imports, dynamic effects, or wildcard imports are conservatively UNKNOWN. No Python-wide soundness claim.

## Decision rules
If any Run307 definite-negative predicts no builtin but CPython calls builtin, report a bounded counterexample. If Run308 has any definite-negative mismatch, report correction failure and preserve it; no post-outcome fixture removal. The 384 variants are correlated and must never be called independent repairs. Do not promote a sixth real repair from these tests. All 89 reserved boundary issues remain sealed.

## Infrastructure and science
Verify original Run307 Python 3.14 GitHub Actions artifact when available. If GitHub is queued or unavailable, preserve local SHA artifacts, continue source-analysis science, and retry later. Do not merge PR #9 or create another PR.
