# K-SYNTH-1 Run345 — historical Jinja ABI-only ablation separates compatibility from context transfer

**2026-10-29 UTC.** Canonical branch `research/exp003-context-order`; sole OPEN/DRAFT/UNMERGED PR #9; all 89 reserved boundary issues SEALED.

## Pre-execution freeze and original cloud evidence

This is a **post-Run344-outcome, pre-Run345-execution frozen** mechanism ablation, not a new benchmark qualification and not model inference. Freeze commit `15d8c2b0755200c4ffa27d9e2cc8c850da4853ef` preceded implementation `cd7a56bb783fd8bd9daa66b1558e0e10166e25ec` and workflow `fe78694749673084bb61fc4e1ff5eeccd40fb2a0`.

Historical Jinja PR #1242 pinned base `94ccd028ef1f3cd9eaec862d6a1d646d02a242bc` and reference `f71f5ebab2e76c5ee6f5f705a2703f3891e762bc`. Original Run344 oracle SHA256 `4d121eb18d8071eacbf5967c7fa62e458f3bcad140b85be1f2398c163e37d5f0` unchanged. Git blob checks for compiler.py/runtime.py were enforced. On the **baseline runtime only**, insert `kwargs.pop("_loop_vars", None)` and `kwargs.pop("_block_vars", None)` before `Context.call` invokes the user function. This strips newly emitted private kwargs but does not transfer scoped values.

[Original Actions Run345 40912342020](https://github.com/sushxnthd/lattice/actions/runs/40912342020) **SUCCESS**. Original artifact 12914402305 ZIP SHA256 `ed0fcf185d1ed05a94f6b3e46326a51467c03369a2b5de371021717a130d5c07` matches GitHub artifact digest. Seven internal payloads SHA-verified. Independent auditor verified 56/56 original Run345 functional records, including 42/42 unchanged-arm observations matched to original Run344, and rejected 10/10 adversarial evidence mutations. An initial independent audit blind spot accepted changed observations on already-failing cases; the final auditor requires exact predicted traces. This **post-outcome audit enhancement does not alter the frozen experiment**.

## Original Run345 results

| Arm | Compiler | Runtime | Targets /6 | Controls /8 |
|---|---|---|---:|---:|
| 00A | baseline | baseline + ABI strip | 1 | 8 |
| 10A | reference | baseline + ABI strip | 2 | 8 |
| 01A | baseline | reference | 1 | 8 |
| 11A | reference | reference | 6 | 8 |

**All pre-execution predictions matched.** In 10A, T03 and T04 pass; T01, T02, T05 and T06 fail without the original compiler-only TypeError, producing ordinary `<missing>` dynamic-context values. All controls remain correct.

The original Run344 five positive casewise target interactions reduce to **four ABI-normalized positive interactions**, T01/T02/T05/T06. T04 was an ABI-only apparent interaction. T03 and all eight controls have zero interaction. Thus mere signature compatibility is insufficient for four bounded context-transfer repairs; this is finite functional evidence for a mechanism beyond ABI, **not** a global proof of semantics or any IR benefit.

The original Run344 reference qualification is unchanged: **8 distinct historical source-qualified PRs across 7 repositories**. These are not model successes. No new model inference, powered IR-vs-Python/AST advantage or breakthrough. All 89 sealed boundary issues untouched.

The SHA-verified local archive includes original cloud ZIP, parent Run344 archive, independent auditor and adversarial tests, 4,096 seeded ABI-strip calls, and full protocol. Archive SHA256 `00edec33d16a3f5d9698d65dfd54668219d65ee1f1ed9844bd315504feece724`. ABI stripping is not universally semantics-preserving for arbitrary functions that explicitly consume reserved kwargs; the counterexample is retained.

**Next:** prospectively frozen matched open-model IR vs ordinary Python/AST functional repairs with same facts, model, edit authority, compiler, verifier and isolated oracle; recruit more independent repositories and stratify ABI-only versus ABI-independent mechanisms.
