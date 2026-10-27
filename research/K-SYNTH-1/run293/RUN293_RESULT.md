# K-SYNTH-1 Run293 — Boolean short-circuit alias false negatives and prospective holdout

## Chronology and results

1. The original 16-case specification was committed BEFORE execution at 3331b3adccb52818d9117524587236c608eaaafc (frozen JSON Git blob 744a4c3176ac47573b17f62e9d4f82883de9e176). Original Run292 analyzer SHA-256: 12f266e715a4f69ff3f691305e899ec546a1521736d76395a96a8ef5c7d44d46.
2. The original Run292 analyzer produced **11/16 definite false-negative MAY-call sets** (empty candidates, unknown=false, despite a real target call), plus five UNKNOWN_DYNAMIC abstentions. All 1,024 trusted CPython 3.13.5 outcomes matched their frozen event expectations. These are 16 correlated semantic templates, not 1,024 independent repair tasks.
3. The corrected bounded transfer joins Python BoolOp operands, tracks NamedExpr bindings and returns UNKNOWN on unsupported expressions. All 16 exposed templates are covered, but this is POSTHOC correction, not prospective success.
4. Eight NEW unseen cases were frozen BEFORE execution at 3db919d633c82cfc1aacd9424df337ffa16aff9e (Git blob 440c08c027ae1dad351e101b7bb20dceb091e993). The corrected transfer covered **8/8 frozen holdout templates under the predeclared coverage-or-UNKNOWN rule**: six had non-abstaining candidate sets and two retained UNKNOWN. All **512/512** actual CPython outcomes matched the frozen events, with no censoring. The two UNKNOWN cases do not establish precise alias identification.
5. A separately written read-only auditor reconstructed source hashes, checked row completeness, uniqueness, event predictions and exceptions for **1,536/1,536** observations with zero discrepancies. Eight local tests passed.

## Mechanism

Python and/or expressions return an operand rather than necessarily a Boolean. A source-only alias MAY-call transfer that treats an unhandled BoolOp as a known empty candidate set is unsound even for a straight-line alias such as g = f or sum. The repaired transfer overapproximates possible operand origins and propagates walrus assignments. This is a narrow conditional source-provenance result, not verified builtin identity, general Python soundness or coding-model superiority. Unsupported semantics remain UNKNOWN.

## Scientific status

**Four independently qualified real issues**: Flask PR6096, urllib3 PR5071, Werkzeug PR3136 and HTTPcore PR1000. No fifth qualified issue, no new coding-model inference, no powered semantic-IR versus information-equivalent Python repair result, and no breakthrough. Original Run292 seven post-freeze mismatches and all earlier negative results are preserved. All 89 reserved boundary issues remain SEALED.

The full SHA-256 verified local reproducibility archive includes both original and holdout frozen specifications, all 1,536 raw observations, source-only transfer, tests, independent auditor, executable counterexample, and previous Run292 evidence. Historical GitHub ZIP mirroring remains incomplete.

## Next decisive work

Prioritize genuinely paired no-cost capable-model inference on four qualified real issues with identical task facts, source, edit authority, model checkpoint SHA, seeds, token budget, shared atomic compiler/verifier, and independently isolated public/heldout/nonregression oracle. Capture raw prompts/completions, token counts and failures. Independently qualify additional multi-production-source production issues, with no retuning of failed Werkzeug PR2535. Preserve draft PR #9 on the same branch and do not unseal the 89 reserved issues.
