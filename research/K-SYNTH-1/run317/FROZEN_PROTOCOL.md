# K-SYNTH-1 Run317 prospective decorator-reattachment protocol

Frozen before executing the Run317 384-case experiment. This is a bounded **trusted synthetic structural-compiler safety study**, not a production-repair qualification, model-inference result, or semantic-IR superiority claim.

- Original compiler: unchanged `run316_structural_compiler.py` from Run316 reproducibility archive, SHA-256 `005fb330be56bc94ba4e7c8c400a609092e6aa9452a2089e8218f13b7601331f`.
- Corrected compiler: `run317_structural_compiler.py`, SHA-256 `0d412e45a296e2be56ad9b7a1a3a2c2966e4d064fefa61a0a857c3cf2a9b26c7`.
- Experiment runner: `run317_decorator_experiment.py`, SHA-256 `5de32a02124e6a6e64ce4806567e30787b7f1cb59a46cec1f1c1032ca8590294`.
- Deterministic 384 trusted Python fixtures: 256 decorated function/class/method/async-function deletion attempts, 128 undecorated deletion controls. Eight decorated families, 32 correlated variants per family; four plain families, 32 variants per family.
- Primary: count old-compiler accepted deletions that silently reattach decorators to a surviving definition; require corrected compiler reject all 256 and preserve 128/128 plain deletion controls with byte-identical results.
- Capture full original and edited source, SHA-256 source and edited bytes, AST action, original/old/new functional observations, rejection errors, independent auditor findings and archive hashes.
- All code executed by functional replay is locally generated trusted fixture code, **never untrusted model output**. Independent auditor must recompute action and functional outcomes rather than trust summary fields.
- Any failure is reported unchanged. No retroactive change to primary criteria. These correlated fixtures are not independent public-repository repairs. Six historical qualified repairs remain six, all 89 reserved issues sealed, PR #9 stays open/draft/unmerged.

The identified hypothesis is that `ast.FunctionDef`, `ast.AsyncFunctionDef` and `ast.ClassDef` node byte spans start at `def`/`class`, omitting leading decorators. Deleting only the node span can silently reattach orphaned decorators to the next definition. Conservative remedy: reject delete/replace of decorated definitions pending decorator-aware atomic editing.
