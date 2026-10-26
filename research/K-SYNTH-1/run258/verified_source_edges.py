#!/usr/bin/env python3
"""Run258 independent narrow source-verified import edge and exact source spans.

This is not a sound general Python call graph or semantic/dataflow IR.
"""
import ast
import hashlib
import json
from pathlib import Path

PATHS = ("src/flask/app.py", "src/flask/testing.py")
NEEDLES = {
    PATHS[0]: 'sn_host, _, sn_port = server_name.partition(":")',
    PATHS[1]: 'ctx.request.host.partition(":")[0]',
}

def source_window(path, source, before=8, after=12):
    lines = source.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if NEEDLES[path] in line]
    if len(hits) != 1:
        raise ValueError("source anchor not unique: " + path)
    at = hits[0]
    lo, hi = max(0, at-before), min(len(lines), at+after+1)
    exact = "".join(lines[lo:hi])
    if source.count(exact) != 1:
        raise ValueError("source span not unique: " + path)
    return {"path": path, "start_line": lo+1, "end_line": hi,
            "sha256": hashlib.sha256(exact.encode()).hexdigest(),
            "source_exact": exact}

def verified_relative_import(sources):
    app = ast.parse(sources[PATHS[0]])
    testing = ast.parse(sources[PATHS[1]])
    classes = [n for n in testing.body if isinstance(n, ast.ClassDef)
               and n.name == "FlaskClient"]
    if len(classes) != 1:
        raise ValueError("target class missing or ambiguous")
    flask = next(n for n in app.body if isinstance(n, ast.ClassDef)
                 and n.name == "Flask")
    method = next(n for n in flask.body if isinstance(n, ast.FunctionDef)
                  and n.name == "test_client")
    edges = [n for n in ast.walk(method) if isinstance(n, ast.ImportFrom)
             and n.level == 1 and n.module == "testing"
             and any(a.name == "FlaskClient" for a in n.names)]
    if len(edges) != 1:
        raise ValueError("relative import missing or ambiguous")
    return {"kind": "verified_relative_import_binding",
            "from": "src/flask/app.py::Flask.test_client",
            "to": "src/flask/testing.py::FlaskClient",
            "import_lineno": edges[0].lineno,
            "target_class_lineno": classes[0].lineno,
            "guaranteed_runtime_invocation": False,
            "uncertainty": "test_client_class can be overridden dynamically"}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    args = parser.parse_args()
    sources = {p: (args.source_root / p).read_text() for p in PATHS}
    result = {"binding": verified_relative_import(sources),
              "windows": [source_window(p, sources[p]) for p in PATHS]}
    print(json.dumps(result, sort_keys=True, indent=2))
