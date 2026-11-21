"""Controlled wheel-byte reproducibility probe; not independent builds."""
import hashlib, io, json, zipfile

def wheel(payload, timestamp=(2020,1,1,0,0,0), order=('pkg/__init__.py','pkg-0.0.1.dist-info/WHEEL')):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in order:
            info=zipfile.ZipInfo(name,timestamp)
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,payload if name.endswith('.py') else b'Wheel-Version: 1.0\nGenerator: probe\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
    return out.getvalue()

def members(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        return {n:z.read(n) for n in z.namelist()}

def run():
    base=wheel(b'x=1\n')
    cases={'identical_rebuild':wheel(b'x=1\n'),
           'timestamp_only':wheel(b'x=1\n',(2022,1,1,0,0,0)),
           'entry_order_only':wheel(b'x=1\n',order=('pkg-0.0.1.dist-info/WHEEL','pkg/__init__.py')),
           'payload_change':wheel(b'x=2\n')}
    results={name:{'sha256':hashlib.sha256(data).hexdigest(),
                   'equal_to_base':data==base,
                   'same_member_payloads':members(data)==members(base)}
             for name,data in cases.items()}
    assert results['identical_rebuild']['equal_to_base']
    assert all(not results[n]['equal_to_base'] for n in ('timestamp_only','entry_order_only','payload_change'))
    assert results['timestamp_only']['same_member_payloads']
    assert results['entry_order_only']['same_member_payloads']
    assert not results['payload_change']['same_member_payloads']
    return {'base_sha256':hashlib.sha256(base).hexdigest(),'cases':results,
            'conclusion':'ZIP timestamp and member ordering change wheel bytes without changing extracted payloads. No independent build attested.'}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
