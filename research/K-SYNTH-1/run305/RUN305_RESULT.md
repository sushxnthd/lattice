# K-SYNTH-1 Run305: missing definition-time annotation calls

Date: 2026-10-28 UTC. Canonical branch: `research/exp003-context-order`.

## Prospectively frozen question

Does the Run304 bounded source-only MAY-call analyzer omit actual CPython builtin calls in function annotation expressions evaluated at **definition time**? Can a separate annotation-aware transfer correct those omissions without inventing calls when `from __future__ import annotations` postpones annotation evaluation?

The 16 trusted source templates, 64 correlated variants each, exact expected calls and source SHA-256 hashes were frozen before executing any functional witness. Freeze SHA-256: `84b15919cf471ad4feda642d535718644f9ba37816fd1e3cd71585a9ffa65933`.

## Actual executed results (CPython 3.13.5)

| Outcome | Legacy Run304 | Corrected Run305 |
|---|---:|---:|
| Frozen source variants with exact builtin-call coverage | 192/1,024 | 1,024/1,024 |
| Omitted actual builtin calls | 896 | 0 |
| False positive builtin calls in this frozen subset | 0 | 0 |
| Independent replay discrepancies | — | 0/1,024 |

The old analyzer skipped positional-only, positional, keyword-only, `*args`, `**kwargs`, and return annotations, including annotations on `async def` and a function named `len` that shadows the builtin **after** its annotations evaluate. The corrected analyzer explicitly visits these expressions, while preserving future-annotations postponement. Defaults continue to be evaluated when annotations are postponed. Two negative-control families plus the future-default family were retained.

The independent audit did not import either Lattice analyzer or the primary runner. It independently parsed all frozen sources, reconstructed expected call sites, executed each trusted source with a separate CPython `c_call` profiler, and checked every original trace and SHA-256. All 1,024 cases matched.

## Scientific interpretation and boundaries

This is a **genuine counterexample to the previous bounded transfer** and a tested correction within the stated trusted, module-level, no-unmodeled-mutation subset. The 1,024 variants arise from only **16 syntactic templates**, so they are not independent repairs, do not estimate field failure rates, and do not demonstrate general Python soundness. Dynamic annotation side effects, descriptors, nested/class scopes, Python 3.14 deferred-annotation semantics, metaclasses, and arbitrary imports remain outside this experiment. No model-generated code was executed. No new model inference was performed.

No sixth independently qualified production repair, paired capable-model superiority, McNemar significance, or breakthrough is claimed. The five previously qualified tasks remain unchanged. All 89 reserved boundary issues remain sealed. Historical GitHub ZIP mirroring remains incomplete.

## Reproduction

Run `python run305_experiment.py freeze`, verify the frozen SHA-256, then `python run305_experiment.py execute`, then `python run305_independent_audit.py`. Source is reconstructed only from the fixed trusted templates. Raw records, independent audit and SHA-256 manifest are in the local ZIP. The prior Run293/301/304 transfer files are included to make the experiment self-contained.

Next: adversarially test unknown annotation side effects and descriptor/import-time rebinding, prospectively qualify a sixth real multi-production-file issue with joint target/control necessity, and run the preflight-validated paired capable-model study using identical source facts, compiler and isolated oracle.
