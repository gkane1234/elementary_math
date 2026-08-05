"""Unit tests for Algebra 1 effort scorers (first + second + EA2e follow-up)."""

from __future__ import annotations

from question_engine.ml.effort import (
    effort_absolute_value,
    effort_completing_square_constant,
    effort_completing_square_solve,
    effort_compound_inequalities,
    effort_distributive,
    effort_equations,
    effort_evaluating_functions,
    effort_fraction_ops,
    effort_graph_linear_equation,
    effort_linear_write,
    effort_literal_equations,
    effort_order_of_operations,
    effort_percent_of_change,
    effort_poly_gcf,
    effort_poly_general_strategy,
    effort_poly_grouping,
    effort_poly_long_division,
    effort_poly_special,
    effort_polynomials,
    effort_properties_of_exponents,
    effort_proportions,
    effort_quadratic_discriminant,
    effort_quadratic_factor_solve,
    effort_quadratic_factoring,
    effort_quadratic_formula,
    effort_quadratic_square_roots,
    effort_radical_add_subtract,
    effort_radical_divide,
    effort_radical_equations,
    effort_radical_multiply,
    effort_radical_simplification,
    effort_rational_equations,
    effort_rational_expression_ops,
    effort_rational_simplification,
    effort_scientific_notation,
    effort_slope,
    effort_systems,
    effort_verbal_expressions,
    effort_wp_age,
    effort_wp_coin,
    effort_wp_consecutive,
    effort_wp_distance_rate_time,
    effort_wp_mixture,
    effort_wp_work,
    effort_graph_linear,
    effort_graph_transform,
    effort_markup_discount,
    has_effort_scorer,
    score_effort,
)

A1_FIRST_FAMILY = [
    "rational_add_subtract",
    "rational_multiply",
    "rational_divide",
    "percents",
    "percent_of_change",
    "scientific_notation_write",
    "scientific_notation_operations",
    "scientific_notation_add_subtract",
    "verbal_expressions",
    "order_of_operations",
    "distributive_property",
]

A1_SECOND_FAMILY = [
    "one_step_equations",
    "two_step_equations",
    "multi_step_equations",
    "solving_proportions",
    "properties_of_exponents",
    "polynomial_naming",
    "polynomial_add_subtract",
    "simplify_polynomials",
    "polynomial_multiply",
    "polynomial_multiply_special",
    "polynomial_factoring_common_factor",
    "rational_simplification",
    "rational_expression_simplification",
]

# Elementary Algebra 2e mining follow-up: PA aliases + factoring beyond GCF.
A1_EA2E_FOLLOWUP = [
    "slope",
    "more_on_slope",
    "writing_linear_equations",
    "systems_graphing",
    "systems_substitution",
    "systems_elimination",
    "systems_word_problems",
    "polynomial_factoring_grouping",
    "polynomial_factoring_special_cases",
    "quadratic_factoring",
    "polynomial_factoring_general_strategy",
    "quadratic_factoring_equations",
]

# Literals / inequality ladder / absolute value (continuous schema + scorers).
A1_INEQUALITY_LITERAL_FAMILY = [
    "literal_equations",
    "one_step_inequalities",
    "two_step_inequalities",
    "multi_step_inequalities",
    "compound_inequalities",
    "absolute_value_equations",
    "absolute_value_inequalities",
]

# Rational expression ×÷ + radical ± (continuous schema + scorers).
A1_RATIONAL_RADICAL_OPS = [
    "rational_expression_multiply_divide",
    "radical_add_subtract",
]

# Quadratic methods beyond factoring + radical ×÷/eqns + rational eqns (EA2e Ch 8–10).
A1_QUADRATIC_RADICAL_RATIONAL_EQ = [
    "quadratic_square_roots",
    "quadratic_completing_square_constant",
    "quadratic_completing_square_solve",
    "quadratic_formula",
    "quadratic_discriminant",
    "radical_multiply",
    "radical_divide",
    "radical_equations",
    "rational_expressions_equations",
]

# Orphans + WP stems + prompt-based graph leaves.
A1_ORPHAN_WP_GRAPH = [
    "polynomial_long_division",
    "radical_simplification",
    "mixture_word_problems",
    "distance_rate_time_word_problems",
    "work_word_problems",
    "age_word_problems",
    "coin_word_problems",
    "consecutive_integers_word_problems",
    "percent_word_problems",
    "evaluating_graphing_functions",
    "graphing_linear_equations",
    "graphing_absolute_value_equations",
    "graphing_systems_of_inequalities",
    "graphing_quadratic_functions",
    "graphing_quadratic_inequalities",
    "graphing_exponential_functions",
    "quadratic_solve_by_graphing",
    "visualizing_data",
    "scatter_plots",
]


