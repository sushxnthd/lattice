# K-SYNTH-1 Run347: verified local binding and dynamic MUST falsifiers

**Status: completed local experiment, not model inference or new task qualification.** The original Run346 source-qualified cohort remains 8 PRs across 7 repositories; all 89 reserved issues remain sealed.

## New executable evidence

Built a SHA-bound static dataflow analyzer that accepts only restricted straight-line Python function bodies. It records the AST location of each local read, the preceding parameter/assignment binding, the actual CPython `LOAD_FAST`/`STORE_FAST` evidence, the proof rule and assumptions. Every certified edge is **MUST_BIND_ON_REACH_ASSUMPTION_SCOPED**, conditional on original function execution and no external frame-local mutation. Every runtime callee remains **UNKNOWN**. This is deliberately narrower than a general semantic/effect graph.

Two historical HTTPX source files, recovered from the original Run335 archive through SHA-verified Run336/Run346 evidence, were parsed and compiled but **never imported or executed**:

| Historical source | SHA-256 | Certificates |
|---|---|---:|
| `httpx/_api.py` | `81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe` | 93 |
| `httpx/_client.py` | `6b223a7a32afcbaf4e1a9a83f6d34caf8f66a31d740a1ac511df678463ecd8a2` | 214 |

Across 78 historical functions, 39 restricted straight-line bodies were eligible. **307/307 certificates passed an independent fresh-AST/bytecode audit**; 85 unresolved nodes/function-level cases remained UNKNOWN, and all 47 syntactic call candidates retained UNKNOWN runtime targets.

A separate seeded diagnostic executed **4,096 locally generated arithmetic functions**, independently checking **26,522 CPython fast-local loads** and all 4,096 functional results against a separately computed arithmetic oracle (zero mismatches). These are synthetic diagnostics, not repository repairs. Thirteen adversarial source cases and six independent evidence/source/hash mutations were tested; all six mutations were rejected. Nine pytest tests passed.

## Soundness counterexamples

Executed in isolated CPython 3.13.5:

- Changing a global callee without changing its caller AST changed `target(10)` from **11 to 9**. Thus a direct syntactic call cannot establish an unconditional runtime MUST callee.
- An external tracing hook mutated a live local frame, changing a function result from **3 to 101**. Therefore even a local reaching-definition statement needs the explicitly declared no-external-frame-mutation assumption.
- The initial bytecode audit omitted some `LOAD_FAST_LOAD_FAST` superinstructions on CPython 3.13. Added a fail-closed, direct `BinOp(Name, Name)` fused-opcode proof rule. This corrected false UNKNOWN coverage, not a false positive certificate.

The positive claim is an **assumption-scoped local binding on reaching the read**, proved by induction on the straight-line statement sequence and checked against CPython bytecode. It does **not** certify runtime effects, cross-file semantic interactions, value influence, or repair success.

## Information-equivalent comparator

From a single immutable fact ledger, produced two source-identical presentations: a typed graph IR and ordinary Python with an AST-node-addressed binding/action map. An independent parser reconstructed the same facts and edit authority from both. Serialized sizes were 50,288 vs 50,497 bytes for `_api.py` and 150,125 vs 150,851 bytes for `_client.py` (IR vs Python/AST). **These are byte counts, not tokenizer counts**; no model tokenizer was available and no token matching or model comparison is claimed.

The full local reproducibility archive includes original-parent SHA provenance, exact historical source excerpts, all source/test files, raw 4,096-case functional traces, the independent production auditor, two presentations, adversarial tests and manifest. The GitHub mirror of the complete local ZIP is still incomplete; no claim of remote full-archive persistence.

## Decision and next gate

**No new model completions, functional real-issue repairs, powered IR advantage, unseen prediction, or breakthrough.** Run348 must freeze a real two-repository paired model pilot (suggested complementary Jinja #1242 ABI-normalized interaction and HTTPcore #882 parallel two-file negative mechanism), pin the actual model tokenizer and source/issue/oracle, and run both views with identical facts, atomic compiler, edit authority and isolated oracle. Add verified-edge ablation and ABI negative control. Never retune failed historical qualifications or touch the 89 sealed boundary issues.
