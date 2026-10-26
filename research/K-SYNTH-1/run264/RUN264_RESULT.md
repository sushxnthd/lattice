# K-SYNTH-1 Run264 (2026-10-26): second independent two-source qualification and encoding-coherence counterexample

## Prospective urllib3 PR5071 qualification: PASS (bounded)

Recovered Actions run 40274404783, artifact 12630071626, ZIP SHA256 `5fa25d28fe6ffa1e4c2a72daa624d96162a68389affb90a6aa6757ddf77c7301`. Independently parsed all six frozen source-ablation outcomes, subprocess stdout/stderr, three source SHA256s per variant, pinned upstream base `f4e4bc31f40f8c94c6a1f1685df28f97ff48c305` and reference `f5cf122346141b187cca0db6e6445297d336b610`. The generated `urllib3._version` shim was identical across all variants; the original frozen six endpoint checks were unchanged.

| Variant | Manager port 0 (public) | Proxy port 0 (heldout) | URL netloc :0 (heldout) | 3 nonregressions |
|---|---|---|---|---|
| baseline | FAIL | FAIL | FAIL | PASS |
| poolmanager.py only | PASS | PASS | FAIL | PASS |
| util/url.py only | FAIL | FAIL | PASS | PASS |
| connectionpool.py only | FAIL | FAIL | FAIL | PASS |
| poolmanager.py + util/url.py | PASS | PASS | PASS | PASS |
| full reference (three files) | PASS | PASS | PASS | PASS |

This is the **second independent real public-repository issue** with two separately necessary *reference-patch components* for the frozen behaviors, following Flask PR6096. It does **not** prove no alternate one-file fix exists. The third production file is not necessary for these particular frozen endpoints. `qualification.json` matches the archived manifest SHA256; `console.txt` does not (tee appended after manifest creation). The original artifact and mismatch are retained, not repaired or concealed.

## New compiler-validity counterexample and v4 mitigation

Run263 v3 validates `compile(source.decode('utf-8'), ...)` but the actual CPython source-file loader compiles **bytes** and respects PEP 263 coding cookies. For the byte-identical source `# coding: latin-1\\nx = "é"\\n` encoded as UTF-8, the string-mode compile yields `x == "é"`, while byte-mode compilation yields `x == "Ã©"`. An unchanged-span transaction was accepted by v3, although its assumed Unicode semantics diverged from execution as a Python source file.

Run264 v4 rejects non-UTF8 coding cookies using `tokenize.detect_encoding` and validates original and edited files with `compile(source_bytes, ..., dont_inherit=True)`. UTF8 cookies and BOM are supported. This is a **bounded source-encoding coherence** guarantee, not a general Python semantic or security guarantee. v3 and all earlier frozen protocols remain immutable.

Evidence: six new tests pass, five inherited v3/reference tests pass (11/11 combined), all five upstream Flask reference edits still reconstruct the pinned two files byte-for-byte, and the matched AST-anchor/Python-byte-span 512-mutant stress remains 145 accepted, 367 rejected, zero outcome disagreements. No model inference occurred in Run264.

## Decision

The real multi-source benchmark count increases from one to **two independent qualified issues**. Both are far below the prospective powered target (306–681 independent pairs before repository-cluster adjustment). No representation superiority, McNemar significance, model repair success or breakthrough is claimed. The current AST-anchor experiment is syntactic; a verified semantic/dataflow IR versus information-equivalent ordinary Python baseline and capable-model study are still required.

Preserve branch `research/exp003-context-order`, single draft PR #9, one K-SYNTH-1 kernel, all 89 sealed boundary issues. Full SHA-verified local archive contains raw cloud ZIP, independent auditor, source v3/v4, counterexamples, test traces and frozen Flask snapshots.
