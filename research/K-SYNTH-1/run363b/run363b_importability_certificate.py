#!/usr/bin/env python3
"""Run363b bounded import-dependency certificate; no production code execution."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Bit 0: app.py, bit 1: ctx.py, bit 2: helpers.py.
# Pinned head sources import _CollectErrors from helpers in app and ctx;
# only head helpers declares that class. Baseline declares none.
ORIGINAL_IMPORTABLE = {0: True, 1: False, 2: False, 3: False,
                       4: True, 5: True, 6: True, 7: True}
ORIGINAL_FUNCTIONAL = {
    0: (0, 6), 1: None, 2: None, 3: None,
    4: (0, 6), 5: (6, 6), 6: (0, 6), 7: (6, 6),
}

def predict(mask):
    app_new, ctx_new, helper_new = bool(mask & 1), bool(mask & 2), bool(mask & 4)
    return helper_new or not (app_new or ctx_new)

def execute_synthetic(mask):
    with tempfile.TemporaryDirectory(prefix="lattice-import-") as temp:
        root = Path(temp)
        pkg = root / "sample"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")
        (pkg / "helpers.py").write_text(
            "class _CollectErrors: pass\n" if mask & 4 else "class ExistingHelper: pass\n"
        )
        for bit, module in ((1, "app"), (2, "ctx")):
            (pkg / (module + ".py")).write_text(
                "from .helpers import _CollectErrors\n" if mask & bit else "VALUE = 1\n"
            )
        code = f"import sys;sys.path.insert(0,{str(root)!r});import sample.app;import sample.ctx"
        run = subprocess.run([sys.executable, "-I", "-c", code],
                             capture_output=True, text=True, timeout=10)
        return {"mask": mask, "success": run.returncode == 0,
                "error": run.stderr[-300:] if run.returncode else None}

def main():
    traces = [execute_synthetic(mask) for mask in range(8)]
    for item in traces:
        mask = item["mask"]
        assert item["success"] == predict(mask) == ORIGINAL_IMPORTABLE[mask]
    print(json.dumps({
        "schema": "run363b.import-dependency.v1",
        "synthetic_imports": traces,
        "prediction_matches_original": 8,
        "original_functional_counts": ORIGINAL_FUNCTIONAL,
        "original_precompletion_import_errors": 36,
        "original_executed_cases": 60,
        "frozen_qualification": "INCONCLUSIVE",
        "soundness_scope": "direct Python from-import, no dynamic import hooks or injection"
    }, sort_keys=True))

if __name__ == "__main__":
    main()
