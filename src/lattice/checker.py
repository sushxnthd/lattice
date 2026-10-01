"""Deterministic semantic preflight for Experiment 001.

The checker intentionally covers only the primitives needed to test whether
machine-checkable intent adds value beyond passive project memory and graph
context. It is not a general-purpose programming language runtime.
"""

from __future__ import annotations

import json
import operator
import sys
from pathlib import Path
from typing import Any

OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}


def _get_path(value: Any, path: str) -> tuple[bool, Any]:
    current = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def _violation(code: str, **details: Any) -> dict[str, Any]:
    return {"code": code, **details}


def check_change(spec: dict[str, Any], proposal: dict[str, Any]) -> dict[str, Any]:
    """Check a proposed semantic change against a frozen Lattice specification."""
    violations: list[dict[str, Any]] = []

    commitments = {
        item["id"]: item
        for item in spec.get("commitments", [])
        if isinstance(item, dict) and "id" in item
    }
    for commitment_id in proposal.get("drop_commitments", []):
        commitment = commitments.get(commitment_id)
        if commitment and commitment.get("protected", False):
            violations.append(
                _violation("protected_commitment_removed", id=commitment_id)
            )

    machines = spec.get("state_machines", {})
    for transition in proposal.get("transitions", []):
        machine_name = transition.get("machine")
        machine = machines.get(machine_name)
        edge = [transition.get("from"), transition.get("to")]
        legal = machine and edge in machine.get("transitions", [])
        if not legal:
            violations.append(
                _violation(
                    "illegal_state_transition",
                    machine=machine_name,
                    source=transition.get("from"),
                    target=transition.get("to"),
                )
            )

    allowed_permissions = {
        (p.get("role"), p.get("action"), p.get("resource"))
        for p in spec.get("permissions", [])
        if isinstance(p, dict)
    }
    for permission in proposal.get("add_permissions", []):
        key = (
            permission.get("role"),
            permission.get("action"),
            permission.get("resource"),
        )
        if key not in allowed_permissions:
            violations.append(
                _violation(
                    "permission_broadening",
                    role=key[0],
                    action=key[1],
                    resource=key[2],
                )
            )

    protected_dependencies = {
        tuple(edge) for edge in spec.get("protected_dependencies", [])
        if isinstance(edge, list) and len(edge) == 2
    }
    for edge in proposal.get("remove_dependencies", []):
        key = tuple(edge)
        if key in protected_dependencies:
            violations.append(
                _violation(
                    "protected_dependency_removed",
                    source=key[0],
                    target=key[1],
                )
            )

    state = proposal.get("state", {})
    for invariant in spec.get("invariants", []):
        path = invariant.get("path")
        op_name = invariant.get("op")
        expected = invariant.get("value")
        exists, actual = _get_path(state, path) if isinstance(path, str) else (False, None)
        if not exists:
            violations.append(
                _violation(
                    "invariant_value_missing",
                    id=invariant.get("id"),
                    path=path,
                )
            )
            continue
        op = OPS.get(op_name)
        if op is None or not op(actual, expected):
            violations.append(
                _violation(
                    "invariant_failed",
                    id=invariant.get("id"),
                    path=path,
                    op=op_name,
                    expected=expected,
                    actual=actual,
                )
            )

    return {"ok": not violations, "violations": violations}


def _main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: python -m lattice.checker SPEC.json PROPOSAL.json", file=sys.stderr)
        return 2

    spec = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    proposal = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    result = check_change(spec, proposal)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
