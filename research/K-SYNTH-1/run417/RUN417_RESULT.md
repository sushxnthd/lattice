# K-SYNTH-1 Run417 result: AST-equivalent edits can shift unchanged trace locations

**Prospective protocol:** [PROTOCOL_LINE_MAP_FROZEN.md](PROTOCOL_LINE_MAP_FROZEN.md), committed as `763d9b2da41a7a933a32ba23cc61e165629a6635` before the new experiment.

## Counterexample

Run416's byte-preserving compiler guarantees identical source bytes outside the authorized RHS expression span and verifies the intended AST. That does **not** guarantee stable runtime source-line locations. A multiline RHS replaced with one line moves subsequent, unchanged statements to earlier physical lines. An external `sys.settrace` observer distinguishes the original and edited program, even when both return the same integer.

This is a source-location observational counterexample, **not** a whole-program noninterference claim. [Executable minimal reproduction](run417_minimal_line_map_counterexample.py).

## Frozen results

- 384 prospectively specified source pairs: 128 LF+Unicode parenthesized multiline, 128 CRLF+tabs parenthesized multiline, 128 LF/CRLF backslash continuations.
- 768 isolated CPython executions, original versus edited. **384/384** returned identical integers and had matching expected AST structure, but the unchanged downstream statements moved to different traced line numbers.
- **384/384** paired semantic-IR versus ordinary-AST compiles produced identical bytes.
- New shared line-map guard returned explicit `UNKNOWN_LINE_MAP_SHIFT` on all 384 cases in both action languages.
- **128/128** single-line controls accepted with byte-identical representation outputs.
- Independent read-only stdlib auditor reconstructed AST spans, source hashes and line positions, then replayed all 768 executions: **11,264 checks, zero disagreements**.
- Regression and adversarial tests: **32/32 passed**.
- Raw JSONL SHA-256: `5d56497dd78cd69f7e9e0bf0b6080f12d9693f17f987e637c8b6be4bacd8edf4`.

The full 15-entry SHA-verified reproducibility ZIP is available in the conversation's Run417 artifact. The GitHub report and minimal reproduction are committed; **the full raw ZIP has not yet been mirrored to GitHub**.

## Corrected contract

The new `compile_line_stable` preflight delegates source hash, authority, bounded AST grammar and atomic patch validation to the same Run416 compiler for both representations. It rejects edits when the ordered physical line-ending byte sequences within the replaced RHS differ. This prevents the demonstrated downstream source-line drift without claiming full Python trace or semantic equivalence. Multiline-edit rejection reduces expressivity and must be measured in real repair trials.

## Scientific status

Still **two** independently qualified real multi-production-source repairs: Flask PR6096 and urllib3 PR5071. No new coding-model inference, powered IR superiority or breakthrough. All 89 reserved boundary issues remain sealed. Keep one K-SYNTH-1 kernel and the sole open/draft/unmerged PR #9 on `research/exp003-context-order`. Historical GitHub artifact mirroring remains incomplete.
