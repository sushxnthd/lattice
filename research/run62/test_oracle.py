"""Run62 independent oracle tests."""

def test_import():
    from research.run62.independent_oracle import OracleError
    assert issubclass(OracleError, ValueError)
