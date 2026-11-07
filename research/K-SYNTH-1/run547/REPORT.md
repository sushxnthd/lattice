# Run547: restricted binding abstract interpretation

Exhaustive differential test of 341 synthetic CPython programs (0–4 statements, alphabet A/T/F/N). A two-state powerset analysis overapproximates both literal-boolean branches. Results: 220 DEFINITE, 5 UNBOUND, 116 UNKNOWN, zero unsound definite/unbound predictions. Flow-insensitive AST assignment inventory fails for `if False: x=1`.

Scope: trusted synthetic restricted grammar only, not Python-wide soundness. Initial harness included deletion of unbound x, raising an exception; deleted that case from the restricted grammar before enumerating the reported experiment. No production repair, no model inference, no superiority claim. All 89 reserved tasks sealed.

Local reproducibility archive SHA256 `1d309f6f7296d24e6794027679465d069d97343ad2663f903ff821922cd7036c`; full source and raw data GitHub mirroring pending.
