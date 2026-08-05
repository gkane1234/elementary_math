"""A2 effort scorers — quadratic methods, radical ops, exp/log, gap-fill families."""

from __future__ import annotations

import json
from pathlib import Path

import question_engine.types  # noqa: F401
from question_engine.ml.effort import (
    effort_a2_exp_equation,
    effort_a2_log_equation,
    effort_binomial_theorem,
    effort_completing_square_constant,
    effort_completing_square_solve,
    effort_complex_ops,
    effort_conic,
    effort_descartes,
    effort_fta,
    effort_growth_decay,
    effort_inverse_exp_log,
    effort_inverse_function,
    effort_law_of_sines_cosines,
    effort_literal_equations,
    effort_matrix_inverse,
    effort_matrix_ops,
    effort_planes,
    effort_poly_end_behavior,
    effort_polynomial_writing,
    effort_quadratic_discriminant,
    effort_quadratic_formula,
    effort_quadratic_system,
    effort_radical_divide,
    effort_radical_domain_range,
    effort_radical_equations,
    effort_radical_multiply,
    effort_rational_zero,
    effort_relations,
    effort_remainder_theorem,
    effort_sequence,
    effort_solve_by_graphing,
    effort_stats_counting,
    effort_stats_perm_comb,
    effort_stats_probability,
    effort_systems_three,
    has_effort_scorer,
    score_effort,
)

A2_EXPORT_TYPES_PATH = (
    Path(__file__).resolve().parents[2] / "scripts" / "output" / "ml" / "a2_export_types.json"
)

A2_NEW_SCORER_TYPES = [
    "a2_quadratic_functions_and_inequalities_completing_the_square",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square",
    "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula",
    "a2_quadratic_functions_and_inequalities_the_discriminant",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots",
    "a2_radical_functions_and_rational_exponents_multiplying_radical_expressions",
    "a2_radical_functions_and_rational_exponents_dividing_radical_expressions",
    "a2_radical_functions_and_rational_exponents_radical_equations",
    "a2_radical_functions_and_rational_exponents_rational_exponent_equations",
    "a2_radical_functions_and_rational_exponents_simplifying_radicals",
    "a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions",
    "a2_rational_expressions_multiplying_and_dividing",
    "a2_rational_expressions_equations",
    "a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms",
    "a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms",
    "a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple",
    "a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard",
    "a2_exponential_and_logarithmic_expressions_evaluating_logarithms",
    "a2_exponential_and_logarithmic_expressions_properties_of_logarithms",
]

A2_GAP_FILL_TYPES = [
    "a2_equations_and_inequalities_literal_equations",
    "a2_linear_relations_and_functions_graphing_linear_equations",
    "a2_linear_relations_and_functions_graphing_absolute_value_equations",
    "a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems",
    "a2_exponential_and_logarithmic_expressions_inverses_of_exponential_and_logarithmic_functions",
    "a2_matrices_operations",
    "a2_matrices_inverses",
    "a2_matrices_cramers_rule",
    "a2_conic_sections_circles_writing_equations",
    "a2_conic_sections_classifying",
    "a2_sequences_and_series_arithmetic_sequences",
    "a2_sequences_and_series_geometric_series",
    "a2_trigonometry_graphing_trig_functions",
    "a2_trigonometry_trig_functions_of_any_angle",
]

A2_THIN_LEAF_TYPES = [
    "a2_systems_of_equations_and_inequalities_planes",
    "a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables",
    "a2_complex_numbers_operations",
    "a2_complex_numbers_absolute_value",
    "a2_complex_numbers_rationalizing_denominators",
    "a2_trigonometry_the_law_of_sines",
    "a2_trigonometry_the_law_of_cosines",
    "a2_trigonometry_area_and_laws_of_sines_and_cosines",
    "a2_probability_and_statistics_sample_spaces_and_the_fundamental_counting_principle",
    "a2_probability_and_statistics_probability_of_independent_and_dependent_events",
    "a2_probability_and_statistics_probability_of_mutually_exclusive_events",
    "a2_probability_and_statistics_permutations",
    "a2_probability_and_statistics_combinations",
    "a2_probability_and_statistics_permutations_vs_combinations",
    "a2_direct_and_inverse_variation_direct_and_inverse_variation",
]

