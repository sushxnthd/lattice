# K-SYNTH-1 Run219 — independent issue-contract audit (2026-10-24)

## Inputs and provenance

Recovered both completed Run218 cloud artifacts from workflow run 40080655875. The original scores remain unchanged. Frozen artifact SHA-256 values:
- googlefonts__ufo2ft-930: `bf563236c88a28d60cf80002b80b2c7ce10882e276134e41b7e544ad11a5724b` (artifact 12555239822)
- spikeinterface__spikeinterface-2775: `c430cd2ae371d7d85a314f23ebc90b35779a4bcf5dc80fa60d70f81e2685f47b` (artifact 12555444396)

Model: Qwen2.5-Coder-7B-Instruct Q4_K_M, pinned SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. Independently verified exact prompt hashes, seeds, JSON schema, model identity, token usage, compiler traces, and shared retrieval equivalence.

## Result: compiler acceptance is not functional repair

| Condition | Compiler accepted | Independently demonstrated issue resolution |
| --- | ---: | ---: |
| Semantic-node JSON | 2/2 | **0/2** |
| Annotated Python | 2/2 | **0/2** |

**ufo2ft #930:** Executed the AST-extracted model-generated `_featuresCompatible` function in a controlled designspace against five contract cases. The semantic-node completion unconditionally returns False, breaking both ordinary identical-feature and default-only cases. The annotated-Python completion retains an early return before its proposed include check, so identical `include(...)` features still incorrectly return True. The original function failed the include cases, while a separately constructed hypothesis guard passed all five controls. This is a retrospective necessary-condition evaluator, not a gold patch or production fix.

**spikeinterface #2775:** Both completions changed only `doc/modules/curation.rst`, not the implementation of `CurationSorting.split` where two new unit IDs are hard-coded. Documentation-only changes cannot repair the reported runtime defect. No integration suite was run for this issue.

These four accepted-but-incorrect edits are counterexamples to treating transactional compiler acceptance as issue resolution. No superiority of semantic IR was observed; n=2 and zero discordant successes preclude a meaningful paired inference. The earlier ~686 paired-issue target is an assumption-dependent planning estimate, not a result from these outputs.

## Reproduction and next experiment

The local reproducibility archive contains the two immutable model artifact ZIPs, independent Python oracle, eight passing unit tests, five executed ufo2ft cases per arm, positive/negative controls, all model prompts and outputs, verifier traces, hashes, and statistics. The remote CI evaluator can be added once the complete source files are persisted.

Next: freeze an independent issue-resolution oracle before additional model inference, then run an adequately powered, repository-cluster-aware paired comparison using identical authority/compiler/verifier and strong open models. Preserve the 89-issue unseen boundary cohort; do not claim an IR mechanism without ablation and unseen prediction.