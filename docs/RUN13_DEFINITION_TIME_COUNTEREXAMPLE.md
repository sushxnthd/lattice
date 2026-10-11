# Run 13: Python definition-time effects falsify naive static commitments

Status: locally reproduced, **not** a model result or Lattice representation advantage. The implementation is not integrated.

A protected Python function's AST and direct same-module dependency closure remained unchanged while an unrelated function's decorator executed at import time and replaced the protected function's `__code__`. The naive closure checker accepted this candidate even though a controlled output changed from 2 to 1000.

Deterministic differential test (seed 20261012): 250 variants each of decorator, default-expression and annotation-expression attacks. Naive checker accepted all 750; restricted checker rejected all 750. Both accepted 250 benign unrelated changes and rejected 250 direct protected-function changes. Ten local tests passed. These are repetitions of three mechanisms, not 750 independent attacks.

**Claim update:** Static AST closure alone is not a semantic preservation guarantee for general Python. Definition-time effects and dynamic mutation must be conservatively rejected or handled by stronger verification. The restriction is representation-neutral, not Lattice-specific novelty.

No new coding-model run occurred; frozen negative Qwen results remain unchanged. Full local scripts, raw results and SHA-256 manifest are available separately; the GitHub code write was blocked. Next discriminator: other definition-time effects, then frozen Python+same-verifier vs Lattice multi-edit comparisons.
