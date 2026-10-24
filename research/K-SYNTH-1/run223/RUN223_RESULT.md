# K-SYNTH-1 Run223 — Independent Run222 behavioral audit (2026-10-24)

Recovered two original completed Run222 Qwen2.5-Coder-7B-Instruct Q4_K_M artifacts, covering Robocop #1329 and PyBaMM #3795. Audited **four raw completions** against exact prompts, seeds, usage counts, source-fact hashes and compiler records. The third Cloud SQL issue was still running at inspection and is excluded. No repeated inference was counted as independent replication.

| Issue | Semantic-node JSON compiler | Annotated Python compiler | Independent finding |
|---|---|---|---|
| Robocop #1329 | rejected | rejected | Semantic arm proposed three same-file deletions and a no-op replacement; Python arm proposed eight file deletions. Neither modified the requested project-check sorting path. Structural evidence only. |
| PyBaMM #3795 | accepted | accepted | **Both failed independent executable necessary-condition tests.** |

For the two completed pairs, compiler acceptance was **1/2 in each arm**. No full issue resolution was verified. The exact paired McNemar p-value is 1, uninformative at this size.

## PyBaMM behavioral counterexample

The issue requires `Simulation.create_gif` and `BatchStudy.create_gif` to check for an unsolved instance **before** plotting. An independent CPython witness extracts the actual method bodies from the frozen model prompts, applies each raw model-proposed replacement, and executes solved and unsolved states using a recording `pybamm.QuickPlot` stub. The witness does not import Lattice's compiler.

* **Semantic arm:** Both patched methods call `QuickPlot.create_gif` **before** checking for a solution. Unsolved states produce one GIF side effect before raising `ValueError`; solved states generate two GIFs. **0/4 necessary-condition cases pass.**
* **Python arm:** Both proposed edits change only `.rst` documentation; the two Python methods remain unchanged. Unsolved states still generate GIFs without raising. **2/4 necessary-condition cases pass.**

These are executable necessary-condition failures, not a full PyBaMM suite. The two source presentations produced different edit localization (code vs documentation) but **neither repaired the bug**.

## Robocop structural counterexample

The semantic completion proposed three deletions of `src/robocop/linter/rules/__init__.py`, plus a replacement whose old and new contents match. The Python completion proposed deleting eight documentation/rules files. Neither modified project-check sorting. The shared compiler rejected both. No full Robocop runtime test is claimed.

## Reproducibility and interpretation

The local Run223 archive preserves both unmodified original GitHub Actions artifact ZIPs (SHA-256 `2db2cbbab20a7d233db24d9fabd873ad602c4e166aae7d1dab3b58c442beff5d` and `182b8d97cc43c8a45d7857b13349c9af8df2ee830d4a6f63f469e6a96b0e8531`), the independent standard-library evaluator, six passing tests, JSON behavioral traces, and SHA-256 manifest.

Run `python -m unittest -v test_run223_independent_audit.py`, then `python run223_independent_audit.py run222_issue2.zip run222_issue6.zip --output RUN223_AUDIT.json`.

**Scientific conclusion:** Compiler acceptance is not a functional repair endpoint. This study still compares *presentations under a common edit grammar*, not intrinsic semantic-operation versus Python-language superiority. No representation advantage is established. The ~686-pair target is assumption-dependent and should not be scaled without valid functional oracles and strong positive controls. Retrieve and independently audit the remaining Cloud SQL artifact when available; maintain the existing research branch and draft PR #9.
