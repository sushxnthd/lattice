# K-SYNTH-1 Run190: branch identity and hidden history counterexamples

Two authorized forks can share the same ordinal root IDs and the same shallow gate/endpoint source and numeric bindings, yet compute different functions because their captured ancestors differ. Across 258 unchanged frozen base graphs, each pair had 32 distinguishing Boolean inputs (8,256 witnesses total); protected outputs remained invariant.

A second counterexample: edit gate to `a`, then to `b`, versus edit gate directly to `b`. All current roots have the same transitive content identities and behavior, but the first history contains two additional immutable nodes. A root-only snapshot hash aliases these states on 258/258 bases. First-class historical handles therefore require a full historical-node commitment and an epoch-to-root log. Version identifiers must be branch/epoch qualified or recursively content addressed.

Reference implementation and raw records are preserved in the local Run190 archive. These are finite Boolean representation-soundness counterexamples, not capable-model evidence. The frozen 258-pair model comparison remains unexecuted.
