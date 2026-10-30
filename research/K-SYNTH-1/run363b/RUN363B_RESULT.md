# K-SYNTH-1 Run363b: original Flask factorial recovered; source-import confound

**2026-10-30 UTC. Frozen verdict: INCONCLUSIVE, not QUALIFIED.** No criteria were changed.

Original [Run363 workflow](https://github.com/sushxnthd/lattice/actions/runs/41044116862) completed SUCCESS at commit `bab4d5b0da4b630f382ac9a60cd6480df3aff29e`. Original [artifact 12970644685](https://github.com/sushxnthd/lattice/actions/runs/41044116862/artifacts/12970644685) ZIP SHA256: `deff0b0a86093b6822dbd46b93239a8e3e4a66979948a7d05110f64a75ae111a` (matches Actions reported upload digest). All **20/20** original manifest entries independently SHA-verified; all three base/head source Git blobs matched the prospective freeze.

Original 8 x 12 case records:

| Changed files (app, ctx, helpers bits) | Mask | Executed cases | Targets | Controls |
|---|---:|---:|---:|---:|
| none | 0 | 12 | 0/6 | 6/6 |
| app | 1 | 0 | N/A | N/A |
| ctx | 2 | 0 | N/A | N/A |
| app + ctx | 3 | 0 | N/A | N/A |
| helpers | 4 | 12 | 0/6 | 6/6 |
| app + helpers | 5 | 12 | 6/6 | 6/6 |
| ctx + helpers | 6 | 12 | 0/6 | 6/6 |
| all three | 7 | 12 | 6/6 | 6/6 |

The 36 missing observations are genuine **pre-oracle Python ImportErrors**, not functional failures. Original stderr shows both new `app.py` and new `ctx.py` import `_CollectErrors` from `helpers.py`, absent in historical baseline helpers. Independent GitHub source inspection pinned the exact imports to head app.py line 39, head ctx.py line 13 and declaration to head helpers.py line 642; all three absent at baseline. Under ordinary direct import semantics (without import hooks or dynamic injection), importability is `helpers_new OR (NOT app_new AND NOT ctx_new)`. This predicts all 8 observed importability outcomes exactly. A separate self-authored subprocess import fixture verified all eight cases. Dynamic import hooks, mutation and other runtime effects remain UNKNOWN.

Because the **prospectively frozen protocol requires 12 observed outcomes in all eight variants**, the result is INCONCLUSIVE. Do not score the 36 import failures as incorrect functional cases or retroactively change the frozen contract. The finite observation that app+helpers passes 12/12 does not prove ctx changes are universally unnecessary. This is a concrete import-ABI dependency and construct-validity limitation, not semantic IR superiority.

**Status:** original eight qualified PRs across seven repositories unchanged; zero new model inference; 89 reserved issues sealed. Sole PR #9 remains open/draft/unmerged. Next: recruit another independent production task, freeze a source-factorial oracle that separately reports importability and runtime behavior, and retain a fair ordinary AST-action baseline.