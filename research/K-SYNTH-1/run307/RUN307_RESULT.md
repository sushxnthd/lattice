# K-SYNTH-1 Run307: version-aware annotation effects

**Status:** prospective trusted CPython 3.13.5 experiment complete and independently replayed; Python 3.14 remains a **symbolic prediction pending original cloud artifact verification**. No sixth real repair, coding-model inference or representation breakthrough.

Protocol frozen at commit `f4e506e942bc6c919d8d15f8679127fce80ac033`; source-manifest SHA frozen at `fa0da9666d00f49538cdbcc99b12133859f43656`, both before functional execution.

256 frozen trusted fixtures = 2 future-import modes x 2 annotation effects (restore builtin `len` / no-op) x 4 annotation-access patterns (none/direct/alias/repeat) x 16 syntactic variants. Frozen manifest SHA-256: `f2646b6dd96169c19cdb3474d3011354124b893e5829fd719ea02d06075da95b`.

## Measured CPython 3.13.5

- 256/256 original trusted subprocess outcomes matched frozen expectations.
- 256/256 independent subprocess replays matched; all 256 source SHA entries verified.
- 64/256 executions restored the builtin `len`; 192 did not.
- Analyzer: 128 `UNKNOWN_DYNAMIC`, 128 `NOT_KNOWN_TARGET`, zero false-negative builtin exclusions under the bounded fixture assumptions.
- 128 eager annotation-effect events; none under `from __future__ import annotations`.
- Four local test families passed.
- Original JSON SHA-256: `416dc4057d7f94d4a7dbac3e88159482c8c5ee394dfb1a9afa32d0882377c31b`.

## Python 3.14: NOT YET EMPIRICALLY VERIFIED

Under PEP 649/749, annotations default to lazy evaluation on first access, cached on subsequent accesses, including aliases. The bounded transfer predicts 48 builtin restorations, 96 unknown final calls, 160 definite non-target calls and 96 annotation-effect events across the same 256 fixtures. These are **normative predictions, not executed 3.14 traces**. Symbolic JSON SHA-256: `d38cac6716943afb323c07d67a90f4e3fc308948d95dbc145087b1a863d5a641`.

Committed original 3.14 GitHub Actions workflow at `a2450549049137d2382e13bbfe83a04c494a7775`, with PR trigger at `c5dc86db52eeef6693aa79780cf785786a3b2f2c`. Original cloud run/artifact remains unverified. Local Python 3.14 installation failed due to DNS resolution, preserved as infrastructure failure.

## Bounded mechanism and limitations

A function annotation may call code that mutates module aliases. On 3.13 default this happens at definition; on 3.14 default at first annotation access. Returning definite non-target without accounting for that effect is unsound in the trusted subset. The implemented analyzer returns explicit UNKNOWN for unmodeled effects and unsupported runtime versions; it does not establish Python-wide soundness. Reflection, descriptors, closures, metaclasses, exceptions and concurrency remain open.

Independent read-only audit: 256 source hashes, 256 subprocess replays, zero discrepancies. All fixtures are correlated, not independent repairs. Official references: https://docs.python.org/3.14/library/annotationlib.html , https://peps.python.org/pep-0649/ , https://peps.python.org/pep-0749/ .

Next: independently audit original Python 3.14 cloud artifact, qualify sixth real multi-production-source repair, conduct valid paired capable-model IR vs ordinary Python/AST-action editing. Keep one K-SYNTH-1 kernel, canonical branch, one OPEN/DRAFT/UNMERGED PR #9, 89 reserved boundary issues SEALED. No powered superiority or breakthrough claim.
