"""Calculus steps 1–3 (non-limits / non-differentiation leaves).

Owns apps of differentiation, indefinite/definite integration, apps of
integration, and differential equations. Limits + Differentiation chapters
(and ``calc_app_diff_limits_in_form_of_definition_of_derivative``) belong to
the derivatives/limits agent.

Writes ``notes/<type_id>.md`` + ``CALC_INDEX.md``. No generator wiring.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

os.environ["QE_LOG_GENERATED"] = "0"

_ROOT = Path(__file__).resolve().parents[4]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from question_engine.api.handler import _generate_for_type
from question_engine.catalogs.calculus import CATALOG
from question_engine.frameworks.primitives.wp_packaging import looks_like_dumped_equation

OUT = Path(__file__).resolve().parent
MINE_V1 = _ROOT / "scripts/output/example_mining/calculus-volume-1/stage1"
MINE_V2 = _ROOT / "scripts/output/example_mining/calculus-volume-2/stage1"

DS = (0.0, 8.0, 16.0, 22.0)
SEEDS = (101, 207)

V1 = "https://openstax.org/books/calculus-volume-1/pages"
V2 = "https://openstax.org/books/calculus-volume-2/pages"

DUMP_MARKERS = (
    "the equation is",
    "giving $",
    "satisfy $",
    "reduces to $",
    "uses a proportion",
    "the system is",
)

# Limits + Differentiation (not DE) + definition-of-derivative limit form.
SKIP_IDS = {
    "calc_app_diff_limits_in_form_of_definition_of_derivative",
}


def _in_scope(entry) -> bool:
    tid = entry.id
    if tid in SKIP_IDS:
        return False
    if tid.startswith("calc_limits_") or tid.startswith("calc_continuity_"):
        return False
    if tid.startswith("calc_diff_") and not tid.startswith("calc_diff_eq_"):
        return False
    return True


# Per-type OpenStax cites: (book_tag, section_title, slug, mine_json_or_none, shape)
# book_tag: "v1" | "v2"
TYPE_CITES: dict[str, list[tuple[str, str, str, str | None, str]]] = {
    "calc_app_diff_slope_tangent_and_normal_lines": [
        ("v1", "3.1 Defining the Derivative", "3-1-defining-the-derivative", "3-1-defining-the-derivative.json", "tangent line from f'(a)"),
        ("v1", "4.2 Linear Approximations and Differentials", "4-2-linear-approximations-and-differentials", "4-2-linear-approximations-and-differentials.json", "linearization / tangent approx"),
    ],
    "calc_app_diff_rolles_theorem": [
        ("v1", "4.4 The Mean Value Theorem", "4-4-the-mean-value-theorem", "4-4-the-mean-value-theorem.json", "Rolle: f(a)=f(b) ⇒ f'(c)=0"),
    ],
    "calc_app_diff_mean_value_theorem": [
        ("v1", "4.4 The Mean Value Theorem", "4-4-the-mean-value-theorem", "4-4-the-mean-value-theorem.json", "find c with f'(c)=(f(b)-f(a))/(b-a)"),
    ],
    "calc_app_diff_intervals_of_increase_and_decrease": [
        ("v1", "4.5 Derivatives and the Shape of a Graph", "4-5-derivatives-and-the-shape-of-a-graph", "4-5-derivatives-and-the-shape-of-a-graph.json", "sign chart of f'"),
    ],
    "calc_app_diff_intervals_of_concavity": [
        ("v1", "4.5 Derivatives and the Shape of a Graph", "4-5-derivatives-and-the-shape-of-a-graph", "4-5-derivatives-and-the-shape-of-a-graph.json", "sign chart of f'' / inflection"),
    ],
    "calc_app_diff_relative_extrema": [
        ("v1", "4.3 Maxima and Minima", "4-3-maxima-and-minima", "4-3-maxima-and-minima.json", "critical points; relative max/min"),
        ("v1", "4.5 Derivatives and the Shape of a Graph", "4-5-derivatives-and-the-shape-of-a-graph", "4-5-derivatives-and-the-shape-of-a-graph.json", "first/second derivative tests"),
    ],
    "calc_app_diff_absolute_extrema": [
        ("v1", "4.3 Maxima and Minima", "4-3-maxima-and-minima", "4-3-maxima-and-minima.json", "closed-interval method"),
    ],
    "calc_app_diff_optimization": [
        ("v1", "4.7 Applied Optimization Problems", "4-7-applied-optimization-problems", "4-7-applied-optimization-problems.json", "several story frames (box, fence, can, …)"),
    ],
    "calc_app_diff_curve_sketching": [
        ("v1", "4.5 Derivatives and the Shape of a Graph", "4-5-derivatives-and-the-shape-of-a-graph", "4-5-derivatives-and-the-shape-of-a-graph.json", "combine intercepts, extrema, concavity, asymptotes"),
        ("v1", "4.6 Limits at Infinity and Asymptotes", "4-6-limits-at-infinity-and-asymptotes", "4-6-limits-at-infinity-and-asymptotes.json", "end behavior / HA-VA for sketch"),
    ],
    "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime": [
        ("v1", "4.5 Derivatives and the Shape of a Graph", "4-5-derivatives-and-the-shape-of-a-graph", "4-5-derivatives-and-the-shape-of-a-graph.json", "match graphs of f / f' / f''"),
    ],
    "calc_app_diff_motion_along_a_line": [
        ("v1", "3.4 Derivatives as Rates of Change", "3-4-derivatives-as-rates-of-change", "3-4-derivatives-as-rates-of-change.json", "s(t) → v(t), a(t); when particle stops"),
    ],
    "calc_app_diff_related_rates": [
        ("v1", "4.1 Related Rates", "4-1-related-rates", "4-1-related-rates.json", "several frames (ladder, cone, shadow, expanding circle, …)"),
    ],
    "calc_app_diff_differentials": [
        ("v1", "4.2 Linear Approximations and Differentials", "4-2-linear-approximations-and-differentials", "4-2-linear-approximations-and-differentials.json", "dy = f'(x) dx; estimate Δy"),
    ],
    "calc_app_diff_linear_approximations": [
        ("v1", "4.2 Linear Approximations and Differentials", "4-2-linear-approximations-and-differentials", "4-2-linear-approximations-and-differentials.json", "L(x)=f(a)+f'(a)(x-a)"),
    ],
    "calc_app_diff_newtons_method": [
        ("v1", "4.9 Newton's Method", "4-9-newtons-method", "4-9-newtons-method.json", "one or more Newton iterates"),
    ],
    "calc_app_diff_lhopitals_rule": [
        ("v1", "4.8 L'Hôpital's Rule", "4-8-lhopitals-rule", "4-8-lhopitals-rule.json", "0/0 or ∞/∞ indeterminate forms"),
    ],
    "calc_indef_int_power_rule": [
        ("v1", "4.10 Antiderivatives", "4-10-antiderivatives", "4-10-antiderivatives.json", "∫ x^n dx power rule + C"),
        ("v1", "5.4 Integration Formulas and the Net Change Theorem", "5-4-integration-formulas-and-the-net-change-theorem", "5-4-integration-formulas-and-the-net-change-theorem.json", "basic antiderivative formulas"),
    ],
    "calc_indef_int_logarithmic_rule_and_exponentials": [
        ("v1", "5.6 Integrals Involving Exponential and Logarithmic Functions", "5-6-integrals-involving-exponential-and-logarithmic-functions", "5-6-integrals-involving-exponential-and-logarithmic-functions.json", "∫ e^{kx}, ∫ 1/x"),
    ],
    "calc_indef_int_trigonometric": [
        ("v1", "5.4 Integration Formulas and the Net Change Theorem", "5-4-integration-formulas-and-the-net-change-theorem", "5-4-integration-formulas-and-the-net-change-theorem.json", "basic trig antiderivatives"),
        ("v2", "3.2 Trigonometric Integrals", "3-2-trigonometric-integrals", "3-2-trigonometric-integrals.json", "powers of sin/cos (Calc 2)"),
    ],
    "calc_indef_int_inverse_trigonometric": [
        ("v1", "5.7 Integrals Resulting in Inverse Trigonometric Functions", "5-7-integrals-resulting-in-inverse-trigonometric-functions", "5-7-integrals-resulting-in-inverse-trigonometric-functions.json", "∫ 1/√(a²−x²) etc."),
    ],
    "calc_indef_int_power_rule_with_substitution": [
        ("v1", "5.5 Substitution", "5-5-substitution", "5-5-substitution.json", "u-sub on power compositions"),
    ],
    "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution": [
        ("v1", "5.5 Substitution", "5-5-substitution", "5-5-substitution.json", "u-sub into ln/exp forms"),
        ("v1", "5.6 Integrals Involving Exponential and Logarithmic Functions", "5-6-integrals-involving-exponential-and-logarithmic-functions", "5-6-integrals-involving-exponential-and-logarithmic-functions.json", "ln/exp after sub"),
    ],
    "calc_indef_int_trigonometric_with_substitution": [
        ("v2", "3.3 Trigonometric Substitution", "3-3-trigonometric-substitution", "3-3-trigonometric-substitution.json", "√(a²±x²) trig sub"),
    ],
    "calc_indef_int_inverse_trigonometric_with_substitution": [
        ("v1", "5.5 Substitution", "5-5-substitution", "5-5-substitution.json", "u-sub into invtrig forms"),
        ("v1", "5.7 Integrals Resulting in Inverse Trigonometric Functions", "5-7-integrals-resulting-in-inverse-trigonometric-functions", "5-7-integrals-resulting-in-inverse-trigonometric-functions.json", "invtrig antiderivative after sub"),
    ],
    "calc_indef_int_integration_by_parts": [
        ("v2", "3.1 Integration by Parts", "3-1-integration-by-parts", None, "∫ u dv = uv − ∫ v du; LIATE"),
    ],
    "calc_indef_int_partial_fractions": [
        ("v2", "3.4 Partial Fractions", "3-4-partial-fractions", None, "PFD then integrate termwise"),
    ],
    "calc_indef_int_multi_trick": [
        ("v1", "5.5 Substitution", "5-5-substitution", "5-5-substitution.json", "u-sub then PFD / parts mix"),
        ("v2", "3.4 Partial Fractions", "3-4-partial-fractions", None, "multi-technique pipelines"),
    ],
    "calc_def_int_approximating_area_under_a_curve": [
        ("v1", "5.1 Approximating Areas", "5-1-approximating-areas", "5-1-approximating-areas.json", "L/R/mid Riemann sums"),
    ],
    "calc_def_int_area_under_a_curve_by_limit_of_sums": [
        ("v1", "5.2 The Definite Integral", "5-2-the-definite-integral", "5-2-the-definite-integral.json", "limit of Riemann sums → exact area"),
    ],
    "calc_def_int_riemann_sum_tables": [
        ("v1", "5.1 Approximating Areas", "5-1-approximating-areas", "5-1-approximating-areas.json", "table values → Riemann sum"),
    ],
    "calc_def_int_first_fundamental_theorem_of_calculus": [
        ("v1", "5.3 The Fundamental Theorem of Calculus", "5-3-the-fundamental-theorem-of-calculus", "5-3-the-fundamental-theorem-of-calculus.json", "d/dx ∫_a^{g(x)} f = f(g(x)) g'(x)"),
    ],
    "calc_def_int_substitution_with_change_of_variables": [
        ("v1", "5.5 Substitution", "5-5-substitution", "5-5-substitution.json", "definite u-sub; change limits"),
    ],
    "calc_def_int_mean_value_theorem": [
        ("v1", "5.2 The Definite Integral", "5-2-the-definite-integral", "5-2-the-definite-integral.json", "mean value for integrals / average value"),
    ],
    "calc_def_int_second_fundamental_theorem_of_calculus": [
        ("v1", "5.3 The Fundamental Theorem of Calculus", "5-3-the-fundamental-theorem-of-calculus", "5-3-the-fundamental-theorem-of-calculus.json", "∫_a^b f = F(b)−F(a)"),
    ],
    "calc_app_int_area_under_a_curve": [
        ("v1", "5.2 The Definite Integral", "5-2-the-definite-integral", "5-2-the-definite-integral.json", "area as definite integral"),
        ("v1", "6.1 Areas Between Curves", "6-1-areas-between-curves", "6-1-areas-between-curves.json", "area under one curve as special case"),
    ],
    "calc_app_int_area_between_curves": [
        ("v1", "6.1 Areas Between Curves", "6-1-areas-between-curves", "6-1-areas-between-curves.json", "∫ (top−bottom) dx or dy"),
    ],
    "calc_app_int_volume_by_slicing_disks_and_washers": [
        ("v1", "6.2 Determining Volumes by Slicing", "6-2-determining-volumes-by-slicing", "6-2-determining-volumes-by-slicing.json", "disk/washer about axis"),
    ],
    "calc_app_int_volume_by_cylinders": [
        ("v1", "6.3 Volumes of Revolution — Cylindrical Shells", "6-3-volumes-of-revolution-cylindrical-shells", "6-3-volumes-of-revolution-cylindrical-shells.json", "shell method 2π∫ x f(x) dx"),
    ],
    "calc_app_int_volume_of_solids_with_known_cross_sections": [
        ("v1", "6.2 Determining Volumes by Slicing", "6-2-determining-volumes-by-slicing", "6-2-determining-volumes-by-slicing.json", "known cross-section (square/semi/equil)"),
    ],
    "calc_app_int_motion_along_a_line_revisited": [
        ("v1", "5.4 Integration Formulas and the Net Change Theorem", "5-4-integration-formulas-and-the-net-change-theorem", "5-4-integration-formulas-and-the-net-change-theorem.json", "net change / displacement from v(t)"),
    ],
    "calc_diff_eq_slope_fields": [
        ("v2", "4.2 Direction Fields and Numerical Methods", "4-2-direction-fields-and-numerical-methods", None, "evaluate F(x,y) at a lattice point (no sketch)"),
    ],
    "calc_diff_eq_introduction": [
        ("v2", "4.1 Basics of Differential Equations", "4-1-basics-of-differential-equations", None, "verify solution; classify order"),
    ],
    "calc_diff_eq_separable": [
        ("v2", "4.3 Separable Equations", "4-3-separable-equations", None, "separate variables + integrate + C"),
    ],
    "calc_diff_eq_exponential_growth_and_decay": [
        ("v2", "4.2 Direction Fields and Numerical Methods", "4-2-direction-fields-and-numerical-methods", None, "growth/decay IVP frames"),
        ("v1", "6.8 Exponential Growth and Decay", "6-8-exponential-growth-and-decay", None, "y'=ky applications (Vol 1 if present)"),
    ],
}

# Force flags when gold look is known-weak (foundations stub, single frame, etc.).
META: dict[str, dict[str, Any]] = {
    "calc_app_diff_intervals_of_concavity": {
        "flag_why": "Shipped leftover lockout + Ex. 4.19 shifted inflections; LIMITATIONS no quintic second-derivative test.",
        "skill": "Find intervals of concavity / inflection from f or f''.",
        "engine": "calc_app_diff `intervals_concavity` (odd-power ray / odd cubic / shifted cubic).",
    },
    "calc_app_diff_rolles_theorem": {
        "flag_why": "Shipped leftover lockout of even-quad c=0 + Checkpoint 4.14 scaled two-root; LIMITATIONS no hypothesis-verify stem.",
        "skill": "Find c with f'(c)=0 when f(a)=f(b).",
        "engine": "calc_app_diff `rolles_theorem` (even-quad / two-root / scaled two-root / odd cubic).",
    },
    "calc_app_diff_relative_extrema": {
        "flag_why": "Shipped leftover lockout + Ex. 4.17 shifted extrema; LIMITATIONS no fractional-power first-derivative test.",
        "skill": "Locate relative extrema via critical points / derivative tests.",
        "engine": "calc_app_diff `relative_extrema` (parabola vertex / odd cubic / shifted cubic).",
    },
    "calc_app_diff_absolute_extrema": {
        "flag_why": "Shipped leftover lockout + Ex. 4.17 shifted closed-interval; LIMITATIONS no fractional-power EVT.",
        "skill": "Find absolute extrema on a closed interval (crits + endpoints).",
        "engine": "calc_app_diff `absolute_extrema` (parabola / odd cubic / shifted cubic on an interval).",
    },
    "calc_app_diff_optimization": {
        "force_flags": ["UNCLEAR", "LOW_VARIETY"],
        "flag_why": "`calculus_foundations` stub and/or single story frame; OpenStax §4.7 needs several frames.",
        "skill": "Set up and solve applied optimization (constraint + objective).",
        "engine": "WP packaging over a max/min core + several OpenStax frames (box/fence/can/…).",
    },
    "calc_app_diff_curve_sketching": {
        "flag_why": "Shipped leftover lockout + shifted inflections; LIMITATIONS no SVG / asymptotes.",
        "skill": "List vertex / extrema / inflection for a sketch (no drawn graph).",
        "engine": "calc_app_diff `curve_sketching` (parabola / odd cubic / shifted cubic).",
    },
    "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "`calculus_foundations` stub — matching f/f'/f'' graphs needs figure bank.",
        "skill": "Match or compare graphs of f, f', and f''.",
        "engine": "Leave leaf until figure bank exists; not Diff skeleton.",
    },
    "calc_def_int_approximating_area_under_a_curve": {
        "flag_why": "Shipped leftover lockout of midpoint f(x)=x n=2; LIMITATIONS three frozen old builders / no sin / 10-x^2 / new figure bank.",
        "skill": "Approximate area under a formula f with a finite left / right / midpoint Riemann sum.",
        "engine": "calc_app_diff `riemann_approximate_area` (linear leftover / affine leftover / quad).",
    },
    "calc_def_int_riemann_sum_tables": {
        "flag_why": "Shipped leftover lockout of 3-point left; LIMITATIONS three frozen old builders / no story tables.",
        "skill": "Approximate a definite integral from tabulated values (left / right / midpoint).",
        "engine": "calc_app_diff `riemann_sum_tables` (left3 leftover / 4-point leftover / midpoint).",
    },
    "calc_def_int_area_under_a_curve_by_limit_of_sums": {
        "force_flags": ["UNCLEAR", "LIMITATIONS", "NOT_IMPLEMENTED"],
        "flag_why": "Skip: live is FTC area-under-curve stem; no existing lim-sum core (finite Riemann / tables are other leaves).",
        "skill": "Evaluate a definite integral from the definition (right-endpoint sum, n→∞).",
        "engine": "Leave leaf; do not invent a lim∑ core; do not rewire onto riemann_approximate_area.",
    },
    "calc_app_int_area_under_a_curve": {
        "flag_why": "Shipped leftover lockout of y=x; LIMITATIONS three frozen monomials on [0,b]. Limit-of-sums sibling skipped (still FTC stem).",
        "skill": "Find the area under y=f(x) from x=0 to x=b via the definite integral.",
        "engine": "calc_app_diff `area_under_curve` (linear leftover / quad leftover / k x^2).",
    },
    "calc_app_int_area_between_curves": {
        "flag_why": "Shipped leftover lockout of exclusive cliffs and of y=k-x vs y=0 at expert; LIMITATIONS five frozen old builders / D=22 always y=x vs y=x^2.",
        "skill": "Find the area between two graphs via ∫(top−bottom) dx.",
        "engine": "calc_app_diff `area_between_curves` (linear-axis leftover / quad leftover / three-line leftover / two-curve).",
    },
    "calc_app_int_volume_by_slicing_disks_and_washers": {
        "flag_why": "Shipped leftover lockout of disk y=x (already in volume_methods); LIMITATIONS three frozen old builders / no Ex. 6.8 sqrt / Ex. 6.10 1/x washer / y-axis.",
        "skill": "Find the volume of a solid of revolution by disks or washers about the x-axis.",
        "engine": "calc_app_diff `volume_disk_washer` (disk-linear leftover / disk-quadratic leftover / washer).",
    },
    "calc_app_int_volume_by_cylinders": {
        "flag_why": "Shipped leftover lockout of exclusive y=x; LIMITATIONS three frozen old builders / no Ex. 6.12 1/x / Ex. 6.13 2x-x^2 / x-axis shells.",
        "skill": "Find the volume of a solid of revolution by cylindrical shells about the y-axis.",
        "engine": "calc_app_diff `volume_shell` (linear leftover / quadratic leftover / y=n-x).",
    },
    "calc_app_int_volume_of_solids_with_known_cross_sections": {
        "flag_why": "Shipped leftover lockout of exclusive squares; LIMITATIONS three frozen old builders / no Ex. 6.6 pyramid / Ex. 68 circular-base squares / Ex. 69 triangular-base semicircles.",
        "skill": "Find the volume of a solid whose cross sections are a given shape (integrate area).",
        "engine": "calc_app_diff `volume_cross_sections` (square leftover / equilateral leftover / semicircle).",
    },
    "calc_app_diff_slope_tangent_and_normal_lines": {
        "flag_why": "Shipped leftover lockout of D=0 poly/trig/exp/ln; LIMITATIONS no implicit/folium / x·5^x normals.",
        "skill": "Find the tangent (and sometimes normal) line to y=f(x) at x=a.",
        "engine": "calc_app_diff `tangent_normal_line` (easy leftover / reciprocal-radical leftover / cubic+nested).",
    },
    "calc_app_diff_motion_along_a_line": {
        "flag_why": "Shipped leftover lockout + Ex. 3.36/3.35 cubics; LIMITATIONS no free-fall / piecewise / trig / s(t) graph.",
        "skill": "From s(t) find velocity / rest / direction and speeding up vs slowing down.",
        "engine": "calc_app_diff `motion_along_a_line` (quadratic leftover / cubic rest / cubic speed-sign).",
    },
    "calc_app_diff_newtons_method": {
        "flag_why": "Shipped leftover lockout of one-quad; LIMITATIONS no Ex. 4.46 cubic / failure cases / two-step quadratic.",
        "skill": "Perform one or more Newton iterations.",
        "engine": "calc_app_diff `newtons_method` (one-quad leftover / one-cubic leftover / two cubic steps).",
    },
    "calc_diff_average_rates_of_change": {
        "flag_why": "Shipped leftover lockout of D=0 x^2; LIMITATIONS seven frozen old builders / no sqrt / trig / story s(t).",
        "skill": "Compute (f(b)-f(a))/(b-a) on a closed interval.",
        "engine": "calculus_derivative_rules `average_rate_of_change` (quad leftover / cubic+quad_const+linear leftover / poly+shifted+reciprocal).",
    },
    "calc_app_diff_limits_in_form_of_definition_of_derivative": {
        "flag_why": "Shipped leftover lockout of D=0 x^2 x→a / h→0; LIMITATIONS eight frozen old builders / no general f.",
        "skill": "Recognize a difference quotient as f'(a) and evaluate it from the definition.",
        "engine": "calculus_derivative_rules `definition_of_derivative` (limit_h/limit_x leftover / cube+kx^2 leftover / reciprocal+sqrt+poly).",
    },
    "calc_app_diff_related_rates": {
        "force_flags": ["LOW_VARIETY"],
        "flag_why": "Related-rates often one geometry Mad-Lib; OpenStax §4.1 rotates ladder/cone/shadow/…",
        "skill": "Implicit differentiate related quantities; plug rates.",
        "engine": "WP frames over Diff/implicit core; several OpenStax frames at same D.",
    },
    "calc_app_diff_linear_approximations": {
        "flag_why": "Shipped leftover lockout of x^2 + Ex. 4.5 estimate-sqrt; LIMITATIONS no Ex. 4.6 sin / cube-root / (1+x)^n.",
        "skill": "Write L(x)=f(a)+f'(a)(x-a), or estimate a nearby value from leftover x^2 / √x.",
        "engine": "calc_app_diff `linear_approximation` (quad leftover / sqrt leftover / estimate / reciprocal / exp).",
    },
    "calc_app_int_motion_along_a_line_revisited": {
        "flag_why": "Shipped leftover lockout of linear v=2t + Ex. 5.25 distance on the same v; LIMITATIONS no Ex. 5.24 nonzero net / quadratic v(t).",
        "skill": "Use FTC / net change for displacement from v(t), or ∫|v| total distance at high D.",
        "engine": "calc_app_diff `motion_along_a_line_integral` (linear leftover / const leftover / sign-change / distance).",
    },
    "calc_diff_eq_introduction": {
        "flag_why": "Shipped leftover lockout of exp verify; LIMITATIONS no classify-order / IVP find-C / trig verify.",
        "skill": "Verify a proposed family solves a first-order DE.",
        "engine": "calc_app_diff `de_introduction` (exp leftover / Euler power).",
    },
    "calc_diff_eq_slope_fields": {
        "flag_why": "Shipped leftover lockout of y'=x; LIMITATIONS eval-at-a-point only (no direction-field figures).",
        "skill": "Evaluate y'=F(x,y) at a lattice point (read a slope-field hash).",
        "engine": "calc_app_diff `slope_field_interpret` (y'=x leftover / y'=x+y leftover / y'=xy).",
    },
    "calc_diff_eq_separable": {
        "flag_why": "Shipped leftover lockout of poly dy/dx=ax; LIMITATIONS frozen y/x IVP / no OpenStax mixes / logistic.",
        "skill": "Separate variables, integrate, apply the initial condition.",
        "engine": "calc_app_diff `separable_diff_eq` (poly leftover / exp leftover / homogeneous y/x).",
    },
    "calc_diff_eq_exponential_growth_and_decay": {
        "flag_why": "Shipped leftover lockout of story y'=ky; LIMITATIONS no Newton's cooling / logistic / find-k from data.",
        "skill": "Solve continuous y'=ky stories, IVPs, and half-life / doubling counts.",
        "engine": "calc_app_diff `calc_continuous_growth_decay` (growth leftover / decay leftover / IVP / doubling / half-life).",
    },
    "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution": {
        "flag_why": "Skip further leftover lockout: EMH presets + stamps already; LIMITATIONS D=0 majority du_over_u_trig / D=16===D=22 challenging.",
        "skill": "Indefinite ln/exp antiderivative after u-sub +C.",
        "engine": "Reuse `integrals.py` `_sample_u_sub_derivative_backed` flavor ln_exp + u_substitution.json presets.",
    },
    "calc_indef_int_inverse_trigonometric_with_substitution": {
        "flag_why": "Skip further leftover lockout: EMH presets + stamps already; LIMITATIONS D=0 and D=8 frozen arctan_of_linear / D=16===D=22 reverse-chain.",
        "skill": "Indefinite invtrig antiderivative after u-sub +C.",
        "engine": "Reuse `integrals.py` `_sample_u_sub_derivative_backed` flavor invtrig + arctan_chain / reverse-chain.",
    },
    "calc_indef_int_power_rule_with_substitution": {
        "flag_why": "Skip further leftover lockout: EMH presets + stamps already; LIMITATIONS D=0 frozen power_linear_du / D=16===D=22 challenging mix.",
        "skill": "Indefinite power antiderivative after u-sub +C.",
        "engine": "Reuse `integrals.py` `_sample_u_sub_derivative_backed` flavor power + u_substitution.json presets.",
    },
    "calc_indef_int_trigonometric_with_substitution": {
        "flag_why": "Skip further leftover lockout: EMH presets + stamps already; LIMITATIONS D=0 frozen sqrt_a2_minus_x2 / D=16===D=22 bc_bank mix.",
        "note": "Catalog name says trig substitution; generator is `integral_trig_substitution` (Calc 2 §3.3).",
        "skill": "Integrate using a trigonometric substitution.",
        "engine": "Reuse `integrals.py` `_sample_trig_sub` + trig_substitution.json + named bc_bank.",
    },
    "calc_indef_int_multi_trick": {
        "flag_why": "Shipped leftover lockout of D=0 linear/exp/trig; LIMITATIONS D=16===D=22 log-only / no u-sub-then-parts.",
        "skill": "Integrate with a multi-step technique pipeline (u-sub then PFD).",
        "engine": "Reuse `integrals.py` `_sample_pipeline_u_sub_then_pfd` (linear leftover / exp+trig leftover / log).",
    },
}


def _targets():
    return [e for e in CATALOG if _in_scope(e)]


def _clip(s: str, n: int = 380) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s if len(s) <= n else s[: n - 1] + "…"


def _math(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return "_(empty)_"
    if "$" in s:
        return s
    return f"${s}$"


def _mine_path(fname: str) -> Path | None:
    for root in (MINE_V1, MINE_V2):
        p = root / fname
        if p.exists():
            return p
    return None


def _extract_examples(fname: str, limit: int = 2) -> list[str]:
    path = _mine_path(fname)
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    out: list[str] = []
    for item in data.get("items") or []:
        if item.get("kind") != "example":
            continue
        title = (item.get("title") or "").strip()
        prompt = re.sub(r"\s+", " ", (item.get("prompt_text") or "").strip())
        if "If you missed" in prompt:
            continue
        if len(prompt) > 180:
            prompt = prompt[:177] + "…"
        if title and prompt:
            out.append(f"{title}: {prompt}")
        elif prompt:
            out.append(prompt)
        if len(out) >= limit:
            break
    return out


def sample_type(type_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for d in DS:
        for seed in SEEDS:
            settings = {
                "difficulty": d,
                "seed": seed,
                "count": 1,
                "include_answer_key": True,
            }
            try:
                qs = _generate_for_type(type_id, settings)
                q = qs[0]
                meta = q.metadata or {}
                rows.append(
                    {
                        "d": d,
                        "seed": seed,
                        "prompt": q.prompt_latex or q.prompt_text or "",
                        "answer": q.answer_latex or "",
                        "pattern": meta.get("skeleton_pattern")
                        or meta.get("integral_method")
                        or meta.get("technique")
                        or "",
                        "form_id": meta.get("form_id") or "",
                        "has_figure": bool(
                            meta.get("figure")
                            or meta.get("diagram")
                            or meta.get("coordinate_plane")
                            or meta.get("slope_field")
                        ),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                rows.append({"d": d, "seed": seed, "error": str(exc)})
    return rows


def _looks_like_generic_dx(prompt: str) -> bool:
    """Foundations fallthrough often emits bare d/dx power."""
    p = re.sub(r"\s+", "", (prompt or "").lower())
    return bool(re.search(r"\\frac\{d\}\{d[a-z]\}", p)) and "int" not in p


def _flags_for(entry, sampled: list[dict[str, Any]]) -> tuple[list[str], str]:
    meta = META.get(entry.id) or {}
    flags = list(meta.get("force_flags") or [])
    why = str(meta.get("flag_why") or "")

    prompts = [str(r.get("prompt") or "") for r in sampled if not r.get("error")]
    blob = "\n".join(prompts).lower()
    if any(m in blob for m in DUMP_MARKERS) or any(
        looks_like_dumped_equation(p) for p in prompts if p
    ):
        if "UNCLEAR" not in flags:
            flags.append("UNCLEAR")
        if "LOW_VARIETY" not in flags:
            flags.append("LOW_VARIETY")
        if not why:
            why = "Old path looks like an equation-dump stub."

    if entry.generator == "calculus_foundations":
        generics = sum(1 for p in prompts if _looks_like_generic_dx(p))
        if generics >= 2 and "UNCLEAR" not in flags:
            flags.append("UNCLEAR")
            if not why:
                why = "Multiple samples look like generic d/dx fallthrough from `calculus_foundations`."

    d0 = [
        re.sub(r"\d+", "N", r.get("prompt") or "")
        for r in sampled
        if r.get("d") == 0 and r.get("prompt")
    ]
    if len(d0) >= 2 and len(set(d0)) == 1 and "LOW_VARIETY" not in flags:
        # Integrals often share one structure at D=0 — only flag story/app leaves.
        if any(
            k in entry.id
            for k in ("optimization", "related_rates", "motion", "growth", "word")
        ):
            flags.append("LOW_VARIETY")
            if not why:
                why = "One template across seeds at D=0."

    errs = [r for r in sampled if r.get("error")]
    if len(errs) >= 4 and "UNCLEAR" not in flags:
        flags.append("UNCLEAR")
        if not why:
            why = "Many generate errors at sampled D/seeds."

    return flags, why


def _has_filled_notes(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "openstax.org" in text and "What old path actually produced" in text


def _engine_proposal(entry) -> str:
    meta = META.get(entry.id) or {}
    if meta.get("engine"):
        return str(meta["engine"])
    gen = entry.generator
    if gen.startswith("integral_") or gen in {
        "integration_by_parts",
        "first_fundamental_theorem",
        "second_fundamental_theorem",
    }:
        return (
            "Reuse `question_engine/frameworks/primitives/integrals.py` + OpenStax "
            "form catalogs; harden difficulty via real technique structure (not Diff)."
        )
    if gen in {
        "area_under_curve",
        "area_between_curves",
        "volume_disk_washer",
        "volume_shell",
        "volume_cross_sections",
        "riemann_approximate_area",
        "riemann_sum_tables",
        "def_int_mean_value",
    }:
        return (
            "Keep constructive integral-application builders; optional Integral "
            "skeleton for shared definite-integral cores."
        )
    if gen in {
        "rolles_theorem",
        "mean_value_theorem",
        "intervals_increase_decrease",
        "lhopitals_rule",
        "differentials",
        "linear_approximation",
        "tangent_normal_line",
        "related_rates_simple",
    }:
        return (
            "Keep current constructive/pilot generators; reuse Diff only where the "
            "student differentiates; apps framing stays separate."
        )
    if gen in {
        "slope_field_interpret",
        "separable_diff_eq",
        "calc_continuous_growth_decay",
        "exponential_growth_decay",
    }:
        return "Keep DE constructive/pilot path; not Diff skeleton."
    if gen == "calculus_foundations":
        return (
            "Leave leaf or replace foundations fallthrough with a dedicated pack; "
            "do not fake difficulty on Diff."
        )
    return f"Reuse live `{gen}` until a dedicated skeleton exists."


def render_notes(entry, sampled: list[dict[str, Any]]) -> str:
    meta = META.get(entry.id) or {}
    flags, why = _flags_for(entry, sampled)
    banner = ""
    if flags:
        banner = f"> **{' / '.join(flags)}**" + (f" — {why}" if why else "") + "\n\n"

    skill = meta.get("skill") or f"Practice {entry.name.lower()}."
    d0 = meta.get("d0") or "As simple as old easy at D=0 — copy live samples below."
    high = meta.get("high") or "Numeric hardness first; technique/format unlocks by D≈16–22."
    must_not = meta.get("must_not") or (
        "Wrong-topic shapes; derivative-only prompts on integral leaves; "
        "equation dumps without story on WP/optimization/related-rates."
    )

    lines = [
        f"# Notes — `{entry.id}`",
        "",
        banner.rstrip(),
        "",
        f"- **Display name:** {entry.name}",
        f"- **Category:** {entry.category}",
        f"- **Generator:** `{entry.generator}`",
        f"- **Suggested family:** `other`",
        "",
        "---",
        "",
        "## What the question should look like (D=0 vs high D)",
        "",
        f"- **Skill:** {skill}",
        f"- **D=0:** {d0}",
        f"- **High D (≈16–22):** {high}",
        f"- **Must not:** {must_not}",
        "",
        "## What old path actually produced (real latex, D=0/8/16/22)",
        "",
        "Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.",
        "",
        "| D | seed | prompt_latex | answer_latex | shape notes |",
        "|---|------|--------------|--------------|-------------|",
    ]
    for row in sampled:
        d = row["d"]
        dlab = int(d) if d == int(d) else d
        if row.get("error"):
            lines.append(
                f"| {dlab} | {row['seed']} | **ERROR** | | `{_clip(row['error'], 120)}` |"
            )
            continue
        notes = []
        if row.get("pattern"):
            notes.append(f"pattern={row['pattern']}")
        if row.get("form_id"):
            notes.append(f"form={row['form_id']}")
        if row.get("has_figure"):
            notes.append("figure")
        shape = ", ".join(notes) if notes else "—"
        lines.append(
            f"| {dlab} | {row['seed']} | {_math(_clip(row.get('prompt') or ''))} | "
            f"{_math(_clip(str(row.get('answer') or ''), 180))} | {shape} |"
        )

    lines.extend(
        [
            "",
            "Opt-out flag used: `(none — live default is old path)`",
            "",
            "## OpenStax examples + chapter/section cites",
            "",
            "Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.",
            "",
            "| Cite | URL | What to copy (shape / frame, not wording) |",
            "|------|-----|-------------------------------------------|",
        ]
    )

    cites = TYPE_CITES.get(entry.id) or [
        ("v1", entry.name, "", None, entry.category),
    ]
    for book, section, slug, mine, shape in cites[:3]:
        base = V1 if book == "v1" else V2
        book_name = "Calculus Volume 1" if book == "v1" else "Calculus Volume 2"
        url = f"{base}/{slug}" if slug else base
        shape_txt = shape
        if mine:
            ex = _extract_examples(mine, limit=2)
            if ex:
                shape_txt += " — e.g. " + "; ".join(ex[:2])
        sec_num = section.split(" ", 1)[0] if section else ""
        lines.append(f"| OpenStax {book_name} §{sec_num} | {url} | {shape_txt} |")

    lines.extend(
        [
            "",
            "Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · "
            "`scripts/output/example_mining/calculus-volume-1/stage1/` "
            "(and volume-2).",
            "",
            "## Variety notes / UNCLEAR flag",
            "",
        ]
    )
    if why:
        lines.append(why)
    else:
        lines.append(
            "Not a Mad-Lib WP unless related-rates / optimization / growth-decay. "
            "Algebra/technique shapes follow old path samples above; OpenStax frames "
            "win for story variety."
        )
    if meta.get("note"):
        lines.append(f"Note: {meta['note']}")
    if flags:
        lines.append(f"Flags: {', '.join(f'`{f}`' for f in flags)}.")
    lines.extend(
        [
            "",
            "## Proposed engine (reuse vs new) — proposal only",
            "",
            f"- **Proposal:** {_engine_proposal(entry)}",
            "- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.",
            "- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.",
            "- **Not this pass:** notes only — no generator wiring.",
            "",
            f"_Catalog generator `{entry.generator}`; limits/differentiation owned by other agent._",
            "",
        ]
    )
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def build_index(summary: dict[str, Any]) -> str:
    excluded = [e.id for e in CATALOG if not _in_scope(e)]
    lines = [
        "# Calculus type index (apps / integrals / DE notes pass)",
        "",
        "Steps 1–3 only: old-path samples, OpenStax Calc Vol 1/2 cites, proposed engine.",
        "Limits + Differentiation chapters (and definition-of-derivative limit form) are",
        "owned by the derivatives/limits agent.",
        "",
        "**No Calc 2 series catalog** in `question_engine/catalogs/calculus.py` —",
        "series / improper integrals / full Calc 2 DE chapter are not separate type_ids here",
        "(technique leaves like parts / trig-sub / PFD live under Indefinite Integration).",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Calculus catalog leaves | {len(CATALOG)} |",
        f"| Excluded (limits/diff agent) | {len(excluded)} |",
        f"| This pass (targets) | {len(_targets())} |",
        f"| Notes written | {len(summary.get('written', []))} |",
        f"| Skipped (already filled) | {len(summary.get('skipped', []))} |",
        f"| UNCLEAR flagged | {len(summary.get('unclear', []))} |",
        f"| LOW_VARIETY flagged | {len(summary.get('low_variety', []))} |",
        "",
        "## UNCLEAR / LOW_VARIETY",
        "",
    ]
    unclear = summary.get("unclear", [])
    low = set(summary.get("low_variety", []))
    if not unclear and not low:
        lines.append("- _(none)_")
    else:
        for tid in sorted(set(unclear) | low):
            flags = summary.get("flags", {}).get(tid, [])
            lines.append(f"- `{tid}` — {', '.join(flags)}")
    lines.extend(
        [
            "",
            "## Excluded (other agent)",
            "",
        ]
    )
    for tid in sorted(excluded):
        lines.append(f"- `{tid}`")
    lines.extend(["", "## Notes files", ""])
    for tid in sorted(summary.get("written", []) + summary.get("skipped", [])):
        lines.append(f"- [`{tid}.md`]({tid}.md)")
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "written": [],
        "skipped": [],
        "unclear": [],
        "low_variety": [],
        "flags": {},
        "errors": {},
    }
    for entry in _targets():
        path = OUT / f"{entry.id}.md"
        if _has_filled_notes(path):
            summary["skipped"].append(entry.id)
            continue
        sampled = sample_type(entry.id)
        flags, _ = _flags_for(entry, sampled)
        summary["flags"][entry.id] = flags
        if "UNCLEAR" in flags:
            summary["unclear"].append(entry.id)
        if "LOW_VARIETY" in flags:
            summary["low_variety"].append(entry.id)
        errs = [r["error"] for r in sampled if r.get("error")]
        if errs:
            summary["errors"][entry.id] = errs[:3]
        path.write_text(render_notes(entry, sampled), encoding="utf-8")
        summary["written"].append(entry.id)
        print(f"wrote {entry.id} flags={flags}", flush=True)

    (OUT / "_calc_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (OUT / "CALC_INDEX.md").write_text(build_index(summary), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in summary.items() if k not in ("errors", "flags")},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