def test_a1_first_family_scorers_registered():
    for tid in A1_FIRST_FAMILY:
        assert has_effort_scorer(tid), tid


def test_a1_second_family_scorers_registered():
    for tid in A1_SECOND_FAMILY:
        assert has_effort_scorer(tid), tid


def test_a1_ea2e_followup_scorers_registered():
    for tid in A1_EA2E_FOLLOWUP:
        assert has_effort_scorer(tid), tid


def test_a1_inequality_literal_family_scorers_registered():
    for tid in A1_INEQUALITY_LITERAL_FAMILY:
        assert has_effort_scorer(tid), tid


def test_a1_rational_radical_ops_scorers_registered():
    for tid in A1_RATIONAL_RADICAL_OPS:
        assert has_effort_scorer(tid), tid


def test_a1_quadratic_radical_rational_eq_scorers_registered():
    for tid in A1_QUADRATIC_RADICAL_RATIONAL_EQ:
        assert has_effort_scorer(tid), tid


def test_a1_orphan_wp_graph_scorers_registered():
    for tid in A1_ORPHAN_WP_GRAPH:
        assert has_effort_scorer(tid), tid


def test_rational_reuses_fraction_ops_and_slash_divide():
    e_like, fl = effort_fraction_ops(r"\frac{1}{5} + \frac{2}{5}", r"\frac{3}{5}")
    e_unlike, fu = effort_fraction_ops(r"\frac{1}{4} + \frac{1}{6}", r"\frac{5}{12}")
    assert e_unlike > e_like
    assert fu.get("like_denoms") is False

    e_div, fd = effort_fraction_ops(
        r"\left(\frac{1}{4}\right) / \left(\frac{1}{2}\right)",
        r"\frac{1}{2}",
    )
    assert fd.get("op") == "/"
    assert e_div >= 5.0

    y, _ = score_effort(
        "rational_divide",
        r"\left(\frac{14}{81}\right) / \left(\frac{42}{135}\right)",
        r"\frac{5}{9}",
    )
    assert y is not None and y >= 5.0


def test_percent_of_change_direction_and_awkwardness():
    e_nice, fn = effort_percent_of_change(
        r"\text{From 20 to 10, find the percent decrease.}",
        r"50\%",
    )
    e_tiny, ft = effort_percent_of_change(
        r"\text{From 20 to 19, find the percent decrease.}",
        r"5\%",
    )
    assert ft.get("dir") == "decrease"
    assert e_tiny > e_nice
    assert fn.get("pct_change") == 50.0


def test_percents_alias_formulas():
    y_easy, _ = score_effort("percents", r"\text{What is 20\% of 10?}", "2")
    y_hard, _ = score_effort(
        "percents",
        r"\text{24 is 59.9\% of what number?}",
        "40.07",
    )
    assert y_easy is not None and y_hard is not None
    assert y_hard > y_easy


def test_scientific_notation_modes():
    e_write, fw = effort_scientific_notation(
        r"\text{Write in scientific notation: } 120",
        r"1.2 \times 10^{2}",
    )
    e_big, _ = effort_scientific_notation(
        r"\text{Write in scientific notation: } 742000000",
        r"7.42 \times 10^{8}",
    )
    assert fw.get("mode") == "write"
    assert e_big > e_write

    e_same, fs = effort_scientific_notation(
        r"(1.4 \times 10^{1}) + (8.6 \times 10^{1})",
        r"1 \times 10^{2}",
    )
    e_mis, fm = effort_scientific_notation(
        r"(9.41 \times 10^{-1}) + (5.41 \times 10^{-3})",
        r"9.4641 \times 10^{-1}",
    )
    assert fm.get("exp_mismatch") is True
    assert e_mis > e_same
    assert fs.get("op") == "add"


def test_ooo_and_distributive_and_verbal():
    e_simple, _ = effort_order_of_operations(r"4 + 6 \div 3", "6")
    e_exp, fe = effort_order_of_operations(r"7 + 3 \cdot 5^{2}", "82")
    assert fe.get("exponent") is True
    assert e_exp > e_simple

    e_pos, _ = effort_distributive(r"6(7 - 5)", "12")
    e_neg, fn = effort_distributive(r"-7(1 - 1)", "0")
    assert fn.get("has_minus") is True
    assert e_neg >= e_pos

    e_prod, _ = effort_verbal_expressions(
        r"\text{the product of } 9 \text{ and a number}",
        "9x",
    )
    e_cons, fc = effort_verbal_expressions(
        r"\text{the sum of three consecutive even integers starting with a number}",
        r"x + (x + 2) + (x + 4)",
    )
    assert fc.get("consecutive") is True
    assert e_cons > e_prod


