# Pytest #14683: predeclared production-candidate screening failure

Original issue: https://github.com/pytest-dev/pytest/issues/14683

Frozen before inspecting reference diff: `PROTOCOL_PYTEST_14683_PRE_REFERENCE.md` committed `1e527ee3c323db12a9d22577c60b8192aea6e772`. Issue/PR title snippets were previously seen, so the candidate was not fully investigator-blind.

Subsequently requested complete changed filenames for https://github.com/pytest-dev/pytest/pull/14694:

- `changelog/14683.bugfix.rst`
- `src/_pytest/fixtures.py`
- `testing/test_conftest.py`
- `testing/test_doctest.py`

Exactly **one** production source changed. The predeclared minimum of two independently changed production sources fails. Disposition: **NOT QUALIFIED**. No baseline or factorial run was performed and no source-component necessity or target success is claimed. No retuning or promotion.

The frozen historical tag was pytest `9.1.1`; original Git blob SHAs: `src/_pytest/main.py` `c4df4e46983447614e3bf6ae860132b378562887` and `src/_pytest/fixtures.py` `f4ca2eac4556b7f2081602451f7309530556f611`.
