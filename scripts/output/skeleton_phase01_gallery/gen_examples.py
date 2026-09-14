"""Phase 0–2 skeleton galleries — rational + poly unification catalog.

Generates live samples via ``question_engine.api.handler._generate_for_type``
(same path as worksheets).

Any catalog ``type_id`` can get a section page (notes + Limitations header) even
when not listed in ``SECTIONS`` — use ``--type-id`` or ``--ensure-stubs``.

Output:
  scripts/output/skeleton_phase01_gallery/index.html
  scripts/output/skeleton_phase01_gallery/<slug>/gallery.html
  scripts/output/skeleton_phase01_gallery/<slug>/samples.json
  scripts/output/skeleton_phase01_gallery/samples.json  (summary)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from question_engine.api.handler import _generate_for_type

OUT = Path(__file__).resolve().parent
# Per-type pages live in <slug>/gallery.html (one level deeper than index.html).
KATEX = "../../topic_fit/_assets/katex"
KATEX_INDEX = "../topic_fit/_assets/katex"

LADDER_DS = (2.0, 8.0, 16.0)
LADDER_SEEDS = (101, 207)

# One section per skeleton_pattern / distinct skill; cards show form_id when present.
SECTIONS: list[dict[str, Any]] = [
    {
        "slug": "add_sub_cancel",
        "title": "AddSubCancel — combine ± rationals",
        "pattern": "AddSubCancel",
        "engine": "rational_skeleton",
        "type_id": "rational_expression_simplification",
        "aliases": [
            "a2_rational_expressions_adding_and_subtracting",
        ],
        "blurb": (
            "Live default for add/subtract rational expressions. "
            "Opt out with <code>use_constructive_rational=True</code>."
        ),
    },
    {
        "slug": "simplify_cancel",
        "title": "SimplifyCancel — single-fraction simplify",
        "pattern": "SimplifyCancel",
        "engine": "rational_skeleton",
        "type_id": "rational_simplification",
        "aliases": ["a2_rational_expressions_simplifying"],
        "blurb": "Single rational with planned cancellation; stamps <code>simplify_cancel</code> form.",
    },
    {
        "slug": "mul_div_cancel",
        "title": "MulDivCancel — multiply / divide rationals",
        "pattern": "MulDivCancel",
        "engine": "rational_skeleton",
        "type_id": "rational_expression_multiply_divide",
        "aliases": ["a2_rational_expressions_multiplying_and_dividing"],
        "blurb": "Cross-operand cancels; remain degree ≤ 2.",
    },
    {
        "slug": "complex_frac_cancel",
        "title": "ComplexFracCancel — nested complex fractions",
        "pattern": "ComplexFracCancel",
        "engine": "rational_skeleton",
        "type_id": "a2_rational_expressions_complex_fractions",
        "aliases": [],
        "blurb": "Complex-fraction skill intent; opt out with <code>use_hand_complex_frac=True</code>.",
    },
    {
        "slug": "factor_quadratic",
        "title": "FactorProduct — quadratic trinomial",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "quadratic_factoring",
        "aliases": [
            "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions",
        ],
        "task": "factor",
        "blurb": "Monic / non-monic trinomial via factor_sampler + OpenStax form when wired.",
    },
    {
        "slug": "factor_special",
        "title": "FactorProduct — special products",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "polynomial_factoring_special_cases",
        "aliases": [
            "a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions",
        ],
        "task": "factor",
        "blurb": "Difference of squares, perfect-square trinomial, etc.",
    },
    {
        "slug": "factor_grouping",
        "title": "FactorProduct — grouping",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "polynomial_factoring_grouping",
        "aliases": ["a2_polynomial_functions_factoring_by_grouping"],
        "task": "factor",
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            "Four-term grouping at every D (OpenStax EA §7.1), not a quadratic trinomial. "
            "Degree 3; larger coeffs at high D."
        ),
    },
    {
        "slug": "factor_cubes",
        "title": "FactorProduct — sum / difference of cubes",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "a2_polynomial_functions_factoring_sum_difference_of_cubes",
        "aliases": [],
        "task": "factor",
        "blurb": "Cube patterns; degree 3.",
    },
    {
        "slug": "factor_quadratic_form",
        "title": "FactorProduct — quadratic form",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "a2_polynomial_functions_factoring_quadratic_form",
        "aliases": [],
        "task": "factor",
        "blurb": "Substitution-style (ax²+b)(cx²+d); degree up to 4.",
    },
    {
        "slug": "factor_all_techniques",
        "title": "FactorProduct — all-techniques mixer",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "polynomial_factoring_general_strategy",
        "aliases": ["a2_polynomial_functions_factoring_all_techniques"],
        "task": "factor",
        "blurb": "D-weighted mixer (A1 catalog or A2 all-techniques pool).",
    },
    {
        "slug": "multiply",
        "title": "FactorProduct — multiply polynomials",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "polynomial_multiply",
        "aliases": [
            "a2_polynomial_functions_multiplying",
            "pa_polynomials_multiplying",
        ],
        "task": "multiply",
        "blurb": "FOIL / distribute; factors shown, product expanded.",
    },
    {
        "slug": "multiply_special",
        "title": "FactorProduct — special products (multiply)",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "polynomial_multiply_special",
        "aliases": ["a2_polynomial_functions_multiplying_special_cases"],
        "task": "multiply",
        "blurb": "(a±b)² and difference-of-squares product forms.",
    },
    {
        "slug": "one_step",
        "title": "SolveLinear — one-step equations",
        "pattern": "SolveLinear",
        "engine": "equation_skeleton",
        "type_id": "one_step_equations",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            "Goal-first reverse op (add/sub or mul/div). "
            "Opt out with <code>use_sample_linear_equation=True</code>."
        ),
    },
    {
        "slug": "two_step",
        "title": "SolveLinear — two-step equations",
        "pattern": "SolveLinear",
        "engine": "equation_skeleton",
        "type_id": "two_step_equations",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"$ax \pm b = c$ — small ints at D=0; larger coeffs before fractions.",
    },
    {
        "slug": "multi_step",
        "title": "SolveLinear — multi-step equations",
        "pattern": "SolveLinear",
        "engine": "equation_skeleton",
        "type_id": "multi_step_equations",
        "aliases": [
            "pa_equations_multi_step_equations",
            "a2_equations_and_inequalities_multi_step_equations",
            "geo_review_multi_step_equations",
        ],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            "D=0 is simple: $2(x+1)=8$ or $3x+2=x+8$. "
            "Numeric hardness first, then distribute + both sides. "
            "Opt out with <code>use_sample_linear_equation=True</code>."
        ),
    },
    {
        "slug": "one_step_ineq",
        "title": "SolveInequality — one-step inequalities",
        "pattern": "SolveInequality",
        "engine": "equation_skeleton",
        "type_id": "one_step_inequalities",
        "aliases": ["g6_solving_and_graphing_one_step_inequalities"],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            "Same reverse tape as SolveLinear with "
            r"$<$, $>$, $\le$, $\ge$. "
            "Flip when multiplying/dividing by a negative. "
            "Opt out with <code>use_sample_linear_inequality=True</code>."
        ),
    },
    {
        "slug": "two_step_ineq",
        "title": "SolveInequality — two-step inequalities",
        "pattern": "SolveInequality",
        "engine": "equation_skeleton",
        "type_id": "two_step_inequalities",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"$ax \pm b < c$ — D=0 small positive coeffs; negatives (and flips) later.",
    },
    {
        "slug": "multi_step_ineq",
        "title": "SolveInequality — multi-step inequalities",
        "pattern": "SolveInequality",
        "engine": "equation_skeleton",
        "type_id": "multi_step_inequalities",
        "aliases": [
            "pa_multi_step_inequalities",
            "a2_equations_and_inequalities_multi_step_inequalities",
        ],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            "D=0 is simple: $2(x+1)<8$ or $3x+2<x+8$ (no flip). "
            "Opt out with <code>use_sample_linear_inequality=True</code>."
        ),
    },
    {
        "slug": "literal",
        "title": "SolveLiteral — literal equations",
        "pattern": "SolveLiteral",
        "engine": "equation_skeleton",
        "type_id": "literal_equations",
        "aliases": ["a2_equations_and_inequalities_literal_equations"],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            "D=0 one-step isolate ($d=rt$ for $t$). "
            "More letters, two-step $ax+by=c$, perimeter / fractions later. "
            "Opt out with <code>use_sample_literal_equation=True</code>."
        ),
    },
    {
        "slug": "one_step_wp",
        "title": "Word problem — one-step equations",
        "pattern": "SolveLinear",
        "engine": "wp_packaging",
        "type_id": "g6_equations_word_problems",
        "aliases": ["pa_equations_one_step_word_problems"],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313, 419, 523, 631),
        "blurb": (
            "OpenStax story frames (number, spent/left, shares, tickets). "
            "G6 stays one-step at every D. "
            "Opt out with <code>use_sample_linear_equation=True</code>."
        ),
    },
    {
        "slug": "two_step_wp",
        "title": "Word problem — two-step equations",
        "pattern": "SolveLinear",
        "engine": "wp_packaging",
        "type_id": "pa_equations_two_step_word_problems",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313, 419, 523, 631),
        "blurb": (
            r"$ax \pm b = c$ as a story (number WP, twice-more, earnings, unit+fee). "
            "Does not dump the equation into the prompt."
        ),
    },
    {
        "slug": "ineq_wp",
        "title": "Word problem — inequalities",
        "pattern": "SolveInequality",
        "engine": "wp_packaging",
        "type_id": "g6_inequalities_word_problems",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313, 419, 523, 631),
        "blurb": (
            "D=0 compare / height / checkout / points (no two-step budget). "
            "Car-rental / phone / tablet budget frames unlock at format_tier ≥ 1. "
            "Opt out with <code>use_sample_linear_inequality=True</code>."
        ),
    },
    {
        "slug": "proportion_wp",
        "title": "Word problem — proportions (recipe / unit rate / calories / dosage)",
        "pattern": "ProportionRate",
        "engine": "wp_packaging",
        "type_id": "pa_proportions_word_problems",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313, 419, 523, 631),
        "blurb": (
            "Recipe scale, unit-rate cost, calories, or dosage — does not dump "
            r"$a/b = x/c$. Opt out with "
            "<code>use_sample_linear_equation=True</code>."
        ),
    },
    {
        "slug": "proportion",
        "title": "Proportion — algebraic a/b = x/c",
        "pattern": "Proportion",
        "engine": "equation_skeleton",
        "type_id": "solving_proportions",
        "aliases": ["pa_checking_for_a_proportion", "g6_equivalent_ratio_equations"],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"D=0 is $2/3 = x/4$. Numeric hardness first, then unknown in a denominator. "
            "Opt out with <code>use_sample_proportion=True</code>. "
            "Rate word problems stay <code>ProportionRate</code>."
        ),
    },
    {
        "slug": "factor_gcf",
        "title": "FactorGcf — monomial GCF only",
        "pattern": "FactorGcf",
        "engine": "poly_skeleton",
        "type_id": "polynomial_factoring_common_factor",
        "aliases": ["g6_factor_gcf", "factor_gcf"],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313, 419),
        "blurb": (
            r"D=0 is $6x+9 \to 3(2x+3)$. At D≥8 the GCF includes $x$ "
            r"(old $4x(2x-3)$), not the same $3x+6$ at every D. "
            "Opt out with <code>use_factor_poly=True</code>."
        ),
    },
    {
        "slug": "graph_ineq",
        "title": "SolveInequality — number-line graphing",
        "pattern": "SolveInequality",
        "engine": "equation_skeleton",
        "type_id": "graphing_single_variable_inequalities",
        "aliases": [
            "g6_solutions_to_inequalities",
            "g6_writing_and_graphing_inequalities",
        ],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"D=0 is already isolated $x < 3$ on a number line. "
            "Catalog generator <code>graph_single_variable_inequality</code> is wired here."
        ),
    },
    {
        "slug": "factor_equations",
        "title": "FactorProduct — solve by factoring",
        "pattern": "FactorProduct",
        "engine": "poly_skeleton",
        "type_id": "quadratic_factoring_equations",
        "aliases": [
            "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring",
        ],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"Same ladder as old <code>factor_poly</code>: D=0 is monic $x^2+7x+12=0$; "
            r"D≥8 is a≠1 (ac method); D>10 unsimplifies. Always degree 2 — not grouping. "
            "Opt out with <code>use_factor_poly=True</code>."
        ),
    },
    {
        "slug": "compound_ineq",
        "title": "CompoundInequality — graph on a number line",
        "pattern": "CompoundInequality",
        "engine": "compound_inequalities",
        "type_id": "compound_inequalities",
        "aliases": ["a2_equations_and_inequalities_compound_inequalities"],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 401, 611),
        "blurb": (
            r"Old <code>CompoundInequalitiesFramework</code>: D=0 is isolated "
            r"$-1 < x < 2$ or $x < -1 \text{ or } x > 1$ (prompt = answer) "
            "on a blank number line. Medium/hard solve a linear compound, then graph "
            "the isolated form. Opt out with "
            "<code>use_sample_compound_inequality=True</code>."
        ),
    },
    {
        "slug": "abs_eq",
        "title": "AbsEquation — split |inner| = k",
        "pattern": "AbsEquation",
        "engine": "equation_skeleton",
        "type_id": "absolute_value_equations",
        "aliases": ["a2_equations_and_inequalities_absolute_value_equations"],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"D=0 is $|x|=k$ or $|x+b|=k$ (a=1), matching old simple/shifted. "
            r"D≥8 is $|ax+b|=k$ with $|a|\ge 2$ (old medium linear inner). "
            "Opt out with <code>use_sample_absolute_value_equation=True</code>."
        ),
    },
    {
        "slug": "abs_ineq",
        "title": "AbsInequality — compound + number line",
        "pattern": "AbsInequality",
        "engine": "equation_skeleton",
        "type_id": "absolute_value_inequalities",
        "aliases": ["a2_equations_and_inequalities_absolute_value_inequalities"],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"D=0 is $|x|<2$ or $|x+b|<k$ (a=1). D≥8 is $|ax+b|\ge k$ with "
            r"$|a|\ge 2$, matching old medium linear. Number line on the answer. "
            "Opt out with <code>use_sample_absolute_value_inequality=True</code>."
        ),
    },
    {
        "slug": "eq_cancel",
        "title": "EqCancel — rational equations",
        "pattern": "EqCancel",
        "engine": "rational_skeleton",
        "type_id": "rational_expressions_equations",
        "aliases": [
            "a2_rational_expressions_equations",
            "pc_rational_equations",
        ],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            "D=0 is a proportion. Then one linear den, LCD, extraneous. "
            "Opt out with <code>use_hand_rational_equations=True</code>."
        ),
    },
    {
        "slug": "like_terms",
        "title": "AffineInflate — like terms",
        "pattern": "AffineInflate",
        "engine": "affine_skeleton",
        "type_id": "g6_combining_like_terms",
        "aliases": ["combining_like_terms"],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"D=0 is $3x+2x$. Term counts follow the old like-terms sampler: "
            r"extra likes/constants at D=8 (~4–5), then up to 8 at D=16, "
            r"~10 with a second variable at D=22. Opt out with "
            "<code>use_sample_like_terms=True</code>."
        ),
    },
    {
        "slug": "distribute",
        "title": "AffineInflate — distribute / expand",
        "pattern": "AffineInflate",
        "engine": "affine_skeleton",
        "type_id": "g6_distributive_property_algebraic",
        "aliases": ["a2_beginning_algebra_simplifying_algebraic_expressions"],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"D=0 is $2(x+3)$. Then 3 terms inside one factor, then "
            r"two-binomials — old distributive maxed at ~4 display terms, "
            r"not an 8-term sum. Expand leftover via <code>construct_affine</code>. "
            "Opt out with <code>use_sample_distributive=True</code>."
        ),
    },
    {
        "slug": "poly_add_sub",
        "title": "PolyAddSub — add / subtract polynomials",
        "pattern": "PolyAddSub",
        "engine": "poly_skeleton",
        "type_id": "polynomial_add_subtract",
        "aliases": [
            "pa_polynomials_adding_and_subtracting",
            "a2_polynomial_functions_adding_and_subtracting",
        ],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"D=0 is $(2x+1)+(x+3)$ (degree 1). Not FactorProduct. "
            "Opt out with <code>use_sample_polynomial_add_subtract=True</code>."
        ),
    },
    {
        "slug": "similar_figures_wp",
        "title": "SimilarFigures — scale-factor story + diagram",
        "pattern": "SimilarFigures",
        "engine": "wp_packaging",
        "type_id": "pa_similar_figures",
        "aliases": ["pa_similar_figures_word_problems"],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207, 313, 419, 523, 631),
        "blurb": (
            "EA §8.7 similar triangles at D=0 (scale 2, missing side). "
            "Quadrilaterals and larger scale at higher D. "
            "Opt out with <code>use_legacy_similar_figures=True</code>."
        ),
    },
    {
        "slug": "check_equation",
        "title": "SolveLinear — is x=k a solution?",
        "pattern": "SolveLinear",
        "engine": "equation_skeleton",
        "type_id": "g6_solutions_to_equations",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"Old <code>check_equation_solution</code>: D=0 is one-step "
            r"$3x=24$ / $x+4=6$. Then two-step, both-sides, fractions. "
            "Opt out with <code>use_sample_linear_equation=True</code>."
        ),
    },
    {
        "slug": "write_rate",
        "title": "Word problem — write a constant-rate equation",
        "pattern": "SolveLinear",
        "engine": "wp_packaging",
        "type_id": "g6_constant_rate_equations",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313, 419, 523),
        "blurb": (
            r"OpenStax EA §2.6: D=0 is $d = r\cdot t$ (bike/car/walk/bus/train). "
            "Find time / rate later. Opt out with "
            "<code>use_sample_linear_equation=True</code>."
        ),
    },
    {
        "slug": "write_other",
        "title": "Word problem — write cost / perimeter equation",
        "pattern": "SolveLinear",
        "engine": "wp_packaging",
        "type_id": "g6_equations_for_other_relationships",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313, 419, 523),
        "blurb": (
            r"D=0 cost / tickets. High D: square $4s=P$ (solve for $s$) and "
            r"triangle $P=a+b+c$. Same SolveLinear one-step core."
        ),
    },
    {
        "slug": "evaluate_affine",
        "title": "AffineInflate — evaluate by substituting",
        "pattern": "AffineInflate",
        "engine": "affine_skeleton",
        "type_id": "g6_evaluating_algebraic_expressions",
        "aliases": ["evaluate_algebraic_expressions"],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            r"Old evaluate: D=0 is $3+x$ or $1-3x$ when $x=k$ "
            r"(not $2(x+3)$). Leftover distribute later. Opt out with "
            "<code>use_sample_evaluate=True</code>."
        ),
    },
    {
        "slug": "g6_points_on_the_coordinate_plane",
        "title": "GeometryMeasure — plot or identify a point",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_points_on_the_coordinate_plane",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": (
            "Plot a given ordered pair on a blank plane, or read a labeled point. "
            "Not the old identity dump. Opt out with "
            "<code>use_legacy_geometry=True</code>."
        ),
    },
    {
        "slug": "g6_distances_on_the_coordinate_plane",
        "title": "GeometryMeasure — axis-aligned distance",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_distances_on_the_coordinate_plane",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "D=0 horizontal; vertical unlocks later. G6 — no Pythagorean.",
    },
    {
        "slug": "g6_shapes_and_perimeter_on_the_coordinate_plane",
        "title": "GeometryMeasure — rectangle perimeter on the plane",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_shapes_and_perimeter_on_the_coordinate_plane",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "Axis-aligned rectangle vertices; find perimeter.",
    },
    {
        "slug": "g6_coordinate_plane_distances_word_problems",
        "title": "Coordinate distance WP (stub — red header)",
        "pattern": "",
        "engine": "wp (untouched)",
        "type_id": "g6_coordinate_plane_distances_word_problems",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207),
        "blurb": "UNCLEAR dump stub. Not on GeometryMeasure. WP engine left alone.",
    },
    {
        "slug": "g6_parallelograms",
        "title": "GeometryMeasure — parallelogram area",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_parallelograms",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"Diagram; $A=bh$. Numeric product grows with D.",
    },
    {
        "slug": "g6_parallelograms_understanding_area_formula",
        "title": "GeometryMeasure — parallelogram missing side",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_parallelograms_understanding_area_formula",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "Same core; high D asks for missing base/height.",
    },
    {
        "slug": "g6_triangles",
        "title": "GeometryMeasure — triangle area",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_triangles",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"$A=\tfrac12 bh$ from a labeled triangle diagram.",
    },
    {
        "slug": "g6_triangles_understanding_area_formula",
        "title": "GeometryMeasure — triangle missing side",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_triangles_understanding_area_formula",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "High D inverts $A=\\tfrac12 bh$ for base or height.",
    },
    {
        "slug": "g6_trapezoids",
        "title": "GeometryMeasure — trapezoid area",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_trapezoids",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"$A=\tfrac12 h(b+B)$ from a labeled trapezoid.",
    },
    {
        "slug": "g6_kites",
        "title": "GeometryMeasure — kite area (UNCLEAR)",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_kites",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"IM-shaped $A=\tfrac12 d_1 d_2$. Not in OpenStax 9.4.",
    },
    {
        "slug": "g6_polygons_on_a_grid_or_coordinate_plane",
        "title": "GeometryMeasure — polygons on a grid",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_polygons_on_a_grid_or_coordinate_plane",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "Count / decompose square units. Shape mix ramps with D.",
    },
    {
        "slug": "g6_polygons_and_shaded_regions",
        "title": "GeometryMeasure — shaded composite (outer − inner)",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_polygons_and_shaded_regions",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "Shaded region = rectangle minus triangle / frame / L-cut.",
    },
    {
        "slug": "g6_classifying_and_naming",
        "title": "GeometryMeasure — classify a polyhedron",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_classifying_and_naming",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "Name the solid from a picture. D=0 prism; later pyramids.",
    },
    {
        "slug": "g6_volume_and_surface_area_using_isometric_drawings",
        "title": "GeometryMeasure — isometric count (UNCLEAR)",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_volume_and_surface_area_using_isometric_drawings",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "Old isometric count. IM vs OpenStax LWH still UNCLEAR.",
    },
    {
        "slug": "g6_formulas_for_volume_and_surface_area_of_a_cube",
        "title": "GeometryMeasure — cube $V=s^3$ / $S=6s^2$",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_formulas_for_volume_and_surface_area_of_a_cube",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": "Cube only. Side length grows with D.",
    },
    {
        "slug": "g6_rectangles_with_fraction_side_lengths",
        "title": "GeometryMeasure — rectangle fraction sides",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_rectangles_with_fraction_side_lengths",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"D=0 unit fraction × whole. Then two fractions.",
    },
    {
        "slug": "g6_triangles_with_fraction_side_lengths",
        "title": "GeometryMeasure — triangle fraction sides",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_triangles_with_fraction_side_lengths",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"Same ramp as the rectangle sibling with extra $\tfrac12$.",
    },
    {
        "slug": "g6_right_rectangular_prisms_with_fraction_side_lengths",
        "title": "GeometryMeasure — prism fraction edges",
        "pattern": "GeometryMeasure",
        "engine": "geometry_skeleton",
        "type_id": "g6_right_rectangular_prisms_with_fraction_side_lengths",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": r"$V=\ell wh$ with one unit fraction at D=0, then three fractions.",
    },
    {
        "slug": "g6_equations_tape_diagrams",
        "title": "Tape diagrams (UNCLEAR — eq engine untouched)",
        "pattern": "",
        "engine": "eq (untouched)",
        "type_id": "g6_equations_tape_diagrams",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207),
        "blurb": "Red-header samples only. Equation engine not changed.",
    },
    {
        "slug": "g6_equations_hanger_diagrams",
        "title": "Hanger diagrams (UNCLEAR — eq engine untouched)",
        "pattern": "",
        "engine": "eq (untouched)",
        "type_id": "g6_equations_hanger_diagrams",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207),
        "blurb": "Red-header samples only. Equation engine not changed.",
    },
    {
        "slug": "g6_inequalities_hanger_diagrams",
        "title": "Inequality hangers (UNCLEAR — eq engine untouched)",
        "pattern": "",
        "engine": "eq (untouched)",
        "type_id": "g6_inequalities_hanger_diagrams",
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207),
        "blurb": "Red-header samples only. Equation engine not changed.",
    },
]


# G6 stubs — notes-locked UNCLEAR / data / write-expression (no new engine this pass).
SECTIONS.extend(
    [
        {
            "slug": "g6_writing_algebraic_expressions",
            "title": "Write algebraic expressions (UNCLEAR high-D powers)",
            "pattern": "",
            "engine": "verbal (untouched)",
            "type_id": "g6_writing_algebraic_expressions",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": (
                "UNCLEAR: old D=22 jumps to $x^2$/$x^3$ (beyond G6 / OpenStax 2.2). "
                "Red-header live samples; no new engine."
            ),
        },
        {
            "slug": "g6_distributive_property_area_diagrams_algebraic",
            "title": "Distributive area model, algebraic (LOW_VARIETY)",
            "pattern": "",
            "engine": "affine (untouched)",
            "type_id": "g6_distributive_property_area_diagrams_algebraic",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": (
                "LOW_VARIETY: always 'Use the area model to expand $a(x\\pm b)$'. "
                "Same core as algebraic distribute; red-header stub."
            ),
        },
        {
            "slug": "g6_interpreting_dot_plots",
            "title": "Interpret dot plots (UNCLEAR — data dump)",
            "pattern": "",
            "engine": "stats (untouched)",
            "type_id": "g6_interpreting_dot_plots",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": (
                "UNCLEAR: stem dumps Data:{…} so the plot can be ignored. "
                "Red-header samples; no stats engine this pass."
            ),
        },
        {
            "slug": "g6_drawing_dot_plots",
            "title": "Draw dot plots (UNCLEAR stub)",
            "pattern": "",
            "engine": "stats (untouched)",
            "type_id": "g6_drawing_dot_plots",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": "UNCLEAR gold for draw-vs-interpret. Red-header live samples.",
        },
        {
            "slug": "g6_interpreting_histograms",
            "title": "Interpret histograms (UNCLEAR stub)",
            "pattern": "",
            "engine": "stats (untouched)",
            "type_id": "g6_interpreting_histograms",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": "UNCLEAR / thin OpenStax match. Red-header live samples.",
        },
        {
            "slug": "g6_drawing_histograms",
            "title": "Draw histograms (UNCLEAR stub)",
            "pattern": "",
            "engine": "stats (untouched)",
            "type_id": "g6_drawing_histograms",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": "UNCLEAR gold. Red-header live samples.",
        },
        {
            "slug": "g6_data_center_and_spread",
            "title": "Center and spread (stub)",
            "pattern": "",
            "engine": "stats (untouched)",
            "type_id": "g6_data_center_and_spread",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": "Mean/median/range from lists. Red-header live samples.",
        },
        {
            "slug": "g6_interpreting_box_plots",
            "title": "Interpret box plots (UNCLEAR stub)",
            "pattern": "",
            "engine": "stats (untouched)",
            "type_id": "g6_interpreting_box_plots",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": "UNCLEAR diagram fidelity. Red-header live samples.",
        },
        {
            "slug": "g6_drawing_box_plots",
            "title": "Draw box plots (UNCLEAR stub)",
            "pattern": "",
            "engine": "stats (untouched)",
            "type_id": "g6_drawing_box_plots",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207),
            "blurb": "UNCLEAR gold. Red-header live samples.",
        },
    ]
)


def _g6n(
    slug: str,
    title: str,
    pattern: str,
    type_id: str,
    blurb: str,
    *,
    aliases: list[str] | None = None,
    extra_settings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "slug": slug,
        "title": title,
        "pattern": pattern,
        "engine": "number",
        "type_id": type_id,
        "aliases": aliases or [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": blurb,
    }
    if extra_settings:
        rec["extra_settings"] = extra_settings
    return rec


# G6 number cores — existing NumberFrameworks (no new skeleton).
SECTIONS.extend(
    [
        _g6n(
            "g6_introduction_to_ratios",
            "Number — introduction to ratios",
            "Ratio",
            "g6_introduction_to_ratios",
            "D=0 write a tiny part:part. High D always simplify. Reuses RatioFramework.",
        ),
        _g6n(
            "g6_equivalent_ratios",
            "Number — equivalent ratios",
            "EquivalentRatio",
            "g6_equivalent_ratios",
            r"D=0 missing value $a:b=c:x$ with scale 2. Reuses RatioFramework(equivalent).",
        ),
        _g6n(
            "g6_part_part_whole_ratios",
            "Number — part–part–whole ratios",
            "PartPartWhole",
            "g6_part_part_whole_ratios",
            "D=0 two small parts, part:part. High D part:whole or split a collection.",
        ),
        _g6n(
            "g6_comparing_ratios",
            "Number — comparing ratios",
            "CompareRatios",
            "g6_comparing_ratios",
            "Which ratio is greater. LOW_VARIETY stem; numeric hardness ramps.",
        ),
        _g6n(
            "g6_unit_rates_and_equivalent_rates",
            "Number — unit rates",
            "UnitRate",
            "g6_unit_rates_and_equivalent_rates",
            "D=0 integer unit rate. High D scale to a non-multiple quantity.",
        ),
        _g6n(
            "g6_comparing_rates",
            "Number — comparing rates",
            "CompareRates",
            "g6_comparing_rates",
            "Unit price / speed compare. Double number lines in metadata (existing helper).",
        ),
        _g6n(
            "g6_converting_units",
            "Number — converting units",
            "ConvertUnits",
            "g6_converting_units",
            "Given equivalence. Double number line in metadata. Keep UNCLEAR if DNL is display-only.",
        ),
        _g6n(
            "g6_introduction_to_percents",
            "Number — introduction to percents",
            "IntroPercent",
            "g6_introduction_to_percents",
            "Shade a 100-grid / bar / circle. SVG in metadata. D=0 benchmarks 10/25/50/75%.",
        ),
        _g6n(
            "g6_relating_percents_fractions_and_decimals",
            "Number — percents, fractions, decimals",
            "RelatePercent",
            "g6_relating_percents_fractions_and_decimals",
            "F↔D↔P conversions. Not percent-of.",
        ),
        _g6n(
            "g6_finding_percents_with_equivalent_fractions",
            "Number — percent via equivalent fractions",
            "FindingPercent",
            "g6_finding_percents_with_equivalent_fractions",
            "Scale the denominator to 100. LOW_VARIETY stem; numeric work ramps.",
        ),
        _g6n(
            "g6_solving_percent_problems_with_formulas",
            "Number — percent problems (formulas)",
            "PercentOf",
            "g6_solving_percent_problems_with_formulas",
            r"D=0 is $p\%$ of $n$. Then find-percent / find-whole. Same PercentFramework as the diagram sibling.",
        ),
        _g6n(
            "g6_solving_percent_problems_with_diagrams",
            "Number — percent problems (diagrams)",
            "PercentOf",
            "g6_solving_percent_problems_with_diagrams",
            "Same percent-of core; percent-shade SVG attached. Catalog still names diagrams.",
        ),
        _g6n(
            "g6_how_many_groups_times",
            "Number — how many groups?",
            "FractionGroups",
            "g6_how_many_groups_times",
            "How many groups of divisor in dividend. FractionDivideWordFramework(groups).",
        ),
        _g6n(
            "g6_what_fraction_of_a_whole",
            "Number — what fraction of a whole?",
            "FractionOfWhole",
            "g6_what_fraction_of_a_whole",
            r"D=0: what fraction of $B$ is $A$ (small wholes). Not multiply-by-$\frac12$.",
        ),
        _g6n(
            "g6_how_much_in_each_group_time",
            "Number — how much in each group?",
            "FractionEach",
            "g6_how_much_in_each_group_time",
            "Partitive divide. FractionDivideWordFramework(each).",
        ),
        _g6n(
            "g6_dividing_fractions",
            "Number — dividing fractions",
            "FractionDiv",
            "g6_dividing_fractions",
            r"Bare $a\div b$ fractions. Non-negative G6.",
        ),
        _g6n(
            "g6_decimal_addition",
            "Number — decimal addition",
            "DecimalAdd",
            "g6_decimal_addition",
            "D=0 one-place addends. Signed addends stay $a+(-b)$, not a subtraction leaf.",
        ),
        _g6n(
            "g6_decimal_addition_with_diagrams",
            "Number — decimal addition with diagrams",
            "DecimalAdd",
            "g6_decimal_addition_with_diagrams",
            "Same add core; decimal-grid SVG when type_id contains with_diagram.",
        ),
        _g6n(
            "g6_decimal_subtraction",
            "Number — decimal subtraction",
            "DecimalSub",
            "g6_decimal_subtraction",
            "D=0 one-place subtract. Borrowing ramps with D.",
        ),
        _g6n(
            "g6_decimal_subtraction_with_diagrams",
            "Number — decimal subtraction with diagrams",
            "DecimalSub",
            "g6_decimal_subtraction_with_diagrams",
            "Same subtract core; decimal-grid SVG attached.",
        ),
        _g6n(
            "g6_decimal_multiplication",
            "Number — decimal multiplication",
            "DecimalMul",
            "g6_decimal_multiplication",
            "D=0 one-place factors. Place-sum effort grows with D.",
        ),
        _g6n(
            "g6_decimal_multiplication_with_equivalent_fractions",
            "Number — decimal × via equivalent fractions",
            "DecimalMulFrac",
            "g6_decimal_multiplication_with_equivalent_fractions",
            r"Shows $0.5\cdot 0.4=\frac{5}{10}\cdot\frac{4}{10}$ so the named method is visible.",
        ),
        _g6n(
            "g6_decimal_multiplication_with_area_diagrams",
            "Number — decimal × with area diagrams",
            "DecimalMul",
            "g6_decimal_multiplication_with_area_diagrams",
            "Same multiply core; area-model SVG attached.",
        ),
        _g6n(
            "g6_long_division_with_remainders",
            "Number — long division with remainders",
            "LongDivision",
            "g6_long_division_with_remainders",
            "D=0 two-digit ÷ one-digit with remainder. Digit count grows.",
        ),
        _g6n(
            "g6_dividing_whole_numbers_that_result_in_decimals",
            "Number — whole ÷ whole → decimal",
            "WholeToDecimal",
            "g6_dividing_whole_numbers_that_result_in_decimals",
            "Terminating non-integer quotients.",
        ),
        _g6n(
            "g6_dividing_decimals_by_whole_numbers",
            "Number — decimal ÷ whole",
            "DecimalDiv",
            "g6_dividing_decimals_by_whole_numbers",
            "Decimal ÷ whole with terminating quotient.",
        ),
        _g6n(
            "g6_dividing_whole_numbers_by_decimals",
            "Number — whole ÷ decimal",
            "WholeByDecimal",
            "g6_dividing_whole_numbers_by_decimals",
            "D=0 tenths divisors in (0,1). ≥1 divisors later.",
        ),
        _g6n(
            "g6_dividing_decimals_by_decimals",
            "Number — decimal ÷ decimal",
            "DecimalDivByDec",
            "g6_dividing_decimals_by_decimals",
            "D=0 tenths ÷ tenths. Awkward divisors at high D.",
        ),
        _g6n(
            "g6_factoring",
            "Number — prime factorization",
            "PrimeFactor",
            "g6_factoring",
            "Factor a composite. Ω(n) ramps; not huge semiprimes.",
        ),
        _g6n(
            "g6_greatest_common_factor",
            "Number — GCF",
            "GCF",
            "g6_greatest_common_factor",
            "Find GCF of two (then three) numbers. Cancel-step effort, not magnitude pads.",
        ),
        _g6n(
            "g6_least_common_multiple",
            "Number — LCM",
            "LCM",
            "g6_least_common_multiple",
            "Find LCM. Combined Ω ramps with D.",
        ),
        _g6n(
            "g6_opposites_of_numbers",
            "Number — opposites",
            "Opposite",
            "g6_opposites_of_numbers",
            "Find the opposite of an integer. Magnitude grows modestly.",
        ),
        _g6n(
            "g6_comparing_numbers",
            "Number — comparing numbers",
            "CompareNumbers",
            "g6_comparing_numbers",
            "Fill $?$ between two values. Form mix then closeness.",
        ),
        _g6n(
            "g6_ordering_numbers",
            "Number — ordering numbers",
            "OrderNumbers",
            "g6_ordering_numbers",
            "Order 3→5 values. Form mix then closeness.",
        ),
        _g6n(
            "g6_absolute_values",
            "Number — absolute value",
            "AbsoluteValue",
            "g6_absolute_values",
            r"Evaluate $|n|$. Structure (signs) before huge magnitude.",
        ),
        _g6n(
            "g6_comparing_with_absolute_values",
            "Number — compare absolute values",
            "CompareAbs",
            "g6_comparing_with_absolute_values",
            r"$|a|\;?\;|b|$. Near-ties at high D.",
        ),
        _g6n(
            "g6_ordering_with_absolute_values",
            "Number — order absolute values",
            "OrderAbs",
            "g6_ordering_with_absolute_values",
            "Order by absolute value. Mixed signs at mid+.",
        ),
        _g6n(
            "g6_numbers_on_a_number_line",
            "Number — numbers on a number line",
            "NumberLinePlot",
            "g6_numbers_on_a_number_line",
            "Prompt is the value; instruction is plot. Number-line spec via include_graph_metadata.",
            extra_settings={"include_graph_metadata": True},
        ),
        _g6n(
            "g6_writing_numeric_expressions",
            "Number — writing numeric expressions",
            "WriteNumeric",
            "g6_writing_numeric_expressions",
            "D=0 two-number phrases. Grouping then exponents later.",
        ),
        _g6n(
            "g6_numeric_expressions_with_exponents",
            "Number — OOO with exponents",
            "OrderOfOperations",
            "g6_numeric_expressions_with_exponents",
            "Evaluate; always at least one exponent. Live path is PRIM_OOO.",
        ),
        _g6n(
            "g6_properties_of_addition_and_multiplication",
            "Number — identify the property",
            "IdentifyProperty",
            "g6_properties_of_addition_and_multiplication",
            "D=0 commutative/identity. Associative then distributive unlock. MC among property names.",
        ),
        _g6n(
            "g6_numeric_expressions_and_order_of_operations",
            "Number — order of operations",
            "OrderOfOperations",
            "g6_numeric_expressions_and_order_of_operations",
            r"D=0 two–three ops, no grouping. Live path is PRIM_OOO (not the old PEMDAS framework).",
        ),
        _g6n(
            "g6_distributive_property_numeric",
            "Number — distributive (numeric)",
            "Distributive",
            "g6_distributive_property_numeric",
            "Rewrite $a(b+c)$. UNCLEAR: key often uncombined. Reuses distributive_property.",
        ),
        _g6n(
            "g6_distributive_property_area_diagrams_numeric",
            "Number — distributive numeric + area (was miswired)",
            "Distributive",
            "g6_distributive_property_area_diagrams_numeric",
            "Catalog was g6_divisibility — fixed to distributive_property + area_model. "
            "UNCLEAR gold (rewrite vs evaluate).",
        ),
        _g6n(
            "g6_gcf_and_lcm_word_problems",
            "Number — GCF/LCM word problems (LOW_VARIETY)",
            "GcfLcmWP",
            "g6_gcf_and_lcm_word_problems",
            "LOW_VARIETY: bags/GCF Mad-Lib dominates. Red-header stub; no new engine.",
        ),
        _g6n(
            "g6_number_line_word_problems",
            "Number — number-line word problems (LOW_VARIETY)",
            "NumberLineWP",
            "g6_number_line_word_problems",
            "LOW_VARIETY: temp / elevation / bank Mad-Libs. Red-header stub.",
        ),
    ]
)

SECTIONS.extend(
    [
        {
            "slug": "pa_number_place",
            "title": "Number — place value and rounding",
            "pattern": "NumberOp",
            "engine": "number_reuse",
            "type_id": "pa_naming_decimal_places_and_rounding",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "D=0 names tenths/hundredths or rounds to a whole. OpenStax PA §5.1.",
        },
        {
            "slug": "pa_number_words",
            "title": "Number — write in words",
            "pattern": "NumberOp",
            "engine": "number_reuse",
            "type_id": "pa_writing_numbers_with_words",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "D=0 two- or three-digit wholes. OpenStax PA §5.1.",
        },
        {
            "slug": "pa_integers",
            "title": "Number — integer add / subtract",
            "pattern": "NumberOp",
            "engine": "number_reuse",
            "type_id": "pa_integers_adding_and_subtracting",
            "aliases": ["pa_integers_multiplying", "pa_integers_dividing"],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": r"D=0 two small integers. OpenStax PA §3.2–3.4.",
        },
        {
            "slug": "pa_factors",
            "title": "Number — factors / GCF / LCM / divisibility",
            "pattern": "NumberOp",
            "engine": "number_reuse",
            "type_id": "pa_factoring",
            "aliases": [
                "pa_greatest_common_factor",
                "pa_least_common_multiple",
                "pa_divisibility",
            ],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "Numeric factor pairs / GCF / LCM — not polynomial GCF. OpenStax PA §2.4–2.5.",
        },
        {
            "slug": "pa_fractions",
            "title": "Number — fraction arithmetic",
            "pattern": "NumberOp",
            "engine": "number_reuse",
            "type_id": "pa_simplifying_fractions",
            "aliases": [
                "pa_fractions_add_like",
                "pa_fractions_subtract_like",
                "pa_fractions_add_unlike",
                "pa_fractions_subtract_unlike",
                "pa_fractions_multiply",
                "pa_fractions_divide",
                "pa_converting_fractions_and_decimals",
                "pa_fractions_decimals_and_percents",
            ],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "Simplify / ± / ×÷ / convert. OpenStax PA Ch. 4–6.1.",
        },
        {
            "slug": "pa_squares",
            "title": "Number — squares and square roots",
            "pattern": "NumberOp",
            "engine": "number_reuse",
            "type_id": "pa_squares_and_square_roots",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": r"D=0 perfect squares $1$–$12$. OpenStax PA §5.7.",
        },
        {
            "slug": "pa_markup",
            "title": "Word problem — markup / discount / tax / commission",
            "pattern": "PercentWP",
            "engine": "percent_wp",
            "type_id": "pa_markup_discount_and_tax",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313, 419, 523),
            "blurb": "OpenStax PA §6.3 retail: tax, discount, markup, commission.",
        },
        {
            "slug": "pa_interest",
            "title": "Word problem — simple interest I=Prt",
            "pattern": "InterestWP",
            "engine": "interest_wp",
            "type_id": "pa_simple_and_compound_interest",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313, 419),
            "blurb": "D=0 find I. Later solve for P / r / t (PA §6.4). Compound is extra at high D.",
        },
        {
            "slug": "pa_slope",
            "title": "Slope — two points or from y=mx+b",
            "pattern": "Slope",
            "engine": "linear_forms",
            "type_id": "pa_slope",
            "aliases": ["slope"],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": r"D=0 slope from two lattice points. OpenStax PA §11.4.",
        },
        {
            "slug": "pa_write_linear",
            "title": "WriteLinear — slope-intercept from m and b",
            "pattern": "WriteLinear",
            "engine": "linear_forms",
            "type_id": "pa_writing_linear_equations",
            "aliases": ["writing_linear_equations"],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": r"D=0 given $m$ and $b$. Two points / point-slope later. OpenStax PA §11.5–11.6.",
        },
        {
            "slug": "pa_systems_sub",
            "title": "LinearSystem — substitution",
            "pattern": "LinearSystem",
            "engine": "systems",
            "type_id": "pa_systems_substitution",
            "aliases": [
                "systems_substitution",
                "a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables",
            ],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": r"D=0 one equation already $y=\ldots$. OpenStax EA §5.2.",
        },
        {
            "slug": "pa_graph_systems",
            "title": "LinearSystem — graph two lines",
            "pattern": "LinearSystem",
            "engine": "systems",
            "type_id": "pa_graphing_systems_of_equations",
            "aliases": [
                "systems_graphing",
                "a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables",
            ],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "Solve by graphing. Parallel / no-solution later. OpenStax EA §5.1.",
        },
        {
            "slug": "pa_systems_wp",
            "title": "Word problem — systems (number / tickets / geometry / motion)",
            "pattern": "SystemsWP",
            "engine": "wp_packaging",
            "type_id": "pa_systems_word_problems",
            "aliases": [
                "systems_word_problems",
                "a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables",
            ],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313, 419, 523),
            "blurb": (
                "OpenStax EA §5.4 frames. Does not dump a system into the prompt. "
                "Opt out with <code>use_legacy_systems=True</code>."
            ),
        },
        {
            "slug": "pa_plot_points",
            "title": "PlotPoints — coordinate plane",
            "pattern": "PlotPoints",
            "engine": "plotting_points",
            "type_id": "pa_plotting_points",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "OpenStax PA §11.1. Notes flag UNCLEAR (old path is a bare ordered pair).",
        },
        {
            "slug": "pa_angles",
            "title": "Geometry — angles and triangles",
            "pattern": "GeoMeasure",
            "engine": "geometry_reuse",
            "type_id": "pa_angle_relationships",
            "aliases": ["pa_plane_figures_triangles"],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "Complementary / supplementary / triangle measures. OpenStax PA §9.3–9.4.",
        },
        {
            "slug": "pa_protractor",
            "title": "Geometry — draw / measure angles (UNCLEAR)",
            "pattern": "GeoMeasure",
            "engine": "geometry_reuse",
            "type_id": "pa_drawing_and_measuring_angles",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "UNCLEAR gold (protractor vs properties). Reuse geo_angles — no new engine. OpenStax PA §9.3.",
        },
        {
            "slug": "pa_area",
            "title": "Geometry — area / quads / circles / solids",
            "pattern": "GeoMeasure",
            "engine": "geometry_reuse",
            "type_id": "pa_area_of_triangles_and_quadrilaterals",
            "aliases": [
                "pa_circles",
                "pa_classifying_volume_and_surface_area",
            ],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": r"D=0 rectangle or right triangle. Circles $C=2\pi r$. OpenStax PA §9.4–9.6.",
        },
        {
            "slug": "pa_quads",
            "title": "Geometry — quadrilaterals (UNCLEAR overlap)",
            "pattern": "GeoMeasure",
            "engine": "geometry_reuse",
            "type_id": "pa_quadrilaterals",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "UNCLEAR vs area leaf (old path is still area). Reuse geo_quadrilateral_area — no new engine.",
        },
        {
            "slug": "pa_pythagorean",
            "title": "Geometry — Pythagorean theorem",
            "pattern": "GeoMeasure",
            "engine": "geometry_reuse",
            "type_id": "pythagorean_theorem",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": r"D=0 3-4-5 missing hypotenuse. OpenStax PA §9.3.",
        },
        {
            "slug": "pa_transformations",
            "title": "Geometry — transformations",
            "pattern": "Transform",
            "engine": "geometry_reuse",
            "type_id": "pa_transformations",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": "No PA/EA OpenStax chapter — old-path shapes. Notes flag UNCLEAR.",
        },
        {
            "slug": "pa_poly_simplify",
            "title": "PolySimplify — combine like terms (degree ≥ 2)",
            "pattern": "PolySimplify",
            "engine": "construct_poly",
            "type_id": "pa_polynomials_simplifying",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": r"D=0 a few $x^2$ likes. OpenStax PA §10.1.",
        },
        {
            "slug": "mixture_word_problems",
            "title": "Word problem — mixture (percent / cost / find amount)",
            "pattern": "MixtureWP",
            "engine": "wp_mixture",
            "type_id": "mixture_word_problems",
            "aliases": ["a2_equations_and_inequalities_mixture_word_problems"],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313, 419),
            "blurb": (
                "OpenStax EA §3.3 / IA §2.4. D=0 blend-percent with small ints. "
                "High D can ask for an unknown amount given a target mix. "
                "Coins/tickets stay on the coin leaf."
            ),
        },
        {
            "slug": "distance_rate_time_word_problems",
            "title": "Word problem — distance / rate / time",
            "pattern": "DistanceRateTime",
            "engine": "wp_distance_rate_time",
            "type_id": "distance_rate_time_word_problems",
            "aliases": [
                "a2_equations_and_inequalities_distance_rate_time_word_problems",
            ],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313, 419, 523),
            "blurb": (
                "OpenStax EA §3.4 vehicles (bike / drive / walk / bus / train). "
                "D=0 missing piece; high D round-trip / catch-up / opposite. "
                "Does not freeze one slow-bus Mad-Lib."
            ),
        },
        {
            "slug": "work_word_problems",
            "title": "Word problem — work (together / pipes / starts later)",
            "pattern": "WorkWP",
            "engine": "wp_work",
            "type_id": "work_word_problems",
            "aliases": ["a2_equations_and_inequalities_work_word_problems"],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313, 419),
            "blurb": (
                "OpenStax EA §8.8 jobs and printing presses. D=0 two people, integer hours. "
                "High D starts-later or fill-and-drain pipes."
            ),
        },
        {
            "slug": "age_word_problems",
            "title": "Word problem — ages (one equation)",
            "pattern": "AgeWP",
            "engine": "narrative_wp",
            "type_id": "age_word_problems",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313, 419),
            "blurb": (
                "OpenStax EA §3.1 / §5.37-style age stories as one equation. "
                "D=0 older-by-k and sum. High D past/future/three people. Not systems WP."
            ),
        },
        {
            "slug": "coin_word_problems",
            "title": "Word problem — coins",
            "pattern": "CoinWP",
            "engine": "narrative_wp",
            "type_id": "coin_word_problems",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313, 419),
            "blurb": (
                "OpenStax EA §3.3 / PA §9.2 coin value. D=0 two types, small counts. "
                "High D three denominations or a relation clause."
            ),
        },
        {
            "slug": "consecutive_integers_word_problems",
            "title": "Word problem — consecutive integers",
            "pattern": "ConsecutiveWP",
            "engine": "narrative_wp",
            "type_id": "consecutive_integers_word_problems",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313, 419),
            "blurb": (
                "OpenStax EA §3.1 / IA §2.2. D=0 sum of two consecutive. "
                "High D even/odd, first+last, or product. Does not dump "
                r"$n+(n+1)=S$."
            ),
        },
        {
            "slug": "percent_word_problems",
            "title": "Word problem — percent applications",
            "pattern": "PercentWP",
            "engine": "percent_wp",
            "type_id": "percent_word_problems",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313, 419, 523),
            "blurb": (
                "OpenStax EA §3.2: percent-of, discount, simple interest "
                "(markup/tax later). D=0 is a part of a whole. "
                "PA retail markup stays on <code>pa_markup_discount_and_tax</code>."
            ),
        },
    ]
)


def _a1(
    slug: str,
    title: str,
    pattern: str,
    type_id: str,
    blurb: str,
    *,
    aliases: list[str] | None = None,
    engine: str = "a1_reuse",
) -> dict[str, Any]:
    return {
        "slug": slug,
        "title": title,
        "pattern": pattern,
        "engine": engine,
        "type_id": type_id,
        "aliases": aliases or [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": blurb,
    }


# A1 leftover poly / factor / rational / radical / quadratic (notes-first).
SECTIONS.extend(
    [
        _a1(
            "simplify_polynomials",
            "PolySimplify — combine like terms (degree ≥ 2)",
            "PolySimplify",
            "simplify_polynomials",
            r"D=0 likes of $x^2$. Distribute leftover at high D. OpenStax EA §6.1.",
            aliases=["a2_polynomial_functions_simplifying"],
            engine="construct_poly",
        ),
        _a1(
            "polynomial_naming",
            "PolyNaming — name by degree (UNCLEAR)",
            "PolyNaming",
            "polynomial_naming",
            "UNCLEAR: old path names quadratic/cubic/quartic only. "
            "OpenStax EA §6.1 also asks monomial/binomial/trinomial. Red-header samples.",
            aliases=["a2_polynomial_functions_naming"],
        ),
        _a1(
            "polynomial_long_division",
            "PolyLongDiv — divide polynomials (UNCLEAR)",
            "PolyLongDiv",
            "polynomial_long_division",
            "UNCLEAR: OpenStax splits monomial ÷ (§6.5) vs long division (§6.6). "
            "One A1 leaf covers both. Red-header samples of the old mix.",
            aliases=[
                "a2_polynomial_functions_dividing",
                "pc_dividing_polynomial_functions",
            ],
        ),
        _a1(
            "sets_of_numbers",
            "NumberCore — sets of numbers (UNCLEAR)",
            "NumberCore",
            "sets_of_numbers",
            "UNCLEAR / LOW_VARIETY: old path is T/F integer/whole. "
            "OpenStax EA §1.8 classifies N/W/Z/Q/irrational/R. Red-header samples.",
            engine="number",
        ),
        _a1(
            "rational_add_subtract",
            "FractionAddSub — numeric rational ±",
            "FractionAddSub",
            "rational_add_subtract",
            r"Numeric fractions, not rational expressions. D=0 unlike-denom $3/2+1/3$. "
            "OpenStax EA §1.6.",
            engine="number",
        ),
        _a1(
            "rational_multiply",
            "FractionMul — numeric rational ×",
            "FractionMul",
            "rational_multiply",
            r"D=0 two fractions. Mixed numbers later. OpenStax EA §1.5 / PA §4.2.",
            engine="number",
        ),
        _a1(
            "rational_divide",
            "FractionDiv — numeric rational ÷",
            "FractionDiv",
            "rational_divide",
            r"D=0 unit-fraction ÷. Reciprocal cancel later. OpenStax EA §1.5.",
            engine="number",
        ),
        _a1(
            "quadratic_square_roots",
            "QuadraticSqrt — square-root property",
            "QuadraticSqrt",
            "quadratic_square_roots",
            r"D=0 is $x^2=k$ or $(x-h)^2=k$. Then $a(x-h)^2=k$. OpenStax EA §10.1.",
            aliases=[
                "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots",
            ],
        ),
        _a1(
            "quadratic_formula",
            "QuadraticFormula — solve with the formula",
            "QuadraticFormula",
            "quadratic_formula",
            r"D=0 integer roots, $a=1$. High D radicals / fractions. OpenStax EA §10.3.",
            aliases=[
                "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula",
            ],
        ),
        _a1(
            "quadratic_discriminant",
            "QuadraticDiscriminant — $b^2-4ac$ classify",
            "QuadraticDiscriminant",
            "quadratic_discriminant",
            "Find D and two real / one real / none. OpenStax EA §10.3.",
            aliases=["a2_quadratic_functions_and_inequalities_the_discriminant"],
        ),
        _a1(
            "quadratic_completing_square_constant",
            "CompleteSquareConst — find $c$ for a PST",
            "CompleteSquareConst",
            "quadratic_completing_square_constant",
            r"D=0 even $b$. Odd $b$ → fraction. OpenStax EA §10.2.",
            aliases=["a2_quadratic_functions_and_inequalities_completing_the_square"],
        ),
        _a1(
            "quadratic_completing_square_solve",
            "CompleteSquareSolve — solve by completing the square",
            "CompleteSquareSolve",
            "quadratic_completing_square_solve",
            r"D=0 $a=1$ even $b$. Later $a\neq 1$. OpenStax EA §10.2.",
            aliases=[
                "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square",
            ],
        ),
        _a1(
            "graphing_quadratic_functions",
            "GraphQuadratic — graph $y=ax^2+bx+c$ (UNCLEAR)",
            "GraphQuadratic",
            "graphing_quadratic_functions",
            "Graphs are outside the algebraic FactorProduct / rational cores. "
            "Red-header samples of the existing graph engine. OpenStax EA §10.5.",
            aliases=[
                "pc_parabolas_graphing_and_properties",
                "a2_quadratic_functions_and_inequalities_graphing_quadratic_functions",
            ],
        ),
        _a1(
            "quadratic_solve_by_graphing",
            "SolveByGraphing — intercepts of a parabola (UNCLEAR)",
            "SolveByGraphing",
            "quadratic_solve_by_graphing",
            "Graph-read, not quadratic formula. Red-header samples. OpenStax EA §10.5.",
        ),
        _a1(
            "graphing_quadratic_inequalities",
            "GraphQuadraticIneq — shade a parabola (UNCLEAR)",
            "GraphQuadraticIneq",
            "graphing_quadratic_inequalities",
            "UNCLEAR: no Elementary Algebra section (IA §9.8 / old path). "
            "Red-header samples.",
            aliases=[
                "a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities",
            ],
        ),
        _a1(
            "radical_simplification",
            "RadicalSimplify — single square roots",
            "RadicalSimplify",
            "radical_simplification",
            r"D=0 $\sqrt{n}$ with a perfect-square factor. OpenStax EA §9.1–9.2.",
            aliases=["a2_radical_functions_and_rational_exponents_simplifying_radicals"],
        ),
        _a1(
            "radical_add_subtract",
            "RadicalAddSub — like square roots",
            "RadicalAddSub",
            "radical_add_subtract",
            r"D=0 already-like $a\sqrt{n}\pm b\sqrt{n}$. Simplify first later. OpenStax EA §9.3.",
        ),
        _a1(
            "radical_multiply",
            "RadicalMul — product rule / FOIL",
            "RadicalMul",
            "radical_multiply",
            r"D=0 $\sqrt{a}\cdot\sqrt{b}$. Binomial FOIL at high D. OpenStax EA §9.4.",
        ),
        _a1(
            "radical_divide",
            "RadicalDiv — quotient / rationalize",
            "RadicalDiv",
            "radical_divide",
            r"D=0 $\sqrt{a}/\sqrt{b}$. Rationalize later. OpenStax EA §9.5.",
        ),
        _a1(
            "radical_equations",
            "RadicalEq — isolate then square",
            "RadicalEq",
            "radical_equations",
            r"D=0 $\sqrt{ax+b}=k$. Two radicals later. OpenStax EA §9.6.",
        ),
    ]
)

# A2 poly-only, exp/log, sequences, trig (non-graph); graphing UNCLEAR → red-header samples.
SECTIONS.extend(
    [
        _a1(
            "binomial_theorem",
            "BinomialTheorem — coefficient of $x^k$",
            "BinomialTheorem",
            "a2_polynomial_functions_the_binomial_theorem",
            r"D=0 $(1+x)^n$ or small $a$. Larger $n$, $a\neq 1$ later. OpenStax IA §5.3.",
        ),
        _a1(
            "remainder_theorem",
            "RemainderTheorem — $p(a)$ when dividing by $(x-a)$",
            "RemainderTheorem",
            "a2_polynomial_functions_the_remainder_theorem",
            r"D=0 quadratic $p(x)$, integer root. OpenStax IA §5.4.",
        ),
        _a1(
            "factor_conjugate",
            "FactorProduct — conjugate roots (DOS / PST)",
            "FactorProduct",
            "a2_polynomial_functions_conjugate_roots_and_factoring",
            r"D=0 $x^2-k^2$. Perfect-square trinomial at mid D. OpenStax IA §6.3.",
            engine="poly_skeleton",
        ),
        _a1(
            "conjugate_write",
            "ConjugateWrite — monic quadratic from complex roots",
            "ConjugateWrite",
            "a2_polynomial_functions_conjugate_roots_and_writing_functions",
            "Write $x^2+bx+c$ from $a\pm bi$ roots. OpenStax IA §6.3 / §6.4.",
        ),
        _a1(
            "a2_write_linear",
            "WriteLinear — convert standard / point-slope (A2)",
            "WriteLinear",
            "a2_linear_relations_and_functions_writing_linear_equations",
            r"D=0 $Ax+By=C$ or $y+k=m(x+h)$ → slope-intercept. "
            r"Differs from A1 write-from-points. OpenStax IA §3.1.",
            engine="linear_forms",
        ),
        _a1(
            "log_evaluate",
            "LogEvaluate — evaluate logs / ln",
            "LogEvaluate",
            "a2_exponential_and_logarithmic_expressions_evaluating_logarithms",
            r"D=0 $\log_b(b^k)$. Larger bases / decimals later. OpenStax IA §10.3.",
        ),
        _a1(
            "log_properties",
            "LogProperties — expand / change-of-base",
            "LogProperties",
            "a2_exponential_and_logarithmic_expressions_properties_of_logarithms",
            r"Product, quotient, power rules. OpenStax IA §10.4.",
        ),
        _a1(
            "exp_equation_simple",
            "ExpEquation — same-base exponential",
            "ExpEquation",
            "a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms",
            r"D=0 $b^x=k$ with integer $x$. OpenStax IA §10.2.",
        ),
        _a1(
            "log_equation",
            "LogEquation — solve $\log_b(x)=k$",
            "LogEquation",
            "a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple",
            r"D=0 one log, integer solution. OpenStax IA §10.3.",
        ),
        _a1(
            "arith_sequence",
            "ArithSequence — $a_n$ from $a_1,d$",
            "ArithSequence",
            "a2_sequences_and_series_arithmetic_sequences",
            r"D=0 find $a_4$ given $a_1,d$. OpenStax CA §9.1.",
        ),
        _a1(
            "geom_sequence",
            "GeomSequence — $a_n$ from $a_1,r$",
            "GeomSequence",
            "a2_sequences_and_series_geometric_sequences",
            r"D=0 integer ratio. OpenStax CA §9.3.",
        ),
        _a1(
            "trig_evaluate",
            "TrigEvaluate — exact values (degrees / radians)",
            "TrigEvaluate",
            "a2_trigonometry_trig_functions_of_any_angle",
            r"D=0 $\cos 120°$ / unit-circle angles. OpenStax CA §5.1 / §7.1.",
        ),
        _a1(
            "right_tri_ratio",
            "RightTriRatio — sin / cos / tan from triangle",
            "RightTriRatio",
            "a2_trigonometry_right_triangle_trig_finding_ratios",
            r"D=0 3-4-5 style. OpenStax CA §7.1.",
        ),
        _a1(
            "law_of_sines",
            "LawOfSines — find missing side",
            "LawOfSines",
            "a2_trigonometry_the_law_of_sines",
            "Two angles and one side. OpenStax CA §7.2.",
        ),
        _a1(
            "a2_graph_quadratic",
            "GraphQuadratic — A2 alias (UNCLEAR)",
            "GraphQuadratic",
            "a2_quadratic_functions_and_inequalities_graphing_quadratic_functions",
            "UNCLEAR: graph outside algebraic cores. Red-header samples. OpenStax IA §9.6.",
        ),
        _a1(
            "a2_graph_polynomial",
            "GraphPolynomial — general poly graph (UNCLEAR)",
            "GraphQuadratic",
            "a2_polynomial_functions_graphing",
            "UNCLEAR: may not match degree>2 OpenStax shapes. Red-header samples.",
        ),
        _a1(
            "a2_graph_rational",
            "GraphRational — rational function graph (UNCLEAR)",
            "",
            "a2_rational_expressions_graphing",
            "UNCLEAR: asymptotes/holes — no skeleton core. Red-header samples.",
        ),
        _a1(
            "a2_graph_exp",
            "GraphExponential — A2 alias (UNCLEAR)",
            "",
            "a2_exponential_and_logarithmic_expressions_graphing_exponential_functions",
            "UNCLEAR: graph transforms not locked to OpenStax §10.2. Red-header samples.",
        ),
        _a1(
            "a2_graph_log",
            "GraphLogarithmic — A2 alias (UNCLEAR)",
            "",
            "a2_exponential_and_logarithmic_expressions_graphing_logarithmic_functions",
            "UNCLEAR: no algebraic skeleton. Red-header samples. OpenStax IA §10.3.",
        ),
        _a1(
            "a2_graph_trig",
            "GraphTrig — amplitude / period (UNCLEAR)",
            "",
            "a2_trigonometry_graphing_trig_functions",
            "UNCLEAR: College Algebra §7.6 transforms TBD. Red-header samples.",
        ),
        _a1(
            "a2_graph_conics",
            "GraphConics — circles / parabolas (UNCLEAR)",
            "",
            "a2_conic_sections_circles_graphing_and_properties",
            "UNCLEAR: conic graph engine vs focus/directrix. Red-header samples.",
        ),
        _a1(
            "a2_complex_graph",
            "GraphComplex — complex plane (UNCLEAR)",
            "",
            "a2_complex_numbers_graphing",
            "UNCLEAR: IA §8.8 complex plane. Red-header samples.",
        ),
        _a1(
            "a2_matrix_transforms",
            "MatrixTransform — geometric transforms (UNCLEAR)",
            "",
            "a2_matrices_geometric_transformations",
            "UNCLEAR: matrix × polygon diagram fidelity. Red-header samples.",
        ),
    ]
)

# A1 systems + linear functions (this agent). PA slope/write/sub/graph/WP already
# in the PA block with A1 aliases.
SECTIONS.extend(
    [
        _a1(
            "systems_elimination",
            "LinearSystem — elimination",
            "LinearSystem",
            "systems_elimination",
            r"D=0 already-opposite coeffs (OpenStax EA §5.3 Ex 5.26). "
            "Multiply one, then both. Specials later.",
            engine="systems",
            aliases=[
                "a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables",
            ],
        ),
        _a1(
            "graphing_systems_of_inequalities",
            "GraphSystemIneq — two half-planes",
            "GraphSystemIneq",
            "graphing_systems_of_inequalities",
            r"D=0 $y>x$ and $y<k$. Mixed solid/dashed later. OpenStax EA §5.6.",
            engine="systems",
            aliases=[
                "a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities",
            ],
        ),
        _a1(
            "graphing_linear_equations",
            "GraphLinear — graph $y=mx+b$",
            "GraphLinear",
            "graphing_linear_equations",
            r"D=0 through origin ($y=x$, $y=3x$). Intercept / $Ax+By=C$ later. "
            "OpenStax EA §4.2–4.5.",
            engine="linear_forms",
            aliases=[
                "a2_linear_relations_and_functions_graphing_linear_equations",
            ],
        ),
        _a1(
            "graphing_linear_inequalities",
            "GraphLinearIneq — shade a half-plane",
            "GraphLinearIneq",
            "graphing_linear_inequalities",
            r"D=0 $y\le x$ / $y>3x$. Rearrange later. OpenStax EA §4.7.",
            engine="linear_forms",
            aliases=[
                "a2_linear_relations_and_functions_graphing_linear_inequalities",
            ],
        ),
        _a1(
            "more_on_slope",
            "MoreOnSlope — parallel / perpendicular",
            "MoreOnSlope",
            "more_on_slope",
            r"D=0 obvious parallel slopes. Perpendicular $-1/m$ then write a "
            r"parallel/perp line through a point. OpenStax EA §4.6.",
            engine="linear_forms",
        ),
        _a1(
            "evaluating_graphing_functions",
            "Evaluate $f(a)$ (UNCLEAR — no graph)",
            "",
            "evaluating_graphing_functions",
            "UNCLEAR / LOW_VARIETY: old path is only $f(a)$ for linear $f$. "
            "No graphing. Red-header samples. OpenStax IA §3.6.",
        ),
        _a1(
            "discrete_relations",
            "Discrete relations (UNCLEAR — table fill)",
            "",
            "discrete_relations",
            "UNCLEAR / LOW_VARIETY: old path completes a $y=mx+b$ table, not "
            "domain/range / function test (IA §3.5). Red-header samples.",
        ),
        _a1(
            "continuous_relations",
            "Continuous relations (UNCLEAR — evaluate $y$)",
            "",
            "continuous_relations",
            "UNCLEAR / LOW_VARIETY: old path is $y$ when $x=a$ for $y=mx+b$. "
            "No graph. Red-header samples.",
        ),
        _a1(
            "graphing_absolute_value_equations",
            "Graph $y=a|x-h|+k$ (UNCLEAR gold)",
            "",
            "graphing_absolute_value_equations",
            "UNCLEAR: not in Elementary Algebra TOC. Gold is College Algebra §3.6 "
            "+ old vertex/V-shape. Red-header samples of existing graph engine.",
            aliases=[
                "a2_linear_relations_and_functions_graphing_absolute_value_equations",
            ],
        ),
    ]
)

# A2 shipped leaves (complex, 3-var, variation) + graphing red-header aliases.
SECTIONS.extend(
    [
        _a1(
            "a2_system_three_variables",
            "LinearSystem3 — 3×3 elimination",
            "LinearSystem3",
            "a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables",
            r"D=0 integer 3×3 with unique solution. Larger coeffs at high D. "
            "OpenStax IA §4.4.",
            engine="systems",
        ),
        _a1(
            "a2_complex_operations",
            "ComplexOp — add / subtract / multiply",
            "ComplexOp",
            "a2_complex_numbers_operations",
            r"D=0 small $a+bi$. FOIL multiply at high D. OpenStax CA §2.4.",
            engine="complex_algebra",
        ),
        _a1(
            "a2_complex_absolute_value",
            "ComplexAbs — $|a+bi|$",
            "ComplexAbs",
            "a2_complex_numbers_absolute_value",
            r"D=0 modulus with simplified radical. OpenStax CA §2.4.",
            engine="complex_algebra",
        ),
        _a1(
            "a2_complex_rationalize",
            "ComplexRationalize — conjugate in denominator",
            "ComplexRationalize",
            "a2_complex_numbers_rationalizing_denominators",
            r"D=0 real over $a+bi$ or pure imaginary. OpenStax CA §2.4.",
            engine="complex_algebra",
        ),
        _a1(
            "direct_inverse_variation",
            "VariationEq — direct + inverse stories (A1)",
            "VariationEq",
            "direct_inverse_variation",
            "Rotates direct (rate, cost, given-$k$) and inverse frames. "
            "Not inverse-only. OpenStax EA §8.9. Opt out with "
            "<code>use_legacy_variation=True</code>.",
            engine="variation_packaging",
            aliases=[
                "a2_direct_and_inverse_variation_direct_and_inverse_variation",
            ],
        ),
        _a1(
            "graph_rational",
            "GraphRational — rational function (UNCLEAR)",
            "",
            "graph_rational",
            "Graphing-only; no honest algebraic core. Red-header samples.",
            aliases=["a2_rational_expressions_graphing"],
        ),
        _a1(
            "graph_radical",
            "GraphRadical — square-root graph (UNCLEAR)",
            "",
            "graph_radical",
            "Graphing-only. Red-header samples of existing graph engine.",
            aliases=[
                "a2_radical_functions_and_rational_exponents_graphing_radical_equations",
            ],
        ),
        _a1(
            "complex_graph",
            "ComplexGraph — plot on complex plane (UNCLEAR)",
            "",
            "complex_graph",
            "Graphing-only. Red-header samples.",
            aliases=["a2_complex_numbers_graphing"],
        ),
    ]
)

SECTIONS.extend(
    [
        {
            "slug": "pc_fundamental_identities",
            "title": "TrigRewrite — fundamental identities (PC §7.1)",
            "pattern": "TrigRewrite",
            "engine": "trig_skeleton",
            "type_id": "pc_fundamental_identities",
            "aliases": ["trig_basic_identities"],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": (
                "Live default for <code>pc_fundamental_identities</code>. "
                "Goal-first Pythagorean / reciprocal / product simplify; verify at D≥8. "
                "Opt out with <code>use_sample_trig_identities=True</code>. "
                "Notes flag <code>LOW_VARIETY</code> (verify LHS=RHS partial)."
            ),
        },
        {
            "slug": "pc_sum_and_difference_identities",
            "title": "TrigSumDiff — sum/difference (PC §7.2)",
            "pattern": "TrigSumDiff",
            "engine": "trig_skeleton",
            "type_id": "pc_sum_and_difference_identities",
            "aliases": ["trig_sum_difference"],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": (
                "Live default for <code>pc_sum_and_difference_identities</code>. "
                "D=0 expands sin/cos(α±β); tan + exact-eval unlock at higher D. "
                "Opt out with <code>use_sample_trig_identities=True</code>."
            ),
        },
        {
            "slug": "pc_multiple_angle_identities",
            "title": "TrigDoubleAngle — double-angle (PC §7.3)",
            "pattern": "TrigDoubleAngle",
            "engine": "trig_skeleton",
            "type_id": "pc_multiple_angle_identities",
            "aliases": ["trig_multiple_angle"],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": (
                "Live default for <code>pc_multiple_angle_identities</code>. "
                "D=0 sin/cos(2θ); tan + alt cos forms unlock later. Half-angle deferred. "
                "Opt out with <code>use_sample_trig_identities=True</code>."
            ),
        },
        {
            "slug": "pc_product_to_sum_identities",
            "title": "TrigProductToSum — product→sum (PC §7.4)",
            "pattern": "TrigProductToSum",
            "engine": "trig_skeleton",
            "type_id": "pc_product_to_sum_identities",
            "aliases": ["trig_product_to_sum"],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": (
                "Live default for <code>pc_product_to_sum_identities</code>. "
                "D=0 sin A cos B; fuller product pool at higher D. Sum→product stub. "
                "Opt out with <code>use_sample_trig_identities=True</code>."
            ),
        },
        {
            "slug": "pc_equations_with_factoring_and_fundamental_identities",
            "title": "TrigFactorEq — factoring equations (PC §7.5)",
            "pattern": "TrigFactorEq",
            "engine": "trig_skeleton",
            "type_id": "pc_equations_with_factoring_and_fundamental_identities",
            "aliases": ["trig_factoring_equations"],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "blurb": (
                "Live default for <code>pc_equations_with_factoring_and_fundamental_identities</code>. "
                "D=0 quadratic-in-trig; factor / double-angle unlock at higher D. "
                "Opt out with <code>use_sample_trig_equations=True</code>."
            ),
        },
    ]
)

# Precalc leaves still on ``precalc_foundations`` stub — need dedicated skeleton.
PC_DEFERRED: frozenset[str] = frozenset()

# Skeleton pattern when live metadata stamps one (empty = no pattern warn).
PC_PATTERN_OVERRIDES: dict[str, str] = {
    "pc_rational_equations": "EqCancel",
    "pc_dividing_polynomial_functions": "PolyLongDiv",
    "pc_parabolas_graphing_and_properties": "GraphQuadratic",
    "pc_fundamental_identities": "TrigRewrite",
    "pc_sum_and_difference_identities": "TrigSumDiff",
    "pc_multiple_angle_identities": "TrigDoubleAngle",
    "pc_product_to_sum_identities": "TrigProductToSum",
    "pc_equations_with_factoring_and_fundamental_identities": "TrigFactorEq",
}

# Hand-built PC sections (override auto slug if present).
PC_MANUAL_SLUGS: frozenset[str] = frozenset(
    {
        "pc_fundamental_identities",
        "pc_sum_and_difference_identities",
        "pc_multiple_angle_identities",
        "pc_product_to_sum_identities",
        "pc_equations_with_factoring_and_fundamental_identities",
    }
)


def _pc(
    slug: str,
    title: str,
    pattern: str,
    type_id: str,
    blurb: str,
    *,
    aliases: list[str] | None = None,
    engine: str = "pc_reuse",
) -> dict[str, Any]:
    return {
        "slug": slug,
        "title": title,
        "pattern": pattern,
        "engine": engine,
        "type_id": type_id,
        "aliases": aliases or [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": blurb,
    }


def _build_pc_sections() -> list[dict[str, Any]]:
    from question_engine.catalogs.precalculus import CATALOG

    sections: list[dict[str, Any]] = []
    for entry in CATALOG:
        tid = str(entry.id)
        if (
            not tid.startswith("pc_")
            or tid in PC_DEFERRED
            or tid in PC_MANUAL_SLUGS
        ):
            continue
        gen = str(entry.generator or "precalc_foundations")
        pat = PC_PATTERN_OVERRIDES.get(tid, "")
        title = f"PC — {entry.name}"
        blurb = (
            f"Live <code>{gen}</code> engine (reuse, no rewrite-skeleton). "
            f"D=0 simple per <code>notes/{tid}.md</code>. "
            "OpenStax PC cite in notes."
        )
        sections.append(
            _pc(
                tid,
                title,
                pat,
                tid,
                blurb,
                engine=gen,
            )
        )
    return sections


SECTIONS.extend(_build_pc_sections())

# Calculus limits / continuity / L'Hôpital — LimitSpec + limits.json (not Diff skeleton).
def _calc_limit(
    slug: str,
    title: str,
    type_id: str,
    engine: str,
    blurb: str,
) -> dict[str, Any]:
    return {
        "slug": slug,
        "title": title,
        "pattern": "",
        "engine": engine,
        "type_id": type_id,
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": (101, 207, 313),
        "blurb": blurb,
    }


SECTIONS.extend(
    [
        _calc_limit(
            "calc_limits_by_direct_evaluation",
            "LimitSpec — direct evaluation (Calc §2.3)",
            "calc_limits_by_direct_evaluation",
            "limit_direct",
            "Live <code>limit_direct_evaluation</code> via LimitSpec / <code>limits.json</code>. "
            "Poly / rational / trig / exp / root plug-in. Not Diff <code>expr_skeleton</code>.",
        ),
        _calc_limit(
            "calc_limits_at_jump_discontinuities_and_kinks",
            "LimitSpec — jump discontinuities (Calc §2.4)",
            "calc_limits_at_jump_discontinuities_and_kinks",
            "limit_jump",
            "Piecewise const → linear → poly sides; optional one-sided lim. "
            "Structural <code>jump_side_*</code> upgrades (no whole-prompt scale).",
        ),
        _calc_limit(
            "calc_limits_at_removable_discontinuities",
            "LimitSpec — removable discontinuities (Calc §2.3–2.4)",
            "calc_limits_at_removable_discontinuities",
            "limit_removable",
            "Factor cancel / rationalize hole limits. Expanded presentations at mid/high D.",
        ),
        _calc_limit(
            "calc_limits_at_essential_discontinuities",
            "LimitSpec — essential discontinuities (Calc §2.2–2.4)",
            "calc_limits_at_essential_discontinuities",
            "limit_essential",
            "1/x, 1/x², rational VA, sin/cos(1/x), tan asymptote + Spec dress wraps.",
        ),
        _calc_limit(
            "calc_limits_at_infinity",
            "LimitSpec — limits at infinity (Calc §4.6)",
            "calc_limits_at_infinity",
            "limit_infinity",
            "Rational degree compare; sin/x; arctan; exp ratio; ln/x^k.",
        ),
        _calc_limit(
            "calc_continuity_determining_and_classifying",
            "LimitSpec — continuity classify (Calc §2.4)",
            "calc_continuity_determining_and_classifying",
            "limit_continuity",
            "Classify continuous / removable / jump / essential at a point.",
        ),
        _calc_limit(
            "calc_app_diff_lhopitals_rule",
            "LimitSpec — L'Hôpital (Calc §4.8)",
            "calc_app_diff_lhopitals_rule",
            "limit_lhopital",
            "0/0, ∞/∞, 0·∞, ∞−∞, exponential indeterminate forms; multipass. "
            "Limit pack — not Diff skeleton.",
        ),
    ]
)

# Calculus Diff leaves already on expr_skeleton (+ implicit Mad-Lib red-header).
SECTIONS.extend(
    [
        {
            "slug": "calc_diff_power_rule",
            "title": "Diff — Power Rule",
            "pattern": "Diff(Pow(H,n))",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_power_rule",
            "aliases": ["pc_power_rule_for_differentiation"],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": (
                "First-derivative power / roots. OpenStax Calc Vol.1 §3.3. "
                "Higher order → <code>calc_diff_higher_order_derivatives</code>."
            ),
        },
        {
            "slug": "calc_diff_product_rule",
            "title": "Diff — Product Rule",
            "pattern": "Diff(Prod(F,G))",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_product_rule",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": (
                "Algebraic uv at D=0; mid/high product+chain "
                r"($(ax+b)^n(cx+d)^m$, poly$\times(u)^n$). "
                "OpenStax Calc Vol.1 §3.3 / §3.6 Example 3.54."
            ),
        },
        {
            "slug": "calc_diff_quotient_rule",
            "title": "Diff — Quotient Rule",
            "pattern": "Diff(Quot(F,G))",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_quotient_rule",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": (
                "Poly/poly by default; exp/log quotients need allow_*. "
                "OpenStax Calc Vol.1 §3.3."
            ),
        },
        {
            "slug": "calc_diff_chain_rule",
            "title": "Diff — Chain Rule",
            "pattern": "Diff(Pow(H,n))",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_chain_rule",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": r"$(ax+b)^n$ at D=0; unlike $f(g)$ / $f(g(h))$ at mid/high. OpenStax Calc Vol.1 §3.6.",
        },
        {
            "slug": "calc_diff_trigonometric",
            "title": "Diff — Trigonometric",
            "pattern": "Diff(Apply(fn,u))",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_trigonometric",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": "Trig + chain / trig×trig. OpenStax Calc Vol.1 §3.5–3.6.",
        },
        {
            "slug": "calc_diff_inverse_trigonometric",
            "title": "Diff — Inverse trigonometric",
            "pattern": "Diff(Apply",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_inverse_trigonometric",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": "arcsin / arctan + chain. OpenStax Calc Vol.1 §3.7.",
        },
        {
            "slug": "calc_diff_natural_logarithms_and_exponentials",
            "title": "Diff — Natural logarithms and exponentials",
            "pattern": "Diff(Apply",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_natural_logarithms_and_exponentials",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": r"$e^u$, $\ln u$, products. OpenStax Calc Vol.1 §3.9.",
        },
        {
            "slug": "calc_diff_general",
            "title": "Diff — General derivatives",
            "pattern": "Diff(",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_general",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": "Mixed rules across classes. OpenStax Calc Vol.1 §3.3–3.9.",
        },
        {
            "slug": "calc_diff_higher_order_derivatives",
            "title": "Diff — Higher order derivatives",
            "pattern": "Diff(Pow(H,n))",
            "engine": "expr_skeleton",
            "type_id": "calc_diff_higher_order_derivatives",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": (
                r"Always $d^2/dx^2$ (or higher). OpenStax Calc Vol.1 §3.2–3.3."
            ),
        },
        {
            "slug": "calc_diff_implicit",
            "title": "Diff — Implicit (OpenStax §3.8 catalog)",
            "pattern": "Diff(implicit",
            "engine": "structured_implicit",
            "type_id": "calc_diff_implicit",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": (
                "Catalog-routed circle / ellipse / xy / cubes / trig / folium. "
                "D=0 stays circle. OpenStax Calc Vol.1 §3.8."
            ),
        },
        {
            "slug": "calc_diff_logarithmic",
            "title": "Diff — Logarithmic differentiation (OpenStax §3.9 catalog)",
            "pattern": "Diff(logarithmic",
            "engine": "structured_logarithmic",
            "type_id": "calc_diff_logarithmic",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": (
                "Catalog-routed power / product / quotient / root / x^x. "
                "D=0 stays x^n. OpenStax Calc Vol.1 §3.9."
            ),
        },
        {
            "slug": "calc_diff_other_base_logarithms_and_exponentials",
            "title": "Diff — Other-base log/exp (OpenStax §3.9 catalog)",
            "pattern": "Diff(other_base",
            "engine": "structured_other_base",
            "type_id": "calc_diff_other_base_logarithms_and_exponentials",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": (
                r"Catalog-routed $a^x$ / $\log_a x$ at D=0; $a^{kx}$ / $\log_a(ax+b)$ mid; "
                r"$a^{x^2}$ / $x a^x$ high. OpenStax Calc Vol.1 §3.9."
            ),
        },
        {
            "slug": "calc_diff_inverse_functions",
            "title": "Diff — Inverse functions (OpenStax §3.7 catalog)",
            "pattern": "Diff(inverse_functions",
            "engine": "structured_inverse_functions",
            "type_id": "calc_diff_inverse_functions",
            "aliases": [],
            "ladder_ds": (0.0, 8.0, 16.0, 22.0),
            "ladder_seeds": (101, 207, 313),
            "pattern_soft": True,
            "blurb": (
                r"IFT $(f^{-1})'(f(a))=1/f'(a)$. D=0 $x^n$; mid table/linear; "
                r"high $\sin x$ / $\ln$ / $x^3+x$ (not leftover $e^x$). OpenStax Calc Vol.1 §3.7."
            ),
        },
    ]
)

# Calculus integrals / apps — reuse integrals.py + related_rates frames.
CALC_UNCLEAR: frozenset[str] = frozenset()

CALC_INTEGRAL_APP_SHIPPED: list[tuple[str, str, str]] = [
    (
        "calc_indef_int_power_rule",
        "Integral — power rule",
        "Reuse <code>integrals.py</code> power pack. D=0 constant/√x; OpenStax Vol 1 §4.10.",
    ),
    (
        "calc_indef_int_logarithmic_rule_and_exponentials",
        "Integral — ln / exp",
        "Forward ln/exp forms. OpenStax Vol 1 §5.6 / Vol 2.",
    ),
    (
        "calc_indef_int_trigonometric",
        "Integral — trig",
        "Basic trig antiderivatives. OpenStax Vol 1 §5.7.",
    ),
    (
        "calc_indef_int_inverse_trigonometric",
        "Integral — inverse trig",
        "arcsin / arctan cores. OpenStax Vol 1 §5.7.",
    ),
    (
        "calc_indef_int_power_rule_with_substitution",
        "Integral — u-sub (power)",
        "Derivative-backed linear/quad u-sub. OpenStax Vol 1 §5.5.",
    ),
    (
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
        "Integral — u-sub (ln/exp)",
        "u-sub ln/exp pack. OpenStax Vol 1 §5.5–5.6.",
    ),
    (
        "calc_indef_int_trigonometric_with_substitution",
        "Integral — trig sub",
        "Genuine a²±x² forms (not plain u-sub). OpenStax Vol 2 §3.3. Named preset <code>trig_sub_form_preset=bc_bank</code> for §5 lookalikes; <code>√(a²−x²)/x</code> deferred.",
    ),
    (
        "calc_indef_int_inverse_trigonometric_with_substitution",
        "Integral — invtrig u-sub",
        "arctan-of-linear style. OpenStax Vol 1 §5.7.",
    ),
    (
        "calc_indef_int_integration_by_parts",
        "Integral — by parts",
        "LIATE catalog: D=0 one-step (ln / xe^x / x sin x); mid D scales k; high D tabular n≤3 + (ln)^n + cyclic + invtrig. OpenStax Vol 2 §3.1 + BC bank §2 lookalikes.",
    ),
    (
        "calc_indef_int_partial_fractions",
        "Integral — PFD",
        "Reuse <code>partial_fractions</code> constructive core then integrate. OpenStax Vol 2 §3.4. Named preset <code>pfd_form_preset=bc_bank</code> for §4 lookalikes; <code>x4_plus_1</code> deferred.",
    ),
    (
        "calc_indef_int_multi_trick",
        "Integral — multi-trick (u-sub→PFD)",
        "Ordered pipeline <code>[u_sub, pfd]</code>. OpenStax Vol 2 §3.4.",
    ),
    (
        "calc_indef_int_general",
        "Integral — general (toggles)",
        "Mixed techniques. Teacher <code>allow_*</code> checkboxes drop catalog "
        "forms whose <code>requires_allows</code> / <code>tricks</code> are off. "
        "D=0 stays power/table; bank-hard families unlock mid/high D.",
    ),
    (
        "calc_def_int_first_fundamental_theorem_of_calculus",
        "FTC — evaluate ∫_a^b",
        "Antiderivative evaluation (OpenStax Part 2). Numeric hardness by D.",
    ),
    (
        "calc_def_int_second_fundamental_theorem_of_calculus",
        "FTC — d/dx ∫_a^{g(x)}",
        "Variable-upper derivative (OpenStax Part 1). Chain unlock at high D.",
    ),
    (
        "calc_def_int_substitution_with_change_of_variables",
        "Definite u-sub (change limits)",
        "Definite integrals with changed u-limits. OpenStax Vol 1 §5.5.",
    ),
    (
        "calc_app_int_area_under_a_curve",
        "App — area under a curve",
        "Constructive area wordings; D=0 linear. OpenStax Vol 1 §5.2 / §6.1.",
    ),
    (
        "calc_app_diff_related_rates",
        "App — related rates (OpenStax frames)",
        "Rotates OpenStax §4.1 frames (circle / balloon / ladder / shadow / "
        "cone-drain / two-rate / rocket angle). D=0 circle only; high D locks "
        "out easy leftovers and adds extra chain (two rates, similar-triangle "
        "inverse, elevation angle).",
    ),
    (
        "calc_app_diff_slope_tangent_and_normal_lines",
        "App — tangent / normal lines",
        "Pilot <code>tangent_normal_line</code>. OpenStax Vol 1 §3.1 / §4.2.",
    ),

    (
        "calc_app_diff_rolles_theorem",
        "App — Rolle's Theorem",
        "D=0 even-quad leftover (old easy, c=0); D≥8 two-root quadratics; "
        "high D odd cubic (OpenStax Ex. 4.14) and locks out even-quad c=0. "
        "OpenStax Vol 1 §4.4.",
    ),

    (
        "calc_app_diff_mean_value_theorem",
        "App — Mean Value Theorem (diff)",
        "D=0 x^2 leftover (old easy); D≥8 unlocks kx^3; high D "
        "OpenStax Ex. 4.15 sqrt(x) and locks out the quadratic. "
        "OpenStax Vol 1 §4.4.",
    ),

    (
        "calc_app_diff_intervals_of_increase_and_decrease",
        "App — intervals of increase/decrease",
        "D=0 parabola leftover (old easy); D≥8 unlocks odd cubics; high D "
        "shifted cubics (OpenStax Ex. 4.17) and locks out the parabola. "
        "OpenStax Vol 1 §4.5.",
    ),

    (
        "calc_app_diff_differentials",
        "App — differentials",
        "dy = f'(x) dx. OpenStax Vol 1 §4.2.",
    ),

    (
        "calc_app_diff_linear_approximations",
        "App — linear approximations",
        "L(x)=f(a)+f'(a)(x-a). OpenStax Vol 1 §4.2.",
    ),

    (
        "calc_def_int_approximating_area_under_a_curve",
        "Riemann — approximate area",
        "Left/right/mid + linear/quad curves. OpenStax Vol 1 §5.1.",
    ),

    (
        "calc_def_int_area_under_a_curve_by_limit_of_sums",
        "Area by limit of sums",
        "Reuse area_under_curve / limit-of-sums path. OpenStax Vol 1 §5.2.",
    ),

    (
        "calc_def_int_riemann_sum_tables",
        "Riemann sums from tables",
        "Left/right/mid from value tables. OpenStax Vol 1 §5.1.",
    ),

    (
        "calc_def_int_mean_value_theorem",
        "Integral MVT — average value",
        "Average value of f on [a,b]. OpenStax Vol 1 §5.4 / §6.x.",
    ),

    (
        "calc_app_int_area_between_curves",
        "App — area between curves",
        "∫(top−bottom); D unlocks. OpenStax Vol 1 §6.1.",
    ),

    (
        "calc_app_int_volume_by_slicing_disks_and_washers",
        "App — disk / washer volumes",
        "Rotate about x-axis. OpenStax Vol 1 §6.2.",
    ),

    (
        "calc_app_int_volume_by_cylinders",
        "App — shell method volumes",
        "Rotate about y-axis. OpenStax Vol 1 §6.3.",
    ),

    (
        "calc_app_int_volume_of_solids_with_known_cross_sections",
        "App — known cross sections",
        "Square / equilateral / semicircle. OpenStax Vol 1 §6.2.",
    ),

    (
        "calc_diff_eq_slope_fields",
        "DE — slope field interpret",
        "Evaluate y' at a point. OpenStax Vol 2 §4.1–4.2.",
    ),

    (
        "calc_diff_eq_separable",
        "DE — separable",
        "IVP poly / exp / homogeneous. OpenStax Vol 2 §4.3.",
    ),

    (
        "calc_diff_eq_exponential_growth_and_decay",
        "DE — continuous growth/decay",
        "y'=ky models (not Algebra discrete %). OpenStax Vol 1 §6.8.",
    ),

    (
        "calc_diff_average_rates_of_change",
        "Diff — average rate of change",
        "Δf/Δx on [a,b]. OpenStax Vol 1 §3.4.",
    ),

    (
        "calc_diff_definition_of_the_derivative",
        "Diff — definition of the derivative",
        "Limit definition. OpenStax Vol 1 §3.1.",
    ),

    (
        "calc_diff_instantaneous_rates_of_change",
        "Diff — instantaneous rate",
        "f'(a) as rate. OpenStax Vol 1 §3.4.",
    ),

    (
        "calc_diff_rules_using_tables",
        "Diff — rules from tables",
        "Product/quotient/chain from tabulated values. OpenStax Vol 1 §3.3.",
    ),

    (
        "calc_app_diff_limits_in_form_of_definition_of_derivative",
        "App — limits as definition of derivative",
        "Recognize lim as f'(a). OpenStax Vol 1 §3.1.",
    ),
    (
        "calc_app_diff_relative_extrema",
        "App — relative extrema",
        "D=0 parabola leftover (old easy); D≥8 unlocks odd cubics; high D "
        "shifted cubics (OpenStax Ex. 4.17) and locks out the parabola. "
        "OpenStax Vol 1 §4.3/4.5.",
    ),
    (
        "calc_app_diff_absolute_extrema",
        "App — absolute extrema",
        "D=0 parabola leftover (old easy); D≥8 unlocks odd cubics on a closed "
        "interval; high D shifted cubics (OpenStax Ex. 4.17 / §4.3 EVT) and "
        "locks out the parabola. OpenStax Vol 1 §4.3.",
    ),
    (
        "calc_app_diff_intervals_of_concavity",
        "App — concavity",
        "D=0 odd-power ray leftover (old easy); D≥8 odd cubics inflecting at 0; "
        "high D shifted cubics (OpenStax Ex. 4.19) and locks out inflection-at-0. "
        "OpenStax Vol 1 §4.5.",
    ),
    (
        "calc_app_diff_optimization",
        "App — optimization (OpenStax frames)",
        "Rotates OpenStax §4.7 frames (pen / garden-or-river / box / revenue / "
        "inscribed rectangle / cylinder). D=0 rectangle-only; high D locks out "
        "easy leftovers.",
    ),
    (
        "calc_app_diff_curve_sketching",
        "App — curve sketching",
        "D=0 parabola leftover (old easy); D≥8 odd cubics inflecting at 0; "
        "high D shifted cubics (same idea as Ex. 4.19) and locks out "
        "inflection-at-0. Checklist, not a drawn graph. OpenStax Vol 1 §4.5.",
    ),
    (
        "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime",
        "App — sign of f′ (no figure bank)",
        "Increasing/decreasing from an explicit f'. LIMITATIONS: no graph-match figures. OpenStax Vol 1 §4.5.",
    ),
    (
        "calc_app_diff_motion_along_a_line",
        "App — motion along a line",
        "D=0 quadratic leftover (old easy eval v); D≥8 rest; high D "
        "OpenStax Ex. 3.36 cubics (two rest times) and Ex. 3.35 speed/direction, "
        "locks out t^2-nt. OpenStax Vol 1 §3.4.",
    ),
    (
        "calc_app_diff_newtons_method",
        "App — Newton's method",
        "D=0 one quadratic leftover (old easy); D≥8 one cubic step; high D "
        "two cubic steps and locks out x^2-a. OpenStax Vol 1 §4.9.",
    ),
    (
        "calc_app_int_motion_along_a_line_revisited",
        "App — motion revisited (integral)",
        "D=0 linear leftover (old easy v=2t); D≥8 const v; high D "
        "sign-change net 0 and locks out linear. OpenStax Vol 1 §5.4.",
    ),
    (
        "calc_diff_eq_introduction",
        "DE — introduction",
        "D=0 exponential leftover (old easy y=Ce^{kx}); D≥8 Euler y=Cx^n; "
        "high D locks out exp. OpenStax Vol 2 §4.1.",
    ),

]

CALC_UNCLEAR_TITLES: dict[str, str] = {
    "calc_app_diff_intervals_of_concavity": "App — concavity (UNCLEAR)",
    "calc_app_diff_relative_extrema": "App — relative extrema (UNCLEAR)",
    "calc_app_diff_absolute_extrema": "App — absolute extrema (UNCLEAR)",
    "calc_app_diff_optimization": "App — optimization (UNCLEAR)",
    "calc_app_diff_curve_sketching": "App — curve sketching (UNCLEAR)",
    "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime": (
        "App — graphical f / f′ / f″ (UNCLEAR)"
    ),
    "calc_app_diff_motion_along_a_line": "App — motion along a line (UNCLEAR)",
    "calc_app_diff_newtons_method": "App — Newton's method (UNCLEAR)",
    "calc_app_int_motion_along_a_line_revisited": (
        "App — motion revisited (UNCLEAR)"
    ),
    "calc_diff_eq_introduction": "DE — introduction (UNCLEAR)",
}


def _calc_sec(
    type_id: str,
    title: str,
    blurb: str,
    *,
    engine: str = "integrals",
    slug: str | None = None,
    pattern: str = "",
    extra_settings: dict[str, Any] | None = None,
    ladder_seeds: tuple[int, ...] | None = None,
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "slug": slug or type_id,
        "title": title,
        "pattern": pattern,
        "engine": engine,
        "type_id": type_id,
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0, 22.0),
        "ladder_seeds": ladder_seeds or (101, 207, 313),
        "blurb": blurb,
    }
    if extra_settings:
        rec["extra_settings"] = extra_settings
    return rec


# Named u-sub form presets + reverse-chain (showcase galleries; share leaf type_ids).
# Presets from ``u_substitution.U_SUB_FORM_PRESETS`` / OpenStax Vol 1 §5.5–5.7.
CALC_USUB_PRESET_SHOWCASE: list[tuple[str, str, str, str, dict[str, Any]]] = [
    (
        "u_sub_preset_power_linear",
        "calc_indef_int_power_rule_with_substitution",
        "u-sub preset — power_linear",
        "Forced <code>u_sub_form_preset=power_linear</code> (∫ a(ax+b)^n). OpenStax Vol 1 §5.5.",
        {"u_sub_form_preset": "power_linear", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_power_quadratic",
        "calc_indef_int_power_rule_with_substitution",
        "u-sub preset — power_quadratic",
        "Forced <code>power_quadratic</code> (quad / root·x du). OpenStax Vol 1 §5.5.",
        {"u_sub_form_preset": "power_quadratic", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_power_cubic",
        "calc_indef_int_power_rule_with_substitution",
        "u-sub preset — power_cubic",
        "Forced <code>power_cubic</code> (x² (x³±c)^n). OpenStax Vol 1 §5.5 Checkpoint 5.25–5.26.",
        {"u_sub_form_preset": "power_cubic", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_du_over_u",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
        "u-sub preset — du/u",
        "Forced <code>du_over_u</code> (∫ g'/g). OpenStax Vol 1 §5.6.",
        {"u_sub_form_preset": "du_over_u", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_exp_chain",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
        "u-sub preset — exp_chain",
        "Forced <code>exp_chain</code> (e^{g} g'). OpenStax Vol 1 §5.6.",
        {"u_sub_form_preset": "exp_chain", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_trig_chain",
        "calc_indef_int_power_rule_with_substitution",
        "u-sub preset — trig_chain",
        "Forced <code>trig_chain</code> (sin/cos/sec² of u). OpenStax Vol 1 §5.7.",
        {"u_sub_form_preset": "trig_chain", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_arctan_chain",
        "calc_indef_int_inverse_trigonometric_with_substitution",
        "u-sub preset — arctan_chain",
        "Forced <code>arctan_chain</code>. OpenStax Vol 1 §5.7.",
        {"u_sub_form_preset": "arctan_chain", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_ln_power_chain",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
        "u-sub preset — ln_power_chain",
        "Forced <code>ln_power_chain</code> ((ln|g|)^2 / (ln x)^n / x). OpenStax Vol 1 §5.6 + BC bank.",
        {"u_sub_form_preset": "ln_power_chain", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_alteration",
        "calc_indef_int_power_rule_with_substitution",
        "u-sub preset — alteration",
        "Forced <code>alteration</code> (linear-over-root rewrite). OpenStax Vol 1 §5.5.",
        {"u_sub_form_preset": "alteration", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_challenging",
        "calc_indef_int_power_rule_with_substitution",
        "u-sub preset — challenging",
        "Forced EMH-hard <code>challenging</code> form set from "
        "<code>u_substitution.json</code> (cubic, root-quad, alteration, …).",
        {"u_sub_form_preset": "challenging", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_challenging_ln_exp",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
        "u-sub preset — challenging (ln/exp)",
        "Forced <code>challenging</code> on the ln/exp host (exp-cubic / exp-quartic / "
        "exp-root / ln-power, …). OpenStax Vol 1 §5.6 Checkpoint 5.33.",
        {"u_sub_form_preset": "challenging", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_bc_bank",
        "calc_indef_int_power_rule_with_substitution",
        "u-sub preset — bc_bank (power)",
        "Forced Calc BC drill-bank §1 families on the power host "
        "(<code>power_quad_neg</code>, roots, hex, …). D=0 auto stays OpenStax easy.",
        {"u_sub_form_preset": "bc_bank", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_preset_bc_bank_ln_exp",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
        "u-sub preset — bc_bank (ln/exp)",
        "Forced BC bank §1 ln/exp families "
        "(<code>ln_power_over_x</code>, <code>exp_over_power_of_exp</code>, …).",
        {"u_sub_form_preset": "bc_bank", "u_sub_construction": "catalog"},
    ),
    (
        "u_sub_reverse_chain",
        "calc_indef_int_power_rule_with_substitution",
        "u-sub — reverse chain (Diff → ∫)",
        "Forced <code>u_sub_construction=reverse_chain</code>: sample F∘g from Diff "
        "<code>expr_skeleton</code>, prompt F′g′, answer F+C.",
        {"u_sub_form_preset": "auto", "u_sub_construction": "reverse_chain"},
    ),
    (
        "u_sub_reverse_chain_ln_exp",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
        "u-sub — reverse chain (ln/exp)",
        "Reverse-chain on the ln/exp substitution leaf.",
        {"u_sub_form_preset": "auto", "u_sub_construction": "reverse_chain"},
    ),
    (
        "u_sub_reverse_chain_invtrig",
        "calc_indef_int_inverse_trigonometric_with_substitution",
        "u-sub — reverse chain (invtrig)",
        "Reverse-chain on the invtrig substitution leaf (also EMH hard preset path).",
        {
            "u_sub_form_preset": "arctan_chain",
            "u_sub_construction": "reverse_chain",
        },
    ),
]


# Named IBP / PFD / trig-sub bank presets (Calc BC drill bank §2 / §4 / §5).
CALC_PARTS_PFD_PRESET_SHOWCASE: list[tuple[str, str, str, str, dict[str, Any]]] = [
    (
        "parts_preset_bc_bank",
        "calc_indef_int_integration_by_parts",
        "Parts preset — bc_bank",
        "Forced Calc BC drill-bank §2 LIATE lookalikes "
        "(<code>x^n e^{ax}</code>, <code>x^n sin/cos</code>, <code>(ln x)^n</code>, "
        "x arctan/arcsin, cyclic). Host D=0 stays one-step LIATE (<code>auto</code>).",
        {"parts_form_preset": "bc_bank"},
    ),
    (
        "pfd_preset_bc_bank",
        "calc_indef_int_partial_fractions",
        "PFD preset — bc_bank",
        "Forced BC bank §4 families the existing PFD core can emit "
        "(distinct linear 2/3, mixed linear-quad, repeated square, irreducible quad). "
        "<code>1/(x^4+1)</code> and <code>(x^2+1)^2</code> stay deferred.",
        {"pfd_form_preset": "bc_bank"},
    ),
    (
        "trig_sub_preset_bc_bank",
        "calc_indef_int_trigonometric_with_substitution",
        "Trig-sub preset — bc_bank",
        "Forced BC bank §5 algebraic-radical lookalikes "
        "(<code>√(x²±a²)</code>, <code>1/√</code>, <code>x²/√</code>, "
        "<code>( )^{±3/2}</code>). Host D=0 stays OpenStax "
        "<code>√(a²−x²)</code>. <code>√(a²−x²)/x</code> and <code>x³/√</code> deferred.",
        {"trig_sub_form_preset": "bc_bank"},
    ),
]


def _build_calc_integral_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for tid, title, blurb in CALC_INTEGRAL_APP_SHIPPED:
        eng = "integrals"
        extra_seeds: tuple[int, ...] | None = None
        if "related_rates" in tid:
            eng = "related_rates_frames"
            # Extra seeds so same-D rotation is visible (101/207/313 can collide).
            extra_seeds = (101, 207, 313, 0, 2, 5, 7)
        elif tid in (
            "calc_app_diff_optimization",
            "calc_app_diff_intervals_of_increase_and_decrease",
            "calc_app_diff_intervals_of_concavity",
            "calc_app_diff_mean_value_theorem",
            "calc_app_diff_relative_extrema",
            "calc_app_diff_absolute_extrema",
        ):
            eng = "calc_apps"
            extra_seeds = (101, 207, 313, 0, 2, 5, 7)
        elif tid == "calc_app_int_area_under_a_curve":
            eng = "area_under_curve"
        elif tid == "calc_app_int_area_between_curves":
            eng = "area_between_curves"
        elif "volume" in tid:
            eng = "volumes"
        elif "riemann" in tid or tid == "calc_def_int_approximating_area_under_a_curve":
            eng = "riemann"
        elif tid.startswith("calc_diff_eq_"):
            eng = "diff_eq"
        elif tid.startswith("calc_app_diff_") or tid.startswith("calc_diff_"):
            eng = "calc_apps"
        elif tid == "calc_def_int_mean_value_theorem":
            eng = "def_int_mvt"
        elif tid == "calc_def_int_area_under_a_curve_by_limit_of_sums":
            eng = "area_under_curve"
        sections.append(
            _calc_sec(tid, title, blurb, engine=eng, ladder_seeds=extra_seeds)
        )
    for tid in sorted(CALC_UNCLEAR):
        title = CALC_UNCLEAR_TITLES.get(tid, f"{tid} (UNCLEAR)")
        sections.append(
            _calc_sec(
                tid,
                title,
                "UNCLEAR gold — red-header live samples of existing generator only. "
                f"See <code>notes/{tid}.md</code>.",
                engine="calculus_foundations",
            )
        )
    for slug, tid, title, blurb, extra in (
        CALC_USUB_PRESET_SHOWCASE + CALC_PARTS_PFD_PRESET_SHOWCASE
    ):
        sections.append(
            _calc_sec(
                tid,
                title,
                blurb,
                engine="integrals",
                slug=slug,
                pattern="",
                extra_settings=extra,
            )
        )
    return sections


SECTIONS.extend(_build_calc_integral_sections())

SKIPPED_NOTE = (
    "Not in this catalog: RRT; "
    "verbal expressions (cubes / binomial products); "
    "direct/inverse variation; graphing rationals; "
    "numeric distributive; G6 GCF/LCM word problems and number-line word problems (WP family). "
    "Former Precalc <code>precalc_foundations</code> stubs are shipped (0 deferred). "
    "LOW_VARIETY trig eqns (<code>pc_simple_trig_equations</code>, "
    "<code>pc_equations_and_multiple_angle_identities</code>) stay red-header / old path. "
    "Calc integrals + named u-sub presets (<code>challenging</code>, reverse-chain, …) "
    "are in this catalog — see <code>notes/CALC_STATUS.md</code> / "
    "<code>notes/CALC_INDEX.md</code>."
)

# Red header tokens in notes/<type_id>.md (word boundary).
_NOTES_FLAG_RE = re.compile(
    r"\b(UNCLEAR|LOW_VARIETY|LIMITATIONS|NOT_IMPLEMENTED)\b"
)


def _notes_candidate_paths(section: dict[str, Any]) -> list[Path]:
    """Prefer notes/<type_id>.md, then slug, aliases, then <slug>/NOTES.md."""
    slug = str(section.get("slug") or "")
    type_id = str(section.get("type_id") or "")
    # type_id first so catalog stubs keyed by type_id win over a mismatched slug.
    names = [type_id, slug]
    names.extend(str(a) for a in (section.get("aliases") or []))
    paths: list[Path] = []
    seen: set[Path] = set()
    for name in names:
        if not name or name.startswith("_"):
            continue
        p = OUT / "notes" / f"{name}.md"
        if p not in seen:
            seen.add(p)
            paths.append(p)
    if slug:
        colocated = OUT / slug / "NOTES.md"
        if colocated not in seen:
            paths.append(colocated)
    return paths


def _load_notes_markdown(section: dict[str, Any]) -> str | None:
    for path in _notes_candidate_paths(section):
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return None


def _notes_flags(md: str) -> list[str]:
    found: list[str] = []
    for m in _NOTES_FLAG_RE.finditer(md):
        flag = m.group(1)
        if flag not in found:
            found.append(flag)
    return found


def _section_by_key() -> dict[str, dict[str, Any]]:
    """Map slug / type_id / alias → SECTIONS entry (first wins)."""
    by_key: dict[str, dict[str, Any]] = {}
    for section in SECTIONS:
        for key in (
            str(section.get("slug") or ""),
            str(section.get("type_id") or ""),
            *(str(a) for a in (section.get("aliases") or [])),
        ):
            if key and key not in by_key:
                by_key[key] = section
    return by_key


def _covered_catalog_ids() -> set[str]:
    covered: set[str] = set()
    for section in SECTIONS:
        covered.add(str(section.get("type_id") or ""))
        covered.add(str(section.get("slug") or ""))
        covered.update(str(a) for a in (section.get("aliases") or []))
    covered.discard("")
    return covered


def _stub_section_for_type(type_id: str) -> dict[str, Any]:
    """Minimal section so any catalog type_id can get a gallery page + notes."""
    title = f"{type_id} (notes stub)"
    engine = "unknown"
    try:
        from question_engine.core.registry import get_catalog_entry

        entry = get_catalog_entry(type_id)
        title = f"{entry.name} (notes stub)"
        engine = str(entry.generator or "unknown")
    except KeyError:
        pass
    return {
        "slug": type_id,
        "title": title,
        "pattern": "",
        "engine": engine,
        "type_id": type_id,
        "aliases": [],
        "ladder_ds": (0.0, 8.0, 16.0),
        "ladder_seeds": (101, 207),
        "blurb": (
            f"Gallery stub for catalog <code>{escape(type_id)}</code> — not on a "
            "wired phase-01 skeleton section. Notes + Limitations still render; "
            "live samples appear when <code>_generate_for_type</code> works."
        ),
        "stub": True,
    }


# A2 thin aliases that belong on an existing SECTIONS type_id (not a new stub).
_A2_ALIAS_ON: dict[str, str] = {
    "a2_beginning_algebra_simplifying_algebraic_expressions": "g6_distributive_property_algebraic",
    "a2_equations_and_inequalities_multi_step_equations": "multi_step_equations",
    "a2_equations_and_inequalities_literal_equations": "literal_equations",
    "a2_equations_and_inequalities_absolute_value_equations": "absolute_value_equations",
    "a2_equations_and_inequalities_multi_step_inequalities": "multi_step_inequalities",
    "a2_equations_and_inequalities_compound_inequalities": "compound_inequalities",
    "a2_equations_and_inequalities_absolute_value_inequalities": "absolute_value_inequalities",
    "a2_relations_and_introduction_to_functions_discrete_relations": "discrete_relations",
    "a2_relations_and_introduction_to_functions_continuous_relations": "continuous_relations",
    "a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions": (
        "evaluating_graphing_functions"
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots": (
        "quadratic_square_roots"
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring": (
        "quadratic_factoring_equations"
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square": (
        "quadratic_completing_square_solve"
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula": (
        "quadratic_formula"
    ),
    "a2_polynomial_functions_solving_polynomial_equations": "quadratic_factoring_equations",
    "a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions": (
        "radical_add_subtract"
    ),
    "a2_radical_functions_and_rational_exponents_multiplying_radical_expressions": (
        "radical_multiply"
    ),
    "a2_radical_functions_and_rational_exponents_dividing_radical_expressions": (
        "radical_divide"
    ),
    "a2_radical_functions_and_rational_exponents_radical_equations": "radical_equations",
    "a2_radical_functions_and_rational_exponents_rational_exponent_equations": (
        "radical_equations"
    ),
}


def _ensure_a2_aliases_on_sections() -> None:
    """Attach missing A2 catalog aliases onto existing gallery sections."""
    by_tid = {
        str(s.get("type_id") or ""): s
        for s in SECTIONS
        if s.get("type_id")
    }
    # Also allow matching by slug when type_id differs (rare).
    by_slug = {str(s.get("slug") or ""): s for s in SECTIONS if s.get("slug")}
    for a2_id, host in _A2_ALIAS_ON.items():
        sec = by_tid.get(host) or by_slug.get(host)
        if not sec:
            continue
        aliases = list(sec.get("aliases") or [])
        if a2_id not in aliases and str(sec.get("type_id")) != a2_id:
            aliases.append(a2_id)
            sec["aliases"] = aliases


def _build_a2_stub_sections() -> list[dict[str, Any]]:
    """Stub gallery pages for Algebra 2 catalog leaves not already in SECTIONS."""
    from question_engine.catalogs.algebra_2 import CATALOG

    _ensure_a2_aliases_on_sections()
    covered = _covered_catalog_ids()
    # After alias attach, recompute covered.
    covered = _covered_catalog_ids()
    out: list[dict[str, Any]] = []
    for entry in CATALOG:
        tid = str(entry.id)
        if tid in covered:
            continue
        sec = _stub_section_for_type(tid)
        low = tid.lower()
        graphish = (
            "graph" in low
            or "end_behavior" in low
            or tid.endswith("_planes")
            or "points_in_three_dimensions" in low
            or "geometric_transformations" in low
        )
        if graphish:
            sec["title"] = f"{entry.name} (UNCLEAR — graph stub)"
            sec["blurb"] = (
                "UNCLEAR / NOT_IMPLEMENTED: graph or spatial display outside "
                "algebraic skeleton cores. Red-header stub — see "
                f"<code>notes/{tid}.md</code> Limitations."
            )
        else:
            sec["title"] = f"A2 — {entry.name} (notes stub)"
            sec["blurb"] = (
                "Algebra 2 gallery stub (not a dedicated phase-01 skeleton row). "
                f"Notes + Limitations in <code>notes/{tid}.md</code>; "
                "live samples when generate works."
            )
        out.append(sec)
    return out


# Fill any remaining A2 catalog gaps (graphing UNCLEAR + leftover leaves).
SECTIONS.extend(_build_a2_stub_sections())


def _build_a1_stub_sections() -> list[dict[str, Any]]:
    """Stub gallery pages for Algebra 1 catalog leaves not already in SECTIONS."""
    from question_engine.catalogs.algebra_1 import CATALOG

    covered = _covered_catalog_ids()
    out: list[dict[str, Any]] = []
    for entry in CATALOG:
        tid = str(entry.id)
        if tid in covered:
            continue
        sec = _stub_section_for_type(tid)
        low = tid.lower()
        graphish = "graph" in low or "scatter" in low or "visualizing" in low
        unclearish = any(
            k in low
            for k in (
                "evaluating_graphing",
                "discrete_relations",
                "continuous_relations",
                "finding_",
                "find_missing",
                "radical_distance",
                "radical_midpoint",
                "exponential_growth",
                "percent",
            )
        )
        if graphish or unclearish:
            sec["title"] = f"A1 — {entry.name} (UNCLEAR / stub)"
            sec["blurb"] = (
                "UNCLEAR / NOT_IMPLEMENTED or notes-limited Algebra 1 leaf. "
                f"Red-header stub — see <code>notes/{tid}.md</code> Limitations. "
                "Live samples when <code>_generate_for_type</code> works."
            )
        else:
            sec["title"] = f"A1 — {entry.name} (notes stub)"
            sec["blurb"] = (
                "Algebra 1 gallery stub (not a dedicated phase-01 skeleton row). "
                f"Notes + Limitations in <code>notes/{tid}.md</code>; "
                "live samples when generate works."
            )
        out.append(sec)
    return out


# Fill remaining A1 catalog gaps (percents, exponents, trig/stats stubs, …).
SECTIONS.extend(_build_a1_stub_sections())


def _alert_banner(flags: list[str]) -> str:
    if not flags:
        return ""
    label = " · ".join(flags)
    if any(f in flags for f in ("LIMITATIONS", "NOT_IMPLEMENTED")):
        detail = "see Limitations in notes below."
    elif any(f in flags for f in ("UNCLEAR", "LOW_VARIETY")):
        detail = "gold look not locked; see notes below."
    else:
        detail = "see notes below."
    return (
        f"<div class='notes-alert'>{escape(label)} — {escape(detail)}</div>"
    )


def _md_inline(text: str) -> str:
    s = escape(text)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def _is_md_table_sep(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells)


def _md_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _notes_body_html(md: str) -> str:
    """Tiny markdown subset for NOTES.md (headings, lists, paragraphs, tables)."""
    parts: list[str] = []
    buf: list[str] = []
    in_list = False
    lines = md.splitlines()
    i = 0

    def flush_p() -> None:
        if buf:
            parts.append("<p>" + " ".join(_md_inline(x) for x in buf) + "</p>")
            buf.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip() or line.strip() == "---":
            if in_list:
                parts.append("</ul>")
                in_list = False
            flush_p()
            i += 1
            continue
        if "|" in line and i + 1 < len(lines) and _is_md_table_sep(lines[i + 1]):
            if in_list:
                parts.append("</ul>")
                in_list = False
            flush_p()
            headers = _md_table_row(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                if _is_md_table_sep(lines[i]):
                    i += 1
                    continue
                rows.append(_md_table_row(lines[i]))
                i += 1
            thead = "".join(f"<th>{_md_inline(h)}</th>" for h in headers)
            body_rows = []
            for row in rows:
                cells = (row + [""] * len(headers))[: len(headers)]
                body_rows.append(
                    "<tr>"
                    + "".join(f"<td>{_md_inline(c)}</td>" for c in cells)
                    + "</tr>"
                )
            parts.append(
                "<table class='notes-table'><thead><tr>"
                + thead
                + "</tr></thead><tbody>"
                + "".join(body_rows)
                + "</tbody></table>"
            )
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        if heading:
            if in_list:
                parts.append("</ul>")
                in_list = False
            flush_p()
            level = len(heading.group(1))
            parts.append(f"<h{level}>{_md_inline(heading.group(2))}</h{level}>")
            i += 1
            continue
        bullet = re.match(r"^[-*]\s+(.*)$", line)
        if bullet:
            flush_p()
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{_md_inline(bullet.group(1))}</li>")
            i += 1
            continue
        if in_list:
            parts.append("</ul>")
            in_list = False
        buf.append(line.strip())
        i += 1
    if in_list:
        parts.append("</ul>")
    flush_p()
    return "\n".join(parts)


def _notes_section_html(
    section: dict[str, Any],
    *,
    generation_ok: int | None = None,
    generation_total: int | None = None,
) -> str:
    """Notes block + red header for flag tokens / failed generate stubs."""
    md = _load_notes_markdown(section)
    flags = _notes_flags(md) if md else []
    # Live generate produced nothing → treat as not implemented for the header.
    if (
        generation_ok is not None
        and generation_total is not None
        and generation_total > 0
        and generation_ok == 0
        and "NOT_IMPLEMENTED" not in flags
    ):
        flags = [*flags, "NOT_IMPLEMENTED"]
    if section.get("stub") and not md and "NOT_IMPLEMENTED" not in flags:
        flags = [*flags, "NOT_IMPLEMENTED"]

    banner = _alert_banner(flags)
    if not md:
        tid = str(section.get("type_id") or section.get("slug") or "type_id")
        return (
            banner
            + "<div class='notes-block'>"
            + "<p>No notes file yet. Copy <code>notes/_TEMPLATE.md</code> to "
            + f"<code>notes/{escape(tid)}.md</code> and fill “should look like”, "
            + "OpenStax cites, and a required <strong>Limitations</strong> section "
            + "(leave <code>LIMITATIONS</code> / <code>NOT_IMPLEMENTED</code> tokens "
            + "when they still apply).</p>"
            + "</div>\n"
        )
    return (
        banner
        + "<div class='notes-block'>"
        + _notes_body_html(md)
        + "</div>\n"
    )


def _fmt_val(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, (list, tuple)):
        if not v:
            return "(none)"
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    return str(v)


def _band_label(d: float) -> str:
    if d <= 4:
        return "low"
    if d <= 12:
        return "mid"
    return "high"


def _debug_rows(meta: dict[str, Any], gen: dict[str, Any]) -> list[tuple[str, Any]]:
    seed = gen.get("seed", meta.get("seed"))
    d = meta.get("effective_d", gen.get("difficulty"))
    k = meta.get("cancel_factor_count", meta.get("cancel_count"))
    rows: list[tuple[str, Any]] = [
        ("skeleton_pattern", meta.get("skeleton_pattern")),
        ("primitive_engine", meta.get("primitive_engine")),
        ("D / effective_d", d),
        ("seed", seed),
        ("form_id", meta.get("form_id")),
        ("openstax_form", meta.get("openstax_form")),
        ("tricks_required", meta.get("tricks_required")),
        ("u_sub_form_preset", meta.get("u_sub_form_preset")),
        ("parts_form_preset", meta.get("parts_form_preset")),
        ("pfd_form_preset", meta.get("pfd_form_preset")),
        ("trig_sub_form_preset", meta.get("trig_sub_form_preset")),
        ("k / cancel_factor_count", k),
        ("dens_style", meta.get("dens_style")),
        ("excluded_values", meta.get("excluded_values")),
        ("task", meta.get("task")),
        ("factor_kind", meta.get("factor_kind")),
        ("factor_bias", meta.get("factor_bias")),
        ("method", meta.get("method")),
        ("operation", meta.get("operation")),
        ("goal_mode", meta.get("goal_mode")),
        ("package_mode", meta.get("package_mode")),
        ("display_intent", meta.get("display_intent")),
        ("mixer_pick", meta.get("mixer_pick")),
        ("n_factors", meta.get("n_factors")),
        ("degree", meta.get("degree")),
        ("steps", meta.get("steps")),
        ("n_ops", meta.get("n_ops")),
        ("species", meta.get("species")),
        ("transforms", meta.get("transforms")),
        ("numeric_tier", meta.get("numeric_tier")),
        ("format_tier", meta.get("format_tier")),
        ("inner_a", meta.get("inner_a")),
        ("inner_b", meta.get("inner_b")),
        ("flipped", meta.get("flipped")),
        ("relation", meta.get("relation")),
        ("frame_id", meta.get("frame_id")),
        ("frame_variant", meta.get("frame_variant")),
        ("vehicle", meta.get("vehicle")),
        ("ask", meta.get("ask")),
        ("mode", meta.get("mode")),
        ("candidate", meta.get("candidate")),
        ("is_solution", meta.get("is_solution")),
        ("subst", meta.get("subst")),
        ("wp_kind", meta.get("wp_kind")),
        ("target_var", meta.get("target_var")),
        ("literal_shape", meta.get("literal_shape")),
        ("form", meta.get("form")),
        ("construction", meta.get("construction")),
        ("axis", meta.get("axis")),
        ("shape_kind", meta.get("shape_kind")),
        ("layout", meta.get("layout")),
        ("nl_blank_prompt", (meta.get("number_line_spec") or {}).get("blank")),
        ("nl_direction", (meta.get("answer_number_line_spec") or {}).get("direction")),
        ("nl_boundary", (meta.get("answer_number_line_spec") or {}).get("boundary")),
        ("nl_boundary_high", (meta.get("answer_number_line_spec") or {}).get("boundary_high")),
        ("diagram_kind", (meta.get("diagram_spec") or {}).get("kind")),
        ("stimulus_kind", meta.get("stimulus_kind") or (meta.get("stimulus") or {}).get("kind")),
        ("has_diagram_svg", bool(meta.get("diagram_svg"))),
    ]
    return [(k, v) for k, v in rows if v is not None and v != ""]


def _sample_cell(
    section: dict[str, Any],
    d: float,
    seed: int,
) -> dict[str, Any]:
    type_id = str(section["type_id"])
    label = f"D≈{d:g} · seed={seed}"
    settings: dict[str, Any] = {
        "difficulty": d,
        "seed": seed,
        "count": 1,
        "include_answer_key": True,
        "integers_only": True,
        "only_x": True,
    }
    extra = section.get("extra_settings")
    if isinstance(extra, dict):
        settings.update(extra)
    try:
        qs = _generate_for_type(type_id, settings)
        if not qs:
            raise RuntimeError("empty question list")
        q = qs[0]
        meta = dict(q.metadata or {})
        gen = dict(meta.get("generation_settings") or {})
        pat = str(meta.get("skeleton_pattern") or "")
        expected = str(section.get("pattern") or "")
        warn = bool(expected) and pat != expected
        if section.get("pattern_soft") and expected and pat:
            # Diff form labels rotate (roots / nested / trig×trig, …).
            warn = expected not in pat and pat not in expected
        if expected == "FactorProduct" and pat != "FactorProduct":
            warn = True
        return {
            "ok": True,
            "warn": warn,
            "label": label,
            "type_id": type_id,
            "difficulty": d,
            "band": _band_label(d),
            "seed": gen.get("seed", seed),
            "prompt_latex": q.prompt_latex,
            "answer_latex": q.answer_latex or "",
            "skeleton_pattern": pat,
            "form_id": meta.get("form_id"),
            "diagram_svg": meta.get("diagram_svg") or "",
            "debug": _debug_rows(meta, gen),
            "metadata": meta,
        }
    except Exception as exc:  # noqa: BLE001 — gallery records failures
        return {
            "ok": False,
            "label": label,
            "type_id": type_id,
            "difficulty": d,
            "band": _band_label(d),
            "seed": seed,
            "error": f"{type(exc).__name__}: {exc}",
        }


def _debug_panel(row: dict[str, Any]) -> str:
    if not row.get("ok"):
        return ""
    items = "".join(
        f"<div class='kv'><span class='k'>{escape(str(k))}</span>"
        f"<span class='v'>{escape(_fmt_val(v))}</span></div>"
        for k, v in row.get("debug") or []
    )
    return f"<div class='debug'>{items}</div>"


def _cards_html(rows: list[dict[str, Any]], *, section: dict[str, Any]) -> str:
    parts: list[str] = []
    for i, row in enumerate(rows, 1):
        if not row.get("ok"):
            parts.append(
                f"<article class='card fail'>"
                f"<header><span class='n'>#{i}</span> "
                f"<strong>{escape(row.get('label', ''))}</strong></header>"
                f"<p class='err'>{escape(row.get('error', ''))}</p>"
                f"<p class='meta'><code>{escape(row.get('type_id', ''))}</code></p>"
                f"</article>"
            )
            continue
        cls = "card warn" if row.get("warn") else "card"
        tags = [
            f"<span class='tag band {escape(str(row.get('band', '')))}'>D≈{escape(str(row.get('difficulty', '')))}</span>",
            f"<span class='tag'>seed={escape(str(row.get('seed', '')))}</span>",
        ]
        if row.get("form_id"):
            tags.append(f"<span class='tag fid'>{escape(str(row['form_id']))}</span>")
        if row.get("warn"):
            tags.append("<span class='tag warn-tag'>pattern mismatch</span>")
        fig = ""
        svg = str(row.get("diagram_svg") or "").strip()
        if svg.startswith("<svg"):
            fig = f"<div class='fig'>{svg}</div>"
        parts.append(
            f"<article class='{cls}'>"
            f"<header><span class='n'>#{i}</span> "
            f"<strong>{escape(row.get('label', ''))}</strong> "
            f"<span class='pat'>{escape(str(row.get('skeleton_pattern', section.get('pattern', ''))))}</span> "
            f"{''.join(tags)}</header>"
            f"<div class='math'><div class='lab'>Prompt</div>$${row['prompt_latex']}$$</div>"
            f"{fig}"
            f"<div class='math'><div class='lab'>Answer</div>$${row.get('answer_latex', '')}$$</div>"
            f"{_debug_panel(row)}"
            f"<p class='meta'>type: <code>{escape(row.get('type_id', ''))}</code></p>"
            f"</article>"
        )
    return "\n".join(parts)


def _katex_head(title: str, katex_rel: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>{escape(title)}</title>
<style>
body {{ font-family: Georgia, "Iowan Old Style", serif; margin: 1.25rem 1.75rem;
  background: #f7f5f0; color: #1a1a1a; }}
h1 {{ font-size: 1.35rem; margin-bottom: 0.35rem; }}
h2 {{ font-size: 1.05rem; margin-top: 1.25rem; }}
.sub {{ color: #555; font-size: 0.9rem; margin-bottom: 1rem; max-width: 52rem; }}
.nav a {{ margin-right: 0.85rem; }}
.card {{ background: #fff; border: 1px solid #d8d2c4; padding: 0.75rem 1rem;
  margin-bottom: 0.75rem; max-width: 54rem; }}
.card.fail {{ border-color: #c44; }}
.card.warn {{ border-color: #c80; }}
header {{ display: flex; flex-wrap: wrap; gap: 0.45rem; align-items: baseline;
  font-size: 0.88rem; margin-bottom: 0.45rem; }}
.n {{ color: #666; }}
.pat {{ color: #3a5a40; font-family: ui-monospace, Consolas, monospace; font-size: 0.82rem; }}
.tag {{ background: #efebe3; padding: 0.1rem 0.4rem; font-size: 0.78rem; }}
.tag.fid {{ background: #e6ebe8; }}
.tag.warn-tag {{ background: #f5e6d3; }}
.tag.band.low {{ background: #e8efe6; }}
.tag.band.mid {{ background: #dde8f0; }}
.tag.band.high {{ background: #e8dde8; }}
.math {{ margin: 0.4rem 0; }}
.lab {{ font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.04em; }}
.debug {{ margin-top: 0.55rem; padding-top: 0.45rem; border-top: 1px dashed #d8d2c4;
  font-size: 0.82rem; }}
.kv {{ display: grid; grid-template-columns: 11rem 1fr; gap: 0.25rem 0.75rem; margin: 0.15rem 0; }}
.k {{ color: #666; }}
.v {{ word-break: break-word; font-family: ui-monospace, Consolas, monospace; font-size: 0.78rem; }}
.meta {{ font-size: 0.78rem; color: #555; margin-top: 0.35rem; }}
.fig {{ margin: 0.45rem 0; overflow-x: auto; }}
.fig svg {{ max-width: 100%; height: auto; border: 1px solid #eee; background: #fff; }}
code {{ font-family: ui-monospace, Consolas, monospace; font-size: 0.85em; }}
ul.topics {{ line-height: 1.75; }}
.note {{ font-size: 0.88rem; color: #555; max-width: 52rem; margin-top: 1.25rem;
  padding: 0.65rem 0.85rem; background: #f0ebe3; border: 1px solid #d8d2c4; }}
.notes-alert {{ background: #c62828; color: #fff; padding: 0.7rem 0.95rem;
  font-weight: 700; margin: 0.85rem 0 1rem; max-width: 54rem; }}
.notes-block {{ background: #fff; border: 1px solid #d8d2c4; padding: 0.75rem 1rem;
  margin-bottom: 1rem; max-width: 54rem; font-size: 0.92rem; }}
.notes-block h1 {{ font-size: 1.1rem; margin: 0 0 0.35rem; }}
.notes-block h2 {{ font-size: 1rem; margin: 0.85rem 0 0.35rem; }}
.notes-block h2:first-child {{ margin-top: 0; }}
.notes-block ul {{ margin: 0.35rem 0 0.5rem 1.2rem; }}
.notes-block p {{ margin: 0.35rem 0; }}
.notes-table {{ border-collapse: collapse; width: 100%; margin: 0.5rem 0 0.75rem;
  font-size: 0.82rem; }}
.notes-table th, .notes-table td {{ border: 1px solid #d8d2c4; padding: 0.3rem 0.45rem;
  text-align: left; vertical-align: top; }}
.notes-table th {{ background: #f3efe7; }}
.fig {{ max-width: 36rem; margin: 0.45rem 0; overflow-x: auto; }}
.fig svg {{ max-width: 100%; height: auto; }}
</style>
<link rel="stylesheet" href="{katex_rel}/katex.min.css"/>
<script defer src="{katex_rel}/katex.min.js"></script>
<script defer src="{katex_rel}/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false}});"></script>
</head><body>
"""


