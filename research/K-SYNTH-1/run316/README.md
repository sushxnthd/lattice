# Run316 reproducibility

Run316 uses the exact frozen Run315 compiler and hardened publisher as dependencies. Their Git blob SHA-1 values are `d510a4600e8c4ba8726e6586a51efaa4ca017589` and `829b304856cbb4bb32ddeaf8c01d2de58ea014e3`, respectively. The Run316 security and editor protocols were committed **before** executing their tests.

From the repository root on a trusted Linux machine with Python 3.13:

```bash
cd research/K-SYNTH-1/run316
export PYTHONPATH="$PWD:$PWD/../run315"
python run316_adversarial_experiment.py
for start in 0 16 32 48 64 80 96 112; do
  python run316_partitioned_transport.py "$start" "$((start+16))"
done
python run316_negative_controls.py
python run316_independent_audit.py
```

The editor test runs trusted generated Python fixtures in isolated Python subprocesses. Never run untrusted model completions on the host. This script is not a substitute for a sandboxed production oracle.

Primary observed results: 32 original parent-symlink escapes and 32 corrected rejections; 128 same-ID and 128 distinct-ID honest concurrent publication pairs; 128 injected rollbacks; 16 snapshots-symlink and 16 destination-symlink rejections. The structural editor produced 128/128 byte-identical expected outputs, 128/128 trusted isolated functional passes, 512 SHA-scoped edits and 8/8 negative-control rejections.

Full 28-entry SHA-verified raw-evidence ZIP remains local; raw GitHub artifact mirroring is incomplete. See [RUN316_RESULT.md](RUN316_RESULT.md) for limitations, including no malicious-concurrency security proof, no qualified production repair, and no model inference.
