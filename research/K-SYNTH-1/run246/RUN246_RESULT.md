# Run246 — original-source byte-span counterexample (2026-10-25)

**Research kernel:** K-SYNTH-1. **Branch:** `research/exp003-context-order`. **Draft PR:** #9.

Independent audit of the immutable Run237 twelve-repository and Run242 CrossGL source cohorts exposed a second construct-validity defect in Run245's typed graph v2. The graph parses `textwrap.dedent(source)` and then publishes its AST coordinates as if they indexed the original source. Python AST columns count UTF-8 **bytes**, not characters. The same incorrect facts are re-derived by v2's validator, so source round-tripping cannot detect this.

| Frozen-cohort measure | v2 | v3 |
|---|---:|---:|
| Parseable Python snippets | 269 | 269 |
| Structural nodes | 2,665 | 2,665 |
| Wrong original-source spans | **854** | **0** |
| Wrong call spans | **364/1,053** | **0/1,053** |
| Targets with any wrong span | **74/269** | **0/269** |
| Invalid UTF-8 original-source slices | **14** | **0** |
| Serialized IR UTF-8 bytes | 708,067 | 726,617 |

There were 26 non-Python exclusions. These are deterministic counts on the frozen cohort, not statistically independent trials or coding-model outcomes. The v3 byte-span correction adds 2.62% serialized bytes versus v2.

**Minimal witness:** `    def get(self):\n        return super().get()\n` parses after dedent with the `def` at column 0; the original source has the `def` at byte column 4. An editor using the v2 offset selects the wrong bytes.

**Repair:** v3 maps each dedented physical line back to its original UTF-8 byte prefix and translates both start/end columns of structural and binding spans. It preserves v2's corrected reference namespaces, exact original source, and full re-derivation validation. Independently checked against 269 frozen parseable snippets and 1,053 call spans. **38/38 tests passed** (22 inherited and 16 new adversarial tests).

**Persistence:** The complete v3 implementation, tests, auditor, per-target traces, original frozen ZIPs, and SHA-256 manifest are preserved in the run-local archive. The source payload under this directory is compressed and SHA-pinned; it must be decoded before use. A report commit is not equivalent to mirroring the full evidence archive.

**Science limitation:** v3 remains a typed syntactic graph, not sound name resolution or semantic dataflow. Its IR exposes original source in base64 while the Python baseline exposes plaintext; that is a model-usability confound even though deterministic reconstruction is lossless. Do not claim a representation win. No new capable-model inference or new multi-repository functional qualification occurred in Run246.

**Next:** Qualify two additional real multi-file reference repairs across independent repositories, then run actual paired open-coding-model inference with readable source and identical facts in both arms, a genuine native-Python editing baseline, equal compiler/verifier and edit authority, pinned tokenizer, seeds, prompts, raw outputs, and independent functional oracles. Recompute cluster-aware sample size before expanding. Keep 89 reserved boundary issues sealed.