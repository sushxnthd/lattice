import functools, json
def make(parent, remove):
    class Response:
        def __init__(self, data): self.data=data
        def get_data(self, as_text=False): return self.data.decode() if as_text else self.data
    if parent:
        Response.text=property(lambda s:s.get_data(as_text=True))
    class TestResponse(Response): pass
    if not remove:
        d=functools.cached_property(lambda s:s.get_data(as_text=True))
        d.__set_name__(TestResponse, "text")
        TestResponse.text=d
    return Response,TestResponse
def trial(p,r):
    Response,TestResponse=make(p,r)
    out={}
    for cls in (Response,TestResponse):
        obj=cls(b"old")
        try: first=obj.text
        except AttributeError: first="ATTRIBUTE_ERROR"
        obj.data=b"new"
        try: second=obj.text
        except AttributeError: second="ATTRIBUTE_ERROR"
        out[cls.__name__]=[first,second]
    return out
arms={f"{int(p)}{int(r)}":trial(p,r) for p in (False,True) for r in (False,True)}
assert arms["00"]["TestResponse"]==["old","old"]
assert arms["10"]["TestResponse"]==["old","old"]
assert arms["11"]["TestResponse"]==["old","new"]
assert arms["01"]["TestResponse"]==["ATTRIBUTE_ERROR","ATTRIBUTE_ERROR"]
assert arms["11"]["Response"]==["old","new"]
print(json.dumps(arms,sort_keys=True,indent=2))
