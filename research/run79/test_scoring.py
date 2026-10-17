from research.run79.independent_scoring import load_tasks, score

def test_scoring_parity():
    for task in load_tasks():
        name = task["allowed"][0]
        expr = task["target"][name]
        assert score(task, "python", "{" + repr(name) + ": " + expr + "}")["ok"]
        assert score(task, "ir", name + " = " + expr)["ok"]
