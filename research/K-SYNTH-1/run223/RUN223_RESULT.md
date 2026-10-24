# K-SYNTH-1 Run223 — Independent Run222 behavioral audit (2026-10-24)

Recovered **all three completed Run222 GitHub Actions artifacts**, covering Robocop #1329, PyBaMM #3795, and Cloud SQL Connector #1201. Independently audited **six raw Qwen2.5-Coder-7B-Instruct Q4_K_M completions** against exact prompts, seeds, usage counts, source-fact hashes, compiler traces and model identifiers. All three original cloud jobs completed successfully. No repeated inference or duplicate workflow runs were counted as independent replication.

| Issue | Semantic-node JSON compiler | Annotated Python compiler | Independent finding |
|---|---|---|---|
| Robocop #1329 | rejected | rejected | Three same-file deletion proposals plus a no-op replacement versus eight file deletions. Neither changes the project-check sorting path. Structural negative only. |
| PyBaMM #3795 | accepted | accepted | **Both fail independently executed necessary-condition tests.** |
| Cloud SQL Connector #1201 | rejected | rejected | Both propose deleting five connector/test files instead of implementing HTTP response-body error handling. Structural negative only. |

Compiler acceptance: **1/3 in each arm**. Complete issue resolution: **NOT_EVALUATED**; no verified successful repairs. The exact paired McNemar p-value is 1 and is uninformative at this size.

## PyBaMM executable counterexample

The issue requires `Simulation.create_gif` and `BatchStudy.create_gif` to check for unsolved instances **before** plotting. The independent CPython witness extracts the exact original method bodies from the frozen model prompts, applies each actual raw model replacement where present, and executes solved/unsolved cases using a recording `pybamm.QuickPlot` stub. It does not import Lattice's compiler.

* **Semantic arm:** Both patched methods call `QuickPlot.create_gif` **before** checking for a solution. Unsolved instances produce one GIF side effect before raising `ValueError`; solved instances generate two GIFs. **0/4 necessary-condition cases pass.**
* **Python arm:** Both proposed edits change only `.rst` documentation, leaving the Python methods unchanged. Unsolved instances generate GIFs without raising. **2/4 necessary-condition cases pass.**

These are executable necessary-condition failures, not a full PyBaMM package test. The representations induced different edit localization (code versus documentation), but neither produced a functional repair.

## Robocop and Cloud SQL structural counterexamples

Robocop: the semantic completion proposes three deletions of `src/robocop/linter/rules/__init__.py` and an identical-content replacement; the Python completion proposes deleting eight documentation/rules files. Both fail shared compiler validation and neither changes the requested sorting logic.

Cloud SQL: **both** completions propose five deletions, targeting connector initialization, asyncpg, client, refresh-utils, and its test. Each response contains exactly **656 completion tokens**, with near-identical action structure across source presentations. The shared compiler rejects both. No aiohttp behavior was executed; this is a structural negative and a possible model/protocol collapse, not a proven causal mechanism. The destructive edits were **never applied**.

## Reproducibility and interpretation

The complete local Run223 archive preserves all three unmodified original workflow artifact ZIPs, an independent standard-library evaluator, **seven passing tests**, raw prompts and model outputs, executable CPython traces, and SHA-256 manifest. Artifact SHA-256 values:
* Robocop: `2db2cbbab20a7d233db24d9fabd873ad602c4e166aae7d1dab3b58c442beff5d`
* PyBaMM: `182b8d97cc43c8a45d7857b13349c9af8df2ee830d4a6f63f469e6a96b0e8531`
* Cloud SQL: recorded in `RUN223_AUDIT.json`

Reproduce with `python -m unittest -v test_run223_independent_audit.py` and `python run223_independent_audit.py run222_issue2.zip run222_issue6.zip run222_issue7.zip --output RUN223_AUDIT.json`.

**Scientific conclusion:** Compiler acceptance cannot substitute for functional issue resolution. The existing comparison changes *source presentation under a common edit grammar*; it does not establish intrinsic semantic-IR editing-language superiority. The assumed ~686-pair power target should not be scaled before independent functional oracles and stronger realistic positive controls. Maintain the existing branch and draft PR #9; no representation breakthrough is claimed.
