"""G6 number leaves: notes-shaped D=0, named methods, skeleton_pattern stamps."""

from __future__ import annotations

import random
import re

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.number import (
    DecimalArithmeticFramework,
    FractionDivideWordFramework,
    IdentifyPropertyFramework,
)
from question_engine.generators import GENERATORS


def _one(type_id: str, d: float, seed: int = 41):
    qs = _generate_for_type(
        type_id,
        {
            "difficulty": d,
            "seed": seed,
            "count": 1,
            "include_answer_key": True,
        },
    )
    assert qs
    return qs[0]


def test_ratio_and_decimal_stamp_skeleton_pattern():
    q = _one("g6_introduction_to_ratios", 0.0)
    assert (q.metadata or {}).get("skeleton_pattern") == "Ratio"
    q2 = _one("g6_decimal_addition", 0.0)
    assert (q2.metadata or {}).get("skeleton_pattern") == "DecimalAdd"
    q3 = _one("g6_numeric_expressions_and_order_of_operations", 0.0)
    assert (q3.metadata or {}).get("skeleton_pattern") == "OrderOfOperations"


def test_decimal_addition_d0_is_one_place_plus():
    q = _one("g6_decimal_addition", 0.0, seed=41)
    latex = q.prompt_latex or ""
    assert "+" in latex
    assert re.search(r"\d+\.\d", latex)


def test_decimal_addition_keeps_plus_for_signed_addends():
    fw = DecimalArithmeticFramework("+")
    random.seed(7)
    latex, _t, _a = fw.build_prompt({"difficulty": 22, "allow_negative": True})
    # Addition leaf must not collapse ``a + (-b)`` into a subtraction item.
    if "-" in latex and "+" not in latex:
        raise AssertionError(f"addition displayed as subtraction: {latex}")


def test_decimal_mul_equiv_fractions_shows_fractions():
    q = _one("g6_decimal_multiplication_with_equivalent_fractions", 0.0, seed=41)
    latex = q.prompt_latex or ""
    assert r"\frac" in latex
    # Place-value method: denom is 10^places, not a reduced equivalent.
    dens = [int(m) for m in re.findall(r"\\frac\{\d+\}\{(\d+)\}", latex)]
    assert dens and all(d in (10, 100, 1000) for d in dens)
    assert (q.metadata or {}).get("skeleton_pattern") == "DecimalMulFrac"


def test_fraction_of_whole_is_part_of_whole_not_half_of_x():
    q = _one("g6_what_fraction_of_a_whole", 0.0, seed=41)
    latex = q.prompt_latex or ""
    assert "What fraction of" in latex
    assert r"\frac{1}{2} \text{ of }" not in latex
    fw = FractionDivideWordFramework(mode="whole")
    random.seed(3)
    latex2, _t, ans = fw.build_prompt({"difficulty": 0})
    assert "What fraction of" in latex2
    assert ans


def test_identify_property_mixes_beyond_zero_at_high_d():
    fw = IdentifyPropertyFramework()
    names: set[str] = set()
    for seed in range(40):
        random.seed(seed + 200)
        name, latex, _t = fw._build_example({"difficulty": 16})
        names.add(name)
        assert "=" in latex
    assert "zero property of multiplication" in names
    assert any("commutative" in n or "associative" in n or n == "distributive property" for n in names)
    assert len(names) >= 3


def test_intro_percents_and_comparing_rates_attach_svg():
    shade = _one("g6_introduction_to_percents", 0.0)
    assert "<svg" in str((shade.metadata or {}).get("diagram_svg") or "")
    rate = _one("g6_comparing_rates", 0.0)
    assert "<svg" in str((rate.metadata or {}).get("diagram_svg") or "")


def test_ooo_d0_is_short_evaluate():
    q = _one("g6_numeric_expressions_and_order_of_operations", 0.0, seed=41)
    latex = q.prompt_latex or ""
    assert latex
    assert "solve" not in latex.lower()
    assert q.answer_latex


def test_generators_dict_covers_g6_number_keys():
    for key in (
        "g6_introduction_to_ratios",
        "g6_greatest_common_factor",
        "g6_long_division_with_remainders",
        "g6_absolute_values",
        "g6_factoring",
    ):
        assert key in GENERATORS
        qs = GENERATORS[key](key, {"difficulty": 0, "count": 1, "seed": 2, "include_answer_key": True})
        assert qs and qs[0].prompt_latex
