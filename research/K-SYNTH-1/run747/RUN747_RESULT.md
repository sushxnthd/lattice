# Run747 — callable-kind differential release gate

Date: 2026-11-19 UTC

## Frozen question
Does the bounded alpha compiler's callable_kind classifier agree with CPython 3.13.5 code-object flags on adversarial nested-scope and definition-time yield placements, without executing candidate modules?

## Protocol
- Seed: 747.
- Archived compiler snapshot SHA-256: `555093c68e031c1de5f37341c087b97bba5d543ab2bd7d1b187f8629a9ce4215`.
- 16 source families × 256 semantics-preserving lexical/context perturbations = 4,096 cases.
- Candidate source was parsed and compiled only; no candidate module was executed.
- Lattice prediction: `callable_kind(ast.FunctionDef|ast.AsyncFunctionDef)`.
- Independent reference: CPython top-level function code-object flags `CO_GENERATOR`, `CO_COROUTINE`, and `CO_ASYNC_GENERATOR`.
- Families include direct yield/yield-from; nested function/lambda yield bodies that must not leak to the enclosing callable; and definition-time nested defaults, decorators, annotations, class bases, and metaclass expressions that must affect the enclosing callable.

## Result
- 4,096 / 4,096 passed.
- 0 mismatches.
- 0 compile/protocol errors.
- Every family was 256 / 256.
- Local complete archive SHA-256: `5d7b0405dd940fa675a9653a85bd3c31c2af64ccfd57bc5a372e7063cfbb1ab1`.
- Raw JSONL SHA-256: `d58303c9ec953100f5969597685e4da0eeec58a11a980a8a9cec714a50864251`.
- Experiment script SHA-256: `fbf8ea3b4d9f8b55440d478cf10273e8f81604c89bcb45478ed5407ccdf41bf1`.
- Summary JSON SHA-256: `bd32dd874bf6aca9507433e64e1351a3438a8a07a368f45c10317ebd5aeedf6b`.

## Interpretation
This closes a bounded alpha release gate for callable-kind classification only under the enumerated grammar families. It is not a proof of general Python semantic soundness, runtime safety, repair performance, or semantic/dataflow-IR superiority.

No new production repair was qualified. The independently qualified real-task count remains TWO. No coding-model inference was attempted. All 89 reserved boundary issues remain SEALED.
