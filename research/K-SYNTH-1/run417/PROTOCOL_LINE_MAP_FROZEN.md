# K-SYNTH-1 Run417 prospective line-map and trace counterexample protocol

Frozen before executing the new Run417 experiment, on 2026-11-01.

Hypothesis: Run416's lossless RHS compiler can preserve every byte outside the authorized AST expression span and preserve expected AST structure while shifting the runtime source-line locations of subsequent unchanged statements. A source-location-aware observer (sys.settrace) will distinguish original and edited code even when the function's integer return value remains unchanged.

Independent test families (not selected on outcomes):
- 128 seeded parenthesized multiline RHSs with LF and Unicode header/comments;
- 128 seeded parenthesized multiline RHSs with CRLF and tabs;
- 128 seeded backslash-continued RHSs with LF or CRLF.
For each, execute original and legacy Run416-edited functions with a CPython line tracer in an isolated subprocess, compare the line numbers of the unchanged 'live' and 'return' statements, and record AST fingerprints, exact raw stdout/stderr, source SHA-256 and compiler receipts.

Intervention: a source-line-stable wrapper around the same Run416 compiler. It must return explicit UNKNOWN_LINE_MAP_SHIFT before committing an edit if a replaced RHS span changes the exact sequence of physical line-ending bytes. It must accept 128 single-line controls and produce byte-identical semantic-IR versus ordinary AST-action outputs under the same authority and shared compiler.

Independent auditor must reconstruct old and new expression spans from AST, recompute source-line deltas without trusting compiler receipts, verify source SHA-256, parse raw CPython trace outputs, and assert the guard rejects all affected multiline cases. Regression tests must cover both action languages, CRLF, Unicode, all-or-nothing and unchanged controls.

This does NOT establish semantic noninterference, complete Python soundness, a model effect, or real-repository repair qualification. All 89 reserved boundary issues remain sealed. No model inference or superiority claim.
