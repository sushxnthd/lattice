# K-SYNTH-1 Run316 frozen adversarial publication protocol

Preexecution prospective freeze, 2026-10-28. The primary endpoint is whether the Run315 hardened publisher allows a **pre-existing lexical ancestor symlink** above the store directory to redirect a trusted snapshot outside the intended lexical store path. The bounded fix rejects any pre-existing symlink component of the lexical store ancestry. This is a filesystem path confinement claim, **not** a claim of security against concurrent malicious writers, power loss, or crash consistency.

Source SHA256:
- run315_multifile_compiler.py: `9031621afe53a3d26c961a3a93cbe718730c10f4d327867f014c1ff806f466fe`
- run315_snapshot_store_hardened.py: `44fd74f2b6f36075659836d8f31d594190313f4c182e3791a1ab7463e545d01e`
- run316_snapshot_store_v2.py: `2b912ec63fa46789e24f9f0cac93e8328809ce432281d9d065cf051d271750be`
- run316_adversarial_experiment.py: `ca492a16cf87dd338f73eb4fc617103dd203aa912cd0f24cb06c000776d4df4c`

All experiments use trusted generated `.py` fixture bytes and `TemporaryDirectory` paths. No model code executes on the host.

Frozen primary checks: 32 parent-symlink escapes must be reproducible on the original and rejected by the bounded fix; 128 honest same-ID concurrent publication pairs; 128 honest distinct-ID concurrent publication pairs; 128 injected failures preserving the pointer; 16 pre-existing `snapshots` symlink rejections; 16 pre-existing content-addressed final-snapshot symlink rejections. Every published snapshot is verified against its SHA256 manifest. Honest concurrency checks are nondeterministic in ordering, but the invariant is frozen. Record all exceptions without post-hoc removal. Failure of any check means experiment FAIL, and the failure must be retained.

This is a local engineering/security negative-control experiment, not a real-repository repair, model-inference result, independent evaluator, or breakthrough. Six previously qualified historical repairs remain six. All 89 reserved issues stay sealed; no new branch or PR.
