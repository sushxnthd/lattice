# Run 31 completed pilot: evidence and claim boundary

On 2026-10-12, standard public GitHub Actions run 38285724683 completed successfully using Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M, with both official shard SHA256 checks and pinned llama.cpp commit 8bb3cf0d216a5ae48360179f2931daf284be4d01. Four raw responses were obtained (one public itsdangerous 2.2.0 feature task, one seed, one model). Token usage A/B/C/D: prompt 248/264/270/295; completion 240/77/122/66. Inference wall times 35.087/9.409/13.997/9.646 seconds.

Strict format-valid responses: **0/4** (all markdown-fenced despite explicit instructions). Exploratory posthoc fence stripping yielded valid JSON envelopes for B and C, but both retained fixed-width >Q packing and did not implement arbitrary-size integer encoding. A's diff failed to apply to the supplied excerpt and attempted protected-code modifications; D used the wrong envelope. No generated code was executed and no hidden tests were run.

This is a negative, **single-task feasibility pilot**, not a held-out four-arm benchmark or a representation-specific scientific result. The earlier negative Qwen 0.5B/1.5B comparisons remain unchanged. No publication claim is justified.

Provenance: workflow https://github.com/sushxnthd/lattice/actions/runs/38285724683 ; artifact ID 11764185018 (GitHub retention 30 days); inference commit a60323972a6034f34bdd82d397bb970cfcbcaaa5. Original raw artifact SHA256 d2227938af07b67468bc3ed9b5627597ed71504286bb1a2569b071f053d638b6. Do not overwrite raw evidence.
