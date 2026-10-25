# Run251 — Functional qualification and semantic-fact encoding

2026-10-25. **No new model inference and no representation advantage established.** Full local reproducibility archive: `lattice_run251_qualified_multifile_semantic_science.zip` (SHA-256 `c197daa6bc5fc3dbf86faf3c0ce1c5d8dcfd184f1c49f9d7dd6335ae78608998`, 65 SHA-256-verified files). The complete code and archive are currently local, not mirrored to GitHub.

## Historical cohort exclusion

Independent re-audit of frozen Run237: 12 rows, **11 unique issue IDs** (`cuthbertlab__music21-1775` duplicated). All 12 original and all 24 model-arm functional statuses were `NOT_EVALUATED`. **Zero** rows have the required executable baseline-negative/reference-positive functional controls. Compiler acceptance and patch application do not establish functional repair. This is a benchmark-validity exclusion, not a model-failure count.

## New prospective synthetic controls

Constructed three **synthetic**, separate, multi-file Python packages: `access`, `billing`, `stream`. Each has two independently mutated editable files, read-only dependencies, two public tests and two withheld adversarial tests. **3/3** tasks qualify: baseline fails in both test splits and reference passes in both. Across all individual tests, baselines fail 7/12 and references pass **12/12**. These are **not** independently pinned real GitHub issues and cannot be counted toward the adequately powered main study.

Implemented source-rederived static semantic facts with cross-file imported-symbol candidates, syntactic call candidates, conservative intra-procedural may-reaching definitions, CFG possibility edges, and explicit unknowns. It is not a sound general Python semantic/dataflow IR. Two frozen input views decode to exactly the same source and semantic facts: JSON semantic-fact IR and Python source annotated with the same facts. This is a **fact-encoding** contrast, not evidence of a semantic-IR advantage over ordinary Python. Six Qwen2.5-Coder-7B-Instruct Q4_K_M requests were frozen before inference, seed 251000–251002, temperature 0, max completion 4096, with exact prompt SHA-256 digests in the local archive. No raw completions or actual tokenizer counts were obtained.

The independent strict native-Python full-file evaluator rejects unauthorized paths, duplicates, framing errors, syntax errors and read-only changes. **20/20 regression tests passed.** Untrusted candidate execution requires a disposable sandbox.

## Paired power, hypothetical assumptions

Exact two-sided McNemar alpha=.05: at discordance q=.30 and conditional IR win p=.65, **306 independent pairs** reach 80% power; 258 pairs provide **72.30%**. At p=.60, **681 independent pairs** are needed. Cluster-aware simulations (4 tasks/repo, ICC=.15, 4000 replications/grid point) first cross 80% on a coarse grid at 400 tasks/100 repositories (p=.65) and 800 tasks/200 repositories (p=.60). These are **sensitivity assumptions**, not observed effects or guaranteed requirements.

**Next:** qualify genuinely independent public-repository multi-file tasks with pinned commits and executable controls, then run matched capable-model functional inference. Keep the 89 sealed boundary issues untouched; no mechanism or boundary advantage claim. The local archive and source remain preserved; GitHub mirroring of full artifacts is outstanding.