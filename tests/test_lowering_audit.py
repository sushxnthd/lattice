from lattice.lowering_audit import audit_framed_lowering


def test_public_api_exists():
    assert callable(audit_framed_lowering)
