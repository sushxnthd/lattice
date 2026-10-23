# K-SYNTH-1 Run202 — matched structural-address pilot (2026-10-23)

Status: prospective design and local compiler evidence; **no capable-model inference yet**.

The previous Run200/201 comparison used identical Python edits with AST-first versus source-first presentation. It did **not** compare distinct editing interfaces. Run202 corrects that confound with a 2×2 factorial design: semantic-target-ID versus exact-Python-text anchoring, crossed with target-table-first versus source-first context. Both arms receive the same issue statement, source bytes, AST target table, hashes, exact preimages, allowed files, compiler and verifier. The sole address-schema difference is `target_id` versus `old_text`. This is a bounded AST-address interface, **not** a complete semantic language.

All edits normalize to the same line patch accepted or rejected by `compile_patch`. For a fixed file snapshot, target IDs and exact preimages are unique over the prospectively constructed target universe. Therefore the encodings are bijective on that universe and every corresponding edit yields the same compiler decision. This does not imply model success, issue resolution, or general semantic superiority.

Local validation: **14 regression/transport tests passed**, including stubbed transport tests explicitly not counted as model inference. In **5,000 deterministic matched multi-file compiler cases**, 1,000 were accepted and 4,000 rejected in each arm, with **zero verifier disagreements**. These are synthetic compiler tests, not real-repository model outcomes.

The prospective real-issue pilot uses two discovery-only tasks from the eight-repository Run201 freeze: `gtalarico__pyairtable-431` and `wntrblm__nox-933`, each at its frozen base commit. Four positive-control completions must succeed before a real issue is attempted. Planned model: Qwen2.5-Coder-7B-Instruct Q4_K_M, pinned SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, temperature zero, 1,536 output tokens, common per-issue seed. Raw prompts, completions, usage, failures and verifier traces must be retained.

Primary outcome: **patch-compiler acceptance, not SWE-bench issue resolution**. The 480-task/196-repository powered study remains outstanding. The previously modeled ~81% power applies only to a large hypothetical effect; two pilot tasks cannot support a statistical superiority claim.

**Frozen mechanism prediction:** Any advantage from structural IDs should grow with the length of exact text that the Python baseline must copy, and attenuate when Python-first context also uses IDs. On a separately held-out unseen repository condition with uniquely addressable preimages longer than 400 characters, the structural-ID arm should have fewer invalid-address/truncated responses. This prediction is not tested in the pilot.

Limitations: the same bounded AST target universe is enforced in both arms, so neither represents arbitrary Python edits. Target selection is lexical and may miss relevant repair files. Independent functional issue evaluation and cluster-aware uncertainty are required before any scientific superiority claim. All 89 boundary issues remain reserved.

Full source, executable parity stress, 5,000 raw records, prospective freeze, tests and the proposed cloud workflow are preserved in the Run202 local reproducibility archive.