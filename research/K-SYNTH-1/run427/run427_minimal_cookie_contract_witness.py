#!/usr/bin/env python3
"""Run427 minimal real HTTPX redirect-cookie specification witness.
Local MockTransport only. Not an exact historical-source qualification.
"""
import asyncio
import json
import httpx

def handler(request):
    if request.url.path == "/start":
        return httpx.Response(302, headers={"location":"/end"})
    return httpx.Response(200, json={"cookie":request.headers.get("cookie")})

def sync():
    with httpx.Client(transport=httpx.MockTransport(handler),follow_redirects=True) as client:
        per_request=client.get("http://example.invalid/start",cookies={"token":"value"}).json()["cookie"]
    with httpx.Client(transport=httpx.MockTransport(handler),follow_redirects=True,cookies={"token":"value"}) as client:
        client_level=client.get("http://example.invalid/start").json()["cookie"]
    return {"per_request":per_request,"client_level":client_level}

async def async_run():
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler),follow_redirects=True) as client:
        per_request=(await client.get("http://example.invalid/start",cookies={"token":"value"})).json()["cookie"]
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler),follow_redirects=True,cookies={"token":"value"}) as client:
        client_level=(await client.get("http://example.invalid/start")).json()["cookie"]
    return {"per_request":per_request,"client_level":client_level}

if __name__=="__main__":
    results={"version":httpx.__version__,"sync":sync(),"async":asyncio.run(async_run())}
    assert results["sync"]==results["async"]
    assert results["sync"]=={"per_request":None,"client_level":"token=value"}
    print(json.dumps(results,sort_keys=True))
