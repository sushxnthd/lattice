# K-SYNTH-1 Run375: target-scoped noninterference certificate

**Result:** Replaced Run374's global call-graph acyclicity requirement with target-reachable acyclicity, preserving the restricted pure Boolean grammar. This recovers 88 previously UNKNOWN programs without admitting any non-total target or observed false NO_DEPENDENCE certificate.

## Frozen corpus and fresh independent replay

The original Run374 raw trace SHA-256 is `ee1022c92fd8b34493f143629f4557aca3c4a386cb32ffeeac91a095496bd76e`. It contains 1,100 self-authored two-/three-function programs, 16 producer truth tables and four Boolean inputs: 70,400 CPython outcomes.

| Verdict | Run374 | Run375 |
|---|---:|---:|
| NO_DEPENDENCE | 297 | 363 |
| MAY_DEPEND | 143 | 165 |
| UNKNOWN | 660 | 572 |
| Accepted | 440 | 528 |
| Accepted non-total targets | 0 | 0 |
| Observed false NO_DEPENDENCE | 0 | 0 |

The 88 recovered cases (66 NO_DEPENDENCE, 22 MAY_DEPEND) all contain global cycles *unreachable from target*. Accepted coverage improves by 20.0% relative (88/440). No previously accepted case was rejected.

An independent auditor, which does not import the candidate analyzer, regenerated all 1,100 source programs, computed target reachability separately, and executed **70,400 fresh CPython observations**. All fresh outcomes matched the frozen Run374 traces. All 1,100 verdicts matched the independently computed graph rule; there were zero source mismatches, zero accepted non-total targets, and zero observed false NO_DEPENDENCE certificates. Twenty local adversarial/unit tests passed.

The implementation also bounds AST depth before recursive traversal: a 1,000-unary-`not` expression crashed Run374 with RecursionError but returns UNKNOWN in Run375. Python 3.12+ generic function type parameters are now explicitly excluded.

## Scope and limitations

The corrected theorem guarantees **target totality**, not totality of all functions in a consumer module. Unreachable recursive helpers are allowed because their definitions have no side effects in the admitted grammar. The proof is topological induction over the target-reachable subgraph. NO_DEPENDENCE guarantees producer replacement noninterference only within the admitted pure Boolean fragment; MAY_DEPEND is not proof of effect, and UNKNOWN carries no guarantee.

This is synthetic-grammar validity/coverage research, **not** a new production repair, coding-model inference, powered IR advantage or breakthrough. Historical cohort remains nine qualified PRs across seven repositories. All 89 reserved boundary issues remain SEALED. Local archive contains the complete raw 70,400-outcome fresh replay, executable auditor, tests and SHA-256 manifest. Archive SHA-256: `65c3c05b8f535be358d6bd3cbe0bf3183a2bf6befe28d0d98d5e73c864211c49`.
