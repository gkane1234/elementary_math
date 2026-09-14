"""Tests for FactorProduct skeleton + extended factor_sampler."""

from __future__ import annotations

import random

import re

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives import PRIM_FACTOR_POLY, PRIM_NUMBERS, PRIM_VARIABLE, build_context
from question_engine.frameworks.primitives.expression_policy import polynomial_policy
from question_engine.frameworks.primitives.factor_sampler import (
    FactorConstraints,
    constraints_from_settings,
    sample_factor_product,
)
from question_engine.frameworks.primitives.poly_helpers import poly_degree
from question_engine.frameworks.primitives.poly_skeleton import (
    generate_factor_product_question,
    knobs_from_form_id,
    sample_factor_product_item,
    sample_factor_product_mixer,
    use_factor_product_skeleton,
)
from question_engine.generators import GENERATORS
from question_engine.generators.primitive_polynomial import quadratic_factoring


def _ctx(d: float = 5.0, *, max_degree: int = 4, leaf: str = "quadratic_factoring", seed: int = 0):
    return build_context(
        {"difficulty": d, "seed": seed, "integers_only": True, "only_x": True},
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
        policy=polynomial_policy(max_degree=max_degree),
        leaf_id=leaf,
    )


def test_factor_sampler_kind_diff_squares_degree_two():
    cons = FactorConstraints(
        factor_kind="diff_squares",
        max_product_degree=2,
        allow_nonmonic=False,
    ).clamped()
    ctx = _ctx(4.0, max_degree=2)
    draw = sample_factor_product(ctx, constraints=cons, factor_kind="diff_squares")
    assert draw.factor_kind == "diff_squares"
    assert poly_degree(draw.product) == 2


def test_factor_sampler_grouping_is_always_cubic():
    cons = FactorConstraints(
        factor_kind="grouping",
        max_product_degree=2,
        allow_nonmonic=False,
    ).clamped()
    ctx = _ctx(0.0, max_degree=3, leaf="polynomial_factoring_grouping")
    draw = sample_factor_product(ctx, constraints=cons, factor_kind="grouping")
    assert draw.factor_kind == "grouping"
    assert poly_degree(draw.product) == 3
    nz = [p for p, c in draw.product.items() if c != 0]
    assert len(nz) == 4


def test_factor_sampler_rational_lane_still_caps_at_two():
    low = constraints_from_settings({}, d=2.0)
    assert low.max_product_degree == 2
    ctx = _ctx(2.0, max_degree=2)
    draw = sample_factor_product(ctx, n_factors=2, constraints=low)
    assert poly_degree(draw.product) <= 2


def test_knobs_from_a2_form_ids():
    assert knobs_from_form_id("trinomial_a_gt_1")["allow_nonmonic"] is True
    assert knobs_from_form_id("factor_by_grouping")["kind"] == "grouping"
    assert knobs_from_form_id("sum_diff_cubes")["max_product_degree"] == 3
    assert knobs_from_form_id("quadratic_form")["max_product_degree"] == 4


def test_sample_factor_product_item_stamps_skeleton():
    ctx = _ctx(2.0, max_degree=2)
    item = sample_factor_product_item(
        ctx, task="factor", form_id="trinomial_x2_bx_c"
    )
    assert item.metadata.get("skeleton_pattern") == "FactorProduct"
    assert item.task == "factor"
    assert item.degree == 2
    assert item.prompt_latex
    assert item.answer_latex


def test_factor_product_default_and_opt_out():
    assert use_factor_product_skeleton({}) is True
    assert use_factor_product_skeleton({"use_factor_poly": True}) is False
    assert use_factor_product_skeleton({"use_factor_product_skeleton": False}) is False

    qs = quadratic_factoring(
        "quadratic_factoring",
        {"difficulty": 4, "count": 3, "seed": 11, "include_answer_key": True},
    )
    assert qs
    for q in qs:
        assert q.metadata.get("skeleton_pattern") == "FactorProduct"
        assert q.metadata.get("primitive_engine") == "poly_skeleton"

    qs_old = quadratic_factoring(
        "quadratic_factoring",
        {
            "difficulty": 4,
            "count": 2,
            "seed": 11,
            "include_answer_key": True,
            "use_factor_poly": True,
        },
    )
    assert qs_old[0].metadata.get("primitive_engine") == "quadratic_factoring"


def test_a2_factoring_leaves_default_to_factor_product():
    for tid in (
        "a2_polynomial_functions_factoring_by_grouping",
        "a2_polynomial_functions_factoring_sum_difference_of_cubes",
        "a2_polynomial_functions_factoring_quadratic_form",
        "a2_polynomial_functions_factoring_all_techniques",
        "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions",
    ):
        qs = GENERATORS[tid](
            tid,
            {
                "difficulty": 8,
                "count": 2,
                "seed": 21,
                "include_answer_key": True,
                "integers_only": True,
                "only_x": True,
            },
        )
        assert len(qs) == 2
        for q in qs:
            assert q.metadata.get("skeleton_pattern") == "FactorProduct"
            assert q.metadata.get("primitive_engine") == "poly_skeleton"
            assert q.answer_latex


