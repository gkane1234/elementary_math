"""Steps 1–3 for Prealgebra catalog leaves: old-path samples + notes.md.

Does not implement engines. Writes ``notes/<type_id>.md``.
Skip if a notes file already exists and contains an openstax.org cite.
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

from question_engine.catalogs.pre_algebra import CATALOG
from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.wp_packaging import looks_like_dumped_equation

OUT = Path(__file__).resolve().parent
MINE_PA = _ROOT / "scripts/output/example_mining/prealgebra-2e/stage1"
MINE_EA = _ROOT / "scripts/output/example_mining/elementary-algebra-2e/stage1"

DS = (0.0, 8.0, 16.0, 22.0)
SEEDS = (101, 207)

DUMP_MARKERS = (
    "the equation is",
    "giving $",
    "satisfy $",
    "reduces to $",
    "uses a proportion",
    "to scale a recipe",
)

SKELETONED = {
    "pa_equations_one_step_word_problems",
    "pa_equations_two_step_word_problems",
    "pa_equations_multi_step_equations",
    "pa_multi_step_inequalities",
    "pa_checking_for_a_proportion",
    "pa_proportions_word_problems",
    "pa_similar_figures",
    "pa_similar_figures_word_problems",
    "pa_polynomials_adding_and_subtracting",
    "pa_polynomials_multiplying",
    "pa_polynomials_simplifying",
}

OPT_OUT: dict[str, dict[str, Any]] = {
    "pa_equations_one_step_word_problems": {"use_sample_linear_equation": True},
    "pa_equations_two_step_word_problems": {"use_sample_linear_equation": True},
    "pa_equations_multi_step_equations": {"use_sample_linear_equation": True},
    "pa_multi_step_inequalities": {"use_sample_linear_inequality": True},
    "pa_checking_for_a_proportion": {"use_sample_proportion": True},
    "pa_proportions_word_problems": {"use_sample_linear_equation": True},
    "pa_similar_figures": {"use_legacy_similar_figures": True},
    "pa_similar_figures_word_problems": {"use_legacy_similar_figures": True},
    "pa_polynomials_adding_and_subtracting": {"use_sample_polynomial_add_subtract": True},
    "pa_polynomials_multiplying": {"use_factor_poly": True},
    "pa_polynomials_simplifying": {"use_sample_expand_simplify": True},
}

PA = "https://openstax.org/books/prealgebra-2e/pages"
EA = "https://openstax.org/books/elementary-algebra-2e/pages"


def _cite(book: str, section: str, slug: str, mine: str | None = None, extra: list[str] | None = None):
    base = PA if book.startswith("Prealgebra") else EA
    return {
        "book": book,
        "section": section,
        "url": f"{base}/{slug}",
        "mine": mine,
        "extra": extra or [],
    }


# Per-type: should-look-like, OpenStax cites, engine proposal, forced flags.
META: dict[str, dict[str, Any]] = {
    "pa_naming_decimal_places_and_rounding": {
        "should": (
            "D=0: name tenths/hundredths of a short decimal (e.g. 4.7 → tenths) "
            "or round to nearest whole/tenth. High D: thousandths–millionths, "
            "round to a named place, or expanded form."
        ),
        "cites": [
            _cite("Prealgebra 2e", "5.1 Decimals", "5-1-decimals", "5-1-decimals.json"),
        ],
        "engine": "Reuse number/place-value generator. No new skeleton. Difficulty already magnitude + place-depth.",
    },
    "pa_writing_numbers_with_words": {
        "should": (
            "D=0: two- or three-digit whole numbers in words. High D: decimals "
            "(and/or large place names) matching OpenStax 5.1 write-in-words items."
        ),
        "cites": [
            _cite("Prealgebra 2e", "5.1 Decimals", "5-1-decimals", "5-1-decimals.json"),
        ],
        "engine": "Reuse writing_numbers_with_words. No new engine.",
    },
    "pa_integers_adding_and_subtracting": {
        "should": (
            "D=0: two small same-sign addends (5+3 or −2+(−4)). High D: unlike signs, "
            "subtract as add-opposite, 3+ addends, parentheses, evaluate a variable expression."
        ),
        "cites": [
            _cite("Prealgebra 2e", "3.2 Add Integers", "3-2-add-integers", "3-2-add-integers.json"),
            _cite(
                "Prealgebra 2e",
                "3.3 Subtract Integers",
                "3-3-subtract-integers",
                "3-3-subtract-integers.json",
            ),
        ],
        "engine": "Reuse integer-ops number engine (pa_integers_adding_and_subtracting). Do not fold into affine.",
    },
    "pa_integers_multiplying": {
        "should": (
            "D=0: two small integers with an obvious sign (−3)(4). High D: three+ factors, "
            "or evaluate a product expression with a substituted integer."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "3.4 Multiply and Divide Integers",
                "3-4-multiply-and-divide-integers",
                "3-4-multiply-and-divide-integers.json",
            ),
        ],
        "engine": "Reuse g6_integer_multiply. Shared G6/PA number engine.",
    },
    "pa_integers_dividing": {
        "should": (
            "D=0: two small integers, exact quotient, one negative. High D: more digits, "
            "or mixed ± with a remainder-free quotient (OpenStax integer ÷ stays exact)."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "3.4 Multiply and Divide Integers",
                "3-4-multiply-and-divide-integers",
                "3-4-multiply-and-divide-integers.json",
            ),
        ],
        "engine": "Reuse g6_integer_divide. Shared G6/PA number engine.",
    },
    "pa_factoring": {
        "should": (
            "This is **numeric** factoring (list factor pairs of n), not polynomial GCF. "
            "D=0: n≤20 with a few pairs. High D: larger n / more pairs, maybe prime-or-composite language."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "2.4 Find Multiples and Factors",
                "2-4-find-multiples-and-factors",
                extra=[
                    "Typical: list all factors of 24; identify multiples of 8; "
                    "prime vs composite (no local mine for Ch 2).",
                ],
            ),
        ],
        "engine": "Reuse g6_factoring (number). Do not wire FactorProduct / poly skeleton.",
    },
    "pa_greatest_common_factor": {
        "should": (
            "D=0: GCF of two small positives (12 and 18 → 6). High D: three numbers "
            "or larger composites; still numeric, not monomial GCF of polynomials."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "2.5 Prime Factorization and the Least Common Multiple",
                "2-5-prime-factorization-and-the-least-common-multiple",
                extra=[
                    "GCF via prime factors (e.g. GCF(24,36)=12). LCM lives on the sibling leaf.",
                ],
            ),
            _cite(
                "Elementary Algebra 2e",
                "7.1 Greatest Common Factor and Factor by Grouping",
                "7-1-greatest-common-factor-and-factor-by-grouping",
                "7-1-greatest-common-factor-and-factor-by-grouping.json",
            ),
        ],
        "engine": "Reuse g6_greatest_common_factor (number). Polynomial monomial GCF is a different leaf (FactorGcf).",
    },
    "pa_least_common_multiple": {
        "should": (
            "D=0: LCM of two small positives (4 and 6 → 12). High D: three numbers or larger."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "2.5 Prime Factorization and the Least Common Multiple",
                "2-5-prime-factorization-and-the-least-common-multiple",
                extra=["LCM(12,18)=36 via primes or listing multiples."],
            ),
        ],
        "engine": "Reuse g6_least_common_multiple (number).",
    },
    "pa_simplifying_fractions": {
        "should": (
            "D=0: cancel a small GCF (10/15 → 2/3). High D: larger GCF / improper leftover, "
            "signed fractions. OpenStax 4.1 also has improper↔mixed and models — those are extra."
        ),
        "cites": [
            _cite("Prealgebra 2e", "4.1 Visualize Fractions", "4-1-visualize-fractions", "4-1-visualize-fractions.json"),
        ],
        "engine": "Reuse simplifying_numeric_fractions (number). Mixed/improper conversion is a catalog gap.",
    },
    "pa_fractions_add_like": {
        "should": (
            "D=0: two unit-ish fractions same denom, already simplified or one cancel after. "
            "High D: larger numerators, simplify after, maybe three terms. No mixed numbers (4.6 gap)."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "4.4 Add and Subtract Fractions with Common Denominators",
                "4-4-add-and-subtract-fractions-with-common-denominators",
                "4-4-add-and-subtract-fractions-with-common-denominators.json",
            ),
        ],
        "engine": "Reuse g6_fraction_add_like (number). PA is a thin alias.",
    },
    "pa_fractions_subtract_like": {
        "should": (
            "Same as add-like but subtraction. D=0: 5/8−1/8. High D: simplify after / signed."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "4.4 Add and Subtract Fractions with Common Denominators",
                "4-4-add-and-subtract-fractions-with-common-denominators",
                "4-4-add-and-subtract-fractions-with-common-denominators.json",
            ),
        ],
        "engine": "Reuse g6_fraction_subtract_like (number).",
    },
    "pa_fractions_add_unlike": {
        "should": (
            "D=0: two fractions whose LCD is one of the denoms (1/2+1/6). High D: LCD "
            "is a product, 3+ terms, cancel after."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "4.5 Add and Subtract Fractions with Different Denominators",
                "4-5-add-and-subtract-fractions-with-different-denominators",
                "4-5-add-and-subtract-fractions-with-different-denominators.json",
            ),
        ],
        "engine": "Reuse g6_fraction_add_unlike (number).",
    },
    "pa_fractions_subtract_unlike": {
        "should": (
            "Unlike-denom subtraction. D=0: LCD is a listed denom. High D: borrow-like "
            "improper results; still not mixed-number arithmetic (4.6 gap)."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "4.5 Add and Subtract Fractions with Different Denominators",
                "4-5-add-and-subtract-fractions-with-different-denominators",
                "4-5-add-and-subtract-fractions-with-different-denominators.json",
            ),
        ],
        "engine": "Reuse g6_fraction_subtract_unlike (number).",
    },
    "pa_fractions_multiply": {
        "should": (
            "D=0: two unit fractions or no cancel (1/2·1/3). High D: cancel-before-multiply, "
            "improper intermediates. Mixed × and complex fractions (4.3) are a catalog gap."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "4.2 Multiply and Divide Fractions",
                "4-2-multiply-and-divide-fractions",
                "4-2-multiply-and-divide-fractions.json",
            ),
        ],
        "engine": "Reuse g6_fraction_multiply (number).",
    },
    "pa_fractions_divide": {
        "should": (
            "D=0: ÷ a unit fraction (multiply by reciprocal). High D: cancel across the reciprocal."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "4.2 Multiply and Divide Fractions",
                "4-2-multiply-and-divide-fractions",
                "4-2-multiply-and-divide-fractions.json",
            ),
        ],
        "engine": "Reuse g6_fraction_divide (number).",
    },
    "pa_converting_fractions_and_decimals": {
        "should": (
            "D=0: terminating tenths/hundredths (3/10 ↔ 0.3). High D: repeating or "
            "awkward terminating (3/8, 2/11)."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "5.3 Decimals and Fractions",
                "5-3-decimals-and-fractions",
                "5-3-decimals-and-fractions.json",
            ),
        ],
        "engine": "Reuse converting_fractions_and_decimals (number).",
    },
    "pa_equations_one_step_word_problems": {
        "should": (
            "Story first (number, spent/left, shares, tickets) whose reverse algebra is "
            "one step. Never dump “the equation is $x+1=3$”. D=0 stays one easy frame."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.1 Use a Problem Solving Strategy",
                "9-1-use-a-problem-solving-strategy",
                extra=[
                    "Translate-then-solve number stories (13 less than a number is 18).",
                ],
            ),
            _cite(
                "Prealgebra 2e",
                "9.2 Solve Money Applications",
                "9-2-solve-money-applications",
                extra=["Tickets / coins / purchase leftover — still one equation."],
            ),
            _cite(
                "Prealgebra 2e",
                "3.5 Solve Equations Using Integers; The Division Property of Equality",
                "3-5-solve-equations-using-integers-the-division-property-of-equality",
                "3-5-solve-equations-using-integers-the-division-property-of-equality.json",
            ),
        ],
        "engine": "Reuse SolveLinear + wp_packaging frames (already skeletoned). Old path is the dump stub — do not revive it.",
        "force_flags": ["UNCLEAR", "LOW_VARIETY"],
        "flag_why": "Old opt-out dumps “the equation is $…$” / one Mad-Lib. OpenStax is richer (number, money, tickets).",
    },
    "pa_equations_two_step_word_problems": {
        "should": (
            "ax±b=c as a story (twice-more, earnings, unit+fee). D=0 small positive ints. "
            "Do not dump the equation. Keep two-step algebra (not mixture/systems)."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "8.2 Solve Equations Using the Division and Multiplication Properties of Equality",
                "8-2-solve-equations-using-the-division-and-multiplication-properties-of-equality",
                extra=["Two-step isolate after one add/sub then ÷."],
            ),
            _cite(
                "Prealgebra 2e",
                "9.1 Use a Problem Solving Strategy",
                "9-1-use-a-problem-solving-strategy",
                extra=["Translate phrases then solve two-step."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "2.2 Solve Equations Using the Division and Multiplication Properties of Equality",
                "2-2-solve-equations-using-the-division-and-multiplication-properties-of-equality",
                "2-2-solve-equations-using-the-division-and-multiplication-properties-of-equality.json",
            ),
        ],
        "engine": "Reuse SolveLinear + wp_packaging (already skeletoned). Old path is dump stub.",
        "force_flags": ["UNCLEAR", "LOW_VARIETY"],
        "flag_why": "Old path: “starts with a number and applies two operations, giving $ax±b=c$”.",
    },
    "pa_equations_multi_step_equations": {
        "should": (
            "D=0: simple distribute or both-sides with small ints, e.g. 2(x+1)=8 or 3x+2=x+8. "
            "High D: larger coeffs, then fraction/decimal coefficients (PA 8.4 / EA 2.5) — "
            "numeric hardness before extra format."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "8.3 Solve Equations with Variables and Constants on Both Sides",
                "8-3-solve-equations-with-variables-and-constants-on-both-sides",
                extra=["Collect like terms across = ; 7x+5=6x−3 shape."],
            ),
            _cite(
                "Prealgebra 2e",
                "8.4 Solve Equations with Fraction or Decimal Coefficients",
                "8-4-solve-equations-with-fraction-or-decimal-coefficients",
                extra=["Clear denominators / ×10^n. Dedicated mode is only partial in PA multi-step."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "2.4 Use a General Strategy to Solve Linear Equations",
                "2-4-use-a-general-strategy-to-solve-linear-equations",
                "2-4-use-a-general-strategy-to-solve-linear-equations.json",
            ),
            _cite(
                "Elementary Algebra 2e",
                "2.3 Solve Equations with Variables and Constants on Both Sides",
                "2-3-solve-equations-with-variables-and-constants-on-both-sides",
                "2-3-solve-equations-with-variables-and-constants-on-both-sides.json",
            ),
        ],
        "engine": "Reuse SolveLinear (already skeletoned as multi_step_equations alias). No new engine.",
    },
    "pa_multi_step_inequalities": {
        "should": (
            "Same reverse tape as multi-step equations with < > ≤ ≥. D=0: 2(x+1)<8, no flip. "
            "High D: negatives that force a flip, both sides. Graph-on-number-line is a different leaf."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "2.7 Solve Linear Inequalities",
                "2-7-solve-linear-inequalities",
                "2-7-solve-linear-inequalities.json",
            ),
            _cite(
                "Prealgebra 2e",
                "11.7 Graphs of Linear Inequalities",
                "11-7-graphs-of-linear-inequalities",
                extra=["PA graphs 2-var inequalities; 1-var multi-step solve is EA 2.7."],
            ),
        ],
        "engine": "Reuse SolveInequality (already skeletoned). No new engine.",
    },
    "pa_divisibility": {
        "should": (
            "D=0: even/odd or divisible-by-2/5/10 on a small n. High D: 3/6/9 tests on larger n. "
            "Yes/no (or which rules), not list-all-factors (that's pa_factoring)."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "2.4 Find Multiples and Factors",
                "2-4-find-multiples-and-factors",
                extra=[
                    "Divisibility tests for 2,3,5,6,10 on a whole number (e.g. is 5,625 divisible by 3?).",
                ],
            ),
        ],
        "engine": "Reuse g6_divisibility (number). No skeleton needed.",
    },
    "pa_squares_and_square_roots": {
        "should": (
            "D=0: perfect squares / √n for 1–12. High D: estimate non-perfects or simplify √(a²b) "
            "at PA level (not full radical algebra)."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "5.7 Simplify and Use Square Roots",
                "5-7-simplify-and-use-square-roots",
                extra=["√36=6; approximate √5; simplify √48 → 4√3 (PA-lite)."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "9.1 Simplify and Use Square Roots",
                "9-1-simplify-and-use-square-roots",
                "9-1-simplify-and-use-square-roots.json",
            ),
        ],
        "engine": "Reuse pa_squares_and_square_roots (number). Do not jump to A1 radical engine.",
    },
    "pa_checking_for_a_proportion": {
        "should": (
            "Catalog name is **check** two ratios (cross-multiply equal?). OpenStax 6.5 also "
            "solves a/b=c/x. D=0 should be either 2/3=4/6? or solve 2/3=x/12. Document the "
            "check-vs-solve mismatch if old path only solves."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "6.5 Solve Proportions and their Applications",
                "6-5-solve-proportions-and-their-applications",
                extra=[
                    "Determine whether 5/8 and 15/24 form a proportion; solve x/63=4/7.",
                ],
            ),
            _cite(
                "Elementary Algebra 2e",
                "8.7 Solve Proportion and Similar Figure Applications",
                "8-7-solve-proportion-and-similar-figure-applications",
                "8-7-solve-proportion-and-similar-figure-applications.json",
            ),
        ],
        "engine": "Reuse Proportion (already skeletoned as solving_proportions alias). Optionally add a check-only prompt mode — do not invent a second engine.",
        "force_flags": ["UNCLEAR"],
        "flag_why": "Leaf title is checking ratios; generator solves a/b=x/c. OpenStax 6.5 has both.",
    },
    "pa_proportions_word_problems": {
        "should": (
            "Recipe scale, unit-rate cost, map, calories, dosage — story first, unknown in a "
            "proportion. Do not dump a/b=x/c into the sentence. D=0 one easy recipe/unit-rate frame."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "6.5 Solve Proportions and their Applications",
                "6-5-solve-proportions-and-their-applications",
                extra=["Cookie recipe scale; map scale; similar-enough rate problems."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "8.7 Solve Proportion and Similar Figure Applications",
                "8-7-solve-proportion-and-similar-figure-applications",
                "8-7-solve-proportion-and-similar-figure-applications.json",
            ),
        ],
        "engine": "Reuse ProportionRate + wp_packaging (already skeletoned). Old path is recipe-dump stub.",
        "force_flags": ["UNCLEAR", "LOW_VARIETY"],
        "flag_why": "Old path: “uses a proportion $a/b=x/c$ to scale a recipe.” One template.",
    },
    "pa_similar_figures": {
        "should": (
            "Two similar polygons (triangles/rects) with a diagram; find a missing side or "
            "scale factor. D=0 integer scale 2–3. High D: larger sides; OpenStax also has "
            "shadows/maps/flags as stories (sibling WP leaf)."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "8.7 Solve Proportion and Similar Figure Applications",
                "8-7-solve-proportion-and-similar-figure-applications",
                "8-7-solve-proportion-and-similar-figure-applications.json",
            ),
            _cite(
                "Prealgebra 2e",
                "9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem",
                "9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem",
                extra=["Similar-triangle angle language sits here; missing-side via proportion is EA 8.7."],
            ),
        ],
        "engine": "Reuse SimilarFigures (already skeletoned). Do not implement a new engine.",
    },
    "pa_similar_figures_word_problems": {
        "should": (
            "Same math as similar figures but a **story** (shadow, map, flag, photo enlarge) "
            "not only labeled polygons. OpenStax 8.7 is richer than a single triangle Mad-Lib."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "8.7 Solve Proportion and Similar Figure Applications",
                "8-7-solve-proportion-and-similar-figure-applications",
                "8-7-solve-proportion-and-similar-figure-applications.json",
            ),
        ],
        "engine": "Reuse SimilarFigures + extra OpenStax story frames (same engine, more frames). Catalog currently shares wp_similar_figures with the diagram leaf.",
        "force_flags": ["LOW_VARIETY"],
        "flag_why": "Same generator as pa_similar_figures; OpenStax 8.7 also has shadows, maps, flags.",
    },
    "pa_fractions_decimals_and_percents": {
        "should": (
            "Conversion triad. D=0: 25% ↔ 1/4 ↔ 0.25. High D: percents >100 or repeating decimals."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "6.1 Understand Percent",
                "6-1-understand-percent",
                "6-1-understand-percent.json",
            ),
        ],
        "engine": "Reuse fractions_decimals_and_percents (number). No new engine.",
    },
    "pa_markup_discount_and_tax": {
        "should": (
            "Retail money: sales tax, commission, discount, mark-up. D=0 one-step (tax on a price). "
            "High D: discount-then-tax. Commission is an OpenStax 6.3 mode — include it."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "6.3 Solve Sales Tax, Commission, and Discount Applications",
                "6-3-solve-sales-tax-commission-and-discount-applications",
                "6-3-solve-sales-tax-commission-and-discount-applications.json",
            ),
            _cite(
                "Prealgebra 2e",
                "6.2 Solve General Applications of Percent",
                "6-2-solve-general-applications-of-percent",
                "6-2-solve-general-applications-of-percent.json",
            ),
        ],
        "engine": "Reuse PercentWordProblemFramework (wp_percent). Extend frames for commission if missing — not a new skeleton. TRACKING previously blocked dump stubs; verify live prompts are real retail stories.",
    },
    "pa_simple_and_compound_interest": {
        "should": (
            "OpenStax PA 6.4 is **simple** interest I=Prt (and solve for P/r/t). Compound is extra. "
            "D=0: find I given P,r,t in years. High D: months/days; solve for principal."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "6.4 Solve Simple Interest Applications",
                "6-4-solve-simple-interest-applications",
                "6-4-solve-simple-interest-applications.json",
            ),
        ],
        "engine": "Reuse wp_simple_and_compound_interest. Prefer OpenStax simple-interest ask-kinds over a single earn-I template.",
        "force_flags": ["LOW_VARIETY"],
        "flag_why": "OpenStax 6.4 solves for I, P, r, or t; old path may only earn-interest. Compound is not in PA 6.4.",
    },
    "pa_plotting_points": {
        "should": (
            "D=0: plot one or two points in Q1 with integer coords. High D: other quadrants, "
            "axes, several points. Identify quadrant language from PA 11.1 / EA 4.1."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "11.1 Use the Rectangular Coordinate System",
                "11-1-use-the-rectangular-coordinate-system",
                extra=["Plot (3,5); name the quadrant of (−2,4)."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "4.1 Use the Rectangular Coordinate System",
                "4-1-use-the-rectangular-coordinate-system",
                "4-1-use-the-rectangular-coordinate-system.json",
            ),
        ],
        "engine": "Reuse plotting_points (geometry/coordinate). Not SolveLinear.",
    },
    "pa_slope": {
        "should": (
            "D=0: slope between two lattice points with integer rise/run, maybe already reduced. "
            "High D: negative / zero / undefined; or from slope-intercept identification."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "11.4 Understand Slope of a Line",
                "11-4-understand-slope-of-a-line",
                extra=["m=(y2−y1)/(x2−x1); horizontal m=0; vertical undefined."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "4.4 Understand Slope of a Line",
                "4-4-understand-slope-of-a-line",
                "4-4-understand-slope-of-a-line.json",
            ),
        ],
        "engine": "Reuse slope generator (already on PRIM_EQUATIONS map). No new engine; graphing-from-slope is a different skill.",
    },
    "pa_writing_linear_equations": {
        "should": (
            "D=0: given slope and y-intercept → y=mx+b. High D: two points, or point-slope then convert."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "11.5 Use the Slope-Intercept Form of an Equation of a Line",
                "11-5-use-the-slope-intercept-form-of-an-equation-of-a-line",
                extra=["Write y=mx+b from m and intercept."],
            ),
            _cite(
                "Prealgebra 2e",
                "11.6 Find the Equation of a Line",
                "11-6-find-the-equation-of-a-line",
                extra=["Point-slope / two points."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "4.6 Find the Equation of a Line",
                "4-6-find-the-equation-of-a-line",
                "4-6-find-the-equation-of-a-line.json",
            ),
        ],
        "engine": "Reuse writing_linear_equations. Not SolveLinear (that solves for x).",
    },
    "pa_graphing_systems_of_equations": {
        "should": (
            "Two lines on a plane; D=0: integer intercepts, unique intersection. High D: "
            "parallel / coincident. Prompt is graph+read intersection, not substitution algebra."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "5.1 Solve Systems of Equations by Graphing",
                "5-1-solve-systems-of-equations-by-graphing",
                "5-1-solve-systems-of-equations-by-graphing.json",
            ),
            _cite(
                "Prealgebra 2e",
                "11.2 Graphing Linear Equations",
                "11-2-graphing-linear-equations",
                extra=["Single-line graphing is the prerequisite; systems graphing is EA 5.1."],
            ),
        ],
        "engine": "Reuse graph_system. Geometry/graph engine, not SolveLinear. Parallel/no-solution must stay on-topic.",
    },
    "pa_systems_substitution": {
        "should": (
            "D=0: one equation already solved for y (y=x+1, x+y=5). High D: solve a first "
            "equation for a variable, then substitute; maybe fractions later."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "5.2 Solving Systems of Equations by Substitution",
                "5-2-solving-systems-of-equations-by-substitution",
                "5-2-solving-systems-of-equations-by-substitution.json",
            ),
        ],
        "engine": "Reuse systems_substitution. New systems skeleton only if later A1 unification needs it — not for this notes pass.",
    },
    "pa_systems_word_problems": {
        "should": (
            "OpenStax EA 5.4: number, money/tickets, geometry, uniform motion. D=0 one easy "
            "number or tickets frame. Do **not** dump the system into the prompt."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "5.4 Solve Applications with Systems of Equations",
                "5-4-solve-applications-with-systems-of-equations",
                "5-4-solve-applications-with-systems-of-equations.json",
            ),
        ],
        "engine": "Need **new WP frames** on the existing systems sampler (not mixture onto one-step). Old path is adult/child tickets only.",
        "force_flags": ["UNCLEAR", "LOW_VARIETY"],
        "flag_why": "Old generator is a single tickets Mad-Lib. OpenStax 5.4 has number, money, geometry, motion.",
    },
    "pa_drawing_and_measuring_angles": {
        "should": (
            "D=0: name/measure an acute angle from a diagram, or classify acute/right/obtuse. "
            "High D: draw to a given measure. PA 9.3 is properties more than protractor skill."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem",
                "9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem",
                extra=["Classify angles; complementary/supplementary as a related skill (sibling leaf)."],
            ),
        ],
        "engine": "Reuse geo_angles. Geometry engine — not affine.",
        "force_flags": ["UNCLEAR"],
        "flag_why": "OpenStax PA 9.3 is angle *properties* more than drawing/measuring with a protractor. Confirm old path matches the leaf name.",
    },
    "pa_angle_relationships": {
        "should": (
            "D=0: complementary (x+40=90) or supplementary. High D: vertical / adjacent / "
            "triangle-sum. Keep PA-level (no parallel-line transveral soup unless the old path already has it)."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem",
                "9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem",
                extra=["Complementary, supplementary, triangle angle sum."],
            ),
        ],
        "engine": "Reuse geo_angle_relationships. Optional SolveLinear for the algebra once the diagram exists — same geometry primitive.",
    },
    "pa_plane_figures_triangles": {
        "should": (
            "Triangle measures: perimeter, area (½bh), maybe classify by sides. D=0 integer b,h. "
            "High D: missing height via a diagram, not trig."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.4 Use Properties of Rectangles, Triangles, and Trapezoids",
                "9-4-use-properties-of-rectangles-triangles-and-trapezoids",
                extra=["Triangle area A=½bh; perimeter as sum of sides."],
            ),
            _cite(
                "Prealgebra 2e",
                "9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem",
                "9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem",
                extra=["Triangle angle sum 180°."],
            ),
        ],
        "engine": "Reuse geo_triangle_area. Geometry — do not invent a poly engine.",
    },
    "pa_quadrilaterals": {
        "should": (
            "Rectangle/square/parallelogram/trapezoid: name, perimeter, or a missing side. "
            "Area can overlap the dedicated area leaf — prefer properties/perimeter here if old path does."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.4 Use Properties of Rectangles, Triangles, and Trapezoids",
                "9-4-use-properties-of-rectangles-triangles-and-trapezoids",
                extra=["Rectangle P=2L+2W; trapezoid area ½(b1+b2)h."],
            ),
        ],
        "engine": "Reuse geo_quadrilateral_area. Check overlap with pa_area_of_triangles_and_quadrilaterals.",
        "force_flags": ["UNCLEAR"],
        "flag_why": "Leaf vs pa_area_of_triangles_and_quadrilaterals may duplicate area. Confirm old-path task (classify vs area vs perimeter).",
    },
    "pa_area_of_triangles_and_quadrilaterals": {
        "should": (
            "Find area. D=0: rectangle or right triangle with integer sides. High D: parallelogram "
            "/ trapezoid; composite later only if old path already does."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.4 Use Properties of Rectangles, Triangles, and Trapezoids",
                "9-4-use-properties-of-rectangles-triangles-and-trapezoids",
                extra=["A=bh, A=½bh, trapezoid formula."],
            ),
        ],
        "engine": "Reuse geo_triangles_and_quadrilaterals_area.",
    },
    "pa_circles": {
        "should": (
            "D=0: circumference or area with integer r and π left in the answer (or 3.14). "
            "High D: given diameter, or find r from C/A."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.5 Solve Geometry Applications: Circles and Irregular Figures",
                "9-5-solve-geometry-applications-circles-and-irregular-figures",
                extra=["C=2πr, A=πr²; irregular figures as optional extra."],
            ),
        ],
        "engine": "Reuse geo_circle_measure.",
    },
    "pa_transformations": {
        "should": (
            "Translate / reflect / rotate / dilate a figure on a grid. OpenStax **Prealgebra and "
            "Elementary Algebra do not teach this** — it is a middle-school / geometry topic. "
            "Copy old-path shapes; do not invent from PA text."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "11.1 Use the Rectangular Coordinate System",
                "11-1-use-the-rectangular-coordinate-system",
                extra=["Nearest PA content is plotting points — not rigid motions."],
            ),
        ],
        "engine": "Reuse geo_transformations. No PA/EA OpenStax chapter — keep old shapes; do not force a SolveLinear rewrite.",
        "force_flags": ["UNCLEAR"],
        "flag_why": "No Prealgebra/EA OpenStax chapter for transformations. Gold is old path + a geometry text, not PA 11.",
    },
    "pa_classifying_volume_and_surface_area": {
        "should": (
            "D=0: rectangular prism volume lwh. High D: surface area, cylinder, or classify the solid. "
            "PA 9.6 is the gold."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.6 Solve Geometry Applications: Volume and Surface Area",
                "9-6-solve-geometry-applications-volume-and-surface-area",
                extra=["Rectangular solid V=lwh; cylinder V=πr²h; SA of a box."],
            ),
        ],
        "engine": "Reuse geo_solid_volume_surface.",
    },
    "pythagorean_theorem": {
        "should": (
            "D=0: 3-4-5 missing hypotenuse. High D: missing a leg, or a short application "
            "(ladder / TV diagonal) if old path has it. No trig."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem",
                "9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem",
                extra=["a²+b²=c²; 5-12-13 and 6-8-10 families."],
            ),
        ],
        "engine": "Reuse geo_pythagorean_theorem. Catalog id has no pa_ prefix but it is a PA leaf.",
    },
    "pa_polynomials_simplifying": {
        "should": (
            "Combine like terms in a polynomial (degree may be 2+). D=0: 3x²+5x² or a few "
            "linear+const terms. High D: more terms / subtraction of a grouped polynomial."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "10.1 Add and Subtract Polynomials",
                "10-1-add-and-subtract-polynomials",
                extra=["Simplify by combining like terms before add/sub of two polynomials."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "6.1 Add and Subtract Polynomials",
                "6-1-add-and-subtract-polynomials",
                "6-1-add-and-subtract-polynomials.json",
            ),
        ],
        "engine": "Reuse AffineInflate expand/simplify if old path is linear; else poly_skeleton / construct_poly. Check live samples before choosing.",
    },
    "pa_polynomials_adding_and_subtracting": {
        "should": (
            "Add or subtract two polynomials. D=0: two binomials degree ≤2. High D: more terms, "
            "subtract requiring distributing a minus."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "10.1 Add and Subtract Polynomials",
                "10-1-add-and-subtract-polynomials",
                extra=["(4x²+5x−3)+(2x²−7x+9); subtract with grouping."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "6.1 Add and Subtract Polynomials",
                "6-1-add-and-subtract-polynomials",
                "6-1-add-and-subtract-polynomials.json",
            ),
        ],
        "engine": "Reuse PolyAddSub (already skeletoned). No new engine.",
    },
    "pa_polynomials_multiplying": {
        "should": (
            "D=0: monomial×binomial or two linear binomials (FOIL). High D: binomial×trinomial. "
            "Special products can wait for the special-multiply leaf."
        ),
        "cites": [
            _cite(
                "Prealgebra 2e",
                "10.3 Multiply Polynomials",
                "10-3-multiply-polynomials",
                extra=["Distribute a monomial; FOIL (x+3)(x+5)."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "6.3 Multiply Polynomials",
                "6-3-multiply-polynomials",
                "6-3-multiply-polynomials.json",
            ),
        ],
        "engine": "Reuse FactorProduct multiply task (already skeletoned as polynomial_multiply).",
    },
}


def _mine_path(fname: str) -> Path | None:
    for root in (MINE_PA, MINE_EA):
        p = root / fname
        if p.exists():
            return p
    return None


def _extract_examples(fname: str, limit: int = 4) -> list[str]:
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
        if len(prompt) > 280:
            prompt = prompt[:277] + "…"
        if title and prompt:
            out.append(f"{title}: {prompt}")
        elif prompt:
            out.append(prompt)
        if len(out) >= limit:
            break
    return out


def _clip(s: str, n: int = 420) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s if len(s) <= n else s[: n - 1] + "…"


def sample_type(type_id: str) -> dict[str, Any]:
    extra = dict(OPT_OUT.get(type_id) or {})
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for d in DS:
        for seed in SEEDS:
            settings = {
                "difficulty": d,
                "seed": seed,
                "count": 1,
                "include_answer_key": True,
                **extra,
            }
            try:
                qs = _generate_for_type(type_id, settings)
                q = qs[0]
                meta = q.metadata or {}
                prompt = q.prompt_latex or q.prompt_text or ""
                rows.append(
                    {
                        "d": d,
                        "seed": seed,
                        "prompt": prompt,
                        "answer": q.answer_latex or "",
                        "pattern": meta.get("skeleton_pattern") or "",
                        "frame_id": meta.get("frame_id") or "",
                        "has_figure": bool(meta.get("figure") or meta.get("diagram") or meta.get("number_line_spec")),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(f"D={d} seed={seed}: {exc}")
                rows.append({"d": d, "seed": seed, "error": str(exc)})
    return {"rows": rows, "errors": errors, "opt_out": extra}


def _flags_for(type_id: str, sampled: dict[str, Any]) -> tuple[list[str], str]:
    meta = META.get(type_id) or {}
    flags = list(meta.get("force_flags") or [])
    why = str(meta.get("flag_why") or "")
    prompts = [str(r.get("prompt") or "") for r in sampled.get("rows") or [] if not r.get("error")]
    blob = "\n".join(prompts).lower()
    dump = any(m in blob for m in DUMP_MARKERS) or any(
        looks_like_dumped_equation(p) for p in prompts if p
    )
    if dump and "UNCLEAR" not in flags:
        flags.append("UNCLEAR")
    if dump and "LOW_VARIETY" not in flags:
        flags.append("LOW_VARIETY")
        if not why:
            why = "Old path looks like an equation-dump stub."
    # Variety: identical prompt skeleton across seeds at D=0 (ignore numbers).
    d0 = [re.sub(r"\d+", "N", r.get("prompt") or "") for r in sampled.get("rows") or [] if r.get("d") == 0 and r.get("prompt")]
    if len(d0) >= 2 and len(set(d0)) == 1 and "LOW_VARIETY" not in flags:
        # Many number types are same shape by design — only flag WP-ish generators.
        gen_wp = type_id.endswith("word_problems") or "markup" in type_id or "interest" in type_id
        if gen_wp:
            flags.append("LOW_VARIETY")
            if not why:
                why = "One template across seeds at D=0."
    return flags, why


def _has_openstax_notes(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "openstax.org" in text and "What old path actually produced" in text


def render_notes(entry, sampled: dict[str, Any]) -> str:
    type_id = entry.id
    meta = META.get(type_id) or {}
    flags, why = _flags_for(type_id, sampled)
    banner = ""
    if flags:
        banner = (
            f"> **{' / '.join(flags)}**"
            + (f" — {why}" if why else "")
            + "\n\n"
        )
    opt = sampled.get("opt_out") or {}
    opt_line = (
        f"Old-path extra settings: `{json.dumps(opt)}`."
        if opt
        else "No skeleton opt-out (old path is the live default)."
    )
    skel = "yes" if type_id in SKELETONED else "no"

    lines = [
        f"# `{type_id}` — {entry.name}",
        "",
        banner.rstrip(),
        "",
        f"- **Course:** Prealgebra (PA catalog)",
        f"- **Category:** {entry.category}",
        f"- **Generator:** `{entry.generator}`",
        f"- **Already on skeleton?** {skel}",
        f"- **{opt_line}**",
        "",
        "## What the question should look like (D=0 vs high D)",
        "",
        meta.get("should") or "Match old-path algebra shapes; copy OpenStax example shapes below.",
        "",
        "## What old path actually produced",
        "",
        "Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).",
        "",
    ]
    by_d: dict[float, list[dict[str, Any]]] = {}
    for row in sampled.get("rows") or []:
        by_d.setdefault(float(row["d"]), []).append(row)
    for d in DS:
        lines.append(f"### D={int(d) if d == int(d) else d}")
        lines.append("")
        for row in by_d.get(d, []):
            if row.get("error"):
                lines.append(f"- seed {row['seed']}: **ERROR** `{row['error']}`")
                continue
            extra = []
            if row.get("pattern"):
                extra.append(f"pattern=`{row['pattern']}`")
            if row.get("frame_id"):
                extra.append(f"frame=`{row['frame_id']}`")
            if row.get("has_figure"):
                extra.append("has_figure")
            tag = f" ({', '.join(extra)})" if extra else ""
            lines.append(f"- seed {row['seed']}{tag}:")
            lines.append(f"  - prompt: `{_clip(row.get('prompt') or '')}`")
            if row.get("answer"):
                lines.append(f"  - answer: `{_clip(str(row['answer']), 200)}`")
        lines.append("")

    if sampled.get("errors"):
        lines.append("Generation errors:")
        for e in sampled["errors"]:
            lines.append(f"- {e}")
        lines.append("")

    lines.extend(["## OpenStax examples + chapter/section cites", ""])
    cites = meta.get("cites") or []
    if not cites:
        lines.append("**UNCLEAR** — no OpenStax PA/EA cite mapped yet.")
        lines.append("")
    for c in cites:
        lines.append(f"### {c['book']} — {c['section']}")
        lines.append("")
        lines.append(f"- {c['url']}")
        examples = _extract_examples(c["mine"]) if c.get("mine") else []
        if examples:
            lines.append("- Mined examples:")
            for ex in examples:
                lines.append(f"  - {ex}")
        for extra in c.get("extra") or []:
            lines.append(f"- Shape: {extra}")
        if not examples and not c.get("extra"):
            lines.append("- (no local mine items; use the section URL)")
        lines.append("")

    lines.extend(
        [
            "## Variety notes",
            "",
            why or "Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.",
            "",
            "## Proposed engine (reuse vs new)",
            "",
            meta.get("engine") or "TBD after samples — do not implement in this pass.",
            "",
            "_Proposal only. No engine implementation in this notes pass._",
            "",
        ]
    )
    # Drop extra blank from empty banner
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "pa_type_count": len(CATALOG),
        "written": [],
        "skipped": [],
        "unclear": [],
        "low_variety": [],
        "errors": {},
    }
    all_samples: dict[str, Any] = {}
    for entry in CATALOG:
        path = OUT / f"{entry.id}.md"
        if _has_openstax_notes(path):
            summary["skipped"].append(entry.id)
            continue
        sampled = sample_type(entry.id)
        all_samples[entry.id] = {
            "name": entry.name,
            "generator": entry.generator,
            **sampled,
        }
        flags, _why = _flags_for(entry.id, sampled)
        if "UNCLEAR" in flags:
            summary["unclear"].append(entry.id)
        if "LOW_VARIETY" in flags:
            summary["low_variety"].append(entry.id)
        if sampled.get("errors"):
            summary["errors"][entry.id] = sampled["errors"]
        path.write_text(render_notes(entry, sampled), encoding="utf-8")
        summary["written"].append(entry.id)
        print(f"wrote {entry.id} flags={flags}", flush=True)

    (OUT / "_pa_samples.json").write_text(
        json.dumps(all_samples, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "_pa_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in summary.items() if k != "errors"}, indent=2))
    print("unclear:", summary["unclear"])
    print("low_variety:", summary["low_variety"])
    print("skipped:", summary["skipped"])


if __name__ == "__main__":
    main()
