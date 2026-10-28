# K-SYNTH-1 Run316 result (2026-10-28)

**Decision: PASS for two bounded engineering experiments; NO production-model result, NO seventh independent repair, NO IR superiority, NO breakthrough.** Both primary protocols were committed to the canonical GitHub research branch before executing their respective tests: security freeze `badac0402cb940fc0a86c76f22ee7602f5d621c2`, structural-editor freeze `031fa3aff21ef97ea6e1e5d06a96e7a6305ed86c`.

## A. Reproduced path confinement counterexample

The Run315 hardened snapshot publisher checked `store` and `store/snapshots` for symlinks but **did not inspect lexical ancestors above `store`**. A pre-existing symlink in the parent path redirects trusted writes outside the intended lexical root. This is a concrete confinement defect, not a proof of attacker exploitability in an actual deployment. All experiments used temporary directories.

Frozen results: original ancestor-symlink escape **32/32**; revised publisher rejected the same cases **32/32**. Honest concurrent same-snapshot-ID pairs **128/128**, distinct-ID pairs **128/128**, content-addressed snapshot verifications **384/384**, injected pre-pointer failure rollbacks **128/128**, `snapshots` symlink rejections **16/16**, and destination-snapshot symlink rejections **16/16**. No failures in the frozen test. The revised publisher only adds a lexical ancestry check before the previous implementation. It **does not** close TOCTOU races against malicious concurrent writers, establish power-loss durability, or make multi-file overwrites atomic.

## B. Structural multi-file editor

Implemented a pure, SHA-preconditioned multi-file AST editor supporting `insert_before`, `replace_expr`, `replace_stmt`, and `delete_stmt`. Each operation checks the exact original source SHA, node SHA, byte-accurate AST location, and edit authority. All files are validated before a new immutable mapping is returned. The editor parses/compiles syntax but never executes generated code. It does not claim semantic soundness.

Frozen 128 correlated trusted three-module fixtures (512 total edits): **128/128** byte-identical to separately specified expected source, **128/128** isolated CPython functional replays, **8/8** malformed/stale/unauthorized negative controls rejected. Independent read-only audit reconstructed expected source and output hashes for all 128 cases, with **0** discrepancies. The unmodified monolithic test harness hit execution time limits twice without a scientific outcome; the *same frozen fixture generator, compiler and isolated oracle* were executed in eight transport partitions of 16 cases, retaining all 128 raw records. Partitioning is disclosed as a postfreeze infrastructure change, not hidden or counted as a new experiment.

The structural editor has **not** yet been shown to express the complete h11 PR #115 reference, is not a production-ready transaction system, and has not been evaluated with a capable coding model. This is progress on shared editing infrastructure, not evidence that a semantic IR outperforms ordinary Python/AST.

## Next decisive work

1. Demonstrate full exact reference expressibility on at least two independent qualified multi-production-file repairs, without using reference-derived localization in model prompts.
2. Execute a paired capable open coding-model pilot with identical task facts, edit authority, compiler, oracle, token budgets, raw completions and independently verified model SHA.
3. Continue prospectively frozen independent production-repository recruitment, then power the real-repair comparison with repository-aware inference.
4. If advancing publisher security, replace lexical path checks with descriptor-relative `openat`-style confinement and analyze concurrent adversarial writers and crash consistency separately.

Six previously qualified historical repairs remain six. All 89 reserved boundary issues remain sealed. GitHub raw ZIP mirroring is not complete; the full SHA-verified evidence bundle is local.
