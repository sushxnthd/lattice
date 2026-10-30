#!/usr/bin/env python3
"""Frozen HTTPX #1532 public API oracle. Run only in isolated no-network container."""
import json
import os
import sys

# Frozen before historical 2x2 execution. Reference-informed, not blind.
CASES = [
 ("P01","public","url","/path/to/somewhere","/somewhere-else","/somewhere-else"),
 ("P02","public","url","/path/to/somewhere","somewhere-else","/path/to/somewhere-else"),
 ("P03","public","client","https://example.org/some/path","/sub:path","https://example.org/some/path/sub:path"),
 ("H01","heldout","url","/path/to/somewhere","../somewhere-else","/path/somewhere-else"),
 ("H02","heldout","url","/path/to/somewhere","../../somewhere-else","/somewhere-else"),
 ("H03","heldout","client","https://example.org/some/path","/testing:123","https://example.org/some/path/testing:123"),
 ("C01","control","url","https://example.org/a/b","../c","https://example.org/c"),
 ("C02","control","url","https://example.org/a/b","/c","https://example.org/c"),
 ("C03","control","client","https://example.org/a/b","c","https://example.org/a/b/c"),
 ("C04","control","client","https://example.org/a/b","/c","https://example.org/a/b/c"),
 ("C05","control","client","https://example.org/a/b","https://other.org/x","https://other.org/x"),
 ("C06","control","url","https://example.org/a/b","https://other.org/x","https://other.org/x"),
 ("C07","control","url","https://example.org/a/b","#frag","https://example.org/a/b#frag"),
]
def run():
 import httpx
 rows=[]
 for ident,group,kind,base,arg,expected in CASES:
  actual=None;error=None
  try:
   if kind=="url":actual=str(httpx.URL(base).join(arg))
   else:
    with httpx.Client(base_url=base) as client:
     actual=str(client.build_request("GET",arg).url)
  except Exception as exc:error=type(exc).__name__+": "+str(exc)[:200]
  rows.append(dict(id=ident,group=group,kind=kind,base=base,arg=arg,expected=expected,actual=actual,error=error,passed=(error is None and actual==expected)))
 return dict(schema="lattice.run368.oracle.v1",arm=os.environ.get("LATTICE_ARM","UNKNOWN"),python=sys.version.split()[0],httpx_version=getattr(httpx,"__version__",None),httpx_file=httpx.__file__,rows=rows)
if __name__=="__main__":
 try:print(json.dumps(run(),sort_keys=True,ensure_ascii=False))
 except BaseException as exc:
  print(json.dumps(dict(schema="lattice.run368.oracle.v1",arm=os.environ.get("LATTICE_ARM","UNKNOWN"),fatal=type(exc).__name__+": "+str(exc)[:200]),sort_keys=True))
