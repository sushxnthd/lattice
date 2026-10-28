# K-SYNTH-1 Run326 frozen protocol: bounded source-read facts and representation parity

Frozen before executing the Run326 generator or independent auditor. This is an **analysis and construct-validity experiment**, not a new production repair or model trial. It does not alter any previously frozen run.

## Hypotheses and evaluation
1. For trusted, syntactically generated Python expression fixtures with ordinary local variable environments, the lexical MAY_READ set (all load-context `ast.Name` occurrences) contains every instrumented direct variable load on normally completing evaluations. This does **not** bound reads performed inside called functions, overloaded operators, descriptors, `eval`, or dynamically executed code. Such paths must be marked UNKNOWN.
2. A recursively computed conservative MUST_READ set is a subset of the direct variable loads on every normally completing evaluation in the bounded fixture domain. Branch-specific reads must not be claimed MUST. Failure in any fixture is reported, not repaired in the frozen score.
3. JSON semantic-IR and ordinary Python/AST-action views must be generated from the **same canonical facts**, with round-trip equality of task facts, candidate IDs, MAY/MUST/UNKNOWN and edit authority. The views are not model-equivalent by fiat; prompt-length and model behavior are unmeasured.
4. Run324's 17 original real urllib3 source candidates are replayed as an external, previously fixed corpus. No reference-patch content, outcome labels or candidate retuning may be used.

## Frozen deterministic fixture design
- 20 fixed expression templates covering `and`, `or`, `if/else`, `not`, identity, equality, ordering, call, attribute, subscript, arithmetic, chained comparisons and nested dynamic truthiness. Generate 1,024 fixture instances by cycling templates and varying literal flags, and test each against 16 deterministic Boolean assignments to x/y/z/a/b.
- Record raw per-evaluation instrumented direct variable-load traces and any exception; count MUST violations only on normally completing evaluations. Each fixture's MAY and MUST sets must be stable across valuation changes.
- Mark UNKNOWN whenever a syntactic construct may trigger dynamic dispatch, arbitrary side effects or unproven truthiness; absence of UNKNOWN is not a general whole-program soundness certificate.
- Independent auditor must not import the primary analyzer. It checks all raw traces, candidate facts and both presentation encodings.
- Preserve raw JSONL, hashes, code, tests, full error records, and a SHA-256 manifest. No network or execution of untrusted model-generated code.

## Interpretation and next gate
A passing experiment supports only a bounded lexical analysis contract and fact-presentation parity. It does not prove general Python semantic soundness, semantic-IR advantage, or production repair. Follow with a genuine prospectively frozen capable-model paired repair pilot using a shared atomic compiler and independently qualified oracle; continue recruiting independently qualified multi-production-source tasks.

Keep canonical `sushxnthd/lattice` branch `research/exp003-context-order`, only PR #9 open/draft/unmerged, one K-SYNTH-1 kernel and all 89 boundary issues SEALED.
