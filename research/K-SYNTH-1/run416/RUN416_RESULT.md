# K-SYNTH-1 Run416: lossless equal-authority compiler and independent repair-candidate rejection

Date 2026-11-01 UTC. Canonical `sushxnthd/lattice`; branch `research/exp003-context-order`; sole PR #9. All 89 boundary issues remain sealed. No new model inference or qualified multi-production-source repair.

## Scientific question and negative baseline

The Run402/415 shared AST compiler reconstructs **the entire source file** with `ast.unparse`, even when its authorized edit changes only one expression. Thus a valid compiler transaction can delete unrelated legal headers, `# noqa`, formatting directives and CRLF style. The prior 320-pair Run415 experiment established AST equivalence, not preservation of source bytes outside the authorized edit. This is a production-editor correctness gap, not a semantic-IR advantage.

## Implemented correction

`run416_lossless_compiler.py` implements an all-or-nothing, byte-span Python expression transaction for the same bounded straight-line SSA-like grammar. Semantic IR selects a unique definition name; ordinary Python/AST selects a statement index. Both have **identical assignment edit authority**, including syntactically dead definitions, and lower through the same lossless byte patcher. The compiler:

1. Verifies every original source SHA-256 and explicit path/function authority; rejects malformed or duplicate actions.
2. Parses and validates every new expression under the same bounded grammar; rejects dynamic calls, attributes, unbound or forward references.
3. Locates only original RHS AST UTF-8 **byte** spans, rejecting overlaps; applies all edits in reverse byte order.
4. Independently builds the expected AST and rejects any output whose parsed AST differs, or whose authorized function leaves the bounded grammar.
5. Returns immutable outputs and precise source-span receipts, never executing untrusted edits on the host.

**Bounded guarantee:** For any accepted transaction, output bytes outside the union of original authorized RHS spans are exactly preserved, and the output AST equals the original AST with precisely the requested RHS replacements (under CPython AST parsing). This is a source-frame and AST-structural guarantee, **not** whole-Python semantic noninterference, a proof of effect purity, or a security sandbox. Run415's overloaded-operator counterexample still applies.

## Executed evidence

Seed `41620261101`, 512 constructed paired transactions across two Python files each, with CRLF, tabs, non-ASCII comments, legal headers, `# noqa`, and `# fmt` directives. The semantic and ordinary AST languages compiled to identical bytes on **512/512 paired transactions**. Across **1,024 edited file outputs**, the lossless compiler matched the legacy compiler's AST while retaining the original license and directive bytes. The legacy full-module `ast.unparse` output differed from the lossless source in **1,024/1,024** edited files.

A separate independent byte-frame verifier checked **1,024** patched RHS spans and source prefixes/suffixes. The functional oracle ran **512** controlled side-effecting Python programs in `python -I -S` subprocesses and checked the returned values. An independent read-only auditor reexecuted all **512** programs and checked exact stdout, stderr, exit status and program SHA-256, performing **12,288** assertions with zero disagreements. **26** unit/adversarial tests passed. Raw case rows, source/output hashes, receipts, oracle traces, test logs and independent audit are in the SHA-256-manifested local archive.

These are constructed compiler tests, not model-generated repairs or independent production-repository tasks. They establish byte-frame and bounded AST parity only.

## Issue-first prospective candidate: HTTPX #1404

Before inspecting any fixing PR, froze the public issue (2020-11-30), pinned HTTPX `0.16.1` commit `92ca4d0cc654859fc2257c492e55d8752370d427`, and wrote a six-outcome localhost HTTP oracle with source-distinct public/heldout and nonregression cases. Oracle SHA-256 `2cc87c31d9463373b65ee1732a01d3807282d9951dc204e81ebcd54b1fba7b65`; public and heldout AST fingerprints are different. The frozen oracle was **not executed on historical HTTPX** and the candidate was **not qualified**.

Only after freezing, inspected historical [HTTPX PR #1574](https://github.com/encode/httpx/pull/1574), merged 2021-04-19. The upstream resolution **deprecates per-request cookies on client instances** rather than guaranteeing that such cookies persist across redirects. This conflicts with the candidate's predeclared expectation. Per the original gate, mark `UNSUPPORTED_ORACLE / NOT QUALIFIED`, do not silently change the expected behavior or promote the candidate. The prospective protocol and original oracle are preserved unchanged.

## Scientific status and next step

The independently qualified real multi-production-source repair count remains **two** (Flask PR6096 and urllib3 PR5071). No new strong-model completions, powered IR-versus-AST functional evidence, mechanism superiority, or breakthrough are claimed. Historical raw GitHub ZIP mirroring remains incomplete. Run417 should prioritize a genuinely qualified issue-first two-production-source repair and a functional matched no-cost model pilot with exact model SHA, prompts, seeds, raw completions and isolated oracle. All 89 reserved issues remain sealed.