def test_equation_ladder_structure_not_magnitude():
    e_one, _ = effort_equations(r"x + 1 = 4", "x = 3")
    e_two, ft = effort_equations(r"2x + 1 = 1", "x = 0")
    e_multi, fm = effort_equations(
        r"-3\left(x + 1\right) + 4x + 3 = 2\left(x - 3\right) - 4x",
        "x = 1",
    )
    assert ft.get("two_step_shape") is True
    assert e_two > e_one
    assert e_multi > e_two
    assert not fm.get("inequality")  # \left must not false-trigger

    y, _ = score_effort("one_step_equations", r"5\alpha = \frac{5}{2}", r"\alpha = \frac{1}{2}")
    assert y is not None and y >= 5.0


def test_solving_proportions_var_placement():
    e_num, _ = effort_proportions(
        r"\text{Solve: } \frac{2}{3} = \frac{x}{4}",
        r"x = \frac{8}{3}",
    )
    e_den, fd = effort_proportions(
        r"\text{Solve: } \frac{48}{x} = \frac{120}{14}",
        r"x = \frac{28}{5}",
    )
    e_lin, fl = effort_proportions(
        r"\text{Solve: } \frac{12}{18} = \frac{y + 2}{6}",
        "y = 2",
    )
    assert fd.get("var_in_den") is True
    assert fl.get("linear_slot") is True
    assert e_den > e_num
    assert e_lin > e_num


def test_properties_of_exponents_pattern_ladder():
    e_prod, fp = effort_properties_of_exponents(r"x^{2} \cdot x^{3}", "x^{5}")
    e_quot, _ = effort_properties_of_exponents(r"\frac{x^{5}}{x^{2}}", "x^{3}")
    e_pow, fpow = effort_properties_of_exponents(r"\left(x^{3}\right)^{2}", "x^{6}")
    e_neg, fn = effort_properties_of_exponents(r"x^{-4}", r"\frac{1}{x^{4}}")
    e_sum, fs = effort_properties_of_exponents(r"x^{9} - x^{2}", "x^{9} - x^{2}")
    assert fp.get("pattern") == "product"
    assert fpow.get("pattern") == "power"
    assert fn.get("pattern") == "negative"
    assert fs.get("pattern") == "sum"
    assert e_pow > e_prod
    assert e_neg > e_quot
    assert e_sum > e_prod


def test_polynomial_ops_naming_and_gcf():
    e_name, fn = effort_polynomials(
        r"\text{Name the polynomial: } 4x^{4} + x^{2} + 1",
        r"\text{quartic}",
    )
    assert fn.get("op") == "naming"
    assert e_name >= 8.0

    e_add, _ = effort_polynomials(
        r"\text{Simplify: } \left(3x^{2} + 2\right) + \left(x^{2} + 3\right)",
        r"4x^{2} + 5",
    )
    e_mul, fm = effort_polynomials(
        r"\text{Multiply: } \left(-2y + 3\right)\left(5y^{2} - 4\right)",
        r"-10y^{3} + 15y^{2} + 8y - 12",
    )
    assert fm.get("op") == "multiply"
    assert e_mul > e_add

    e_easy, _ = effort_poly_gcf(r"\text{Factor: } 4x + 2", r"2\left(2x + 1\right)")
    e_hard, fg = effort_poly_gcf(
        r"\text{Factor: } 54x + 27x^{2}",
        r"9x\left(3x + 6\right)",
    )
    assert fg.get("gcf_var_pow") == 1
    assert e_hard > e_easy


def test_rational_simplification_degree_and_addends():
    e_easy, _ = effort_rational_simplification(
        r"\frac{x+2}{x^{2}-2x-8}",
        r"\frac{1}{x-4},\; x \neq -2",
    )
    e_hard, fh = effort_rational_simplification(
        r"\frac{3x^{3}+12x^{2}-36x}{3x^{3}+24x^{2}+12x-144}",
        r"\frac{x}{x+4},\; x \neq -6, 2",
    )
    assert fh.get("n_excluded") == 2
    assert e_hard > e_easy

    e_add, fa = effort_rational_simplification(
        r"\frac{4}{x} + \frac{1}{x}",
        r"\frac{5}{x}",
    )
    assert fa.get("multi_addend") is True
    assert e_add >= 8.0

    y, _ = score_effort(
        "rational_expression_simplification",
        r"\frac{5}{12x^{2}-x-1} + \frac{-22x-11}{(3x-1)(4x+1)(2x+3)}",
        r"\frac{-4}{(4x+1)(2x+3)},\; x \neq \frac{1}{3}, \frac{4}{3}",
    )
    assert y is not None and y >= 12.0


