# K-SYNTH-1 Run353 — fail-closed two-file atomic literal-default compiler

**Classification:** New executable production-source editor and independent static/binding audit. Not a new qualified PR, model inference, production runtime repair, or representation advantage.

## Provenance and method

The original Run351/352 HTTPX paired Qwen pilot accepted four actions per arm but only one action actually changed source. Both models patched `httpx/_api.py::head`, leaving `Client.head` and `AsyncClient.head` untouched. Run353 builds a shared atomic multi-source transaction compiler rather than treating accepted actions as successful repairs.

Historical pre-fix HTTPX issue #1146 baseline commit: `891d865044d27c229278f0fa20d84ba4007cb289`. Pinned SHA-256: `httpx/_api.py` = `bd646bd7bfddd75eba6687bef45b52f5c9e1b7634d680fbcbfaf16304b618f5d`; `httpx/_client.py` = `6b223a7a32afcbaf4e1a9a83f6d34caf8f66a31d740a1ac511df678463ecd8a2`.

The compiler accepts only frozen allowlisted function-parameter default slots with exact source SHA, AST-expression anchor SHA, typed expected-value preconditions, literal-only replacements, duplicate-target rejection and whole-tree syntax validation. All edits validate before any staging directory is published. Model-authored code is never executed on the host. Stage publication assumes one writer and same-filesystem rename.

## Results

A manually specified **post-outcome diagnostic** changed three HEAD `allow_redirects` defaults from `False` to `True` across the two historical production source files. Independent AST reconstruction confirmed **3 effective edits, 0 no-ops**, with **18/18 independently checked signature-binding observations** (omitted, explicit False, explicit True for each function before/after). **14/14 local tests passed**, including 512 seeded Unicode/literal property cases; **10/10 adversarial evidence mutations rejected**.

**Negative diagnostic:** all three edits leave an adjacent historical comment claiming that HEAD differs from the usual default. The compiler records three `ADJACENT_DEFAULT_COMMENT` review obligations. Syntax validity is not documentation consistency.

These 18 observations are AST/signature-binding simulations, **not execution of historical HTTPX or a redirect oracle**. This narrow literal-default editor is not a general statement editor and has not yet been integrated into matched coding-model inference. The manually authored transaction is not model success. The cohort remains 8 historically qualified PRs across 7 repositories. Run351/352 remains equal and incomplete (1/3 targets, 6/6 controls per arm). No superiority or breakthrough is claimed. All 89 reserved boundary issues remain sealed.

The full 14-payload SHA-verified reproducibility archive is preserved locally; GitHub mirroring of all raw payloads remains incomplete.

## Independent GitHub Actions execution

[Run353 source-editor smoke](https://github.com/sushxnthd/lattice/actions/runs/40982313747) completed SUCCESS on 2026-10-30 UTC. It cloned and SHA-verified the pinned historical HTTPX source, ran the committed compiler and preserved the complete source stage. Original Actions artifact ID `12945312294`, ZIP SHA-256 `9cb913cec5169a108ef877446fa36b62120084b6427d4447d25ec3fed4d96ee0`, independently downloaded and verified against GitHub's artifact digest. All 7/7 inner manifest entries passed SHA-256. Cloud and independent local actions, authority and staged source SHAs matched exactly: `_api.py` `81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe`; `_client.py` `97f9ba016b14033c347a398444662e795e02e0118729d67ecbfbfa0192a0bd60`. This verifies compiler behavior, not a model-generated repair or isolated HTTP redirect runtime oracle.
