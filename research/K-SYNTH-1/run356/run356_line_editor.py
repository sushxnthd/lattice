"""Run356: pinned, atomic, line-addressed two-file Python source editor.

All content is treated as data. Candidate source is parsed, never executed.
This is a *new* prospective grammar and MUST NOT rescore frozen Run355.
"""
from __future__ import annotations
import ast
import hashlib

PINS = {
    'httpcore/_sync/http11.py': 'e108f88b124043b05258f6d98363119b79f92d88',
    'httpcore/_async/http11.py': 'a5eb480840dd4eae73bc8285c9d374a09a0bd44c',
}

class Reject(ValueError):
    pass

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob(source: str) -> str:
    raw = source.encode('utf-8')
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def compile_transaction(sources: dict[str, str], actions: list[dict],
                        *, max_per_file: int = 12, max_total: int = 24,
                        pins: dict[str, str] | None = None) -> dict[str, str]:
    """Atomic edit: 1-based inclusive [start_line,end_line], or insertion [s,s-1].

    Authority is the pinned *entire original file*, not an untrusted preimage.
    Overlap checks use original coordinates; identical insertion boundaries reject.
    Return a new mapping only if every staged file parses as Python.
    """
    pins = PINS if pins is None else pins
    if not isinstance(sources, dict) or set(sources) != set(pins):
        raise Reject('SOURCE_SET')
    if any(not isinstance(s, str) or git_blob(s) != pins[p] for p, s in sources.items()):
        raise Reject('SOURCE_PIN_MISMATCH')
    if not isinstance(actions, list) or not 1 <= len(actions) <= max_total:
        raise Reject('ACTION_COUNT')
    counts = {p: 0 for p in pins}
    intervals: dict[str, list[tuple[int, int]]] = {p: [] for p in pins}
    grouped: dict[str, list[tuple[int, int, str]]] = {p: [] for p in pins}
    for action in actions:
        if not isinstance(action, dict) or set(action) != {'path', 'start_line', 'end_line', 'new'}:
            raise Reject('ACTION_SCHEMA')
        p, start, end, new = (action[k] for k in ('path', 'start_line', 'end_line', 'new'))
        if p not in pins or type(start) is not int or type(end) is not int or not isinstance(new, str):
            raise Reject('ACTION_TYPE_OR_AUTHORITY')
        if len(new.encode()) > 16000 or (new and not new.endswith('\n')):
            raise Reject('NEW_TEXT_INVALID')
        src_lines = sources[p].splitlines(keepends=True)
        if not (1 <= start <= len(src_lines)+1 and start-1 <= end <= len(src_lines)):
            raise Reject('LINE_RANGE')
        counts[p] += 1
        if counts[p] > max_per_file:
            raise Reject('PER_FILE_LIMIT')
        l, r = start-1, end
        if (l == r and not new) or ''.join(src_lines[l:r]) == new:
            raise Reject('NOOP_ACTION')
        for lo, hi in intervals[p]:
            if l == r == lo == hi or (l < hi and lo < r) or (lo == hi and l <= lo < r) or (l == r and lo <= l < hi):
                raise Reject('OVERLAP')
        intervals[p].append((l, r))
        grouped[p].append((l, r, new))
    staged = {}
    for p, source in sources.items():
        src_lines = source.splitlines(keepends=True)
        for l, r, new in sorted(grouped[p], key=lambda t: (t[0], t[1]), reverse=True):
            src_lines[l:r] = [new]
        candidate = ''.join(src_lines)
        if candidate != source:
            try:
                ast.parse(candidate, filename=p)
            except (SyntaxError, ValueError) as exc:
                raise Reject('PYTHON_SYNTAX') from exc
        staged[p] = candidate
    if all(staged[p] == sources[p] for p in pins):
        raise Reject('NO_EFFECT')
    return staged

def reference_expressibility(sources: dict[str, str], actions: list[dict],
                             expected_reference_blobs: dict[str, str]):
    staged = compile_transaction(sources, actions)
    result = {p: {'reference_blob': git_blob(staged[p]),
                  'expected_blob': expected_reference_blobs[p],
                  'match': git_blob(staged[p]) == expected_reference_blobs[p]}
              for p in staged}
    assert all(v['match'] for v in result.values())
    return result
