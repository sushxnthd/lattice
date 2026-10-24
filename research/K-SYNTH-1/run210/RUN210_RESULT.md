# K-SYNTH-1 Run210 — bounded-context capable-model experiment

**2026-10-24.** Persistent branch: `research/exp003-context-order`. This is a preregistered feasibility pilot, not a powered functional representation-science study.

## Independent audit of completed Run209

Recovered GitHub Actions run `40044994418`, artifacts `12541968066` and `12541317076`. Replayed the six Qwen2.5-Coder-7B-Instruct Q4_K_M controls and six real-issue outputs against the frozen compiler.

| Measure | Result |
| --- | ---: |
| Positive controls accepted | 6/6 |
| Real-issue edits accepted | 0/6 |
| Real-issue no-op transactions | 2 |
| Truncated responses | 1 |
| HTTP 400 context failures | 3 |
| Functional resolutions tested | 0 |

The server log identifies the three HTTP 400 failures as **18,526–18,528 input tokens against a 16,384-token context limit**. The old context serialized complete file sources and repeated target preimages: the Ragna issue used a 69,746-character prompt, including 37,411 repeated-preimage characters; the Zulip issue used 24,987 characters, including 11,493 repeated-preimage characters.

The shared retriever also rejected requested files above 8,000 bytes. Repository-wide edit *authorization* therefore did not imply that the model could actually inspect or modify those files. The two no-op completions edited an irrelevant documentation file, and the ordinary-Python completion was truncated. None of this establishes IR superiority.

## Frozen Run210 correction

Run210 retains the two discovery issues, identical model and model SHA-256, common retrieval, shared compiler, verifier, six-field JSON grammar, edit authority and source facts across all three arms. It introduces:

- Trusted full-file snapshots up to 250 KB each, with 1.2 MB total snapshot budget.
- Shared, gold-blind excerpts and up to five candidate edit targets per file.
- A 26,000-character bound on shared source/target facts and 480-character target preimages.
- Local line targets for non-Python files and support for AST targets appearing after the first 8 KB of a Python file.
- A new prospective seed prefix and immutable freeze before capable-model inference.

On **previously retrieved files only**, offline prompt sizes fell from 24,987 to 7,126 characters (71.48%) and from 69,746 to 15,655 characters (77.55%). These are *counterfactual serialization measurements*, not new model outcomes; actual Run210 retrieval may include additional files. A character cap is not a tokenizer guarantee.

Five new bounded-view tests and 29 existing tests passed locally (**34 total**). The three-arm compiler parity and exact preimage checks are also included in the cloud workflow.

## Statistical and scientific limits

The prior conditional power simulation suggested about **468 discovery issues from 187 repositories** for ~80% power under a specified large-effect model, versus 391/157 and ~73.4% modeled power in the existing discovery cohort. Actual functional discordance and repository clustering must determine final power.

Crucially, the current `semantic_node_ir` and `python_short_id` arms use identical target IDs, identical compiler semantics and the same source information. They differ in instruction framing. Their contrast **cannot** identify an intrinsic semantic-IR benefit. A genuine typed semantic representation, independent functional evaluator, matched Python baseline, mechanism ablation and sealed unseen-boundary prediction remain mandatory. No boundary tasks have been used.

## Reproduction

The Run210 runner is reconstructed by applying the immutable Run208, Run209 and Run210 compressed patches to the SHA-pinned Run207 base. The workflow verifies the frozen public dataset hash `f615b8c5f4f7e4b1996992105515b3e15e9678fb57a3cc0cff5cf1aef64641f2`, runs tests, launches the pinned open coding model and preserves prompts, raw completions, usage, seeds, verifier traces and logs. The independent Run209 audit, complete source, local traces and SHA-256 manifest are preserved in the Run210 reproducibility archive.

**Interpretation:** The result to date is a diagnosis of information-access and prompt-construction failures, not a positive or negative finding about semantic representations.
