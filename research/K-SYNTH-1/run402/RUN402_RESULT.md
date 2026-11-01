# K-SYNTH-1 Run402: exact same-runner crossover and executable dual-edit-language pilot

Date: 2026-11-01 UTC. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole open/draft/unmerged PR #9. All 89 reserved boundary issues remain sealed.

## Original failure preserved; corrected experiment succeeded

Original prospectively frozen crossover Actions [41257605463](https://github.com/sushxnthd/lattice/actions/runs/41257605463) failed in both Python 3.13 and 3.14 before the first performance observation. Both original ZIP artifacts were independently SHA-256 verified: Python 3.13 `ae9724c6b31edcfc2c8276eca64dbdee703a627e48924ba26dce7f31a2365db9`; Python 3.14 `6ddafd7af0599e3df1c79a5657920a2c52aafd423f1fe307b632afb368ca4921`. The source used `Path(venv_python).resolve()`, following the symlink to the system interpreter and losing the virtual environment; `import pytest` failed. An independent local symlink-venv counterexample reproduced the mechanism. The corrected script preserves the lexical absolute venv path with `os.path.abspath`. This is an infrastructure correction, not an alteration of the frozen performance acceptance threshold.

Corrected Actions [41261642563](https://github.com/sushxnthd/lattice/actions/runs/41261642563) **completed successfully in both Python versions**. GitHub artifact ZIP SHA-256: Python 3.13 `1d7b6a860e12f2d6daee3020c29b2a7f26f8da09185be1f4490334b6924a7edc`; Python 3.14 `43dd26d5ff706753b91d070367a9f06b42c4e946fb676ef09f16d3274a4aaf3e`. Independent read-only audit reconstructed all 348 source hashes and verified **134,400 exact collected node IDs across 120 successful isolated pytest collection calls**, the ABBA/BAAB order, eight measured observations per version per workload, pinned package versions, internal file SHA manifests and all medians. **135,296 checks; zero disagreements.**

| Python | Modules | pytest 9.1.1 / 9.0.3 median wall time | Block-geometric ratio |
|---|---:|---:|---:|
| 3.13 | 8 | 0.9674 | 0.9677 |
| 3.13 | 32 | 1.0528 | 1.0444 |
| 3.13 | 128 | 1.5664 | 1.5670 |
| 3.14 | 8 | 0.9804 | 0.9404 |
| 3.14 | 32 | 1.0381 | 1.0370 |
| 3.14 | 128 | 1.4385 | 1.4402 |

**Original Run400 qualification remains NONREPRODUCING / NOT QUALIFIED.** The separate corrected same-host crossover also fails the frozen >=3x slowdown at both larger workloads. The experiment concerns a synthetic public-library fixture workload, not the reporter's private 30,495-test workload. Same-runner crossover reduces between-host confounding but does not eliminate all time drift or prove absence of regression elsewhere.

## Distinct executable edit-language pilot

Built a read-only soundness-scoped SSA-like def-use analyzer with explicit `UNKNOWN` for unsupported Python, a semantic reaching-definition action language and a separate ordinary AST statement-index action language, with a shared atomic SHA-pinned compiler, source/edit authority and identical task facts. These are distinct **edit action languages**, not JSON-versus-Python-literal renderings. A deterministic 512-seed compiler parity suite passed; 10/10 regression/adversarial tests passed. Independent arithmetic oracles and isolated CPython subprocesses verified 32 paired synthetic two-file tasks (256 functional observations), with 740 independent audit checks and zero mismatches. A 64-prompt / 32-task matched diagnostic was frozen with identical common-facts hashes across conditions. **No model was run on these prompts.**

Limitations: the bounded graph covers straight-line single-assignment arithmetic only, not general Python or intermodule calls; the two files in this diagnostic are independent, not a semantically coupled production repair. The 512-seed parity and 32 functional tests demonstrate compiler expressibility, not useful model repair performance, semantic superiority or production qualification. Raw artifacts, prompt SHA-256s, executable scripts, logs and negative outcomes are retained in the Run402 local SHA-manifest ZIP.

## Decision

No new independently qualified real multi-source repair and no powered semantic-IR superiority evidence. Prioritize unseen issue-first production repairs with neutral-shim behavioral necessity and actual paired capable-model inference. Never promote pytest #14942 or any failed historical candidate post hoc. Keep all 89 reserved issues sealed.
