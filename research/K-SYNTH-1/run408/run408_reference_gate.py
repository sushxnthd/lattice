#!/usr/bin/env python3
"""Run408: structural production-source gate; not behavioral qualification."""
from pathlib import PurePosixPath

def is_production_python(path):
    if not isinstance(path, str) or not path or "\\" in path or path.startswith("/"):
        return False
    p = PurePosixPath(path)
    if ".." in p.parts or "." in p.parts or not p.parts or p.parts[0] != "src":
        return False
    if p.suffix != ".py" or len(p.parts) < 3:
        return False
    return not any(x in {"test", "tests", "testing", "examples", "docs", "generated", "fixtures"}
                   or x.startswith("test_") for x in p.parts)

def evaluate(paths, minimum=2):
    if not isinstance(paths, list) or len(set(paths)) != len(paths):
        raise ValueError("MALFORMED_OR_DUPLICATE_FILE_LIST")
    production = sorted(p for p in paths if is_production_python(p))
    return {
        "changed_files": len(paths),
        "production_python_files": production,
        "production_count": len(production),
        "minimum_required": minimum,
        "status": "STRUCTURALLY_ELIGIBLE_NOT_BEHAVIORALLY_QUALIFIED"
                  if len(production) >= minimum else "NOT_QUALIFIED",
        "behavioral_necessity_tested": False,
    }

if __name__ == "__main__":
    files = ["changelog/14635.bugfix.rst", "src/_pytest/main.py",
             "testing/test_conftest.py"]
    result = evaluate(files)
    assert result["status"] == "NOT_QUALIFIED"
    assert result["production_count"] == 1
    print(result)
