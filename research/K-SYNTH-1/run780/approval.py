"""Experimental HMAC approval verification. Not a public-key release signature."""
import hashlib, hmac, json, re
FIELDS=('schema','repository','source_commit','artifact_sha256','release_tag')
HEX=re.compile(r'[0-9a-f]{64}\Z')
COMMIT=re.compile(r'[0-9a-f]{40}\Z')
def canonical(p):
    if not isinstance(p,dict) or set(p)!=set(FIELDS): raise ValueError('UNKNOWN: schema')
    if p['schema']!='lattice-alpha-approval-v1' or p['repository']!='sushxnthd/lattice': raise ValueError('UNKNOWN: scope')
    if not isinstance(p['source_commit'],str) or not COMMIT.fullmatch(p['source_commit']): raise ValueError('UNKNOWN: commit')
    if not isinstance(p['artifact_sha256'],str) or not HEX.fullmatch(p['artifact_sha256']): raise ValueError('UNKNOWN: digest')
    if not isinstance(p['release_tag'],str) or not re.fullmatch(r'v0\.[0-9]+\.[0-9]+a[0-9]+',p['release_tag']): raise ValueError('UNKNOWN: tag')
    return json.dumps(p,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()
def sign(p,key):
    if len(key)<32: raise ValueError('UNKNOWN: key')
    return hmac.new(key,b'lattice-release-approval-v1\0'+canonical(p),hashlib.sha256).hexdigest()
def verify(p,sig,key,wheel,commit,tag):
    if len(key)<32: return False
    try: data=canonical(p)
    except ValueError: return False
    if not isinstance(sig,str) or not HEX.fullmatch(sig): return False
    expected=hmac.new(key,b'lattice-release-approval-v1\0'+data,hashlib.sha256).hexdigest()
    return (hmac.compare_digest(expected,sig) and p['source_commit']==commit and p['release_tag']==tag and hmac.compare_digest(hashlib.sha256(wheel).hexdigest(),p['artifact_sha256']))
