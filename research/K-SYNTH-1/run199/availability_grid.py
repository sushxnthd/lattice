"""Outcome-blind availability grid: vary repository quota, never model outcomes."""
import json
from pathlib import Path
from datasets import load_dataset
from huggingface_hub import HfApi
from select_real_tasks import select, SEED

DATASET="PrimeIntellect/SWE-rebench-V2"
revision=HfApi().dataset_info(DATASET,revision="main").sha
rows=load_dataset(DATASET,split="train",revision=revision)
grid=[]
for per_repo in (1,2,3,4):
    target_repos=480//per_repo
    _,_,summary=select(rows,repos=target_repos,per_repo=per_repo)
    grid.append(dict(per_repo=per_repo,requested_repos=target_repos,
                     eligible_repos=summary["eligible_repositories"],
                     selected_repos=summary["selected_repositories"],
                     selected_issues=summary["selected_issues"],
                     inference_ready=summary["inference_ready"]))
result=dict(dataset=DATASET,revision=revision,seed=SEED,
            caveat="Selection availability only; zero model completions; no post-outcome tuning.",grid=grid)
Path("artifacts/run199").mkdir(parents=True,exist_ok=True)
Path("artifacts/run199/availability_grid.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
