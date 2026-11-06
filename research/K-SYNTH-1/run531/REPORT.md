# Run531: bounded Python binding classification adversarial audit

2026-11-06 UTC. K-SYNTH-1; branch `research/exp003-context-order`; 89 sealed boundary issues untouched.

Executable local source parser (never executes input) tested 14 directed cases, all passing after correcting an initial false UNKNOWN on a purely local assignment. Local SHA-verified ZIP: d6a4df96dcc4757ec2b4428176d2f9bc0f9ae4d78ffef88996783c70a7212d38. Source SHA256 bc9be88716429ace362b8d0480e5a4ac9b02f476ec0d4fe913467c860a622c6d; raw JSON SHA256 9ab33c7dd65f696b964e92fb85dc4ec49be59cb51cc0aee518d1f9fa8ac09082.

Distinguishes lexical local bindings from module bindings; flags global/nonlocal declarations, walrus, conditional assignments, star imports, dynamic namespace access as UNKNOWN. No runtime semantic soundness claim: Python metaclasses, import hooks, and dynamic attribute mutation are not exhaustively modeled. Import binding is syntactic only. `TARGET=1; object.__setattr__(module, 'TARGET', 2)` is not proved safe by this analyzer.

No new real task, model inference, statistical superiority, or qualified production repair. Two independent qualified repairs remain. Primary priority is prospectively frozen real multi-source repairs and blinded paired model evaluation. Source/raw mirroring pending.