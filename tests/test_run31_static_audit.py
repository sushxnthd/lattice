import json
import pytest
from research.run31_static_audit import extract, strict_json, audit
from research.run31_pilot import run

def test_python_valid_and_invalid():
    valid=json.dumps({'interface':'python','symbol':'int_to_bytes',
                      'replacement':'def int_to_bytes(num: int) -> bytes:\n    return b""\n'})
    assert extract('B',valid)['kind']=='function'
    assert extract('D',valid)['kind']=='function'
    with pytest.raises(ValueError):
        extract('B',valid+' garbage')
    with pytest.raises(ValueError):
        extract('B',json.dumps({'interface':'python','symbol':'bytes_to_int','replacement':'def bytes_to_int(x): return 0'}))

def test_lattice_same_function():
    valid=json.dumps({'interface':'lattice','scope':{'symbol':'int_to_bytes'},
                      'change':{'source':'def int_to_bytes(num: int) -> bytes:\n    return b""\n'}})
    assert extract('C',valid)['kind']=='function'
    with pytest.raises(ValueError):
        extract('C',valid.replace('lattice','python'))

def test_compile_rejects_return_outside_function():
    payload=json.dumps({'interface':'python','symbol':'int_to_bytes',
                        'replacement':'return 1'})
    with pytest.raises(SyntaxError):
        extract('B',payload)

def test_duplicate_keys_rejected():
    with pytest.raises(ValueError):
        strict_json('{"interface":"python","interface":"lattice"}')

def test_dry_run_not_scored(tmp_path):
    run(tmp_path/'run')
    result=audit(tmp_path/'run')
    assert result['status']=='STATIC_FORMAT_AUDIT_NOT_HIDDEN_TEST_SCORING'
    assert all(row['format_valid'] is None for row in result['rows'])
