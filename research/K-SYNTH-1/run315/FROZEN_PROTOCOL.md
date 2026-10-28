# K-SYNTH-1 Run315 prospective protocol

Frozen before running the primary experiment. Synthetic engineering validation only, not model performance or independent repair qualification.

## Hypothesis and contract
A bounded multi-file Python constant editor using UTF-8 AST byte offsets, exact source SHA-256, exact AST-node digest and explicit per-path authority will either reject a transaction without producing any partial patch, or return a complete snapshot with six edits across three files. Semantic-IR and literal `ast.Constant(value=INTEGER)` constructor frontends must produce byte-identical output with identical facts and authority. A prepublication injected failure must preserve the prior snapshot pointer.

## Frozen sample and criteria
384 correlated deterministic synthetic cases, each with three trusted modules and two edits per module. Seed 3151028. Criteria: 384/384 IR-vs-AST parity; 384/384 prepublication failures preserving old pointer; 2304/2304 edits; independent byte-span auditor and trusted functional execution; zero negative-control accepts. Preserve failures.

## Frozen source hashes
- `run315_multifile_compiler.py`: `9031621afe53a3d26c961a3a93cbe718730c10f4d327867f014c1ff806f466fe`
- `run315_snapshot_store.py`: `ef1057bc742b427c45e74523c72cc446b30e81227ba649d2f41fbcbbd122b5cb`
- `run315_experiment.py`: `e74aa4d631e6a41ec8a69a12f55186f27899b6a4a3b4dc68cc1ccff9c99d2d7e`
- `frozen_cases.jsonl`: `4eb549ac02991a2b2298b6bcf81093702179f429c8d84c25c6ced3e74d31bc14`

## Limitations
No production-repository repair, model inference or superiority claim. Snapshot-pointer atomicity only for readers resolving CURRENT once; independent file overwrites are not atomic. No general filesystem crash-consistency proof. Correlated synthetic variants are not independent issues.