# Run464: Bounded AST target identity and negative controls

A non-executing verifier checks pinned source SHA, a unique top-level function identity, unchanged signature, and one literal return-value replacement. It returns explicit UNKNOWN outside the declared scope. Ten deterministic adversarial cases pass, including import-time side-effect insertion, decorator insertion, a dynamic call, and a comment-only no-op. This does not establish semantic equivalence, effect safety, model fairness, or production patch correctness. No model inference or new qualified real repair occurred. All 89 reserved issues remain sealed.

Local SHA-256 verified reproducibility ZIP: 3ae1e75aaac0d4a7658fc1a269567bc078954c819d9620728ca5ba2fbdd21157. Executable and raw results remain local pending mirroring.
