"""Independent public API state-transition oracle for pinned Werkzeug PR3341.
Requires upstream Werkzeug importable from each isolated factorial worktree.
"""
import json
from werkzeug.wrappers import Response
from werkzeug.test import Client

def test_response():
    def app(environ, start_response):
        start_response('200 OK',[('Content-Type','text/plain')]);return [b'alpha']
    return Client(app, Response).get('/')

def probe(obj):
    out={'class':type(obj).__name__}
    try:
        out['first']=obj.text
        obj.set_data('beta')
        out['second']=obj.text
        out['fresh']=out['second']=='beta'
        out['initial_correct']=out['first']=='alpha'
    except Exception as exc:
        out['error_type']=type(exc).__name__
    return out

if __name__=='__main__':
    print(json.dumps({'ordinary':probe(Response('alpha')),'client':probe(test_response())},sort_keys=True))
