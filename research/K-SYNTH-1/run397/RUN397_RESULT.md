# K-SYNTH-1 Run397: real-source binding-time provenance

Date: 2026-11-01 IST. Historical Rich #3176 exploratory mechanism study; **not** an unseen repair, new coding-model inference, or evidence of IR superiority.

Reused two SHA-pinned real production files from Run389: `rich/_wrap.py` SHA-256 `c5f57ff6dd1283aaf38a69ab0ebbbc7c25665256a56007072c37eb2599db6f04`, `rich/cells.py` SHA-256 `eb6ef3b49b3dcce2fedfc1c9ee45c17ab47e813f0a05f602f14cc4c0c243618a`. Eight isolated CPython `-I -S` interventions exercised 30 frozen text/width cases each: **240 identical functional outputs**, but different wrapper call traces.

| Intervention | cell_len calls | cached_cell_len calls | chop_cells calls |
|---|---:|---:|---:|
| none | 0 | 0 | 0 |
| rebind cells.cell_len after _wrap import | 1 | 0 | 0 |
| rebind _wrap.cell_len after import | 150 | 0 | 0 |
| rebind cells.cached_cell_len after definition | 0 | 0 | 0 |
| rebind cells.chop_cells after _wrap import | 0 | 0 | 0 |
| rebind _wrap.chop_cells after import | 0 | 0 | 20 |
| rebind cells.cell_len before _wrap import | 151 | 0 | 0 |
| explicit cached argument override | 0 | 1 | 0 |

A read-only AST provenance extractor recorded **20 conditional binding events and five UNKNOWN caveats**. Critical facts independently verified: `from .cells import cell_len, chop_cells` snapshots module-import-time objects; `cell_len(..., _cell_len=cached_cell_len)` captures a function-definition-time default; `divide_line` assigns a call-time local alias. A syntactic call graph alone does not determine post-monkeypatch targets. The result is ordinary Python binding semantics, **not a universal MUST_CALL theorem**.

An independent auditor verified source hashes, 240 bounded outputs, call-count relationships and four critical facts (764 reported checks; zero disagreements). **12/12 regression/adversarial tests passed**. Two frozen historical Rich repair prompts use identical task facts, original source, edit authority, 20 provenance records and five caveats, represented as JSON IR versus ordinary Python AST literal; independent decoding verified exact fact parity. Prompt SHA-256 IR `a2da154e519cca1f36fde53e87be1a743526e2d3318a766f9b7c072be3c1006a`, Python `101744453234535c945bd79372d5b57b81cd5985f5c8b02e694e04055345efc0`. **No model inference occurred.**

**Environment limitation:** Studied production files are exact historical bytes, but the test uses a bundled installed `_loop.py` and a restricted test-only Unicode width table, not the historical complete dependency tree. It is a bounded binding intervention, not a full production oracle.

Local 23-payload SHA-verified archive `lattice_run397_binding_time_provenance_and_matched_prompt_freeze.zip` SHA-256 `32d44275f747fda91c15d2204797c49e93534bad6e392dbffce975ead7a1f087`; clean extraction replayed five scripts, six critical outputs and 12 tests. Full ZIP GitHub mirroring remains pending.

All 89 reserved boundary issues sealed. Sole PR #9 remains draft/unmerged. Next: unseen issue-first multi-source qualification and genuinely paired strong open-model functional evaluation.
