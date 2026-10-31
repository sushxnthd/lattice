#!/usr/bin/env python3
"""Run382: strict lossless IR2 transport and legacy delimiter collision.

This is a syntactic encoding contract, NOT a Python semantic soundness proof.
No untrusted Python source is executed.
"""
import json

KEYS = ("epistemic", "handler", "kind", "qualname", "sequence", "statement")
KINDS = ("async", "sync")
EPISTEMIC = ("UNKNOWN", "MAY", "NO_DEPENDENCE")

def validate(f):
    if not isinstance(f, dict) or set(f) != set(KEYS):
        raise ValueError("incorrect fact schema")
    if f["kind"] not in KINDS or f["epistemic"] not in EPISTEMIC:
        raise ValueError("unsupported kind or epistemic value")
    if not isinstance(f["sequence"], list) or not all(isinstance(x, str) for x in f["sequence"]):
        raise ValueError("invalid sequence")
    if any(not isinstance(f[k], str) or not f[k] for k in KEYS if k != "sequence"):
        raise ValueError("invalid text field")
    return {k: f[k] for k in KEYS}

def encode(f):
    f = validate(f)
    out = bytearray(b"IR2")
    for key in KEYS:
        raw = json.dumps(f[key], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        out.extend(str(len(raw)).encode("ascii") + b":" + raw)
    return bytes(out)

def decode(raw):
    if not isinstance(raw, bytes) or not raw.startswith(b"IR2"):
        raise ValueError("invalid magic")
    pos = 3
    values = []
    for _ in KEYS:
        colon = raw.find(b":", pos)
        if colon <= pos or colon - pos > 12 or not raw[pos:colon].isdigit():
            raise ValueError("invalid length prefix")
        length = int(raw[pos:colon])
        pos = colon + 1
        if length > 100000 or pos + length > len(raw):
            raise ValueError("invalid field length")
        values.append(json.loads(raw[pos:pos + length].decode("utf-8")))
        pos += length
    if pos != len(raw):
        raise ValueError("trailing bytes")
    return validate(dict(zip(KEYS, values)))

def legacy_node(f):
    f = validate(f)
    return "|".join(("NODE", f["kind"], f["qualname"], f["handler"], f["statement"], f["epistemic"]))

def collision():
    base = dict(kind="async", epistemic="UNKNOWN", qualname="A", handler="B",
                statement="self._requests.remove(status)",
                sequence=["WAIT", "EXCEPT", "REMOVE", "RAISE"])
    a = {**base, "qualname": "A|B", "handler": "C"}
    b = {**base, "qualname": "A", "handler": "B|C"}
    assert a != b
    assert legacy_node(a) == legacy_node(b)
    assert encode(a) != encode(b)
    assert decode(encode(a)) == a and decode(encode(b)) == b
    return legacy_node(a)

if __name__ == "__main__":
    print("legacy collision:", collision())
