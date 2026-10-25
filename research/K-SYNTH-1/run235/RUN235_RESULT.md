# Lattice Run235: independent symbol-preservation counterexample

Date: 2026-10-25. Independent read-only audit of the first completed Run234 Qwen2.5-Coder-7B-Instruct issue. The original frozen compiler/verifier and primary endpoint are unchanged.

## Original model evidence

Cloud run [40148667367](https://github.com/sushxnthd/lattice/actions/runs/40148667367), job 121035374896, artifact 12581389142, task `bluesky__bluesky-1850`, pinned base commit `92d2633127e33e51aa1d1b109c80503e74bbe0e0`. Independently verified the artifact's 20 files against its SHA-256 manifest (`0a0da6391a628751543ddac697c4f73c5194f6b586873cf2c0de2b8a2358c505`) and checked prompts, model ID, seed, token usage, source facts and original verifier records.

| Frozen measurement | Annotated Python | Semantic-node JSON |
| --- | ---: | ---: |
| Prompt tokens | 6,772 | 6,393 |
| Completion tokens | 323 | 325 |
| Compiler accepted | yes | yes |
| Git patch applies | yes | yes |
| Python AST parses | yes | yes |
| Top-level `wait` declaration survives | **no** | **no** |
| Dangling `_wait = wait` alias | yes | yes |
| Functional issue resolution | **not evaluated** | **not evaluated** |

Both genuine model outputs selected the entire top-level `@plan def wait(...)` AST target (selector `bc0e21ba406fb2c8d429e944`) but replaced it with **only an indented docstring and return statement**, deleting the decorator and function declaration. The replacement text became unreachable statements inside the preceding `sleep` function. Consequently, `ast.parse` and `git apply --check` succeeded, but the resulting module has no `wait` declaration and retains `_wait = wait` at line 648. Independently executing the isolated alias AST raises `NameError`. Neither condition produced a correct repair.

## Mechanism and prospective correction

This is an executable counterexample to the proposition that syntax validity plus patch applicability guarantees API binding preservation. A `replace` targeting a `FunctionDef`, `AsyncFunctionDef`, or `ClassDef` should, by default, preserve the named declaration and its structural scope; explicit rename/delete operations need separately verified authority. This **necessary**, not sufficient, safety condition should be added to a *prospective* common verifier for both arms. Do **not** retroactively change Run234 scores.

Construct validity also matters: the annotated-Python arm contains JSON-serialized `AST_TARGET` records, so the current study compares two presentations of bounded AST-target facts, **not** an unrestricted ordinary-Python editing workflow. One issue cannot establish a general representation advantage or parity.

Seven new local unit tests passed, including real artifact integrity, explicit alias runtime failure, synthetic positive control, nested-method preservation, rename rejection and tamper detection. Full original model outputs, exact requests, independent auditor, tests and SHA-256 manifest are preserved in the Run235 local reproducibility archive. The 89 reserved boundary issues remain untouched.

**Next:** Audit the other 11 Run234 jobs as their artifacts become available, distinguish compiler acceptance from functional resolution, and freeze a prospective declaration-preservation and functional-verifier gate for both representations. Lattice remains unfinished.

## Independent replication on a second repository

During this run, job 121035374958 also completed. Downloaded artifact 12582279840 for `benchopt__benchopt-697` (base commit `ffd91c081ad72c8b949564bbddf8687569d2a64b`) and verified all 20 files against SHA-256 manifest `8707f53fbbd2498bdfbbb96f9983c21968a4033ed306c5116e2039a7868b9598`.

Both genuine model arms again passed transactional compilation, Python syntax checks, and `git apply --check` while deleting the class method `Objective.evaluate_result`. Each replaced the entire method declaration with a body-only `raise TypeError(...)` statement, leaving that statement unreachable inside the preceding `get_one_result` method. Neither edit is a valid repair.

| Benchopt measurement | Annotated Python | Semantic-node JSON |
| --- | ---: | ---: |
| Prompt tokens | 8,681 | 8,176 |
| Completion tokens | 173 | 160 |
| Compiler accepted / syntax valid | yes / yes | yes / yes |
| `Objective.evaluate_result` preserved | **no** | **no** |
| Functional resolution | not evaluated | not evaluated |

**Combined observed result:** Across the first two completed, independent repository issues and four genuine model outputs, compiler acceptance was **4/4** but targeted declaration preservation was **0/4**. This is an exploratory diagnostic, not a population reliability estimate. It suggests a systematic mismatch between the model's body-only replacement and the compiler's whole-AST-node replacement semantics, shared by both presentations. The independent local test suite now passes **eight** tests. Remaining cloud jobs are still pending. The original frozen primary endpoint remains unchanged.
