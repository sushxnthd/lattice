# Run563 — bounded definite-assignment prototype

Executed six synthetic CPython AST examples with 18 emitted facts and six passing assertions. The prototype intersects definite assignments across conditional branches and marks unsupported syntax UNKNOWN, clearing known bindings. A first assertion failed because the expected line number was 9 instead of 8; this was corrected and the six assertions passed.

This is NOT a sound general Python dataflow analysis: exceptions, global/nonlocal bindings, comprehensions, dynamic scope and expression side effects are not modeled. MUST is a syntactic fact under a restricted subset, not proof of runtime name resolution or repair soundness. Production IR must enforce a restricted grammar or downgrade unsupported semantics to UNKNOWN.

Local SHA-verified archive: lattice_run563.zip SHA256 1c4b9262738f2bd9cf892a220464f8c0eeaff5bed87189c357db48396a94fe48. The local archive contains reproduce.py, raw.json, REPORT.md and SHA256SUMS; GitHub source/raw mirroring is pending. No new real qualified repair, no model inference, no superiority claim. All 89 reserved issues untouched.