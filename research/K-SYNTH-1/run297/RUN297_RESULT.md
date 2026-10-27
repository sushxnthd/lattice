# K-SYNTH-1 Run297 — independently qualified fifth real task

**Prospective qualification: PASS**, under unchanged, pre-execution criteria. This is NOT a model repair or IR-vs-Python result.

- Candidate: [python-hyper/h11 PR115](https://github.com/python-hyper/h11/pull/115), three production source files. Base `522b00470b5776dda2dc7e98ff778eb1e418e6ad`, head `a1197d68630bc37a941b516c7cc74833460fc97c`.
- [Frozen protocol](RUN297_PROSPECTIVE_FREEZE.md) committed **before oracle execution**, commit `59aa97ba1ae9bed1ac9b7739277ea00f48678c77`. All six Git blob source hashes pinned and verified.
- [Original CI](https://github.com/sushxnthd/lattice/actions/runs/40561189649) completed SUCCESS; artifact `12760252473`, ZIP SHA-256 `3b005b830e08ed2733a6e2532b01f4b0578e0e2b923a2ce25209bd05ad0b83a0`.
- Original raw JSON SHA-256 `1684af143c0693b507a98998994210131a4ae635e1f67e2076a69539d7c1b603`. Original Python 3.10 trusted-upstream isolated public API oracle, not model code.

| Frozen configuration | LF targets | CRLF controls | Combined |
|---|---:|---:|---:|
| Baseline | 0/5 | 5/5 | 5/10 |
| Full reference | 5/5 | 5/5 | 10/10 |
| Full minus _connection.py | 0/5 | 0/5 | 0/10 |
| Full minus _readers.py | 5/5 | 4/5 | 9/10 |
| Full minus _receivebuffer.py | 0/5 | 4/5 | 4/10 |

**Independent audit:** 50/50 original functional outcomes, nine ablation source-hash relationships, zero discrepancies; independent qualification PASS. Original GitHub artifact independently downloaded and its ZIP SHA-256 matched GitHub's digest. Local audit replay produced the identical decision.

**Mechanism:** removing _readers.py causes a regression on the chunked-transfer **control**, despite preserving all LF targets. Removing _connection.py produces an AttributeError due to buffer API incompatibility, not proof of deeper causal interaction. The frozen joint target-plus-control criterion is therefore essential. Local installed h11 0.16.0 smoke 10/10 is explicitly not counted as historical reference evidence.

**Limits:** Ten cases, not exhaustive; historical PR selected after examining upstream diff, so not a blind model task. Five independent qualified tasks remain far below the powered target. No new coding-model inference, model repair, representation superiority, or breakthrough. All 89 reserved boundary issues SEALED; canonical branch, one OPEN/DRAFT/UNMERGED PR #9.

Reproducibility: [original cloud artifact](https://github.com/sushxnthd/lattice/actions/runs/40561189649), SHA-pinned runner and independent auditor in losslessly compressed transport with workflow verification, local 13-entry SHA manifest, complete original raw traces. Historical mirroring beyond Run297 remains incomplete.