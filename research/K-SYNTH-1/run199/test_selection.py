"""Adversarial and determinism checks for the prospective real-issue sampler."""
import copy
from select_real_tasks import changed_files, eligibility, select, digest

def fake(repo, num):
    return dict(language="Python", license="MIT", repo=repo,
        instance_id=f"{repo}-{num}", base_commit="a"*40,
        image_name="docker.io/test/image:tag", created_at=1750000000000,
        problem_statement="Fix this cross-module defect " + "observed in production tests "*9,
        patch="diff --git a/pkg/a.py b/pkg/a.py\n@@ -1 +1 @@\n-a\n+b\n"+
              "diff --git a/pkg/b.py b/pkg/b.py\n@@ -1 +1 @@\n-a\n+b\n",
        test_patch="diff --git a/tests/test_a.py b/tests/test_a.py\n",
        FAIL_TO_PASS=["test_a"], PASS_TO_PASS=["test_b"],
        install_config={"python":"3.11"})

def test_paths_and_eligibility():
    assert changed_files(fake("r",0)["patch"]) == ["pkg/a.py","pkg/b.py"]
    assert eligibility(fake("r",0)) is None

def test_reproducibility_repository_split_and_no_gold_leakage():
    rows = [fake(f"org/r{i}",j) for i in range(8) for j in range(4)]
    a,b,m = select(rows,repos=5,per_repo=4)
    a2,b2,m2 = select(list(reversed(rows)),repos=5,per_repo=4)
    assert (a,b,m)==(a2,b2,m2)
    assert m["inference_ready"] and m["selected_issues"]==20
    assert len({x["repo"] for x in a if x["split"]=="boundary"})==1
    assert not any("patch" in x or "FAIL_TO_PASS" in x or "test_patch" in x or "files" in x for x in a)
    assert all("patch" in x and "gold_changed_files" in x for x in b)
    assert m["public_sha256"]==digest(a)

def test_ineligible_tasks_do_not_create_power_claim():
    rows=[fake("r",j) for j in range(4)]
    bad=copy.deepcopy(rows[0])
    bad["instance_id"]="bad"
    bad["patch"]="diff --git a/x.py b/x.py\n"
    rows.append(bad)
    _,_,m=select(rows,repos=3,per_repo=4)
    assert not m["inference_ready"]
    assert m["selected_repositories"]==1
    assert m["exclusions"]["file_count"]==1

def test_duplicate_ids_cannot_fake_independent_issues():
    rows=[fake("r",0)]*4
    _,_,m=select(rows,repos=1,per_repo=4)
    assert not m["inference_ready"]
    assert m["exclusions"]["duplicate_id"]==3
