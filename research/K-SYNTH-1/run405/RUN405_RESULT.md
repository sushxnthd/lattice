# K-SYNTH-1 Run405: issue-first pytest #14997 frozen qualification

Date: 2026-11-01 IST. No semantic-IR superiority claim.

Selected [pytest issue #14997](https://github.com/pytest-dev/pytest/issues/14997) from its issue description only, before examining any reference fix, linked PR or gold localization. Reports a pytest 9.1.1 regression in subpackage conftest fixture resolution when file arguments are interleaved with sibling top-level files.

**Frozen exact source:** pytest 9.0.3 peeled commit `a7d58d7a21b78581e636bbbdea13c66ad1657c1e`; pytest 9.1.1 peeled commit `cf470ec0bf7eb89cd97dd56df4859eae5db46447`. The committed [oracle](run405_issue14997_oracle.py) and [protocol](PROTOCOL_PYTEST14997_PRE_REFERENCE.md) freeze 3 public targets, 3 heldout targets, and 6 controls. Eligibility requires at least 2/3 failures in each target partition on 9.1.1 and all six controls passing. Later qualification requires full-reference 12/12 success and **joint target-plus-control behavioral necessity of both production source edits**, with independent neutral-shim checks. Import aborts alone are insufficient.

**Executed local preflight:** installed pytest 9.0.2 / Python 3.13 passed all **12/12** isolated CPython pytest subprocesses (3/3 public, 3/3 heldout, 6/6 controls). A separate independent auditor reconstructed all 14 source files and reexecuted **12/12** cases with zero status or exit-code disagreements. **13/13** local tests passed. This 9.0.2 preflight is NOT the pinned 9.0.3 negative control and does not establish the 9.1.1 regression.

**Cloud:** committed [two-version pinned Actions workflow](../../../.github/workflows/k-synth-run405-pytest14997.yml) on `research/exp003-context-order`, asserting exact git SHAs and retaining full stdout/stderr, source hashes, environment and artifacts. The original cloud results have **not yet been independently recovered or verified**; no completed cloud run is claimed.

Local conversation archive: 11 entries, 10 SHA-256-verified payloads, clean-extraction 13/13 tests. ZIP SHA-256 `7632d1605ff54d085e96ff5cf9be3dec116f05c0202fdd934ee8920d0b8553a3`.

**Status:** New issue-first real candidate frozen, **NOT QUALIFIED** pending baseline/reference/ablations. Historical qualified real multi-source count remains **2** (Flask PR6096, urllib3 PR5071). No new model inference or powered IR superiority. All 89 reserved boundary issues remain SEALED. One K-SYNTH-1 kernel; PR #9 remains open/draft/unmerged.
