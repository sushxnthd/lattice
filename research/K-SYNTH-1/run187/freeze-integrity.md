# K-SYNTH-1 freeze integrity (2026-10-23)

The prospectively frozen Run186 corpus comprises 258 paired synthetic four-module Boolean repairs. The preregistered primary endpoint is first-attempt fully verified repair success (graph minus Python SSA). No capable-model completions have been obtained; this document must not be interpreted as a result.

Frozen public SHA-256: `75a29941a8802ab6b1c8a55e501d25e2273267839eb965fe303698d164c0cc94`.
Frozen sealed SHA-256: `84c83e21e06ade4c8372725d89d371cd4d771794bf21698216cdef1ad6cb03c9`.
The source model file is `bartowski/Qwen2.5-Coder-7B-Instruct-GGUF` at revision `b6b3aefe0cbdb2e0fc55016cba9f9827b3b59ad7`, Q4_K_M SHA-256 `0d10372614925f17c1fd0b9f987d9c542a6f9b1548f83621b70c3ce8e9d3c1d8` (verified against pinned revision, not `main`).

Python SSA prompts are approximately 18% longer by characters than graph prompts, despite equal semantic facts. Report actual model token usage; do not attribute any observed advantage to representation-specific reasoning without the localization ablation. The 258-pair power calculation assumes IR-only 0.14 and Python-only 0.06 and does not support product-scale claims. Freeze cannot be changed post inference.
