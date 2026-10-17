# Run 76 evaluator audit and blocker

- Existing default CI `pyproject.toml` declares `testpaths = ["tests"]`. Five independent-oracle tests under `research/run62/test_oracle.py` are not discovered by the default invocation. CI success therefore does not establish that those five fault-injection tests passed.
- The attempt to update `pyproject.toml` on `build/run76-oracle-ci-repair-20261017` was blocked by GitHub connector safety checks.
- The attempt to add `tests/test_run76_independent_oracle_gate.py` was also blocked. The branch and this evidence are preserved; no code integration is claimed.
- Eight development-only repair contracts were checked exhaustively on 128 Boolean inputs with 15 intended authorized changes. Sixteen paired prompts share identical semantic context. No capable model was run.
- Control-parser hazard caught before inference: `parse_python_patch` expects unquoted Boolean AST values such as `{'read': a and b}`; a quoted value `{'read': 'a and b'}` becomes a string constant and is rejected. The local prompt generator was corrected before any model outputs were obtained.
- Local evaluator tests: 5/5 passed. These are protocol/manifest tests, not production integration tests.
- No claim of representation superiority or repository-level repair improvement. Strongest current alternative remains shared verifier/semantic context rather than IR.
- Next: restore code-write path, ensure independent-oracle CI collection, run both arms with the same compiler, capable model, tokenizer-matched prompts, raw transcripts and an unseen independent evaluation.