A2_FINAL_GAP_TYPES = [
    "a2_relations_and_introduction_to_functions_discrete_relations",
    "a2_relations_and_introduction_to_functions_continuous_relations",
    "a2_systems_of_equations_and_inequalities_points_in_three_dimensions",
    "a2_matrices_geometric_transformations",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_graphing",
    "a2_polynomial_functions_the_binomial_theorem",
    "a2_polynomial_functions_the_remainder_theorem",
    "a2_polynomial_functions_writing_functions",
    "a2_polynomial_functions_conjugate_roots_and_writing_functions",
    "a2_polynomial_functions_descartes_rule_of_signs",
    "a2_polynomial_functions_rational_zero_root_theorem",
    "a2_polynomial_functions_fundamental_theorem_of_algebra",
    "a2_polynomial_functions_end_behavior_and_general_graph_shape",
    "a2_polynomial_functions_graphing",
    "a2_general_functions_inverses",
    "a2_radical_functions_and_rational_exponents_domain_and_range_of_radical_functions",
    "a2_conic_sections_parabolas_writing_equations",
    "a2_conic_sections_systems_of_quadratic_equations",
]


def test_a2_new_tranche_scorers_registered():
    for tid in A2_NEW_SCORER_TYPES:
        assert has_effort_scorer(tid), tid


def test_a2_gap_fill_scorers_registered():
    for tid in A2_GAP_FILL_TYPES:
        assert has_effort_scorer(tid), tid


def test_a2_thin_leaf_scorers_registered():
    for tid in A2_THIN_LEAF_TYPES:
        assert has_effort_scorer(tid), tid


def test_a2_final_gap_scorers_registered():
    for tid in A2_FINAL_GAP_TYPES:
        assert has_effort_scorer(tid), tid


def test_a2_export_types_include_new_scorers():
    data = json.loads(A2_EXPORT_TYPES_PATH.read_text(encoding="utf-8"))
    ids = set(data["type_ids"])
    for tid in A2_NEW_SCORER_TYPES + A2_GAP_FILL_TYPES + A2_THIN_LEAF_TYPES + A2_FINAL_GAP_TYPES:
        assert tid in ids, tid
    assert len(ids) >= 145


