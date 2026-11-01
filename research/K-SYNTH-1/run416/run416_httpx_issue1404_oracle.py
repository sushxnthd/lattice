#!/usr/bin/env python3
"""Prospectively specified httpx 0.16.1 issue #1404 local HTTP oracle.

Freeze before inspecting any historical fixing PR. Run only in an isolated
Python 3.9 environment containing the exact pinned httpx source checkout.
Do not score as a qualified repair until source attestation, public/heldout
separation, and four-arm reference component ablations all pass.
"""
from __future__ import annotations
import argparse,asyncio,json,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        redirects={'/pub-302':(302,'/pub-final'),
                   '/held-307':(307,'/held-final'),
                   '/held-hop1':(302,'/held-hop2'),
                   '/held-hop2':(307,'/held-final2')}
        if self.path in redirects:
            status,location=redirects[self.path]
            self.send_response(status)
            self.send_header('Location',location)
            self.end_headers();return
        payload=json.dumps({'path':self.path,'cookie':self.headers.get('Cookie'),
                            'marker':self.headers.get('X-Run416-Marker')},sort_keys=True).encode()
        self.send_response(200);self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)

def public_cases(base):
    import httpx
    with httpx.Client() as client:
        a=client.get(base+'/pub-302',cookies={'sid':'public-sync'},allow_redirects=True)
        b=client.get(base+'/direct',cookies={'sid':'direct-control'},allow_redirects=True)
        c=client.get(base+'/direct',allow_redirects=True)
    return {'public_sync_302':a.json(),'control_direct_cookie':b.json(),
            'control_no_cookie':c.json()}

async def public_async_case(base):
    import httpx
    async with httpx.AsyncClient() as client:
        r=await client.get(base+'/pub-302',cookies={'sid':'public-async'},allow_redirects=True)
        return {'public_async_302':r.json()}

def heldout_cases(base):
    import httpx
    with httpx.Client(headers={'X-Run416-Marker':'heldout'}) as client:
        r=client.get(base+'/held-307',cookies={'sid':'held-sync'},allow_redirects=True)
        return {'heldout_sync_307':r.json()}

async def heldout_async_case(base):
    import httpx
    async with httpx.AsyncClient(headers={'X-Run416-Marker':'heldout-async'}) as client:
        r=await client.get(base+'/held-hop1',cookies={'sid':'held-async'},allow_redirects=True)
        return {'heldout_async_two_hops':r.json()}

def classify(results):
    expectations={'public_sync_302':('/pub-final','sid=public-sync',None),
                  'public_async_302':('/pub-final','sid=public-async',None),
                  'heldout_sync_307':('/held-final','sid=held-sync','heldout'),
                  'heldout_async_two_hops':('/held-final2','sid=held-async','heldout-async'),
                  'control_direct_cookie':('/direct','sid=direct-control',None),
                  'control_no_cookie':('/direct',None,None)}
    return {key:results.get(key)=={'path':path,'cookie':cookie,'marker':marker}
            for key,(path,cookie,marker) in expectations.items()}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
    try:
        base='http://127.0.0.1:'+str(server.server_address[1])
        outcomes={**public_cases(base),**asyncio.run(public_async_case(base)),
                  **heldout_cases(base),**asyncio.run(heldout_async_case(base))}
        results={'outcomes':outcomes,'checks':classify(outcomes)}
        with open(args.output,'w') as f:json.dump(results,f,sort_keys=True,indent=2)
        print(json.dumps(results['checks'],sort_keys=True))
    finally:
        server.shutdown();server.server_close();t.join(timeout=3)

if __name__=='__main__':main()
