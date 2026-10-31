#!/usr/bin/env python3
"""Reference-blind frozen HTTPcore #724 public API / actual h2-wire oracle.
No source patches, external network, test edits or reference code are loaded.
"""
import asyncio
import hashlib
import h2.config
import h2.connection
import h2.events
import httpcore
import json
import platform
import sys

CASES = [
    ("public_network_stream_identity", "target"),
    ("heldout_network_stream_server_addr", "target"),
    ("control_http_version", "control"),
    ("control_status", "control"),
    ("control_body", "control"),
    ("control_reuse", "control"),
]

class Peer:
    def __init__(self):
        self.server = h2.connection.H2Connection(config=h2.config.H2Configuration(client_side=False))
        self.server.initiate_connection()
        self.pending = bytearray(self.server.data_to_send())
        self.paths = []
    def accept(self, data):
        for event in self.server.receive_data(data):
            if isinstance(event, h2.events.RequestReceived):
                path = dict(event.headers).get(b":path", b"")
                self.paths.append(path.decode("ascii"))
                self.server.send_headers(event.stream_id, [(b":status", b"201"), (b"x-lattice", b"381")])
                self.server.send_data(event.stream_id, b"OK", end_stream=True)
        self.pending.extend(self.server.data_to_send())
    def take(self):
        data = bytes(self.pending)
        self.pending.clear()
        return data

class SyncStream:
    def __init__(self): self.peer = Peer()
    def read(self, max_bytes, timeout=None): return self.peer.take()
    def write(self, buffer, timeout=None): self.peer.accept(buffer)
    def close(self): pass
    def get_extra_info(self, info): return ("127.0.0.1", 443) if info == "server_addr" else None

class AsyncStream:
    def __init__(self): self.peer = Peer()
    async def read(self, max_bytes, timeout=None): return self.peer.take()
    async def write(self, buffer, timeout=None): self.peer.accept(buffer)
    async def aclose(self): pass
    def get_extra_info(self, info): return ("127.0.0.1", 443) if info == "server_addr" else None

def request(path):
    return httpcore.Request("GET", "https://example.com" + path, headers=[(b"host", b"example.com")])

def summarize(response, stream, body):
    ext = response.extensions
    return {
        "status": response.status,
        "headers": [[k.decode(), v.decode()] for k, v in response.headers],
        "body": body.decode(),
        "http_version": ext.get("http_version", b"").decode(),
        "stream_id": ext.get("stream_id"),
        "network_stream_present": "network_stream" in ext,
        "network_stream_identity": ext.get("network_stream") is stream,
        "network_stream_server_addr": ext["network_stream"].get_extra_info("server_addr") if "network_stream" in ext else None,
    }

def sync_run():
    from httpcore._sync.http2 import HTTP2Connection
    stream = SyncStream()
    r = request("/first")
    conn = HTTP2Connection(r.url.origin, stream)
    response = conn.handle_request(r)
    body = response.read()
    result = summarize(response, stream, body)
    response.close()
    second = conn.handle_request(request("/second"))
    second_body = second.read()
    second.close()
    result["reuse"] = (second.status, second_body, stream.peer.paths) == (201, b"OK", ["/first", "/second"])
    return result

async def async_run():
    from httpcore._async.http2 import AsyncHTTP2Connection
    stream = AsyncStream()
    r = request("/first")
    conn = AsyncHTTP2Connection(r.url.origin, stream)
    response = await conn.handle_async_request(r)
    body = await response.aread()
    result = summarize(response, stream, body)
    await response.aclose()
    second = await conn.handle_async_request(request("/second"))
    second_body = await second.aread()
    await second.aclose()
    result["reuse"] = (second.status, second_body, stream.peer.paths) == (201, b"OK", ["/first", "/second"])
    return result

def judge(result, case):
    return {
        "public_network_stream_identity": lambda: result["network_stream_identity"],
        "heldout_network_stream_server_addr": lambda: result["network_stream_server_addr"] == ("127.0.0.1", 443),
        "control_http_version": lambda: result["http_version"] == "HTTP/2" and isinstance(result["stream_id"], int),
        "control_status": lambda: result["status"] == 201,
        "control_body": lambda: result["body"] == "OK" and ["x-lattice", "381"] in result["headers"],
        "control_reuse": lambda: result["reuse"],
    }[case]()

def main():
    observations=[]
    for kind, fn in [("sync", sync_run), ("async", lambda: asyncio.run(async_run()))]:
        try:
            result=fn()
            for name, role in CASES:
                observations.append({"kind":kind,"case":name,"role":role,"pass":bool(judge(result,name)),"trace":result})
        except BaseException as exc:
            for name,role in CASES:
                observations.append({"kind":kind,"case":name,"role":role,"pass":False,"error":repr(exc)})
    output={"schema":1,"issue":"encode/httpcore#724","httpcore_version":getattr(httpcore,"__version__", "unknown"),"python":platform.python_version(),"h2":__import__('h2').__version__,"observations":observations}
    raw=json.dumps(output,sort_keys=True,indent=2).encode()
    print(raw.decode())
    return 0

if __name__=="__main__": sys.exit(main())