def test_literal_equations_form_depth():
    e_area, fa = effort_literal_equations(
        r"A = \ell w \quad \text{Solve for } w.",
        r"w = \frac{A}{\ell}",
    )
    e_vol, fv = effort_literal_equations(
        r"V = \ell w h \quad \text{Solve for } w.",
        r"w = \frac{V}{\ell h}",
    )
    assert fa.get("form") == "named_formula"
    assert e_vol > e_area
    assert fv.get("rhs_vars", 0) >= 2


def test_inequality_ladder_reuses_equations_and_compound():
    e_one, _ = effort_equations(r"x - 2 > -5", r"x > -3")
    e_multi, fm = effort_equations(
        r"-3x - 9 + 2\left(x + 3\right) > -8x + 2 + 3\left(x + 1\right)",
        r"x > 2",
    )
    assert fm.get("inequality") is True
    assert e_multi > e_one

    e_int, fi = effort_compound_inequalities(r"-1 < x < 1", r"-1 < x < 1")
    e_or, fo = effort_compound_inequalities(
        r"32x - 8 \leq -296 \text{ or } 8x + 10 > 186",
        r"x \leq -9 \text{ or } x > 22",
    )
    assert fi.get("style") == "interval"
    assert fo.get("style") == "or"
    assert e_or > e_int


def test_absolute_value_branching():
    e_eq, _ = effort_absolute_value(r"|x| = 6", r"x = -6 \text{ or } x = 6")
    e_ineq, fi = effort_absolute_value(r"|-2x + 4| > 2", r"x < 1 \text{ or } x > 3")
    assert fi.get("inequality") is True
    assert fi.get("shifted") is True
    assert e_ineq > e_eq


def test_rational_expression_ops_multiply_vs_divide_expand():
    e_mul, fm = effort_rational_expression_ops(
        r"\frac{\left(x+3\right)\left(x-2\right)}{x-1} \cdot \frac{x+4}{\left(x+2\right)\left(x-2\right)}",
        r"\frac{x^{2}+7x+12}{x^{2}+x-2},\; x \neq -2, 1, 2",
    )
    e_div, fd = effort_rational_expression_ops(
        r"\frac{25x^{2}-55x+24}{6x^{2}+17x+5} \div \frac{25x^{2}-20x+3}{6x^{2}+5x-25}",
        r"\frac{15x^{2}-49x+40}{15x^{2}+2x-1},\; x \neq -\frac{5}{2}, -\frac{1}{3}, \frac{1}{5}, \frac{3}{5}, \frac{5}{3}",
    )
    assert fm.get("op") == "multiply"
    assert fd.get("op") == "divide"
    assert fd.get("max_deg", 0) >= 2
    assert e_div > e_mul

    y, _ = score_effort(
        "rational_expression_multiply_divide",
        r"\frac{2x^{2}-x-45}{3x^{2}-20x+12} \cdot \frac{2x^{2}-9x-18}{5x^{2}-31x+30}",
        r"\frac{4x^{2}+24x+27}{15x^{2}-28x+12},\; x \neq \frac{2}{3}, \frac{6}{5}, 5, 6",
    )
    assert y is not None and y >= 10.0


def test_radical_add_subtract_like_vs_unsimplified():
    e_like, fl = effort_radical_add_subtract(r"6\sqrt{6} - \sqrt{6}", r"5\sqrt{6}")
    e_hard, fh = effort_radical_add_subtract(
        r"4\sqrt{50} - 2\sqrt{50} + 2\sqrt{32} - 8\sqrt{72}",
        r"-30\sqrt{2}",
    )
    assert fl.get("mode") == "like"
    assert fh.get("mode") == "unsimplified"
    assert fh.get("n_terms", 0) >= 3
    assert e_hard > e_like

    y, _ = score_effort("radical_add_subtract", r"8\sqrt{56} + 6\sqrt{504}", r"50\sqrt{14}")
    assert y is not None and y >= 6.0


def test_poly_factoring_beyond_gcf_ladder():
    e_dos, _ = effort_poly_special(r"x^{2} - 9", r"\left(x + 3\right)\left(x - 3\right)")
    e_a, fa = effort_quadratic_factoring(r"3x^{2}+33x+30", r"(3x+3)(x+10)")
    e_grp, fg = effort_poly_grouping(
        r"3x^{2} - 2x - 8 + 3\left(x^{3} + 2\right)",
        r"\left(x + 1\right)\left(3x^{2} - 2\right)",
    )
    assert e_a > e_dos
    assert e_grp >= e_dos
    y, _ = score_effort("polynomial_factoring_general_strategy", r"12x^{2} - 15x", r"3x\left(4x - 5\right)")
    assert y is not None and y >= 5.0


