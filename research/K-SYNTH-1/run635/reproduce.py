from functools import cached_property
import json
class Parent:
 def __init__(self): self.calls=0; self.payload='first'
 def get_data(self,as_text=False):
  self.calls+=1
  return self.payload
class BaselineTestResponse(Parent):
 @cached_property
 def text(self): return self.get_data(as_text=True)
class ParentPatched(Parent):
 @property
 def text(self): return self.get_data(as_text=True)
class FullTestResponse(ParentPatched): pass
class ParentOnlyTestResponse(ParentPatched):
 @cached_property
 def text(self): return self.get_data(as_text=True)
records=[]
for cls in (BaselineTestResponse,ParentOnlyTestResponse,FullTestResponse):
 x=cls(); first=x.text; x.payload='second'; second=x.text
 records.append({'arm':cls.__name__,'first':first,'second':second,'calls':x.calls,'cached_instance_attribute':'text' in x.__dict__})
assert records[0]['second']=='first' and records[1]['second']=='first'
assert records[2]['second']=='second'
print(json.dumps(records,indent=2))
