# Lattice K-SYNTH-1 Run255 — independently audited capable-model failures and real two-source ablation launch

Date: 2026-10-26 (IST). Branch: `research/exp003-context-order`. Draft PR #9.

## Genuine inference recovered

Recovered completed GitHub Actions [run 40232048444](https://github.com/sushxnthd/lattice/actions/runs/40232048444), artifact ID 12614796697, artifact SHA-256 `4703e8d40d9fffcb5108f50ac05232535ad186ab284839f0a5f1bc1bc60bec7e`. This is the earlier Run254 workflow revision at `eee76d986a04742bb380c45277c1fe40eaa6b8ac`. Independent auditor reverified exact four requests against the **prospectively frozen Run254 archive**, source and fact parity, request/prompt hashes, pinned model SHA, seeds, tokenizer usage, raw response text, strict compiler outcomes and public/held-out oracle traces. Auditor does not import the original runner.

| Issue | Representation | Prompt tokens | Completion | Compiler | Public/heldout |
|---|---|---:|---:|---|---|
| humanize #206 | semantic JSON facts | 7,876 | 45 | REJECTED | Not run |
| humanize #206 | Python-comment facts | 7,878 | 45 | REJECTED | Not run |
| packaging #1411 | semantic JSON facts | 11,949 | 164 | ACCEPTED | FAIL / FAIL |
| packaging #1411 | Python-comment facts | 11,951 | 176 | ACCEPTED | FAIL / FAIL |

**0/4 functional repairs, 0/2 paired wins, 0 discordant pairs.** These are two real *single-production-file* repair tasks, not a powered multi-source-edit benchmark. This is a fact-ENCODING comparison (identical source and CFG facts), **not** semantic-IR editor superiority or a valid null-equivalence finding.

Independent failure witnesses: humanize completions are byte-identical and incorrectly terminate `REPLACE_BEGIN` with `SEARCH_END`, so the strict compiler rejects them. Both packaging completions introduce recursive `resolve_dependency_groups` self-calls; both public and held-out oracles raise `RecursionError`. No posthoc output normalization is scored. `run254_summary.json` contains stale `inference_started:false`; raw responses and actual evaluator traces are authoritative.

The later final Run254 [run 40232108742](https://github.com/sushxnthd/lattice/actions/runs/40232108742) was still executing inference when inspected; repeated runs on the same two issues must never be counted as independent observations.

## Genuine two-production-file candidate

Verified Flask PR #6096: reference merge `05e9c6bd630ecf4ec0ec884b1fc7901663737bc7`, first parent `514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b`. The patch changes both `src/flask/app.py` and `src/flask/testing.py`.

Committed and launched [Run255 Flask source-ablation workflow](https://github.com/sushxnthd/lattice/actions/runs/40236090884), commit `a50c92d10d7a98709492aa05bb0262f1c83f6b7c`. It executes pinned upstream source with identical dependencies and read-only public IPv6 server, withheld IPv6 session, and IPv4 nonregression oracles against baseline, app-only, testing-only and reference variants. It records source/test/dependency hashes, complete subprocess stdout/stderr, exit codes and timings. Qualification requires the two single-file ablations to each fix only its respective oracle and full reference to fix both. **Run was queued at last inspection; no functional qualification claimed yet.**

## Reproducibility and limitations

Local complete 46-file SHA-256-verified archive: `/mnt/data/lattice_run255/lattice_run255_real_model_audit_and_flask_qualification.zip`; archive SHA-256 `9104ee069e441d3aae33e47ea1b7f55ea0f43460ad148a5d384c351850c06b1f`. Includes exact raw completions, response JSON, frozen requests, upstream source snapshots, evaluator traces, independent auditor, and protocol. Complete archive remains local, not fully mirrored to GitHub. Draft PR #9 remains open/draft; 89 sealed issues untouched.

**Next:** independently audit Flask ablation and final Run254 artifact, then qualify further real two-source-edit issues and freeze an adequately powered *semantic-IR versus ordinary Python* study with identical task information, edit authority, compiler, verifier and held-out oracles. Previously hypothetical power targets: 306 optimistic independent pairs, 681 moderate pairs, potentially 400–800+ clustered issues. No representation breakthrough or statistical significance claimed.
