# K-SYNTH-1 Run401: original pytest performance audit and measurement identifiability

Date: 2026-11-01 IST. Canonical sushxnthd/lattice, research/exp003-context-order, sole open draft PR #9. All 89 reserved issues remain sealed.

Recovered all eight original GitHub Actions ZIPs from Run400 jobs [41252417259](https://github.com/sushxnthd/lattice/actions/runs/41252417259) and [41252538279](https://github.com/sushxnthd/lattice/actions/runs/41252538279). Eight GitHub-published ZIP SHA-256 digests and eight internal manifests verified. The workflow update changed only trigger paths and concurrency; the executed oracle source Git blob is identical (60bf44ede78986bee6dbc8a58be91d5573580aed). Independent reconstruction verified 1,392 generated source-file SHA-256 entries and all 80,640 exact collected test IDs across 72 successful collections. Twelve adversarial/regression tests passed locally.

| Original Actions | Python | 8 modules B/A | 32 modules B/A | 128 modules B/A | Frozen >=3x both larger? |
|---|---|---:|---:|---:|---|
| 41252417259 | 3.13 | 0.915 | 1.140 | 1.807 | NO |
| 41252417259 | 3.14 | 1.159 | 1.256 | 1.773 | NO |
| 41252538279 | 3.13 | 1.257 | 1.516 | 2.258 | NO |
| 41252538279 | 3.14 | 0.656 | 0.674 | 0.814 | NO |

A = pytest 9.0.3; B = pytest 9.1.1. Each ratio is between original three-repetition medians from distinct GitHub jobs. **Original frozen decision: NONREPRODUCING, NOT QUALIFIED.** No reference patch, heldout repair oracle, source ablation or neutral-shim necessity was evaluated. This says nothing definitive about the reporter's unavailable private 30,495-test workload.

**New counterexample / construct-validity flaw:** distinct GitHub runners prevent identification of a pure version effect. Write measured wall time T_v = H_v C_v, with unknown host/load multiplier H_v and intrinsic version cost C_v. Then T_B/T_A = (H_B/H_A)(C_B/C_A). Without measuring/bounding H_B/H_A, every positive C_B/C_A can fit the same observations. The observed Python 3.14/128-module ratio even changes from 1.773 to 0.814 across original batches, with identical oracle and package pins. The first-run-only Python 3.13/8-module ratio in the second batch is 3.254 versus frozen median ratio 1.257, illustrating cold-start sensitivity. These diagnostics do not revise the original frozen criterion.

Separately froze a new ABBA/BAAB same-host crossover, with identical sources, two pinned venvs, complete traces and no post-hoc retuning; see PROTOCOL_RUN401_CROSSOVER.md. It is not evidence until the new Actions artifacts finish. No new coding-model inference, independently qualified repair, powered IR advantage or breakthrough. Primary priority remains unseen issue-first multi-production-source repair qualification and genuinely distinct semantic/dataflow IR versus information-equivalent Python/AST action model comparison.