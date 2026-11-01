# K-SYNTH-1 Run407: original pinned pytest #14997 regression reproduced

Date 2026-11-01 IST. Canonical branch `research/exp003-context-order`; sole draft PR #9; 89 reserved boundary issues SEALED.

Recovered the **original pre-correction** GitHub Actions run [41274411758](https://github.com/sushxnthd/lattice/actions/runs/41274411758), including BOTH complete raw artifacts. Independently SHA-256-verified ZIP digests, internal manifests, exact source commit IDs, raw stdout/stderr and the twelve frozen case outcomes per version.

| Exact pytest source commit | Public passing | Heldout passing | Controls passing |
|---|---:|---:|---:|
| `a7d58d7a21b78581e636bbbdea13c66ad1657c1e` | 3/3 | 3/3 | 6/6 |
| `cf470ec0bf7eb89cd97dd56df4859eae5db46447` | 0/3 | 0/3 | 6/6 |

All six regression targets reported **two passes and one fixture-not-found setup error** for the reentered package file. All six controls passed. The independently implemented local verifier performed **252 checks with zero disagreements** and **15/15 adversarial/regression tests passed**. This is one real issue with one abstract interleaving pattern, not six independent repairs. Exact-source installation produced `0.1.dev1+g<sha>` metadata, so do not infer an installed tagged-release version from that string.

**Original artifact IDs/digests:** control 13071331496 SHA256 `8476adf7ac95eb32c4d92be3e4269093945761cb4f851bdeef84d1f3cc63a15e`; regression 13070971375 SHA256 `89bbb9ecf1269044cc5ee78b27bf6ec2c384cd49bbc73374bbb12a250e971633`.

**Critical provenance finding:** The actual frozen GitHub oracle SHA256 in BOTH artifacts is `9af9417ad6b082968557bf43820dcf20c6fcb8ee9354334e90909590b933135d`. The Run405/406 local archive copy SHA256 `5bbb1ec4b94f18e00f22ac9c4ae5f532cca45d6fc8d62b991b210cb9815c16b9` is NOT byte-identical, although all 14 source files, twelve cases and frozen requirements match. The original GitHub oracle uses positional `sys.argv[1]`; the local copy uses `--output`. Therefore Run406's workflow correction to `--output evidence` was wrong for the actual GitHub source: [run 41278962653](https://github.com/sushxnthd/lattice/actions/runs/41278962653) finished green but uploaded no `evidence/raw_oracle.json`. Both original transport-failure ZIPs are retained. Restored the correct positional workflow invocation in commit `9da4bb28d1ec939b626c740026d0216abaecbf59`.

Before inspecting any fixing reference, froze the deterministic [reference/ablation gate](research/K-SYNTH-1/run407/PROTOCOL_ABLATION_PRE_REFERENCE.md), commit `f7f0f1664d50302e68b894efbd2d87a6f0c9dcd5`. It requires full-reference success on all twelve original cases and genuine joint target-plus-control behavioral necessity of at least two modified production source files, not merely import failures. An exact historical fixing PR/reference commit has **not** been established, so this candidate is **BASELINE REPRODUCED / REPAIR NOT QUALIFIED**.

[Standalone SHA auditor](research/K-SYNTH-1/run407/run407_original_artifact_audit.py) accepts the original two ZIPs, independently checks digests, manifests, statuses and outcome counts. Full 252-check auditor, all original raw ZIPs, tests, local frozen copy and failure artifacts are in the separately SHA-verified local Run407 reproducibility archive.

**Scientific status:** still only TWO independently qualified historical real multi-production-source repairs (Flask PR6096, urllib3 PR5071). No new model inference, powered IR advantage or breakthrough. Continue issue-first qualification, production-capable IR versus information-equivalent Python/AST, genuine paired coding-model inference and independent evaluation.
