"""Format-neutral repair diagnostic; post-hoc only, not a causal IR result."""
from __future__ import annotations
import json
from pathlib import Path
from lattice.semantic_edits import parse_lattice_patch, parse_python_patch
from research.run79.independent_scoring import load_tasks, score
from research.run79.model_pilot import normalize

PARSERS = {"python": parse_python_patch, "ir": parse_lattice_patch}


def diagnose(task, native_arm, response):
    """Use identical compiler and independent oracle for both patch surfaces."""
    if native_arm not in PARSERS:
        raise ValueError("unknown arm")
    text = normalize(response)
    native = score(task, native_arm, text)
    candidates = []
    for syntax, parser in PARSERS.items():
        try:
            patch = parser(text)
            candidates.append((syntax, patch))
        except (ValueError, SyntaxError, TypeError):
            continue
    if not candidates:
        return {"native": native, "normalized": {"ok": False, "error": "syntax"}}
    if any(patch != candidates[0][1] for _, patch in candidates[1:]):
        return {"native": native, "normalized": {"ok": False, "error": "ambiguous"}}
    if set(candidates[0][1]) != set(task["allowed"]):
        return {"native": native, "normalized": {"ok": False, "error": "scope"}}
    normalized = score(task, candidates[0][0], text)
    return {"native": native, "normalized": normalized,
            "parsed_as": candidates[0][0],
            "format_only_failure": bool(normalized["ok"] and not native["ok"])}


def reanalyze(path):
    """Analyze raw Run79 attempts without altering frozen prompts or feedback."""
    tasks = {task["id"]: task for task in load_tasks()}
    source = json.loads(Path(path).read_text())
    rows = source["rows"]
    if len(rows) != len(tasks) * 2:
        raise ValueError("incomplete paired transcript")
    seen = set()
    output = []
    for row in rows:
        key = (row["task"], row["arm"])
        if key in seen or key[0] not in tasks or key[1] not in PARSERS:
            raise ValueError("invalid task/arm")
        seen.add(key)
        scores = [diagnose(tasks[key[0]], key[1], a["raw_text"]) for a in row["attempts"]]
        output.append({"task": key[0], "arm": key[1],
                       "native_success": any(x["native"]["ok"] for x in scores),
                       "normalized_success": any(x["normalized"]["ok"] for x in scores),
                       "attempts": scores})
    return {"schema": "run82-posthoc-format-diagnostic-v1", "rows": output,
            "warning": "Observational post-hoc re-score; repair feedback was native-format-specific."}
