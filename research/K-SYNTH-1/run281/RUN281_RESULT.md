# K-SYNTH-1 Run281 | Original HTTPcore replay censored; conditional semantic-risk experiment

Date: 2026-10-27 IST. Canonical branch `research/exp003-context-order`; sole PR #9 OPEN/DRAFT/UNMERGED. All 89 reserved boundary issues SEALED.

## Independent recovery of original Run280 evidence

GitHub Actions [40430591378](https://github.com/sushxnthd/lattice/actions/runs/40430591378) completed at the workflow level. Original artifact ID **12701239726**, ZIP SHA256 `2f4b9a501d3cf9c4bcfa893c94adf34c1beba588a2135ecf283dec5f80b25aa2` matches the GitHub artifact digest. All **10/10 original SHA256 manifest entries** verified. Frozen Run279 oracle SHA256 `6d1fbb5d18aa7b58da802fb34f43ec6a5efcfc7a3842049df2fb02f18d2e2e96`, frozen spec SHA256 `769d660400e39511bfbc80c93b2c9688ca555fc037903f80d82436b0895f60cd`, raw results SHA256 `cf6d50774a416db2f3adc92c5b279998241d2610cb13dc45f73385b08b004e2a`.

**All four source configurations failed during import, before ANY functional check.** The pinned source imports `certifi` in `httpcore/_ssl.py`, but the workflow installed only h11/h2/sniffio. Each configuration exited with `ModuleNotFoundError: No module named 'certifi'`. The 40 mechanically failed case records have null observations; **zero actual functional tests ran**. Do not call these 40 repair failures or a scientific qualification failure.

The pinned upstream [pyproject.toml](https://github.com/encode/httpcore/blob/5974b03c7df89d3ee4e23779900d5349d550753c/pyproject.toml) declares certifi, h11>=0.16, and optional asyncio/anyio. New [Run281 replay](https://github.com/sushxnthd/lattice/actions/runs/40438772162) was launched (commit `72ac7f0`), installing complete upstream-declared dependencies while retaining the **exact unchanged Run279 frozen 4x10 oracle, source blobs, and expected outcomes**. It was queued at last check. Pending does not mean failure; HTTPcore is not promoted until original frozen checks actually execute and pass.

## New independently tested conditional semantic science

Source-provenance audit confirmed both HTTPcore sync and async production changes replace `len([connection.is_idle() for connection in self._connections])` with `sum(connection.is_idle() for connection in self._connections)`. Under **explicit, not inferred** assumptions (finite stable collection, pure Boolean predicate, integer threshold), for total `n`, true count `i`, threshold `k`, old/new disagree exactly iff `i <= k < n`. Original is true and corrected is false in every such discordance.

The executable [minimal contract](./run281_minimal_contract.py) and complete local science suite evaluated **53,247 independent CPython Boolean vectors/thresholds**: **20,481 predicted disagreements, zero mismatches**. Non-Boolean `[2,2]` at threshold 3 reverses direction, proving the Boolean precondition is necessary. An additional exact binomial-risk calculation (hypothetical IID Boolean p, NOT observed workloads) was independently checked by enumeration. **13/13 local tests passed**. Unsupported assumptions produce `UNKNOWN`. This is expression-level conditional semantics, not a general sound Python IR, and not evidence of semantic representation superiority.

## Research integrity

Qualified real issue cohort remains **three**: Flask PR6096, urllib3 PR5071, Werkzeug PR3136. HTTPcore PR1000 pending; Werkzeug PR2860 and PR2535 remain unqualified. No new coding-model repair, powered significance, or breakthrough. Complete historical source/ZIP GitHub mirroring remains outstanding; local SHA-verified archive preserved. All 89 reserved boundary issues remain sealed.
