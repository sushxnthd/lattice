# K-SYNTH-1 Run478 — literal grammar audit (2026-11-04 UTC)

Executed 30 deterministic Python 3.13.5 parser/tokenizer cases without executing untrusted code. 26 parse as expressions, 19 pass the bounded AST literal family, 7 equal their repr canonical spelling, and 21 pass a conservative lexical hygiene check. Counts overlap.

Counterexamples: `0x3` and `3_0` are valid bounded literals but fail source==repr(value); `3 # injected` parses as a literal but fails lexical hygiene; `3;4` does not parse in expression mode. AST checking alone does not establish textual hygiene, while canonical spelling unnecessarily excludes equivalent literals. This is not a complete production grammar or a soundness proof.

An initial test incorrectly expected `3` followed by backslash-newline to parse; execution falsified it, then the assertion was corrected and the 30-case audit passed. Local reproducibility archive SHA256: 407661bc265b4b3883427cdc666452eb4254cf7718fa71090612afe697fa521c. Source, raw token-level JSON, and internal manifest are in the archive; GitHub mirroring of executable/raw data remains pending.

No model inference or real repair qualification. Two qualified real tasks remain; all 89 reserved issues sealed. Next: a shared formally specified literal grammar and blinded paired model trials on prospectively qualified production repairs.