def test_a2_final_gap_scorer_behavior():
    e_tab, ft = effort_relations(
        r"\text{Complete the table for } y = 2x + 1. \\ \begin{array}{|c|c|} \hline x & y \\ \hline 1 & 3 \\ 2 & ? \\ \hline \end{array}",
        "5",
    )
    e_ev, fe = effort_relations(
        r"\text{Given } y = -3x + 4, \text{ find } y \text{ when } x = 2.",
        "-2",
    )
    assert ft.get("mode") == "discrete_table"
    assert fe.get("mode") == "continuous_eval"
    assert e_tab > e_ev

    e_bin, fb = effort_binomial_theorem(
        r"\text{Find the coefficient of } x^{3} \text{ in } (2 + x)^{5}.",
        "40",
    )
    assert fb.get("n") == 5
    assert e_bin >= 5.0

    e_rem, _ = effort_remainder_theorem(
        r"\text{Find the remainder when } x^{2} + 3x - 4 \text{ is divided by } (x - 2).",
        "6",
    )
    assert e_rem >= 4.0

    e_write, fw = effort_polynomial_writing(
        r"\text{Write a quadratic function with zeros } 2 \text{ and } -3 \text{ and leading coefficient } 2.",
        r"2x^{2} + 2x - 12",
    )
    e_conj, fc = effort_polynomial_writing(
        r"\text{Write a monic quadratic with roots } 1 + 2i \text{ and } 1 - 2i.",
        r"x^{2} - 2x + 5",
    )
    assert fw.get("mode") == "real_zeros"
    assert fc.get("mode") == "conjugate"
    assert e_conj > e_write

    e_d, _ = effort_descartes(
        r"\text{Use Descartes' Rule of Signs for } f(x)=x^{3} - 2x^{2} + x - 4.",
        r"\text{positive: } 3, 1; \text{negative: } 0",
    )
    assert e_d >= 5.0

    e_rz, _ = effort_rational_zero(
        r"\text{List all possible rational zeros of } 2x^{3} + x^{2} - x + 6.",
        r"\pm\{1, 2, 3, 6, 1/2, 3/2\}",
    )
    assert e_rz >= 6.0

    e_fta, ff = effort_fta(
        r"\text{By the Fundamental Theorem of Algebra, how many complex zeros, counting multiplicity, does a degree-}5\text{ polynomial have?}",
        "5",
    )
    assert ff.get("degree") == 5
    assert e_fta >= 2.0

    e_eb, _ = effort_poly_end_behavior(
        r"\text{Describe the end behavior of } f(x)=-2x^{5} + 3x^{2} - 1.",
        r"x\to-\infty:f(x)\to\infty;\quad x\to\infty:f(x)\to-\infty",
    )
    assert e_eb >= 4.0

    e_inv, fi = effort_inverse_function(
        r"\text{Find the inverse of } f(x) = 3x - 2",
        r"f^{-1}(x) = \frac{1}{3}(x + 2)",
    )
    assert fi.get("frac_slope") is True
    assert e_inv >= 4.5

    e_dr, _ = effort_radical_domain_range(
        r"\text{Find the domain and range of } f(x)=2\sqrt{x - 1} + 3.",
        r"\text{Domain }[1, \infty);\ \text{Range }[3, \infty)",
    )
    assert e_dr >= 5.0

    e_sg, fs = effort_solve_by_graphing(
        r"(x - 1)(x + 2) = 0",
        r"x = -2, x = 1",
    )
    assert fs.get("form") == "factored"
    assert e_sg >= 6.0

    e_qs, fq = effort_quadratic_system(
        r"\text{Solve } \begin{cases} y=x^2\\ y=3x-2\end{cases}",
        r"(1, 1),\ (2, 4)",
    )
    assert fq.get("mode") == "quadratic_system"
    assert e_qs >= 7.0

    y, _ = score_effort(
        "a2_polynomial_functions_the_binomial_theorem",
        r"\text{Find the coefficient of } x^{2} \text{ in } (1 + x)^{4}.",
        "6",
    )
    assert y is not None and y >= 4.0


