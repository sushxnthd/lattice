"""Run79 two-turn CPU-only paired model pilot; never execute model-produced code."""
import argparse
import hashlib
import json
import os
import platform
import time
import urllib.request
from pathlib import Path
from research.run79.independent_scoring import load_tasks, score
from research.run79.prompts import paired_prompts, gate

MODEL = "Qwen2.5-Coder-7B-Instruct-GGUF-Q4_K_M"
URL = "http://127.0.0.1:8080/v1/chat/completions"
SEED = 271828

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def normalize(raw):
    lines = raw.strip().splitlines()
    if len(lines) >= 3 and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
        tag = lines[0].strip()[3:].lower()
        if tag in ("", "python", "lattice", "ir"):
            return "\n".join(lines[1:-1]).strip()
    return raw.strip()

def call(messages):
    request = {"model": MODEL, "messages": messages, "temperature": 0.0, "top_p": 1.0,
               "seed": SEED, "max_tokens": 256, "stream": False}
    body = json.dumps(request, sort_keys=True).encode()
    req = urllib.request.Request(URL, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    started = time.monotonic()
    with opener.open(req, timeout=1200) as response:
        if response.status != 200:
            raise RuntimeError("HTTP " + str(response.status))
        raw = response.read(3000001)
    if len(raw) > 3000000:
        raise RuntimeError("oversized response")
    result = json.loads(raw)
    usage = result["usage"]
    if not all(type(usage.get(k)) is int for k in ("prompt_tokens", "completion_tokens")):
        raise RuntimeError("missing token usage")
    content = result["choices"][0]["message"]["content"]
    if not isinstance(content, str):
        raise RuntimeError("nontext response")
    return body, raw, content, usage, round(time.monotonic() - started, 3)

def feedback(result):
    if result.get("error") == "semantic":
        witness = {k: result[k] for k in ("input", "output", "expected", "got")}
        return ("Semantic verification failed at " + json.dumps(witness, sort_keys=True)
                + ". Revise only the authorized output and return the requested format.")
    return ("The compiler or independent verifier rejected the edit. "
            "Revise only the authorized output and return the requested format.")

def run(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    pairs = paired_prompts()
    manifest = Path(__file__).with_name("tasks.json").read_bytes()
    freeze = {"status": "DEVELOPMENT_ONLY", "model": MODEL, "seed": SEED,
              "temperature": 0, "top_p": 1, "max_tokens": 256, "max_calls": 2,
              "task_manifest_sha256": digest(manifest), "git_sha": os.getenv("GITHUB_SHA"),
              "weight_sha256": os.getenv("LATTICE_MODEL_SHA256", "NOT_ATTESTED"),
              "llama_commit": os.getenv("LATTICE_LLAMA_COMMIT", "NOT_ATTESTED"),
              "python": platform.python_version(), "platform": platform.platform()}
    (out / "freeze.json").write_text(json.dumps(freeze, indent=2, sort_keys=True))
    gate(out)
    rows = []
    for idx, task in enumerate(load_tasks()):
        arms = ("python", "ir") if idx % 2 == 0 else ("ir", "python")
        for arm in arms:
            messages = [{"role": "user", "content": pairs[task["id"]][arm]}]
            attempts = []
            for turn in (1, 2):
                body, raw, answer, usage, seconds = call(messages)
                stem = task["id"] + "_" + arm + "_" + str(turn)
                (out / (stem + "_request.json")).write_bytes(body)
                (out / (stem + "_response.json")).write_bytes(raw)
                evaluated = score(task, arm, normalize(answer))
                attempts.append({"turn": turn, "raw_text": answer,
                                 "normalized_text": normalize(answer),
                                 "request_sha256": digest(body), "response_sha256": digest(raw),
                                 "usage": usage, "wall_seconds": seconds, "score": evaluated})
                (out / "partial_results.json").write_text(json.dumps(rows + [{
                    "task": task["id"], "arm": arm, "attempts": attempts}], indent=2))
                if evaluated["ok"]:
                    break
                messages += [{"role": "assistant", "content": answer},
                             {"role": "user", "content": feedback(evaluated)}]
            rows.append({"task": task["id"], "arm": arm, "attempts": attempts})
    summary = {"model": MODEL, "tasks": len(load_tasks()), "paired": {},
               "claim_boundary": "One model, six development Boolean tasks; not a scientific breakthrough."}
    for task in load_tasks():
        subset = {row["arm"]: row for row in rows if row["task"] == task["id"]}
        summary["paired"][task["id"]] = {arm: {
            "success": subset[arm]["attempts"][-1]["score"]["ok"],
            "calls": len(subset[arm]["attempts"]),
            "tokens": sum(a["usage"]["prompt_tokens"] + a["usage"]["completion_tokens"]
                          for a in subset[arm]["attempts"])}
            for arm in ("python", "ir")}
    summary["successes"] = {arm: sum(int(v[arm]["success"]) for v in summary["paired"].values())
                            for arm in ("python", "ir")}
    summary["difference_ir_minus_python"] = (
        summary["successes"]["ir"] - summary["successes"]["python"]) / len(load_tasks())
    (out / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=2))
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--gate-only", action="store_true")
    args = parser.parse_args()
    if args.gate_only:
        print(json.dumps(gate(args.output), indent=2))
    else:
        print(json.dumps(run(args.output), indent=2))
