# Run570: bounded atomic UTF-8 multi-file compiler contract

Locally executed 1,000 deterministic seeded two-file Python transactions with three non-overlapping edits, SHA-pinned source checks, UTF-8 byte boundary validation, overlap rejection, and syntax validation before returning immutable updated file mappings. All 1,000 succeeded. Two labels (IR and Python/AST) constructed identical canonical edit transactions and matched on all 1,000 cases by construction. All 3,000 adversarial transactions (stale source SHA, overlap, invalid UTF-8 boundary) were rejected.

The initial test run failed because the invalid-boundary fixture used an ASCII offset; the fixture was corrected to force a leading emoji and target an interior byte. The corrected run passed. Local ZIP SHA256: `1f9c3ab84c3ac797e140ff1dd82d8e5b1b3cc59b13cdac4afa15774c5893ef7f`. Complete raw source/results are in the local archive, not yet mirrored on GitHub.

This is synthetic compiler-contract evidence, **not** genuine model inference, real public-repo qualification, production soundness, or evidence of semantic-IR advantage. Two qualified independent real tasks remain (Flask PR6096, urllib3 PR5071); all 89 reserved boundary issues remain sealed. Werkzeug PR2535 remains disqualified under its original frozen criteria.
