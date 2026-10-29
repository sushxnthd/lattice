"""Finite counterexample: joint multi-file necessity does not imply interaction.

This is a deterministic mathematical test over the original frozen Run340
public-API target outcomes, not a new model run or reference-free prediction.
"""

def y(mode, sync_ref, async_ref):
    if mode == "sync":
        return int(sync_ref)
    if mode == "async":
        return int(async_ref)
    raise ValueError(mode)

def interaction(mode):
    return y(mode, 1, 1) - y(mode, 1, 0) - y(mode, 0, 1) + y(mode, 0, 0)

if __name__ == "__main__":
    modes = ("sync", "async", "sync", "async")
    outcomes = {
        "base_base": sum(y(m, 0, 0) for m in modes),
        "ref_sync": sum(y(m, 1, 0) for m in modes),
        "ref_async": sum(y(m, 0, 1) for m in modes),
        "ref_ref": sum(y(m, 1, 1) for m in modes),
    }
    assert outcomes == {"base_base": 0, "ref_sync": 2, "ref_async": 2, "ref_ref": 4}
    assert all(interaction(m) == 0 for m in modes)
    assert all(y(m, 1, 1) == 1 for m in modes)
    assert any(y(m, 1, 0) == 0 for m in modes)
    assert any(y(m, 0, 1) == 0 for m in modes)
    print("PASS: both files necessary for full coverage, but each target interaction = 0")
