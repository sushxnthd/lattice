# K-SYNTH-1 Run220 — Eight-repository capable-model feasibility experiment

**2026-10-24.** Prospective experiment frozen before any Run220 model outputs. This is a real-repository, information-matched feasibility study, **not** the adequately powered representation claim.

## Frozen cohort and inference

Eight discovery issues, one per repository: datadog__guarddog-419, gridtools__gt4py-1411, marketsquare__robotframework-robocop-1329, qchackers__tqec-376, spikeinterface__spikeinterface-3778, jlowin__fastmcp-317, pybamm-team__pybamm-3795, googlecloudplatform__cloud-sql-python-connector-1201.

The selection is made by exact issue IDs against the SHA-256 verified Run199 public cohort. The generated JSON cohort uses `json.dumps(rows, indent=2, sort_keys=True) + "\\n"`; its expected SHA-256 is `e262048bb9785bb1774b4d9e0a76654e928d7b647af144edf29379d8976fa686`. None of the 89 reserved boundary issues is used.

Two paired conditions: typed semantic-node JSON and annotated Python source. Both receive exactly the same retrieved file information and structural target records, use the same short target IDs, original preimages, shared tracked-file edit authority, transaction compiler, verifier, constrained JSON action schema, per-issue seed, temperature zero, and 2048-token completion budget. Arm order alternates across repositories. The open coding model is Qwen2.5-Coder-7B-Instruct Q4_K_M, SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`.

The shared retriever runs before both representations. If no issue-named function/class is retrieved, the issue is marked `PREFLIGHT_MISSING_NAMED_TARGET` in both conditions and remains in the denominator of retrieval feasibility; it is not silently omitted. Each task preserves frozen manifests, exact prompts, seeds, raw model outputs, usage counts, compiler traces, failures, and model runtime logs.

## Evidence boundary

Run219 found four compiler-accepted but functionally inadequate patches on two previous real issues. Accordingly **compiler acceptance is not a proxy for issue resolution**. Run220 explicitly records independent functional issue resolution as `NOT_EVALUATED`. No Run220 model outcomes were available at protocol creation. This run must not be described as a functional win, mechanism result, or breakthrough.

The earlier 686-pair target is assumption-dependent (discordance 0.30, IR wins among discordant 0.65, ICC 0.5, unequal repository sizes and a specified test). Eight pairs are only an exploratory pilot. The next decisive step is to preregister independent issue-specific functional oracles and expand the real-repository cohort using measured discordance and repository-cluster uncertainty, while reserving the 89-issue boundary cohort for an unseen prediction.

## Reproducibility

Run `python -m unittest -v test_run218 test_run220` after restoring the pinned Run207 compiler and Run208–210 patches; then `python run220.py --cohort cohort.json --out /tmp/run220-0 --task-index 0 --freeze-only`. The GitHub Actions workflow restores the trusted source, downloads the SHA-verified public cohort, freezes all eight tasks before inference, and executes eight isolated no-cost CPU jobs.

**Operational contingency:** GitHub CI or model download failure does not alter the frozen design. Preserve partial artifacts, record failure and retry on a later run. Keep the existing research branch and draft PR #9; no new PR.
