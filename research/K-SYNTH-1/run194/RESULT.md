# K-SYNTH-1 Run194: complete independent Qwen 7B output audit

**Status (2026-10-23): 8/8 GitHub Actions shards completed, 258 paired tasks, 516 real model completions. This is a synthetic diagnostic, not real-repository evidence.**

## Frozen results

- Model: `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M`, GGUF SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; llama.cpp v0.7.0.
- Original strict scorer: **IR 0/258; Python SSA 0/258**. All **516/516** raw completions were Markdown-fenced JSON, despite a JSON-only instruction. All failed the strict `json.loads` before semantic evaluation.
- Post-hoc mechanical outer-fence removal only (no schema repair or expression modification): **IR 0/258; Python SSA 0/258**. Paired table: (IR fail, Python fail) = 258; all other cells = 0.
- Recovered JSON shape: IR: 236 root-name maps, 1 exact patch envelope, 21 other objects; Python: 220 exact patch envelopes, 38 other objects. This large format asymmetry makes the zero-zero semantic result **uninformative about representation superiority**.
- Post-fence verifier outcomes: IR 257 missing `edits` envelope and 1 invalid patch; Python 36 missing `edits`, 164 invalid patches, 58 self-reference cycles.
- Recorded prompt tokens: IR 124,131 total (mean 481.128); Python 143,286 total (mean 555.372). Recorded completion tokens: IR 15,560; Python 12,223.
- The independent audit regenerated and verified all 516 exact requests, prompt hashes, model IDs, seeds, usage counts, original scorer verdicts, and paired task IDs. **No mismatches.**
- Reference/oracle positive control: 258/258 correct repairs pass the unchanged evaluator, including 64 exhaustive Boolean inputs per task and independent CPython evaluation. This is not model performance.

## Immutable provenance

- Actions workflow and eight retained raw artifact ZIPs: https://github.com/sushxnthd/lattice/actions/runs/39923385972
- Task SHA-256: `f54d4c05b5176f18ecf187d57c144de3ec03b56fa80e7d3077517788f5eb06f7`
- Paired prompt manifest SHA-256: `fa121f0dde370d61c6c5818023fdd9b5194c4b130995d38f06540e51b6dc6a03`
- Runner source SHA-256: `74c3ccbc5da6cfc7b902490c619d45f8b5d48bcf01d0d376a54cb796bb38d023`
- Local reproducibility archive contains all eight original GitHub artifact ZIPs, independent audit script and tests, per-response SHA-256, original scorer replay, recovered-output classifications, and reference positive control.

## Interpretation and next gate

**Run193 failed the measurement-validity gate, not the semantic-IR hypothesis.** Its strict JSON output contract was violated on every request. Post-hoc fence removal is diagnostic only; it does not rescue any correct repairs. The original 258-pair power assumed independent tasks and discordance 0.14/0.06; the actual generator has only four instruction families, two graph topologies, and file labels rather than real files. Do not use nominal McNemar significance or claim a breakthrough.

Next: (1) separately freeze a schema-controlled positive-control study with identical output schema and constrained JSON decoding; (2) build a real multi-repository task set with pinned commits, independent tests and diverse edit families; (3) re-estimate cluster-aware sample size; (4) preregister nontrivial information-preserving dependency-navigation ablation and unseen high-coupling/depth boundary; (5) test two Python-vs-IR reformulations and pivot to a Python semantic verifier/editor if Python matches or wins both. Preserve all negative outcomes.

Related evaluation precedents: https://github.com/SWE-bench/SWE-bench and https://arxiv.org/abs/2404.03543. This audit is a post-hoc output-format sensitivity study, not a preregistered representation-science result.
