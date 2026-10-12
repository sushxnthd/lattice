import hashlib
import json
import pytest
from research.run31_pilot import ARMS, COMMON, make_prompts, run, sha, canonical

def test_arm_prompts_share_common_source():
    prompts = make_prompts()
    assert set(prompts) == set(ARMS)
    for arm in ARMS:
        assert canonical(COMMON).decode() in prompts[arm]
        assert 'int_to_bytes' in prompts[arm]
    assert len(set(prompts.values())) == 4

def test_dry_run_preserves_bytes(tmp_path):
    result = run(tmp_path / 'run')
    assert result['status'] == 'DRY_RUN_NO_MODEL'
    assert len(result['rows']) == 4
    assert all(r['status'] == 'PROMPT_ONLY_NOT_INFERENCE' for r in result['rows'])
    freeze = json.loads((tmp_path / 'run' / 'freeze.json').read_text())
    prompts = json.loads((tmp_path / 'run' / 'prompts.json').read_text())
    assert freeze['prompts_sha256'] == {a: sha(prompts[a].encode()) for a in ARMS}
    assert result['freeze_sha256'] == hashlib.sha256((tmp_path / 'run' / 'freeze.json').read_bytes()).hexdigest()

def test_no_overwrite(tmp_path):
    run(tmp_path / 'run')
    with pytest.raises(ValueError):
        run(tmp_path / 'run')

def test_only_loopback(tmp_path):
    with pytest.raises(ValueError):
        run(tmp_path / 'run', 'https://example.com/v1/chat/completions')
