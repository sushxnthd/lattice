"""Fail-closed wheel digest verifier; independent expected digest is mandatory."""
import argparse
import hashlib
import pathlib
import re
import sys

def verify(path: pathlib.Path, expected: str) -> str:
    if not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError('UNKNOWN: expected SHA-256 must be 64 lowercase hex characters')
    if not path.is_file() or path.suffix != '.whl':
        raise ValueError('UNKNOWN: wheel missing or wrong extension')
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if actual != expected:
        raise ValueError('UNKNOWN: wheel SHA-256 differs from independent approved pin')
    return actual

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('wheel', type=pathlib.Path)
    parser.add_argument('approved_sha256')
    args = parser.parse_args()
    try:
        print(verify(args.wheel, args.approved_sha256))
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)

if __name__ == '__main__':
    main()
