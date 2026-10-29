# K-SYNTH-1 Run333: original Run332 recovery and new ID-binding experiment

## Original Run332 result (unchanged)

Recovered GitHub Actions runs [40819679072](https://github.com/sushxnthd/lattice/actions/runs/40819679072) and [40819708725](https://github.com/sushxnthd/lattice/actions/runs/40819708725), artifacts 12873893687 and 12874292193. An independent read-only SHA-256 auditor verified **26/26** and **27/27** original manifest entries; both ZIP integrity checks passed. Original ZIP SHA-256: `52f6aafc1d60842464f5843bb3d773d2d0457b134a17439181fd8d547b0d60ef` and `7a2d3c02119ddc5de3cedc0660e2d42fba59e67410734203f4935178ebcb9d40`.

Both Qwen2.5-Coder-7B arms in both runs produced identical, syntactically valid JSON with **two semantically correct edits**, but output human-readable IDs `probe_a` and `probe_b` instead of the authorized opaque IDs `D3f3bee0a582d` and `Dfdd006778dd3`. The original compiler correctly rejected both arms: `GATE_REQUIRES_BOTH_DISTINCT_IDS`. **Original strict gate result: IR 0/1 and Python/AST 0/1 in each run.** The real production task was **not attempted**. Original model completions are immutable and are not repaired or rescored. Identical seeds/prompts mean the runs are not independent samples.

Original completion SHA-256 (both arms): `aa40e952e8dd6edf73bd6fd7997e8f01346d35085973940f8ef64f98d7a89b65`. Each completion used 55 tokens; prompt tokens 353 IR and 357 Python/AST. The independent auditor also confirmed the original baseline oracle: 0/3 repair targets and 6/6 controls. A **counterfactual read-only** alias-to-ID translation produces two valid target actions, identifying a format/ID-binding failure, not an original compiler pass or evidence of semantic-IR superiority.

## Prospectively frozen Run333 exploratory reformulation

After observing and documenting the original failure, froze a new **post-Run332 exploratory** protocol (commit `b609cc40be873c054c449685e6b8f163cf97b6ef`). The only changed model input is an explicit function-name-to-opaque-ID mapping in **both** gate prompts. The pinned Qwen model SHA, seed, original HTTPX issue, source, real prompts, candidate facts, shared compiler and isolated oracle are unchanged. The new gate still requires two exact opaque IDs and correct edits across two files; no alias translation is permitted in scoring. Real paired inference is conditional on both new gates passing.

Source commit `54ec114cdcbe8056c093f0f80755920a233d3954`; workflow commit `25d7f3a808c0d82ee3cbb6fb42dcd7be0f277b19`. [Run333 cloud workflow](https://github.com/sushxnthd/lattice/actions/runs/40822825928) passed source checkout, independent frozen AST/request audit and reformulation freeze/audit. At the last check, model-engine build was in progress. No Run333 model result is claimed yet.

Three independent historical production issues remain qualified (Flask PR6096, urllib3 PR5071, HTTPX PR1183). No powered statistical result, semantic-IR advantage or breakthrough. All 89 reserved issues remain sealed. Single PR #9 remains open, draft and unmerged on `research/exp003-context-order`.
