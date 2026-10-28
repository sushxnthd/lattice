# K-SYNTH-1 Run322: two-action AST congruence and an observational counterexample

Date: 2026-10-28 UTC. Canonical branch `research/exp003-context-order`; PR #9 remains draft. All 89 reserved boundary issues untouched.

## Frozen primary experiment

The [Run322 protocol](FROZEN_PROTOCOL.md) was committed **before primary execution** as `f3ed1bca42e4828b32cf505f3d12b13671307588`. Deterministic seed 3222026, eight families x 64 = 512 correlated synthetic cases. Each case uses two actions on one source file and an unchanged second file. Run320's shared byte-splicing compiler was compared with a new fail-closed whole-module AST-congruence validator that constructs simultaneous expected AST substitutions on the original tree. This is an editor-correctness experiment, **not a model or repository-repair comparison**.

| Primary measure | Observed |
|---|---:|
| Safe cases accepted by guarded compiler | 320/320 |
| Unsafe cases rejected by guarded compiler | 192/192 |
| Unsafe patches accepted by original structural compiler | 128/192 |
| Original accepted patches with intended-AST mismatch | 128/448 |
| Guarded accepted patches with intended-AST mismatch | 0/320 |
| Independent raw-trace audit discrepancies | 0/512 |
| Trusted isolated functional value agreements | 256/256 |
| Trusted isolated exception-outcome agreements | 64/64 |

The 64 exception-outcome agreements are **not successful value-returning functional tests**. The preregistered `safe_insert_delete` fixture deletes `a` but leaves `return a + b`; both the actual patch and intended AST raise `NameError`. The original independent auditor aborted on this exception; its original source, error output and failed summary are preserved. The corrected auditor treats exceptions as recorded outcomes without changing any frozen primary input, code or outcome. It independently reconstructs expected ASTs and checks SHA-256 hashes, all 512 raw records and 320 trusted isolated CPython replays. No model-authored code was executed.

Per-family: 64/64 accepted for each of the five safe families (`safe_expr_pair`, `safe_stmt_pair`, `safe_mixed`, `safe_insert_delete`, `safe_unicode_crlf`). `unsafe_comment` and `unsafe_precedence` each yielded 64/64 original-compiler accepted but AST-incorrect patches, all rejected by the guard. `unsafe_nested` yielded 64/64 rejections by both compilers. The original structural compiler's 128 unsafe acceptances establish the practical value of a whole-module AST check under these fixtures, but not production security or semantic soundness.

## Postfreeze negative result: AST equality is not full observational equivalence

A separate **postfreeze exploratory** 64-case test replaced a one-line assignment with a parenthesized three-line assignment. All 64 patches passed the whole-module AST check and returned the same integer value, yet all 64 changed CPython `code.co_lines()` tables. This is a reproducible counterexample to treating AST congruence (with `include_attributes=False`) as observational equivalence. It is not a failure of the narrower AST-congruence contract. Location-sensitive tooling, coverage, debugging, tracebacks and source introspection remain outside the guarantee.

## Scope and research consequence

The guard validates two nonoverlapping actions in one source file, including expression replacements, statement replacements, insertion and deletion. It retains source SHA and edit-authority checks and rejects nested action collisions. This is bounded synthetic validation, not a general theorem for all Python syntax, no security proof, and no semantic-IR superiority. The source-local AST comparison also cannot establish cross-file dataflow soundness or comment preservation. A future production-grade compiler must specify which observational properties it preserves, possibly including location tables, comments and formatting, and explicitly return UNKNOWN for unproven semantics.

**Unchanged research status:** six independently qualified historical production repairs; no new coding-model inference, no powered IR-vs-Python result, no breakthrough. All 89 reserved issues remain sealed. The primary research priority is still a strong no-cost open coding model under paired, information-equivalent IR and Python/AST conditions on independently qualified real repairs. Do not treat these 512 synthetic cases as independent repairs or evidence of a representation advantage.

## Reproducibility

Run locally with Python 3.13.5:

```bash
python run322_primary_experiment.py
python run322_independent_audit.py
python run322_postfreeze_location_counterexample.py
```

Primary trace SHA-256: `27e429ad27aff05e13dabbaf7f5c2195607396806bb17a777fbd2b9dbbf80759`.
Independent functional trace SHA-256: `c229a701546cd30a055e6d87fc99b7e4bbd9c8ab19f6f00722906c3c3dcbc133`.
Postfreeze location trace SHA-256: `01815fb0854c392285dfaec584d47626cdbcedf10b054e4f82cd91173d3f5ab8`.

The local ZIP includes all code, exact primary and exploratory traces, original auditor failure, corrected auditor, report, protocol and SHA manifest. Full historical GitHub artifact mirroring remains incomplete.
