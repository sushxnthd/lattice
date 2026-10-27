#!/usr/bin/env python3
"""K-SYNTH-1: shared untrusted-output-to-isolated-snapshot compiler.

This compiler does NOT execute candidate code.  It never modifies the input
repository.  Both representations normalize to exactly the same canonical edit
records; there is no claim that either representation is better for a model.

Scope: UTF-8 Python files, existing regular files only, bounded byte offsets,
whole-file SHA-256 and replaced-span SHA-256. No deletes/renames/new files.
No concurrent attacker modifying the snapshot root while compiling. A returned
stage is a complete validated copy, but not an OS-level atomic directory swap.
"""
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile

MAX_OUTPUT = 2_000_000
MAX_EDITS = 64
MAX_SOURCE_FILES = 500
MAX_SOURCE_BYTES = 10_000_000

class Rejected(ValueError):
    def __init__(self, code):
        super().__init__(code)
        self.code = code

def sha(data):
    return hashlib.sha256(data).hexdigest()

def strict_object(pairs):
    d = {}
    for k,v in pairs:
        if k in d:
            raise Rejected('DUPLICATE_JSON_KEY')
        d[k] = v
    return d

def parse_json(raw):
    if not isinstance(raw, str) or len(raw.encode('utf-8')) > MAX_OUTPUT:
        raise Rejected('OUTPUT_SIZE')
    try:
        return json.loads(raw, object_pairs_hook=strict_object,
                          parse_constant=lambda _: (_ for _ in ()).throw(Rejected('NONFINITE_JSON')))
    except Rejected:
        raise
    except (ValueError, TypeError):
        raise Rejected('INVALID_JSON') from None

def exact_keys(d, expected):
    if not isinstance(d, dict) or set(d) != set(expected):
        raise Rejected('SCHEMA')

def canonicalize(raw):
    doc = parse_json(raw)
    exact_keys(doc, {'representation','edits','assumptions'})
    if doc['assumptions'] != {'runtime_binding':'UNKNOWN','edit_authority':'EXACT_BYTE_SPANS'}:
        raise Rejected('ASSUMPTIONS')
    kind = doc['representation']
    if kind not in ('SEMANTIC_IR','PYTHON_AST_ACTIONS'):
        raise Rejected('REPRESENTATION')
    edits = doc['edits']
    if not isinstance(edits,list) or not 1 <= len(edits) <= MAX_EDITS:
        raise Rejected('EDIT_COUNT')
    canon = []
    for e in edits:
        if kind == 'SEMANTIC_IR':
            exact_keys(e, {'path','start_byte','end_byte','expected_file_sha256','expected_span_sha256','replacement_utf8'})
            v = dict(e)
        else:
            exact_keys(e, {'op','file','byte_interval','file_sha256','span_sha256','text'})
            if e['op'] != 'replace_span' or not isinstance(e['byte_interval'],list) or len(e['byte_interval']) != 2:
                raise Rejected('SCHEMA')
            v = {'path':e['file'],'start_byte':e['byte_interval'][0],
                 'end_byte':e['byte_interval'][1], 'expected_file_sha256':e['file_sha256'],
                 'expected_span_sha256':e['span_sha256'],'replacement_utf8':e['text']}
        p = v['path']
        if not isinstance(p,str) or not p or '\\' in p or '\x00' in p:
            raise Rejected('PATH')
        pp = PurePosixPath(p)
        if pp.is_absolute() or any(x in ('..','.') for x in p.split('/')) or '//' in p or pp.suffix != '.py':
            raise Rejected('PATH')
        if type(v['start_byte']) is not int or type(v['end_byte']) is not int or v['start_byte'] < 0 or v['end_byte'] < v['start_byte']:
            raise Rejected('OFFSET')
        if not all(isinstance(v[k],str) and len(v[k])==64 and all(c in '0123456789abcdef' for c in v[k])
                   for k in ('expected_file_sha256','expected_span_sha256')):
            raise Rejected('SHA_FORMAT')
        if not isinstance(v['replacement_utf8'],str):
            raise Rejected('REPLACEMENT')
        try:
            v['replacement_utf8'].encode('utf-8',errors='strict')
        except UnicodeEncodeError:
            raise Rejected('REPLACEMENT') from None
        canon.append(v)
    canon.sort(key=lambda x:(x['path'],x['start_byte'],x['end_byte']))
    last = {}
    for v in canon:
        p = v['path']
        if p in last and v['start_byte'] < last[p]:
            raise Rejected('OVERLAPPING_SPANS')
        if p in last and v['start_byte'] == last[p] and v['start_byte'] == v['end_byte']:
            raise Rejected('AMBIGUOUS_INSERTIONS')
        last[p] = v['end_byte']
    return canon

