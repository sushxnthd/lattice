# Run 73: independent oracle CI-discovery audit (2026-10-17)

SCIENCE: No coding-model generation or representation comparison was performed. The active kernel remains semantic-IR repair complexity versus ordinary Python with identical verifier/compiler, information and decoding. Status: UNTESTED.

SYSTEM: Default pytest configuration uses testpaths = ["tests"]. Five independent oracle tests exist in research/run62/test_oracle.py but are not collected by default. The intended adapter tests/test_run73_oracle_ci.py would import those five tests for discovery. Attempt to write that adapter on build/run73-oracle-ci-discovery-20261017 was blocked by GitHub connector safety checks; no code was committed.

Strongest alternative explanation: the existing tests may pass locally but fail when discovered in CI. Next discriminating action: run pytest explicitly against research/run62/test_oracle.py and, if integration write becomes possible, compare CI test collection and fault-injection results. This is evaluator capability work only, not evidence that semantic IR helps a coding model.

Frozen holdouts: untouched. Model calls: none. Smallest supported claim: five tests are outside default testpaths and repository code-write integration was rejected.
