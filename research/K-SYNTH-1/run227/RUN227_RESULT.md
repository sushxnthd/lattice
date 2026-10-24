# K-SYNTH-1 Run227 — PyBaMM partial-solve oracle counterexample (2026-10-24)

**Research kernel:** independent functional validity of the frozen Run225 two-method experiment. **Inference:** no new capable-model completions. This is a post-freeze *secondary diagnostic* and does not alter Run225's registered eight-case endpoint.

## Upstream witness and counterexample

Pinned PyBaMM commit `c3def31a04df163769851733657d9b49b3700bca`, `pybamm/batch_study.py`: `BatchStudy.solve` assigns `self.sims = []` *before* the simulation loop, and appends each `sim` only after completing its solve. Consequently, the object can have `sims=[]` or a partially populated list when a solve is incomplete. See [upstream pinned source](https://github.com/pybamm-team/PyBaMM/blob/c3def31a04df163769851733657d9b49b3700bca/pybamm/batch_study.py).

The Run225 reference positive control guarded BatchStudy with `if not hasattr(self, "sims"): raise ValueError(...)`. It passed all eight old oracle cases, but **presence of the attribute does not establish a solved simulation**. On empty, one-unsolved and partially solved lists, with both cached and uncached plotting, the old reference incorrectly permits GIF creation.

## Independently executed expanded evaluator

A *separately versioned*, 16-case CPython necessary-condition evaluator checks six BatchStudy states (absent, empty, one-unsolved, partial, solved, multi-solved), each with cached/uncached plot, plus four Simulation cases. Both controls are accepted by the same frozen Run225 two-file compiler; the difference is behavioral, not syntactic.

| Two-file patch | Frozen eight-case oracle | Expanded sixteen-case oracle |
| --- | ---: | ---: |
| Run225 reference positive | 8/8 | **10/16** |
| Corrected reference guard | 8/8 | **16/16** |
| Guard missing empty-list check | 8/8 | 14/16 |
| Guard missing partial-solve check | 8/8 | 12/16 |
| Wrong exception mutation | 6/8 | 8/16 |
| Duplicate-GIF mutation | 6/8 | 12/16 |

Corrected BatchStudy guard:
```python
if (not hasattr(self, "sims") or not self.sims or
        any(getattr(sim, "solution", None) is None for sim in self.sims)):
    raise ValueError("Not solved")
```

The corrected guard is a *necessary-condition reference for this reduced snapshot*, not a proof of complete PyBaMM correctness or a production-ready upstream patch. The source-level `BatchStudy.solve` witness supports empty and partially populated `sims` as meaningful intermediate states.

**Validation:** 22 local tests passed (6 new Run227, 11 frozen Run225, 5 Run226 power tests). Full local archive preserves the exact frozen fixture, compiler, independent evaluator, expanded evaluator, 16-case traces for all controls, tests and SHA-256 manifest.

## Scientific consequence and decision

The old reference's 8/8 positive-control score is a **false positive** for the stated issue, even though all eight previously chosen negative mutations were killed. The Run225 primary endpoint must remain frozen and separately reported, but its positive-control calibration is insufficient to justify scaling. The next *prospectively frozen* functional model comparison must include the expanded oracle, repository-level tests, and a broader realistic multi-file issue cohort; do not pool these post-hoc cases with Run225 primary scores. No representation superiority or capable-model success is claimed.

**Persistence:** report committed on the existing `research/exp003-context-order` branch and PR #9. Full executable bundle preserved locally; if remote code upload is blocked, record it and retry without pausing research.
