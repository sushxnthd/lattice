# Run439 prospective issue-first freeze: Flask #4834

Frozen **before inspecting any fixing PR or reference diff**.

- Issue: https://github.com/pallets/flask/issues/4834
- Historical baseline: Flask tag 2.2.2, resolve and pin full commit SHA before executing.
- Fixing reference selection: first upstream merged PR explicitly resolving issue #4834; record immutable SHA and changed production files before outcome inspection.
- Local complete frozen oracle: `run439_flask4834_frozen_oracle.py`, SHA-256 `8cec6cd6938a1b42025966f9dba4bb12b6be1ff977002391c81aaddf9048d36f`.
- Local detailed freeze: `RUN439_FLASK4834_PROSPECTIVE_FREEZE.md`, SHA-256 `9fea3fc9ca2d646c933e4ebef70a993e98207412410cac5e8de1d884f87469a6`.

Frozen 8-case oracle: T1 child inherits parent subdomain; T2 grandchild inherits; T3 combined prefix and inherited subdomain; C1 parent subdomain; C2 root host; C3 nested prefix-only; C4 unrelated subdomain must not expose child; C5 unrelated subdomain must not expose parent/root.

Qualification requires baseline fails a target and passes all five controls, full reference passes all eight, >=2 production Python sources changed, and removing each of at least two distinct reference source components causes a frozen target OR control failure. A successful one-source reference alternative disqualifies. Same pinned dependency closure, isolated subprocesses, source hashes and raw output required. No retuning, no post-reference qualification, no proof that all possible fixes require two files.

This is a **screening candidate only**. No model inference. All 89 reserved issues sealed. One K-SYNTH-1 kernel, branch `research/exp003-context-order`, one draft/unmerged PR #9.
