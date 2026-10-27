#!/usr/bin/env python3
"""Reproduce Run295 compiler v2 from the pinned Run294 source. No execution."""
from pathlib import Path
import hashlib,sys

OLD_SHA='8801e6da5c9bf37c353d8378bb334b0aeb53e104239d71bdd53a60bf7df50df3'
NEW_SHA='0efcf451b5d571033b138bddc8f9acdc7d37131017ace9f21636c8c394ad53c3'
OLD="""        try:
            text=new.decode('utf-8',errors='strict')
        except UnicodeDecodeError:
            raise Rejected('INVALID_UTF8') from None
        try:
            ast.parse(text, filename=path)
        except SyntaxError:
            raise Rejected('INVALID_PYTHON_AST') from None
        resulting[path]=new"""
NEW="""        # A Unicode AST parse is NOT a source-file validity check. The CPython
        # source loader honors PEP-263 coding cookies and performs compile-time
        # semantic checks that ast.parse deliberately defers. Never execute.
        try:
            new.decode('utf-8-sig',errors='strict')
        except UnicodeDecodeError:
            raise Rejected('INVALID_UTF8') from None
        try:
            encoding,_ = tokenize.detect_encoding(io.BytesIO(new).readline)
            if codecs.lookup(encoding).name not in ('utf-8','utf-8-sig'):
                raise Rejected('UNSUPPORTED_ENCODING')
        except (SyntaxError, LookupError, UnicodeError):
            raise Rejected('UNSUPPORTED_ENCODING') from None
        try:
            compile(new,filename=path,mode='exec',dont_inherit=True)
        except (SyntaxError,ValueError,UnicodeError,OverflowError,RecursionError):
            raise Rejected('INVALID_PYTHON_BYTECODE') from None
        resulting[path]=new"""

def main(src,dst):
    original=Path(src).read_bytes()
    assert hashlib.sha256(original).hexdigest()==OLD_SHA
    text=original.decode('utf-8')
    assert text.count(OLD)==1
    text=text.replace('import ast\n','import ast\nimport codecs\nimport io\nimport tokenize\n',1)
    text=text.replace(OLD,NEW,1)
    text=text.replace('Scope: UTF-8 Python files, existing regular files only, bounded byte offsets,','Scope: UTF-8 Python files with UTF-8-compatible PEP-263 cookies only, existing regular files, bounded byte offsets,',1)
    data=text.encode('utf-8')
    assert hashlib.sha256(data).hexdigest()==NEW_SHA
    Path(dst).write_bytes(data)

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