def verify_snapshot(root):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise Rejected('ROOT')
    count = total = 0
    for here, dirs, files in os.walk(root, followlinks=False):
        for d in dirs:
            if (Path(here)/d).is_symlink():
                raise Rejected('SYMLINK')
        for f in files:
            p = Path(here)/f
            if p.is_symlink() or not p.is_file():
                raise Rejected('SYMLINK')
            count += 1
            total += p.stat().st_size
            if count > MAX_SOURCE_FILES or total > MAX_SOURCE_BYTES:
                raise Rejected('SNAPSHOT_SIZE')
    return root

def compile_to_isolated_stage(root, raw, staging_parent):
    canon = canonicalize(raw)
    root = verify_snapshot(root)
    # Validate every edit and every resulting Python module BEFORE exposing a stage.
    grouped = {}
    for e in canon:
        grouped.setdefault(e['path'],[]).append(e)
    resulting = {}
    for path, edits in grouped.items():
        src = root / path
        if not src.is_file() or src.is_symlink():
            raise Rejected('MISSING_OR_SYMLINK')
        # Intermediate symlinks forbidden, including a directory ancestor.
        cur = root
        for part in PurePosixPath(path).parts:
            cur = cur / part
            if cur.is_symlink():
                raise Rejected('SYMLINK')
        data = src.read_bytes()
        for e in edits:
            if sha(data) != e['expected_file_sha256']:
                raise Rejected('STALE_FILE_SHA')
            a,b=e['start_byte'],e['end_byte']
            if b > len(data):
                raise Rejected('OUT_OF_BOUNDS')
            if sha(data[a:b]) != e['expected_span_sha256']:
                raise Rejected('SPAN_SHA')
        new = data
        for e in reversed(edits):
            a,b=e['start_byte'],e['end_byte']
            new=new[:a]+e['replacement_utf8'].encode('utf-8')+new[b:]
        try:
            text=new.decode('utf-8',errors='strict')
        except UnicodeDecodeError:
            raise Rejected('INVALID_UTF8') from None
        try:
            ast.parse(text, filename=path)
        except SyntaxError:
            raise Rejected('INVALID_PYTHON_AST') from None
        resulting[path]=new
    parent = Path(staging_parent)
    parent.mkdir(parents=True,exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='ksynth1-stage-',dir=parent))
    try:
        shutil.copytree(root,stage,dirs_exist_ok=True,symlinks=False)
        for path,data in resulting.items():
            (stage/path).write_bytes(data)
        # Verify stage and original SHA independently after copying.
        for path,data in resulting.items():
            if sha((stage/path).read_bytes()) != sha(data):
                raise Rejected('STAGE_MISMATCH')
        return {'stage':str(stage),'edits':len(canon),
                'files':{k:sha(v) for k,v in sorted(resulting.items())},
                'canonical_sha256':sha(json.dumps(canon,sort_keys=True,separators=(',',':')).encode())}
    except Exception:
        shutil.rmtree(stage,ignore_errors=True)
        raise

def encode_views(edits):
    assumptions={'runtime_binding':'UNKNOWN','edit_authority':'EXACT_BYTE_SPANS'}
    ir={'representation':'SEMANTIC_IR','assumptions':assumptions,'edits':edits}
    ordinary={'representation':'PYTHON_AST_ACTIONS','assumptions':assumptions,'edits':[
        {'op':'replace_span','file':e['path'],'byte_interval':[e['start_byte'],e['end_byte']],
         'file_sha256':e['expected_file_sha256'],'span_sha256':e['expected_span_sha256'],
         'text':e['replacement_utf8']} for e in edits]}
    return json.dumps(ir,ensure_ascii=False,sort_keys=True),json.dumps(ordinary,ensure_ascii=False,sort_keys=True)
