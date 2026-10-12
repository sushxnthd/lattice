# Run 31: free-cloud model feasibility pilot (NOT final evaluation)

Predeclared objective: determine whether a capable 7B coding model can complete a single public-package editing task on a standard free public-repository GitHub runner, and preserve raw four-arm responses for independent evaluation. This is a **development pilot**; no hidden-test inference, no publication claim, and no tuning on the frozen final holdout.

Model candidate: Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M from the official Qwen repository. Record both split-file SHA256 values, merged model SHA256, llama.cpp commit, runner image, prompts, seeds, decoding, raw responses, token usage, and wall time. Abort if model checksums do not match expected values. No paid APIs, GPU runners, self-hosted devices, or secrets. Never treat a generated code patch as safe to execute without isolation.

Controls: A ordinary Python patch, B Python edit protocol + verifier, C Lattice edit protocol + identical verifier, D Python edit protocol + executable-invariant instructions. A/B/C/D use identical public task facts. A/B/C/D must be scored on the same independent tests. The pilot is a feasibility study only; it does not substitute for prospectively frozen multi-repository, multi-model evaluation.

Prior negative Qwen 0.5B and 1.5B sequential-edit results are preserved; no representation advantage is established.
