# Run242 — prospective five-arm capable-model pilot

**Status (2026-10-25):** A new cloud workflow was launched after freezing exact requests. At publication of this report, no Run242 model completions had been independently recovered or audited. Do not claim a representation advantage.

## Scientific contribution

Run241 found that both representations erased original method declarations and that model-copied file hashes could fail. Run242 separates **metadata transport** from **source presentation** using a 2×2 factorial protocol: semantic-IR vs ordinary-Python source views, crossed with trusted path/hash derivation vs model-copied metadata. The primary pair uses the **same constrained JSON schema** `{selector,content}` and common compiler. A fifth arm emits **plaintext Python replacement source** between selector markers rather than JSON-escaped Python; it is an explicitly secondary output-interface diagnostic, not a pure representation comparison or unrestricted Python diff baseline.

## Executable deliverables

- `run242.py.zlib.b64`: exact runner; decoded SHA-256 `f26d7fcad3d0a0999d6311f00c4f140da94898e90d80bc8c4d0411cae96429c8`.
- `test_run242.py.zlib.b64`: 18 locally passing tests; decoded SHA-256 `be617b1731078b60b366b0498e50433fbc11b3ef31554de5868892c6cc1480d4`.
- `PROTOCOL.md`: frozen model, issue, five request hashes, endpoints, power assumptions and limitations.
- [Cloud workflow](https://github.com/sushxnthd/lattice/actions/workflows/lattice-k-synth-1-run242-factorial.yml) using the pinned Qwen2.5-Coder-7B-Instruct Q4_K_M and llama.cpp engine, with an independent five-case functional oracle. Cloud preparation and preregistration verification are separate from model inference.

The local suite tests shared facts and authority, native-source framing, stale-hash and read-only rejection, and a reference repair that passes the same three-target transaction compiler. The workflow verifies source and request hashes before any inference and preserves raw responses, token counts, and functional traces even on failure.

**Security:** Generated code is evaluated in a separate resource-limited subprocess with credentials scrubbed, not a full network sandbox. Only use on a disposable read-only-token worker.

**Interpretation:** This is one task, one seed and five conditions. Even a clean IR win would be a hypothesis-generating result, not statistical evidence of representation superiority. Exact paired-power sensitivity still calls for at least 306 independent pairs under a hypothetical large effect (and more under clustering). The 89 reserved boundary issues remain sealed.

**Next:** Independently audit all five cloud completions, then qualify and freeze additional independent real multi-file issues with functional reference controls; build a conventional Python unified-diff/full-file baseline before the powered experiment.