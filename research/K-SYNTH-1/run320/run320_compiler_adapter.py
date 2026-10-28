"""Run320 production-oriented boundary adapter for the existing Run317 editor.

Preserves Run317 Action identity and its source/AST SHA, authority, overlap,
whole-snapshot and syntax validation. Adds a fail-closed statement boundary gate.
Does not claim general AST semantic congruence or untrusted-code safety.
"""
from __future__ import annotations
from pathlib import Path
import sys
_HERE = Path(__file__).resolve().parent
for _sibling in ('run315', 'run317'):
    _dir = _HERE.parent / _sibling
    if _dir.is_dir() and str(_dir) not in sys.path:
        sys.path.insert(0, str(_dir))
from run315_multifile_compiler import PatchRejected
from run317_structural_compiler import Action, compile_structural
from run320_boundary_guard import BoundaryRejected, require_single_standalone_statement

def compile_boundary_checked(sources, actions, *, allowed_paths):
    """Return a complete edited snapshot or reject without mutating inputs."""
    for action in actions:
        if not isinstance(action, Action):
            raise PatchRejected('invalid action')
        if action.operation in ('replace_stmt', 'insert_before'):
            try:
                require_single_standalone_statement(action.replacement)
            except BoundaryRejected as exc:
                raise PatchRejected(str(exc)) from exc
    return compile_structural(sources, actions, allowed_paths=allowed_paths)
