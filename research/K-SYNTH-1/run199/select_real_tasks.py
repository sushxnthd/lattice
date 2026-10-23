"""Prospectively frozen selection of independent real multi-file repository repairs.

Gold patches/tests are used only for eligibility and held in a sealed evaluator
artifact, never included in model-visible task prompts or edit localization.
This sampler DOES NOT run model inference or claim benchmark success.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

PROTOCOL = "K-SYNTH-1/real-multifile-selection-v1"
SEED = "lattice-199-frozen-2026-10-23"
LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"}
COMMIT = re.compile(r"^[0-9a-f]{40}$")
DIFF = re.compile(r"^diff --git a/(.+?) b/(.+)$", re.M)

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()

def digest(x):
    return hashlib.sha256(canonical(x)).hexdigest()

def rank(s):
    return hashlib.sha256((SEED + ":" + s).encode()).hexdigest()

def changed_files(patch):
    return sorted(set(b for a, b in DIFF.findall(patch) if a == b and not b.startswith("/")))

def eligibility(row):
    if str(row.get("language", "")).lower() != "python": return "language"
    if row.get("license") not in LICENSES: return "license"
    if len(str(row.get("problem_statement") or "").split()) < 40: return "issue_length"
    if not COMMIT.fullmatch(str(row.get("base_commit") or "")): return "base_commit"
    if not row.get("image_name"): return "no_image"
    if not row.get("FAIL_TO_PASS"): return "no_f2p"
    if not isinstance(row.get("patch"), str) or len(row["patch"]) > 20000: return "patch_size"
    paths = changed_files(row["patch"])
    if not 2 <= len(paths) <= 6: return "file_count"
    if sum(p.endswith(".py") for p in paths) < 2: return "python_files"
    if not row.get("repo") or not row.get("instance_id"): return "identity"
    created = row.get("created_at")
    if created is None: return "created_at"
    try:
        if isinstance(created, datetime):
            year = created.year
        elif isinstance(created, str) and not created.strip().isdigit():
            year = datetime.fromisoformat(created.replace("Z", "+00:00")).year
        else:
            stamp = int(created)
            year = datetime.fromtimestamp(stamp / (1000 if stamp > 10**11 else 1), tz=timezone.utc).year
    except (TypeError, ValueError, OverflowError): return "created_at"
    if year < 2024: return "too_old"
    return None

def select(rows, *, repos=120, per_repo=4):
    """Select by deterministic hashes, not model results or gold solution quality."""
    grouped = defaultdict(list)
    exclusions = Counter()
    seen = set()
    for row in rows:
        reason = eligibility(row)
        if reason:
            exclusions[reason] += 1
            continue
        ident = str(row["instance_id"])
        if ident in seen:
            exclusions["duplicate_id"] += 1
            continue
        seen.add(ident)
        grouped[row["repo"]].append(row)
    eligible = {
        repo: sorted(v, key=lambda r: (rank(str(r["instance_id"])), str(r["instance_id"])))
        for repo, v in grouped.items() if len(v) >= per_repo
    }
    selected_repos = sorted(eligible, key=lambda r: (rank("repo:" + r), r))[:repos]
    boundary = set(sorted(selected_repos, key=lambda r: (rank("boundary:" + r), r))[:round(len(selected_repos)*0.2)])
    public, sealed = [], []
    for repo in selected_repos:
        for row in eligible[repo][:per_repo]:
            paths = changed_files(row["patch"])
            split = "boundary" if repo in boundary else "discovery"
            public.append(dict(
                instance_id=row["instance_id"], repo=repo, base_commit=row["base_commit"],
                image_name=row["image_name"], problem_statement=row["problem_statement"],
                split=split, language="python"))
            sealed.append(dict(
                instance_id=row["instance_id"], repo=repo, patch=row["patch"],
                gold_changed_files=paths, test_patch=row.get("test_patch"),
                FAIL_TO_PASS=row["FAIL_TO_PASS"], PASS_TO_PASS=row.get("PASS_TO_PASS", []),
                install_config=row.get("install_config"), meta=row.get("meta")))
    public.sort(key=lambda r: (r["repo"], r["instance_id"]))
    sealed.sort(key=lambda r: (r["repo"], r["instance_id"]))
    summary = dict(
        protocol=PROTOCOL, seed=SEED, requested_repositories=repos,
        requested_issues=repos*per_repo, selected_repositories=len(selected_repos),
        selected_issues=len(public), per_repository=per_repo,
        discovery_repositories=len(selected_repos)-len(boundary),
        boundary_repositories=len(boundary),
        discovery_issues=sum(x["split"] == "discovery" for x in public),
        boundary_issues=sum(x["split"] == "boundary" for x in public),
        eligible_repositories=len(eligible), exclusions=dict(sorted(exclusions.items())),
        public_sha256=digest(public), sealed_sha256=digest(sealed),
        inference_ready=(len(selected_repos)==repos),
        caution="No inference before freeze, positive controls and matched compiler/verifier. No outcome peeking. Gold/test fields forbidden in prompts.")
    return public, sealed, summary

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-jsonl", type=Path)
    p.add_argument("--hf-dataset", default="PrimeIntellect/SWE-rebench-V2")
    p.add_argument("--revision", default="main")
    p.add_argument("--repos", type=int, default=120)
    p.add_argument("--per-repo", type=int, default=4)
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args()
    if a.repos < 1 or a.per_repo < 1: p.error("positive quotas required")
    if a.input_jsonl:
        rows = (json.loads(line) for line in a.input_jsonl.open() if line.strip())
        source = dict(kind="jsonl", input_sha256=hashlib.sha256(a.input_jsonl.read_bytes()).hexdigest())
    else:
        from datasets import load_dataset
        from huggingface_hub import HfApi
        revision = HfApi().dataset_info(a.hf_dataset, revision=a.revision).sha
        rows = load_dataset(a.hf_dataset, split="train", revision=revision)
        source = dict(kind="huggingface", dataset=a.hf_dataset, revision=revision)
    public, sealed, manifest = select(rows, repos=a.repos, per_repo=a.per_repo)
    manifest["source"] = source
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out/"public.json").write_bytes(canonical(public))
    (a.out/"sealed_evaluator.json").write_bytes(canonical(sealed))
    (a.out/"manifest.json").write_bytes(canonical(manifest))
    print(json.dumps(manifest, indent=2))
    if not manifest["inference_ready"]:
        print("INSUFFICIENT ELIGIBLE REPOSITORIES: DO NOT CALL THIS POWERED", flush=True)

if __name__ == "__main__":
    main()
