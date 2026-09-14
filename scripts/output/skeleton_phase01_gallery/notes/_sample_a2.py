"""A2 steps 1–3 (non-equations/WP leaves): old-path samples + notes.md.

Writes ``notes/<type_id>.md``. Does not implement engines.
Skips types covered by the equations/WP agent and files that already have
openstax.org + old-path sections.
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
from question_engine.catalogs.algebra_1 import CATALOG as A1_CATALOG
from question_engine.catalogs.algebra_2 import CATALOG as A2_CATALOG
from question_engine.frameworks.primitives.wp_packaging import looks_like_dumped_equation

OUT = Path(__file__).resolve().parent
MINE_IA = _ROOT / "scripts/output/example_mining/intermediate-algebra-2e/stage1"
MINE_EA = _ROOT / "scripts/output/example_mining/elementary-algebra-2e/stage1"

DS = (0.0, 8.0, 16.0, 22.0)
SEEDS = (101, 207)

IA = "https://openstax.org/books/intermediate-algebra-2e/pages"
EA = "https://openstax.org/books/elementary-algebra-2e/pages"
CA = "https://openstax.org/books/college-algebra-2e/pages"

DUMP_MARKERS = (
    "the equation is",
    "giving $",
    "satisfy $",
    "reduces to $",
    "uses a proportion",
    "the system is",
    "the costs satisfy",
)

# Equations / WP / systems-solving agent scope — do not duplicate here.
EQ_WP_EXCLUDE: set[str] = {
    e.id for e in A2_CATALOG if e.id.startswith("a2_equations_and_inequalities_")
} | {
    "a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities",
    "a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables",
    "a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables",
    "a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables",
    "a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables",
    "a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_graphing",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square",
    "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula",
    "a2_polynomial_functions_solving_polynomial_equations",
    "a2_radical_functions_and_rational_exponents_radical_equations",
    "a2_radical_functions_and_rational_exponents_rational_exponent_equations",
    "a2_rational_expressions_equations",
    "a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms",
    "a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms",
    "a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple",
    "a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard",
    "a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems",
    "a2_exponential_and_logarithmic_expressions_continuous_exponential_growth_and_decay_word_problems",
    "a2_conic_sections_systems_of_quadratic_equations",
    "a2_trigonometry_equations",
    "a2_matrices_cramers_rule",
    "a2_matrices_equations",
    "a2_probability_and_statistics_probability_of_independent_and_dependent_events_word_problems",
    "a2_probability_and_statistics_probability_of_mutually_exclusive_events_word_problems",
}

# Opt-out flags for the *old* path when a skeleton exists (by generator name).
OPT_OUT_BY_GENERATOR: dict[str, dict[str, Any]] = {
    "expand_simplify": {"use_sample_distributive": True},
    "polynomial_add_subtract": {"use_sample_polynomial_add_subtract": True},
    "simplify_polynomials": {"use_sample_expand_simplify": True},
    "polynomial_multiply": {"use_factor_poly": True},
    "polynomial_multiply_special": {"use_factor_poly": True},
    "polynomial_factoring_grouping": {"use_factor_poly": True},
    "quadratic_factoring": {"use_factor_poly": True},
    "polynomial_factoring_special_cases": {"use_factor_poly": True},
    "a2_polynomial_functions_factoring_sum_difference_of_cubes": {"use_factor_poly": True},
    "a2_polynomial_functions_factoring_quadratic_form": {"use_factor_poly": True},
    "a2_polynomial_functions_factoring_all_techniques": {"use_factor_poly": True},
    "quadratic_factoring_equations": {"use_factor_poly": True},
    "rational_simplification": {"use_constructive_rational": True},
    "rational_expression_simplification": {"use_constructive_rational": True},
    "rational_expression_multiply_divide": {"use_hand_muldiv": True},
    "complex_fractions": {"use_hand_complex_frac": True},
    "rational_equations": {"use_hand_rational_equations": True},
    "exponential_growth_decay": {"use_legacy_exponential_growth": True},
}

# Gallery skeleton aliases (type_id → slug) from gen_examples SECTIONS.
_SKELETON_ALIASES: dict[str, str] = {}
try:
    from scripts.output.skeleton_phase01_gallery import gen_examples as _ge

    for sec in _ge.SECTIONS:
        tid = sec.get("type_id") or ""
        slug = sec.get("slug") or ""
        if tid and slug:
            _SKELETON_ALIASES[tid] = slug
        for alias in sec.get("aliases") or []:
            _SKELETON_ALIASES[str(alias)] = slug
except Exception:  # noqa: BLE001
    pass

A1_BY_GENERATOR: dict[str, list[str]] = {}
for _e in A1_CATALOG:
    A1_BY_GENERATOR.setdefault(_e.generator, []).append(_e.id)

# Per-type overrides (skill text, forced flags, extra cites).
META: dict[str, dict[str, Any]] = {
    "a2_beginning_algebra_order_of_operations": {
        "skill": "Evaluate a numeric expression using order of operations.",
        "d0": "Four ops, no nested parens; small ints.",
        "high": "Nested parens / exponents; larger operands.",
        "must_not": "Algebraic variables; equation solving.",
        "a1_alias": "order_of_operations",
        "force_flags": [],
    },
    "a2_beginning_algebra_simplifying_algebraic_expressions": {
        "skill": "Expand and simplify an algebraic expression (distribute, combine).",
        "d0": r"$2(x+3)$ or $3x+2x$.",
        "high": "Two binomials; more terms before simplify.",
        "must_not": "Solve equations; factor-only prompts.",
        "a1_alias": None,
        "note": "A2 uses `expand_simplify`; A1 has `distributive_property` + `combining_like_terms` separately.",
    },
    "a2_polynomial_functions_naming": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Old path names by degree (quadratic/cubic) only; OpenStax also asks monomial/binomial/trinomial.",
        "a1_alias": "polynomial_naming",
    },
    "a2_polynomial_functions_dividing": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "OpenStax splits monomial ÷ poly (§5.4) vs long division (§5.5); one leaf mixes both.",
        "a1_alias": "polynomial_long_division",
    },
    "a2_quadratic_functions_and_inequalities_graphing_quadratic_functions": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Graph engine outside algebraic skeleton cores; verify against OpenStax §9.6–9.7.",
        "a1_alias": "graphing_quadratic_functions",
    },
    "a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Graph-shade skill; old path vs OpenStax IA §9.8 interval form not locked.",
        "a1_alias": "graphing_quadratic_inequalities",
    },
    "a2_polynomial_functions_graphing": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Uses `graph_quadratic` generator for general polynomial graphing — may not match degree>2 OpenStax shapes.",
        "a1_alias": "graph_quadratic",
    },
    "a2_rational_expressions_graphing": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Rational function graphing (asymptotes/holes) — no skeleton core yet.",
    },
    "a2_radical_functions_and_rational_exponents_graphing_radical_equations": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Graph radical functions — verify domain/range vs graph prompt.",
    },
    "a2_exponential_and_logarithmic_expressions_graphing_exponential_functions": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Graph exponential — transformations/base not locked to OpenStax §10.2.",
        "a1_alias": "graph_exponential",
    },
    "a2_exponential_and_logarithmic_expressions_graphing_logarithmic_functions": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Graph log — no algebraic skeleton; compare IA §10.3.",
    },
    "a2_trigonometry_graphing_trig_functions": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Trig graph transforms — College Algebra §7.6; old amplitude/period shapes TBD.",
    },
    "a2_conic_sections_parabolas_graphing_and_properties": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Conic graph/properties reuse quadratic graph engine — may not distinguish focus/directrix.",
    },
    "a2_conic_sections_circles_graphing_and_properties": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Circle graph vs standard form — College Algebra §11.1.",
    },
    "a2_conic_sections_ellipses_graphing_and_properties": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Ellipse graph engine TBD vs CA §11.2.",
    },
    "a2_conic_sections_hyperbolas_graphing_and_properties": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Hyperbola graph engine TBD vs CA §11.3.",
    },
    "a2_matrices_geometric_transformations": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Matrix transformation UX (apply 2×2 to polygon) — verify diagram fidelity.",
    },
    "a2_complex_numbers_graphing": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Complex plane graph — IA §8.8; old path may be identity-style.",
    },
    "a2_systems_of_equations_and_inequalities_points_in_three_dimensions": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "3D point identification — supplemental; sparse OpenStax IA coverage.",
    },
    "a2_systems_of_equations_and_inequalities_planes": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Plane identification in 3D — supplemental skill.",
    },
    "a2_polynomial_functions_descartes_rule_of_signs": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Sign-variation rule — verify prompt asks for sign changes vs root count.",
    },
    "a2_polynomial_functions_fundamental_theorem_of_algebra": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Find all zeros (including complex) — degree and method mix TBD.",
    },
    "a2_polynomial_functions_conjugate_roots_and_factoring": {
        "a1_alias": "polynomial_factoring_special_cases",
        "note": "Same generator as A1 special cases; A2 expects conjugate-pair / complex roots context.",
    },
    "a2_polynomial_functions_conjugate_roots_and_writing_functions": {
        "force_flags": ["UNCLEAR"],
        "flag_why": "Write poly from conjugate roots — A2-only generator `polynomial_conjugate_writing`.",
    },
    "a2_polynomial_functions_factoring_all_techniques": {
        "note": "A2 mixer pool may include cubes/grouping beyond A1 general strategy.",
        "a1_alias": "polynomial_factoring_general_strategy",
    },
    "a2_polynomial_functions_factoring_sum_difference_of_cubes": {
        "note": "A2-only generator; A1 has no dedicated cubes leaf.",
    },
    "a2_polynomial_functions_factoring_quadratic_form": {
        "note": "A2-only generator (substitution $u=x^2$); A1 has no twin.",
    },
    "a2_direct_and_inverse_variation_direct_and_inverse_variation": {
        "a1_alias": "direct_inverse_variation",
    },
    "a2_relations_and_introduction_to_functions_discrete_relations": {
        "a1_alias": "discrete_relations",
    },
    "a2_relations_and_introduction_to_functions_continuous_relations": {
        "a1_alias": "continuous_relations",
    },
    "a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions": {
        "a1_alias": "evaluating_graphing_functions",
    },
    "a2_linear_relations_and_functions_graphing_linear_equations": {
        "a1_alias": "graph_linear_equation",
    },
    "a2_linear_relations_and_functions_writing_linear_equations": {
        "a1_alias": "writing_linear_equations",
    },
    "a2_linear_relations_and_functions_graphing_absolute_value_equations": {
        "a1_alias": "graph_absolute_value",
    },
    "a2_linear_relations_and_functions_graphing_linear_inequalities": {
        "a1_alias": "graph_linear_inequality",
    },
    "a2_radical_functions_and_rational_exponents_simplifying_radicals": {
        "a1_alias": "radical_simplification",
    },
    "a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions": {
        "a1_alias": "radical_add_subtract",
    },
    "a2_radical_functions_and_rational_exponents_multiplying_radical_expressions": {
        "a1_alias": "radical_multiply",
    },
    "a2_radical_functions_and_rational_exponents_dividing_radical_expressions": {
        "a1_alias": "radical_divide",
    },
    "a2_rational_expressions_simplifying": {
        "a1_alias": "rational_simplification",
    },
    "a2_rational_expressions_multiplying_and_dividing": {
        "a1_alias": "rational_expression_multiply_divide",
    },
    "a2_rational_expressions_adding_and_subtracting": {
        "a1_alias": "rational_expression_simplification",
    },
    "a2_rational_expressions_complex_fractions": {
        "note": "A2-only catalog id; shares `complex_fractions` generator with no A1 twin.",
    },
    "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions": {
        "a1_alias": "quadratic_factoring",
    },
    "a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions": {
        "a1_alias": "polynomial_factoring_special_cases",
    },
    "a2_quadratic_functions_and_inequalities_completing_the_square": {
        "a1_alias": "quadratic_completing_square_constant",
    },
    "a2_quadratic_functions_and_inequalities_the_discriminant": {
        "a1_alias": "quadratic_discriminant",
    },
    "a2_polynomial_functions_adding_and_subtracting": {
        "a1_alias": "polynomial_add_subtract",
    },
    "a2_polynomial_functions_multiplying": {
        "a1_alias": "polynomial_multiply",
    },
    "a2_polynomial_functions_multiplying_special_cases": {
        "a1_alias": "polynomial_multiply_special",
    },
    "a2_polynomial_functions_factoring_by_grouping": {
        "a1_alias": "polynomial_factoring_grouping",
    },
    "a2_polynomial_functions_simplifying": {
        "a1_alias": "simplify_polynomials",
    },
}

# Default OpenStax cites by A2 category (paraphrase shapes only).
CATEGORY_CITES: dict[str, list[tuple[str, str, str, str | None]]] = {
    "Algebra 2 — Beginning Algebra": [
        ("Intermediate Algebra 2e", "1.1 Use the Language of Algebra", "1-1-use-the-language-of-algebra", None),
        ("Intermediate Algebra 2e", "5.2 Properties of Exponents and Scientific Notation", "5-2-properties-of-exponents-and-scientific-notation", "5-2-properties-of-exponents-and-scientific-notation.json"),
    ],
    "Algebra 2 — Relations and Introduction to Functions": [
        ("Intermediate Algebra 2e", "3.5 Graphs of Functions", "3-5-graphs-of-functions", None),
        ("Intermediate Algebra 2e", "3.6 Graphs of Functions", "3-6-graphs-of-functions", None),
    ],
    "Algebra 2 — Linear Relations and Functions": [
        ("Intermediate Algebra 2e", "3.1 Use a General Strategy to Solve Linear Equations", "3-1-use-a-general-strategy-to-solve-linear-equations", "2-1-use-a-general-strategy-to-solve-linear-equations.json"),
        ("Intermediate Algebra 2e", "3.4 Graph Linear Equations in Two Variables", "3-4-graph-linear-equations-in-two-variables", None),
    ],
    "Algebra 2 — Direct and Inverse Variation": [
        ("Intermediate Algebra 2e", "3.7 Variation", "3-7-variation", None),
    ],
    "Algebra 2 — Systems of Equations and Inequalities": [
        ("Intermediate Algebra 2e", "4.1 Use the Rectangular Coordinate System", "4-1-use-the-rectangular-coordinate-system", None),
    ],
    "Algebra 2 — Matrices": [
        ("College Algebra 2e", "7.5 Matrices and Matrix Operations", "7-5-matrices-and-matrix-operations", None),
        ("College Algebra 2e", "7.6 Solving Systems with Gaussian Elimination", "7-6-solving-systems-with-gaussian-elimination", None),
    ],
    "Algebra 2 — Complex Numbers": [
        ("Intermediate Algebra 2e", "8.8 Use the Complex Number System", "8-8-use-the-complex-number-system", "8-8-use-the-complex-number-system.json"),
    ],
    "Algebra 2 — Quadratic Functions and Inequalities": [
        ("Intermediate Algebra 2e", "9.6 Graph Quadratic Functions Using Properties", "9-6-graph-quadratic-functions-using-properties", "9-6-graph-quadratic-functions-using-properties.json"),
        ("Intermediate Algebra 2e", "9.2 Solve Quadratic Equations by Completing the Square", "9-2-solve-quadratic-equations-by-completing-the-square", "9-2-solve-quadratic-equations-by-completing-the-square.json"),
    ],
    "Algebra 2 — Polynomial Functions": [
        ("Intermediate Algebra 2e", "5.1 Add and Subtract Polynomials", "5-1-add-and-subtract-polynomials", "5-1-add-and-subtract-polynomials.json"),
        ("Intermediate Algebra 2e", "5.3 Multiply Polynomials", "5-3-multiply-polynomials", "5-3-multiply-polynomials.json"),
        ("Intermediate Algebra 2e", "5.4 Divide Polynomials", "5-4-dividing-polynomials", "5-4-dividing-polynomials.json"),
        ("Intermediate Algebra 2e", "6.4 General Strategy for Factoring Polynomials", "6-4-general-strategy-for-factoring-polynomials", "6-4-general-strategy-for-factoring-polynomials.json"),
    ],
    "Algebra 2 — General Functions": [
        ("Intermediate Algebra 2e", "10.1 Finding Composite and Inverse Functions", "10-1-finding-composite-and-inverse-functions", "10-1-finding-composite-and-inverse-functions.json"),
    ],
    "Algebra 2 — Radical Functions and Rational Exponents": [
        ("Intermediate Algebra 2e", "8.1 Simplify Expressions with Roots", "8-1-simplify-expressions-with-roots", "8-1-simplify-expressions-with-roots.json"),
        ("Intermediate Algebra 2e", "8.2 Simplify Radical Expressions", "8-2-simplify-radical-expressions", "8-2-simplify-radical-expressions.json"),
        ("Intermediate Algebra 2e", "8.3 Simplify Rational Exponents", "8-3-simplify-rational-exponents", "8-3-simplify-rational-exponents.json"),
    ],
    "Algebra 2 — Conic Sections": [
        ("College Algebra 2e", "11.1 Distance and Midpoint Formulas; Circles", "11-1-distance-and-midpoint-formulas-circles", None),
        ("College Algebra 2e", "11.2 Parabolas", "11-2-parabolas", None),
        ("College Algebra 2e", "11.3 Ellipses", "11-3-ellipses", None),
        ("College Algebra 2e", "11.4 Hyperbolas", "11-4-hyperbolas", None),
    ],
    "Algebra 2 — Rational Expressions": [
        ("Intermediate Algebra 2e", "7.1 Multiply and Divide Rational Expressions", "7-1-multiply-and-divide-rational-expressions", "7-1-multiply-and-divide-rational-expressions.json"),
        ("Intermediate Algebra 2e", "7.2 Add and Subtract Rational Expressions", "7-2-add-and-subtract-rational-expressions", "7-2-add-and-subtract-rational-expressions.json"),
        ("Intermediate Algebra 2e", "7.3 Simplify Complex Rational Expressions", "7-3-simplify-complex-rational-expressions", "7-3-simplify-complex-rational-expressions.json"),
    ],
    "Algebra 2 — Exponential and Logarithmic Expressions": [
        ("Intermediate Algebra 2e", "10.2 Evaluate and Graph Exponential Functions", "10-2-evaluate-and-graph-exponential-functions", "10-2-evaluate-and-graph-exponential-functions.json"),
        ("Intermediate Algebra 2e", "10.3 Evaluate and Graph Logarithmic Functions", "10-3-evaluate-and-graph-logarithmic-functions", "10-3-evaluate-and-graph-logarithmic-functions.json"),
        ("Intermediate Algebra 2e", "10.4 Use the Properties of Logarithms", "10-4-use-the-properties-of-logarithms", "10-4-use-the-properties-of-logarithms.json"),
    ],
    "Algebra 2 — Sequences and Series": [
        ("College Algebra 2e", "9.1 Sequences and Their Notations", "9-1-sequences-and-their-notations", None),
        ("College Algebra 2e", "9.3 Geometric Sequences", "9-3-geometric-sequences", None),
        ("College Algebra 2e", "9.4 Series and Their Notations", "9-4-series-and-their-notations", None),
    ],
    "Algebra 2 — Trigonometry": [
        ("College Algebra 2e", "5.1 Angles", "5-1-angles", None),
        ("College Algebra 2e", "7.1 Right Triangle Trigonometry", "7-1-right-triangle-trigonometry", None),
        ("College Algebra 2e", "7.2 Non-right Triangles: Law of Sines", "7-2-non-right-triangles-law-of-sines", None),
    ],
    "Algebra 2 — Probability and Statistics": [
        ("College Algebra 2e", "13.1 Counting Principles", "13-1-counting-principles", None),
        ("College Algebra 2e", "13.2 Probability", "13-2-probability", None),
    ],
}


def _targets() -> list[Any]:
    return [e for e in A2_CATALOG if e.id not in EQ_WP_EXCLUDE]


def _opt_out_for(entry) -> dict[str, Any]:
    meta = META.get(entry.id) or {}
    if meta.get("opt_out") is not None:
        return dict(meta["opt_out"])
    return dict(OPT_OUT_BY_GENERATOR.get(entry.generator) or {})


def _a1_alias(entry) -> str | None:
    meta = META.get(entry.id) or {}
    if "a1_alias" in meta:
        val = meta.get("a1_alias")
        return val if val else None
    hits = A1_BY_GENERATOR.get(entry.generator) or []
    return hits[0] if len(hits) == 1 else None


def _mine_path(fname: str) -> Path | None:
    for root in (MINE_IA, MINE_EA):
        p = root / fname
        if p.exists():
            return p
    return None


def _extract_examples(fname: str, limit: int = 3) -> list[str]:
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
        if len(prompt) > 200:
            prompt = prompt[:197] + "…"
        if title and prompt:
            out.append(f"{title}: {prompt}")
        elif prompt:
            out.append(prompt)
        if len(out) >= limit:
            break
    return out


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


def sample_type(type_id: str, extra: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
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
                rows.append(
                    {
                        "d": d,
                        "seed": seed,
                        "prompt": q.prompt_latex or q.prompt_text or "",
                        "answer": q.answer_latex or "",
                        "pattern": meta.get("skeleton_pattern") or "",
                        "form_id": meta.get("form_id") or "",
                        "has_figure": bool(
                            meta.get("figure")
                            or meta.get("diagram")
                            or meta.get("coordinate_plane")
                        ),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                rows.append({"d": d, "seed": seed, "error": str(exc)})
    return rows


def _flags_for(entry, sampled: list[dict[str, Any]], a1_rows: list[dict[str, Any]] | None) -> tuple[list[str], str]:
    meta = META.get(entry.id) or {}
    flags = list(meta.get("force_flags") or [])
    why = str(meta.get("flag_why") or "")

    prompts = [str(r.get("prompt") or "") for r in sampled if not r.get("error")]
    blob = "\n".join(prompts).lower()
    if any(m in blob for m in DUMP_MARKERS) or any(looks_like_dumped_equation(p) for p in prompts if p):
        if "UNCLEAR" not in flags:
            flags.append("UNCLEAR")
        if "LOW_VARIETY" not in flags:
            flags.append("LOW_VARIETY")
        if not why:
            why = "Old path looks like an equation-dump stub."

    d0 = [
        re.sub(r"\d+", "N", r.get("prompt") or "")
        for r in sampled
        if r.get("d") == 0 and r.get("prompt")
    ]
    if len(d0) >= 2 and len(set(d0)) == 1 and "LOW_VARIETY" not in flags:
        flags.append("LOW_VARIETY")
        if not why:
            why = "One template across seeds at D=0."

    if a1_rows:
        diffs = 0
        for a2r, a1r in zip(sampled, a1_rows, strict=False):
            if a2r.get("error") or a1r.get("error"):
                continue
            if (a2r.get("prompt") or "").strip() != (a1r.get("prompt") or "").strip():
                diffs += 1
        if diffs == 0 and len(sampled) >= 2:
            pass  # identical — documented in alias section, not a flag
        elif diffs > 0 and "UNCLEAR" not in flags:
            flags.append("UNCLEAR")
            if not why:
                why = "A2 type_id samples differ from A1 alias at same D/seeds — verify intended divergence."

    return flags, why


def _has_filled_notes(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "openstax.org" in text and "What old path actually produced" in text


def _engine_family(entry) -> str:
    cat = entry.category
    gen = entry.generator
    if "word" in entry.name.lower():
        return "wp"
    if gen.startswith("wp_"):
        return "wp"
    if "graph" in gen or "graphing" in entry.name.lower():
        return "other"
    if gen in {
        "order_of_operations",
        "complex_operations",
        "matrix_operations",
        "stats_counting_principle",
    }:
        return "number"
    if gen in {"expand_simplify", "simplify_polynomials"}:
        return "affine"
    if "polynomial" in gen or "quadratic" in gen or "binomial" in gen:
        return "other"
    if "rational" in gen or "complex_frac" in gen:
        return "other"
    if "radical" in gen or "properties_of_exponents" in gen:
        return "other"
    if "log_" in gen or "exponential" in gen or "inverse_exponential" in gen:
        return "other"
    if gen.startswith("sequence_") or "law_of" in gen or gen.startswith("trig_") or gen.startswith("geo_"):
        return "other"
    if "conic" in gen:
        return "other"
    if "function" in gen:
        return "other"
    if "direct_inverse" in gen:
        return "proportion"
    if "relation" in gen or "evaluating_graphing" in gen:
        return "other"
    if "matrix" in gen:
        return "other"
    if "stats_" in gen:
        return "other"
    return "other"


def render_notes(entry, sampled: list[dict[str, Any]], a1_rows: list[dict[str, Any]] | None, a1_id: str | None) -> str:
    meta = META.get(entry.id) or {}
    opt = _opt_out_for(entry)
    flags, why = _flags_for(entry, sampled, a1_rows)
    banner = ""
    if flags:
        banner = f"> **{' / '.join(flags)}**" + (f" — {why}" if why else "") + "\n\n"

    skill = meta.get("skill") or f"Practice {entry.name.lower()} (catalog: {entry.generator})."
    d0 = meta.get("d0") or "As simple as old easy at D=0 — copy live samples below."
    high = meta.get("high") or "Numeric hardness first; format unlocks by D≈16–22."
    must_not = meta.get("must_not") or "Wrong-topic shapes; equation dumps in story leaves."

    opt_desc = json.dumps(opt) if opt else "(none — live default is old path)"
    skeleton_slug = _SKELETON_ALIASES.get(entry.id)
    on_skeleton = "yes" if skeleton_slug else "no"

    lines = [
        f"# Notes — `{entry.id}`",
        "",
        banner.rstrip(),
        "",
        f"- **Display name:** {entry.name}",
        f"- **Category:** {entry.category}",
        f"- **Generator:** `{entry.generator}`",
        f"- **Already on skeleton?** {on_skeleton}" + (f" (`{skeleton_slug}`)" if skeleton_slug else ""),
        f"- **Suggested family:** `{_engine_family(entry)}`",
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
        f"Live `_generate_for_type` with opt-out `{opt_desc}`.",
        "",
        "| D | seed | prompt_latex | answer_latex | shape notes |",
        "|---|------|--------------|--------------|-------------|",
    ]
    for row in sampled:
        d = row["d"]
        dlab = int(d) if d == int(d) else d
        if row.get("error"):
            lines.append(f"| {dlab} | {row['seed']} | **ERROR** | | `{_clip(row['error'], 120)}` |")
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

    lines.extend(["", f"Opt-out flag used: `{opt_desc}`", ""])

    if a1_id:
        lines.extend(
            [
                "## A1 alias comparison",
                "",
                f"- **A1 catalog twin:** `{a1_id}` (same generator `{entry.generator}` unless noted).",
            ]
        )
        if meta.get("note"):
            lines.append(f"- **Note:** {meta['note']}")
        if a1_rows:
            same = sum(
                1
                for a2r, a1r in zip(sampled, a1_rows, strict=False)
                if not a2r.get("error")
                and not a1r.get("error")
                and (a2r.get("prompt") or "").strip() == (a1r.get("prompt") or "").strip()
            )
            total = sum(1 for r in sampled if not r.get("error"))
            if same == total and total > 0:
                lines.append("- **Old path vs A1:** Identical prompts at all sampled D/seeds (shared generator).")
            else:
                lines.append("- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.")
                for a2r, a1r in zip(sampled, a1_rows, strict=False):
                    if a2r.get("error") or a1r.get("error"):
                        continue
                    if (a2r.get("prompt") or "").strip() != (a1r.get("prompt") or "").strip():
                        lines.append(
                            f"  - D={a2r['d']} seed={a2r['seed']}: A2 `{_clip(a2r.get('prompt') or '', 80)}` "
                            f"≠ A1 `{_clip(a1r.get('prompt') or '', 80)}`"
                        )
        else:
            lines.append("- **Old path vs A1:** Not re-sampled (multiple A1 hits for this generator).")
        lines.append("")

    lines.extend(
        [
            "## OpenStax examples + chapter/section cites",
            "",
            "Paraphrase stems; cite book + chapter/section + URL.",
            "",
            "| Cite | URL | What to copy (shape / frame, not wording) |",
            "|------|-----|-------------------------------------------|",
        ]
    )
    cites = CATEGORY_CITES.get(entry.category) or [
        ("Intermediate Algebra 2e", entry.category.replace("Algebra 2 — ", ""), "", None)
    ]
    for book, section, slug, mine in cites[:3]:
        if book.startswith("College"):
            url = f"{CA}/{slug}" if slug else CA
        elif book.startswith("Elementary"):
            url = f"{EA}/{slug}" if slug else EA
        else:
            url = f"{IA}/{slug}" if slug else IA
        shape = section
        if mine:
            ex = _extract_examples(mine, limit=2)
            if ex:
                shape += " — e.g. " + "; ".join(ex[:2])
        lines.append(f"| {book} §{section.split(' ', 1)[0]} | {url} | {shape} |")

    lines.extend(
        [
            "",
            "Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.",
            "",
            "## Variety notes / UNCLEAR flag",
            "",
        ]
    )
    if why:
        lines.append(why)
    else:
        lines.append("Not a WP leaf unless the generator is story-based. Algebra shapes follow old path samples above.")
    if flags:
        lines.append(f"Flags: {', '.join(f'`{f}`' for f in flags)}.")
    lines.extend(
        [
            "",
            "## Proposed engine (reuse vs new) — proposal only",
            "",
        ]
    )
    if skeleton_slug:
        lines.append(f"- **Reuse:** Existing skeleton slug `{skeleton_slug}` / shared `{entry.generator}` family.")
    elif a1_id:
        lines.append(f"- **Reuse:** Share A1 `{a1_id}` generator; wire A2 catalog id when skeleton lands.")
    else:
        lines.append(f"- **Reuse:** Existing `{entry.generator}` hand path until a skeleton exists.")
    lines.extend(
        [
            "- **New:** only if no honest match — leave leaf and document skip.",
            "- **Not this pass:** notes only; no generator implementation.",
            "",
            f"_Catalog generator `{entry.generator}`; equations/WP agent owns solve/WP siblings._",
            "",
        ]
    )
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def build_index(summary: dict[str, Any]) -> str:
    lines = [
        "# Algebra 2 type index (non-equations/WP notes pass)",
        "",
        "Steps 1–3 only: old-path samples, OpenStax cites, proposed engine.",
        "Equations, inequalities, systems-solving, and WP leaves are owned by the eq/WP agent.",
        "",
        f"| Metric | Count |",
        f"|---|---:|",
        f"| A2 catalog leaves | {len(A2_CATALOG)} |",
        f"| Excluded (eq/WP agent) | {len(EQ_WP_EXCLUDE)} |",
        f"| This pass (targets) | {len(_targets())} |",
        f"| Notes written | {len(summary.get('written', []))} |",
        f"| Skipped (already filled) | {len(summary.get('skipped', []))} |",
        f"| UNCLEAR flagged | {len(summary.get('unclear', []))} |",
        f"| LOW_VARIETY flagged | {len(summary.get('low_variety', []))} |",
        "",
        "## UNCLEAR / LOW_VARIETY",
        "",
    ]
    for tid in sorted(summary.get("unclear", [])):
        flags = summary.get("flags", {}).get(tid, [])
        lines.append(f"- `{tid}` — {', '.join(flags)}")
    if not summary.get("unclear"):
        lines.append("- _(none)_")
    lines.extend(["", "## Notes files", ""])
    for tid in sorted(summary.get("written", [])):
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
        opt = _opt_out_for(entry)
        sampled = sample_type(entry.id, opt)
        a1_id = _a1_alias(entry)
        a1_rows = sample_type(a1_id, opt) if a1_id else None
        flags, _ = _flags_for(entry, sampled, a1_rows)
        summary["flags"][entry.id] = flags
        if "UNCLEAR" in flags:
            summary["unclear"].append(entry.id)
        if "LOW_VARIETY" in flags:
            summary["low_variety"].append(entry.id)
        errs = [r["error"] for r in sampled if r.get("error")]
        if errs:
            summary["errors"][entry.id] = errs
        path.write_text(render_notes(entry, sampled, a1_rows, a1_id), encoding="utf-8")
        summary["written"].append(entry.id)
        print(f"wrote {entry.id} flags={flags}", flush=True)

    (OUT / "_a2_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (OUT / "A2_INDEX.md").write_text(build_index(summary), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in summary.items() if k not in ("errors", "flags")},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
