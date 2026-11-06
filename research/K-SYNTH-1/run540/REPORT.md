# Run540: dynamic import and data dependency closure

Six assertions passed. The entrypoint SHA remained unchanged while changing an untracked payload changed output. The entrypoint AST static-import inventory omitted the dynamically imported helper. Copying only the entrypoint failed; copying the complete three-file snapshot restored baseline output. This demonstrates that a static-import-only snapshot is not generally a complete execution closure. No untrusted model code executed. Synthetic experiment only; no real repair qualification or model inference.

Limits: this does not establish isolation or complete dynamic dependency discovery. All 89 reserved issues untouched.