def test_systems_reuse_scorer():
    e_sub, fs = effort_systems(
        r"\begin{cases} y = -4x + 25 \\ x + 3y = 20 \end{cases}",
        r"(x, y) = (5, 5)",
    )
    e_wp, fw = effort_systems(
        r"\text{Taylor buys two items. The costs satisfy } \begin{cases} 3x + y = 11 \\ -x - y = -5 \end{cases}",
        r"x = 3,\ y = 2",
    )
    assert fs.get("isolated_y") is True
    assert fw.get("wp") is True
    assert e_wp > e_sub

    y, _ = score_effort(
        "systems_elimination",
        r"\begin{cases} 9x + 7y = -43 \\ 6x - 4y = -20 \end{cases}",
        r"(x, y) = (-4, -1)",
    )
    assert y is not None and y >= 6.0


def test_a1_aliases_slope_write_systems():
    e_eq, fe = effort_slope(r"\text{Find the slope of the line } y = -\frac{1}{3}x + 1.", r"-1/3")
    e_pts, fp = effort_slope(
        r"\text{Find the slope of the line through } (0, 0) \text{ and } (2, 4).",
        "2",
    )
    e_hard, fh = effort_slope(
        r"\text{Find the slope of the line through } (-5, -8) \text{ and } (-6, -5).",
        "-3",
    )
    assert fe.get("mode") == "from_equation"
    assert fe.get("fractional_m") is True
    assert fp.get("mode") == "two_point"
    assert e_eq >= 2.5
    assert e_hard >= e_pts
    assert "dx" in fh

    e_ps, fps = effort_linear_write(
        r"\text{Write the point-slope equation of the line with slope } 3 \text{ through } (1, 6).",
        r"y - 6 = 3(x - 1)",
    )
    e_two, ft = effort_linear_write(
        r"\text{Write an equation of the line through } (0, 4) \text{ and } (2, 12).",
        r"y = 4x + 4",
    )
    assert fps.get("mode") == "point_slope"
    assert ft.get("mode") == "two_points"
    assert e_two > e_ps

    e_sub, _ = effort_systems(
        r"\text{Solve: } \begin{cases} y = -\frac{3}{2}x + \frac{3}{2} \\ 9x + 6y = 7 \end{cases}",
        r"(x, y) = (1, 0)",
    )
    e_wp, fw = effort_systems(
        r"\text{Sam buys two items. The costs satisfy } \begin{cases} -3x + y = 0 \\ x - 5y = -14 \end{cases}",
        r"x = 1,\ y = 3",
    )
    assert fw.get("wp") is True
    assert e_wp > e_sub

    for tid in (
        "slope",
        "writing_linear_equations",
        "systems_elimination",
        "systems_word_problems",
    ):
        y, _ = score_effort(tid, r"y = 2x + 1", "2")
        assert y is not None, tid


def test_factoring_ladder_beyond_gcf():
    e_dos, fd = effort_poly_special(r"x^{2} - 16", r"\left(x + 4\right)\left(x - 4\right)")
    e_pst, fp = effort_poly_special(
        r"4x^{2} - 12x + 9",
        r"\left(2x - 3\right)^{2}",
    )
    assert fd.get("pattern") == "diff_squares"
    assert fp.get("pattern") == "perfect_square"
    assert e_pst > e_dos

    e_grp, fg = effort_poly_grouping(
        r"4x^{3} - 12x^{2} - 3x + 9",
        r"\left(x - 3\right)\left(4x^{2} - 3\right)",
    )
    assert fg.get("four_term") is True
    assert e_grp > e_dos

    e_monic, fm = effort_quadratic_factoring(
        r"x^{2} + 4x + 3",
        r"\left(x + 1\right)\left(x + 3\right)",
    )
    e_ac, fa = effort_quadratic_factoring(
        r"3w^{2} + 32w + 64",
        r"\left(3w + 8\right)\left(w + 8\right)",
    )
    e_gcf, fgc = effort_quadratic_factoring(
        r"2x^{2} - 26x + 72",
        r"2\left(x - 9\right)\left(x - 4\right)",
    )
    assert fm.get("method") == "monic"
    assert fa.get("method") == "ac"
    assert fgc.get("gcf_first") is True
    assert e_ac > e_monic
    assert e_gcf > e_monic

    e_solve, fs = effort_quadratic_factor_solve(
        r"3x^{2} + 23x - 8 = 0",
        r"x = -8, x = \frac{1}{3}",
    )
    assert fs.get("solve") is True
    assert fs.get("frac_root") is True
    assert e_solve > e_ac

    e_gen, fgen = effort_poly_general_strategy(
        r"4x^{3} - 12x^{2} - 3x + 9",
        r"\left(x - 3\right)\left(4x^{2} - 3\right)",
    )
    assert fgen.get("strategy") is True
    assert fgen.get("routed") == "grouping"
    assert e_gen >= e_grp

    y, _ = score_effort(
        "quadratic_factoring",
        r"x^{2} + 5x + 6",
        r"\left(x + 2\right)\left(x + 3\right)",
    )
    assert y is not None and y >= 5.0


