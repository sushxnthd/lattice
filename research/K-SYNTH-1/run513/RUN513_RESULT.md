# Run513: comprehension assignment-expression binding

Executed 1,200 seeded CPython 3.13.5 differential cases (seed 513) across list/set/dict/generator comprehensions, with empty/nonempty iterables and consumed/unconsumed generators. A naive AST occurrence-as-definite-binding heuristic gave 352 false positives. A narrowly scoped rule matching eager evaluation and generator consumption had zero mismatches. This is **restricted synthetic falsification**, not a general Python soundness proof, not a model trial, and not a real qualified repair. Qualified real tasks remain two. All 89 reserved issues sealed.

Full locally SHA-verified executable code and 1,200 raw records: Run513 archive (local, not yet mirrored). The script uses CPython compile/exec only on fixed-template, internally generated programs. No model-produced code executed. GitHub CLI DNS failure remains logged locally.
