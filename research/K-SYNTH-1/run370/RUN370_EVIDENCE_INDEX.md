# Run370 evidence integrity index

**Date:** 2026-10-30 UTC. **Qualification:** INCONCLUSIVE / BASE_MISMATCH. No historical full-tree qualification and no real-model inference.

## Immutable pre-reference evidence
- Prospective freeze commit: `0933976ba3e1443f29176122a453f15b1ca5d464`
- Freeze Git blob: `a48357763948261bbd39fc420c7e1db5cbe70bf8`
- Upstream 0.14.7 sync pool Git blob: `32bc77895191c35e0f155c913462395f1b2067d6`
- Upstream 0.14.7 async pool Git blob: `ae3854b1815540625c1dffa1b8503fd9b9f07f44`
- Upstream 0.14.7 synchronization Git blob: `e7cb1d60c1a6043555e2a9b4f0a2d85089255c7a`
- All three pre-fix files were mirrored byte-identically to `pre_fix_httpcore_0_14_7/httpcore/`.

## Local reproducibility archive
`lattice_run370_reference_blind_freeze_and_pool_ownership_counterexamples.zip`
SHA-256 `890c0105692afece2325f05e39eb6c2f593eb27b99ecf481c69dbf72c4cf454d`.
Contains 17 entries; every ZIP entry was independently checked against its local source SHA-256.

Key payload SHA-256:
- `run370_raw_model_check.json`: `99474036e9f17ea3a2e95cb775dd6844267609206dbc7d63a8695b5042083111`
- `run370_event_raw.json`: `d09b290d6120a5b51e7640ae50eb6698eaad2037e55c14d5a7fd412518b02fa8`
- `run370_guard_ablation_raw.json`: `294ea6c5eb63137e68c10a8e1c3bce733e93b069741b0934a5291eac1ef3e448`
- `run370_pool_ownership_model.py`: `4e917cadf6375992f3f24d8a9999d6e998cd3b1685544f539ee144eb36f3e562`
- `run370_independent_audit.py`: `c252402d940d4376a5e05442b92a8ee73da5dc17255d345d5b4b2da71deb822d`
- `run370_event_boundary_replay.py`: `f1fd418e8bfe3372bc0041b24f4cf1c2bde9ee65d2df2f93c8e285913894efb8`
- `run370_post_reference_guard_ablation.py`: `b8837a0bdf78a2e0975a230e61fabd6dd5b368312b55b4364232cc39720c6293`
- `test_run370.py`: `81b8f5f0f7df54e5fa93be3134c60b14b1af12cf434e5fd313e46a6815f0e0e2`

Independent replay: 3 graph modes, 3 fresh-process functional executions, 14/14 local tests. The complete 16-file per-payload SHA manifest is inside the ZIP. The ZIP itself has not been uploaded to GitHub; historical full ZIP mirroring remains incomplete. The minimal executable bounded witness is committed and Git-blob-identical to the local tested version.

All 89 reserved boundary issues remain sealed. PR #9 stays the sole open, draft, unmerged PR.
