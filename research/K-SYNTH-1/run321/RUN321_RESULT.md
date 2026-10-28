# K-SYNTH-1 Run321: AST congruence as a fail-closed compiler invariant

**Prospective protocol commit:** `9d5fba4fc090c55b28925c74c52fdb7df9754dd7`. The two exploratory Run320 witnesses were excluded from primary data.

## Primary prospective experiment

Seed 321028; 512 correlated trusted synthetic fixtures, eight fixed contexts × 64. The unchanged Run320 structural compiler accepted 496 patches, **176 of which changed the AST outside the intended target substitution**. Sixteen original patches were rejected before congruence comparison. The new AST-congruence guard accepted 320, rejected all 176 unsafe originally accepted patches, rejected zero originally safe patches, and accepted zero AST-mismatched patches. All frozen decision criteria passed.

| Measure | Result |
| --- | ---: |
| Original compiler accepted | 496/512 |
| Original accepted with wrong AST | 176/496 |
| Guard accepted | 320/512 |
| Guard accepted with wrong AST | 0/320 |
| Original AST mismatches escaping guard | 0/176 |
| Safe original patches rejected by guard | 0/320 |
| Independently audited fixtures | 512/512 |
| Trusted isolated functional replays | 320/320, zero mismatches |

The independent auditor reconstructed the expected AST without importing the guard, checked source and patch SHA-256 hashes, and compared trusted generated function results in a Python `-I -S` subprocess. Zero discrepancies. The raw local JSONL preserves each fixture's source, action, AST dump, patched source, hashes, decisions and failures.

## Postfreeze exploratory multi-file test (not part of frozen primary)

128 two-file transactions with one deliberately unsafe expression edit were rejected in full; 128 separate two-file safe transactions were accepted. All 256 input snapshots remained unchanged. This does not validate concurrent publication or filesystem durability.

## Scope

For the supported one-expression-per-file action subset, accepted patched modules have the same parsed AST, ignoring location metadata, as an explicitly constructed target-node substitution. This is a bounded **structural** guarantee, not proof of runtime equivalence in every environment. It does not cover statement edits, multiple actions in one file, arbitrary Python features, source comments as first-class data, or malicious concurrent writers. The 512 fixtures are correlated synthetic cases, **not independent production repairs**.

No coding-model inference or IR-versus-Python superiority claim follows. The six previously reported qualified historical repairs remain six; this run did not re-audit that count.

## Evidence

Local primary raw JSONL SHA-256: `00a7ba8f5bbcd514fa7618e7712e95838b60cef803df87924279315fbd42337d`.
Independent functional traces SHA-256: `3440ad324ca6d16bb43f9aa08fb7bb1295ce2f3f28cc1d34d6bebb713eb38c52`.

The complete local archive includes the frozen protocol, original baseline dependencies, exact executed source, raw traces, independent auditor, postfreeze experiment, stdout/stderr and SHA-256 manifest. The GitHub guard and primary experiment files are source mirrors; the SHA-verified archive is authoritative for the exact locally executed source. No independent GitHub Actions reproduction was performed for Run321.

Canonical branch `research/exp003-context-order`, one PR #9 open/draft/unmerged verified at start. All 89 reserved boundary issues remain SEALED. Historical GitHub artifact mirroring remains incomplete.

## Run322 priorities

1. Prospectively freeze multiple-action-per-file and statement-edit AST congruence, including decorated functions, comments and Unicode.
2. Verify exact reference expressibility on another qualified multi-production-source repair, with identical IR and ordinary Python/AST authority.
3. Execute genuine paired capable-model inference with raw prompts, model hashes, seeds, tokens, compiler traces and isolated oracle outcomes.
4. Continue independent repository recruitment and historical artifact mirroring without delaying science.
