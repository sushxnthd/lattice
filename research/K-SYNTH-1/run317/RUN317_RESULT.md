# K-SYNTH-1 Run317 — Decorator reattachment counterexample and production patch expressibility audit

Date: 2026-10-28 UTC. Branch: `research/exp003-context-order`. Existing PR #9 remains open/draft/unmerged. All 89 reserved boundary issues remain sealed.

## Finding A: structural statement deletion can silently mutate a different function

The Run316 shared AST compiler's `delete_stmt` uses `FunctionDef`/`ClassDef` start locations. Python AST node spans exclude leading decorators. Thus deleting the function/class statement while retaining its decorator lines can attach the decorators to a **different surviving declaration**, without a syntax error. A trusted executed minimal witness leaves `@marker` above a subsequent `protected` function and sets `protected.tainted=True` even though only the unrelated `disposable` function was authorized for deletion. This is an accepted edit with a semantically nonlocal side effect.

**Prospective protocol:** committed `FROZEN_PROTOCOL.md` at `9f6acf017eac2fe7518cb7735c9e806bdd91bf28` before any Run317 main execution. Its initial runner failed its own controls because the old and corrected compilers define distinct `Action` dataclass types. Original failure and stderr preserved; **this first run is invalid as a primary test**. An explicit `POSTFREEZE_HARNESS_ADDENDUM.md` was committed at `318cb60c65acfd95b86a57409aed120bf082462e` before executing a separately identified corrected-harness follow-up. Only the adapter from old to new `Action` type changed; source fixtures and endpoints were not retuned.

**Corrected-harness observed results:** 256/256 decorated deletion attempts were accepted by the old compiler and silently applied a marker to a surviving function/class/method; the corrected compiler rejected 256/256. The 128 undecorated deletion controls compiled identically before/after. Independent read-only SHA/AST-span reconstruction and **768 isolated-process functional evaluations** found zero discrepancies. These are correlated trusted synthetic fixtures across eight attack families, **not** 256 independent repairs. Twelve additional postfreeze decorated/plain edit controls passed. The fix is fail-closed for delete/replace of decorated nodes, pending an explicitly decorator-aware edit primitive. It may conservatively reject legitimate replacements.

**Original source SHA-256:** `005fb330be56bc94ba4e7c8c400a609092e6aa9452a2089e8218f13b7601331f`. **Corrected source SHA-256:** `0d412e45a296e2be56ad9b7a1a3a2c2966e4d064fefa61a0a857c3cf2a9b26c7`. Corrected runner SHA-256 `fae870c428772bf43931fca1aa004c78b513087bb8022efe7e2395d3c20302e4`. Raw trace SHA-256 `d51ab83e3230c7d0d28e65bac41b2928f90715ca60c9f68c3a383feffa599d80`.

## Finding B: actual urllib3 PR #5071 source reference is exact-text expressible

A separate read-only, postfreeze GitHub connector audit fetched the exact historical base `f4e4bc31f40f8c94c6a1f1685df28f97ff48c305` and head `8b6b36f57e139755356074908abbcb0b07732d6d` for three **production** source files. Five distinct old-to-new expression-line replacements each had exactly one occurrence, and applying all five yielded **byte-exact equality with all three historical reference production files** (Git blob SHA values preserved in local JSON). This establishes ordinary-Python exact-text baseline reference expressibility for this repair, but **does not prove** AST-compiler exact patch expressibility, semantic IR expressibility, or model success. Tests and changelog files are excluded. No new qualification is counted.

## Decision and limitations

Six previously qualified historical repairs remain six. No new capable-model completion, independent production-repository repair, powered IR superiority or breakthrough. The 89 reserved issues remain sealed. Main priority is actual production-source structural-compiler expressibility with pinned source/node hashes and a genuinely paired capable-model functional comparison, not more synthetic-only claims. Full local SHA-verified reproducibility archive includes both initial harness failure and corrected follow-up; GitHub mirroring of large raw artifacts remains incomplete.
