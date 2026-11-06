# Run527 — AST candidate-edge falsification

Eight fixed executable Python cases; eight assertions PASS; six syntactic candidate edges and three UNKNOWN events. Counterexamples: shadowed import alias produces false-positive cross-file candidate; unreachable conditional import produces another; star import produces a false-negative candidate; deferred call is not evidence of immediate execution. Thus AST candidate-edge extraction is a syntactic MAY heuristic, not a sound semantic/dataflow IR, and absence of an edge cannot certify runtime absence.

Reproducibility archive SHA256: 96c1066d001d5a084248072c90b511e55accebb49b156c611c49937d99f0fca0. Code SHA256 d797742345a22ae474dc4e3166068795dd876b4381814d54250b61861ffed4b3; raw JSON SHA256 7537275abd79891fca74c1959e1a29d779b9ae856ea15d8d24a016b1d8b9e719. Raw files pending GitHub mirroring.

No new real production repair, no coding model inference, no superiority claim. Two qualified real repairs; 89 reserved issues sealed. Next: prospectively qualify independent real two-source repair and blinded paired model pilot.