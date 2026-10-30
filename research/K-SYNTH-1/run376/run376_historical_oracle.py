#!/usr/bin/env python3
"""Frozen network-free historical httpcore issue #670 oracle; no upstream monkeypatching."""
import argparse, asyncio, json, os, subprocess, threading, time, traceback
from pathlib import Path
BASE='5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e'
BLOBS={'httpcore/_async/connection_pool.py':'e6c4ef66312d4d6f31fcbfc417905ae329ef5885',
'httpcore/_sync/connection_pool.py':'53536d05e8c3d127b466e44dcf20e9f028aadab0',
'httpcore/_synchronization.py':'be3dcfda72158d1430c34c0387988eacac3452b8'}
PUBLIC=['T1','T2','C1','C2','C3','C4','C5','C6']
HELDOUT=['H1','H2','H3','H4']
EXPECTED={'T1':'CancelledError','T2':'PoolTimeout','C1':'PoolTimeout','C2':'PoolTimeout',
'C3':'OK','C4':'OK','C5':'UnsupportedProtocol','C6':'UnsupportedProtocol',
'H1':'CancelledError,CancelledError','H2':'PoolTimeout,PoolTimeout',
'H3':'CancelledError','H4':'PoolTimeout'}

def source_integrity(root):
    got={}
    for name,expected in BLOBS.items():
        actual=subprocess.check_output(['git','hash-object',str(root/name)],text=True).strip()
        got[name]=actual
        if actual!=expected: raise AssertionError(f'source mismatch {name}: {actual} != {expected}')
    head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if head!=BASE: raise AssertionError(f'base mismatch: {head}')
    return {'commit':head,'blobs':got}

def request(timeout=None,scheme='http'):
    import httpcore
    return httpcore.Request('GET',f'{scheme}://example.com/',extensions={'timeout':{'pool':timeout}})

async def wait_queue_async(pool,count):
    for _ in range(500):
        if len(pool._requests)==count:
            await asyncio.sleep(0); return
        await asyncio.sleep(.001)
    raise TimeoutError('queue scheduling timed out')

def wait_queue_sync(pool,count):
    deadline=time.monotonic()+1
    while time.monotonic()<deadline:
        if len(pool._requests)==count:return
        time.sleep(.001)
    raise TimeoutError('queue scheduling timed out')

async def async_waiter(pool,timeout=None):
    try:
        await pool.handle_async_request(request(timeout))
        return 'UNEXPECTED_RESPONSE'
    except BaseException as exc:return type(exc).__name__

def sync_waiter(pool,timeout):
    try:
        pool.handle_request(request(timeout))
        return 'UNEXPECTED_RESPONSE'
    except BaseException as exc:return type(exc).__name__

async def async_case(case):
    import httpcore
    pool=httpcore.AsyncConnectionPool(max_connections=0)
    if case=='C3':
        await pool.aclose();await pool.aclose();return 'OK',len(pool._requests)
    if case=='C5':
        try:await pool.handle_async_request(request(.02,'ftp'))
        except BaseException as exc:return type(exc).__name__,len(pool._requests)
        return 'UNEXPECTED_RESPONSE',len(pool._requests)
    if case=='C1':return await async_waiter(pool,.025),len(pool._requests)
    if case in ('T1','H1','H3'):
        n=2 if case=='H1' else 1
        tasks=[asyncio.create_task(async_waiter(pool,None)) for _ in range(n)]
        await wait_queue_async(pool,n)
        if case!='H3':await pool.aclose()
        for task in tasks:task.cancel()
        vals=await asyncio.gather(*tasks,return_exceptions=True)
        return ','.join(v if isinstance(v,str) else type(v).__name__ for v in vals),len(pool._requests)
    raise ValueError(case)

def sync_case(case):
    import httpcore
    pool=httpcore.ConnectionPool(max_connections=0)
    if case=='C4':
        pool.close();pool.close();return 'OK',len(pool._requests)
    if case=='C6':
        try:pool.handle_request(request(.02,'ftp'))
        except BaseException as exc:return type(exc).__name__,len(pool._requests)
        return 'UNEXPECTED_RESPONSE',len(pool._requests)
    if case in ('T2','C2','H2','H4'):
        n=2 if case=='H2' else 1
        results=[None]*n
        def run(i):results[i]=sync_waiter(pool,.12 if case in ('T2','H2') else .025)
        threads=[threading.Thread(target=run,args=(i,),daemon=True) for i in range(n)]
        for t in threads:t.start()
        if case in ('T2','H2'):
            wait_queue_sync(pool,n);pool.close()
        for t in threads:t.join(1)
        if any(t.is_alive() for t in threads):raise TimeoutError('worker thread hung')
        return ','.join(results),len(pool._requests)
    raise ValueError(case)

def run_case(case):
    start=time.monotonic()
    try:
        if case in ('T1','C1','C3','C5','H1','H3'):
            observed,remaining=asyncio.run(async_case(case))
        else:observed,remaining=sync_case(case)
        error=None
    except BaseException as exc:
        observed=type(exc).__name__;remaining=None;error=traceback.format_exc(limit=8)
    return {'case':case,'expected':EXPECTED[case],'observed':observed,
            'passed':observed==EXPECTED[case] and remaining==0,
            'queue_remaining':remaining,'elapsed_ms':round((time.monotonic()-start)*1000,3),
            'error_trace':error}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--upstream',default='upstream')
    p.add_argument('--phase',choices=['public','heldout'],default='public')
    p.add_argument('--out',required=True)
    a=p.parse_args()
    integrity=source_integrity(Path(a.upstream).resolve())
    import httpcore
    cases=PUBLIC if a.phase=='public' else HELDOUT
    data={'issue':'encode/httpcore#670','phase':a.phase,'integrity':integrity,
          'httpcore_version':getattr(httpcore,'__version__','UNKNOWN'),
          'python':os.sys.version,'cases':[run_case(c) for c in cases]}
    Path(a.out).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'phase':a.phase,'passed':sum(x['passed'] for x in data['cases']),
          'total':len(cases),'cases':[(x['case'],x['observed']) for x in data['cases']]},sort_keys=True))

if __name__=='__main__':main()
