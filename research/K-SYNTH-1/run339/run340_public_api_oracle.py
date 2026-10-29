"""Frozen HTTPcore #882 public-API oracle. No reference-derived localization.

Must execute in isolated historical source arm with RUN340_ARM, RUN340_OUT,
RUN340_SCOPE environment variables. Historical qualification is separate from
the installed-package scaffold; no untrusted model-generated code is run.
"""
import asyncio
import json
import os
from pathlib import Path
import httpcore

class SyncStream(httpcore.NetworkStream):
    def __init__(self, chunks):
        self.chunks=list(chunks); self.trace=[]
    def read(self,max_bytes,timeout=None):
        value=self.chunks.pop(0) if self.chunks else b""
        self.trace.append(["read",max_bytes,value.hex()])
        return value
    def write(self,buffer,timeout=None):
        self.trace.append(["write",len(buffer),buffer.hex()])
    def close(self): self.trace.append(["close"])
    def start_tls(self,*args,**kwargs): raise AssertionError("Unexpected TLS")
    def get_extra_info(self,info): return None

class SyncBackend(httpcore.NetworkBackend):
    def __init__(self,chunks): self.stream=SyncStream(chunks)
    def connect_tcp(self,*args,**kwargs): return self.stream
    def connect_unix_socket(self,*args,**kwargs): raise AssertionError("Unexpected UDS")
    def sleep(self,seconds): pass

class AsyncStream(httpcore.AsyncNetworkStream):
    def __init__(self,chunks): self.chunks=list(chunks); self.trace=[]
    async def read(self,max_bytes,timeout=None):
        value=self.chunks.pop(0) if self.chunks else b""
        self.trace.append(["read",max_bytes,value.hex()])
        return value
    async def write(self,buffer,timeout=None):
        self.trace.append(["write",len(buffer),buffer.hex()])
    async def aclose(self): self.trace.append(["aclose"])
    async def start_tls(self,*args,**kwargs): raise AssertionError("Unexpected TLS")
    def get_extra_info(self,info): return None

class AsyncBackend(httpcore.AsyncNetworkBackend):
    def __init__(self,chunks): self.stream=AsyncStream(chunks)
    async def connect_tcp(self,*args,**kwargs): return self.stream
    async def connect_unix_socket(self,*args,**kwargs): raise AssertionError("Unexpected UDS")
    async def sleep(self,seconds): pass

CASES=[(mode,kind,trailing)
       for kind in ("connect","upgrade","ordinary")
       for trailing in ((True,False) if kind!="ordinary" else (True,))
       for mode in ("sync","async")]
assert len(CASES)==10

def make_case(kind,trailing):
    if kind=="connect":
        method="CONNECT"; headers=None
        prefix=b"HTTP/1.1 200 Connection Established\r\n\r\n"
    elif kind=="upgrade":
        method="GET"; headers={"Connection":"Upgrade","Upgrade":"websocket"}
        prefix=b"HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: websocket\r\n\r\n"
    else:
        method="GET"; headers=None
        prefix=b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\n"
    if kind=="ordinary": return method,headers,[prefix+b"HELLO"]
    return method,headers,[prefix+(b"HELLO" if trailing else b""),b"WORLD"]

def evaluate_sync(kind,trailing):
    method,headers,chunks=make_case(kind,trailing)
    backend=SyncBackend(chunks)
    try:
        with httpcore.ConnectionPool(network_backend=backend) as pool:
            with pool.stream(method,"http://example.com:80/",headers=headers) as response:
                status=response.status
                if kind=="ordinary":
                    got=[b"".join(response.iter_stream())]; expected=[b"HELLO"]
                else:
                    stream=response.extensions["network_stream"]
                    got=[stream.read(1024)]
                    if trailing: got.append(stream.read(1024))
                    expected=[b"HELLO",b"WORLD"] if trailing else [b"WORLD"]
                return {"ok":got==expected and status==({"connect":200,"upgrade":101,"ordinary":200}[kind]),
                        "status":status,"got":[v.hex() for v in got],
                        "expected":[v.hex() for v in expected],"trace":backend.stream.trace}
    except Exception as exc:
        return {"ok":False,"exception":type(exc).__name__,"message":str(exc),
                "trace":backend.stream.trace}

async def evaluate_async(kind,trailing):
    method,headers,chunks=make_case(kind,trailing)
    backend=AsyncBackend(chunks)
    try:
        async with httpcore.AsyncConnectionPool(network_backend=backend) as pool:
            async with pool.stream(method,"http://example.com:80/",headers=headers) as response:
                status=response.status
                if kind=="ordinary":
                    got=[b"".join([v async for v in response.aiter_stream()])]
                    expected=[b"HELLO"]
                else:
                    stream=response.extensions["network_stream"]
                    got=[await stream.read(1024)]
                    if trailing: got.append(await stream.read(1024))
                    expected=[b"HELLO",b"WORLD"] if trailing else [b"WORLD"]
                return {"ok":got==expected and status==({"connect":200,"upgrade":101,"ordinary":200}[kind]),
                        "status":status,"got":[v.hex() for v in got],
                        "expected":[v.hex() for v in expected],"trace":backend.stream.trace}
    except Exception as exc:
        return {"ok":False,"exception":type(exc).__name__,"message":str(exc),
                "trace":backend.stream.trace}

async def main():
    records=[]
    for mode,kind,trailing in CASES:
        result=evaluate_sync(kind,trailing) if mode=="sync" else await evaluate_async(kind,trailing)
        records.append({"mode":mode,"kind":kind,"trailing":trailing,**result})
    result={"scope":os.environ.get("RUN340_SCOPE","SCAFFOLD_ONLY"),
            "arm":os.environ.get("RUN340_ARM","installed"),
            "httpcore_version":httpcore.__version__,
            "records":records,"passes":sum(r["ok"] for r in records)}
    out=Path(os.environ.get("RUN340_OUT","run340_oracle.json"))
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"arm":result["arm"],"passes":result["passes"],"total":10}))

if __name__=="__main__": asyncio.run(main())
