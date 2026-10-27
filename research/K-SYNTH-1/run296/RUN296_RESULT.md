# K-SYNTH-1 Run296: independently recovered original Click PR2956 qualification failure

Date: 2026-10-27 UTC. Canonical branch `research/exp003-context-order`, one draft PR #9.

## Original prospectively frozen experiment

Candidate: [pallets/click PR2956](https://github.com/pallets/click/pull/2956), an upstream merged public-repository change touching two production Python files. Exact upstream base `5c1239b0116b66492cdd0848144ab3c78a04495a`, reference head `9caedb9206103dfb5465e1916bc2f13b9c10c0e4`. Original test cases, expected outcomes, source blob SHAs and qualification rule were frozen in [PROTOCOL_FROZEN.md](PROTOCOL_FROZEN.md) and [run296_qualification.py](run296_qualification.py) **before** running the upstream source ablations.

[Original GitHub Actions execution](https://github.com/sushxnthd/lattice/actions/runs/40550689275) completed successfully and uploaded [artifact 12754103542](https://github.com/sushxnthd/lattice/actions/runs/40550689275/artifacts/12754103542). This is a successful *experiment execution*, not a successful *candidate qualification*. Original artifact ZIP SHA-256: `ab457185c962f306d1c90592c645e24a6e84fce6b40806204c120e09f4858c58`. Original raw JSON SHA-256: `650ed47b983f10874afb30fa1d782992d64d2cd39765386b67e72aab1cc2907d`.

| Source configuration | Target cases passed | Control cases passed | Combined |
| --- | ---: | ---: | ---: |
| base | 1/3 | 5/7 | 6/10 |
| core.py only | 1/3 | 6/7 | 7/10 |
| types.py only | 1/3 | 5/7 | 6/10 |
| full reference | 3/3 | 6/7 | 9/10 |

**Original prospective qualification: FAILED.** Full reference failed control C6. Base failed controls C2 and C6. The full reference must pass all controls and the base must preserve all controls, so PR2956 is **NOT** promoted as an independent qualified repair. Do not retune this PR's control set, expectations, or qualification threshold.

## Scientific mechanism and measurement counterexample

The C6 oracle expected a CLI usage error to exit with status 2 while invoking Click's `CliRunner.invoke(..., standalone_mode=False)`. The original full reference instead produced status 1, with a caught `BadParameter`. A separate, explicitly **post-hoc** experiment with installed Click 8.1.8 reproduced the harness mechanism: `standalone_mode=False` yields status 1, whereas `standalone_mode=True` yields status 2 and `SystemExit`. This is an oracle-design error, not a reference-code regression. Independently, C2 was not a valid base-preserved control: baseline interpreted an environment string `false` as true, whereas the reference correctly returned false. These failures demonstrate why target-plus-control *prospective* qualification is necessary.

An independent read-only audit of the original ZIP checked all **40 original public API outcomes**, the 4x2 source-file ablation hash relations, all case IDs, all expected-versus-observed booleans, and both artifact hashes. Zero audit discrepancies. The audit did **not** alter the original frozen outcomes. The GitHub auditor source is in [run296_independent_audit.py](run296_independent_audit.py).

## Limitations and next step

This candidate was selected with upstream patch awareness; it is not gold-blind model-task sampling. The experiment involved **zero new model inference** and **zero model-generated repair**. No evidence for IR superiority, no powered result, no fifth qualified independent issue, and no breakthrough. Four previously qualified real issues remain unchanged. The 89 reserved boundary issues remain sealed. Historical GitHub artifact mirroring remains incomplete.

Run297 must prioritize a **new** independent PR with base-preserved controls, a separately frozen oracle with error-mode semantics checked *before* the freeze, and actual paired capable-model functional inference on the existing qualified issues. Preserve failures rather than retroactively repairing the PR2956 qualification.