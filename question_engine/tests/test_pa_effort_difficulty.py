"""Unit tests for Pre-Algebra continuous-D effort scorers and F↔D ladder."""

from __future__ import annotations

import random

from question_engine.frameworks.number import FractionDecimalConvertFramework
from question_engine.ml.effort import (
    effort_equations,
    effort_factoring,
    effort_fraction_decimal_convert,
    effort_fraction_ops,
    effort_gcf,
    effort_integer_ops,
    effort_interest,
    effort_lcm,
    effort_place_value_rounding,
    effort_polynomials,
    effort_proportions,
    effort_simplify_fractions,
    effort_slope,
    effort_squares_roots,
    effort_systems,
    effort_writing_numbers_words,
    has_effort_scorer,
    score_effort,
)


PA_FIRST_TRANCHE = [
    "pa_naming_decimal_places_and_rounding",
    "pa_writing_numbers_with_words",
    "pa_integers_adding_and_subtracting",
    "pa_integers_multiplying",
    "pa_integers_dividing",
    "pa_factoring",
    "pa_greatest_common_factor",
    "pa_least_common_multiple",
    "pa_simplifying_fractions",
    "pa_converting_fractions_and_decimals",
    "pa_fractions_decimals_and_percents",
    "pa_simple_and_compound_interest",
    "pa_squares_and_square_roots",
    "pa_markup_discount_and_tax",
]

PA_SECOND_TRANCHE = [
    "pa_fractions_add_like",
    "pa_fractions_subtract_like",
    "pa_fractions_add_unlike",
    "pa_fractions_subtract_unlike",
    "pa_fractions_multiply",
    "pa_fractions_divide",
    "pa_equations_one_step_word_problems",
    "pa_equations_two_step_word_problems",
    "pa_equations_multi_step_equations",
    "pa_multi_step_inequalities",
    "pa_checking_for_a_proportion",
    "pa_proportions_word_problems",
    "pa_slope",
    "pa_writing_linear_equations",
    "pa_graphing_systems_of_equations",
    "pa_systems_substitution",
    "pa_systems_word_problems",
    "pa_polynomials_simplifying",
    "pa_polynomials_adding_and_subtracting",
    "pa_polynomials_multiplying",
]


def test_pa_first_tranche_scorers_registered():
    for tid in PA_FIRST_TRANCHE:
        assert has_effort_scorer(tid), tid
    # G6 aliases for shared generators
    assert has_effort_scorer("g6_factoring")
    assert has_effort_scorer("g6_greatest_common_factor")
    assert has_effort_scorer("g6_least_common_multiple")


def test_pa_second_tranche_scorers_registered():
    for tid in PA_SECOND_TRANCHE:
        assert has_effort_scorer(tid), tid


def test_integer_ops_signs_and_nonint_matter_more_than_magnitude():
    e_easy, _ = effort_integer_ops(r"3 + 4", "7")
    e_signs, f_signs = effort_integer_ops(r"-8 - (-3)", "-5")
    e_nonint, f_nonint = effort_integer_ops(r"17 \div 5", r"\frac{17}{5}")
    assert e_signs > e_easy
    assert f_signs.get("op") == "-"
    assert e_nonint > e_easy + 3
    assert f_nonint.get("nonint") is True


def test_factoring_omega_not_large_semiprime_theater():
    e_small, f_small = effort_factoring(
        r"\text{Write the prime factorization of } 12", "2^2 \\cdot 3"
    )
    e_many, f_many = effort_factoring(
        r"\text{Write the prime factorization of } 360", "2^3 \\cdot 3^2 \\cdot 5"
    )
    e_semi, f_semi = effort_factoring(
        r"\text{Write the prime factorization of } 134", "2 \\cdot 67"
    )
    assert f_small["omega"] == 3
    assert f_many["omega"] >= 5
    assert e_many > e_small
    # 2×67 is only Ω=2 — should not outscore a multi-factor 360.
    assert f_semi["omega"] == 2
    assert e_semi < e_many


def test_gcf_lcm_and_simplify_use_meaningful_steps():
    e_g, fg = effort_gcf(r"\text{Find the GCF of } 12, 18", "6")
    e_g3, _ = effort_gcf(r"\text{Find the GCF of } 72, 144, 216", "72")
    assert e_g3 > e_g
    assert fg["gcf"] == 6

    e_l, _ = effort_lcm(r"\text{Find the LCM of } 4, 6", "12")
    assert e_l >= 3.5

    e0, f0 = effort_simplify_fractions(r"\text{Simplify } \frac{2}{6}.", r"\frac{1}{3}")
    e_hard, f_hard = effort_simplify_fractions(
        r"\text{Simplify } \frac{48}{216}.", r"\frac{2}{9}"
    )
    assert f0["steps"] >= 1
    assert f_hard["steps"] >= f0["steps"]
    assert e_hard > e0


def test_fd_convert_and_relating_alias():
    e_easy, _ = effort_fraction_decimal_convert(
        r"\text{Write } \frac{1}{2} \text{ as a decimal.}", "0.5"
    )
    e_hard, _ = effort_fraction_decimal_convert(
        r"\text{Write } 0.0625 \text{ as a fraction in simplest form.}",
        r"\frac{1}{16}",
    )
    assert e_hard > e_easy + 3

    y, feats = score_effort(
        "pa_fractions_decimals_and_percents",
        r"\text{Write } 12.5\% \text{ as a fraction in simplest form.}",
        r"\frac{1}{8}",
    )
    assert y is not None and y >= 10
    assert isinstance(feats, dict)


