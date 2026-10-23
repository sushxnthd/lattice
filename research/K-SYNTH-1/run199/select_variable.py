"""Outcome-blind variable-cluster selection for real Python multi-file issues.

The eligibility predicate and source revision are frozen from Run199 v1.
Variable cluster allocation was chosen after inspecting only availability
counts, before ANY capable-model outcomes on these real issues.
"""
from collections import defaultdict, Counter
from pathlib import Path
import json
from select_real_tasks import eligibility, rank, changed_files, canonical, digest

PROTOCOL="K-SYNTH-1/real-multifile-variable-cluster-v2"
REVISION="8851474cc41be8bce981362d1363d9f92e247b4b"
TARGET=480
MAX_PER_REPO=6
MAX_REPOS=200

def select_variable(rows,target=TARGET,max_per_repo=MAX_PER_REPO,max_repos=MAX_REPOS):
    grouped=defaultdict(list);excluded=Counter();seen=set()
    for r in rows:
        reason=eligibility(r)
        if reason:
            excluded[reason]+=1;continue
        key=str(r["instance_id"])
        if key in seen:
            excluded["duplicate_id"]+=1;continue
        seen.add(key);grouped[r["repo"]].append(r)
    for repo in grouped:
        grouped[repo].sort(key=lambda r:(rank(str(r["instance_id"])),str(r["instance_id"])))
    repos=sorted(grouped,key=lambda x:(rank("repo:"+x),x))[:max_repos]
    selected=defaultdict(list)
    # Every eligible repository contributes one issue before any second issue.
    for slot in range(max_per_repo):
        for repo in repos:
            if len(selected[repo])>=slot+1:continue
            if len(grouped[repo])<=slot:continue
            if sum(map(len,selected.values()))>=target:break
            selected[repo].append(grouped[repo][slot])
        if sum(map(len,selected.values()))>=target:break
    active=[repo for repo in repos if selected[repo]]
    boundary=set(sorted(active,key=lambda x:(rank("boundary:"+x),x))[:round(len(active)*.2)])
    public=[];sealed=[]
    for repo in active:
        for row in selected[repo]:
            public.append(dict(instance_id=row["instance_id"],repo=repo,base_commit=row["base_commit"],
                image_name=row["image_name"],problem_statement=row["problem_statement"],language="python",
                split="boundary" if repo in boundary else "discovery"))
            sealed.append(dict(instance_id=row["instance_id"],repo=repo,patch=row["patch"],
                gold_changed_files=changed_files(row["patch"]),test_patch=row.get("test_patch"),
                FAIL_TO_PASS=row["FAIL_TO_PASS"],PASS_TO_PASS=row.get("PASS_TO_PASS",[]),
                install_config=row.get("install_config"),meta=row.get("meta")))
    public.sort(key=lambda r:(r["repo"],r["instance_id"]))
    sealed.sort(key=lambda r:(r["repo"],r["instance_id"]))
    sizes=Counter(len(selected[r]) for r in active)
    manifest=dict(protocol=PROTOCOL,source_dataset="PrimeIntellect/SWE-rebench-V2",source_revision=REVISION,
        seed="lattice-199-frozen-2026-10-23",target_issues=target,selected_issues=len(public),
        selected_repositories=len(active),eligible_repositories=len(grouped),max_per_repository=max_per_repo,
        cluster_size_histogram=dict(sorted(sizes.items())),
        discovery_issues=sum(x["split"]=="discovery" for x in public),
        boundary_issues=sum(x["split"]=="boundary" for x in public),
        boundary_repositories=len(boundary),exclusions=dict(sorted(excluded.items())),
        public_sha256=digest(public),sealed_sha256=digest(sealed),
        inference_ready=len(public)==target and len(active)>=150,
        note="Variable cluster sizes require actual-cluster power re-estimation; 480 alone does not prove adequate power. No model outcomes inspected.")
    return public,sealed,manifest

def main():
    import argparse
    from datasets import load_dataset
    p=argparse.ArgumentParser();p.add_argument("--out",type=Path,required=True);a=p.parse_args()
    rows=load_dataset("PrimeIntellect/SWE-rebench-V2",split="train",revision=REVISION)
    public,sealed,manifest=select_variable(rows)
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"public.json").write_bytes(canonical(public))
    (a.out/"sealed_evaluator.json").write_bytes(canonical(sealed))
    (a.out/"manifest.json").write_bytes(canonical(manifest))
    print(json.dumps(manifest,indent=2))

if __name__=="__main__":main()
