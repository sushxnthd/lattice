"""Run90: public preflight only; the target oracle is sealed until final scoring.

The model may see parser/scope/compiler acceptance but never hidden target
truth-table witnesses or the hidden target's success bit between attempts.
Both Python and IR arms call this identical preflight.
"""
from lattice.semantic_edits import Program, parse_python_patch, parse_lattice_patch
from lattice.framed_edits import FramedProgram
from research.run62.independent_oracle import audit_three_way


def public_check(task, arm, response):
    """Check only facts that would be available without the hidden target.

    Never read task['target'], and never return oracle witnesses to the model.
    """
    if arm not in ("python", "ir"):
        raise ValueError("unknown experiment arm")
    try:
        before = FramedProgram.from_program(
            Program(tuple(task["inputs"]), tuple(task["rules"].items()))
        )
        parser = parse_python_patch if arm == "python" else parse_lattice_patch
        patch = parser(response)
        allowed = set(task["allowed"])
        if set(patch) != allowed:
            return {"ok": False, "error": "scope"}
        after = before.edit(patch, allowed)
        if not audit_three_way(before, after, allowed)["ok"]:
            return {"ok": False, "error": "frame"}
        return {"ok": True, "error": None}
    except (ValueError, SyntaxError, TypeError, RecursionError):
        return {"ok": False, "error": "parse_or_compile"}


def public_feedback(result):
    """Fixed strings only: ignore any untrusted or private diagnostic fields."""
    if result.get("ok") is True:
        raise ValueError("do not request repair after public acceptance")
    messages = {
        "scope": "Public scope check failed. Edit exactly the authorized output and retry.",
        "frame": "Public frame check failed. Preserve protected outputs and retry.",
        "parse_or_compile": "Public parser/compiler rejected the edit. Retry in the requested output grammar.",
    }
    return messages.get(
        result.get("error"),
        "Public preflight rejected the edit. Retry without changing the authorized scope.",
    )
