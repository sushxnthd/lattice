# Run771: externally pinned CI verification candidate

Date: 2026-11-20 UTC. Research branch: `research/exp003-context-order`; draft PR #9 remains the sole designated research PR.

## Finding
Run769's candidate CI driver computed SHA-256 from the wheel it was checking. This cannot detect replacement of the wheel before verification. The Run771 candidate requires an independently supplied digest (`--sha256`) and delegates to the resource-bounded verifier. For the local alpha fixture, the observed SHA-256 was `73a4c1a6ec1b3fac27ce470d78f76b8337aadd91121f0d696af458d511a9054a`. This published digest is not a signature or authenticated provenance.

## Evidence
Five deterministic local cases passed on Python 3.13: original pinned wheel accepted; wrong digest, malformed digest, modified bytes, and truncated archive refused. Raw traces and reproducibility archive were produced locally. No model inference or untrusted wheel execution occurred.

## Integration status
`research/release_gates/run771_ci_pinned_gate.py` is a candidate requiring `bounded_release_gate.py`, `release_gate.py`, and `record_gate.py` on the Python path. It is NOT integrated into runnable canonical CI. Python 3.11–3.13 matrix remains unexecuted. Public alpha remains unreleased. Do not infer research superiority; only two real production repair tasks are independently qualified. Preserve all 89 boundary issues sealed and the single K-SYNTH-1 kernel.
