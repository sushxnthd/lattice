"""Collect remote experiment evidence without relying on the assistant workspace."""
import gzip, hashlib, io, json, os, subprocess, time, zipfile
from pathlib import Path
import requests

API = "https://api.github.com/repos/sushxnthd/lattice"
PRIMARY = 37017261765
DIAGNOSTIC = 37018691609
session = requests.Session()
session.headers.update({"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
                        "Accept": "application/vnd.github+json"})
def api(path):
    response = session.get(API + path, timeout=60)
    response.raise_for_status()
    return response.json()

deadline = time.monotonic() + 45*60
while api(f"/actions/runs/{PRIMARY}")["status"] != "completed":
    if time.monotonic() > deadline:
        raise RuntimeError("Primary run has not finished; no final results fabricated")
    time.sleep(30)

collected = {}
provenance = []
for run, folder in ((PRIMARY, "exp002"), (DIAGNOSTIC, "exp003")):
    artifacts = api(f"/actions/runs/{run}/artifacts")["artifacts"]
    for artifact in artifacts:
        response = session.get(API + f"/actions/artifacts/{artifact['id']}/zip", timeout=60)
        response.raise_for_status()
        # requests strips Authorization on redirects to a different host.
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            for filename in z.namelist():
                if not filename.endswith(".json"): continue
                content = z.read(filename)
                data = json.loads(content)
                basename = Path(filename).name
                if folder == "exp002":
                    expected = "678f1372ec4a728a10137ec1eb66b78aba722851c440c5d7c87909f08628781e"
                    if data["manifest"]["task_definition_sha256"] != expected:
                        raise RuntimeError("Task definition changed")
                target = Path("artifacts") / folder / basename
                target.parent.mkdir(parents=True, exist_ok=True)
                compact = json.dumps(data, sort_keys=True, separators=(",",":")).encode()
                target.with_suffix(".json.gz").write_bytes(gzip.compress(compact, mtime=0))
                summary = {k:v for k,v in data.items() if k != "rows"}
                target.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True)+"\n")
                collected[basename] = data
                provenance.append({"run_id":run,"artifact_id":artifact["id"],
                    "artifact_digest":artifact.get("digest"),"file":str(target.with_suffix(".json.gz")),
                    "raw_file_sha256":hashlib.sha256(content).hexdigest()})

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
