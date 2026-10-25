# Run238 — Independent pipx functional oracle and multi-file action audit

Date: 2026-10-25. This is a **secondary, post-hoc diagnostic** of the unchanged Run234 Qwen2.5-Coder-7B-Instruct Q4_K_M outputs. The original functional primary endpoint remains **NOT_EVALUATED** for all 24 completions. The 89 boundary issues remain untouched.

## Independently rechecked authentic artifacts

Verified the SHA-256 top-level archive manifest and all twelve original per-repository manifests; re-read the raw 24 model responses and original compiler traces.

| Metric | Semantic IR | Annotated Python |
|---|---:|---:|
| Genuine completions | 12 | 12 |
| Valid JSON | 11 | 10 |
| Frozen compiler accepted | 7 | 5 |
| Compiler accepted and Git patch check passed | 7 | 4 |
| Attempted 2+ file edits | 1 | 1 |
| **Accepted 2+ file edits** | **0** | **0** |

Only Harmonica #510 attempted edits in more than one file (three per arm); both outputs were compiler-rejected. This **does not prove** the other tasks intrinsically require multi-file changes. It does show that Run234 offers zero accepted multi-file edits, much less demonstrated functional multi-file repairs. The earlier paired compiler-acceptance p=0.625 is not evidence of representation superiority.

## New executable real-issue functional witness

For pypa/pipx #1186, reconstructed original src/pipx/interpreter.py from the frozen target and compiler-accepted model output. Verified original SHA-256 `ee8103943178abdfd997d54e2e3bcbc0fa0dcc230cb554b688ec5384b84ce195`. Executed the original, genuine semantic-IR model edit, and independently written minimal reference through the same isolated CPython function evaluator with a deterministic launcher subprocess stub. Tested prefixed and numeric Python versions, missing launcher, and empty/absent version.

| Source | Passed post-hoc necessary checks |
|---|---:|
| Original pinned source | 7/10 |
| Genuine semantic-IR edit (compiler accepted, Git patch applies) | **7/10** |
| Independent calibration reference | **10/10** |

The model left the incorrect `-python3.11` launcher argument unchanged and appended an unreachable duplicate block after unconditional return. The reference is a positive control, **not a model completion or proof of a full upstream fix**. This is a post-hoc necessary-condition oracle, not the frozen primary endpoint or a complete integration test.

## New representation-equivalence artifact

Implemented a byte-reversible literal Python-source presentation of the exact frozen semantic facts, replacing JSON-stringified `# AST_TARGET` source. It preserves hashes, AST target IDs, source excerpts and metadata. Verified `parse(render(facts)) == facts` on all twelve frozen repositories, plus Unicode/CRLF/embedded-marker adversarial cases. This is a candidate source-view baseline, not yet an unrestricted Python edit interface or a new capable-model comparison.

## Exact statistical sensitivity

For independent issue pairs, hypothetical discordance 30%, two-sided exact McNemar alpha=.05: at conditional IR win probability .65, power is 72.3% for 258 pairs and 80.0% for 306. At .60, corresponding power is 37.7% and 44.4%. These are assumptions, **not measured functional effects**. Clustering requires more: the previous Run234 simulation suggested about 440 independent repositories and 1,089 issues for 80% power at the smaller assumed advantage under its assumptions.

## Scientific decision

Next: freeze genuinely actionable multi-file issues with executable functional oracles **before inference**, establish red/green and seeded-bug controls, use a truly ordinary Python-source baseline with the same edit authority/compiler/verifier/output grammar, and execute a new prospective strong-open-model comparison. Enforce byte-faithful Git patch application and declaration/descriptor safety in both arms. Do not use compiler acceptance as a proxy for functional success. Do not unseal the 89 boundary issues without a frozen mechanism prediction.

Local reproducibility bundle: `lattice_run238_functional_oracle_and_multifile_audit.zip`, containing independent functional traces, structural audit, exact-power computation, reversible-view code, ten passing regression tests and SHA-256 manifest. Original Run237 raw evidence is an immutable input and is not modified. No new model inference was performed in Run238.