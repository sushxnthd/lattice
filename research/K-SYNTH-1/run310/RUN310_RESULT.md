# K-SYNTH-1 Run310: prospective annotation NamedExpr soundness test

**Result:** The Run309 bounded module-binding analyzer returned `NOT_KNOWN_TARGET` for 240 genuine `builtins.len` calls when a Python 3.13 function annotation executed an assignment expression. A conservative correction produced zero false-negative exclusions on the frozen cohort, at a cost of 96 UNKNOWN classifications on negative controls.

## Preregistration and reproducibility

- Prospective protocol committed **before oracle execution**: [commit 9264d8a](https://github.com/sushxnthd/lattice/commit/9264d8a2609698a950c80f5d1f2da3dac02f7dd2).
- Frozen manifest SHA-256: `6a98891ae449dbe98ed2a048c0d1f8a98b05384159207ba7c905635dc2498726` (152,529 bytes; 384 programs, 16 templates × 24 correlated variants).
- Generator SHA-256: `fba68c7ebf6235595289397d45dc646c1d34cb73a5b3fceac92e044ea1129e80`.
- Corrected analyzer SHA-256: `ba7db6d2f0044000fda1a4b7904889f7b6b093ddc80a2aab16420e5b5f9125ba`.
- Raw original executions SHA-256: `1c110344e41872eaefac9ff02fd741b2ee62b8117f3384b61e684fe6dd02696f`.
- Trusted CPython 3.13.5 `-I -S` subprocesses; no untrusted model code executed. Independent replay via a different subprocess entry path matched all 384 source hashes, exit statuses, builtin identities and outputs, with zero discrepancies.

| Endpoint | Original Run309 | Corrected Run310 |
|---|---:|---:|
| Definite-negative exclusions of real builtin calls | 240 | 0 |
| UNKNOWN outcomes | 0 | 336 |
| UNKNOWN on negative controls | 0 | 96 |
| Runtime/expected-label errors | 0 | 0 |

### Mechanism

In Python 3.13, `def f(x: (len := saved_len)): pass` evaluates its annotation when the function is defined. That `ast.NamedExpr` can rebind the module-level `len` even without any `ast.Call`. Run309 checked only annotation calls. The correction conservatively invalidates the alias on either an annotation `ast.Call` or `ast.NamedExpr`. See [executable witness](run310_minimal_witness.py).

**Scope:** 384 correlated variants are not 384 independent real repairs; this is bounded source-analysis evidence, not Python-wide soundness, coding-model inference, or semantic-IR superiority. Deferred annotations in Python 3.14 require separate verification.

## Sixth-repair screen

[wsproto PR #6](https://github.com/python-hyper/wsproto/pull/6) changes two production files. Pinned merge `99aeafa3f188d5fb4563d4e9543e8cd8892a793d` and first parent `7314c8428a2d02625828e5a705529b2e2fe1ac21`. `connection.py` and `events.py` jointly change the `ConnectionRequested` constructor signature, but **no prospectively frozen isolated target-plus-control functional oracle was executed**. It remains **NOT QUALIFIED**.

**State:** Retain five previously reported real qualifications without re-auditing them here; no sixth, no powered advantage or breakthrough. One K-SYNTH-1 kernel, canonical branch, one open/draft/unmerged PR #9, 89 reserved boundary issues sealed. Full raw source manifest, both analyzers, 384 original traces, independent replay, SHA manifest and Run311 protocol are preserved in the local Run310 archive. GitHub ZIP mirroring remains incomplete.

## Original isolated wsproto qualification completed: NOT QUALIFIED

The [frozen four-arm protocol](PROTOCOL_WSPROTO_PR6.md) was committed before the isolated oracle (commit `622ceea36a6e3be0eb530da0f6d7e919ca22a247`). The [original GitHub Actions run 40649766841](https://github.com/sushxnthd/lattice/actions/runs/40649766841) completed successfully as infrastructure. Independently verified all four original artifact ZIP SHA-256 hashes, source Git blob hashes, Python 3.8.18, pinned `h11==0.7.0`, oracle exit codes and 44 per-case records.

| Arm | Public /3 | Heldout /2 | Controls /6 | Total /11 |
|---|---:|---:|---:|---:|
| Baseline | 0 | 0 | 5 | 5 |
| Connection-only | 0 | 0 | 1 | 1 |
| Events-only | 0 | 0 | 4 | 4 |
| Full historical reference | 0 | 0 | 1 | 1 |

**Frozen qualification FAILED.** The baseline failed one control, and the full reference failed all five targets and five of six controls. The full reference calls `.items()` on a list of h11 request headers under its declared `h11==0.7.0` dependency, yielding `AttributeError: 'list' object has no attribute 'items'`. The baseline's `accept_default` control also failed the frozen response assertion. No tests or dependency versions were retuned. Both ablations fail, but cannot rescue a failed full-reference oracle. **wsproto PR #6 remains NOT QUALIFIED** and the previous five-qualified count is unchanged. No model inference or superiority claim follows.

Original artifact ZIP SHA-256: baseline `8e856f5d47b041ca3719d89d58b3b570a9dbf73504b2ce8679a634598cb14f6c`; connection-only `e42a0aeced3606d81d353ef1fc5b75adba872949e3b78e08a805a095a4c9a754`; events-only `71c80c838e8f7df0d671a70e8d0b369a30998b7945f7c8bc6341ff947d6cf34b`; full reference `faaf8c5c216cee2968c1e4b0bdab87a282d473b7d6cb639e1c061851f840c9c5`. Original artifacts and read-only independent audit are SHA-verified in the local Run310 reproducibility archive.
