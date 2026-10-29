# K-SYNTH-1 Run329: HTTPX default-argument repair and security counterexample

2026-10-29 UTC. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, one draft/unmerged PR #9; all 89 reserved issues sealed.

## Prospective order
Frozen protocol commit `c3a0b308c143f4151b23d4a7b05687be33ad7464` preceded primary execution. The original shared Python AST-action compiler supports SHA-preconditioned, authorized, atomic argument-default edits across sync and async functions with whole-module AST congruence and byte preservation outside edited spans. The exact reference AST change in already-qualified HTTPX PR1183 (three `allow_redirects=False` defaults across `_api.py` and `_client.py`) is not expressible by Run324's `If/IfExp.test`-only editor. Other possible repairs under that earlier grammar are not ruled out.

## Original local primary
256/256 correlated synthetic two-file, three-default transactions compiled and returned the expected values. 128/128 malformed/stale/unauthorized transactions rejected with inputs unchanged. An independent read-only auditor reconstructed all 256 patches, checked AST deltas and independently replayed **1,536** trusted CPython function observations (768 default and 768 explicit-false controls) in separate subprocesses with zero discrepancies. These are **not independent real repairs or model completions**.

## Original real HTTPX cloud reproduction
[GitHub Actions run 40801376816](https://github.com/sushxnthd/lattice/actions/runs/40801376816) completed success. Original artifact ID `12865847895`, ZIP SHA256 `bab8e11897c886a55de89074413910ee057d0a3aa2269f7fa687278f9a4c6e2b`; all six manifest entries independently verified. Frozen Run328 oracle SHA256 `51cefba11ede1692bf543500f410fcf3406f95705f6b5876af886893574394f7`, exact historical baseline `891d865044d27c229278f0fa20d84ba4007cb289`.

| Configuration | Targets | Controls |
|---|---:|---:|
| Historical baseline | 0/3 | 6/6 |
| Trusted reference-informed 3-action AST-default patch | 3/3 | 6/6 |

An independent read-only audit checked all 18 original functional records with zero discrepancies. Patched source SHA256: `httpx/_api.py` = `81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe`; `httpx/_client.py` = `97f9ba016b14033c347a398444662e795e02e0118729d67ecbfbfa0192a0bd60`. Trailing source comments are preserved, so the patch is not byte-identical to the historical reference. This is **trusted reference expressibility**, not model-generated repair, a new issue, or full package correctness.

Reproduction: [SHA-pinned code archive](run329_real_code.tar.zlib.b64) (Git blob `481d4b023769ded2da2c5d459641fc8ced437612`), [workflow](../../../.github/workflows/lattice-k-synth-1-run329-httpx.yml). Local full source, raw synthetic traces, independent auditors and original cloud ZIP are retained in a SHA-verified reproducibility archive.

## Postfreeze security flaw (original scores unchanged)
The original generic editor **accepted executable default expressions** such as `__import__('os').system('echo NEVER_RUN')` because AST congruence checks structural intent, not side-effect safety. Python evaluates function defaults during import. No hostile payload was executed. A separately labelled **postfreeze** boolean-literal guard was added: [source](run329_postfreeze_boolean_guard.py). In a separate security audit, original compiler accepted **64/64** hostile expressions; corrected guard rejected **64/64**, accepted **64/64** benign boolean controls and reproduced **256/256** original safe patches byte-identically. The guard is mandatory for future untrusted model output in this scoped default-edit operation; general Python execution still requires isolation.

## Decision
Three previously qualified independent historical issues remain: Flask PR6096, urllib3 PR5071 and HTTPX PR1183. **Zero new capable-model completions; no powered IR advantage or breakthrough.** The frozen Run328 oracle and 89 sealed boundary issues remain untouched. Historical artifact mirroring remains incomplete.

**Run330:** freeze and execute genuinely paired, positive-control-gated Qwen2.5-Coder-7B inference across the three qualified issues with pre-fix issue facts, source-provenance-backed bounded MAY/UNKNOWN facts, information-equivalent ordinary Python/AST baseline, shared safe compiler, isolated oracle and complete raw traces. Three issues remain feasibility only.
