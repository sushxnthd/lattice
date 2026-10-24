#!/usr/bin/env python3
"""Run233 standalone guard-mechanism witness (Python 3.10+, stdlib only).

This is a *minimal reproduction*, not a replay of the original full model
outputs. For byte-exact primary evaluation and raw completions, use the
Run233 reproducibility archive and its frozen Run232 independent auditor.
"""
from types import SimpleNamespace

STATES = ("absent", "empty", "one_unsolved", "partial", "solved", "multi_solved")
EXPECTED = {"number_of_images": 3, "duration": .2, "output_filename": "output.gif"}

def probe(kind, state, cached):
    events = []
    class QuickPlot:
        def __init__(self, source):
            events.append("construct")
        def create_gif(self, **kwargs):
            events.append(("gif", kwargs))
    obj = SimpleNamespace(quick_plot=QuickPlot([]) if cached else None)
    events.clear()
    solved = SimpleNamespace(solution=object())
    unsolved = SimpleNamespace(solution=None)
    if state == "empty": obj.sims = []
    if state == "one_unsolved": obj.sims = [unsolved]
    if state == "partial": obj.sims = [solved, unsolved]
    if state == "solved": obj.sims = [solved]
    if state == "multi_solved": obj.sims = [solved, solved]
    error = None
    try:
        if kind == "ir":
            if obj._solution is None:
                raise ValueError("unsolved")
        elif kind == "python":
            if obj.sims == []:
                raise ValueError("unsolved")
        elif kind == "corrected":
            if (not hasattr(obj, "sims") or not obj.sims or
                    any(getattr(sim, "solution", None) is None for sim in obj.sims)):
                raise ValueError("unsolved")
        else:
            raise AssertionError(kind)
        if obj.quick_plot is None:
            obj.quick_plot = QuickPlot(obj.sims)
        obj.quick_plot.create_gif(**EXPECTED)
    except Exception as exc:
        error = type(exc).__name__
    valid = state in ("solved", "multi_solved")
    if valid:
        return (error is None and events ==
                ([] if cached else ["construct"]) + [("gif", EXPECTED)])
    return error == "ValueError" and not events

def sim_probe(solved, cached):
    # Both genuine model outputs correctly guard Simulation._solution.
    events = []
    obj = SimpleNamespace(_solution=object() if solved else None,
                          quick_plot=object() if cached else None)
    error = None
    try:
        if obj._solution is None:
            raise ValueError("unsolved")
        if obj.quick_plot is None:
            events.append("construct")
        events.append("gif")
    except Exception as exc:
        error = type(exc).__name__
    return (error is None and events == ([] if cached else ["construct"]) + ["gif"]
            if solved else error == "ValueError" and not events)

def main():
    for kind, expected in (("ir", 4), ("python", 10), ("corrected", 16)):
        batch = sum(probe(kind, state, cached) for state in STATES
                    for cached in (False, True))
        sim = sum(sim_probe(solved, cached) for solved in (False, True)
                  for cached in (False, True))
        assert batch + sim == expected, (kind, batch, sim)
        print(f"{kind}: BatchStudy {batch}/12, Simulation {sim}/4, total {batch+sim}/16")
    print("Minimal witness passed. Guard correction is POST-HOC, not model success.")

if __name__ == "__main__":
    main()