def test_a2_multiply_leaves_use_factor_product():
    for tid in (
        "a2_polynomial_functions_multiplying",
        "a2_polynomial_functions_multiplying_special_cases",
    ):
        qs = GENERATORS[tid](
            tid,
            {"difficulty": 6, "count": 2, "seed": 3, "include_answer_key": True},
        )
        assert qs
        for q in qs:
            assert q.metadata.get("skeleton_pattern") == "FactorProduct"
            assert q.metadata.get("task") == "multiply"


def test_a2_all_techniques_mixer_includes_cubes():
    ctx = _ctx(10.0, max_degree=3, leaf="a2_polynomial_functions_factoring_all_techniques")
    ctx.rng = random.Random(99)
    ctx.topic_d = 10.0
    seen = set()
    for seed in range(40):
        ctx.rng = random.Random(seed)
        item = sample_factor_product_mixer(ctx, leaf_id="a2_polynomial_functions_factoring_all_techniques")
        seen.add(item.metadata.get("mixer_pick") or item.form_id)
    assert "sum_diff_cubes" in seen or "factor_by_grouping" in seen


def test_live_generate_smoke():
    qs = _generate_for_type(
        "a2_polynomial_functions_factoring_by_grouping",
        {"difficulty": 6, "count": 1, "seed": 42, "include_answer_key": True},
    )
    meta = qs[0].metadata or {}
    assert meta.get("skeleton_pattern") == "FactorProduct"
    assert meta.get("form_id") == "factor_by_grouping"


def test_demo_api():
    r = generate_factor_product_question(
        {"difficulty": 5, "seed": 1, "form_id": "difference_of_squares"},
        leaf_id="polynomial_factoring_special_cases",
    )
    assert "FactorProduct" in r.metadata.get("skeleton_pattern", "")


def _eq(d: float, seed: int):
    qs = _generate_for_type(
        "quadratic_factoring_equations",
        {
            "difficulty": d,
            "seed": seed,
            "count": 1,
            "include_answer_key": True,
            "integers_only": True,
            "only_x": True,
        },
    )
    assert qs
    return qs[0]


def _stem_leading(prompt: str) -> int | None:
    """Leading coeff of a plain expanded ax²+…=0 stem; None if unsimplified."""
    blob = (prompt or "").replace(" ", "").split("=")[0]
    if r"\left(" in blob or r"\left" in blob:
        return None
    m = re.match(r"(-?\d*)x\^\{2\}", blob)
    if not m:
        return None
    raw = m.group(1)
    if raw in ("", "+"):
        return 1
    if raw == "-":
        return -1
    return int(raw)


def test_factor_equations_d0_monic_like_old():
    """Old factor_poly D=0 is always a=1, both constants positive."""
    for seed in range(12):
        q = _eq(0.0, seed=101 + seed)
        assert q.metadata.get("skeleton_pattern") == "FactorProduct"
        blob = (q.prompt_latex or "").replace(" ", "")
        assert blob.endswith("=0")
        assert (q.metadata or {}).get("method") == "monic_simple"
        a = _stem_leading(q.prompt_latex or "")
        assert a == 1, (seed, q.prompt_latex)
        assert r"x^{3}" not in blob
        assert "x =" in (q.answer_latex or "")


def test_factor_equations_d8_emits_a_ne_1():
    """Old path forces ac_method (a≠1) at nonmonic_from_d=8. Still degree 2."""
    hits = 0
    for seed in range(20):
        q = _eq(8.0, seed=200 + seed)
        meta = q.metadata or {}
        assert meta.get("skeleton_pattern") == "FactorProduct"
        blob = (q.prompt_latex or "").replace(" ", "")
        assert r"x^{3}" not in blob and "x^3" not in blob
        a = _stem_leading(q.prompt_latex or "")
        if meta.get("method") == "ac_method" or (a is not None and abs(a) != 1):
            hits += 1
        assert "x =" in (q.answer_latex or "")
    assert hits >= 16, hits


def test_factor_equations_high_d_still_quadratic_not_grouping():
    """Old equation leaf never grouped / cubicked — only ac_method + unsimplify."""
    unsimp = 0
    ac = 0
    for seed in range(16):
        q = _eq(16.0, seed=300 + seed)
        meta = q.metadata or {}
        blob = (q.prompt_latex or "").replace(" ", "")
        assert r"x^{3}" not in blob and "x^3" not in blob
        ups = meta.get("upgrades") or []
        if "unsimplified" in ups:
            unsimp += 1
        if meta.get("method") == "ac_method":
            ac += 1
        assert meta.get("degree") == 2
    assert ac >= 12, ac
    assert unsimp >= 8, unsimp
