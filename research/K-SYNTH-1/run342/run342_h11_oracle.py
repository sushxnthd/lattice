#!/usr/bin/env python3
"""Run342 prospectively frozen h11 public API oracle.

This file contains only externally specified behavior and is intentionally
independent of the historical PR implementation. Never modify it in response
to reference outcomes. Run in an isolated checkout via PYTHONPATH.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

BASE = '522b00470b5776dda2dc7e98ff778eb1e418e6ad'
REF = 'a1197d68630bc37a941b516c7cc74833460fc97c'
PR = 'https://github.com/python-hyper/h11/pull/115'


def ev_response(status, headers):
    return {'event':'Response','status':status,'headers':[[a.lower(),b] for a,b in headers]}

def ev_data(data):
    return {'event':'Data','hex':data.hex()}

EOM = {'event':'EndOfMessage','headers':[]}
NEED = {'event':'NEED_DATA'}
ERR = {'event':'ERROR','class':'RemoteProtocolError'}

CASES = [
    {'id':'T1_lf_content_length','group':'target',
     'chunks':[b'HTTP/1.1 200 OK\nContent-Length: 5\nX-Test: yes\n\nhello'],
     'expected':[ev_response(200,[('content-length','5'),('x-test','yes')]),ev_data(b'hello'),EOM]},
    {'id':'T2_lf_no_content','group':'target',
     'chunks':[b'HTTP/1.1 204 No Content\n\n'],
     'expected':[ev_response(204,[]),EOM]},
    {'id':'T3_lf_header_chunked_body','group':'target',
     'chunks':[b'HTTP/1.1 200 OK\nTransfer-Encoding: chunked\n\n5\r\nhello\r\n0\r\n\r\n'],
     'expected':[ev_response(200,[('transfer-encoding','chunked')]),ev_data(b'hello'),EOM]},
    {'id':'T4_lf_incremental_boundary','group':'target',
     'chunks':[b'HTTP/1.1 200 OK\nContent-Length: 5\n',b'\nhello'],
     'expected':[NEED,ev_response(200,[('content-length','5')]),ev_data(b'hello'),EOM]},
    {'id':'C1_crlf_content_length','group':'control',
     'chunks':[b'HTTP/1.1 200 OK\r\nContent-Length: 5\r\nX-Test: yes\r\n\r\nhello'],
     'expected':[ev_response(200,[('content-length','5'),('x-test','yes')]),ev_data(b'hello'),EOM]},
    {'id':'C2_crlf_no_content','group':'control',
     'chunks':[b'HTTP/1.1 204 No Content\r\n\r\n'],
     'expected':[ev_response(204,[]),EOM]},
    {'id':'C3_crlf_chunked','group':'control',
     'chunks':[b'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nhello\r\n0\r\n\r\n'],
     'expected':[ev_response(200,[('transfer-encoding','chunked')]),ev_data(b'hello'),EOM]},
    {'id':'C4_crlf_incremental_boundary','group':'control',
     'chunks':[b'HTTP/1.1 200 OK\r\nContent-Length: 5\r\n',b'\r\nhello'],
     'expected':[NEED,ev_response(200,[('content-length','5')]),ev_data(b'hello'),EOM]},
    {'id':'C5_invalid_status_line','group':'control',
     'chunks':[b'HTTP/1.1 abc OK\r\n\r\n'],
     'expected':[ERR]},
    {'id':'C6_invalid_header_field','group':'control',
     'chunks':[b'HTTP/1.1 200 OK\r\nBadHeader\r\n\r\n'],
     'expected':[ERR]},
]


def normalize(event, h11):
    if event is h11.NEED_DATA:
        return NEED
    name = type(event).__name__
    if name in ('Response','InformationalResponse'):
        return {'event':name,'status':event.status_code,
                'headers':[[bytes(a).decode('ascii'),bytes(b).decode('ascii')] for a,b in event.headers]}
    if name == 'Data':
        return {'event':'Data','hex':bytes(event.data).hex()}
    if name == 'EndOfMessage':
        return {'event':'EndOfMessage',
                'headers':[[bytes(a).decode('ascii'),bytes(b).decode('ascii')] for a,b in event.headers]}
    return {'event':name}


def execute_case(case, h11):
    c=h11.Connection(h11.CLIENT)
    c.send(h11.Request(method='GET',target='/',headers=[('host','example.test')]))
    c.send(h11.EndOfMessage())
    events=[]; exception=None
    for part in case['chunks']:
        try:
            c.receive_data(part)
            for _ in range(16):
                item=c.next_event()
                e=normalize(item,h11)
                events.append(e)
                if item is h11.NEED_DATA or e['event']=='EndOfMessage':
                    break
            else:
                events.append({'event':'LIMIT_EXCEEDED'})
                break
        except Exception as exc:
            exception={'class':type(exc).__name__,'message':str(exc)}
            events.append({'event':'ERROR','class':type(exc).__name__})
            break
    return {'id':case['id'],'group':case['group'],'input_chunks_hex':[x.hex() for x in case['chunks']],
            'expected':case['expected'],'got':events,'ok':events==case['expected'],
            'exception':exception}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--arm',required=True,choices=['base_base','ref_A','ref_B','ref_ref','abi_only'])
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    import h11
    records=[execute_case(c,h11) for c in CASES]
    out={'scope':'HISTORICAL_PINNED','pr':PR,'base':BASE,'ref':REF,'arm':args.arm,
         'h11_import':str(Path(h11.__file__).resolve()),
         'oracle_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'records':records,
         'targets':sum(x['ok'] for x in records if x['group']=='target'),
         'controls':sum(x['ok'] for x in records if x['group']=='control')}
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'arm':args.arm,'targets':out['targets'],'controls':out['controls'],
                      'failures':[r['id'] for r in records if not r['ok']]},sort_keys=True))
    if any('/site-packages/' in out['h11_import'] for _ in [0]):
        print('WARNING: installed h11 used; this is a local scaffold, not historical qualification',file=sys.stderr)

if __name__=='__main__':main()