def test_quadratic_square_roots_form_ladder():
    e_iso, fi = effort_quadratic_square_roots(r"x^{2} = 169", r"x = \pm 13")
    e_vert, fv = effort_quadratic_square_roots(
        r"5\left(x + 1\right)^{2} = 180",
        r"x = -1 \pm 6",
    )
    e_exp, fe = effort_quadratic_square_roots(
        r"x^{2} - 6x + 5 = 0",
        r"x = 3 \pm 2",
    )
    assert fi.get("form") == "isolated"
    assert fv.get("form") == "vertex"
    assert fv.get("scaled_a") is True
    assert fe.get("form") == "complete_square"
    assert e_vert > e_iso
    assert e_exp > e_vert


def test_completing_square_constant_and_solve():
    e_small, fs = effort_completing_square_constant(
        r"x^{2} + 6x + c \text{ is a perfect square trinomial. Find } c.",
        "9",
    )
    e_big, fb = effort_completing_square_constant(
        r"x^{2} - 18x + c \text{ is a perfect square trinomial. Find } c.",
        "81",
    )
    assert fb.get("abs_b", 0) >= fs.get("abs_b", 0)
    assert e_big >= e_small

    e_monic, _ = effort_completing_square_solve(r"x^{2} + 6x - 7 = 0", r"x = -3 \pm 4")
    e_a, fa = effort_completing_square_solve(
        r"3x^{2} - 42x - 45 = 0",
        r"x = 7 \pm 8",
    )
    assert fa.get("a_ne_1") is True
    assert e_a > e_monic


def test_quadratic_formula_and_discriminant():
    e_missing_b, _ = effort_quadratic_formula(r"3x^{2} - 48 = 0", r"x = 4, -4")
    e_full, ff = effort_quadratic_formula(
        r"2x^{2} - 10x + 12 = 0",
        r"x = 3, 2",
    )
    e_int, _ = effort_quadratic_formula(r"x^{2} + 2x - 3 = 0", r"x = 1, -3")
    e_rad, fr = effort_quadratic_formula(
        r"x^{2} + 2x - 1 = 0",
        r"x = -1 \pm \sqrt{2}",
    )
    assert ff.get("full_abc") is True
    assert e_full > e_missing_b
    assert fr.get("radical_simplify") is True
    assert e_rad > e_int

    e_sq, fsq = effort_quadratic_discriminant(
        r"\text{Find the discriminant of } 3x^{2} + 4x - 4.",
        r"D = 64; \text{two real roots}",
    )
    e_neg, fn = effort_quadratic_discriminant(
        r"\text{Find the discriminant of } 2x^{2} + 3x + 2.",
        r"D = -7; \text{no real roots}",
    )
    assert fsq.get("classify") == "two"
    assert fn.get("classify") == "none"
    assert e_neg > e_sq


def test_radical_multiply_divide_modes():
    e_simple, fs = effort_radical_multiply(r"\sqrt{2} \cdot \sqrt{6}", r"2\sqrt{3}")
    e_coef, fc = effort_radical_multiply(
        r"4\sqrt{3} \cdot 2\sqrt{12}",
        r"48",
    )
    e_bin, fb = effort_radical_multiply(
        r"\left(2\sqrt{3} + \sqrt{5}\right)\left(2\sqrt{3} - \sqrt{5}\right)",
        "7",
    )
    assert fs.get("mode") == "simple"
    assert fc.get("mode") == "coeff"
    assert fb.get("mode") == "binomial"
    assert e_coef > e_simple
    assert e_bin > e_coef

    e_red, fr = effort_radical_divide(r"\frac{\sqrt{18}}{\sqrt{2}}", "3")
    e_rat, frat = effort_radical_divide(r"\frac{3}{\sqrt{5}}", r"\frac{3\sqrt{5}}{5}")
    assert fr.get("mode") in {"reduced", "simplify_quotient"}
    assert frat.get("mode") == "rationalize"
    assert e_rat > e_red

    y, _ = score_effort("radical_multiply", r"\sqrt{15} \cdot \sqrt{18}", r"3\sqrt{30}")
    assert y is not None and y >= 4.0


