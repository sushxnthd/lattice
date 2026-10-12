# Run 30 — evidence integrity and explainable dependency witnesses

Status: local prototype; no new coding-model inference, no hidden-test evaluation, and no representation advantage. Python and Lattice share the same verifier.

Two parallel engineering changes are under local test: deterministic shortest static dependency witnesses in the agent preflight, and an independent audit of frozen prompt bytes, raw model transcripts, token accounting, repair-message chains, and candidate-tree presence. The audit does not authenticate model weights or evaluator truth, and a passing result must never be reported as model performance.

Do not merge this research branch automatically. Preserve prior negative results and frozen evidence. Local source and tests are pending canonical integration.
