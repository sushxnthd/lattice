# K-SYNTH-1 Run358: prospectively declared context-capacity replay

Date: 2026-10-30 UTC. This is a **NEW** execution configuration, not a rescore or alteration of the original Run357b failure.

Original Run357b GitHub Actions run 41007027701 and artifact 12956780014 completed with a precompletion context gate: actual raw tokenizer lengths IR=14315 and PYTHON_AST=14909, each with a 3500-token completion budget, exceeding the original 16384-token slot. Original artifact SHA-256 76911acfe755713fa56866cdd72ff19947dbbecea01b15326c3ff2e27b004317; no model completions occurred. Baseline isolated oracle reproduced 6/10.

Run358 repeats the SAME prospectively frozen Run357b prompts and model without modifying task facts, source, seed, authority, compiler, or oracle, but expands llama.cpp context slot from 16384 to **20480** tokens. The predeclared acceptance gate is n_prompt+3500 < 20480 for both arms. IR prompt SHA-256 e6f75e8b9e594d21c198e36c8c50ad4d8f3b7a6b50b5d3737856ff556dcd8dcd; Python/AST prompt SHA-256 184a9b7e7207a4694e7cdb706ce6f58aa7d9b2ac0b23521bf65fdd060c127fbd. Model SHA-256 509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c; seed 3572026, temperature 0, max_tokens 3500. Frozen source base c46802478cdd8a82ee8cb333420080fab1aed00b. Same line-addressed atomic compiler, isolated 10-case Docker oracle, baseline 6/10 requirement, and original reference-blind source-derived facts.

Classification: context overflow, model precompletion timeout, invalid JSON, compiler rejection, isolated oracle failure, partial repair, complete repair. Both arms must complete to form a paired functional comparison. Raw completions and exact token lengths must be preserved, SHA-manifested, and independently audited. Any context or memory failure is missingness, not a model or representation failure. A single historical task cannot establish superiority.

Separate post-freeze h11 parser-boundary functional tests (Run358 h11=0.16.0) are exploratory mechanism evidence and MUST NOT be added to the original frozen 10-case score or used to retroactively change success criteria. All 89 reserved boundary issues remain sealed; one open/draft/unmerged PR #9.
