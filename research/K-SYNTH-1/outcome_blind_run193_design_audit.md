# K-SYNTH-1 Run193: outcome-blind design audit

Committed before reading any capable-model outputs. The GitHub Actions 7B run is in progress. This audit does **not** report model performance.

- 258 deterministic synthetic Boolean tasks; 516 paired prompts; one shared semantic compiler and independent CPython AST evaluator.
- Four distinct repair instructions, with family sizes 66, 64, 64, 64.
- Two node-count topologies: 129 tasks with 10 nodes and 129 with 11 nodes. One shared four-file logical mapping.
- Mean prompt lengths: semantic graph 1,495.25 characters; Python SSA 1,705.54 characters. Python is longer by 210.29 characters on average. The shared model context and output limits do not remove this representation-length confound.
- Predeclared task manifest SHA-256: `f54d4c05b5176f18ecf187d57c144de3ec03b56fa80e7d3077517788f5eb06f7`.
- Predeclared paired-prompt hash manifest SHA-256: `fa121f0dde370d61c6c5818023fdd9b5194c4b130995d38f06540e51b6dc6a03`.
- Source SHA-256: `74c3ccbc5da6cfc7b902490c619d45f8b5d48bcf01d0d376a54cb796bb38d023`.
- Pinned official Qwen2.5-Coder-7B-Instruct Q4_K_M GGUF SHA-256: `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`.

**Exact four-cluster sign-test resolution:** under independent sign flips of the four instruction families, even all four family effects having the same sign yields a minimum attainable two-sided p-value of `2/16 = 0.125`. With eight independently exchangeable family-by-capture cells the minimum would be `2/256 = 0.0078125`, but independence of those cells is not established. This does not assert that every valid statistical procedure has this p-floor; it demonstrates that treating 258 correlated generated tasks as independent is indefensible.

**Decision rule:** Run193 can establish whether the capable model produces meaningful successes in either representation on a synthetic diagnostic. It cannot establish real-repository superiority or satisfy the breakthrough gate, regardless of its nominal task-level p-value. The next experiment must vary genuine repository repairs, freeze unseen structural boundaries, and run a mechanism ablation that actually changes the model's information-access structure while preserving facts.

GitHub Actions run: https://github.com/sushxnthd/lattice/actions/runs/39923385972
