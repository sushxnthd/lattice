# Run244 — Typed AST representation construct-validity audit

**Date:** 2026-10-25. **Status:** tested local prototype and independent frozen-source audit. **No new model inference.** Research kernel K-SYNTH-1, draft PR #9.

Run243 established that earlier "semantic IR" was merely a JSON envelope of Python source strings. Run244 implements a typed AST graph with field-level child references, syntactic call candidates, binding records, exact UTF-8 source recovery, and a compact structural projection. An ordinary-Python view carries the **identical graph facts**, verified by inverse parsing. Neither graph claims sound interprocedural dataflow or resolution of dynamic dispatch.

### Frozen-source results

Input: unchanged Run237 twelve-repository evidence archive SHA-256 `76c0e84f052f9dc87d9d8147e3fd2916539c36939dbc899adc0011c003dfc748` and Run242 CrossGL archive SHA-256 `83f82851d62fd2a147fa274f338e569ce01684e10d28a5f5edf989327ef383ab`.

- 295 distinct frozen source blocks; 269 valid Python targets and 26 non-Python blocks (7 RST, 6 YAML, 6 XML, 3 JS, 2 HTML, 1 Markdown, 1 PO). All Python targets parsed successfully.
- 147,799 original UTF-8 source bytes, 17,735 full AST nodes, 2,665 compact structural nodes, 1,053 syntactic call candidates, and 1,284 syntactic bindings.
- Across all 269 Python blocks, full and compact representations each recovered the exact source and identical typed facts in both views. Independent CPython AST structural hashes matched.
- Full typed IR serialization: 2,526,615 bytes (**17.09×** source). Full Python plus the same facts: 2,491,772 bytes (**16.86×**).
- Compact typed IR: 623,908 bytes (**4.22×**). Compact Python plus same facts: 589,065 bytes (**3.99×**).
- Compact projection reduced IR byte cost **75.3%** relative to the full AST. This is a byte comparison, **not** a model tokenizer measurement or an accuracy improvement.
- 12 adversarial regression tests passed, including Unicode, CRLF, decorators, nested classes, match, f-strings, dynamic calls, delimiter collision, and source/graph tampering.

### Theoretical and empirical interpretation

For source `s` and deterministic graph `G(s)`, both checked serializations are invertible encodings of `(s,G(s))`. Therefore neither has additional ground-truth task information on the tested domain. Differences in finite-model performance could still arise from presentation, tokenizer cost, model priors, and computation. This is a straightforward equivalence observation, not a novel information-theoretic theorem.

**Critical negative finding:** naive full AST prompts inflate bytes by approximately 17×. Any future claimed representation benefit must account for tokenizer/context overhead, and non-Python targets require language-specific frontends rather than silent exclusion.

### Reproducibility and limitations

The full source, tests, per-target fact hashes, exact exclusion log, statistical aggregates, SHA-256 manifest and executable audit are preserved in local artifact `lattice_run244_typed_ast_construct_audit.zip` (ZIP SHA-256 `222e8133e2e5647f949b4b7615370431d67b4e609af2d8897e3992236b911d90`). The full local artifact is not automatically mirrored to GitHub. If unavailable from the run's attached artifact, retrieve it from the conversation history.

No additional real-world issue was functionally qualified in this run, no new model inference occurred, and no representation superiority is established. The next substantive experiment must qualify independent real multi-file issues with failing originals, passing references and per-file negative controls; freeze tokenized prompts and common compiler/evaluator before capable-model inference. Existing paired-power sensitivity suggests 306 independent pairs under a hypothetical 65% conditional IR win rate, before clustering; 258 is not presumed sufficient. Keep 89 boundary issues untouched.
