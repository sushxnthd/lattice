# K-SYNTH-1 Run415: dynamic effects invalidate syntactic dead-edit pruning

Date: 2026-11-01 UTC. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole draft PR #9. All 89 reserved boundary issues remain sealed.

## Executable finding

Run402's bounded SSA-like Python graph identifies definitions in the syntactic reaching-return closure. Run403 restricts the ordinary AST-action baseline to the same closure. That is a valid syntactic property but **not a complete set of behavior-changing edits** when parameter types are unconstrained. Python `+`, `*`, and unary operators may invoke user-defined methods with side effects.

In the minimal reproducible witness, `dead = x + 1; live = x + 2; return live` returns 3 when `x.__add__` accumulates operands in shared state. Editing only the syntactically dead definition to `dead = x + 101` returns 103. The original semantic action rejects the edit (`DEFINITION_NOT_UNIQUE_AND_REACHING_RETURN`), as does Run403's fair AST action (`NOT_REACHING_RETURN`). The original unrestricted AST action accepts it. This is an **edit-authority incompleteness counterexample**, not a contradiction of syntactic def-use correctness.

## Executed finite evidence

Seed `41520261101`, five constructed families, 64 cases per family. All 320 original and 320 edited programs ran in isolated `python -I -S -c` subprocesses with raw stdout, stderr, exit code and source/program SHA-256 preserved.

| Family | Behavior-changing dead edits /64 | Original syntactic PROVEN_BOUNDED /64 | New UNKNOWN_EFFECTS /64 |
|---|---:|---:|---:|
| Overloaded addition | 64 | 64 | 64 |
| Overloaded multiplication | 64 | 64 | 64 |
| Overloaded unary operators | 64 | 64 | 64 |
| Alias plus overloaded addition | 64 | 64 | 64 |
| Bounded pure integer constants | 0 | 64 | 0 |

The independent auditor reexecuted all 640 programs, matched every raw outcome and performed **7,045 checks** with zero disagreements. Ten regression/adversarial tests passed, including trace and untrusted class-source tampering.

## Equal-authority remedy

Implemented an effect-aware semantic action front end that permits **all** assignments in the original bounded grammar, not just syntactically reaching ones. It exposes `UNKNOWN_EFFECTS` rather than asserting absence of effects. Semantic actions use unique definition names; ordinary AST actions use statement indices; both lower to the same atomic AST compiler/verifier. Across 320 paired transactions, the output sources were byte-identical and 320 isolated functional oracle runs matched expected edited outcomes. An independent AST-only parity audit performed 1,920 checks with zero disagreements. This restores action-set parity for the bounded grammar; it does not demonstrate model advantage.

Total executed CPython subprocesses: 1,602 (640 initial, 640 independent replay, 320 paired functional oracle, two minimal authority witnesses). Full source, raw traces, independent auditors, tests, SHA manifest and reproducibility archive are retained locally. The GitHub file `run415_minimal_effect_counterexample.py` is a standalone demonstration.

## Scope and limitations

The constructed families are not independent real-repository repairs or model outputs. The effect screen only recognizes a narrow exact built-in int/bool constant-expression scope; it is not a whole-Python semantic-equivalence proof. No new capable-model inference, powered IR superiority or breakthrough is claimed. Qualified independent real multi-production-source repairs remain **two** (Flask PR6096, urllib3 PR5071). urllib3 #3472/PR5093 remains NOT QUALIFIED. Full historical raw-artifact GitHub mirroring remains incomplete.

Next: issue-first prospectively frozen real repair with source-distinct heldout and joint target-plus-control component necessity, plus matched strong open-model inference on the two qualified repairs. Do not weaken qualification criteria or open another PR.
