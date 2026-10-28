# K-SYNTH-1 Run319 — Explicit decorator-span editing and Run318 recovery

**Date:** 2026-10-28 UTC. **Branch:** `research/exp003-context-order`. **PR:** #9, draft/unmerged. All 89 reserved boundary issues remain sealed.

## Prospective scientific result

Frozen protocol committed before execution at `5d34b10084a9f43374fc52c4607140e260347cc2`. Run317 found that deleting a decorated declaration at the ordinary FunctionDef AST span can silently attach its decorator to the next surviving declaration. Run319 implements explicit `delete_decorated_stmt` and `replace_decorated_stmt` actions with source and node SHA-256 preconditions, line-anchored decorator verification, contiguous decorator blocks, path authority and collision checks. Ordinary decorated `delete_stmt` and `replace_stmt` remain fail-closed. Only trusted synthetic fixtures were executed.

Frozen 8 × 32 matrix: **256/256 exact decorated deletions**, **256/256 exact decorated replacements**, **128/128 ordinary undecorated parity controls**. Independent read-only byte-span reconstruction: **256/256**. Independent isolated CPython subprocess replays: **768/768** (original, deleted and replaced), with zero discrepancies. Structural families cover one/two decorators, multiline decorator calls, classes, async functions, methods, Unicode preceding source, nested scope and CRLF. These cases are correlated and do not represent independent repository repairs.

## Negative-control correction, preserved without retuning

The first negative-control run failed its own `def disposable(): return 1; x=2` test expectation. In CPython `x=2` belongs to the function's one-line suite, not to a sibling statement; deleting the function legitimately deletes both. The invalid original test and failure log are retained. A separately labelled postfreeze addendum was committed at `1f18936c8c02a255cf6ae02dd16fd388237e12dc`, before rerunning with a genuine trailing inline-comment control. **16/16 postfreeze negative controls rejected**, including ordinary decorated edits, stale SHA, unauthorized paths, collisions, comment/blank gaps, invalid replacement shape and invalid UTF-8. This is not claimed as an untouched frozen negative-control result.

## Original Run318 cloud artifact recovered

[Original GitHub Actions run](https://github.com/sushxnthd/lattice/actions/runs/40703329939) completed **SUCCESS**. Original artifact ID `12822619414`, ZIP SHA-256 `80a0aaaf401739c65edb150698031f2763e9628b76dffe5b97d4b0153093e469`. Its raw-result SHA-256 is `b883ec1e82be5dff5593f2d3ce1880d2e7cc0ecd41e575594d27ef97233ecff5`. The original cloud result reports five AST `replace_expr` actions reproducing the exact historical urllib3 PR #5071 production-source reference across three files. Run319 independently verified the original ZIP hash, four entries, result hash, schema and internal head/patched hashes. It did **not** independently reexecute the upstream source in Run319. This is reference expressibility, not model repair success.

## Preservation, limitations and next work

Executable [compiler](run319_decorator_compiler.py) and [smoke test](run319_smoke_test.py) are committed and independently Git-blob-SHA verified against locally tested files. Complete raw primary traces, original negative failure, independent audit, tests, exact SHA manifest and original Run318 artifact are preserved in a local 18-entry reproducibility ZIP; full large-artifact GitHub mirroring remains incomplete.

Six independently qualified historical repairs remain six. No new capable-model inference, powered IR advantage, seventh repair or breakthrough. Run320 priority: independent real-repair recruitment, a genuinely paired capable-model IR vs information-equivalent Python/AST-action experiment on qualified tasks, and adversarial multi-file/comment-boundary testing.
