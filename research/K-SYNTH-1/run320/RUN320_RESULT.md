# K-SYNTH-1 Run320: orphan-decorator transaction-boundary counterexample

Date 2026-10-28 UTC. Canonical branch research/exp003-context-order, one draft/unmerged PR #9. All 89 reserved boundary issues sealed.

## Counterexample

Run317's replace_stmt accepted replacement text consisting solely of @marker, since only the assembled file was compiled. Replacing an unrelated assignment immediately preceding def protected(): ... caused @marker to bind to the next declaration. A trusted isolated Python execution observed protected.touched == True even though protected was not the edited AST target. insert_before admitted the same incomplete-statement payload. This is a bounded compiler correctness defect, not a deployed exploit or a malicious model completion.

## Prospective freeze, original failure, corrected results

Original prospective protocol commit d3345f1721e5cb00611613768402e6d361885629 froze source hashes and 8 families x 32 variants x 2 operations = 512 correlated attacks, 512 benign controls, 128 cross-file rollback controls, and an independent read-only auditor.

The original frozen harness failed before its first completed scientific case: Action dataclasses from two compiler modules were distinct, producing PatchRejected("unauthorized action"). The original traceback is preserved locally. The correction was registered BEFORE rerun in addendum commit 21aec7ae2942ef92f552a743944c7c1124326df3. The original run is not retroactively successful. The separately labeled POSTFREEZE CORRECTED harness SHA256 is 8cca424f3f3208f801570228ecf4b05a4d17c5974ea7c40078619fa993d72739.

Corrected results:
- Original compiler accepted 512/512 orphan-decorator attacks and isolated execution observed 512/512 touched=True.
- Hardened compiler rejected 512/512 incomplete statement replacements.
- 512/512 benign complete-statement edits accepted by both compilers, with byte-identical output and no unexpected decoration.
- 128/128 mixed multi-file malicious transactions rejected without mutating inputs.
- Independent read-only auditor reconstructed 512 attack outputs and 512 benign outputs, verified 512 decorator AST changes and replayed 1,536 trusted CPython subprocess evaluations with zero discrepancies.
- Raw trace SHA256 b8ba053e89b0d5fa0ef5a07b70d76f9c166432a34036b04e586acf2f897447ea; CPython 3.13.5.

Mitigation: require replace_stmt and insert_before payloads to parse as exactly one complete standalone AST statement before insertion. Narrow guard committed b48198887cc2412453eec66df4189a72cc1cf4db, Git blob verified 414ddedadbbc47ea469166e93fd4bf5b03e7b7f1.

## Additional exploratory unfixed defects

Even the hardened compiler accepts replace_expr "1 #" in x = 1 + 2, producing x = 1 # + 2 (value 1 instead of AST-substitution value 3), and replace_expr "1 + 2" in x = 3 * 1, producing x = 3 * 1 + 2 (value 5 instead of intended 9). Both are trusted postfreeze exploratory witnesses, NOT frozen Run320 outcomes. Next: enforce AST-context congruence, not merely parseability.

These are correlated synthetic fixtures, not independent production repairs. Six historical qualified repairs remain six. No new coding-model inference, powered IR advantage or breakthrough. Local full SHA-verified evidence archive is available; GitHub raw-artifact mirroring is incomplete.