def test_radical_and_rational_equations_extraneous():
    e_light, fl = effort_radical_equations(r"\sqrt{2x - 3} = 1", r"x = 2")
    e_lin, fli = effort_radical_equations(
        r"\sqrt{x} = x - 2",
        r"x = 4;\ x = 1 \text{ (extraneous)}",
    )
    assert fl.get("form") in {"isolate", "light_prep"}
    assert fli.get("form") == "radical_equals_linear"
    assert fli.get("extraneous") is True
    assert e_lin > e_light

    e_simple, _ = effort_rational_equations(r"\frac{-12}{x} = 3", r"x = -4")
    e_lin_den, fd = effort_rational_equations(r"\frac{2}{x + 2} = 2", r"x = -1")
    e_two, ft = effort_rational_equations(
        r"\frac{1}{x} + \frac{1}{x + 1} = 1",
        r"x = \frac{1 + \sqrt{5}}{2};\ x = \frac{1 - \sqrt{5}}{2}",
    )
    assert fd.get("linear_den") is True
    assert ft.get("form") == "two_fractions"
    assert e_lin_den > e_simple
    assert e_two > e_lin_den

    y, _ = score_effort(
        "rational_expressions_equations",
        r"\frac{32}{x + 2} = 4",
        r"x = 6",
    )
    assert y is not None and y >= 6.0


def test_poly_long_division_and_radical_simplification():
    e_lin, fl = effort_poly_long_division(
        r"\frac{x^{2} + 5x + 6}{x + 2}",
        r"x + 3",
    )
    e_hi, fh = effort_poly_long_division(
        r"\frac{2x^{4} - 3x^{3} + x - 5}{x^{2} + 1}",
        r"2x^{2} - 3x - 2 + \frac{3x - 3}{x^{2} + 1}",
    )
    assert fl.get("deg_gap") == 1
    assert fh.get("deg_gap") >= 2
    assert fh.get("remainder") is True
    assert e_hi > e_lin

    e_sm, fs = effort_radical_simplification(r"\sqrt{18}", r"3\sqrt{2}")
    e_lg, flg = effort_radical_simplification(r"\sqrt{288}", r"12\sqrt{2}")
    assert fs.get("skill") == "simplify"
    assert flg.get("outer_sq", 1) >= fs.get("outer_sq", 1)
    assert e_lg >= e_sm

    y, _ = score_effort("polynomial_long_division", r"\frac{x^{3}-1}{x-1}", r"x^{2}+x+1")
    assert y is not None and y >= 5.0
    y2, _ = score_effort("radical_simplification", r"\sqrt{50}", r"5\sqrt{2}")
    assert y2 is not None and y2 >= 4.0


def test_wp_mixture_drt_work_scorers():
    e_pct, fp = effort_wp_mixture(
        r"\text{Casey mixes 12 cubic yards of soil that is 25\% sand with "
        r"3 cubic yards of soil that is 40\% sand. What percent of the mixture is sand?}",
        r"28\%",
    )
    e_cost, fc = effort_wp_mixture(
        r"\text{Uma blends 8 lb of Sri Lankan tea costing \$2 per lb with "
        r"6 lb of Indian tea costing \$9 per lb. What is the cost per pound?}",
        r"\$5",
    )
    assert fp.get("kind") == "percent"
    assert fc.get("kind") == "cost"
    assert e_cost > e_pct

    e_rt, fr = effort_wp_distance_rate_time(
        r"\text{Grace drives to a destination at 33 mi/hr and returns at 44 mi/hr, "
        r"taking 3 hr on the way back. How long did the trip there take?}",
        r"4 hr",
    )
    e_miss, fm = effort_wp_distance_rate_time(
        r"\text{A car travels 120 miles at 40 mi/hr. How many hours does the trip take?}",
        r"3 hr",
    )
    assert fr.get("mode") == "round_trip"
    assert fm.get("mode") == "find_missing"
    assert e_rt > e_miss

    e_tog, ft = effort_wp_work(
        r"\text{Alex can finish a job in 6 hr and Jordan can finish the same job "
        r"in 3 hr. Working together, how many hr will it take them to finish the job?}",
        r"2 hr",
    )
    e_pipe, fpipe = effort_wp_work(
        r"\text{Pipe A can fill a tank in 8 hr and Pipe B can fill the same tank "
        r"in 12 hr. Working together, how long to fill the tank?}",
        r"4.8 hr",
    )
    assert ft.get("mode") == "together"
    assert fpipe.get("mode") == "pipes"
    assert e_pipe > e_tog

    for tid in (
        "mixture_word_problems",
        "distance_rate_time_word_problems",
        "work_word_problems",
    ):
        y, _ = score_effort(tid, r"\text{Working together takes 4 hr.}", "4")
        assert y is not None, tid


