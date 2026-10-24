# K-SYNTH-1 Run221 — Independent audit of Run220 (2026-10-24)

All eight Run220 GitHub Actions jobs finished successfully. Retrieved all eight original artifact ZIPs and independently checked the frozen cohort/model SHA-256, all ten actual coding-model requests and responses, prompt hashes, seeds, model identifiers, token usage, source-facts digests, and verifier records. Five independent regression tests passed.

## Frozen paired results

| Measure | Semantic IR JSON | Annotated Python |
|---|---:|---:|
| Frozen issues/repositories | 8 | 8 |
| Preflight retrieval failures, no inference | 3 | 3 |
| Actual coding-model completions | 5 | 5 |
| Compiler accepted | 1/8 | 1/8 |
| Accepted edits disproved by independent issue-specific checks | 1/1 | 1/1 |
| Confirmed functional resolutions | 0 | 0 |

The three preflight failures were `marketsquare__robotframework-robocop-1329`, `pybamm-team__pybamm-3795`, and `googlecloudplatform__cloud-sql-python-connector-1201`. They remain in the frozen denominator, but no coding completion was generated for them. The paired compiler-acceptance table is both=0, IR-only=1, Python-only=1, neither=6; two-sided exact McNemar p=1.0. Wilson 95% interval for shared retrieval feasibility 5/8: [0.306,0.863]; for acceptance 1/8 per arm: [0.022,0.471]. Original functional endpoint was NOT_EVALUATED; no retrospective score change is claimed.

## Two independently disproved compiler-accepted patches

**GT4Py issue 1411, semantic IR:** the model edited `Program.with_bound_args` and inserted an earlier `Program._process_args`. The existing later `Program._process_args` definition overrides the insertion under CPython class binding; the actual `ProgramWithBoundArgs._process_args` override is unchanged. The executable witness for `bound(b=True)` called with `a=1,c=2` still constructs positional `[True]` with kwargs `{'a':1,'c':2}`, instead of binding `b=True` as a keyword. Compiler acceptance was a false positive for issue resolution.

**FastMCP issue 317, annotated Python:** the model replaced unrelated `set_group_attributes` in `examples/smart_home/src/smart_home/lights/server.py` with `test_args`, without modifying the decorator/argument binder responsible for the reported `*args/**kwargs` bug. This destroys an example tool without fixing the framework issue.

Seven other completions failed transaction validation and one hit the 2,048-token cap with incomplete JSON. Exact inference token totals: IR 41,394 prompt / 5,458 completion; Python 43,669 prompt / 4,099 completion. The common action schema appears to be a usability bottleneck, and 3/8 retrieval failures are a construct-validity bottleneck.

## Scientific decision

Do **not** scale this pipeline to the assumption-dependent 686-pair target yet. First prospectively freeze a gold-blind retrieval fallback, a format-control positive gate, independently executable issue-specific functional oracles, and balanced identical-authority Python/AST-action controls. Run a new small feasibility gate, then re-estimate paired repository-cluster power. Keep the 89 unseen boundary issues sealed. If Python matches/beats IR under two controlled reformulations, pivot the central thesis toward immutable epoch history and trusted edit authority, not cosmetic syntax changes.

The eight raw artifact ZIPs, independent auditor, five tests, machine-readable results, full report, and SHA-256 manifest are preserved in the Run221 local reproducibility archive. No semantic-IR superiority, functional issue repair, or world-class completion is claimed.

Original inference: https://github.com/sushxnthd/lattice/actions/runs/40088567234
