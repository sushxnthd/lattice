"""Fail-closed wheel structural integrity CLI; does not authenticate digest source."""
import argparse
import pathlib
import sys
from wheel_integrity import Unknown, inspect

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wheel', type=pathlib.Path)
    parser.add_argument('approved_sha256')
    args = parser.parse_args()
    try:
        result = inspect(args.wheel, args.approved_sha256)
    except (Unknown, OSError, ValueError) as exc:
        print(f'UNKNOWN: {exc}', file=sys.stderr)
        return 2
    print(f"VERIFIED: {result['sha256']} entries={result['entries']}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
