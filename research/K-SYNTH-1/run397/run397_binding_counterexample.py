"""Executable import-snapshot, definition-default, and call-time-alias counterexample."""
import sys,types
m=types.ModuleType('_run397_binding_module')
m.f=lambda: 'original'
sys.modules[m.__name__]=m
from _run397_binding_module import f as imported_f

def default_capture(f=m.f):
    return f()

def call_time_alias():
    f=m.f
    return f()

assert imported_f()=='original'
assert default_capture()=='original'
assert call_time_alias()=='original'
m.f=lambda: 'rebound'
assert imported_f()=='original'
assert default_capture()=='original'
assert call_time_alias()=='rebound'
print({'import_snapshot':'original','default_snapshot':'original','call_time_alias':'rebound'})
