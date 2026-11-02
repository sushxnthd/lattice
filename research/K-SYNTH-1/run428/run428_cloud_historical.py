"""Frozen 14-case historical urllib3 #3352 oracle, isolated GitHub Actions only."""
import hashlib, json, os, threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
CASES=[('//v:h','/v:h','T'),('///v:h','/v:h','T'),('//host:bad/path','/host:bad/path','T'),('//v:h?x=1','/v:h?x=1','T'),('///v:h?x=1&y=2','/v:h?x=1&y=2','T'),('//v:h#fragment','/v:h','T'),('/v:h','/v:h','C'),('/v:h?x=1','/v:h?x=1','C'),('/simple','/simple','C'),('/?x=1','/?x=1','C'),('/','/','C'),('/v%3Ah','/v%3Ah','C'),('/a%2Fb','/a%2Fb','C'),('//hello/world','/hello/world','C')]
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  data=json.dumps({'target':self.path}).encode();self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def log_message(self,*args):pass
def main():
 import urllib3
 source=Path(urllib3.__file__).resolve();root=Path(os.environ['EXPECTED_UPSTREAM_SRC']).resolve()
 assert source.is_relative_to(root),(source,root)
 srv=ThreadingHTTPServer(('127.0.0.1',0),H);t=threading.Thread(target=srv.serve_forever,daemon=True);t.start()
 rows=[];pool=urllib3.PoolManager(retries=False)
 try:
  for path,expected,kind in CASES:
   row={'path':path,'expected':expected,'kind':kind}
   try:
    r=pool.request('GET',f'http://127.0.0.1:{srv.server_port}{path}',retries=False,timeout=urllib3.Timeout(connect=1,read=1))
    row.update({'status':r.status,'observed':json.loads(r.data)['target']})
   except Exception as exc:row.update({'exception':type(exc).__name__,'message':str(exc)[:200]})
   row['pass']=row.get('status')==200 and row.get('observed')==expected;rows.append(row)
 finally:
  pool.clear();srv.shutdown();srv.server_close();t.join(timeout=3)
 summary={'version':urllib3.__version__,'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'target_pass':sum(r['pass'] for r in rows if r['kind']=='T'),'control_pass':sum(r['pass'] for r in rows if r['kind']=='C')}
 print(json.dumps({'summary':summary,'rows':rows},sort_keys=True))
if __name__=='__main__':main()
