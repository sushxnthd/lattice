# K-SYNTH-1 Run367: exact historical HTTPcore #1000 replay

Date: 2026-10-30 UTC. Canonical branch: `research/exp003-context-order`. Sole PR #9 must remain draft and unmerged. All 89 reserved boundary issues remain SEALED.

## Immutable prospective contract

Execute the **unchanged** Run366 oracle `run366_historical_oracle.py`, SHA-256 `1889d4e0b71610018b94fa87084199de280323cedf3133eeac7588025ff30797`, on complete historical HTTPcore source trees, not the installed 1.0.9 reconstruction. It contains eight target cases and ten controls per backend, including the previously failed `busy_idle_closed` control. Do not change cases, thresholds or classifications after outcomes.

Upstream base: `5974b03c7df89d3ee4e23779900d5349d550753c`; PR #1000 head: `7fb20526175e2300185ce2b472a97acca95b2525`. Historical Git blob IDs:

| Source | Base | Head |
| --- | --- | --- |
| `httpcore/_sync/connection_pool.py` | `9ccfa53e597a29ee387f9d16f3af4f695ac0d33a` | `4b26f9c63032be5c6c932b9d1339c43d4029368e` |
| `httpcore/_async/connection_pool.py` | `96e973d0ce223f6bed9be9e6a6a2f3c01622c611` | `5ef74e6497f1fe44b7be520f8e1502e8786e91fd` |

The new GitHub workflow clones the exact upstream history, verifies source blobs, constructs four combinations, and executes each in a no-network, read-only, unprivileged, resource-limited Python 3.11 container with pinned `h11==0.16.0` and `certifi==2025.1.31`. Retain original stdout, stderr, exit codes, source hashes, raw outcomes, independent audit and SHA manifest. Pre-oracle errors are NOT semantic repair failures.

## Qualification rule

Independent auditor verifies all 144 rows, 36 unique case IDs per variant, frozen oracle digest, original source Git blobs, expected/observed state transitions, summary counts and all 36 per-case factorial interactions. A positive qualification requires all variants to execute, all baseline controls to pass, all full-reference targets and controls to pass, and both single-file variants to fail at least one frozen requirement. If the baseline retains the two prior control failures, qualification is FAIL. No retuning or retroactive promotion.

## Completed local preflight

Eight adversarial independent-auditor tests passed. The auditor replayed the existing Run366 **modern-package source-normalized proxy**, finding 144/144 rows auditable, zero interaction on all 36 individual cases, baseline control contamination and a FAIL qualification. This is **not** a new historical result and is **not** Qwen inference.

The exact historical workflow is a new, separately labelled run. Its results remain pending until original GitHub Actions evidence is recovered and independently SHA-verified.

## Interpretation and priorities

Even a successful exact historical replay does not establish a new independently selected benchmark task or semantic-IR superiority. HTTPcore #1000 repairs mirrored sync/async backends. The primary gap remains prospectively frozen, reference-blind, independent multi-production-file issues and a matched strong open-model comparison against information-equivalent ordinary Python/AST actions with identical source facts, edit authority, atomic compiler, isolated oracle, and tokenizer-measured budgets. The cohort remains eight qualified PRs across seven repositories; no breakthrough claim.
