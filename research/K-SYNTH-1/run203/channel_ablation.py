"""Run203: exact address-copy channel and Python short-ID mechanism control.

Input is the per_target.jsonl in the Run203 reproducibility archive.
The experiment is a mathematical model, NOT observed LLM performance.
"""
import argparse, json, math, statistics
from pathlib import Path

def exact_copy(length, per_character_error):
    if not 0 <= per_character_error < 1:
        raise ValueError("invalid channel rate")
    if length < 0:
        raise ValueError("negative length")
    return math.exp(length*math.log1p(-per_character_error))

def evaluate(rows, rate):
    if not rows:
        raise ValueError("empty target set")
    structural=[exact_copy(r["id_json_chars"],rate) for r in rows]
    python_text=[exact_copy(r["text_json_chars"],rate) for r in rows]
    # Same exact address bytes and same compiler authority in this ablation.
    python_short_id=[exact_copy(r["id_json_chars"],rate) for r in rows]
    assert structural==python_short_id
    savings=[r["text_json_chars"]-r["id_json_chars"] for r in rows]
    return {"target_count":len(rows),"per_character_error":rate,
        "mean_structural_id":statistics.mean(structural),
        "mean_python_text":statistics.mean(python_text),
        "mean_python_short_id_ablation":statistics.mean(python_short_id),
        "median_json_address_savings":statistics.median(savings),
        "structural_shorter_count":sum(s>0 for s in savings),
        "status":"length-only hypothetical channel; no model inference"}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--per-target",type=Path,required=True)
    p.add_argument("--rate",type=float,default=.001)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    rows=[json.loads(line) for line in args.per_target.read_text().splitlines() if line.strip()]
    result=evaluate(rows,args.rate)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,indent=2))
