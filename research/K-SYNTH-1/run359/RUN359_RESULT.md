# K-SYNTH-1 Run359 — Original expanded-context Qwen artifact, independent syntax audit

Date: 2026-10-30 UTC. One canonical K-SYNTH-1 kernel; draft PR #9 remains open/unmerged. All 89 reserved boundary issues remain SEALED and untouched.

## Original evidence
Recovered original [Run358 GitHub Actions #41007904628](https://github.com/sushxnthd/lattice/actions/runs/41007904628), artifact ID **12958880623**. ZIP SHA-256 `d86cf50ce87ad283935a53b485327988288ac69036ca870d059757ce02f38b66`; **28/28 original manifest entries** verified. Frozen prompts, facts SHA, base `c46802478cdd8a82ee8cb333420080fab1aed00b`, and both historical production Git blobs independently matched. The original isolated baseline oracle reproduced **6/10** cases. Model SHA record identifies Qwen2.5-Coder-7B Q4_K_M `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; this audit verified the recorded digest, not the model bytes.

Both genuine model requests completed with `finish_reason=stop`. Actual request prompt tokens before chat overhead were **14,315 IR / 14,909 Python/AST**, API prompt usage **14,344 / 14,938**, and completion usage **905 / 267**. Both fit the 20,480-token context. **594-token prompt imbalance remains.**

| Frozen outcome | IR | Python/AST |
|---|---:|---:|
| Original JSON edit actions | 16 (8/file) | 4 (2/file) |
| Shared compiler | `Reject:PYTHON_SYNTAX` | `Reject:PYTHON_SYNTAX` |
| Candidate accepted | No | No |
| Isolated candidate oracle | Not reached | Not reached |
| Valid repair | Not established | Not established |

Independent text-only staging identified IR replacements at original lines 328 and 335 in each file that break existing `for` and `with` suites. Python/AST's replacement at line 163 in each file produces unexpected indentation. No untrusted model code was executed on the host.

## Exhaustive diagnostic, not retrospective scoring
Enumerated **520** per-file subsets: 256 each for the two IR files and four each for the two Python/AST files. Independent reconstruction verified **520/520** candidate hashes and AST outcomes: **132 syntactically valid / 388 invalid**. IR: 64/256 syntactically valid per file, yielding 4,096/65,536 theoretical cross-file combinations. Python/AST: 2/4 per file, yielding 4/16 combinations. In each IR file two individually syntax-invalid edits poison all subsets containing them; in each Python/AST file one edit does. The other subsets were **not** sent to the oracle. Syntax validity is not functional correctness, and post-outcome subset selection cannot be counted as model repair.

**15/15 local adversarial and independent-audit tests passed.** Full original ZIP, raw completions, source, 520 traces, independent auditor, test suite, and SHA manifest are in the local Run359 reproducibility archive (SHA-256 `56c05c7761757b5bcc73a7a1e5c2af3c58838746b6b1b278087c5aef2f18ded1`).

**Decision:** Expanded context removed precompletion overflow but both frozen model transactions failed at syntax validation. This is a shared grammar/localization failure, **not** evidence for IR or Python superiority. No new independently qualified production task, powered comparison, or breakthrough. Do not retune failed Werkzeug PR2535. Proceed with prospectively frozen, token-balanced, independent multi-production-source repairs, shared compiler and isolated oracle.
