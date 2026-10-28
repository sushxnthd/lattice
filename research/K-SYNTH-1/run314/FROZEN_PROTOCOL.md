# K-SYNTH-1 Run314: prospectively frozen compiler-parity test

Frozen before execution on 2026-10-28 UTC. The canonical branch is research/exp003-context-order; PR #9 must remain open, draft and unmerged. All 89 boundary issues remain sealed.

## Primary question
Can a common atomic source compiler accept (A) typed semantic IR replacement and (B) an actual ordinary Python AST-constructor action, with identical source facts, authority, and verifier, and produce byte-identical edits even in the presence of multibyte UTF-8 and CRLF?

## Frozen fixtures and executable
- 1,024 trusted generated cases; 8 templates x 128 variants.
- Source JSONL SHA-256: `5bd87106b6ab13326767018d65264c9738d7bde2b2c09baa4beee485cfc3b09d`.
- Executable Python SHA-256: `76303ad14489e035d95a1714469e7ba333efd6d5b8f06f3ecdcf4646333ec839`.
- Frozen protocol JSON SHA-256: `87e90f8f8336d7f92e68d35f97e21948c3a5bb4c577c75661491e9bc7d457401`.
- Interpreter: CPython 3.13.5.
- Predeclared primary checks: 1024/1024 exact IR-vs-Python-AST output byte parity; 1024/1024 independent AST semantic oracle; source and AST-node precondition SHA verification.
- Negative control: naive Unicode character-index splice using AST UTF-8 byte offsets; count mismatches without excluding failures.
- Input source and replacement values are trusted fixture data. No untrusted model code is executed. No model inference is performed.
- Report exact failures, preserve all traces, SHA-256 manifest and independent auditor. No semantic-IR superiority claim.

The source-manifest and executable hashes are fixed before evaluating the cases. This is a compiler-contract experiment, not a real-repository repair comparison. No historical task qualifications change.
