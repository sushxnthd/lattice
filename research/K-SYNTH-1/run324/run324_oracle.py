"""Trusted no-network functional oracle. Run ONLY inside an isolated Docker container."""
import json,sys,traceback
sys.path.insert(0,sys.argv[1]+'/src')
from urllib3 import PoolManager
from urllib3.util.url import Url,parse_url

def check(name,kind,fn):
 try:
  observed=fn();return dict(name=name,kind=kind,passed=bool(observed),error=None)
 except Exception as e:return dict(name=name,kind=kind,passed=False,error=type(e).__name__+': '+str(e))
checks=[
 check('explicit_pool_port_zero','target',lambda:PoolManager().connection_from_host('example.com',port=0,scheme='http').port==0),
 check('url_pool_port_zero','target',lambda:PoolManager().connection_from_url('http://example.com:0').port==0),
 check('url_object_port_zero','target',lambda:Url(scheme='http',host='example.com',port=0).url=='http://example.com:0'),
 check('missing_pool_port','control',lambda:PoolManager().connection_from_host('example.com',port=None,scheme='http').port==80),
 check('explicit_pool_port_80','control',lambda:PoolManager().connection_from_host('example.com',port=80,scheme='http').port==80),
 check('explicit_pool_port_8080','control',lambda:PoolManager().connection_from_host('example.com',port=8080,scheme='http').port==8080),
 check('https_default_port','control',lambda:PoolManager().connection_from_host('example.com',port=None,scheme='https').port==443),
 check('url_parse_zero','control',lambda:parse_url('http://example.com:0').port==0),
 check('url_without_port','control',lambda:Url(scheme='http',host='example.com',port=None).url=='http://example.com'),
]
print(json.dumps(dict(rows=checks,all_pass=all(x['passed'] for x in checks),targets=sum(x['passed'] for x in checks if x['kind']=='target'),controls=sum(x['passed'] for x in checks if x['kind']=='control')),sort_keys=True))
