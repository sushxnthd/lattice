# Lattice Run256 — independently qualified real two-source task and frozen capable-model pilot

Date: 2026-10-26 (Asia/Kolkata). Kernel K-SYNTH-1. Branch `research/exp003-context-order`, draft PR #9.

## Independent real-source qualification

Recovered completed GitHub Actions run [40236090884](https://github.com/sushxnthd/lattice/actions/runs/40236090884), artifact 12615680769, SHA-256 `4e058e5f00f450ddc7241df89c8568f37508a79f43317ff1ed25d2cdda0d0656`. Independently checked ZIP CRC, oracle and environment SHA, pinned upstream commits, all twelve subprocess traces, and per-source SHA parity.

Flask PR6096 pinned base `514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b`, reference `05e9c6bd630ecf4ec0ec884b1fc7901663737bc7`:

| Source variant | Public IPv6 server | Held-out IPv6 session | IPv4 nonregression |
|---|---|---|---|
| Baseline | FAIL | FAIL | PASS |
| Reference app.py only | PASS | FAIL | PASS |
| Reference testing.py only | FAIL | PASS | PASS |
| Both reference source files | PASS | PASS | PASS |

First independently verified real upstream two-production-file *reference-patch source ablation* in this kernel. It shows that the two reference changes independently fix distinct observed failures, NOT that every possible successful solution must edit both files. No AI repair on Flask is claimed.

## Independently recovered final Run254 rerun

Completed Actions run [40232108742](https://github.com/sushxnthd/lattice/actions/runs/40232108742), artifact 12616021399, SHA-256 `8509cb2bee67b370e1941c0de1c4069573368305e578c96c0e28034b7f7ffc11`. Four Qwen2.5-Coder-7B-Instruct raw completions matched their exact preregistered request SHA and all four were byte-identical to earlier run 40232048444. Humanize both arms compiler-rejected; packaging both arms compiler-accepted but failed public and held-out oracles with recursive self-call. Zero of four repairs; zero paired discordances. These are deterministic *repeats* of two single-source tasks, not independent new samples.

## Frozen two-source capable-model pilot

Committed compressed runner `research/K-SYNTH-1/run256/run256_flask_overlay.py.zlib.b64` at `91c5bcc7a54daaa2ff42c92504bd607755c3c6bb`; decompressed SHA-256 `fe8ab7160d8fa549c12392c4834f71b4f62f18ede4520558c16aed625ee19c51`. Workflow `.github/workflows/lattice-k-synth-1-run256-flask-paired.yml` created at `c198198c01c5e1b561935a156753e84a062a3305` and deterministic overlay directory corrected at `f49f90f1626e99507926c3933e5cbaa8f12a2eb0`. Workflow push submitted; run ID/outcome not verified yet.

Prospective protocol: pinned real Flask upstream, baseline/reference controls, freeze requests before inference, identical source method excerpts and conservative CFG facts, JSON versus Python-comment fact encoding, same two-file native patch authority, same compiler and network-isolated Docker oracle. Qwen2.5-Coder-7B-Instruct Q4_K_M SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; seed 256001, temperature 0, max completion 2048, context 24576. Exact prompt hashes and token counts will be recorded by workflow if executed. This is an information-equivalent *fact-encoding* contrast, NOT true semantic-IR superiority; CFG-v2 does not establish full Python semantic soundness.

Two local prospective protocol tests passed. Complete raw evidence, independent auditor, source, tests and SHA manifest are preserved locally.

## Scientific verdict

No semantic-IR advantage established. Powered capable-model comparison, genuine semantic-IR versus ordinary-Python contrast, mechanism ablation, unseen boundary prediction and independent multi-repository sample remain outstanding. Draft PR #9 stays open/unmerged. Preserve all 89 sealed boundary issues.