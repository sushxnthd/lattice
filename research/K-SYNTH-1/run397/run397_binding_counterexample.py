"""Minimal executable Python binding-time counterexample; Run397."""
import types
m=types.SimpleNamespace(f=lambda: "original")
from_import_f=m.f
def default_capture(f=m.f):
    return f()
def call_time_alias():
    f=m.f
    return f()
assert from_import_f()=="original"
assert default_capture()=="original"
assert call_time_alias()=="original"
m.f=lambda: "rebound"
assert from_import_f()=="original"
assert default_capture()=="original"
assert call_time_alias()=="rebound"
print({"import_snapshot":"original","default_snapshot":"original","call_time_alias":"rebound"})
