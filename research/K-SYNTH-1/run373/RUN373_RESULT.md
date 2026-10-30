# K-SYNTH-1 Run373: Totality hole in the scoped MAY-dependence certificate

Date: 2026-10-30 UTC / 2026-10-31 IST. One K-SYNTH-1 kernel, 89 reserved boundary issues sealed.

## Original counterexample
The Run369 portable analyzer classified the following consumer as `NO_DEPENDENCE`:

```python
from producer import produce as p
def x(x,y):
    return False
def target(x,y):
    return x(x,y)
```

Actual CPython execution raises `TypeError: 'bool' object is not callable` on all four Boolean inputs, because the formal parameter `x` shadows the module-level function. The same failure occurs for `y` and imported aliases named `x` or `y`. Thus the original claimed **accepted pure total language** was too broad. This is a totality/domain flaw, **not** an observed false-negative Boolean-output dependency certificate.

## Corrected certificate
`run373_portable_certificate.py` conservatively returns `UNKNOWN` for any direct `ast.Call` whose callee identifier is `x` or `y`, while preserving the original Run369 implementation and its immutable evidence. The revised bounded totality and noninterference proof follows by induction on the pure expression grammar and acyclic call graph, with local Boolean arguments excluded from callable identifiers.

## Executed evidence
1,024 deterministic generated two-module consumers plus 7 adversarial/positive controls; baseline plus all 16 Boolean truth-table producer implementations; four Boolean inputs. **1,031 programs, 70,108 actual CPython input observations**, independently replayed from a clean extracted archive.

| Metric | Original | Corrected |
|---|---:|---:|
| NO_DEPENDENCE | 694 | 597 |
| MAY_DEPEND | 239 | 154 |
| UNKNOWN | 98 | 280 |
| Accepted non-total programs | **121** (62 NO, 59 MAY) | **0** |

No observed changed outputs under a corrected NO_DEPENDENCE certificate. Twelve local tests passed; independent auditor verified all 1,031 source hashes, 70,108 outputs/exceptions, classification counts, and evidence-tampering tests. This does not establish general Python soundness or any model-representation advantage.

Local SHA-verified 13-entry reproducibility archive: `lattice_run373_scoped_totality_counterexample_and_replay.zip`, SHA-256 `1b1ee262245ed6fe2aa05236d9efbadc3bc8e529718b2bfe5e263ec220792e02`. Full raw JSON remains locally archived; GitHub raw ZIP mirroring is incomplete.

**Status:** 9 historically qualified PRs across 7 repositories, unchanged. No coding-model inference, powered IR advantage, or new production repair. PR #9 remains the sole open draft unmerged PR. All 89 reserved issues sealed.

**Next:** Reference-blind two-production-source issue with prospectively frozen exact source/oracle; controlled strong no-cost real-model IR versus information-equivalent Python/AST pilot with shared atomic compiler, isolated oracle and raw completions.
