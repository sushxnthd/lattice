"""Regression and adversarial tests for epoch-addressed semantic transactions."""
import itertools
import pytest
from lattice.semantic_edits import Program, InvalidProgram
from lattice.framed_edits import FramedProgram
from lattice.epoch_editor import EpochEditor, EpochConflict, state_commit


def fixture():
    return FramedProgram.from_program(Program(('a', 'b'), (
        ('gate', 'a and b'), ('endpoint', 'gate or b'), ('audit', 'not gate'))))


def test_historical_ref_persists_across_recompilation():
    h = EpochEditor(fixture())
    genesis = h.tip
    h.edit({'gate': 'not h0_gate'}, {'gate', 'endpoint'}, h.tip)
    h.edit({'gate': 'h0_gate and h1_gate'}, {'gate', 'endpoint'}, h.tip)
    h.edit({'gate': 'h1_gate or h0_gate'}, {'gate', 'endpoint'}, h.tip)
    assert h.verify(pinned_genesis=genesis, pinned_tip=h.tip)
    for a, b in itertools.product((False, True), repeat=2):
        vals = {'a': a, 'b': b}
        original = a and b
        assert h.at(0).run(vals)['gate'] == original
        assert h.at(1).run(vals)['gate'] == (not original)
        assert h.at(2).run(vals)['gate'] is False
        assert h.at(3).run(vals)['gate'] is True
        assert h.current.run(vals)['audit'] == (not original)
        assert h.current.run(vals)['endpoint'] is True


def test_stale_rejected_without_mutation():
    h = EpochEditor(fixture())
    stale = h.tip
    h.edit({'gate': 'h0_gate or a'}, {'gate', 'endpoint'}, h.tip)
    count = len(h.records)
    with pytest.raises(EpochConflict, match='stale'):
        h.edit({'gate': 'b'}, {'gate', 'endpoint'}, stale)
    assert len(h.records) == count and h.verify()


@pytest.mark.parametrize('patch,scope', [
    ({'audit': 'True'}, {'gate', 'endpoint'}),
    ({'gate': 'h9_gate'}, {'gate', 'endpoint'}),
    ({'gate': 'h0_unknown'}, {'gate', 'endpoint'}),
    ({'gate': 'gate'}, {'gate', 'endpoint'}),
    ({'gate': 'h0_gate or a'}, {'gate', 'absent'}),
    ({}, {'gate', 'endpoint'}),
])
def test_rejected_edits_are_atomic(patch, scope):
    h = EpochEditor(fixture())
    tip = h.tip
    with pytest.raises((InvalidProgram, EpochConflict, ValueError)):
        h.edit(patch, scope, tip)
    assert h.tip == tip and len(h.records) == 1


def test_forks_share_genesis_but_not_history():
    left, right = EpochEditor(fixture()), EpochEditor(fixture())
    left.edit({'gate': 'h0_gate'}, {'gate', 'endpoint'}, left.tip)
    right.edit({'gate': 'h0_gate'}, {'gate', 'endpoint', 'audit'}, right.tip)
    assert state_commit(left.current) != state_commit(right.current)
    assert left.tip != right.tip
    assert left.verify() and right.verify()


def test_authority_commitment_is_not_authentication():
    legit = EpochEditor(fixture())
    genesis = legit.tip
    legit.edit({'gate': 'not a'}, {'gate', 'endpoint'}, legit.tip)
    attacker = EpochEditor(fixture())
    attacker.edit({'audit': 'a'}, {'audit'}, attacker.tip)
    assert attacker.verify()  # Self-consistency does not establish authorization.
    assert not attacker.verify(pinned_tip=legit.tip)
    assert legit.verify(pinned_genesis=genesis, pinned_tip=legit.tip)


def test_258_repeated_three_epoch_exhaustive():
    # Stress test, NOT 258 independent real-repository issue samples.
    records = []
    for seed in range(258):
        before = FramedProgram.from_program(Program(('a', 'b'), (
            ('gate', ('a and b', 'a or b', 'a ^ b', 'not a')[seed % 4]),
            ('endpoint', 'gate or b'), ('audit', 'not gate'))))
        h = EpochEditor(before)
        h.edit({'gate': 'not h0_gate'}, {'gate', 'endpoint'}, h.tip)
        h.edit({'gate': 'h0_gate and h1_gate'}, {'gate', 'endpoint'}, h.tip)
        h.edit({'gate': 'h1_gate or h0_gate'}, {'gate', 'endpoint'}, h.tip)
        assert h.verify()
        for a, b in itertools.product((False, True), repeat=2):
            vals = {'a': a, 'b': b}
            g = before.run(vals)['gate']
            assert h.at(1).run(vals)['gate'] == (not g)
            assert h.at(2).run(vals)['gate'] is False
            assert h.at(3).run(vals)['gate'] is True
            assert h.at(3).run(vals)['audit'] == (not g)
        records.append((seed, h.tip))
    assert len(records) == 258
