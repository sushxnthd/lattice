"""Run200 minimal counterexample: protected file bytes do not imply protected output."""
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile

def digest(data):
    return hashlib.sha256(data).hexdigest()

def demonstrate():
    a = b"def f():\n    return 0\n"
    b = b"from a import f\n\ndef protected():\n    return f()\n"
    replacement = b"def f():\n    return 1\n"
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "a.py").write_bytes(a)
        (root / "b.py").write_bytes(b)
        before = subprocess.check_output(
            [sys.executable, "-c", "import b;print(b.protected())"],
            cwd=root, text=True).strip()
        (root / "a.py").write_bytes(replacement)
        after = subprocess.check_output(
            [sys.executable, "-c", "import b;print(b.protected())"],
            cwd=root, text=True).strip()
        assert digest((root / "b.py").read_bytes()) == digest(b)
    assert before == "0" and after == "1"
    return {"before": before, "after": after, "protected_file_sha256": digest(b),
            "conclusion": "File-level frame is not semantic-output noninterference."}

if __name__ == "__main__":
    import json
    print(json.dumps(demonstrate(), indent=2))
