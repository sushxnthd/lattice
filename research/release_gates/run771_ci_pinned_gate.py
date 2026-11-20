"""Pinned-digest release gate: never derive the expected digest from the wheel being checked."""
import argparse
import json
import pathlib
import sys
from bounded_release_gate import verify_bounded

def check(wheel, pinned_digest):
    return verify_bounded(wheel, pinned_digest)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=pathlib.Path)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    try:
        result = check(args.wheel, args.sha256)
    except (OSError, ValueError) as exc:
        result = {"ok": False, "error": type(exc).__name__}
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if result["ok"] else 3)
