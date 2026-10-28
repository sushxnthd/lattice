#!/usr/bin/env python3
"""Read-only comparison of original corrected cloud ZIP against local frozen evidence."""
import hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
ZIP=pathlib.Path('/mnt/data/lattice_run304_corrected_cloud_original.zip')
with zipfile.ZipFile(ZIP) as z:
    names=z.namelist()
    manifest=json.loads(z.read('RUN304_CLOUD_SHA256_MANIFEST.json'))
    verified=[]
    for name in names:
        if name=='RUN304_CLOUD_SHA256_MANIFEST.json':continue
        digest=hashlib.sha256(z.read(name)).hexdigest()
        assert manifest[name]==digest,(name,digest,manifest.get(name))
        verified.append(name)
    for name in manifest:
        if name not in verified:
            local_file=ROOT/name
            assert local_file.exists(),name
            assert hashlib.sha256(local_file.read_bytes()).hexdigest()==manifest[name],name
            verified.append(name)
    cloud_sources=json.loads(z.read('RUN304_FROZEN_SOURCES.json'))
    cloud_raw=json.loads(z.read('RUN304_RAW_FUNCTIONAL.json'))
    cloud_audit=json.loads(z.read('RUN304_INDEPENDENT_AUDIT.json'))
local_sources=json.loads((ROOT/'RUN304_FROZEN_SOURCES.json').read_text())
local_raw=json.loads((ROOT/'RUN304_RAW_FUNCTIONAL.json').read_text())
local_audit=json.loads((ROOT/'RUN304_INDEPENDENT_AUDIT.json').read_text())
assert cloud_sources['python']!=local_sources['python']
assert cloud_sources['records']==local_sources['records']
assert cloud_raw['rows']==local_raw['rows']
assert cloud_raw['passed']==local_raw['passed']==1536
assert cloud_raw['failed']==local_raw['failed']==0
assert cloud_audit['records_checked']==local_audit['records_checked']==1536
assert cloud_audit['discrepancies']==local_audit['discrepancies']==0
assert cloud_audit['classification_differences']==local_audit['classification_differences']==512
assert cloud_audit['group_counts']==local_audit['group_counts']
report={'schema':'ksynth1-run304-independent-cloud-compare-v1',
    'original_cloud_run':40614571206,'original_cloud_artifact':12784172977,
    'cloud_zip_sha256':hashlib.sha256(ZIP.read_bytes()).hexdigest(),
    'cloud_manifest_entries_verified_total':len(verified),
    'cloud_manifest_entries_total':len(manifest),
    'cloud_python':cloud_sources['python'],'local_python':local_sources['python'],
    'source_rows_identical':len(cloud_sources['records']),
    'functional_rows_identical':len(cloud_raw['rows']),
    'classification_changes_identical':512,'discrepancies':0,
    'environment_metadata_only_difference':'full source-manifest root differs because Python sys.version is included; source-only digest remains frozen'}
(ROOT/'RUN304_CLOUD_INDEPENDENT_VERIFY.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps(report,sort_keys=True))
