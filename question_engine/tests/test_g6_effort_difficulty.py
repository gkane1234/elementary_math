"""Unit tests for meaningful cancel-step effort (place-value ÷10ⁿ free)."""

from __future__ import annotations

import math
import random

from question_engine.frameworks.number import (
    FindingPercentsEquivalentFractionsFramework,
    PartPartWholeRatioFramework,
    ComparingRatiosFramework,
    RatioFramework,
    meaningful_cancel_steps,
    strip_place_value_tens,
    _sample_ratio_inflate_k,
    continuous_ratio_inflate_max,
)


def test_strip_place_value_tens():
    assert strip_place_value_tens(1) == 1
    assert strip_place_value_tens(1000) == 1
    assert strip_place_value_tens(500) == 5  # one leftover 5 after ÷100? 500=5*100 → strip 100 → 5
    assert strip_place_value_tens(20) == 2
    assert strip_place_value_tens(24) == 24
    assert strip_place_value_tens(12) == 12


def test_meaningful_cancel_steps_place_value_free():
    # Pure place-value GCFs are free
    assert meaningful_cancel_steps(10) == 0
    assert meaningful_cancel_steps(100) == 0
    assert meaningful_cancel_steps(1000) == 0
    # Leftover non-10 factors count
    assert meaningful_cancel_steps(20) == 1  # leftover 2
    assert meaningful_cancel_steps(50) == 1  # leftover 5
    assert meaningful_cancel_steps(24) == 4  # 2^3 * 3
    assert meaningful_cancel_steps(12) == 3  # 2^2 * 3
    # 500:1000 style — gcd 500 → strip to 5 → 1 step (not "hard" magnitude)
    assert meaningful_cancel_steps(500) == 1
    assert meaningful_cancel_steps(math.gcd(500, 1000)) == 1
    assert meaningful_cancel_steps(math.gcd(24, 136)) >= 3


def test_inflate_k_targets_meaningful_steps_not_pure_tens():
    """High D inflate-k should usually have real cancel work, not only ×10ⁿ."""
    k_max = continuous_ratio_inflate_max({"difficulty": 25})
    assert k_max is not None and k_max >= 20
    meaningful = 0
    pure_tens = 0
    for seed in range(80):
        random.seed(seed)
        k = _sample_ratio_inflate_k(25.0, k_max, min_k=2)
        steps = meaningful_cancel_steps(k)
        if steps == 0 and k > 1:
            pure_tens += 1
        if steps >= 3:
            meaningful += 1
    assert pure_tens <= 8, f"too many pure place-value k: {pure_tens}"
    assert meaningful >= 40, f"not enough multi-step k: {meaningful}"


def test_intro_ratios_mode_split_and_effort_ramp():
    fw = RatioFramework(equivalent=False)
    # High D: always simplify form
    for seed in range(30):
        random.seed(9000 + seed)
        latex, _t, _a = fw.build_prompt({"difficulty": 20})
        assert "simplest form" in latex
    # Low D: mostly write-as-given
    word = 0
    for seed in range(40):
        random.seed(seed)
        latex, _t, _a = fw.build_prompt({"difficulty": 0})
        if "There are" in latex:
            word += 1
    assert word >= 25


def test_part_part_whole_and_comparing_not_standins():
    ppw = PartPartWholeRatioFramework()
    random.seed(1)
    latex, _t, ans = ppw.build_prompt({"difficulty": 0})
    assert "There are" in latex or "ratio" in latex.lower()
    assert ":" in str(ans)

    cmp = ComparingRatiosFramework()
    random.seed(2)
    latex, _t, ans = cmp.build_prompt({"difficulty": 5})
    assert "greater" in latex.lower() or "Compare" in latex or "equal" in latex.lower()


def test_comparing_ratios_closeness_and_simplify_ladder():
    """Harder D → closer unit rates AND more meaningful cancel work."""
    import re
    from fractions import Fraction

    from question_engine.frameworks.number import (
        _ratio_compare_max_rel_diff,
        _ratio_rel_diff,
    )

    fw = ComparingRatiosFramework()

    def parse_parts(latex: str) -> tuple[int, int, int, int] | None:
        m = re.search(r"frac\{(\d+)\}\{(\d+)\}.*?frac\{(\d+)\}\{(\d+)\}", latex)
        if m:
            return tuple(int(x) for x in m.groups())  # type: ignore[return-value]
        m = re.search(r"(\d+):(\d+).*?(\d+):(\d+)", latex)
        if m:
            return tuple(int(x) for x in m.groups())  # type: ignore[return-value]
        return None

    def stats(d: float, n: int = 50) -> tuple[float, float, float]:
        rels: list[float] = []
        steps: list[int] = []
        same_part = 0
        for seed in range(n):
            random.seed(10_000 + int(d) * 1000 + seed)
            latex, _t, _a = fw.build_prompt({"difficulty": d})
            parts = parse_parts(latex)
            assert parts is not None, latex
            a, b, c, e = parts
            v1, v2 = Fraction(a, b), Fraction(c, e)
            if v1 != v2:
                rels.append(_ratio_rel_diff(v1, v2))
            g1, g2 = math.gcd(a, b), math.gcd(c, e)
            steps.append(meaningful_cancel_steps(g1) + meaningful_cancel_steps(g2))
            if a == c or b == e:
                same_part += 1
        mean_rel = sum(rels) / max(1, len(rels))
        mean_steps = sum(steps) / len(steps)
        return mean_rel, mean_steps, same_part / n

    # Budget itself tightens with D.
    assert _ratio_compare_max_rel_diff(5) > _ratio_compare_max_rel_diff(15)
    assert _ratio_compare_max_rel_diff(15) > _ratio_compare_max_rel_diff(25)

    lo_rel, lo_steps, lo_same = stats(5)
    mid_rel, mid_steps, mid_same = stats(15)
    hi_rel, hi_steps, hi_same = stats(25)

    # Easy: mostly same-part, clearly separable, light cancel.
    assert lo_same >= 0.85
    assert mid_same <= 0.05
    assert hi_same <= 0.05
    assert lo_rel > mid_rel
    assert mid_rel > hi_rel
    assert hi_rel < 0.20
    assert mid_steps > lo_steps
    assert hi_steps >= mid_steps - 0.5  # allow small noise; high should not collapse
    assert hi_steps >= 4.0


def test_finding_percents_equiv_frac_unreduced_surface():
    fw = FindingPercentsEquivalentFractionsFramework()
    unreduced = 0
    for seed in range(40):
        random.seed(3000 + seed)
        latex, _t, ans = fw.build_prompt({"difficulty": 22})
        m = __import__("re").search(r"frac\{(\d+)\}\{(\d+)\}", latex)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if math.gcd(a, b) > 1:
                unreduced += 1
        assert ans is not None
    assert unreduced >= 15
