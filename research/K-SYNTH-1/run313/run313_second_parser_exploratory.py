#!/usr/bin/env python3
"""Exploratory Run313 second-parser comparison, after historical frozen run.
Trusted stdlib http.client only; no network; not a security exploit demonstration.
"""
import hashlib
import http.client
import io
import json
from pathlib import Path
import sys

class FakeSocket:
    def __init__(self, data):
        self.data=data
    def makefile(self, mode):
        return io.BytesIO(self.data)

sys.path.insert(0,str(Path(__file__).resolve().parent))
# The exact 22 wire streams are in the SHA-pinned original runner, which must
# first be decoded from run313_runner.zlib.b64 as in the CI workflow.
from run313_adversarial_h11 import STREAMS

for name,group,wire in STREAMS:
    response=http.client.HTTPResponse(FakeSocket(wire))
    error=None;status=None;body=None;headers=None
    try:
        response.begin()
        status=response.status
        headers=[(k,v) for k,v in response.getheaders()]
        body=response.read(4096).hex()
    except Exception as exc:
        error={'type':type(exc).__name__,'message':str(exc)[:240]}
    print(json.dumps({'stream':name,'group':group,
                      'wire_sha256':hashlib.sha256(wire).hexdigest(),
                      'status':status,'body_hex':body,'headers':headers,
                      'error':error},sort_keys=True))
