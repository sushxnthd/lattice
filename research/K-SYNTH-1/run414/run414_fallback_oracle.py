#!/usr/bin/env python3
"""Post-reference historical real TLS forwarding fallback experiment; no external hosts."""
import hashlib,json,pathlib,ssl,tempfile,urllib3,warnings
from run414_real_tls_historical_oracle import Proxy,make_cert,proxy_context

def run_case(cert,key,verify,trusted,explicit,target_verify):
    server=Proxy(cert,key)
    pc=proxy_context(cert,verify,trusted)
    tc=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tc.check_hostname=False
    tc.verify_mode=ssl.CERT_REQUIRED if target_verify else ssl.CERT_NONE
    opts={'use_forwarding_for_https':True,'retries':False,
          'timeout':urllib3.Timeout(connect=2,read=2)}
    if explicit:
        opts['proxy_ssl_context']=pc
        opts['ssl_context']=tc
    else:
        opts['ssl_context']=pc
    with warnings.catch_warnings(record=True) as ww:
        warnings.simplefilter('always')
        mgr=urllib3.ProxyManager(f'https://localhost:{server.port}',**opts)
    proxy_config=mgr.proxy_config
    state={'manager_proxy_ssl_context_is_pc':mgr.proxy_ssl_context is pc,
           'config_ssl_context_is_pc':proxy_config.ssl_context is pc if proxy_config else None,
           'config_ssl_context_is_none':proxy_config.ssl_context is None if proxy_config else None,
           'warnings':[str(w.message)[:160] for w in ww]}
    status=None;error=None;body=None
    try:
        r=mgr.request('GET','https://target.invalid/run414-fallback',retries=False)
        status=r.status;body=r.data.decode('ascii','replace')
    except Exception as exc:error={'type':type(exc).__name__,'message':str(exc)[:400]}
    finally:mgr.clear();server.wait()
    accepted=status==200 and body=='LATTICE_RUN414_REAL_TLS'
    expected=not verify or trusted
    return {'verify':verify,'trusted':trusted,'explicit':explicit,
            'target_verify':target_verify,'accepted':accepted,'expected':expected,
            'correct':accepted==expected,'status':status,'error':error,
            'manager_state':state,'proxy_events':server.events}

def main():
    with tempfile.TemporaryDirectory(prefix='run414-fallback-') as tmp:
        cert,key=make_cert(pathlib.Path(tmp))
        rows=[run_case(cert,key,verify,trust,explicit,target_verify)
              for explicit in (False,True) for verify in (False,True)
              for trust in (False,True) for target_verify in (False,True)]
    root=pathlib.Path(urllib3.__file__).resolve().parent
    print(json.dumps({'experiment':'post-reference historical real TLS fallback and explicit context',
        'source_sha256':{n:hashlib.sha256((root/n).read_bytes()).hexdigest()
                         for n in ('connection.py','poolmanager.py')},
        'rows':rows,'correct':sum(r['correct'] for r in rows),'total':len(rows)},sort_keys=True))
if __name__=='__main__':main()
