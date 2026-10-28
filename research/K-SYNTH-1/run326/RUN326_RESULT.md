# K-SYNTH-1 Run326: scoped lexical read facts and counterexamples

**Protocol frozen before execution:** commit `86e7e78dcc728208d8532e1bc0d41843f62384c2`.

## Original failure and postfreeze corrections
The first independent auditor found **816/16,384 mismatches**, all from a lambda-scope fixture error: tracer/variable names were provided only to evaluation locals rather than to the nested function's globals. The original raw failure and source are preserved locally. After correcting the namespace, a separate contract audit found the fact views lacked explicit SHA-scoped edit authority required by the frozen protocol. That intermediate result was also preserved. The figures below are **postfreeze-corrected** and must not be represented as a clean original preregistered success.

## Corrected evidence
- 1,024 correlated synthetic fixtures, 20 trusted Python expression templates, 16 deterministic valuations per fixture: **16,384/16,384 normal completions**.
- Direct lexical Name-load MAY coverage: **0/16,384 observed omissions**. Conservative normally-completing MUST_READ: **0/16,384 violations**.
- Naively treating every syntactic Name as MUST_READ fails in **3,484/16,384 (21.26%)** cases due to short-circuit and conditional execution.
- **972/1,024** synthetic fixtures carry explicit UNKNOWN. **13/17** previously frozen real urllib3 Run324 source candidates carry UNKNOWN for dynamic operations or unproven truthiness.
- Typed JSON fact view and ordinary Python literal view share candidate IDs, source/node SHA-256 edit authority, MAY, MUST and UNKNOWN; all 1,024 fixture and 17 real-candidate records round-trip exactly. They differ in text length, and this is not a genuine coding-model AST-action comparison.
- Independent auditor imported no primary analyzer and replayed all **16,384** trusted CPython evaluations with **zero discrepancies**. **7/7** regression tests passed.
- Three executable counterexamples: custom `__bool__` mutates hidden state despite the same lexical test AST; `x and y` can skip reading `y`; `eval('hidden')` can read outside the lexical Name set.

## Scientific limit
Syntactic MAY only bounds **direct lexical loads** in the bounded analysis scope, not transitive dynamic reads, arbitrary Python effects, or whole-program semantics. `UNKNOWN` is mandatory for unresolved calls, attributes, overloaded operations and truthiness. These are correlated synthetic diagnostics, **not** independent repository repairs. No new coding-model inference, powered IR advantage, or breakthrough was established.

Historical independent production tasks remain **Flask PR6096 and urllib3 PR5071**. Werkzeug PR2535 remains disqualified. A new candidate, merged [urllib3 PR2482](https://github.com/urllib3/urllib3/pull/2482), touches three production files but is **not qualified**; exact parent `1c6405832e5348c740bc3b67b8b171b5da100a26`, reference `111e609250bc7bf67b080b124298e0cf59efef9d`. A prospective isolated target-plus-control component-ablation oracle is still required.

Full original failures, raw traces, corrected code, independent audit, tests, source corpus and SHA manifest are preserved in the SHA-verified local Run326 archive. GitHub mirroring of the complete ZIP is not yet finished. One draft unmerged PR #9, same canonical branch; all 89 reserved boundary issues sealed.