def test_interest_compound_harder_than_simple():
    e_s, fs = effort_interest(
        r"\text{Alex invests \$500 at 5\% simple interest for 2 years. "
        r"How much interest is earned?}",
        r"\$50",
    )
    e_c, fc = effort_interest(
        r"\text{Alex invests \$5000 at 6.5\% interest compounded monthly "
        r"for 10 years. How much interest is earned?}",
        r"\$...",
    )
    assert fc["compound"] is True
    assert fs["compound"] is False
    assert e_c > e_s + 4


def test_place_words_squares_scorers():
    e_tenth, _ = effort_place_value_rounding(
        r"\text{Round } 10.65 \text{ to the nearest tenth.}", "10.7"
    )
    e_thou, _ = effort_place_value_rounding(
        r"\text{What digit is in the thousandths place of } 12.456?", "6"
    )
    assert e_thou > e_tenth

    e_small, _ = effort_writing_numbers_words(r"\text{Write } 20 \text{ in words.}", "twenty")
    e_big, _ = effort_writing_numbers_words(
        r"\text{Write } 2500000 \text{ in words.}", "two million..."
    )
    assert e_big > e_small + 5

    e_sq, fs = effort_squares_roots(r"7^{2}", "49")
    e_root, fr = effort_squares_roots(r"\sqrt{49}", "7")
    e_np, fn = effort_squares_roots(r"\sqrt{50}", r"5\sqrt{2}")
    assert fs["mode"] == "square" and e_sq < 8
    assert fr.get("perfect") is True
    assert fn.get("perfect") is False
    assert e_np > e_root + 4


def test_fraction_ops_unlike_and_cancel_harder():
    e_like, fl = effort_fraction_ops(r"\frac{1}{5} + \frac{2}{5}", r"\frac{3}{5}")
    e_unlike, fu = effort_fraction_ops(r"\frac{1}{4} + \frac{1}{6}", r"\frac{5}{12}")
    assert fu.get("like_denoms") is False
    assert fl.get("like_denoms") is True
    assert e_unlike > e_like

    e_nocancel, _ = effort_fraction_ops(r"\frac{3}{4} \cdot \frac{1}{5}", r"\frac{3}{20}")
    e_cancel, fc = effort_fraction_ops(
        r"-\frac{14}{15} \cdot \frac{20}{21}", r"-\frac{8}{9}"
    )
    assert fc.get("op") == "*"
    assert fc.get("cancel", 0) >= 1
    assert e_cancel > e_nocancel


def test_equations_proportions_slope_systems_polys():
    e_one, _ = effort_equations(
        r"\text{Taylor thinks of a number. After a one-step change, "
        r"the equation is $2x = 10$. What was the number?}",
        "x = 5",
    )
    e_multi, fm = effort_equations(
        r"\left(x - 3\right)3 - x + 6 = \left(x - 2\right)\left(-2\right) + 7x",
        "x = 1",
    )
    assert e_multi > e_one
    assert fm.get("parens", 0) >= 2

    e_prop, _ = effort_proportions(r"\text{Solve: } \frac{6}{x} = \frac{21}{4}", r"x = \frac{8}{7}")
    assert e_prop >= 6

    e_slope_easy, _ = effort_slope(
        r"\text{Find the slope of the line through } (0, 0) \text{ and } (2, 4).",
        "2",
    )
    e_slope_hard, fs = effort_slope(
        r"\text{Find the slope of the line through } (-5, -8) \text{ and } (-6, -5).",
        "-3",
    )
    assert e_slope_hard >= e_slope_easy
    assert "dx" in fs

    e_sys, _ = effort_systems(
        r"\begin{cases} y = x + 10 \\ x + 11y = 86 \end{cases}",
        "(x, y) = (-2, 8)",
    )
    assert e_sys >= 4

    e_add, _ = effort_polynomials(
        r"\text{Simplify: } \left(4x^{3} + 4x^{2} + 5\right) + \left(x^{3} + 3\right)",
        r"5x^{3} + 4x^{2} + 8",
    )
    e_mul, fm = effort_polynomials(
        r"\text{Multiply: } \left(2x^{2} - 4\right)\left(2x + 2\right)",
        r"4x^{3} + 4x^{2} - 8x - 8",
    )
    assert fm.get("op") == "multiply"
    assert e_mul > e_add


def test_fd_convert_framework_climbs_with_continuous_d():
    """High D should prefer awkward terminating decimals (eighths/sixteenths)."""
    fw = FractionDecimalConvertFramework()
    hard_markers = (
        "0.125",
        "0.375",
        "0.625",
        "0.875",
        "0.0625",
        "0.1875",
        "0.325",
        "\\frac{1}{8}",
        "\\frac{3}{8}",
        "\\frac{5}{8}",
        "\\frac{7}{8}",
        "\\frac{1}{16}",
        "\\frac{3}{16}",
        "\\frac{13}{40}",
    )

    def _hard_hits(d: float, n: int = 80) -> int:
        hard = 0
        for seed in range(n):
            random.seed(seed)
            latex, _t, _a = fw.build_prompt({"difficulty": d})
            if any(m in latex for m in hard_markers):
                hard += 1
        return hard

    hard0 = _hard_hits(0.0)
    hard25 = _hard_hits(25.0)
    assert hard0 <= 5, f"low D should avoid hard bank: hard={hard0}"
    assert hard25 >= 40, f"high D should hit hard bank: hard={hard25}"
    assert hard25 > hard0
