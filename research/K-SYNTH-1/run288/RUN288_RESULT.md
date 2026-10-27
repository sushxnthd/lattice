# K-SYNTH-1 Run288: runtime binding provenance and source-only non-identifiability

Date: 2026-10-27 IST. Canonical branch `research/exp003-context-order`; one OPEN/DRAFT/UNMERGED PR #9; 89 reserved boundary issues SEALED.

## Scientific result
Source-only Python AST cannot certify that `len` and `sum` resolve to the intended builtins without environment assumptions. A constructive witness holds the complete source, AST, bytecode, Boolean predicate and input fixed while changing only the runtime global or builtins namespace. Pristine execution yields (old=True,new=True); shadowing global len yields (False,True); shadowing global sum yields (True,False). This is an identifiability counterexample, **not** evidence of semantic-IR superiority.

## Executed experiment
Trusted fixed source SHA256 `91c5cf804e3ea167233dc4bd79192d65f9076bc32da2fe8ac54a94d05f56cd02`; seed 288; 512 finite Boolean-sequence/threshold scenarios crossed with five runtime environments. 2,560 paired comparisons, 5,120 CPython function executions and 5,120 actual `LOAD_GLOBAL` binding observations through CPython 3.13 `sys.monitoring` INSTRUCTION callbacks. The separate read-only auditor passed all 2,560 records; 13/13 local tests passed.

| Runtime environment | Pairs | Guard disagreements | Nonbuiltin loads | Disagreement flips vs pristine |
|---|---:|---:|---:|---:|
| Pristine | 512 | 103 | 0 | 0 |
| Global len shadow | 512 | 105 | 512 | 208 |
| Global sum shadow | 512 | 208 | 512 | 105 |
| Builtins len shadow | 512 | 105 | 512 | 208 |
| Builtins sum shadow | 512 | 208 | 512 | 105 |

Independent audit of Run287 archive: 13/13 SHA-256 payloads verified. Run287 scientific CI 40475919025 was still queued at latest inspection. Initial `sys.settrace` opcode events failed to fire on this runtime; preserved as infrastructure failure and replaced by working `sys.monitoring`.

## Soundness boundary
The static scanner returns `CONDITIONAL`, not an unconditional runtime-binding proof. Imports, explicit shadowing, dynamic introspection, class scopes, and unsupported mutations return `UNKNOWN`. Opcode observation assumes trusted fixed code, single-threaded CPython and stable global/builtin mappings between observation and instruction. No untrusted model-generated code was executed on the host.

## Reproduction and limitations
Local SHA-verified Run288 archive contains complete raw traces, executable analyzer, independent audit, 13 tests, manifest, failed-attempt ledger, pilot-design specification and previous Run287 archive. This run does not contain new coding-model outputs, a fifth qualified repository repair, a powered McNemar comparison or a breakthrough. Four independent qualified real issues remain: Flask PR6096, urllib3 PR5071, Werkzeug PR3136, HTTPcore PR1000. Run283 failed holdout (8/32 wrong), Run284 (72/72 correct) and Run285 (120/120 correct) remain unchanged, all within HTTPcore. Historical GitHub ZIP mirroring remains incomplete.

Archive SHA256: `57a3368c72f087671abbfcc2d6a253ff52a919783af79ceeab8029ff2c964c20`.
