# K-SYNTH-1 Run204: launched capable-model pilot and independent parity audit

2026-10-24 (Asia/Kolkata). Single kernel K-SYNTH-1; existing branch `research/exp003-context-order`; draft PR #9 retained.

## Executed work

- Prospective four-arm runner committed in `acccdf2913c72387a0d7912179d9614d18087b8c`.
- GitHub Actions workflow committed in `ff729debd5a5ce4e5eab29ed67a57e51f98e45d3`.
- Workflow run [40011951251](https://github.com/sushxnthd/lattice/actions/runs/40011951251) queued at last inspection. No capable-model completions or real-task outcomes claimed yet.
- Two frozen discovery issues: `gtalarico__pyairtable-431` and `wntrblm__nox-933`. The 89 boundary issues remain unseen.
- Four conditions: targets-first vs source-first crossed with short structural IDs vs exact Python-text anchors. Same issue/source/target facts, edit authority, common compiler and verifier. Qwen2.5-Coder-7B-Instruct Q4_K_M pinned by SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. Positive controls gate real tasks. Raw prompts, responses, seeds, token usage, verifier traces and failures are persisted as workflow artifacts.
- Independent local audit on six previously model-visible real Python files: **53 unique targets, 318 matched adversarial cases, 636 compiler calls, zero parity disagreements**. 53 cases accepted and 265 rejected in each address encoding. All four local positive-control encodings accepted. 18 inherited tests passed.

## Scientific interpretation

The independent audit verifies bounded compiler equivalence, not capable-model accuracy. This pilot tests structural address transport and context order; **it does not compare a full semantic IR against ordinary Python** and does not measure issue resolution. Do not claim representation superiority.

Run203 estimated only 73.4% primary power for the large hypothetical effect at 391 discovery issues / 157 repositories. Approximately 468 discovery issues / 187 repositories were suggested by the same sensitivity model for 80% power; the expansion is not yet a frozen, approved sample. The 89 held-out boundary issues must remain untouched.

## Next gate

Retrieve and independently audit actual Run204 model artifacts. If controls fail, repair and rerun without changing the held-out tasks or post-hoc scoring. Then run a properly powered, prospectively frozen genuine semantic-IR vs ordinary-Python comparison with Python short-ID ablation, functional issue evaluator, repository-cluster uncertainty, mechanism ablation, and unseen-boundary prediction.

The full local archive includes independent parity source and all 318 raw paired records.