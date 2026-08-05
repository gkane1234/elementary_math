"""Continuous-D migration smoke tests for newly migrated profiles."""

from __future__ import annotations

import question_engine.types  # noqa: F401 — register catalog types
from question_engine.core.base import QUESTION_TYPES
from question_engine.frameworks.number import (
    PercentFramework,
    RationalFramework,
    ScientificNotationFramework,
    _sci_continuous_knobs,
    _sci_exp_bounds,
)
from question_engine.generators.advanced import _writing_numeric_complexity_from_continuous
from question_engine.generators.misc import _exponent_bounds_from_continuous


def _has_continuous_difficulty(type_id: str) -> bool:
    qt = QUESTION_TYPES[type_id]
    fields = qt.settings_schema()
    return any(
        getattr(f, "key", None) == "difficulty"
        and getattr(f, "type", None) in {"int", "float", "number", "range"}
        for f in fields
    )


def test_scientific_notation_types_expose_continuous_difficulty():
    for type_id in (
        "scientific_notation_write",
        "scientific_notation_operations",
        "scientific_notation_add_subtract",
    ):
        assert type_id in QUESTION_TYPES
        assert _has_continuous_difficulty(type_id)


def test_writing_numeric_and_verbal_expose_continuous_difficulty():
    for type_id in (
        "g6_writing_numeric_expressions",
        "verbal_expressions",
        "g6_writing_algebraic_expressions",
    ):
        assert type_id in QUESTION_TYPES
        assert _has_continuous_difficulty(type_id)


def test_a1_number_percent_types_expose_continuous_difficulty():
    for type_id in (
        "rational_add_subtract",
        "rational_multiply",
        "rational_divide",
        "percents",
        "percent_of_change",
    ):
        assert type_id in QUESTION_TYPES
        assert _has_continuous_difficulty(type_id)


def test_a1_polynomial_and_exponents_expose_continuous_difficulty():
    for type_id in (
        "polynomial_naming",
        "polynomial_add_subtract",
        "simplify_polynomials",
        "polynomial_multiply",
        "properties_of_exponents",
    ):
        assert type_id in QUESTION_TYPES
        assert _has_continuous_difficulty(type_id)


def test_a1_ea2e_followup_types_expose_continuous_difficulty():
    """Slope / systems / factoring ladder must expose continuous ``difficulty``."""
    for type_id in (
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
    ):
        assert type_id in QUESTION_TYPES
        assert _has_continuous_difficulty(type_id), type_id


def test_a1_inequality_literal_types_expose_continuous_difficulty():
    """Literals / inequality ladder / abs value must expose continuous ``difficulty``."""
    for type_id in (
        "literal_equations",
        "one_step_inequalities",
        "two_step_inequalities",
        "multi_step_inequalities",
        "compound_inequalities",
        "absolute_value_equations",
        "absolute_value_inequalities",
        "rational_expression_multiply_divide",
        "radical_add_subtract",
    ):
        assert type_id in QUESTION_TYPES
        assert _has_continuous_difficulty(type_id), type_id


def test_a1_quadratic_radical_rational_eq_expose_continuous_difficulty():
    """Quadratic methods / radical ×÷ eqns / rational eqns expose continuous D."""
    for type_id in (
        "quadratic_square_roots",
        "quadratic_completing_square_constant",
        "quadratic_completing_square_solve",
        "quadratic_formula",
        "quadratic_discriminant",
        "radical_multiply",
        "radical_divide",
        "radical_equations",
        "rational_expressions_equations",
    ):
        assert type_id in QUESTION_TYPES
        assert _has_continuous_difficulty(type_id), type_id


def test_a1_orphan_wp_graph_expose_continuous_difficulty():
    """Catalog orphans + WP + prompt-graph leaves expose continuous D."""
    for type_id in (
        "polynomial_long_division",
        "radical_simplification",
        "mixture_word_problems",
        "distance_rate_time_word_problems",
        "work_word_problems",
        "evaluating_graphing_functions",
        "graphing_linear_equations",
    ):
        assert type_id in QUESTION_TYPES
        assert _has_continuous_difficulty(type_id), type_id


