# K-SYNTH-1 Run477: canonicalization changes the accepted language

## Scope
A pre-registered-style *instrumentation audit*, not a production repair or model experiment. Run476 adopted a canonical literal policy to exclude comments and trailing source. That policy is stricter than the AST-literal grammar and must be treated as a shared compiler restriction, not as semantic necessity.

## Deterministic counterexamples
For example, Python parses `0x3`, `+3`, `(3)`, and `3 # note` as expressions with the integer value 3, while the canonical spelling `repr(3)` is `3`. Likewise `"a"` and `'a'` yield the same string but only the latter matches `repr("a")`. Requiring exact canonical spelling excludes syntactically valid, semantically equivalent literals. The script enumerates 15 cases: 3 canonical accepted, 8 valid noncanonical rejected, 4 invalid or disallowed. The comments are excluded intentionally for source-hygiene reasons; this is not a Python-semantic difference.

## Interpretation
A paired comparison must apply **the same accepted language** to both representation arms. Normalization or canonicalization can be justified for security and determinism but cannot be advertised as preserving all Python-literal expressibility. Distinguish: (1) AST parses, (2) bounded literal-value grammar accepts, (3) canonical source accepts, (4) edit-authority/preimage checks pass, and (5) oracle behavior passes. These are separate events. No code from model output is executed.

## Evidence and limits
`run477_canonicalization_audit.py` contains executable assertions and emits raw JSON plus a SHA-256 digest when run with Python 3. This report does not claim that Python execution was performed in this automation environment; the 12-case abstract enumeration was executed separately, and this more precise 15-case Python parser check awaits independent execution. All 89 reserved issues remain sealed. Only two real production tasks qualified historically. No superiority or powered inference claim.

## Next
Execute the Python script independently, pin Python interpreter/version and source SHA, retain stdout and full provenance. Then prioritize prospectively frozen real multi-source qualification and actual paired model inference rather than further synthetic-only studies.
