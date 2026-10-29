# K-SYNTH-1 Run352: independently audited real Qwen pilot

Original completed cloud run: https://github.com/sushxnthd/lattice/actions/runs/40965977369
Artifact ID 12938459387, original ZIP SHA-256 `c95448a5ba0a175ebcf09b24344154999d4f8069d0b0b798e2d81c227e82170f`.
All 46/46 original manifest entries independently SHA-verified; 225 ZIP entries. The original manifest excludes the staged tree: all 89 staged files per arm were separately compared byte-for-byte across arms. The edited production `_api.py` was independently reconstructed from the original historical source, and unchanged `_client.py` was verified against its pinned baseline. Other staged files lack independent pinned baseline hashes.

Qwen2.5-Coder-7B-Instruct Q4_K_M SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, llama.cpp commit `620d2225cc436ab0b001e3200e590e3b286ef9ab`, temperature 0, seed 3322026. Both positive-control gates passed and both genuine model calls completed. The 23 conditional lexical dataflow facts were information-equivalent; all runtime callees remained UNKNOWN.

| Arm | Prompt tokens | Raw actions | Effective | No-op | Targets | Controls |
|---|---:|---:|---:|---:|---:|---:|
| Graph IR | 6021 | 4 | 1 | 3 | 1/3 | 6/6 |
| Python/AST | 6300 | 4 | 1 | 3 | 1/3 | 6/6 |
| Baseline | — | — | 0 | — | 0/3 | 6/6 |

Raw completions differed, but both accepted transactions compiled to **exactly identical source bytes**: `httpx/_api.py` SHA-256 `81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe`; neither edited `_client.py`. The only effective edit was `head(allow_redirects=False -> True)`. IR no-ops: get/options/post. Python/AST no-ops: get/options/request. The original compiler accepted these no-ops; do not retroactively change acceptance.

Original isolated oracle: API HEAD target repaired, client HEAD and held-out client redirect targets failed, all six controls passed. Zero paired outcome discordances. Python/AST prompt had 279 more actual tokens (4.63%), so the arms are not token-matched. This is a negative/equal pilot, **not** evidence of semantic-IR superiority or a powered comparison.

New read-only counterfactual source experiment: all 16 subsets of each arm's four edits (32 subsets total) were independently compiled by a byte-offset AST-located source transformer, with no model-authored code executed. Each arm produced exactly two distinct source byte states: the original baseline without the HEAD edit and the identical HEAD-patched source with it. All 14 local tests passed, including malformed/duplicate/stale actions and provenance checks. Original oracle records were audited for expected/observed consistency, not rerun on the host.

Scientific limitations: The original artifact manifest did not hash the entire staged tree. This is one historical HTTPX task, not a new independent repair. The cohort remains 8 qualified PRs across 7 repositories. Full historical GitHub ZIP mirroring remains incomplete. No significance, runtime-MUST claim, or breakthrough.

Full local SHA-verified Run352 archive: `lattice_run352_independent_model_equivalence_audit.zip`, SHA-256 `b231103150f70e699b62f48d9cecb7a78f43e8bd24e98ae544d8b6e0d3109876` (includes original cloud ZIP, Run351 parent, full auditor, tests, outputs, report and protocol). This archive is preserved as a conversation artifact, not claimed mirrored to GitHub.

Next: freeze genuine Jinja #1242 and HTTPcore #882 paired inference, actual tokenizer balancing, source-only localization, shared compiler, isolated oracle, effective-edit metrics and repository-clustered planning. One K-SYNTH-1 kernel; PR #9 open/draft/unmerged; 89 boundary issues sealed.
