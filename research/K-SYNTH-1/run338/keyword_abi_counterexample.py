"""Two-file necessity false positive induced by a keyword-only ABI rename.

Synthetic executable counterexample. This is NOT a claim that Rich's semantic
fix is confined to one file; it disproves the general inference from a 2x2
pass/fail matrix to semantic two-component necessity.
"""

def base_caller(callee, text, width):
    return callee(text, max_size=width)

def ref_caller(callee, text, width):
    return callee(text, width=width)

def base_callee(text, max_size):
    return text[:max_size][::-1]

def ref_callee(text, width):
    return text[:width]

def compatible_ref_callee(text, max_size=None, width=None):
    assert (max_size is None) != (width is None)
    return text[:max_size if width is None else width]

def test():
    cases = []
    for a, caller in (("base", base_caller), ("ref", ref_caller)):
        for b, callee in (("base", base_callee), ("ref", ref_callee)):
            try:
                value = caller(callee, "ABCDE", 3)
                cases.append((a, b, value, value == "ABC"))
            except TypeError:
                cases.append((a, b, "TypeError", False))
    assert cases == [
        ("base", "base", "CBA", False),
        ("base", "ref", "TypeError", False),
        ("ref", "base", "TypeError", False),
        ("ref", "ref", "ABC", True),
    ]
    assert base_caller(compatible_ref_callee, "ABCDE", 3) == "ABC"
    assert ref_caller(compatible_ref_callee, "ABCDE", 3) == "ABC"
    return cases

if __name__ == "__main__":
    print(test())