def test_prompt_based_graph_leaves():
    e_lin, fl = effort_evaluating_functions(
        r"\text{Given } f(x) = 2x + 3, \text{ find } f(3).",
        "9",
    )
    e_neg, fn = effort_evaluating_functions(
        r"\text{Given } f(x) = 4x - 8, \text{ find } f(-7).",
        "-36",
    )
    e_quad, fq = effort_evaluating_functions(
        r"\text{Given } f(x) = x^{2} - 3, \text{ find } f(-4).",
        "13",
    )
    assert fl.get("family") == "linear"
    assert fn.get("input") == -7
    assert fq.get("family") == "quadratic"
    assert e_neg > e_lin
    assert e_quad > e_lin

    e_si, fs = effort_graph_linear_equation(r"\text{Graph: } y = 2x", r"y = 2x")
    e_std, fstd = effort_graph_linear_equation(
        r"\text{Graph: } 3x + 2y = 6",
        r"3x + 2y = 6",
    )
    assert fs.get("form") == "slope_intercept"
    assert fstd.get("form") == "standard"
    assert e_std > e_si

    y, _ = score_effort(
        "evaluating_graphing_functions",
        r"\text{Given } f(x) = x + 1, \text{ find } f(2).",
        "3",
    )
    assert y is not None and y >= 3.0
    y2, _ = score_effort("graphing_linear_equations", r"\text{Graph: } y = -x + 1.", r"y = -x + 1")
    assert y2 is not None and y2 >= 4.0


def test_age_coin_consecutive_percent_wp_scorers():
    e_age, fa = effort_wp_age(
        r"\text{Alex is 4 years older than Jordan. The sum of their ages is 28 years. "
        r"How old is Jordan?}",
        "12",
    )
    assert fa.get("kind") == "age"
    assert fa.get("diff") is True
    assert e_age >= 6.0

    e_coin, fc = effort_wp_coin(
        r"\text{A jar contains 20 coins, all quarters and nickels, worth \$3.40 in total. "
        r"How many quarters are in the jar?}",
        "12",
    )
    assert fc.get("kind") == "coin"
    assert fc.get("denoms", 0) >= 2
    assert e_coin >= 6.0

    e_sum, fs = effort_wp_consecutive(
        r"\text{The sum of three consecutive integers is 24. Find the smallest integer.}",
        "7",
    )
    e_prod, fp = effort_wp_consecutive(
        r"\text{The product of the first and last of four consecutive even integers is 48. "
        r"Find the smallest integer.}",
        "2",
    )
    assert fs.get("goal") == "sum"
    assert fp.get("goal") == "product"
    assert fp.get("parity") == "even"
    assert e_prod > e_sum

    e_disc, fd = effort_markup_discount(
        r"\text{Sam buys an item priced at \$40. It is on sale for 25\% off. "
        r"What is the sale price?}",
        r"\$30.00",
    )
    e_combo, fcombo = effort_markup_discount(
        r"\text{An item priced at \$80 is discounted 20\% then has 8\% tax added. "
        r"What is the final cost?}",
        r"\$69.12",
    )
    assert fd.get("kind") == "discount"
    assert fcombo.get("kind") == "discount_then_tax"
    assert e_combo > e_disc

    for tid in (
        "age_word_problems",
        "coin_word_problems",
        "consecutive_integers_word_problems",
        "percent_word_problems",
    ):
        y, _ = score_effort(tid, r"\text{Sam is 3 years older than Lee.}", "10")
        assert y is not None, tid


def test_abs_systems_quadratic_graph_scorers():
    e_abs, fabs = effort_graph_transform(r"y = |x - 3| + 2", r"y = |x - 3| + 2")
    e_parent, _ = effort_graph_transform(r"y = |x|", r"y = |x|")
    assert fabs.get("kind") == "abs"
    assert fabs.get("h_shift") is True
    assert e_abs > e_parent

    e_sys, fsys = effort_graph_linear(
        r"\text{Graph the system: } \begin{cases} y > 2x + 1 \\ y < -x + 3 \end{cases}",
        r"y > 2x + 1, y < -x + 3",
    )
    assert fsys.get("system") is True
    assert fsys.get("inequality") is True
    assert e_sys >= 8.0

    e_v, fv = effort_graph_transform(r"y = (x + 2)^2", r"y = (x + 2)^2")
    e_std, fstd = effort_graph_transform(r"y = x^2 + 4x + 3", r"y = x^2 + 4x + 3")
    e_ineq, fineq = effort_graph_transform(r"y \geq (x - 1)^2 + 2", r"y \geq (x - 1)^2 + 2")
    assert fv.get("kind") == "quadratic"
    assert fstd.get("form") == "standard"
    assert fineq.get("inequality") is True
    assert e_std > e_v
    assert e_ineq > e_v

    for tid in (
        "graphing_absolute_value_equations",
        "graphing_systems_of_inequalities",
        "graphing_quadratic_functions",
        "graphing_quadratic_inequalities",
    ):
        y, _ = score_effort(tid, r"y = |x|", r"y = |x|")
        assert y is not None, tid
