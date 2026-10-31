# K-SYNTH-1 Run380: independent audit of genuine Qwen inference (2026-10-31)

Original successful Actions run: https://github.com/sushxnthd/lattice/actions/runs/41159715407
Original artifact ID 13026863365; ZIP SHA256 `719f30e99f3d608683b8bdf643c6549105b6c6381fa4340ff8952a0f56fef7f1`; all 49 original artifact payloads independently verified against its SHA manifest. Exact original Run379 freeze matches all four requests, prompt hashes, and source Git blobs. Model Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M SHA256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. Unrelated schema-only preflight passed. No personal machine or paid API.

| Arm | Prompt tokens | Completion tokens | Compiler | Public | Heldout |
| --- | ---: | ---: | --- | ---: | ---: |
| A IR | 1404 | 308 | ACCEPT | 8/8 | 4/4 |
| A Python/AST | 1430 | 308 | ACCEPT | 8/8 | 4/4 |
| B IR | 1404 | 308 | ACCEPT | 8/8 | 4/4 |
| B Python/AST | 1430 | 308 | ACCEPT | 8/8 | 4/4 |
| Historical base | n/a | n/a | n/a | 6/8 | 2/4 |

All **four genuine model completions are byte-identical** SHA256 `522c56839327533457909ee01dc9fe68e5f2061e0160a47e6713222f27831c77`, and all four accepted two-file transactions yield identical patched source SHA256: async `b9bff6b55d6ae8936b4f0f371a519fd0432dab23f7be5cdb0d065f24e0a4a02d`; sync `c3fa11d5034159d4f7ac90cbafe0a5be6da88d4a11a7c35c6968acb85f84969e`. The model guarded `self._requests.remove(status)` in both exception handlers. The original frozen compiler accepted the fenced JSON outputs: this is a *new prospective editor study*, not a retrospective rescore of Run377.

Independent read-only replay checked original manifest integrity, frozen request equality, exact prompt/seed/model metadata, raw completion and usage, two historical source Git blobs, AST statement location, source-preserving byte reconstruction, compiler output hashes, 48 retained patched functional observations and 12 baseline observations. **Six adversarial tests passed**, including tampered hashes, tampered functional records, compiler traces and duplicate ZIP entries. Original functional tests ran in isolated GitHub Actions Docker; this independent audit validates the retained records and reconstructs compiled bytes, but does not re-execute untrusted patches.

**Interpretation:** IR and Python/AST each achieved 2/2 matched successful reformulations, but this is only **one distinct real issue**. Zero discordant pairs, zero demonstrated representation advantage, and no evidence of population equivalence. Prompts explicitly describe the failure and show relevant code, so this is not a hidden-mechanism discovery. Investigator was not blind to the historical reference. The ten qualified historical PR cohort and all 89 sealed issues remain unchanged. Run377 strict 0/1 per arm and Run378 post-hoc results remain unchanged. Next: unseen prospectively frozen repair, strong model, genuine semantic/dataflow IR, matched Python/AST, and cluster-valid powered evaluation.

Local full evidence bundle SHA256 `d519777fa00d731f4ed3248ba3118b98a3d8bc48359356e191f803214ab9a254` includes original cloud ZIP, original Run379 freeze ZIP, independent executable auditor, six tests, full SHA manifest and raw results. Full binary bundle not mirrored in this GitHub commit. One K-SYNTH-1 kernel, one draft PR #9, same branch.