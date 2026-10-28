#!/usr/bin/env python3
"""Read-only post-outcome audit. Never executes model output or promotes salvage."""
import ast, hashlib, json, pathlib, re, sys, zipfile
archive = pathlib.Path(sys.argv[1])
with zipfile.ZipFile(archive) as z:
    files = {n: z.read(n) for n in z.namelist()}
manifest = json.loads(files["SHA256_MANIFEST.json"])
assert set(manifest) == set(files) - {"SHA256_MANIFEST.json"}
assert all(hashlib.sha256(files[n]).hexdigest() == digest for n, digest in manifest.items())
candidates = json.loads(files["candidates.json"])
known = {c["id"] for c in candidates}
assert len(candidates) == len(known) == 17
def identifiers(expr):
    tree = ast.parse(expr, mode="eval")
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
def lexical_port(expr):
    return any("port" in token.lower().split("_") for token in identifiers(expr))
lexical = {c["id"]: lexical_port(c["expr"]) for c in candidates}
assert sum(lexical.values()) == 11
out = {"manifest_verified": len(manifest), "lexical_port": 11, "substring_only": 6, "arms": {}}
for arm in ("IR", "PYTHON_AST"):
    request = json.loads(files[f"request_{arm}.json"])
    raw = json.loads(files[f"raw_{arm}.json"])
    completion = raw["choices"][0]["message"]["content"]
    assert completion.encode() == files[f"completion_{arm}.txt"]
    assert raw["choices"][0]["finish_reason"] == "stop"
    text = completion.removeprefix("```json\n").removesuffix("\n```")
    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        error = {"offset": e.pos, "reason": e.msg}
    else:
        raise AssertionError("Original completion unexpectedly valid")
    # Counterfactual diagnostic ONLY. This is not an accepted model output.
    assert text.count('port == """') == 1
    escaped = text.replace('port == """', 'port == \\"\\""')
    edits = json.loads(escaped)["edits"]
    bad_ids = [e["id"] for e in edits if e["id"] not in known]
    changed_known = [e["id"] for e in edits if e["id"] in known and e["new_expr"] != next(c["expr"] for c in candidates if c["id"] == e["id"])]
    out["arms"][arm] = {
        "strict_accepted": False,
        "json_error": error,
        "finish_reason": "stop",
        "prompt_tokens": raw["usage"]["prompt_tokens"],
        "completion_tokens": raw["usage"]["completion_tokens"],
        "counterfactual_action_count": len(edits),
        "counterfactual_unknown_ids": bad_ids,
        "counterfactual_changed_known_ids": changed_known,
        "counterfactual_exceeds_edit_limit": len(edits) > 15,
    }
print(json.dumps(out, indent=2, sort_keys=True))
