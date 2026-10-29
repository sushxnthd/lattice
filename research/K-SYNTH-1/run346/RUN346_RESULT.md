# K-SYNTH-1 Run346 — independent original-model audit and semantic-IR construct validity

**2026-10-29 UTC.** Canonical branch research/exp003-context-order; sole PR #9 OPEN/DRAFT/UNMERGED; all 89 reserved boundary issues SEALED.

## Original evidence independently verified

Recovered the ORIGINAL Run335 Qwen2.5-Coder-7B Q4_K_M inference artifact from the Run336 SHA-verified archive. Verified **9/9 outer manifest entries and 44/44 original inner manifest entries**. Recomputed all **27 original functional oracle observations** from observed/expected traces and error fields. Original baseline: 0/3 repair targets and 6/6 controls; IR: 1/3 and 6/6; ordinary Python/AST: 1/3 and 6/6. Both real model completions and both binding-gate completions were byte-identical across representations. Both compiler transactions were accepted and produced identical patched-source SHA-256 values. No new model inference or untrusted model-code execution occurred in this audit.

Original model SHA-256: 509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c. Both arms used the same seed 3322026, temperature 0, completion limit 768, response schema, source, issue and edit authority.

## Construct-validity result

The original 31 real candidate facts are **exactly equivalent after normalizing only the IR_DEFAULT / PY_AST_DEFAULT labels and AST slot spelling**. Both presentations contain the same lexical MAY_FORWARD hints. All **31/31** candidates explicitly report runtime callee **UNKNOWN** and runtime effect **UNKNOWN**. A new independent Python AST checker verified **28/28 lexical parameter-to-keyword forwarding observations** at the recorded production-source lines, with three candidates having no forwarding observation. These are lexical **MAY** edges, not runtime MUST edges: **zero runtime callees or effects were certified**.

Therefore this original paired experiment tests the serialization of an information-equivalent lexical candidate table, **not the benefit of a distinct verified semantic/dataflow IR**. This does not establish that a stronger IR cannot help. A runtime monkeypatch counterexample shows why syntactic forwarding alone cannot soundly establish an open-world runtime callee.

Real model prompt token counts were **4,088 IR versus 4,208 Python/AST** (120 tokens, 2.94% difference); the gate was 459 versus 463. Generation settings and maximum completion tokens were equal, but prompt lengths were **not token-matched**. The two completions nevertheless matched exactly.

## Exact McNemar planning and clustering

An independent exact two-sided conditional-binomial McNemar calculation (alpha 0.05, discordance 0.30) confirms historical nominal assumptions: **n=306, conditional IR win 0.65 -> 80.04% power**; **n=681, conditional IR win 0.60 -> 80.05% power**, assuming independent issues. With four issues per repository and *hypothetical* ICC 0.10, design effect 1.30 yields approximately **398 optimistic or 886 moderate issues**. This is sensitivity analysis, not an empirical ICC or a substitute for cluster-robust simulation.

## Validation and limitations

Nine local tests passed, including rejection of tampered original SHA manifests, corrupted lexical forwarding values/locations/callees, changed candidate facts, and a trusted runtime-monkeypatch counterexample. The full independent auditor, exact power calculation, adversarial tests, 28-edge evidence ledger and original Run336/Run335 nested ZIP are retained in the SHA-verified local Run346 archive. The portable read-only GitHub gate reproduces the original manifest, candidate, compiler, model-output and oracle checks.

Archived staged source is **post-model-edit**, not independently reconstructed pre-edit source. No new model inference, source qualification, powered representation advantage or breakthrough is claimed. Historical cohort remains **8 distinct source-qualified PRs across 7 repositories**, not 8 model repairs.

**Next:** Implement an independently verified, soundness-scoped semantic/dataflow IR with explicit UNKNOWN; compare against information-equivalent ordinary Python/AST actions using the same model, token-budget controls, compiler and isolated oracle. Recruit independent repositories and retain negative-result stopping criteria.

Original experiment: https://github.com/sushxnthd/lattice/actions/runs/40831990253
