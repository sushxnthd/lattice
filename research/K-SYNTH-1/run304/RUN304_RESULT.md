# K-SYNTH-1 Run304: builtin-name shadowing breaks lexical target provenance

## Prospective registration
Before executing trusted CPython witnesses, the generator and correction SHA-256, 24-template/64-seed design, 1,536-source manifest root, five expected groups and strict failure policy were committed on the canonical research branch at `1fd93f705fced84085ccb14bc0aac0679f8bbffc`. The canonical source-manifest SHA-256 is `923fa8cd7f204378dd22f7a21fa8f53cfb3cac492452c490f2fc277f7807a375`. No outcomes were used to change this protocol.

## Counterexample and correction
The inherited Run301 transfer treated an undecorated `def len(x): ...` as a candidate for `builtins.len` solely because the lexical identifier is `len`. That creates a spurious MAY-call edge: a Python `def` binds a fresh user function, not the builtin object of the same name.

```python
def len(x):
    return x[0]
result = len([7, 8])
```

CPython calls the user function, not `builtins.len`. The original analyzer reports `MAY_TARGET`; the corrected transfer reports `NOT_KNOWN_TARGET` within the bounded module-level subset. Decorated function bindings remain explicitly `UNKNOWN`.

**Bounded proof:** With no unmodeled mutation, an undecorated function definition creates a fresh function object and binds it to the identifier. That object is not identical to the pre-existing builtin `len` or `sum`. An immediate direct call through that binding therefore cannot invoke the builtin by identity. Decorator application invalidates this inference and requires `UNKNOWN`. This is not a general Python soundness proof.

## Frozen results and independent replay

| Group | Correlated runs | Original | Corrected | Actual builtin calls |
|---|---:|---|---|---:|
| User-defined `len`/`sum` shadowing | 512 | MAY_TARGET | NOT_KNOWN_TARGET | 0 |
| Direct builtins | 256 | MAY_TARGET | MAY_TARGET | 256 |
| `from builtins import` aliases | 256 | MAY_TARGET | MAY_TARGET | 256 |
| Decorator rebinding to builtin | 256 | UNKNOWN_DYNAMIC | UNKNOWN_DYNAMIC | 256 |
| Unrelated user-function controls | 256 | NOT_KNOWN_TARGET | NOT_KNOWN_TARGET | 0 |

The original experiment matched **1,536/1,536** frozen expectations. A separately implemented read-only auditor, importing neither analyzer nor the primary experiment, recompiled and executed all 1,536 SHA-pinned trusted sources, independently checked builtin `c_call` identities and return values, and found **zero discrepancies**. Exactly **512** static classifications changed, all in the frozen shadowing group. Direct/import positive controls and decorated-UNKNOWN controls were preserved.

This establishes a lexical-provenance **precision defect**, not a false-negative safety failure. The 1,536 executions are correlated variants of 24 templates, not independent repair tasks. All executed sources were hardcoded trusted templates; no model-generated code was run on the host.

## Preservation and limitations
The complete local reproducibility ZIP contains the original archived analyzers, frozen source manifest, raw 1,536-row functional traces, independent auditor, result summary and SHA-256 manifest. ZIP SHA-256: `97617e1327c3b1363c9ffd60afee5a66f747ebca01c9a0f2d20a874a32de5b18`. Source generator SHA-256: `7fe65688feeeccdf496cb36c98d789a5eb97d72f66afaeb0065f59853d3e57ef`; correction SHA-256: `974d6e01a175c1959fc2dd5b01daace7e1d27253d377b365fc919dd4ab2a96f9`.

**Status:** five independently qualified real multi-production-source repairs; no sixth, no new coding-model inference, no powered IR-versus-Python advantage and no breakthrough. Run301/303 original results remain immutable. Historical GitHub ZIP mirroring is incomplete. All 89 reserved boundary issues remain SEALED; one K-SYNTH-1 kernel and existing draft PR #9 remain.

Next: prospectively qualify a sixth independent real public-repo repair, then execute a schema-valid paired capable-model experiment with information-equivalent semantic/dataflow IR and ordinary Python/AST actions, a shared compiler and isolated oracle.
