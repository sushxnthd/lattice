# Run530: conservative module-binding compiler precondition

2026-11-06 UTC. One K-SYNTH-1 kernel, research/exp003-context-order, PR #9. All 89 sealed issues untouched.

A scope-aware static precondition distinguishes top-level assignments from function/class-local bindings and refuses uncertain control flow. Twelve deterministic source cases passed locally, including function shadowing, conditional/try assignment, dynamic exec, import rebinding, and destructuring. This corrects Run529's concrete lexical-scope misclassification in the bounded subset.

UNIQUE_STATIC_MODULE_BINDING means only one syntactically direct unconditional module-level assignment was found in this bounded AST scan. It does not certify runtime uniqueness, execution, semantic identity, monkeypatch absence, or repair correctness. Additional Python constructs remain unhandled. The scanner is exploratory, not production-approved or sound semantic IR.

Local reproducibility archive /mnt/data/lattice_run530/run530.zip SHA256 7d5af73ab50cb5843ce8ba4543eed7b5962c48539100aeb1b704404f307f0031; contains experiment.py, raw_results.json, REPORT.md and SHA256 MANIFEST.json. No model inference, no new qualified real production repair, benchmark remains n=2. Raw code/results GitHub mirroring outstanding.
