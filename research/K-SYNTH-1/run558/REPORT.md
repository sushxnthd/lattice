# Run558: atomic original-coordinate edit ordering counterexample

Executed exhaustive synthetic enumeration of 400 ordered pairs of edits on base string `abc`. Edits use half-open original-source coordinates and replacement strings from {empty, X}. A conservative transaction compiler rejects overlapping replacements and same-start operations; accepted edits apply right-to-left.

Observed 168 conflicts, 232 accepted transactions, 78 accepted pairs where naive sequential application is order-sensitive, and 39 accepted pairs where naive forward application differs from the atomic result. The atomic compiler was invariant to input ordering on all 232 accepted pairs. Four assertions passed after fixing a discovered same-start insertion ambiguity (initial assertion failed; corrected by rejecting same-start operations).

Implication: both IR and ordinary Python/AST-action conditions must use the same atomic original-coordinate transaction compiler, including deterministic conflict policy. Sequential application is not equivalent even with non-overlapping edits.

No production repair, model inference, semantic superiority, or new qualification. Two real qualified repairs remain. All 89 reserved issues remain sealed. Local archive SHA256: 8f5d0c2029f5c900bfd8f43707b02646f22ca47f3ab69224ffcf0c3689cfe76b. Raw 400-case matrix and source in local archive; GitHub raw mirroring outstanding.