# K-SYNTH-1 Run426 — prospective issue screens and reference-ablation counterexample

**2026-11-02 UTC.** No new qualified task, coding-model inference or IR superiority.

## Frozen real issue candidates

1. [Werkzeug #3007](https://github.com/pallets/werkzeug/issues/3007): issue-first frozen at pre-fix base `cb307c144e7b9092bf72b1a1dba5281e7c6ff838`, manifest SHA-256 `d932b03712c1a1a9659dc9b285e1cf4a80ea3bb2801c1f5fa007a85ecad17c18`. Four positive, two negative, five control cases were specified before fixing-reference inspection. Historical [PR #3008](https://github.com/pallets/werkzeug/pull/3008) changes only **one production source**, `src/werkzeug/routing/map.py`, plus tests and changelog. **REJECTED** under original >=2 production-file gate. Do not retune.
2. [Flask #5804](https://github.com/pallets/flask/issues/5804): issue-first frozen at issue-named base `330123258e8c3dc391cbe55ab1ed94891ca83af3`, manifest SHA-256 `d22f0c1c93dabfc880d26c48d03c23b8c282fdd595b941b3d53bc0bb5a4fa5f6`. Four positive, three negative, four controls were specified before inspecting the fixing reference. Maintainer comments identify broad architectural [PR #5812](https://github.com/pallets/flask/pull/5812) as a side-effect fix. It changes 36 files, 11 Python production sources. A pinned exact-source import-isolated oracle and leave-one-out analysis is committed in `run426_cloud.py`; [Actions 41374248574](https://github.com/sushxnthd/lattice/actions/runs/41374248574) was **QUEUED** at audit time. **PENDING**, not qualified; never count unimportable ablations as semantic necessity.

## New executable counterexample

Reference-relative source ablations do **not** prove the minimum number of source files required to repair a bug. Constructed a two-file Python example in which the reference renames `f` to `h` and changes behavior from `x` to `x+1`, updating the importer accordingly. Full reference passes the target and independent unchanged control `control(5)==25`. Reverting either reference file causes a genuine `ImportError`. Yet a one-file alternative updates the original `f` to `x+1` while leaving the original importer byte-identical and passing target and control.

The standalone [CPython witness](run426_minimal_counterexample.py) passes. A separate 256-case seeded experiment executed **1,280 actual CPython functional observations** in five isolated subprocess batches. Independent read-only audit performed **3,072 checks** with zero disagreements: all 256 base targets failed, all 256 references and one-file alternatives passed, both reference ablations failed import, and all 256 alternative bridge files were byte-identical to base. Original raw JSONL, source hashes, independent auditor and SHA manifest are preserved in the local reproducibility ZIP.

**Interpretation:** The reference-relative component gate may be useful for detecting coupled reference edits, but cannot certify intrinsic multi-file patch irreducibility or a semantic IR advantage. Do not change any original frozen outcome. Future candidates must distinguish importability, reference-relative necessity, and genuinely irreducible multi-file behavior.

**Status:** Two historically qualified real multi-production-source tasks; zero new model completions; no powered McNemar evidence or breakthrough. The 89 reserved boundary issues were not used for inference. PR #9 remains the sole draft/unmerged research PR on `research/exp003-context-order`. Historical ZIP mirroring remains incomplete.
