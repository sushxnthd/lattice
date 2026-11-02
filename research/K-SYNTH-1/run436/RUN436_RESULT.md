# K-SYNTH-1 Run436 — Two-file atomic compiler parity and bounded necessity

## Decision
Implemented two distinct edit representations: semantic/dataflow IR with an explicit static cross-file import-call edge, and ordinary Python AST actions specifying file/function/AST paths. Both canonicalize into the same SHA-locked atomic two-file compiler. Unsupported dynamic constructs are marked UNKNOWN. This is a **trusted synthetic fixture** result, not real-repository qualification or model evidence.

## Executed evidence
- 128 independently seeded two-source affine integer fixtures; 256 compiler transactions (128 IR, 128 AST). 128/128 output source pairs byte-identical and canonical transaction receipts matched.
- 1,024 input rows × 5 variants × 4 public functions = **20,480 actual CPython function calls**. Both full variants passed 1,024/1,024 joint public-API targets. Base, provider-only and consumer-only each passed 0/1,024 joint targets. Both nonregression controls passed in all 5,120 variant observations.
- Separate auditor reconstructs fixture sources without importing the compiler and executes **20,480 additional CPython function calls**; 31,744 observation/classification predicates plus 2,048 input-source SHA checks agreed, zero discrepancies.
- Exhaustive finite search: 128 × 101² = **1,305,728** candidate (provider.bias, consumer.offset) pairs. Every case has exactly one joint two-API solution and no one-file solution **within the frozen edit grammar**. With only the consumer API observed, each case has at least two explicit one-file alternatives.
- 13/13 adversarial tests passed. Star imports, dynamic calls, monkeypatches, decorators, reordered imports, extra files, unauthorized AST edits and hash mismatches are refused.

## Bounded theorem
With `provider.core(x)=a*x+b` and `consumer.compute(x)=provider.core(x)+o`, fixed `a`, and only `b,o` editable, two frozen public API targets require `b'=b+δ_b` and `o'=o+δ_o` for nonzero corrections. Both files must change under this grammar. Observing only `consumer.compute` permits one-file compensation, showing that apparent multi-file necessity depends on the observation set. This **does not prove global minimum repair cardinality for any real repository**.

## Fairness and scope
Both views carry the same edit values, source facts, SHA locks, authority, compiler and functional oracle. IR exposes a derived graph; AST view includes the source from which the graph is mechanically recoverable. No prompts were sent to a coding model, so prompt/token parity and model superiority remain untested. Only trusted constructed code was executed; `python -I -S` is not a security sandbox.

## Status
Historical independently qualified real multi-source repairs remain **two** (Flask PR6096 and urllib3 PR5071). New model completions: **zero**. No powered IR superiority or breakthrough. All 89 reserved issues sealed. One canonical branch and draft PR #9 preserved.

## Local reproducibility
Run436 local SHA-verified ZIP: `lattice_run436_dual_view_atomic_repair_and_minimality.zip`, SHA-256 `74289861e411e95fd712638d0b361988555cab9ed5bb099fcb65380a14be9817`. 17 verified payloads / 18 ZIP entries. Contains full compiler, primary and independent executable oracles, raw JSONL, exhaustive search, tests, stdout, protocol and manifest.

## Next
Qualify a genuinely independent real two-production-source repair prospectively, with byte-level heldout and nonregression oracles and alternative-repair challenge. Then execute genuinely functional matched no-cost open coding model inference with pinned SHA, raw completions and isolated oracle; do not substitute synthetic parity for model evidence.
