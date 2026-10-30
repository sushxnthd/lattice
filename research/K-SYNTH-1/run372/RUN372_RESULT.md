# K-SYNTH-1 Run372 result: reference-blind AnyIO issue, negative two-file qualification

**Freeze before reference:** Issue [AnyIO #642](https://github.com/agronholm/anyio/issues/642) selected from issue text. Prospective two-file criteria committed as `a3d1cf68632dcde063584abbb8998eb6de76756a` before inspecting the fixing patch. Base tag 4.1.0 commit `46a45c7454e4d87ab5671b158f746a2b3beaaae9`; candidate files `src/anyio/_backends/_asyncio.py` and `src/anyio/_core/_tasks.py`. Seven frozen targets/controls T1-T3,C1-C4.

**Historical functional evidence:** [GitHub Actions run 41112883206](https://github.com/sushxnthd/lattice/actions/runs/41112883206) completed successfully on 2026-10-30 UTC, Python 3.11.17. Isolated 2-second subprocess results:

| PyPI release | T1 shielded-main/sibling cancellation | C4 ordinary task group |
|---|---|---|
| AnyIO 4.1.0 | TIMEOUT | PASS |
| AnyIO 4.2.0 | PASS | PASS |

Original GitHub artifact [4.1.0](https://github.com/sushxnthd/lattice/actions/runs/41112883206/artifacts/13004098404) ZIP SHA256 `028eb4fd513eda9816f7ec804e797a8a50314e925cdb078db59d45e80f4e2529`; [4.2.0](https://github.com/sushxnthd/lattice/actions/runs/41112883206/artifacts/13003454955) ZIP SHA256 `f85d6466f2bd0a5bb98d117f9a0cf5a20cbc6d03cbeaff58ba97d7c51441da0e`. JSON hashes are in original job logs. Installed modern AnyIO 4.13.0 passed all seven frozen public-API cases in isolated local subprocesses, 7/7.

**Negative qualification:** Only after the prospective freeze, issue timeline identified fixing commit `238a340d1237e1d5e7353eec36f7adc03746fc5f`. It modifies **one production file**, the asyncio backend, plus a test and version history. `_core/_tasks.py` Git blob is unchanged between 4.1.0 and 4.2.0: `2f21ea20b13e0653e288161082e503f81162b507`. Backend blob changes `9827e55090640af5c37a8de6db2c0903380267fe` to `e884f564857eb8fa75a8bf401abbd633d52d9df7`. This candidate is **NOT QUALIFIED** as a two-production-source repair. No criteria were retuned. A call-path source file is not necessarily a causally necessary edit.

**Verification and limitations:** Independent local read-only auditor passed 7 tests and checked 7 modern raw case records plus 4 historical cloud summary outcomes. Cloud summaries are transcribed from logs, not claimed as original artifact bytes. PyPI release-wheel SHA was not independently matched to source trees. No real coding-model inference, IR superiority, or powered claim. Historical cohort remains **9 qualified PRs across 7 repositories**; all 89 reserved issues SEALED.

Local SHA-verified reproducibility archive: `lattice_run372_reference_blind_anyio_negative_and_historical_traces.zip`, SHA256 `79f0e91e4fcb5869c200a7ffa26e4069185e2ad4798b511e8a2ba201915489ed` (14 payloads + manifest). Contains raw modern subprocess stdout/stderr, prospective freeze, historical cloud evidence metadata, auditor, tests and full report. GitHub ZIP mirroring pending.

Branch `research/exp003-context-order`; sole PR #9 remains OPEN/DRAFT/UNMERGED. Next: new reference-blind multi-production-source issue and matched real-model IR vs Python/AST-action pilot.
