# K-SYNTH-1 Run418: real-repair compiler coverage failure and line-trace counterexample

Date: 2026-11-01. Branch `research/exp003-context-order`; sole PR #9 remains draft/unmerged. Frozen capability-audit protocol committed first at `225636f6da8270f676be04b469fbb5c9347964cf`. This is **post-reference** analysis, not a blind repair trial.

## Primary scientific result: neither qualified reference patch is expressible

The actual Run416/417 shared compiler accepts only bounded arithmetic RHS changes to unique straight-line assignments inside top-level, undecorated, unannotated Python functions. It cannot edit conditionals, imports, call arguments, nested assignments or multi-statement changes. This differs from earlier broader byte-span editors; old gold-expressibility claims must not be transferred to the new compiler.

Exact upstream reference changes were inspected against pinned source:
- [Flask PR6096](https://github.com/pallets/flask/pull/6096): base `514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b`, reference `05e9c6bd630ecf4ec0ec884b1fc7901663737bc7`. Six production change sites: import, assignment-structure, conditional, nested RHS and two call arguments.
- [urllib3 PR5071](https://github.com/urllib3/urllib3/pull/5071): base `f4e4bc31f40f8c94c6a1f1685df28f97ff48c305`, reference `f5cf122346141b187cca0db6e6445297d336b610`. Five production change sites, all conditional tests.

**0/11 reference sites eligible; 0/2 exact reference repairs expressible.** Seven paired compiler witnesses produced five equal-language rejections and two positive RHS controls (including one demonstrating that the original import remains untouched). The site catalog is a manually transcribed PR-diff audit checked against pinned base excerpts, not a full automated tree-diff reconstruction. This does **not** establish that every alternative correct repair is impossible or change the two historical benchmark qualifications. It does establish a critical validity gate before any claimed paired functional coding-model study using this compiler.

## Secondary executed experiment

An alternative shared atomic RHS compiler preserves the ordered physical line-ending bytes inside each authorized edit span. On the 384 Run417 multiline cases rejected by the previous line-map guard, it accepted **384/384** and produced byte-identical semantic-IR/ordinary-AST outputs **384/384**. Return values and unchanged downstream trace events matched **384/384**, but full `sys.settrace` line-event sequences differed **384/384**. Physical line-map preservation is **not** full trace preservation.

An independently seeded 128-case unseen set reproduced equal compiler outputs and downstream trace-event parity **128/128**, with full trace differences **128/128**. Sixty-four overloaded-operator tests demonstrated behavior-changing edits to syntactically dead RHS expressions. Two in-span comment tests were explicitly rejected as `UNKNOWN_COMMENT_IN_RHS`.

Independent read-only audit reexecuted 768 original-grid plus 256 unseen-grid CPython subprocesses; 6,148 + 768 checks, zero disagreements. Generation runs executed 768 original-grid and 384 unseen-grid subprocesses, including 128 effect executions. **50 inherited/new tests passed.**

## Decision

The qualified real multi-source repair count remains **two**. No new model inference, powered semantic-IR advantage, unseen real repair, or breakthrough is claimed. Full SHA-256-verifiable local evidence includes exact scripts, raw JSONL, independent auditor, source witnesses, summaries and 50-test suite. Historical GitHub raw artifact mirroring remains incomplete.

**Run419 gate:** build and independently verify a realistic multi-file atomic editor with equal IR/AST authority over if tests, call arguments, imports and nested edits before matched open-model functional inference. Keep all 89 boundary issues sealed.
