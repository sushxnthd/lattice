#!/usr/bin/env python3
"""Standalone CPython witness for Run230's genuine Qwen outputs.

Argument: directory extracted from GitHub Actions artifact 12576070605.
This checks immutable response hashes and replays 16 necessary-condition
cases. It does not replace the full independent compiler audit.
"""
import hashlib
import json
import pathlib
import sys
import types

EXPECTED = {
    "semantic_ir_json": ("043c8c9d95cc27ba64e3b29551c80dd8db5bdfc67cdd9839e09eba48a40cac3f", "5323eb060ef4c48f950109f95994b08524d96c03d3f85d8d41861d23e50d0937"),
    "python_annotated": ("7c646bf995f80136bea983e85d3f310ee1c18a415a750c6df9c2338e4460ed2c", "a697af22d73875f82d06e9b8a3a50170e7199a07d26e97c3e2d75ec44d5c91e4"),
}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def evaluate(method, batch, state, cached):
    events = []
    class QuickPlot:
        def __init__(self, obj):
            events.append(("construct", None))
        def create_gif(self, **kwargs):
            events.append(("gif", kwargs))
    ns = {"pybamm": types.SimpleNamespace(QuickPlot=QuickPlot)}
    exec(compile("class Candidate:\n" + method, "<run231-qwen-method>", "exec"), ns)
    obj = ns["Candidate"]()
    obj.quick_plot = QuickPlot(None) if cached else None
    events.clear()
    if batch:
        solved = types.SimpleNamespace(solution=object())
        unsolved = types.SimpleNamespace(solution=None)
        if state == "empty": obj.sims = []
        if state == "one_unsolved": obj.sims = [unsolved]
        if state == "partial": obj.sims = [solved, unsolved]
        if state == "solved": obj.sims = [solved]
        if state == "multi_solved": obj.sims = [solved, solved]
        valid = state in ("solved", "multi_solved")
    else:
        obj._solution = object() if state == "solved" else None
        valid = state == "solved"
    error = None
    try:
        obj.create_gif(number_of_images=3, duration=.2, output_filename="output.gif")
    except Exception as e:
        error = type(e).__name__
    gifs = [v for kind,v in events if kind == "gif"]
    constructs = [v for kind,v in events if kind == "construct"]
    expected = {"number_of_images":3, "duration":.2, "output_filename":"output.gif"}
    if valid:
        passed = error is None and gifs == [expected] and len(constructs) == (0 if cached else 1)
    else:
        passed = error == "ValueError" and not gifs and not constructs
    return {"state":state, "cached":cached, "passed":passed, "error":error, "events":events}

def main(folder):
    out = {}
    for arm,(req_sha,resp_sha) in EXPECTED.items():
        req = (folder/f"{arm}-request.json").read_bytes()
        resp = (folder/f"{arm}-response.json").read_bytes()
        record = json.loads((folder/f"{arm}-inference-record.json").read_text())
        assert sha(req) == req_sha == record["request_sha256"]
        assert sha(resp) == resp_sha == record["response_sha256"]
        assert record["model_sha256"] == "509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c"
        assert record["seed"] == 1560714227
        response = json.loads(resp)
        assert response["usage"] == record["usage"]
        actions = json.loads(response["choices"][0]["message"]["content"])["actions"]
        assert len(actions) == 2
        assert all(set(a) == {"op","path","file_sha256","selector","replacement"} for a in actions)
        cases = []
        for a in actions:
            batch = a["path"] == "pybamm/batch_study.py"
            assert a["op"] == "replace" and a["replacement"].startswith("    def create_gif(")
            states = ("absent","empty","one_unsolved","partial","solved","multi_solved") if batch else ("unsolved","solved")
            for state in states:
                for cached in (False,True):
                    cases.append({"path":a["path"],**evaluate(a["replacement"],batch,state,cached)})
        assert len(cases) == 16
        assert sum(c["passed"] for c in cases) == 4
        assert all(c["error"] == "AttributeError" for c in cases if c["path"] == "pybamm/batch_study.py")
        out[arm] = {"passed":4, "total":16, "usage":record["usage"], "cases":cases}
    return out

if __name__ == "__main__":
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".")
    print(json.dumps(main(root),indent=2,sort_keys=True))
