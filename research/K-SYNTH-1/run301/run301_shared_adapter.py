#!/usr/bin/env python3
"""Prospective shared exact-preimage adapter for IR/Python presentation pilots.

No model-generated code is executed. This tests presentation, not intrinsic
semantic editing-language superiority.
"""
import hashlib
from pathlib import Path
import run295_compiler_v2 as compiler

ALLOWED=frozenset({'h11/_readers.py','h11/_connection.py',
                   'h11/_receivebuffer.py','h11/_abnf.py'})
def digest(b):return hashlib.sha256(b).hexdigest()

def strip_one_fence(text):
    if not isinstance(text,str):raise compiler.Rejected('INVALID_JSON')
    if text.startswith('```json\n') and text.endswith('\n```'):
        return text[8:-4]
    if text.startswith('```\n') and text.endswith('\n```'):
        return text[4:-4]
    return text

def to_views(text,root):
    doc=compiler.parse_json(strip_one_fence(text))
    compiler.exact_keys(doc,{'edits'})
    if not isinstance(doc['edits'],list) or not 1<=len(doc['edits'])<=3:
        raise compiler.Rejected('EDIT_COUNT')
    out=[]
    for item in doc['edits']:
        compiler.exact_keys(item,{'path','old','new'})
        path,old,new=item['path'],item['old'],item['new']
        if type(path) is not str or path not in ALLOWED:
            raise compiler.Rejected('EDIT_AUTHORITY')
        if type(old) is not str or not old or type(new) is not str:
            raise compiler.Rejected('EDIT_TYPE')
        data=(Path(root)/path).read_bytes()
        oldb=old.encode('utf-8',errors='strict')
        if data.count(oldb)!=1:raise compiler.Rejected('OLD_NOT_UNIQUE')
        start=data.index(oldb)
        out.append({'path':path,'start_byte':start,'end_byte':start+len(oldb),
                    'expected_file_sha256':digest(data),
                    'expected_span_sha256':digest(oldb),'replacement_utf8':new})
    return compiler.encode_views(out)
