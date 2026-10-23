"""Shared exact-preimage anchored edits, independent of presentation order.

Opt-in protocol; never silently reinterprets a line-addressed experiment.
"""
from __future__ import annotations
from typing import Mapping
from multifile_editor import compile_patch, PatchRejected, sha256, CompiledPatch


def compile_anchored_patch(snapshot: Mapping[str, bytes], output: object,
                           allowed_paths: set[str], *, max_edits: int = 16,
                           max_replacement_bytes: int = 32768) -> CompiledPatch:
    """Resolve only unique nonempty exact line-aligned preimages in SHA-pinned files."""
    if not isinstance(output, dict) or set(output) != {'edits'}:
        raise PatchRejected('wrong envelope')
    edits = output['edits']
    if not isinstance(edits, list) or not 1 <= len(edits) <= max_edits:
        raise PatchRejected('invalid edit count')
    normalized = []
    for i, edit in enumerate(edits):
        if not isinstance(edit, dict) or set(edit) != {'path','file_sha256','old_text','replacement'}:
            raise PatchRejected(f'edit {i}: invalid anchored schema')
        path, old = edit['path'], edit['old_text']
        if not isinstance(path, str) or path not in allowed_paths or path not in snapshot:
            raise PatchRejected(f'edit {i}: unauthorized path')
        if not isinstance(old, str) or not old:
            raise PatchRejected(f'edit {i}: empty or invalid anchor')
        if not isinstance(edit['file_sha256'], str) or edit['file_sha256'] != sha256(snapshot[path]):
            raise PatchRejected(f'edit {i}: stale file hash')
        try:
            lines = snapshot[path].decode('utf-8').splitlines(keepends=True)
        except UnicodeError as exc:
            raise PatchRejected(f'edit {i}: non-UTF8 source') from exc
        anchor_lines = old.splitlines(keepends=True)
        if ''.join(anchor_lines) != old or not anchor_lines:
            raise PatchRejected(f'edit {i}: invalid anchor')
        matches = [idx for idx in range(len(lines))
                   if lines[idx:idx+len(anchor_lines)] == anchor_lines]
        if len(matches) != 1:
            raise PatchRejected(f'edit {i}: anchor must occur exactly once; found {len(matches)}')
        start = matches[0]+1
        normalized.append({**edit, 'start_line':start,
                           'end_line':start+len(anchor_lines)-1})
    return compile_patch(snapshot, {'edits':normalized}, allowed_paths,
                         max_edits=max_edits,
                         max_replacement_bytes=max_replacement_bytes)


def posthoc_readdress_line_patch(snapshot: Mapping[str,bytes], output: object,
                                  allowed_paths: set[str]) -> CompiledPatch:
    """Diagnostic ONLY: changes the original addressing protocol after inference."""
    if not isinstance(output,dict) or set(output) != {'edits'}:
        raise PatchRejected('invalid envelope')
    anchored=[]
    for edit in output['edits']:
        if not isinstance(edit,dict) or set(edit) != {'path','file_sha256','start_line','end_line','old_text','replacement'}:
            raise PatchRejected('invalid original schema')
        anchored.append({key:edit[key] for key in ('path','file_sha256','old_text','replacement')})
    return compile_anchored_patch(snapshot,{'edits':anchored},allowed_paths)
