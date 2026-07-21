"""Tests for factors-first quadratic factoring ladder."""

from __future__ import annotations

import random

from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs
from question_engine.frameworks.primitives.expression_policy import polynomial_policy
from question_engine.frameworks.primitives.factor_poly import (
    sample_factoring_grouping,
    sample_quadratic_factoring,
    sample_special_factoring,
)
from question_engine.frameworks.primitives.registry import (
    PRIM_FACTOR_POLY,
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.generators import GENERATORS


def _ctx(d: float):
    return build_context(
        {
            "difficulty": d,
            "integers_only": True,
            "only_x": True,
            "seed": int(d * 10) + 3,
        },
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
        policy=polynomial_policy(max_degree=2),
        leaf_id="quadratic_factoring",
    )


def test_quadratic_factoring_low_d_is_monic_simple():
    reload_knobs()
    for seed in range(20):
        ctx = _ctx(0)
        ctx.rng = random.Random(seed)
        ctx.topic_d = 0.0
        item = sample_quadratic_factoring(ctx)
        assert item.degree == 2
        assert item.method == "monic_simple"
        assert "unsimplified" not in item.upgrades
        # Expanded form should look like standard ax^2+bx+c with a=1
        assert item.poly_coeffs is not None
        assert item.poly_coeffs.get(2) == 1


def test_quadratic_factoring_unsimplifies_above_d10():
    reload_knobs()
    hits = 0
    for seed in range(30):
        ctx = _ctx(18)
        ctx.rng = random.Random(seed)
        ctx.topic_d = 18.0
        item = sample_quadratic_factoring(ctx)
        if "unsimplified" in item.upgrades:
            hits += 1
            assert item.latex != ""  # disguised stem
    assert hits >= 8


def test_quadratic_factoring_generator_ladder_print():
    reload_knobs()
    gen = GENERATORS["quadratic_factoring"]
    for d in (0, 5, 10, 15, 20):
        qs = gen(
            "quadratic_factoring",
            {
                "difficulty": d,
                "count": 3,
                "seed": 7 + d,
                "integers_only": True,
                "only_x": True,
                "include_answer_key": True,
            },
        )
        for q in qs:
            assert q.prompt_latex
            assert q.answer_latex
            assert "=" not in (q.prompt_latex or "") or "Factor" in ""
            print(
                f"D={d}: {q.prompt_latex} -> {q.answer_latex} "
                f"method={q.metadata.get('method')} up={q.metadata.get('upgrades')}"
            )


def test_quadratic_equations_factors_first():
    reload_knobs()
    gen = GENERATORS["quadratic_factoring_equations"]
    qs = gen(
        "quadratic_factoring_equations",
        {
            "difficulty": 2,
            "count": 5,
            "seed": 11,
            "integers_only": True,
            "only_x": True,
            "include_answer_key": True,
        },
    )
    for q in qs:
        assert "= 0" in (q.prompt_latex or "")
        assert "x =" in (q.answer_latex or "")
        print(f"EQ: {q.prompt_latex} -> {q.answer_latex}")


def test_special_factoring_smoke():
    reload_knobs()
    ctx = _ctx(2)
    item = sample_special_factoring(ctx)
    assert item.degree == 2
    assert item.method in ("difference_of_squares", "perfect_square")
    assert len(item.factor_coeffs) == 2
    # Stem-only: no "Factor:" wrapper on the expression.
    assert not item.latex.lower().startswith("factor")
    assert not item.text.lower().startswith("factor")


def test_grouping_has_factor_coeffs_and_stem_only():
    reload_knobs()
    ctx = build_context(
        {
            "difficulty": 5,
            "integers_only": True,
            "only_x": True,
            "seed": 42,
        },
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
        policy=polynomial_policy(max_degree=3),
        leaf_id="polynomial_factoring_grouping",
    )
    item = sample_factoring_grouping(ctx)
    assert len(item.factor_coeffs) == 2
    assert item.poly_coeffs is not None
    assert not item.latex.lower().startswith("factor")
    assert not item.text.lower().startswith("factor")


def test_special_and_grouping_generators_stem_only():
    reload_knobs()
    for tid in ("polynomial_factoring_special_cases", "polynomial_factoring_grouping"):
        qs = GENERATORS[tid](
            tid,
            {
                "difficulty": 4,
                "count": 4,
                "seed": 9,
                "integers_only": True,
                "only_x": True,
                "include_answer_key": True,
                "max_degree": 2,
            },
        )
        for q in qs:
            pl = (q.prompt_latex or "").strip()
            pt = (q.prompt_text or "").strip()
            assert not pl.lower().startswith("\\text{factor")
            assert not pt.lower().startswith("factor")
            assert q.answer_latex