def _build_section(section: dict[str, Any]) -> dict[str, Any]:
    slug = str(section["slug"])
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    ds = tuple(section.get("ladder_ds") or LADDER_DS)
    seeds = tuple(section.get("ladder_seeds") or LADDER_SEEDS)
    for d in ds:
        for seed in seeds:
            row = _sample_cell(section, d, seed)
            rows.append(row)
            if not row.get("ok"):
                failures.append(
                    {"d": d, "seed": seed, "error": row.get("error")}
                )

    section_dir = OUT / slug
    section_dir.mkdir(parents=True, exist_ok=True)
    (section_dir / "samples.json").write_text(
        json.dumps(
            {"section": section, "rows": rows, "failures": failures},
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    aliases = section.get("aliases") or []
    alias_txt = ""
    if aliases:
        alias_txt = (
            "<p class='sub'>Also wired: "
            + ", ".join(f"<code>{escape(a)}</code>" for a in aliases)
            + "</p>"
        )
    ok_n = sum(1 for r in rows if r.get("ok"))
    warn_n = sum(1 for r in rows if r.get("warn"))
    stub_note = ""
    if ok_n == 0:
        stub_note = (
            "<p class='note'><strong>Stub / not wired:</strong> live generate "
            "produced 0 samples. Notes and Limitations still shown above. "
            "Leave <code>NOT_IMPLEMENTED</code> / <code>LIMITATIONS</code> in "
            "notes when the engine is deferred.</p>\n"
        )
    elif section.get("stub") and ok_n < len(rows):
        stub_note = (
            f"<p class='note'><strong>Partial stub:</strong> {ok_n}/{len(rows)} "
            "live samples; failures recorded in <code>samples.json</code>.</p>\n"
        )

    pattern = str(section.get("pattern") or "")
    pattern_txt = (
        f" · pattern <strong>{escape(pattern)}</strong>" if pattern else " · pattern <em>(none / stub)</em>"
    )

    html = (
        _katex_head(f"{section['title']} — skeleton gallery", KATEX)
        + f"""<p class="nav"><a href="../index.html">← all types</a></p>
<h1>{escape(str(section['title']))}</h1>
<p class="sub"><code>{escape(str(section['type_id']))}</code> · live <code>_generate_for_type</code>
{pattern_txt}
 · {ok_n}/{len(rows)} ok"""
        + (f" · {warn_n} pattern warnings" if warn_n else "")
        + f""" · D ladder {', '.join(str(int(x)) if x == int(x) else str(x) for x in (section.get('ladder_ds') or LADDER_DS))}
 · seeds {', '.join(str(s) for s in (section.get('ladder_seeds') or LADDER_SEEDS))}</p>
<p class="sub">{section.get('blurb', '')}</p>
{alias_txt}
{_notes_section_html(section, generation_ok=ok_n, generation_total=len(rows))}
{stub_note}
{_cards_html(rows, section=section)}
</body></html>
"""
    )
    (section_dir / "gallery.html").write_text(html, encoding="utf-8")

    return {
        "slug": slug,
        "title": section["title"],
        "pattern": section.get("pattern") or "",
        "type_id": section["type_id"],
        "aliases": aliases,
        "stub": bool(section.get("stub")),
        "ok": ok_n,
        "total": len(rows),
        "warn": warn_n,
        "failures": failures,
    }


def _resolve_sections(
    *,
    only: set[str],
    type_ids: set[str],
    ensure_stubs: bool,
) -> list[dict[str, Any]]:
    """Pick SECTIONS rows and/or catalog stubs. Never drops existing SECTIONS defs."""
    by_key = _section_by_key()
    out: list[dict[str, Any]] = []
    seen_slugs: set[str] = set()

    def add(section: dict[str, Any]) -> None:
        slug = str(section["slug"])
        if slug in seen_slugs:
            return
        seen_slugs.add(slug)
        out.append(section)

    if ensure_stubs:
        from question_engine.core.registry import TYPE_CATALOG

        covered = _covered_catalog_ids()
        for entry in TYPE_CATALOG:
            tid = str(entry.id)
            if tid in covered:
                continue
            add(_stub_section_for_type(tid))
        return out

    keys = only | type_ids
    if keys:
        for key in sorted(keys):
            if key in by_key:
                add(by_key[key])
            else:
                # Unknown slug/type_id → catalog stub page (notes + limitations).
                add(_stub_section_for_type(key))
        if not out:
            raise SystemExit(f"no matching slugs/type_ids in {sorted(keys)}")
        return out

    return list(SECTIONS)


def _summary_from_disk(section: dict[str, Any]) -> dict[str, Any]:
    """Build an index summary from an existing samples.json (no live generate)."""
    slug = str(section["slug"])
    path = OUT / slug / "samples.json"
    ok_n = 0
    total = 0
    warn_n = 0
    failures: list[str] = []
    if path.is_file():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            rows = list(payload.get("rows") or payload.get("samples") or [])
            if not rows and isinstance(payload.get("ok"), int):
                ok_n = int(payload["ok"])
                total = int(payload.get("total") or ok_n)
            else:
                total = len(rows)
                for row in rows:
                    if row.get("ok"):
                        ok_n += 1
                        if row.get("warn"):
                            warn_n += 1
                    else:
                        failures.append(str(row.get("error") or "fail"))
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            pass
    aliases = [str(a) for a in (section.get("aliases") or []) if a]
    return {
        "slug": slug,
        "title": section["title"],
        "pattern": section.get("pattern") or "",
        "type_id": section["type_id"],
        "aliases": aliases,
        "stub": bool(section.get("stub")),
        "ok": ok_n,
        "total": total,
        "warn": warn_n,
        "failures": failures,
    }


def _write_catalog_index(summaries: list[dict[str, Any]]) -> None:
    index_items = []
    for s in summaries:
        fail_note = ""
        if s["failures"]:
            fail_note = f" · <em>{len(s['failures'])} failed</em>"
        stub_mark = " · <em>stub</em>" if s.get("stub") else ""
        index_items.append(
            f"<li><a href=\"{escape(s['slug'])}/gallery.html\"><strong>{escape(s['title'])}</strong></a>"
            f" · <code>{escape(s['pattern'])}</code>"
            f" · <code>{escape(s['type_id'])}</code>"
            f" · {s['ok']}/{s['total']} ok{fail_note}{stub_mark}</li>"
        )

    index_html = (
        _katex_head("Phase 0–2 skeleton catalog", KATEX_INDEX)
        + f"""<h1>Phase 0–2 skeleton question catalog</h1>
<p class="sub">Rational skeleton (<code>rational_skeleton</code>) + poly skeleton
 (<code>poly_skeleton</code> / FactorProduct) + equation skeleton
 (<code>equation_skeleton</code> / SolveLinear, SolveInequality, SolveLiteral)
 + trig rewrite skeleton (<code>trig_skeleton</code> / TrigRewrite)
 + Precalc reuse engines ({len(_build_pc_sections())} PC leaves; {len(PC_DEFERRED)} deferred)
 + Calculus integrals / apps + named u-sub presets
 + G6 <code>number</code> frameworks. Live generation via
 <code>_generate_for_type</code> · KaTeX · D≈2/8/16 × 2 seeds per skill
 (equations / inequalities / literals: D≈0/8/16 × 3 seeds).
 Catalog types missing from this list can still get a notes stub page via
 <code>--type-id &lt;id&gt;</code> or <code>--ensure-stubs</code>.</p>
<ul class="topics">
{''.join(index_items)}
</ul>
<p class="note"><strong>Skipped:</strong> {SKIPPED_NOTE}</p>
<p class="sub">Regenerate:
<code>python scripts/output/skeleton_phase01_gallery/gen_examples.py</code>
 · stub one type:
<code>python scripts/output/skeleton_phase01_gallery/gen_examples.py --type-id verbal_expressions</code>
 · all missing catalog stubs:
<code>python scripts/output/skeleton_phase01_gallery/gen_examples.py --ensure-stubs</code>
 · refresh index only:
<code>python scripts/output/skeleton_phase01_gallery/gen_examples.py --refresh-index</code></p>
</body></html>
"""
    )
    (OUT / "index.html").write_text(index_html, encoding="utf-8")
    (OUT / "samples.json").write_text(
        json.dumps({"sections": summaries}, indent=2, default=str),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Phase-01 gallery: live samples + notes. Any catalog type_id can get "
            "a stub section page (notes + LIMITATIONS / NOT_IMPLEMENTED header)."
        )
    )
    parser.add_argument(
        "--only",
        default="",
        help="Comma-separated section slugs and/or type_ids (default: all SECTIONS)",
    )
    parser.add_argument(
        "--type-id",
        default="",
        help=(
            "Comma-separated catalog type_ids. Creates a stub gallery page when "
            "the id is not already in SECTIONS (does not rewrite other sections)."
        ),
    )
    parser.add_argument(
        "--ensure-stubs",
        action="store_true",
        help=(
            "Write gallery stubs for every catalog type_id not covered by SECTIONS. "
            "Does not regenerate existing SECTIONS pages or wipe them."
        ),
    )
    parser.add_argument(
        "--refresh-index",
        action="store_true",
        help=(
            "Rewrite index.html from SECTIONS + on-disk samples.json counts "
            "(no live generate). Can combine with --only after a partial regen."
        ),
    )
    args = parser.parse_args()
    only = {s.strip() for s in str(args.only).split(",") if s.strip()}
    type_ids = {s.strip() for s in str(args.type_id).split(",") if s.strip()}

    OUT.mkdir(parents=True, exist_ok=True)

    if args.refresh_index and not only and not type_ids and not args.ensure_stubs:
        summaries = [_summary_from_disk(s) for s in SECTIONS]
        _write_catalog_index(summaries)
        print(f"refreshed index ({len(summaries)} SECTIONS) -> {OUT / 'index.html'}")
        return

    sections = _resolve_sections(
        only=only, type_ids=type_ids, ensure_stubs=bool(args.ensure_stubs)
    )

    summaries = [_build_section(s) for s in sections]

    # --only / --type-id / --ensure-stubs: do not rewrite the full catalog index
    # unless --refresh-index is also set.
    if only or type_ids or args.ensure_stubs:
        print("sections:")
        for s in summaries:
            status = f"{s['ok']}/{s['total']} ok"
            if s.get("stub"):
                status = "stub · " + status
            if s["failures"]:
                status += f" FAIL={len(s['failures'])}"
            if s["warn"]:
                status += f" warn={s['warn']}"
            print(f"  {s['slug']}: {status}")
        if args.ensure_stubs:
            print(f"wrote {len(summaries)} catalog stub page(s) under {OUT}")
        if args.refresh_index:
            by_slug = {str(s["slug"]): s for s in summaries}
            full = []
            for sec in SECTIONS:
                slug = str(sec["slug"])
                if slug in by_slug:
                    full.append(by_slug[slug])
                else:
                    full.append(_summary_from_disk(sec))
            _write_catalog_index(full)
            print(f"index -> {OUT / 'index.html'} ({len(full)} SECTIONS)")
        return

    _write_catalog_index(summaries)

    print("sections:")
    for s in summaries:
        status = f"{s['ok']}/{s['total']} ok"
        if s["failures"]:
            status += f" FAIL={len(s['failures'])}"
        if s["warn"]:
            status += f" warn={s['warn']}"
        print(f"  {s['slug']}: {status}")
    print(f"index -> {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
