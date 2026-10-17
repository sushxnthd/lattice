"""Exact design audit; no model calls or frozen holdout access."""
from research.run83.exact_design_audit import N, two_sided_p, exact_power


def test_exact_significance_region():
    significant = {(a, b) for a in range(N + 1) for b in range(N - a + 1)
                   if two_sided_p(a, b) < 0.05}
    assert significant == {(6, 0), (0, 6)}


def test_ten_point_effect_has_negligible_six_pair_power():
    assert abs(exact_power(.1, 0) - 1e-6) < 1e-12
    assert abs(exact_power(.3, .2) - .000793) < 1e-12


def test_paired_resolution():
    assert 1 / N > .1
    assert two_sided_p(6, 0) == .03125
    assert two_sided_p(5, 0) == .0625