def test_a2_thin_leaf_scorer_behavior():
    e_s, fs = effort_law_of_sines_cosines(
        r"\text{In } \triangle ABC,\ m\angle A = 30^\circ,\ m\angle B = 45^\circ,\ a = 10.\ \text{Find } b \text{ (Law of Sines).}",
        "14.14",
    )
    e_c, fc = effort_law_of_sines_cosines(
        r"\text{In } \triangle ABC,\ a = 8,\ b = 10,\ m\angle C = 120^\circ.\ \text{Find } c \text{ (Law of Cosines).}",
        "15.62",
    )
    assert fs.get("mode") == "sines"
    assert fc.get("mode") == "cosines"
    assert fc.get("obtuse") is True
    assert e_c > e_s

    e_add, fa = effort_complex_ops(r"\left(2+3i\right) + \left(1-i\right)", r"3+2i")
    e_mul, fm = effort_complex_ops(r"\left(2+3i\right)\left(1-i\right)", r"5+i")
    e_rat, fr = effort_complex_ops(
        r"\text{Rationalize } \dfrac{3}{2+i}.",
        r"\frac{6}{5}-\frac{3}{5}i",
    )
    assert fa.get("mode") == "add_sub"
    assert fm.get("mode") == "multiply"
    assert fr.get("mode") == "rationalize"
    assert e_mul > e_add
    assert e_rat > e_mul

    e_p, fp = effort_planes(
        r"\text{Does } (1, 2, 3) \text{ lie on the plane } x+2y-z=2\text{?}",
        r"\text{Yes}",
    )
    assert fp.get("three_vars") is True
    assert e_p >= 5.0

    e3, f3 = effort_systems_three(
        r"\text{Solve } \begin{cases} x+y+z=6\\ 2x-y+z=3\\ x+2y-z=3\end{cases}",
        r"(1, 2, 3)",
    )
    assert f3.get("vars") == 3
    assert e3 >= 8.0

    e_ct, fct = effort_stats_counting(
        r"\text{A restaurant offers 4 entrees and 3 desserts. How many entree-dessert combinations are possible?}",
        "12",
    )
    assert fct.get("mode") == "counting"
    assert e_ct >= 3.0

    e_ind, fi = effort_stats_probability(
        r"\text{A bag has 3 red, 2 blue, and 4 green marbles. You draw one marble, replace it, then draw again. What is the probability of drawing red both times?}",
        r"\frac{1}{9}",
    )
    e_or, fo = effort_stats_probability(
        r"\text{A bag has 3 red, 2 blue, and 4 green marbles. What is the probability of drawing a red or blue marble?}",
        r"\frac{5}{9}",
    )
    assert fi.get("mode") == "independent"
    assert fo.get("mode") == "mutually_exclusive"
    assert e_ind > e_or

    e_perm, fperm = effort_stats_perm_comb(r"\text{Evaluate } {}_{8}P_{3}.", "336")
    e_word, fword = effort_stats_perm_comb(
        r"\text{How many ways can 3 students be lined up from a class of 9?}",
        "504",
    )
    assert fperm.get("mode") == "perm"
    assert fword.get("mode") == "perm_word"
    assert e_word >= e_perm

    y, _ = score_effort(
        "a2_trigonometry_the_law_of_sines",
        r"\text{In } \triangle ABC,\ m\angle A = 40^\circ,\ m\angle B = 60^\circ,\ a = 7.\ \text{Find } b \text{ (Law of Sines).}",
        "9.40",
    )
    assert y is not None and y >= 5.0


def test_a2_literal_equations_alias():
    e, feats = effort_literal_equations(
        r"I = p r t \quad \text{Solve for } r.",
        r"r = \frac{I}{p t}",
    )
    assert e >= 4.0
    assert feats.get("frac_sol") is True
    y, _ = score_effort(
        "a2_equations_and_inequalities_literal_equations",
        r"A = \ell w \quad \text{Solve for } w.",
        r"w = \frac{A}{\ell}",
    )
    assert y is not None and y >= 4.0


def test_a2_growth_decay_and_inverse_scorers():
    e_g, fg = effort_growth_decay(
        r"\text{An investment of \$800 changes by 5\% growth each year. Find the amount after 4 years.}",
        "972.41",
    )
    e_r, fr = effort_growth_decay(
        r"\text{What rate of growth is needed for \$1000 to reach \$2000 in 5 years?}",
        "0.15",
    )
    assert fg.get("mode") == "find_final"
    assert fr.get("mode") == "find_rate"
    assert e_r > e_g

    e_inv, _fi = effort_inverse_exp_log(
        r"\text{Find the inverse of } f(x)=3^{x +1} -2.",
        r"f^{-1}(x)=\log_{3}(x +2) -1",
    )
    assert e_inv >= 6.0


def test_a2_matrix_conic_sequence_scorers():
    e_m, fm = effort_matrix_ops(
        r"\begin{pmatrix}2 & 3 \\ 0 & -1\end{pmatrix} + \begin{pmatrix}-5 & 1 \\ 2 & 2\end{pmatrix}",
        r"\begin{pmatrix}-3 & 4 \\ 2 & 1\end{pmatrix}",
    )
    e_i, fi = effort_matrix_inverse(
        r"\text{Find the inverse of } \begin{pmatrix}3 & -1 \\ 1 & 1\end{pmatrix}.",
        r"\frac{1}{4}\begin{pmatrix}1 & 1 \\ -1 & 3\end{pmatrix}",
    )
    assert fm.get("op") == "add"
    assert e_i > e_m
    assert fi.get("frac_det") is True

    e_c, fc = effort_conic(
        r"\text{Write the equation of the circle with center }(2, -1)\text{ and radius }5.",
        r"(x-(2))^2+(y-(-1))^2=25",
    )
    assert fc.get("mode") == "write"
    assert e_c >= 5.0

    e_s, fs = effort_sequence(
        r"\text{Find the } 11^{\text{th}} \text{ term of the arithmetic sequence with } a_1 = 3 \text{ and } d = -3.",
        "-27",
    )
    assert fs.get("kind") == "arithmetic"
    assert e_s >= 4.0


