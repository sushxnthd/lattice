# K-SYNTH-1 Run290: pre-execution frozen temporal predictions

Status: **FROZEN BEFORE ORACLE EXECUTION**. Do not change this commitment after observing functional results.

- Frozen predictions JSON SHA-256: `ccfe66f7d7096eeda297a8a08ad3aec6da9033dcebd32e63b9fd7d45e275d6e6`
- Freeze generator source SHA-256: `306ce8ecb3533953fa18aa4380ab7db7ae740b6ea30acff17491408bed65bbbc`
- Independent oracle source SHA-256: `55316d57b80f22d32812222f7f9a7f4050a954c5b4f8d9109dc41312176487a9`
- Six fixed CPython 3.13 mechanisms, 256 seeded value variants each, 1,536 frozen predictions; **six semantic templates, not 1,536 independent issues**.
- Seed: 290271027. Modes: eager_annotation, future_annotation, lazy_type_alias, lazy_type_param, forced_alias_before_rebind, forced_param_before_rebind.
- Prediction: eager function annotations evaluate at definition; postponed future annotations do not execute the expression; lazy aliases and generic bounds resolve the then-current binding at first force and cache the result.
- No model-generated source is executed; trusted templates only. No claim of general Python soundness or representation superiority.
- Original failed Run289 CI `40486504311` remains an authentic failure: first child symtable was an unrelated lambda, yielding `KeyError: len`. Corrected witness committed as `0897afc3bd2dedca07c4c97c4edf4ad0945e6c2c`.
- Canonical branch `research/exp003-context-order`, draft/unmerged PR #9. All 89 reserved boundary issues SEALED.

The frozen JSON, independent oracle, raw outcomes and SHA manifest are retained in the local reproducibility archive. Results are to be committed separately after execution.
