#!/usr/bin/env python3
"""Byte-reversible Python-source view of Run234 semantic facts.

This presents source code verbatim rather than JSON-escaped AST_TARGET strings.
It is an input-presentation control, NOT an unrestricted Python editing UI.
"""
from __future__ import annotations
import io
import json

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()

def emit_record(tag, meta, body):
    return b'# LATTICE ' + tag.encode() + b' ' + canon(dict(meta, utf8_bytes=len(body))) + b'\n' + body + b'\n'

def render(facts):
    parts = [b'# LATTICE PYTHON SOURCE VIEW v1\n']
    for path, item in sorted(facts.items()):
        parts.append(b'# LATTICE FILE ' + canon({
            'path': path, 'file_sha256': item['file_sha256'],
            'full_source_bytes': item['full_source_bytes']}) + b'\n')
        parts.append(emit_record('CONTEXT', {}, item['source_excerpt'].encode()))
        for target in item['targets']:
            meta = {k: v for k, v in target.items() if k != 'old_text'}
            parts.append(emit_record('TARGET', meta, target['old_text'].encode()))
        parts.append(b'# LATTICE END_FILE\n')
    return b''.join(parts)

def parse(raw):
    stream = io.BytesIO(raw)
    if stream.readline() != b'# LATTICE PYTHON SOURCE VIEW v1\n':
        raise ValueError('bad view version')
    out = {}
    path = item = None
    while (line := stream.readline()):
        if line.startswith(b'# LATTICE FILE '):
            if path is not None:
                raise ValueError('nested file')
            meta = json.loads(line[len(b'# LATTICE FILE '):])
            if set(meta) != {'path', 'file_sha256', 'full_source_bytes'}:
                raise ValueError('bad file metadata')
            path = meta.pop('path')
            item = dict(meta, source_excerpt=None, targets=[])
            if path in out:
                raise ValueError('duplicate file')
        elif line.startswith((b'# LATTICE CONTEXT ', b'# LATTICE TARGET ')):
            if path is None:
                raise ValueError('record outside file')
            tag = 'CONTEXT' if line.startswith(b'# LATTICE CONTEXT ') else 'TARGET'
            meta = json.loads(line[len(b'# LATTICE ' + tag.encode() + b' '):])
            n = meta.pop('utf8_bytes')
            if type(n) != int or n < 0 or n > 5_000_000:
                raise ValueError('bad length')
            body = stream.read(n)
            if len(body) != n or stream.read(1) != b'\n':
                raise ValueError('truncated record')
            content = body.decode('utf-8')
            if tag == 'CONTEXT':
                if item['source_excerpt'] is not None or meta:
                    raise ValueError('bad context')
                item['source_excerpt'] = content
            else:
                if set(meta) != {'target_id', 'kind', 'name', 'start_line', 'end_line'}:
                    raise ValueError('bad target metadata')
                item['targets'].append(dict(meta, old_text=content))
        elif line == b'# LATTICE END_FILE\n':
            if path is None or item['source_excerpt'] is None:
                raise ValueError('bad end file')
            out[path] = item
            path = item = None
        else:
            raise ValueError('unknown view line')
    if path is not None:
        raise ValueError('unterminated file')
    return out
