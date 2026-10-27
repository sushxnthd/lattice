#!/usr/bin/env python3
"""Trusted historical h11 parser-frontier witness; never imports model output."""
import hashlib,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
assert hashlib.sha256((root/'h11/_receivebuffer.py').read_bytes()).hexdigest()=='8719682225b96f983f71d6c50333f0fadbfa6292a70c8b0de33d45516968a5c8'
assert hashlib.sha256((root/'h11/_readers.py').read_bytes()).hexdigest()=='05c760d59ecfb456d30075c053e2a65559d7c3260f7902339949f98dd6f18777'
sys.path.insert(0,str(root))
from h11._receivebuffer import ReceiveBuffer
from h11._readers import request_line_re
from h11._util import validate

def lines(raw):
    b=ReceiveBuffer();b+=raw
    return b.maybe_extract_lines()

lf=b'GET / HTTP/1.1\nHost: x\n\n'
valid=b'GET / HTTP/1.1\r\nHost: x\r\n\r\n'
extra=b'GET / HTTP/1.1\n\r\nHost: x\r\n\r\n'
assert lines(lf) is None
assert lines(valid)[0]==b'GET / HTTP/1.1'
first=lines(extra)[0]
assert first==b'GET / HTTP/1.1\n'
try:
    validate(request_line_re,first)
except Exception:
    pass
else:
    raise AssertionError('Malformed line unexpectedly accepted by trusted original validator')
assert validate(request_line_re,first[:-1])['method']==b'GET'
print('TRUSTED_WITNESS_OK: LF-only blocked upstream; CRLF valid; embedded bare-LF rejected but stripped line validates')
