"""Make the five existing Run62 independent-oracle fault-injection tests part of default CI.

The canonical pytest configuration discovers tests/ only. These wrappers execute
the original tests unchanged against the production framed compiler, not stand-ins.
This is a verifier integration gate, not representation-science evidence.
"""
import pytest
from research.run62 import test_oracle as run62

CASES = (
    "test_valid_edit_and_protected_frame",
    "test_independent_oracle_detects_protected_change",
    "test_independent_oracle_detects_production_corruption",
    "test_independent_oracle_detects_lowering_corruption",
    "test_independent_oracle_fails_closed_on_bound",
)

@pytest.mark.parametrize("case", CASES)
def test_production_independent_oracle_gate(case):
    getattr(run62, case)()
