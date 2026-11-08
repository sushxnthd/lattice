# Run569 — CPython AST UTF-8 coordinate contract

Executed 341 deterministic CPython AST cases over all length-0-to-4 strings from {a, é, 中, 😀}, inserted before a target Name on the same source line. All 341 AST byte slices returned the exact token `target`; naive Unicode-character indexing returned the token in only 5/341 cases and failed in 336/341. These are synthetic compiler contract tests, not real repair/model evidence.

**Mechanism:** CPython AST `col_offset` and `end_col_offset` are UTF-8 byte offsets. A compiler must use UTF-8 byte buffers (with explicit boundary checks), or convert offsets to Unicode character positions before editing. Applying byte offsets to Python string indexing silently selects the wrong span.

**Method:** parse `v = {prefix!r}; result = target + 1`, take the left `Name` of the second assignment's `BinOp`, compare `source.encode('utf8')[col_offset:end_col_offset]` to `source[col_offset:end_col_offset]`. Exhaustive Cartesian enumeration of four prefix symbols at lengths 0..4. The source includes a string literal whose printed representation may itself differ from prefix length; the assertion uses actual parser locations, not guessed offsets.

**Status:** 2 qualified independent real production repairs unchanged. No coding-model calls, no superiority claim. 89 sealed issues untouched. Full raw data and executable are preserved in local SHA-verified Run569 archive; GitHub report alone is not full mirroring. Next: prospectively freeze and independently qualify a new multi-production-source real repair, then blinded paired comparison.
