"""Bounded trusted-local snapshot publisher: lexical ancestor symlink rejection.

Not a secure publisher for hostile concurrent writers or a power-loss durability
proof. No untrusted code is evaluated or executed by this module.
"""
from __future__ import annotations
import os
from pathlib import Path
from run315_multifile_compiler import PatchRejected
from run315_snapshot_store_hardened import publish as _run315_publish


def _reject_ancestor_symlinks(path: Path) -> None:
    """Reject symlink in *any* existing lexical component of store path.

    This closes a bounded pre-existing-parent-symlink escape. A hostile actor
    with concurrent write access can still replace components after this check.
    """
    if not isinstance(path, Path):
        raise PatchRejected('store must be pathlib.Path')
    absolute = Path(os.path.abspath(os.fspath(path)))
    for component in (*reversed(absolute.parents), absolute):
        if component.is_symlink():
            raise PatchRejected('symlink in store path ancestry')
        if component.exists() and not component.is_dir():
            raise PatchRejected('non-directory store path component')


def publish(store: Path, files: dict[str, bytes], *, fail_before_pointer: bool = False) -> str:
    _reject_ancestor_symlinks(store)
    return _run315_publish(store, files, fail_before_pointer=fail_before_pointer)
