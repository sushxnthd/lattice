"""Compare independently produced wheel bytes; equality is not release approval."""
import argparse
import hashlib
import json
from pathlib import Path


def compare(first: Path, second: Path) -> dict:
    if first.resolve() == second.resolve():
        raise ValueError('independent paths required')
    if not first.is_file() or not second.is_file():
        raise ValueError('both wheel files required')
    if first.suffix != '.whl' or second.suffix != '.whl':
        raise ValueError('wheel files required')
    if first.name != second.name:
        raise ValueError('wheel filenames differ')
    def digest(path):
        h = hashlib.sha256()
        with path.open('rb') as f:
            for block in iter(lambda: f.read(1024 * 1024), b''):
                h.update(block)
        return h.hexdigest()
    a, b = digest(first), digest(second)
    return {'status': 'MATCH_UNAPPROVED' if a == b else 'UNKNOWN',
            'wheel': first.name, 'first_sha256': a, 'second_sha256': b,
            'approval': False, 'identical_bytes': a == b}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('first', type=Path)
    parser.add_argument('second', type=Path)
    args = parser.parse_args()
    try:
        result = compare(args.first, args.second)
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'UNKNOWN', 'approval': False, 'error': str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0 if result['identical_bytes'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
