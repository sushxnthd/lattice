# K-SYNTH-1 Run621: bounded AST evidence with explicit UNKNOWN

This is a conservative, reproducible analyzer artifact, not an independently qualified production repair. Twelve syntactic examples were parsed and emitted as raw records. All 12 receive `runtime_dispatch=UNKNOWN`: the AST alone cannot certify executed call target, particularly under dynamic import hooks, rebinding and namespace mutation. This avoids the invalid inference that an import edge proves invocation. The analysis does not certify semantic/dataflow IR superiority and is not a model comparison. All 89 reserved issues remain sealed. Qualified real production repair count remains two.

The current highest-value unresolved experiment is a prospective frozen isolated oracle for a new independent multi-production-source repair, followed by source- and authority-matched Python/AST versus semantic IR paired inference. The static cases here are a bounded supporting tool only.

Local ZIP SHA-256: `738d2fad17873429ecbe6863978069c2ea786ce10e1092b265f20e0fe53a1e24`.
