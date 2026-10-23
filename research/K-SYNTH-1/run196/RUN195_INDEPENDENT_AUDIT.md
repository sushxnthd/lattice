# K-SYNTH-1 Run196: independent audit of Run195 model inference

**Status:** The Run195 GitHub Actions workflow finished successfully on 2026-10-23; both CPU shards produced complete raw evidence. This audit replays all 40 actual Qwen2.5-Coder-7B-Instruct responses, not simulated outputs. Frozen prompt SHA-256: `1e87c431e73c79ecf975ace9e406a44a7ba6e3ff920300df024030a4fd4dea98`.

- **Positive controls:** 8/8 valid and correct (two controls × two representations × two shards).
- **Pilot:** IR 0/16, Python SSA 0/16. All 32 model responses obey the exact JSON schema.
- **Failure mechanisms:** IR: 8 cyclic current-gate references, 8 semantically incorrect expressions. Python SSA: 16 cyclic current-gate references.
- **Prompt tokens:** IR 8,867; Python SSA 10,045. Completion tokens: IR 456, Python 413.
- **Paired outcome:** 0 discordant tasks out of 16, exact two-sided McNemar p=1. This is **not** evidence of equivalence or of a representation effect.
- **Statistical limitation:** 16 synthetic tasks share only four instruction families. If issues were independent, the two-sided exact 95% upper bound for a zero-discordance probability would be 0.206; if only four independent families, 0.602. Neither justifies a real-repository conclusion.

The independent evaluator reconstructed the immutable node graph, evaluated all 64 Boolean assignments per task with CPython, and checked the raw prompts, seeds, response model IDs, usage, schema and verdicts against the frozen protocol. Every recorded verdict agreed with independent evaluation. The original Run195 workflow and raw artifacts remain at https://github.com/sushxnthd/lattice/actions/runs/39940142990 (artifact IDs 12496736474 and 12496124121).

**Decision:** The format-only explanation is falsified for this pilot: structured JSON and elementary edit controls succeed, but complex repairs fail. The compiler currently treats a reference to the authorized `gate` as a new-version cycle, even when the request needs the historical gate. Next: separately freeze a matched snapshot-addressed edit interface in both arms and test whether explicit immutable version addresses repair this failure. Then use independent realistic multi-file issues with cluster-aware uncertainty and a separate unseen-condition prediction. Do not expand the four-family synthetic suite to 258 and claim adequate power.

**Claim boundary:** This is a negative, measurement-validity diagnostic. It is not a mechanism ablation, a real-repository benchmark, or evidence that either representation is superior.
