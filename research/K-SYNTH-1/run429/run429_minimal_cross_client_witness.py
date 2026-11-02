#!/usr/bin/env python3
"""Minimal same-request oracle non-identifiability witness, loopback only."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import requests
import urllib3

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        raw = self.raw_requestline.split(b' ')[1].decode('latin-1')
        data = json.dumps({'raw': raw, 'observed': self.path}).encode()
        self.send_response(200)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, *args): pass

if __name__ == '__main__':
    srv = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=srv.serve_forever, daemon=True); thread.start()
    url = f'http://127.0.0.1:{srv.server_port}//v:h'
    try:
        with requests.Session() as session:
            session.trust_env = False
            a = session.get(url, timeout=3).json()
        pool = urllib3.PoolManager(retries=False)
        try:
            b = json.loads(pool.request('GET', url, timeout=urllib3.Timeout(connect=3, read=3)).data)
        finally:
            pool.clear()
    finally:
        srv.shutdown(); srv.server_close(); thread.join(timeout=4)
    assert a == {'raw':'/v:h', 'observed':'/v:h'}, a
    assert b == {'raw':'//v:h', 'observed':'/v:h'}, b
    print(json.dumps({'requests':a, 'urllib3':b, 'server_only_indistinguishable':a['observed']==b['observed']},sort_keys=True))
