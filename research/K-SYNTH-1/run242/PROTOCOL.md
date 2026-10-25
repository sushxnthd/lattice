# Run242 — prospective metadata-burden × representation pilot (2026-10-25)

**Frozen before new model inference.** One real CrossGL/crosstl issue (#41) at commit `d456c2b5f509104dd97b74ce40c597531784e2ca`. This is a single-issue pilot, not an adequately powered representation experiment. Run240/241 outputs are discovery data, not prospective Run242 outcomes. The 89 reserved boundary issues remain untouched.

## Five frozen arms

1. `ir_trusted_json`: semantic-IR source view, JSON `{selector,content}`, trusted path/hash derivation.
2. `python_trusted_json`: ordinary-Python source view, **identical** JSON schema and compiler.
3. `ir_copied_metadata_json`: semantic-IR view, JSON `{path,file_sha256,selector,content}`.
4. `python_copied_metadata_json`: Python view, **identical** copied-metadata schema.
5. `python_native_source`: Python source view, plaintext Python replacement code in selector-delimited blocks, deterministic projection to the **same** compiler.

The first four arms form a 2×2 source-presentation × metadata-responsibility design. The **primary** pair is arms 1 vs 2. Arms 3–5 are construct-validity diagnostics. The native-source arm has unconstrained decoding and a different output interface; any difference is not a pure representation effect. It is still selector-delimited, not a full conventional Python diff baseline.

## Immutable experimental facts

- Canonical source-facts SHA-256: `743cb14479c89ca8bc4c648a47cf85e1379d6d744e3379e8136ee7292aef5723`.
- Pinned open model: Qwen2.5-Coder-7B-Instruct Q4_K_M, SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`.
- Pinned inference engine: llama.cpp v0.7.0 commit `620d2225cc436ab0b001e3200e590e3b286ef9ab`.
- All arms: seed 24241, temperature 0, max completion 3072 tokens; identical three editable targets, four read-only targets, shared AST/decorator-preserving compiler, and five-case independent functional oracle.
- Original source passes 3/5; the independently authored three-file reference passes 5/5. Reference repair is excluded from prompts.

### Frozen request SHA-256 (ordered execution)

| Arm | SHA-256 |
|---|---|
| ir_trusted_json | `9b2e2478673f4021a6b71f02847af355524b7d3127bf75cb75ec4bca1a0d1148` |
| python_trusted_json | `d1080b2222d63c091d2294ab46a537c9519cebafa1e185d084a1a295fe707c98` |
| ir_copied_metadata_json | `d56dbbfaa9064213abac69a9a1ac27c5ad123731401e766c6b2958bf2d84b3e3` |
| python_copied_metadata_json | `a799257d01fa76a16638d3aee07199a2e433fed4752a644761b3f9f9bb9eec56` |
| python_native_source | `2ae9854cac65edc46aaff435fc8179c12e4c3ee51bd2efe652428eee36bc1b8c` |

## Endpoints and limitations

**Primary:** all five functional checks pass, transaction valid, Git patch applies, no original declarations/decorators erased. Secondary: raw token usage, schema validity, metadata-copy errors, unauthorized selectors, declaration deletion, changed-file count, full failure and verifier traces. With one issue, report descriptive outcomes and **no superiority p-value**. A post-hoc repair never counts as model success.

Falsifiable transport prediction: copied-hash/path errors are structurally impossible in trusted-metadata arms, but authorization/declaration/functional failures remain possible. Any native-source advantage is confounded by output format and constrained decoding.

**Power:** at assumed discordance .30 and conditional IR win .65, exact two-sided McNemar α=.05 gives 258 independent pairs ≈72.3% power, 306 ≈80%; at win .60 about 681 independent pairs. Increase for repository clustering; do not count multiple seeds from one repository as independent issues.

Model-generated code is evaluated in a resource-bounded subprocess with credentials stripped, **not** a complete network sandbox. This pilot is run only on a disposable read-only-token worker. No representation breakthrough is claimed.