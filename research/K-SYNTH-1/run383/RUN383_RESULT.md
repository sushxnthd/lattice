# K-SYNTH-1 Run383: exact counterfactual dependency under bounded Python semantics

Date: 2026-10-31. Canonical branch: `research/exp003-context-order`. One draft PR #9; all 89 reserved issues sealed.

## New result

Run375 used conservative reachability: a reachable producer call yielded MAY_DEPEND and a target-reachable syntactic cycle yielded UNKNOWN. Run383 implements a restricted **exact counterfactual Boolean dependency certificate**. For admitted pure two-module Python programs, it enumerates all 16 possible total Boolean producer truth tables and all four Boolean inputs. It returns NO_DEPENDENCE if every intervention yields the same target value, DEPENDENCE_CERTIFIED with a checkable two-table witness if outcomes differ, and UNKNOWN if any intervention does not terminate or the source violates the restricted grammar. An AST interpreter never executes untrusted model code.

## Independent experimental evidence

On the original frozen 1,100-program Run374 corpus, the new certificate exactly matched **70,400 original CPython observations**. A fresh, separately implemented CPython replay executed **70,400 additional observations**, with **zero mismatches**. An independent auditor, without importing the new analyzer, verified all 1,100 verdicts and all **165 counterfactual witnesses**. All **22/22** adversarial/regression tests passed.

| Classification | Run375 | Run383 |
|---|---:|---:|
| NO_DEPENDENCE | 363 | 374 |
| MAY_DEPEND | 165 | 0 |
| DEPENDENCE_CERTIFIED | 0 | 165 |
| UNKNOWN | 572 | 561 |
| Accepted | 528 | 539 |

Of 165 prior MAY_DEPEND verdicts, **154** are now witnessed DEPENDENCE_CERTIFIED and **11** are proved NO_DEPENDENCE. **11** previously UNKNOWN programs with syntactic recursive cycles are now certified dependent because short-circuiting makes the recursion unreachable for every intervention and input. No accepted non-total programs and no false NO_DEPENDENCE verdicts occurred in the frozen corpus.

## Mechanism

```python
from producer import produce as p
def target(x,y):
    return p(x,y) or f(x,y)
def f(x,y):
    return True
```

The target is always True, despite a producer call. The prior reachability classifier returned MAY_DEPEND; the new exact classifier proves NO_DEPENDENCE. Another admitted example is `target = p(x,y) or f(x,y)` with `f = p(x,y) and target(x,y)`; the syntactic cycle is masked by short circuit, so exact counterfactual dependence can be certified.

## Scope, limitations and next step

The bounded theorem applies only to pure Boolean expressions, functions taking x/y, direct declared calls, finite aliases, and all 16 total Boolean producer interventions. It is **not** unrestricted Python soundness, a production repair, a model inference result or evidence of semantic-IR superiority. Historical qualified bug-repair cohort remains **10**. Screening of HTTPX issues #1256/#1498 did not qualify either task.

The complete SHA-verified local Run383 reproducibility archive contains executable analyzer, frozen Run374 corpus, original Run375 classifier, independent CPython replay, independent auditor, 22 tests, raw results and theorem. The next step is an independently qualified unseen multi-source bug repair, then a paired real-model experiment with information-equivalent semantic IR2 and Python/AST facts and shared atomic editor.
