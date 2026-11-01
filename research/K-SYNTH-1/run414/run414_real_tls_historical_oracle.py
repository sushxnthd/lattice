#!/usr/bin/env python3
"""Post-reference, isolated real HTTPS forwarding-proxy policy oracle. No external hosts."""
import hashlib,json,pathlib,ssl,socket,threading,tempfile,datetime
import urllib3
from cryptography import x509
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

def make_cert(folder):
    key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'localhost')])
    cert=(x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(days=1))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost')]),critical=False)
        .add_extension(x509.BasicConstraints(ca=True,path_length=None),critical=True)
        .sign(key,hashes.SHA256()))
    cp=folder/'proxy.crt';kp=folder/'proxy.key'
    cp.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    kp.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    return cp,kp

class Proxy:
    def __init__(self,cert,key):
        self.listener=socket.socket()
        self.listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.listener.bind(('127.0.0.1',0));self.listener.listen(1);self.listener.settimeout(6)
        self.port=self.listener.getsockname()[1];self.events=[]
        self.ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);self.ctx.load_cert_chain(str(cert),str(key))
        self.thread=threading.Thread(target=self.serve,daemon=True);self.thread.start()
    def serve(self):
        try:
            raw,_=self.listener.accept();raw.settimeout(5)
            with self.ctx.wrap_socket(raw,server_side=True) as conn:
                data=b''
                while b'\r\n\r\n' not in data and len(data)<16384:
                    chunk=conn.recv(4096)
                    if not chunk:break
                    data+=chunk
                self.events.append({'request_line':data.split(b'\r\n',1)[0].decode('ascii','replace')})
                body=b'LATTICE_RUN414_REAL_TLS'
                conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Length: '+str(len(body)).encode()+b'\r\nConnection: close\r\n\r\n'+body)
        except Exception as exc:self.events.append({'server_error':type(exc).__name__,'message':str(exc)[:150]})
        finally:self.listener.close()
    def wait(self):self.thread.join(timeout=7)

def proxy_context(cert,verify,trusted):
    c=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    c.check_hostname=False;c.verify_mode=ssl.CERT_REQUIRED if verify else ssl.CERT_NONE
    if verify and trusted:c.load_verify_locations(cafile=str(cert))
    c.check_hostname=verify
    return c

def run_case(cert,key,pverify,tverify,trust,hostname,kind='grid'):
    proxy=Proxy(cert,key)
    pc=proxy_context(cert,pverify,trust)
    tc=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tc.check_hostname=False;tc.verify_mode=ssl.CERT_REQUIRED if tverify else ssl.CERT_NONE
    opts={'proxy_ssl_context':pc,'ssl_context':tc,'use_forwarding_for_https':True,
          'retries':False,'timeout':urllib3.Timeout(connect=2,read=2)}
    if kind=='target_assert_hostname':opts['assert_hostname']='not-localhost.invalid'
    elif kind=='target_assert_fingerprint':opts['assert_fingerprint']='00'*32
    elif kind=='target_missing_client_cert':opts['cert_file']=str(cert.parent/'missing-target-cert.pem')
    elif kind!='grid':raise ValueError(kind)
    manager=urllib3.ProxyManager(f'https://{hostname}:{proxy.port}',**opts)
    status=None;body=None;error=None
    try:
        r=manager.request('GET','https://target.invalid/run414',retries=False)
        status=r.status;body=r.data.decode('ascii','replace')
    except Exception as exc:error={'type':type(exc).__name__,'message':str(exc)[:400]}
    finally:manager.clear();proxy.wait()
    expected=(not pverify or (trust and hostname=='localhost'))
    accepted=(status==200 and body=='LATTICE_RUN414_REAL_TLS')
    return {'kind':kind,'proxy_verify':pverify,'target_verify':tverify,
            'proxy_trust':trust,'proxy_hostname':hostname,'expected_accept':expected,
            'accepted':accepted,'correct':expected==accepted,'status':status,
            'error':error,'proxy_events':proxy.events,
            'http_reached':any('request_line' in e for e in proxy.events)}

def main():
    with tempfile.TemporaryDirectory(prefix='lattice-run414-real-') as td:
        cert,key=make_cert(pathlib.Path(td))
        rows=[run_case(cert,key,p,t,tr,h) for p in (False,True) for t in (False,True)
              for tr in (False,True) for h in ('localhost','127.0.0.1')]
        rows += [run_case(cert,key,True,False,True,'localhost',kind)
                 for kind in ('target_assert_hostname','target_assert_fingerprint','target_missing_client_cert')]
    root=pathlib.Path(urllib3.__file__).resolve().parent
    print(json.dumps({'experiment':'post-reference historical real TLS forwarding and identity',
       'version':urllib3.__version__,'source_root':str(root),
       'source_sha256':{f:hashlib.sha256((root/f).read_bytes()).hexdigest()
                        for f in ('connection.py','poolmanager.py')},
       'rows':rows,'correct':sum(r['correct'] for r in rows),'total':len(rows),
       'false_accept':sum(r['accepted'] and not r['expected_accept'] for r in rows),
       'false_reject':sum(not r['accepted'] and r['expected_accept'] for r in rows)},sort_keys=True))
if __name__=='__main__':main()
