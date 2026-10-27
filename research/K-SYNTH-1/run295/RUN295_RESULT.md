# K-SYNTH-1 Run295 | CPython source-loader validity regression

Date: 2026-10-27 IST. Canonical branch research/exp003-context-order, single open/draft/unmerged PR #9, 89 reserved boundary issues sealed.

## Frozen chronology

The prospective 12-case protocol was committed BEFORE local execution at ff b15236 (full SHA ff b15236 with spaces removed: ffb15236f0b22370698c2cd2c5516e76b83ea70b). Freeze blob fcb5f18a427298c9b853d38dda5292fd7826b966, SHA256 5c642203c007b81625f7de06530b7fb24565dc6ebd9bfeb79d2ff8cd7b06f6f4. Original Run294 compiler SHA256 8801e6da5c9bf37c353d8378bb334b0aeb53e104239d71bdd53a60bf7df50df3.

Original v1 accepted 24/24 paired trusted transactions, including 18 invalid/semantically incoherent acceptances. Seven distinct module-level constructs parse as AST but fail actual CPython 3.13.5 source-byte compilation: return, break, continue, nonlocal, yield, await and misplaced future import. Two non-UTF8 PEP-263 cookies decode the same UTF8 bytes differently: Unicode-AST string é vs actual source-file string Ã©. This coding-cookie defect was already documented in Run264's different compiler; Run295 detects its reintroduction in the new Run294 compiler. It is not novel Python behavior.

## Correction and independent validation

The SHA-pinned Run295 patch reconstructs compiler v2 byte-for-byte from Run294, using tokenize.detect_encoding, UTF8-compatible cookie restriction and compile(source_bytes, filename, 'exec', dont_inherit=True). No candidate code is executed by the compiler. New compiler SHA256 0efcf451b5d571033b138bddc8f9acdc7d37131017ace9f21636c8c394ad53c3; GitHub patch blob 48484fb8bed101a2274701878c0ee752b8d1f35b.

All 24/24 prospectively frozen v2 outcomes matched (18 rejects, six accepts). An independent read-only auditor, importing neither compiler nor experiment runner, found zero errors across both 24-row traces, source hashes, stage hashes and representation parity. 256 new paired trusted arithmetic transactions (512 compiles) produced identical staged hashes and CPython functional values. Replaying Run294's original 48 adversarial arm outcomes preserved 48/48 original source snapshots; only two invalid-syntax rejection labels changed as expected. All 1,024 inherited valid paired transactions retained parity. Seven local unit tests passed.

An initial test-harness exception caught v1's Rejected class but not v2's; the failure was preserved and the runner corrected without changing frozen cases. Raw v1/v2 outcomes, 256 seeded functional traces, separate auditor, encoding counterexample, source files, SHA manifest and previous Run294 archive are in the complete local reproducibility ZIP. Full historical GitHub ZIP mirroring remains incomplete.

## Limits

This establishes a bounded compiler validity repair, not general Python soundness, an IR advantage or model repair. No new coding-model inference, fifth independently qualified real issue, powered representation comparison or breakthrough. Four independently qualified real issues remain: Flask PR6096, urllib3 PR5071, Werkzeug PR3136 and HTTPcore PR1000. All 89 boundary issues remain sealed. Next priority is genuinely paired strong no-cost model inference with exact prompts, model SHA, isolated functional oracle, and new independent issue qualification.
