"""Adversarial tests for unique anchored addressing."""
import pytest
from multifile_editor import sha256,PatchRejected,compile_patch
from anchored_compiler import compile_anchored_patch,posthoc_readdress_line_patch

S={'src/a.py':b'def compute(x):\n    return x + 1\n'}
def patch(old='    return x + 1\n', replacement='    return x + 2\n', **kw):
    return {'edits':[{'path':'src/a.py','file_sha256':sha256(S['src/a.py']),
                       'old_text':old,'replacement':replacement,**kw}]}

def test_unique_anchor_accepts():
    c=compile_anchored_patch(S,patch(),set(S))
    assert b'x + 2' in c.files['src/a.py']

def test_original_line_patch_is_not_mutated():
    wrong=patch(start_line=1,end_line=1)
    with pytest.raises(PatchRejected):compile_patch(S,wrong,set(S))
    assert posthoc_readdress_line_patch(S,wrong,set(S)).files['src/a.py'].endswith(b'x + 2\n')

def test_reject_ambiguous_anchor():
    s={'x.py':b'a=1\na=1\n'}
    e={'edits':[{'path':'x.py','file_sha256':sha256(s['x.py']),
                 'old_text':'a=1\n','replacement':'a=2\n'}]}
    with pytest.raises(PatchRejected,match='exactly once'):compile_anchored_patch(s,e,set(s))

def test_reject_empty_anchor():
    with pytest.raises(PatchRejected,match='empty'):compile_anchored_patch(S,patch(old=''),set(S))

def test_reject_stale_hash():
    p=patch();p['edits'][0]['file_sha256']='0'*64
    with pytest.raises(PatchRejected,match='stale'):compile_anchored_patch(S,p,set(S))

def test_reject_unauthorized():
    with pytest.raises(PatchRejected,match='unauthorized'):compile_anchored_patch(S,patch(),set())

def test_reject_syntax_error():
    with pytest.raises(PatchRejected,match='syntax'):compile_anchored_patch(S,patch(replacement='    return (\n'),set(S))

def test_reject_overlapping():
    p=patch();p['edits'].append(dict(p['edits'][0]))
    with pytest.raises(PatchRejected,match='overlapping'):compile_anchored_patch(S,p,set(S))

def test_reject_non_line_aligned():
    with pytest.raises(PatchRejected,match='exactly once'):compile_anchored_patch(S,patch(old='return x + 1'),set(S))