def test_a1_orphan_wp_generate_at_continuous_d():
    """Live generate path for newly wired orphans + narrative WP."""
    for type_id in (
        "polynomial_long_division",
        "radical_simplification",
        "mixture_word_problems",
        "distance_rate_time_word_problems",
        "work_word_problems",
    ):
        qt = QUESTION_TYPES[type_id]
        for d in (0, 12, 22):
            qs = qt.generate({"difficulty": d, "count": 1, "include_answer_key": True})
            assert len(qs) == 1
            assert (qs[0].prompt_latex or qs[0].prompt_text or "").strip()


def test_a1_quadratic_radical_rational_eq_generate_at_continuous_d():
    """Live generate path for new EA2e Ch 8–10 effort types."""
    for type_id in (
        "quadratic_square_roots",
        "quadratic_formula",
        "radical_multiply",
        "radical_equations",
        "rational_expressions_equations",
    ):
        qt = QUESTION_TYPES[type_id]
        for d in (0, 12, 22):
            qs = qt.generate({"difficulty": d, "count": 1, "include_answer_key": True})
            assert len(qs) == 1
            assert (qs[0].prompt_latex or qs[0].prompt_text or "").strip()


def test_a1_form_ladders_unlock_via_api_resolve():
    """Continuous D must unlock EMH form toggles (defaults must not freeze easy mode)."""
    from question_engine.api.handler import _resolve_generation_settings

    easy = _resolve_generation_settings(
        "radical_multiply", {"difficulty": 0, "count": 1}
    )
    hard = _resolve_generation_settings(
        "radical_multiply", {"difficulty": 22, "count": 1}
    )
    assert easy.get("allow_simple_product") is True
    assert hard.get("allow_binomial_product") is True

    rq_easy = _resolve_generation_settings(
        "rational_expressions_equations", {"difficulty": 0, "count": 1}
    )
    rq_hard = _resolve_generation_settings(
        "rational_expressions_equations", {"difficulty": 22, "count": 1}
    )
    assert rq_easy.get("allow_simple_fraction") is True
    assert rq_hard.get("allow_two_fractions") is True

    sq_easy = _resolve_generation_settings(
        "quadratic_square_roots", {"difficulty": 0, "count": 1}
    )
    sq_hard = _resolve_generation_settings(
        "quadratic_square_roots", {"difficulty": 22, "count": 1}
    )
    assert sq_easy.get("allow_isolated") is True
    assert sq_hard.get("allow_complete_square") is True


def test_sci_continuous_knobs_widen_with_d():
    assert _sci_continuous_knobs({"difficulty_tier": "hard"}) is None
    easy = _sci_continuous_knobs({"difficulty": 0})
    mid = _sci_continuous_knobs({"difficulty": 10})
    hard = _sci_continuous_knobs({"difficulty": 22})
    assert easy is not None and mid is not None and hard is not None
    assert easy["allow_negative_exponents"] is False
    assert mid["allow_negative_exponents"] is True
    lo0, hi0 = _sci_exp_bounds({"difficulty": 0})
    lo20, hi20 = _sci_exp_bounds({"difficulty": 20})
    assert hi20 - lo20 >= hi0 - lo0
    assert abs(lo20) >= abs(lo0) or hi20 >= hi0


def test_sci_framework_generates_at_continuous_d():
    fw = ScientificNotationFramework(mode="write")
    for d in (0, 10, 20):
        latex, _text, answer = fw.build_prompt({"difficulty": d, "include_answer_key": True})
        assert latex
        assert answer


