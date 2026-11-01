# K-SYNTH-1 Run408: pytest #14997 disqualified by frozen production-source gate

Date: 2026-11-01 IST. No IR superiority, powered significance or new qualified repair claimed.

## Decisive original-reference result

The independently reproduced pytest #14997 regression from Run407 is real: earlier pinned source passed 3/3 public targets, 3/3 heldout targets, 6/6 controls; regression source passed 0/3, 0/3, 6/6. Its reference qualification gate was prospectively frozen in commit f7f0f1664d50302e68b894efbd2d87a6f0c9dcd5 before viewing the fixing reference.

Issue #14997 is explicitly a duplicate of #14635. The documented fix is pytest PR #14645, fix commit fc8f56bd211128db4dd33b1a9ad42f50d9c8a3f8, merged commit a933cf5de4d64192d1d588a851ca4e76eec71efc; backport PR #14968. Independently retrieved both PR file lists and the merge commit. Each changes exactly:

- changelog/14635.bugfix.rst (documentation)
- src/_pytest/main.py (ONE production Python source)
- testing/test_conftest.py (test code)

The frozen criterion requires at least TWO changed production Python files and two behaviorally necessary production files. This is a deterministic failure at criterion 3. Do not count the test file as production. Do not run unnecessary ablations or retune the frozen criterion. **pytest #14997: NOT QUALIFIED.** The historical qualified independent real multi-source task count remains **2** (Flask PR6096 and urllib3 PR5071).

Original evidence and issue/fix provenance:
https://github.com/pytest-dev/pytest/issues/14997
https://github.com/pytest-dev/pytest/issues/14635
https://github.com/pytest-dev/pytest/pull/14645
https://github.com/pytest-dev/pytest/pull/14968

## New executable cross-module study

Built a closed-world two-module call-edge analyzer with explicit UNKNOWN for unsupported dynamic import, getattr dispatch, rebinding, changed import form, extra module functions and module getattr. Used two genuinely distinct semantic-definition and AST-statement editing interfaces, identical authority and source hashes, and the shared atomic compiler plus the independent AST liveness gate from Run403.

Original local results: **256/256 identical paired compiled sources**, **128 isolated CPython subprocesses**, **1,408 exact functional observations**, **1,536 explicit UNKNOWN cases** and **5,763 independent audit checks with zero disagreements**. Fifteen cross-module adversarial tests passed. An executable rebinding counterexample shows that replacing b.helper changes runtime results despite the static import path; the analyzer explicitly refuses this case.

This is bounded synthetic compiler validation under a fresh isolated interpreter. It is not general Python soundness, a production repair, or coding-model inference.

## New issue-first candidate

Selected pytest issue #14992 from its public description and froze its 12-case oracle before inspecting any reference fix. Local pytest **9.0.2** preflight: all 6 target variants and all 6 controls passed, 12 real isolated subprocesses, 100 independent audit checks, zero disagreements. The six variants share a structural mechanism. Exact pinned 9.0.3/9.1.1 regression comparison and reference qualification are still unexecuted. **NOT QUALIFIED**.

## Reproducibility and next run

The complete local Run408 archive contains **34 SHA-256-verified payloads**, the prior Run407 original/restored/failed-transport evidence, all new source and raw JSONL, independent auditors, tests and protocols. Clean-extraction replay passed **27/27** new tests. Archive SHA-256: 176e35a4c45fcc6fa763ac7c81cf9fdaa638534f567c69a4634a6e92879a2b73.

Next: pinned #14992 cloud baseline; issue-first real multi-source repair qualification; production-capable matched model inference with full raw outputs. All 89 reserved boundary issues remain sealed. One K-SYNTH-1 kernel, canonical branch research/exp003-context-order, sole open/draft/unmerged PR #9.
## Cloud continuation and byte provenance

The frozen pytest #14992 GitHub oracle is byte-identical to the archived local script after a metadata-only correction (installed pytest version now reported dynamically). Verified Git blob SHA-1 f0f16861395c252c4063e81f7d97ccb956850a7c. Pinned two-version cloud workflow committed at c575075e49e25fc94aca86e6974f877d96b021b3. Cloud raw outcomes have NOT yet been recovered or independently verified; do not claim the workflow passed or the candidate qualified.

The independently executable cross-module rebinding counterexample was also committed (37d48ce2); local and GitHub Git-blob hashes match 0d8de6f814a8256e41798bc991e65ab3debdd1f8.
