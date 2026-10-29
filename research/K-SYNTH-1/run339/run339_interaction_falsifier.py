"""Finite causal counterexample from Run339's audited Rich #3180 11 target cases.

Full 160-record functional traces, baseline source and independent auditor are in
the separately SHA-verified local Run339 archive. This script reproduces only
the *derived* interaction arithmetic; it does not rerun the historical source.
Rich #3180 remains NOT QUALIFIED. No model superiority claim.
"""

ORIGINAL = {
    (0, 0): (4, 0),   # (passed targets, TypeErrors) on 11 targets
    (0, 1): (0, 11),
    (1, 0): (0, 11),
    (1, 1): (11, 0),
}
ABI_FACTORED = {
    (0, 0): (4, 0),
    (0, 1): (11, 0),
    (1, 0): (4, 0),
    (1, 1): (11, 0),
}

def interaction(matrix):
    return matrix[(1, 1)][0] - matrix[(1, 0)][0] - matrix[(0, 1)][0] + matrix[(0, 0)][0]

def necessity(matrix):
    """True if full passes 11 and neither single-component variant does."""
    return matrix[(1, 1)][0] == 11 and matrix[(1, 0)][0] < 11 and matrix[(0, 1)][0] < 11

def check():
    assert interaction(ORIGINAL) == 15
    assert interaction(ABI_FACTORED) == 0
    assert necessity(ORIGINAL)
    assert not necessity(ABI_FACTORED)
    assert ABI_FACTORED[(0, 1)][0] == ABI_FACTORED[(1, 1)][0] == 11
    assert ABI_FACTORED[(0, 0)][0] == ABI_FACTORED[(1, 0)][0] == 4
    assert all(0 <= passes <= 11 and 0 <= errors <= 11 for passes, errors in ORIGINAL.values())
    return {
        "original_interaction": interaction(ORIGINAL),
        "abi_factored_interaction": interaction(ABI_FACTORED),
        "semantic_wrap_effect_on_frozen_cases": 0,
        "semantic_cells_effect_on_frozen_cases": 7,
        "qualified": False,
    }

if __name__ == "__main__":
    import json
    print(json.dumps(check(), sort_keys=True))
