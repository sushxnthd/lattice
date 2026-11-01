# K-SYNTH-1 Run405: issue-first pytest #14997 prospective qualification

Frozen 2026-11-01 IST before examining any reference fix, linked repair PR, source diff, or source-localization hints. Issue-only source: https://github.com/pytest-dev/pytest/issues/14997 (reported 2026-09-10; closed 2026-09-21).

**Question:** does pytest 9.1.1 lose subpackage conftest fixtures when CLI file arguments from a sibling package are interleaved with a top-level file? A two-production-source *repair* is not assumed. This is an independent candidate, not part of the sealed 89 boundary issues.

**Exact historical source commits:** pytest 9.0.3 peeled release commit `a7d58d7a21b78581e636bbbdea13c66ad1657c1e` (negative control); pytest 9.1.1 peeled release commit `cf470ec0bf7eb89cd97dd56df4859eae5db46447` (reported failing baseline). These commit identities were independently frozen in Run400. The workflow checks out each SHA and asserts `git rev-parse HEAD`, installs it, logs environment and source commit.

**Frozen independent oracle:** `run405_issue14997_oracle.py`. Two independent subpackages, fixtures `widget=31` and `gadget=47`, top-level sibling files, six disjoint interleaving sequences P1–P3 and H1–H3, six noninterleaved controls C1–C6. Each runs in a separate pytest subprocess with plugin autoload disabled, fixed hash seed, exact command, exit code, full stdout/stderr, elapsed time and source-file SHA-256. No tests are modified after baseline results.

**Eligibility:** reported 9.1.1 baseline must FAIL at least 2/3 public targets and at least 2/3 heldout targets while PASSING 6/6 controls. The 9.0.3 negative control should PASS 12/12. A later exact historical reference repair, if independently identified, must PASS all 12. A *qualified two-production-source* case additionally requires prospectively fixed source-ablations and separately verified neutral compatibility shims, with each production component behaviorally necessary under joint target-plus-control outcomes. Import failures alone are insufficient. If reference, ablations, or source necessity do not satisfy the frozen contract, label NOT QUALIFIED; never retune.

**Leakage policy:** Only P1–P3 and the public source facts may be shown to a coding model. H1–H3, controls and the reference fix are withheld from model prompts. A functional model experiment is prohibited until full independent qualification. No reference-derived localization, no model code executed on the host.

**Preflight only:** installed pytest 9.0.2 on local Python 3.13 passed 12/12 subprocesses, including 6/6 controls. This is neither the pinned 9.0.3 negative control nor 9.1.1 regression evidence.

**State:** candidate prospectively frozen, NOT QUALIFIED pending pinned baseline/control cloud artifacts. Two previously qualified real tasks remain Flask PR6096 and urllib3 PR5071. No model inference or representation advantage claimed. The sole K-SYNTH-1 kernel, branch `research/exp003-context-order`, open/draft/unmerged PR #9, and all 89 SEALED issues remain unchanged.
