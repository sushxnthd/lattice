# K-SYNTH-1 Run374: exhaustive short-circuit-cycle scope falsification

## Verdict

**Found and corrected a second totality-scope defect in the Run373 semantic/dataflow certificate.** The old graph traversal used Python `any` with a short-circuiting recursive visitor. When the producer edge was visited first, a recursive consumer edge could remain unvisited, causing the analyzer to accept non-total programs as `MAY_DEPEND`. A separate unreachable-cycle pattern could be accepted as `NO_DEPENDENCE`, contradicting the broad all-consumer-functions totality lemma (but not necessarily target-only noninterference).

## Direct functional witness

```python
from producer import produce as p
def target(x,y):
    return p(x,y) or target(x,y)
```

Run373 returns `MAY_DEPEND`; Run374 returns `UNKNOWN`. Actual CPython with an all-False producer raises `RecursionError` for all four Boolean input pairs; an all-True producer returns `True` for all four. The dependency graph contains a self-cycle even though `@producer` is visited first. The correction validates *all* edges and all declared consumer functions for acyclicity before any producer-reachability search.

## Exhaustive finite experiment

A frozen deterministic grammar enumerated 1,100 two-/three-function consumers (10 expressions per function). For each consumer, all 16 Boolean producer truth tables and all four Boolean inputs were executed in fresh module namespaces: **70,400 real CPython functional observations**. No untrusted model code was executed.

| Metric | Run373 | Run374 |
|---|---:|---:|
| NO_DEPENDENCE | 363 | 297 |
| MAY_DEPEND | 605 | 143 |
| UNKNOWN | 132 | 660 |
| Accepted programs with non-total target outcomes | 429 | **0** |
| Accepted programs with recursion outcomes | 429 | **0** |

Of the old accepted programs, 462 `MAY_DEPEND` and 66 `NO_DEPENDENCE` were conservatively changed to `UNKNOWN`. The independent source-graph auditor identified **660 cyclic programs**, all rejected by Run374. It replayed all 70,400 outcomes with zero trace mismatches and verified every source SHA-256. There were zero observed false `NO_DEPENDENCE` certificates within the enumerated grammar. Sixteen adversarial/unit tests passed.

## Scope and caveats

This is a validity correction, not a proof of semantic IR superiority. The earlier Run373 name-shadowing fix remains intact. The theorem is restricted to a pure acyclic Boolean two-module Python fragment; arbitrary Python and dynamic calls remain UNKNOWN. The old accepted-non-total observations must not be treated as soundness evidence. No new production repair, coding-model completion, or powered paired IR/Python comparison occurred in this run.

## Project invariants

Historical cohort remains **9 qualified PRs across 7 repositories**, unchanged. The 89 reserved boundary issues are SEALED. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole open/draft/unmerged PR #9. GitHub mirroring status is recorded separately from the local SHA-verified evidence archive.
