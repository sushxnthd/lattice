# K-SYNTH-1 Run445 addendum — independent **real Flask API** factorial audit

**GitHub Actions:** [run 41522993332](https://github.com/sushxnthd/lattice/actions/runs/41522993332), completed **SUCCESS** 2026-11-02 UTC. Original unmodified artifact ID `13177664423`, ZIP SHA-256 `5cca13b9d9e6c781f187282c75f8cf3480207ba2ad8e2ce57e2d0aa3febf8ef0`. All **11/11 original manifest payloads** independently verified by byte size and SHA-256. All four isolated Python processes exited 0.

The workflow froze 128 valid host authorities (32 each: DNS no port, DNS with port, bracketed IPv6 no port, bracketed IPv6 with port) **before fetching the fixing reference**, verified exact source SHA values at historical Flask PR6096 parent `514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b`, then overlaid the two actual fixing-source components from pinned PR head `7203feabf723edae0286ae5dc64fec8ac4c91735`. Each variant executed **128 actual `Flask.run` calls** with a mocked non-network `run_simple` and **128 actual `FlaskClient.session_transaction` plus GET pairs**. All source overlays ran in separate Python processes. No model-generated code was executed.

| Actual source overlay: app, testing | Correct run /128 | Correct session /128 | Sum /256 | Joint /128 |
|---|---:|---:|---:|---:|
| 00 historical parent | 64 | 60 | 124 | 60 |
| 01 testing only | 64 | 128 | 192 | 64 |
| 10 app only | 128 | 60 | 188 | 60 |
| 11 full fixing reference | **128** | **128** | **256** | **128** |

The independent auditor recomputed all **512 original real API rows** and **5,398 checks**, verified source/manifest provenance, and found **exact observational separability**: changing `testing.py` never changed the run result (256/256 paired comparisons), and changing `app.py` never changed the session result (256/256 paired comparisons). Thus the per-API additive interaction is **0**, but the joint-success factorial interaction is **+64**. This is a concrete real-public-repository counterexample to treating a positive joint-score interaction as evidence of cross-file causal dataflow. It is not proof of whole-program noninterference.

**New discrepancy versus the Run445 source-expression micro-oracle:** four DNS `host:0` cases (`dns_with_port_01/09/17/25`) failed actual historical session round-trips despite their cookie-host source expression looking correct. All four were fixed by the `testing.py` reference overlay. This shows why source-expression simulations cannot substitute for actual isolated public API oracles. The exact downstream mechanism has **not** been established; do not infer it from the results alone.

**Limits:** This is a post-hoc reference-component mechanism ablation on an already historically known repair, **not** a third independently qualified issue, not fresh model inference, and not a powered IR-vs-AST comparison. The cloud artifact did not preserve a full dependency lockfile, Python patch version or overlay-file SHA-256 receipts; exact source parent/head and base source SHA are pinned, but dependency-level reproducibility should be strengthened in a follow-up. No general Python soundness or breakthrough claim.

The complete local Run445 ZIP preserves both original Actions artifacts, raw traces, independent auditors, tests and SHA manifest. One K-SYNTH-1 kernel; PR #9 remains open/draft/unmerged; 89 reserved boundary issues remain sealed.