def test_writing_numeric_complexity_ramps():
    assert _writing_numeric_complexity_from_continuous({"difficulty_tier": "hard"}) is None
    c0, _ = _writing_numeric_complexity_from_continuous({"difficulty": 0})
    c20, hi20 = _writing_numeric_complexity_from_continuous({"difficulty": 22})
    assert c0 == "simple"
    assert c20 == "advanced"
    assert hi20 >= 18


def test_exponent_bounds_ramp_with_continuous_d():
    assert _exponent_bounds_from_continuous({"difficulty_tier": "hard"}) is None
    _lo0, hi0 = _exponent_bounds_from_continuous({"difficulty": 0})
    _lo20, hi20 = _exponent_bounds_from_continuous({"difficulty": 22})
    assert hi0 <= 3
    assert hi20 >= hi0


def test_a1_rational_and_percent_generate_at_continuous_d():
    rat = RationalFramework(operation="+")
    pct = PercentFramework(percent_change=False)
    for d in (0, 10, 20):
        latex, _text, answer = rat.build_prompt({"difficulty": d, "include_answer_key": True})
        assert latex and answer
        latex2, _t2, answer2 = pct.build_prompt({"difficulty": d, "include_answer_key": True})
        assert latex2 and answer2


def test_a1_polynomial_and_exponents_generate_via_api_path():
    for type_id, diffs in (
        ("polynomial_naming", (0, 10, 20)),
        ("properties_of_exponents", (0, 10, 20)),
    ):
        qt = QUESTION_TYPES[type_id]
        for d in diffs:
            qs = qt.generate({"difficulty": d, "count": 1, "include_answer_key": True})
            assert len(qs) == 1
            assert (qs[0].prompt_latex or qs[0].prompt_text or "").strip()


def test_all_a1_a2_catalog_types_expose_continuous_difficulty():
    """Hard requirement: every Algebra 1 / Algebra 2 leaf exposes numeric difficulty."""
    import json
    from pathlib import Path

    rows = json.loads(
        Path("scripts/output/_continuous_d_buckets.json").read_text(encoding="utf-8")
    )["rows"]
    missing: list[str] = []
    for row in rows:
        if row["course"] not in {"algebra_1", "algebra_2"}:
            continue
        tid = row["id"]
        if tid not in QUESTION_TYPES:
            missing.append(f"{tid}:not_registered")
            continue
        if not _has_continuous_difficulty(tid):
            missing.append(tid)
    assert not missing, f"Missing continuous difficulty: {missing[:20]}"


def test_all_ready_catalog_types_expose_continuous_difficulty():
    """Hard requirement: every non-scaffold ready catalog type exposes numeric difficulty."""
    from question_engine.core.registry import TYPE_CATALOG
    from question_engine.type_readiness import type_not_ready

    missing: list[str] = []
    checked = 0
    for entry in TYPE_CATALOG:
        tid = entry.id
        if entry.intent == "scaffold" or type_not_ready(tid):
            # Scaffolds / not-ready still should expose the field when registered.
            if tid in QUESTION_TYPES and not _has_continuous_difficulty(tid):
                missing.append(f"{tid}:scaffold_or_not_ready_missing")
            continue
        checked += 1
        if tid not in QUESTION_TYPES:
            missing.append(f"{tid}:not_registered")
            continue
        if not _has_continuous_difficulty(tid):
            missing.append(tid)
    assert checked > 0
    assert not missing, (
        f"Missing continuous difficulty ({len(missing)}): {missing[:30]}"
    )


def test_all_bucket_audit_rows_already_continuous():
    """Bucket audit should mark every row already_continuous after full migration."""
    import json
    from pathlib import Path

    rows = json.loads(
        Path("scripts/output/_continuous_d_buckets.json").read_text(encoding="utf-8")
    )["rows"]
    leftover = [
        f"{r['course']}:{r['id']}:{r['bucket']}"
        for r in rows
        if r["bucket"] != "already_continuous"
    ]
    assert not leftover, f"Non-continuous buckets remain: {leftover[:20]}"
