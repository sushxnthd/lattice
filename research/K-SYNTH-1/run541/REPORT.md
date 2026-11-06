# Run541: file-closure versus environment-closure counterexample

Five of five executable assertions passed. The experiment independently constructs a three-file Python program whose output changes when an external data file changes, while a complete three-file snapshot restores the original output. It then shows a distinct counterexample: two executions over identical file bytes produce different outputs solely through a changed environment variable. Thus a complete observed file inventory is insufficient for deterministic oracle replay without an execution-environment contract. This is a synthetic reproducibility result, not a qualified real repair, an OS-level isolation proof, or evidence of IR superiority.

Reproduce with `python experiment.py` in the local SHA-verified archive. Raw outcomes are in `raw.json`. No reserved benchmark issue was accessed.

Archive SHA256: `e61f340e0a9e6464d661e2a67bd853e0974e1eeb8ede9b52f38cc449b4a46f40`.
