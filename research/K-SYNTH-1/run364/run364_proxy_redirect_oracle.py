#!/usr/bin/env python3
"""Prospective public-API oracle: urllib3 PR #5126, proxy redirect origin.

Derived from public PR *description*, without inspecting the reference patch.
Only loopback sockets; no external network. Each case runs a fresh HTTP proxy.
"""
from __future__ import annotations
import contextlib
import http.server
import json
import threading
import urllib3
from urllib3.util.retry import Retry

class _Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *args): pass
    def do_GET(self):
        self.server.observations.append({
            'target': self.path,
            'host': self.headers.get('Host'),
            'authorization': self.headers.get('Authorization'),
            'cookie': self.headers.get('Cookie'),
            'keep': self.headers.get('X-Keep'),
        })
        if self.path.endswith('/start'):
            location = self.server.redirect_to
            self.send_response(302)
            self.send_header('Location', location)
            self.send_header('Content-Length', '0')
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-Length', '2')
            self.end_headers()
            self.wfile.write(b'OK')

@contextlib.contextmanager
def _proxy(redirect_to):
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), _Handler)
    server.daemon_threads = True
    server.observations = []
    server.redirect_to = redirect_to
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)

HEADERS = {'Authorization': 'Bearer secret', 'Cookie': 'session=secret', 'X-Keep': 'yes'}
CASES = (
 'T01_proxy_same_origin_auth_retained',
 'T02_proxy_same_origin_cookie_retained',
 'T03_proxy_cross_origin_auth_stripped',
 'T04_proxy_cross_origin_cookie_stripped',
 'T05_proxy_cross_origin_host_regenerated',
 'T06_proxy_to_proxy_origin_auth_stripped',
 'T07_proxy_to_proxy_origin_host_regenerated',
 'C01_proxy_no_redirect_status',
 'C02_proxy_no_redirect_host',
 'C03_proxy_redirect_disabled',
 'C04_proxy_same_origin_target',
 'C05_proxy_cross_origin_target',
 'C06_proxy_keep_header_retained',
)

def _scenario(case):
    if case.startswith(('T01', 'T02', 'C04')):
        destination = 'http://a.example/second'
    elif case.startswith(('T03', 'T04', 'T05', 'C05', 'C06')):
        destination = 'http://b.example/second'
    elif case.startswith(('T06', 'T07')):
        destination = 'SELF'
    else:
        destination = 'http://a.example/second'
    with _proxy(destination) as server:
        if destination == 'SELF':
            server.redirect_to = f'http://127.0.0.1:{server.server_port}/second'
        proxy_url = f'http://127.0.0.1:{server.server_port}'
        client = urllib3.ProxyManager(proxy_url, retries=Retry(total=2, redirect=2), timeout=3.0)
        redirect = case != 'C03_proxy_redirect_disabled'
        url = 'http://a.example/normal' if case.startswith(('C01','C02')) else 'http://a.example/start'
        try:
            response = client.request('GET', url, headers=HEADERS, redirect=redirect)
            status = response.status
            response.release_conn()
        finally:
            client.clear()
        return status, server.observations

def evaluate(case):
    status, obs = _scenario(case)
    first, last = obs[0], obs[-1]
    if case == 'T01_proxy_same_origin_auth_retained': return len(obs) == 2 and last['authorization'] == 'Bearer secret'
    if case == 'T02_proxy_same_origin_cookie_retained': return len(obs) == 2 and last['cookie'] == 'session=secret'
    if case == 'T03_proxy_cross_origin_auth_stripped': return len(obs) == 2 and last['authorization'] is None
    if case == 'T04_proxy_cross_origin_cookie_stripped': return len(obs) == 2 and last['cookie'] is None
    if case == 'T05_proxy_cross_origin_host_regenerated': return len(obs) == 2 and last['host'] == 'b.example'
    if case == 'T06_proxy_to_proxy_origin_auth_stripped': return len(obs) == 2 and last['authorization'] is None
    if case == 'T07_proxy_to_proxy_origin_host_regenerated': return len(obs) == 2 and last['host'].lower() == f'127.0.0.1:{int(last["target"].split(":")[2].split("/")[0])}'
    if case == 'C01_proxy_no_redirect_status': return status == 200 and len(obs) == 1
    if case == 'C02_proxy_no_redirect_host': return len(obs) == 1 and first['host'] == 'a.example'
    if case == 'C03_proxy_redirect_disabled': return status == 302 and len(obs) == 1
    if case == 'C04_proxy_same_origin_target': return status == 200 and len(obs) == 2 and last['target'] == 'http://a.example/second'
    if case == 'C05_proxy_cross_origin_target': return status == 200 and len(obs) == 2 and last['target'] == 'http://b.example/second'
    if case == 'C06_proxy_keep_header_retained': return len(obs) == 2 and last['keep'] == 'yes'
    raise KeyError(case)

def main():
    results = []
    for case in CASES:
        try:
            results.append({'case': case, 'status': 'OBSERVED', 'pass': bool(evaluate(case))})
        except Exception as e:
            results.append({'case': case, 'status': 'EXCEPTION', 'pass': None,
                            'error': type(e).__name__, 'detail': str(e)[:250]})
    print(json.dumps({'schema':'lattice.run364.proxy_redirect.v1',
                      'installed_urllib3':urllib3.__version__, 'cases':results}, sort_keys=True, indent=2))

if __name__ == '__main__': main()
