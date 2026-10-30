# K-SYNTH-1 Run368: frozen HTTPX #1532 historical source-factorial experiment

Frozen 2026-10-30 UTC **before executing historical source combinations**. This candidate was selected after inspecting the upstream PR patch; it is **reference-informed** and must **never** be called reference-blind model evaluation or pooled with the prospectively blind model cohort.

- Repository: https://github.com/encode/httpx
- PR: https://github.com/encode/httpx/pull/1532 (merged 2021-03-24)
- Exact baseline (merge parent): `ea5ffce14f6a1430a3cb89eae573b388047f3f2c`
- Exact reference merge: `6cb1672459b0c1386cb36b89a92b87419fdc478c`
- Two production files only: `httpx/_client.py`, `httpx/_models.py`
- Baseline Git blob IDs: client `3465a10b758830201f6b7406ffef0026a3b79758`; models `2d11888254a03491d646c9ce07cec60502f1f59d`
- Reference Git blob IDs: client `da38a14346bcc079daccb171702b295fd1593166`; models `83deb9a243530f0a78038805b8143a249cd45bbb`
- All other historical files must remain at baseline. No upstream tests are substituted into source arms.

Four isolated source arms: client0_models0, client1_models0, client0_models1, client1_models1. Each executes 13 frozen public API cases: three public targets, three heldout targets and seven baseline nonregression controls. All 52 observations must execute; pre-oracle import failure is **INCONCLUSIVE**, not a zero score.

Target cases (ID / API / base / relative / expected):
- P01 URL.join /path/to/somewhere + /somewhere-else => /somewhere-else
- P02 URL.join /path/to/somewhere + somewhere-else => /path/to/somewhere-else
- P03 Client.build_request https://example.org/some/path + /sub:path => https://example.org/some/path/sub:path
- H01 URL.join /path/to/somewhere + ../somewhere-else => /path/somewhere-else
- H02 URL.join /path/to/somewhere + ../../somewhere-else => /somewhere-else
- H03 Client.build_request https://example.org/some/path + /testing:123 => https://example.org/some/path/testing:123

Controls:
- C01 URL.join https://example.org/a/b + ../c => https://example.org/c
- C02 URL.join https://example.org/a/b + /c => https://example.org/c
- C03 Client.build_request https://example.org/a/b + c => https://example.org/a/b/c
- C04 Client.build_request https://example.org/a/b + /c => https://example.org/a/b/c
- C05 Client.build_request https://example.org/a/b + https://other.org/x => https://other.org/x
- C06 URL.join https://example.org/a/b + https://other.org/x => https://other.org/x
- C07 URL.join https://example.org/a/b + #frag => https://example.org/a/b#frag

**Prospective qualification:** baseline 7/7 controls; baseline <6/6 targets; full reference 6/6 targets + 7/7 controls; each one-file reference arm <6/6 targets; all arms 7/7 controls; no pre-oracle failures. Record casewise interactions `Y11-Y10-Y01+Y00` independently from nonlinear aggregate ALL_PASS. Do not infer semantic coupling from aggregate success.

Model inference: NONE. This run is historical reference qualification, not a paired IR-vs-Python/AST model comparison. Do not retune failures or promote post-outcome controls. Preserve SHA-256 of exact prompts/runner/source/artifacts and isolate untrusted historical code in a no-network, read-only, unprivileged Docker container. Historical PR duplicates must be checked against the existing eight-PR cohort before promotion. One canonical K-SYNTH-1 kernel; only branch `research/exp003-context-order`; sole open/draft/unmerged PR #9; all 89 reserved boundary issues SEALED.
