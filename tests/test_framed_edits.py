import random
import pytest
from lattice.semantic_edits import Program, InvalidProgram, cases
from lattice.framed_edits import FramedProgram, BoundRule


def test_read_expansion_preserves_edit_without_oracle_or_manual_rewrite():
    p = Program(("auth", "owner", "blocked"),
                (("read", "auth and not blocked"), ("edit", "read and owner"), ("ship", "edit")))
    old = FramedProgram.from_program(p)
    new = old.edit({"read": "not blocked"}, {"read"})
    for values in cases(p.inputs):
        assert new.run(values)["edit"] == old.run(values)["edit"]
        assert new.run(values)["ship"] == old.run(values)["ship"]
        assert new.run(values)["read"] == (not values["blocked"])


def test_explicit_propagation_and_captured_semantics_across_edits():
    p = Program(("a", "b"), (("read", "a"), ("edit", "read and b")))
    one = FramedProgram.from_program(p).edit({"read": "True"}, {"read"})
    two = one.edit({"edit": "read and b"}, {"edit"})
    assert one.run({"a": False, "b": True}) == {"read": True, "edit": False}
    assert two.run({"a": False, "b": True}) == {"read": True, "edit": True}
    propagated = FramedProgram.from_program(p).edit({"read": "True"}, {"read", "edit"})
    assert propagated.run({"a": False, "b": True}) == two.run({"a": False, "b": True})


def test_authority_is_enforced_and_cycles_rejected():
    p = FramedProgram.from_program(Program(("a",), (("read", "a"), ("edit", "read"))))
    with pytest.raises(InvalidProgram): p.edit({"edit": "True"}, {"read"})
    with pytest.raises(InvalidProgram): p.edit({"read": "edit", "edit": "read"}, {"read", "edit"})
    # A reference to a protected prior version is not a new-version cycle.
    p.edit({"read": "edit"}, {"read"})


def test_forged_versioned_state_cannot_introduce_cycles_or_unbound_refs():
    with pytest.raises(InvalidProgram):
        FramedProgram(("a",), (BoundRule("read", (("read", 0),)),), (("read", 0),), (("read", "read"),))
    with pytest.raises(InvalidProgram):
        FramedProgram(("a",), (BoundRule("missing", ()),), (("read", 0),), (("read", "missing"),))


def test_random_long_edit_sequences_frame_and_native_lowering():
    rng = random.Random(20261002)
    for _ in range(40):
        p = FramedProgram.from_program(Program(("a", "b", "c", "_lattice_v0"),
            (("read", "a or b"), ("edit", "read and c"), ("ship", "edit and _lattice_v0"))))
        for _ in range(10):
            name = rng.choice(["read", "edit", "ship"])
            other = rng.choice(["read", "edit", "ship"])
            if other == name: other = "a"
            allowed = {name}
            new = p.edit({name: f"{other} {rng.choice(['and', 'or'])} {rng.choice(['b', 'c'])}"}, allowed)
            scope = {"__builtins__": {}}
            exec(compile(new.lower_python(), "<trusted-lowering>", "exec"), scope)
            for values in cases(p.inputs):
                old, current = p.run(values), new.run(values)
                for k in old:
                    if k not in allowed: assert old[k] == current[k]
                assert tuple(current.values()) == scope["policy"](**values)
            p = new
