# K-SYNTH-1 Run434 — Active frame mutation falsifies open-world final-state commutation

## Decision
**Executed bounded negative counterexample and conditional scope repair.** Run432's pure-integer adjacent-assignment certificate is correct only in a closed-world environment that prevents external mutation of live function locals during evaluation. Run433 showed read-only line traces differ; Run434 demonstrates a stronger failure: an active CPython tracer changes **final return values** after a certified swap. This is not evidence about semantic-IR repair success. The two independently qualified real production multi-source repairs remain unchanged.

## Minimal witness and exact formula
Original:
```python
def f(x):
    a = x + 3
    b = x * 5
    return a - b
```
Swapped:
```python
def f(x):
    b = x * 5
    a = x + 3
    return a - b
```
Both satisfy Run432's read/write independence conditions, with exact built-in integer input and arithmetic restricted to +,-,*. In an ordinary closed-world call with x=7, both return -25.

In CPython 3.13, a sys.settrace callback can write through frame.f_locals. On the second line event, the observer changes x from 7 to 99. The original returns 10-495=-485; the swapped program returns 102-35=67. Neither raises an exception. Difference -552.

General family: a=x+c; b=k*x; return a-b, k>=2, external frame mutation x->x' after first assignment. Original returns x+c-k*x'; swapped returns x'+c-k*x. Difference **(k+1)(x-x')**, nonzero whenever x!=x'. Without mutation both return x+c-k*x. This is an algebraic counterexample family for CPython 3.13, not arbitrary Python implementations.

## Executed functional evidence
- 256 deterministic programs, four distinct input/mutation pairs each, 1,024 paired cases.
- 4,096 real CPython 3.13.5 executions: 2,048 closed-world and 2,048 actively traced.
- Closed-world equality **1,024/1,024**; active-trace inequality **1,024/1,024**; predicted algebraic delta **1,024/1,024**.
- Independent evaluator recompiled and re-executed **2,048 additional CPython calls**, checked **10,240 predicates**, zero disagreements.
- Exact original Run432 compiler accepts all 256 cases, with **512 IR/AST matched compiler transactions** and **1,024 parity/certificate checks**, zero disagreements. Prior compiler SHA256 abe06337fe6f76a425e355d8963e6d4017ab92eac870021376cdcf92a501b7bc.
- 10 adversarial and regression tests passed. Raw JSONL SHA256 99e695440d7d53252bc3ebf5bea663fbc917f42f423c9ae24032b897cc5d40a4.

## Scope correction
A new conservative scope guard reuses Run432's compiler and identical IR/ordinary-AST action authority, but rejects LINE_TRACE as UNKNOWN_TRACE_OBSERVABILITY and unrestricted external frame observation as UNKNOWN_EXTERNAL_FRAME_MUTATION. FINAL_STORE_RETURN is permitted only under a declared CLOSED_WORLD_NO_EXTERNAL_FRAME_MUTATION assumption.

**Critical:** The guard is a conditional contract, not runtime enforcement. sys.gettrace() is None at compile time cannot prove that tracing or frame mutation will remain absent at execution time. Receipts explicitly say environment_verified=false. A production certificate needs enforced isolation or a justified conditional assumption; otherwise abstain.

## Reproduction and limits
The complete SHA256-manifested local Run434 ZIP includes raw JSONL, independent auditor, parity audit, compiler, tests, stdout and scripts. Requires CPython 3.13+ for write-through frame.f_locals. No untrusted model code executed. No new model inference, qualified real repair, powered IR advantage, or breakthrough. All 89 reserved boundary issues untouched. One open/draft/unmerged PR #9 on research/exp003-context-order.
