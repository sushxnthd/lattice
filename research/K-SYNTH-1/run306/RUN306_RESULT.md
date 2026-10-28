# K-SYNTH-1 Run306 — Definition-time call mutation counterexample

**Original prospective freeze:** commit `f6d2a9c4c59d192a7642962668c385be83e4b53f`, before functional execution. **Runtime:** trusted CPython 3.13.5, no model-generated code. This is not an independent real-repository repair or IR-versus-Python model comparison.

## Falsifying witness

```python
import builtins
len = lambda xs: -777
def install():
    globals()['len'] = builtins.len
    return int
def f(x: install()): pass
observed = len([0, 1, 2])  # 3 on CPython 3.13.5
```

Run305 incorrectly marked the final `len(...)` as `NOT_KNOWN_TARGET`. An arbitrary definition-time call may mutate module bindings; leaving `env['len'] = NON_TARGET` unchanged across that call is unsound. The Run306 bounded transfer conservatively invalidates known aliases after an executed unknown Call, returning explicit `UNKNOWN`, not a claimed runtime identity.

## Frozen experiment

Three sites (annotation/default/decorator) × two effects (restore/no-op) × two modes (eager/future-annotations) × 32 correlated variants = **384** trusted functional cases.

| Outcome | Run305 | Run306 |
| --- | ---: | ---: |
| False-negative MAY classifications | **160** | **0** |
| Final-call UNKNOWN_DYNAMIC | 0 | 320 |
| CPython observations matching frozen predictions | 384/384 | 384/384 |
| Independent isolated subprocess replays | — | 384/384 |

The 160 false negatives comprise 32 eager-annotation, 64 default and 64 decorator restore cases. Postponed annotations do not execute on CPython 3.13; defaults and decorators still do. Conservative UNKNOWN incurs a deliberate precision cost.

**Regression:** Reanalyzed the original 1,024 Run305 frozen cases. All previously observed builtin calls remained MAY or UNKNOWN; 896 MAY and 128 UNKNOWN, with zero definite-negative omissions. These cases and the 384 Run306 variants are correlated, not independent repair tasks.

**SHA256:** frozen sources `1ce234ff74f60224173b6b6d950f62c791b06f0d338d65ca61238525931dfd79`; raw outcomes `56d43399ac90e8687427fb30a898d87839c8f8f4408ffb0a9921bc3957ec0496`. Independent auditor checked 384 source hashes and 384 subprocess results. Local full archive SHA256 `01c23f86d9a4ea9eeaef88dc264941f5c7adc5642ebdb205623f4030d44bd65f`.

**Scope:** This repairs one concrete MAY-analysis false negative, not Python-wide soundness. Import hooks, descriptors, threads, metaclasses, other non-call effects, and dynamic runtime identity remain unsupported. **Python 3.14** changes default annotation evaluation to lazy/deferred; this code and experiment are explicitly CPython 3.13.5 scoped. Reference: https://docs.python.org/3.14/library/annotationlib.html

**Status:** Five qualified independent real repairs, no sixth, no new model inference, no powered IR advantage, no breakthrough. All 89 boundary issues SEALED. Single open/draft/unmerged PR #9. Historical full GitHub archive mirroring remains incomplete; full Run306 raw records are SHA-preserved locally.
