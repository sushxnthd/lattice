import functools, itertools, json
def arm(parent, subclass):
    class Response:
        def __init__(self, value): self.data=value; self.calls=0
        if parent:
            @property
            def text(self): self.calls+=1; return self.data
    class TestResponse(Response):
        if subclass:
            @functools.cached_property
            def text(self): self.calls+=1; return self.data
    return Response, TestResponse
def probe(cls):
    o=cls('alpha')
    try:
        first=o.text; o.data='beta'; second=o.text
        return {'initial':first,'after_change':second,'reads':o.calls}
    except AttributeError: return {'error':'AttributeError'}
results={}
for p,s in itertools.product((False,True),repeat=2):
    R,T=arm(p,s)
    results[f'parent_{int(p)}_subclass_{int(s)}']={'ordinary':probe(R),'client':probe(T)}
assert results['parent_0_subclass_1']['client']['after_change']=='alpha'
assert results['parent_1_subclass_1']['client']['after_change']=='alpha'
assert results['parent_1_subclass_0']['client']['after_change']=='beta'
assert results['parent_0_subclass_0']['client']['error']=='AttributeError'
print(json.dumps(results,indent=2,sort_keys=True))
