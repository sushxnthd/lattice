# K-SYNTH-1 Run343 — prospective Click PR1604 freeze

**Freeze before reference source/patch inspection and before any historical qualification execution.** This commit SHA is the timestamped preregistration; no reference source was inspected when authored.

Candidate: pallets/click PR #1604, merged; issue #729. PR-reported baseline `6271cee2e8b2cf9a392377271bc9ed8345ce77c8`, head `3d3ea9c64420fd8978a41ce8b4db3ac2d245849c`, merge `82ca854f587af919789a9baae9a732fe0ce0052c`. Direct ancestry UNVERIFIED. Two production files: `src/click/core.py` and `src/click/parser.py`; baseline Git blob SHAs `9651deb652383b9480a5e91e92b3f98e1395f5bd` and `158abb0dea2a8ee6f20e8b5cd8063aa08160b157`. No reference blob opened.

**Immutable locally authored source commitments:**
- `FROZEN_CLICK_PROTOCOL.md` SHA-256 `b90f142e29a68e20a4c03d1a142074016d08849c708a6d37641cb8cef4d1bc5a`
- `run343_click_oracle.py` SHA-256 `903b306fca3f2fb03eb8277cc6d34631dd1edde032aa665f5b013c9045bdf397`
- `qualified_tasks.json` SHA-256 `b5c3df2fdd2811dcf1d089f9fb0b3eab9ee0e7931082ff9d45c16fc36c33a9ad`

Four source arms 00,10,01,11 plus identity ABI negative control. Exactly 14 frozen CLI cases: public T01–T02, heldout T03–T06, nonregression C01–C08. Each runs under isolated historical Python 3.10 with source Git-blob verification and complete stdout/error trace. Frozen PASS iff baseline fails ≥1 target and passes 8/8 controls; full reference passes 6/6 targets and 8/8 controls; each single-source arm fails ≥1 target and preserves all controls; identity ABI negative is byte/outcome-equivalent to baseline; no transport censoring, unexplained interface mismatch, or static signature drift in the four predeclared cross-module methods. Otherwise NOT QUALIFIED. Post-outcome adapters may be diagnostic but cannot rescue the frozen decision.

This is reference-patch source qualification only, **not** model inference, prospective model success, semantic IR superiority, or powered significance. Historical ledger is deduplicated by (repo, PR) and Run342 h11 #115 is not a new task. Keep one K-SYNTH-1 kernel, branch research/exp003-context-order, only PR #9 OPEN/DRAFT/UNMERGED; 89 reserved boundary issues SEALED.
