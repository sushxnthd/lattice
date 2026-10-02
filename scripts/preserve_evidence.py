"""Preserve completed experiment artifacts downloaded by the official Action."""
import gzip, hashlib, json, subprocess
from pathlib import Path

collected = {}
provenance = []
sources = [
    (37017261765,"exp002",Path("_evidence_downloads/exp002")),
    (37018691609,"exp003",Path("_evidence_downloads/exp003")),
]
artifact_ids = {
 "Qwen2.5-Coder-0.5B-Instruct.json":11232245905,
 "Qwen2.5-Coder-1.5B-Instruct.json":11233200612,
 "prompt_order.json":11232787130,
}
for run, folder, source in sources:
    for p in source.rglob("*.json"):
        content = p.read_bytes()
        data = json.loads(content)
        basename = p.name
        if basename not in artifact_ids:
            raise RuntimeError("Unexpected evidence file")
        if folder == "exp002":
            expected = "678f1372ec4a728a10137ec1eb66b78aba722851c440c5d7c87909f08628781e"
            if data["manifest"]["task_definition_sha256"] != expected:
                raise RuntimeError("Task definition changed")
        target=Path("artifacts")/folder/basename
        target.parent.mkdir(parents=True,exist_ok=True)
        compact=json.dumps(data,sort_keys=True,separators=(",",":")).encode()
        target.with_suffix(".json.gz").write_bytes(gzip.compress(compact,mtime=0))
        target.with_suffix(".summary.json").write_text(json.dumps({k:v for k,v in data.items() if k!="rows"},indent=2,sort_keys=True)+"\n")
        collected[basename]=data
        provenance.append({"run_id":run,"artifact_id":artifact_ids[basename],
            "file":str(target.with_suffix(".json.gz")),"raw_file_sha256":hashlib.sha256(content).hexdigest()})

# Validate and preserve the final framed compiler revision too.
subprocess.run(["python","experiments/exp002/frame_validation.py"],check=True)
p = Path("artifacts/exp002/frame_validation.json")
data = json.loads(p.read_text())
p.with_suffix(".json.gz").write_bytes(gzip.compress(json.dumps(data,sort_keys=True,separators=(",",":")).encode(),mtime=0))
p.with_suffix(".summary.json").write_text(json.dumps({k:v for k,v in data.items() if k!="rows"},indent=2,sort_keys=True)+"\n")
p.unlink()
Path("artifacts/evidence_provenance.json").write_text(json.dumps(provenance,indent=2,sort_keys=True)+"\n")

larger = collected.get("Qwen2.5-Coder-1.5B-Instruct.json")
diagnostic = collected.get("prompt_order.json")
if larger is None or diagnostic is None:
    raise RuntimeError("Missing required completed evidence")

report = Path("docs/EXP002_ASSESSMENT.md")
body = report.read_text()
marker = "Pending completion when this draft was first written. Fill only from the completed\nartifact; do not infer success from a green workflow or the compiler stress test."
table = ["| Condition | Hold-out first attempt | After one repair | All three checkpoints |",
         "|---|---:|---:|---:|"]
labels = {"python_full":"Complete Python","python_patch":"Python expression patch","lattice_patch":"Lattice assignment patch"}
for arm in ("python_full","python_patch","lattice_patch"):
    s=larger["summary"]["holdout"][arm]
    table.append(f"| {labels[arm]} | {s['first_attempt_successes']} / {s['checkpoints']} | {s['successes_with_one_repair']} / {s['checkpoints']} | {s['all_three_checkpoints_succeeded']} / {s['trajectories']} |")
table += ["", "These are completed artifact values. Full prompts and generations:",
          "artifacts/exp002/Qwen2.5-Coder-1.5B-Instruct.json.gz.",
          "Both model sizes are one model family; no general-language superiority",
          "or external application result is inferred."]
if marker not in body: raise RuntimeError("Expected report marker missing")
body=body.replace(marker,"\n".join(table))
diag=["", "### Completed prompt diagnostic", "",
      "| Prompt variant | Complete Python | Python patch | Lattice patch |",
      "|---|---:|---:|---:|"]
for condition in ("original","request_last","alias_example","both"):
    s=diagnostic["summary"][condition]
    diag.append(f"| {condition} | {s['python_full']['correct']} / 3 | {s['python_patch']['correct']} / 3 | {s['lattice_patch']['correct']} / 3 |")
diag += ["", "This diagnostic did not establish a Lattice advantage. Task-named examples",
         "solved one of three tasks for both patch interfaces. These previously evaluated",
         "tasks cannot serve as fresh hold-out confirmation. Full transcripts:",
         "artifacts/exp003/prompt_order.json.gz.",
         "[Diagnostic workflow](https://github.com/sushxnthd/lattice/actions/runs/37018691609)."]
body=body.replace("## Existing negative evidence","\n".join(diag)+"\n\n## Existing negative evidence")
report.write_text(body)

# Stage only designated evidence and documentation; never tokens or temporary archives.
subprocess.run(["git","config","user.name","github-actions[bot]"],check=True)
subprocess.run(["git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com"],check=True)
subprocess.run(["git","add","artifacts","docs/EXP002_ASSESSMENT.md"],check=True)
changed=subprocess.run(["git","diff","--cached","--quiet"]).returncode
if changed:
    subprocess.run(["git","commit","-m","Preserve completed model transcripts and compiler validation evidence"],check=True)
    subprocess.run(["git","push","origin","HEAD:research/exp003-context-order"],check=True)
print(json.dumps({"larger_model_summary":larger["summary"],"diagnostic_summary":diagnostic["summary"],
                  "compiler_summary":data["summary"]},sort_keys=True))
