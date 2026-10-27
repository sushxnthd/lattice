# K-SYNTH-1 Run289 — lexical binding provenance and CPython 3.13

Date: 2026-10-27. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, one OPEN/DRAFT/UNMERGED PR #9. All 89 reserved boundary issues remain SEALED.

## Scientific result

A new gold-blind lexical MAY analysis resolves `len` and `sum` calls through Python module, function, parameter, local, closure, class, lambda, and comprehension scopes using `symtable`. It never equates a source token with the runtime builtin object without external trusted attestations. Its soundness-scoped certificate explicitly returns `UNKNOWN` for unverified binding identity, ambiguous/dynamic operations, and unsupported scopes. Semantic IR and ordinary Python/AST views contain identical canonical task facts. That is an information-control construction, not a model-performance result.

The initial test failures revealed CPython 3.13 inline list-comprehension scopes, `LOAD_FAST_CHECK` for potentially unbound locals, fused `STORE_FAST_LOAD_FAST` bytecodes, and same-line lambda ordinal ambiguity. The implementation and test oracle were corrected, with the failure ledger preserved.

**Empirical evidence:** 13 fixed lexical templates × 256 deterministic harmless whitespace variants = **3,328 CPython-compiled bytecode comparisons**, with **zero** expected lexical-category mismatches. These are not 3,328 independent semantic tasks. Six hard-coded trusted runtime fixtures × 512 seeded scenarios = **3,072 actual CPython calls**, including **512/512 `UnboundLocalError`** in the call-before-local-binding fixture and 2,560 normal returns. **9/9** final unit tests passed. A separate read-only auditor checked all 6,400 records and reported no disagreements.

An executable compact counterexample is committed as `run289_compact_lexical_witness.py`. The complete source, 3,328-row and 3,072-row raw traces, independent auditor, failure ledger and SHA-256 manifest are preserved in the Run289 local reproducibility archive; the compact GitHub executable is not claimed byte-identical to the full local analyzer.

## Infrastructure and limits

The previously queued Run287 GitHub Actions run [40475919025](https://github.com/sushxnthd/lattice/actions/runs/40475919025) was independently checked and is **completed SUCCESS**.

The qualified independent real-repair cohort remains **four**: Flask PR6096, urllib3 PR5071, Werkzeug PR3136 and HTTPcore PR1000. No new coding-model inference, accepted model repair, prospective independent real issue, powered IR-vs-Python advantage or breakthrough. The original failed Run283 holdout is unchanged. Full historical GitHub artifact mirroring remains incomplete.

## Next protocol

Run a real capable-open-model, gold-blind, paired repair pilot with identical source, facts, edit authority, atomic compiler, isolated oracle, budgets and frozen prompts. Capture checkpoint SHA, seeds, raw completions, tokens, compiler/oracle traces and precompletion failures. Independently qualify more real two-production-source repairs. Extend lexical provenance to CPython class-cell and dynamic-binding adversarial cases, preserving `UNKNOWN`.
