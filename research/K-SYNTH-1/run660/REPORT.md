# Run660: finite-state descriptor observation audit

Executed synthetic Python descriptor experiment over all 340 action sequences of length 1–4 from `read`, `mutate`, `delete`, `assign`. 137 sequences distinguished `full` from `add_parent_only` by public values/exceptions. Shortest witnesses: `(read, assign)` and `(assign, read)` at length 2. Inherited read-only `property` rejects assignment; child `cached_property` permits it. Freshness requires `read, mutate, read`. These are potential observation differences, not independently justified upstream repair targets. No real upstream execution, no new qualified production task, no coding-model inference. Qualified count remains two; 89 reserved tasks sealed.

Local complete SHA-verified archive `lattice_run660.zip` SHA256 `acb8b6c5458a37795f6c74ce59a6695016047833dcd69dc348bd790a90dbcbdb` contains experiment.py, raw.json, stdout.txt, REPORT.md, manifest.json. GitHub code/raw mirroring outstanding.
