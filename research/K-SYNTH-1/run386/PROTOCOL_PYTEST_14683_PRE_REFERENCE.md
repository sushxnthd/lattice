# K-SYNTH-1 Run386 candidate freeze: pytest #14683

**Freeze status:** Before inspecting any reference patch/diff for PR #14694. The issue text, PR title and its short public search snippet were already seen, so this is **not fully investigator-blind**. Do not label it genuinely unseen. No original heldout/sealed boundary issue is accessed.

* Candidate: https://github.com/pytest-dev/pytest/issues/14683, reported regression in pytest 9.1.x; historical base tag `9.1.1`.
* Pre-fix source file hashes (Git blob SHA-1, retrieved by read-only GitHub API at `9.1.1`): `src/_pytest/main.py` `c4df4e46983447614e3bf6ae860132b378562887`; `src/_pytest/fixtures.py` `f4ca2eac4556b7f2081602451f7309530556f611`.
* Expected issue behavior: an autouse rootdir conftest fixture injecting a name through `doctest_namespace` should be available when collecting a doctest outside rootdir with explicit `--rootdir`.
* Public target A: rootdir `r/`, fixture in `r/conftest.py` sets `doctest_namespace['answer']=42`; doctest in sibling `outside/doc.txt` contains `>>> answer` / `42`; invoke `pytest --rootdir=r --doctest-glob='*.txt' outside/doc.txt` from project parent; expected 1 pass.
* Public target B: same but fixture injects `answer=17` and doctest expects 17; expected 1 pass. This is a metamorphic value change, not a new bug family.
* Heldout target C: use two names `answer` and `extra` injected by the same fixture; doctest outside rootdir accesses both; expected pass.
* Heldout target D: place outside doctest one directory deeper; expected pass if the same rootdir fixture policy applies.
* Nonregression controls: doctest within rootdir; ordinary doctest without injected variables; direct fixture usage in an in-root Python test; ordinary Python test outside rootdir with local fixture; collection of two independent doctests; no accidental autouse application to unrelated tests.
* Candidate qualification requires baseline failing A and B, complete historical reference passing A-D and all six controls, and **two independently edited production source files** with both source components necessary to satisfy the combined target-plus-control oracle. Baseline and each component-only arm must be run in an isolated historical environment; no fabricated partial reference edits. Per-case 2x2 interactions are recorded, not assumed.
* If only one production source changes, if baseline cannot reproduce, if oracle depends on undocumented behavior, or if reference fails controls: record as **NOT QUALIFIED**, no retuning or promotion.
* Model inference is forbidden until the historical base and oracle are independently qualified. Do not reuse the 89 reserved boundary issues. All model completions require shared AST-span editor and isolated execution.

This freeze does not assert the tests have been executed. It is a prospective candidate protocol, not a qualified production-repair observation.
