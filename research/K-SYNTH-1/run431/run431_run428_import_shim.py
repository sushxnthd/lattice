#!/usr/bin/env python3
"""Import-only metadata shim for Run428 historical urllib3 source replay.
Does not modify upstream source files or the frozen Run428 functional oracle.
"""
import hashlib, json, os, pathlib, runpy, sys, types
root=pathlib.Path(os.environ["EXPECTED_UPSTREAM_SRC"]).resolve()
missing=not (root/"urllib3"/"_version.py").exists()
if missing:
    mod=types.ModuleType("urllib3._version")
    mod.__version__="0+run431-metadata-shim"
    sys.modules["urllib3._version"]=mod
receipt={"upstream_src":str(root),"metadata_shim_installed":missing,
         "source_version_file_exists":not missing,
         "shim_scope":"urllib3._version.__version__ only; no upstream files modified"}
p=os.environ.get("RUN431_SHIM_RECEIPT")
if p:pathlib.Path(p).write_text(json.dumps(receipt,sort_keys=True)+"\n")
print("RUN431_IMPORT_RECEIPT",json.dumps(receipt,sort_keys=True),file=sys.stderr,flush=True)
oracle=pathlib.Path(__file__).resolve().parents[1]/"run428"/"run428_cloud_historical.py"
runpy.run_path(str(oracle),run_name="__main__")
