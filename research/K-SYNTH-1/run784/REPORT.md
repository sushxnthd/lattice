# Run784: conservative syntactic MAY-dependency scope

2026-11-20 UTC. Experimental code is retained locally in SHA-verified archive.

An AST-only analyzer over an explicit subset of Python expressions returns CERTIFIED with a syntactic MAY-dependency overapproximation, or UNKNOWN for unsupported syntax. This is not minimal semantic necessity: `a and False` mentions a syntactically yet does not depend on it for Boolean a. Arbitrary Python object overloading breaks purity; certification is restricted to primitive immutable bool/int domains and requires exception semantics to be specified for deployment.

Proof sketch: structural induction over literals, names, and supported pure operators shows all dependencies are included in the union of child free-name sets. Unsupported nodes refuse. Local deterministic tests: 8/8 passed, including calls, attributes, comprehensions, conditional expressions, chained comparisons, unbound names, and future-import refusal.

Local archive SHA-256: c4b41ca176236e7e0485e7da833e6c6c0920d97ef8a608102ce2256dc4d7810d. No real repair qualification, model inference, or comparative superiority evidence. No kernel, PR state, or reserved issue changes.