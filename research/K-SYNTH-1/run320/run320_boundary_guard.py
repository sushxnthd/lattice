"""Run320 narrow statement-boundary guard.

Use before inserting replacement text into a larger Python source file.
This rejects bare decorators and other incomplete/multi-statement payloads.
It does NOT prove semantic preservation for arbitrary Python edits.
"""
from __future__ import annotations
import ast

class BoundaryRejected(ValueError):
    pass

def require_single_standalone_statement(text: str) -> None:
    if not isinstance(text, str):
        raise BoundaryRejected('replacement must be text')
    try:
        parsed = ast.parse(text, mode='exec')
    except (SyntaxError, ValueError, UnicodeError, TypeError) as exc:
        raise BoundaryRejected('replacement is not a standalone statement') from exc
    if len(parsed.body) != 1 or not isinstance(parsed.body[0], ast.stmt):
        raise BoundaryRejected('replacement must be exactly one standalone statement')
