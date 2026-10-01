from lattice.checker import check_change


SPEC = {
    "commitments": [{"id": "private_by_default", "protected": True}],
    "state_machines": {
        "Document": {
            "states": ["draft", "published"],
            "transitions": [["draft", "published"]],
        }
    },
    "permissions": [
        {"role": "owner", "action": "read", "resource": "document"},
        {"role": "owner", "action": "write", "resource": "document"},
    ],
    "protected_dependencies": [["publish", "authorization"]],
    "invariants": [
        {"id": "nonnegative_revision", "path": "document.revision", "op": ">=", "value": 0}
    ],
}


def test_accepts_semantically_valid_change():
    proposal = {
        "transitions": [{"machine": "Document", "from": "draft", "to": "published"}],
        "state": {"document": {"revision": 2}},
    }
    assert check_change(SPEC, proposal) == {"ok": True, "violations": []}


def test_rejects_protected_commitment_removal():
    result = check_change(
        SPEC,
        {"drop_commitments": ["private_by_default"], "state": {"document": {"revision": 0}}},
    )
    assert not result["ok"]
    assert any(v["code"] == "protected_commitment_removed" for v in result["violations"])


def test_rejects_illegal_transition_and_permission_broadening():
    result = check_change(
        SPEC,
        {
            "transitions": [{"machine": "Document", "from": "published", "to": "draft"}],
            "add_permissions": [
                {"role": "viewer", "action": "write", "resource": "document"}
            ],
            "state": {"document": {"revision": 1}},
        },
    )
    codes = {v["code"] for v in result["violations"]}
    assert {"illegal_state_transition", "permission_broadening"} <= codes


def test_rejects_dependency_removal_and_invariant_failure():
    result = check_change(
        SPEC,
        {
            "remove_dependencies": [["publish", "authorization"]],
            "state": {"document": {"revision": -1}},
        },
    )
    codes = {v["code"] for v in result["violations"]}
    assert {"protected_dependency_removed", "invariant_failed"} <= codes
