"""Two distinct HTTP request-targets collapse to one server observation."""
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        b=json.dumps({"path":self.path}).encode()
        self.send_response(200)
        self.send_header("Content-Length",str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def log_message(self,*args):pass

def probe(path):
    s=ThreadingHTTPServer(("127.0.0.1",0),Handler)
    t=threading.Thread(target=s.serve_forever,daemon=True);t.start()
    try:
        with socket.create_connection(("127.0.0.1",s.server_port),timeout=2) as c:
            c.sendall(("GET "+path+" HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n").encode())
            response=b""
            while True:
                chunk=c.recv(65536)
                if not chunk:break
                response+=chunk
        return json.loads(response.split(b"\r\n\r\n",1)[1])["path"]
    finally:
        s.shutdown();s.server_close();t.join(timeout=3)

a,b="//v:h","/v:h"
observed_a,observed_b=probe(a),probe(b)
assert a!=b and observed_a==observed_b=="/v:h"
print(json.dumps({"raw_a":a,"raw_b":b,"observed_a":observed_a,"observed_b":observed_b,"noninjective":True},sort_keys=True))
