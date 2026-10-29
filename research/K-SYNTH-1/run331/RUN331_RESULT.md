# K-SYNTH-1 Run331: original Run330 recovery and AST-baseline counterexample

**2026-10-29 UTC.** This is a post-outcome independent audit, not newly preregistered model inference. The original Run330 cloud execution [40805383096](https://github.com/sushxnthd/lattice/actions/runs/40805383096) completed successfully. Its original artifact 12868064523 has ZIP SHA-256 `6645a898b5ae3b51de78f45a2271a5205434a5dc0762cc20b019123e8df9672a` (1,695,317 bytes). **37/37** original evidence-manifest entries passed SHA-256 checks. The stage checkout is not included in that manifest; the two frozen production source hashes were checked separately.

## Original, unchanged Qwen evidence

Qwen2.5-Coder-7B Q4_K_M SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. Both positive-control gates passed. Both real requests finished normally with the **same** 31-token completion:

`{"edits":[{"id":"Df26e71a760d4","new_expr":"True"}]}`

Both compiled successfully and modified only the default in `httpx/_api.py.head`. `httpx/_client.py` stayed byte-identical to its frozen baseline SHA. The original isolated nine-case oracle scored baseline **6/9**, IR **7/9**, Python/AST **7/9**. The API HEAD target improved; both Client HEAD targets remained broken; all six controls passed. Both are valid *partial* repairs, not complete repairs. Prompt tokens: IR **4,059**, Python/AST **4,620** (13.82% more).

## New independently reproduced structural defect

The original Python/AST prompt labels all 31 default-argument candidates `ast.FunctionDef.args.defaults[allow_redirects]`. In the exact historical Python AST, **29/31** candidates use keyword-only parameters, whose values live in `ast.arguments.kw_defaults`, **not** `args.defaults`. Only two internal `_send_handling_redirects` candidates use positional defaults. The audit reversed the model's single source-token change and verified the reconstructed `httpx/_api.py` against the prospectively frozen baseline SHA, then parsed both production files with standard-library `ast`. A corrected prompt was generated and SHA-frozen **but never sent to a model**.

Therefore the Run330 Python/AST presentation was not a fully truthful structural baseline. This is a real confound, **not** evidence that the confound changed the result: both original arms generated identical edits and oracle outcomes. Context-length differences are another uncontrolled factor.

The independent read-only auditor checked original ZIP manifest, prompt/request/model/seed hashes, raw completion hashes, finish reasons, compiled edits, source SHA, AST structure and nine-case oracle records. Five deliberately corrupted evidence packages were detected, including a forged oracle verdict with recomputed manifest. No untrusted model code ran on the host; the original oracle executed in isolated cloud Docker.

## Decision

**No semantic-IR superiority, powered result or breakthrough.** Three independently qualified historical production issues remain Flask PR6096, urllib3 PR5071 and HTTPX PR1183. Previously failed candidates remain failed. All 89 reserved issues stay sealed. PR #9 stays open/draft/unmerged on the same branch.

Local Run331 reproducibility ZIP: `lattice_run331_original_model_and_ast_baseline_counterexample.zip`, SHA-256 `f9ec06a95a5730e82b22eb7ccb95b8f8230257262108a6b9485999ed9be00847`, containing original Run330 cloud ZIP, independent audit source, all original model completions, functional traces, 31-row AST audit, five tamper tests, corrected-but-unexecuted request, and SHA manifest.

**Next:** prospectively freeze a corrected 29 keyword-only / 2 positional Python-AST prompt, verify 31/31 entries, use a two-action positive-control gate, then run new paired inference and isolated functional oracles. Keep Run330 original results separate. Expand independently qualified repositories for cluster-aware powered inference.