def test_a2_quadratic_formula_cts_discriminant_aliases():
    e_c, _ = effort_completing_square_constant(
        r"x^{2} - 10x + c \text{ is a perfect square trinomial. Find } c.",
        "25",
    )
    e_s, fs = effort_completing_square_solve(r"2x^{2} + 12x - 14 = 0", r"x = -3 \pm 4")
    e_f, _ = effort_quadratic_formula(r"2x^{2} - 14x - 88 = 0", r"x = 11, -4")
    e_d, fd = effort_quadratic_discriminant(
        r"\text{Find the discriminant of } 4x^{2} + 10x - 10.",
        r"D = 260; \text{two real roots}",
    )
    assert e_c >= 3.0
    assert fs.get("a_ne_1") is True
    assert e_s > e_c
    assert e_f >= 6.0
    assert fd.get("classify") == "two"

    for tid in (
        "a2_quadratic_functions_and_inequalities_completing_the_square",
        "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square",
        "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula",
        "a2_quadratic_functions_and_inequalities_the_discriminant",
    ):
        y, _ = score_effort(tid, r"x^{2} + 6x - 7 = 0", r"x = 1, -7")
        assert y is not None, tid


def test_a2_radical_ops_and_equations_aliases():
    e_m, fm = effort_radical_multiply(r"\sqrt{3} \cdot \sqrt{12}", "6")
    e_d, fd = effort_radical_divide(r"\frac{3}{\sqrt{5}}", r"\frac{3\sqrt{5}}{5}")
    e_eq, fe = effort_radical_equations(
        r"\sqrt{x} = x - 12",
        r"x = 16;\ x = 9 \text{ (extraneous)}",
    )
    assert fm.get("mode") == "simple"
    assert fd.get("mode") == "rationalize"
    assert fe.get("extraneous") is True
    assert e_d > e_m
    assert e_eq >= 8.0

    y, _ = score_effort(
        "a2_radical_functions_and_rational_exponents_multiplying_radical_expressions",
        r"\sqrt{3} \cdot \sqrt{8}",
        r"2\sqrt{6}",
    )
    assert y is not None and y >= 3.0
    y2, _ = score_effort(
        "a2_radical_functions_and_rational_exponents_radical_equations",
        r"5\sqrt{4x - 12} = 10",
        r"x = 4",
    )
    assert y2 is not None and y2 >= 5.0


def test_a2_exp_log_equation_scorers():
    e_plain, fp = effort_a2_exp_equation(r"5^{x} = 5", r"x = 1")
    e_coef, fc = effort_a2_exp_equation(r"3^{3x} = 729", r"x = 2")
    assert fp.get("plain_exponent") or "base" in fp
    assert fc.get("coef_on_exponent") is True
    assert e_coef > e_plain

    e_log, fl = effort_a2_log_equation(r"\log_{9}(x) = 3", r"x = 729")
    e_big, fb = effort_a2_log_equation(r"\log(x) = 5", r"x = 100000")
    assert fl.get("equation") is True
    assert fl.get("solve_for_x") is True
    assert fb.get("large_solution") is True
    assert e_big > e_log
    assert e_log >= 5.0

    y_exp, _ = score_effort(
        "a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms",
        r"2^{5x} = 32768",
        r"x = 3",
    )
    y_log, _ = score_effort(
        "a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple",
        r"\log_{7}(x) = 4",
        r"x = 2401",
    )
    y_eval, _ = score_effort(
        "a2_exponential_and_logarithmic_expressions_evaluating_logarithms",
        r"\log_{4}\left(64\right)",
        "3",
    )
    assert y_exp is not None and y_exp >= 8.0
    assert y_log is not None and y_log >= 5.0
    assert y_eval is not None and y_eval >= 3.0
