from select_variable import select_variable
from test_selection import fake

def test_round_robin_determinism_and_no_gold():
    rows=[fake(f"org/r{i}",j) for i in range(10) for j in range(7)]
    a,b,m=select_variable(rows,target=48,max_per_repo=6,max_repos=10)
    a2,b2,m2=select_variable(list(reversed(rows)),target=48,max_per_repo=6,max_repos=10)
    assert (a,b,m)==(a2,b2,m2)
    assert m["selected_issues"]==48 and m["selected_repositories"]==10
    assert max(m["cluster_size_histogram"])<=6
    assert not any("patch" in r or "gold_changed_files" in r for r in a)
    assert len({r["repo"] for r in a if r["split"]=="boundary"})==2

def test_insufficient_supply_fails_closed():
    rows=[fake("org/one",j) for j in range(3)]
    _,_,m=select_variable(rows,target=480,max_per_repo=6,max_repos=200)
    assert not m["inference_ready"] and m["selected_issues"]==3
