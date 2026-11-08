# Run576: logical recovery of two-file partial commits

Executed 16 deterministic scenarios (four injection stages × four recovery policies). A two-file patch may expose a mixed old/new state after the first replacement. Exactly four of 16 pre-recovery observations are mixed; only the no-recovery policy retains that mixed state (one of 16 post-recovery). Twelve of twelve rollback, roll-forward, or journal-phase-conditional recoveries restore a homogeneous pair in this **logical simulation**.

**Critical boundary:** This is not a crash-consistent filesystem implementation. The simulation does not persist journal records, fsync directories, model power loss, concurrent readers/writers, hardlink aliases, symlinks, or tampering. A recovery policy can restore consistency only if trustworthy old/new bytes and journal state survive. Even with recovery, concurrent readers may observe intermediate states. For Lattice's oracle, use an isolated snapshot/worktree and do not advertise cross-file atomicity on the host filesystem. Do not run untrusted model-generated code on the host.

Local reproducibility archive SHA256 af8d3e3ab4794b0def44fc94b67f0e0d15b4727c4f4b9c1cc23e2e21e79b0b9e. Source, 16 raw outcomes, stdout, manifest in archive.

No new real production task qualified; no coding-model evaluation; no superiority claim. All 89 reserved issues remain sealed.
