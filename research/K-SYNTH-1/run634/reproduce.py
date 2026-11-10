"""Controlled Python analogue, not a Werkzeug oracle."""
import json
from functools import cached_property
class Response:
    def __init__(self, data): self._data=data; self.calls=0
    def get_data(self, as_text=False):
        self.calls+=1
        return self._data.decode() if as_text else self._data
class TestResponse(Response):
    @cached_property
    def text(self): return self.get_data(as_text=True)
class MovedResponse(Response):
    @property
    def text(self): return self.get_data(as_text=True)
class MovedTestResponse(MovedResponse): pass
class BothTestResponse(MovedResponse):
    @cached_property
    def text(self): return self.get_data(as_text=True)
out={}
for name,cls in [('base',Response),('old_test',TestResponse),('add_parent_only',MovedTestResponse),('both_changes',BothTestResponse),('parent',MovedResponse)]:
    x=cls(b'hello')
    try:
        a=x.text; b=x.text
        out[name]={'text':[a,b],'get_data_calls':x.calls,'property_owner':next(c.__name__ for c in cls.__mro__ if 'text' in c.__dict__)}
    except AttributeError: out[name]={'text':'ABSENT','get_data_calls':x.calls}
assert out['add_parent_only']['text']==out['both_changes']['text']==['hello','hello']
assert out['add_parent_only']['get_data_calls']==2
assert out['both_changes']['get_data_calls']==1
assert out['base']['text']=='ABSENT'
print(json.dumps(out,indent=2,sort_keys=True))
