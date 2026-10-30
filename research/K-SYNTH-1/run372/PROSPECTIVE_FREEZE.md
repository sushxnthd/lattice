# K-SYNTH-1 Run372 prospective freeze (reference-blind)

Freeze date: 2026-10-30 UTC. This was committed before opening any reference fix, patch, or reference tests.

Issue: https://github.com/agronholm/anyio/issues/642
Pre-fix tag: 4.1.0; commit: 46a45c7454e4d87ab5671b158f746a2b3beaaae9.
Candidate source files, selected by public API boundaries:
- src/anyio/_backends/_asyncio.py blob 9827e55090640af5c37a8de6db2c0903380267fe
- src/anyio/_core/_tasks.py blob 2f21ea20b13e0653e288161082e503f81162b507

Targets (asyncio): T1 shielded main wait must not shield sibling cancellation; T2 same with two sibling observers; T3 same with nested main shield. All must finish in 2s.
Controls: C1 unshielded group cancellation; C2 inverse sibling-shielded scenario from issue; C3 local shield protects its own task without shielding unrelated sibling; C4 ordinary task-group completion.

Use isolated hard-timeout processes; preserve raw stdout, stderr, exceptions, versions and hashes. Pre-oracle import failures are not functional failures. Four arms: exact historical base, each single-file reference swap, exact historical reference. Qualification requires base fail >=1 target, all controls pass; reference all targets and controls pass; each partial fail >=1 target or control; no import/ABI unknowns. A single-file reference change or any baseline-control failure means NOT QUALIFIED. No post-outcome criteria changes. Installed AnyIO 4.13.0 results are exploratory only. No model win without raw paired model evidence.

One K-SYNTH-1 kernel; research/exp003-context-order; one open draft unmerged PR #9; 89 boundary issues sealed.
