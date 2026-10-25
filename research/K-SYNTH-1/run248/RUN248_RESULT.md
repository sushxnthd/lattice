# K-SYNTH-1 Run248 — pinned capable-model launch and cluster-aware power

2026-10-25. Branch `research/exp003-context-order`; existing draft PR #9 retained.

## Executed inference launch

Mirrored the original SHA-pinned Run247 runner (`run247.py.zlib.b64`, decoded SHA-256 `ac06e7934b6503efbdea9e4b59076936d7d461c2bd5c1fa372e2965654e9d2e8`) and created `.github/workflows/lattice-k-synth-1-run248-native-edit.yml`. Pinned Qwen2.5-Coder-7B-Instruct Q4_K_M, CrossGL commit `d456c2b5f509104dd97b74ce40c597531784e2ca`, llama.cpp `620d2225cc436ab0b001e3200e590e3b286ef9ab`, model weights SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`.

The first two workflow attempts failed at SHA-pinned source restoration, before inference. Investigated the actual logs and corrected transport corruption and an inconsistent local-vs-mirrored compiler source hash. The third workflow, [Run248 Actions](https://github.com/sushxnthd/lattice/actions/runs/40204335375), passed code restoration and frozen-request/reference-control preflight; model building/inference is pending at the time of this report. **No new model completions or representation-performance result is claimed.** Preserve exact prompts, raw responses, model IDs, seeds, usage, compiler traces, failures and functional oracle records from this run.

The three arms are graph-first, Python-first and Python-only. The first two contain exactly the same source and verified typed *syntactic* graph objects in reverse order; they test **presentation ordering**, not semantic-IR superiority. The third arm is a shorter source-only baseline, not information-equivalent. All arms use the same native-Python transaction grammar and hardened compiler/oracle. CrossGL has been used repeatedly and cannot count as an unseen boundary task.

## Independent paired-power simulation

Executed a reproducible 30-scenario cluster-aware simulation (10,000 replications each; nine local regression tests passed), using four issues/repository, discordance probability 0.30, conditional IR win probability 0.60 or 0.65, and latent repository heterogeneity 0/0.05/0.15. A two-sided cluster-studentized test at alpha 0.05 yields illustrative power:

| Issues | Repositories | Conditional IR win | Repo heterogeneity | Estimated power |
|---:|---:|---:|---:|---:|
| 480 | 120 | 0.60 | 0.15 | 0.608 |
| 640 | 160 | 0.60 | 0.15 | 0.730 |
| 960 | 240 | 0.60 | 0.15 | 0.878 |
| 480 | 120 | 0.65 | 0.15 | 0.916 |
| 640 | 160 | 0.65 | 0.15 | 0.970 |

These are **assumption-driven planning numbers, not model outcomes**. Neither 258 pairs nor 306 nominally independent pairs suffice to establish adequate power under arbitrary repository clustering. Final inference must account for repository-level dependence and task selection.

Complete local Run248 archive contains the original runner, pinned frozen requests, simulation source, 30-scenario JSON, regression tests, manifests and detailed report. Next: recover real completions; qualify new independently pinned multi-file tasks with executable positive/negative controls; conduct a properly powered typed-semantic-IR versus ordinary-Python comparison with identical compiler, verifier and edit authority. Keep the 89 sealed boundary issues untouched.

No breakthrough is claimed.