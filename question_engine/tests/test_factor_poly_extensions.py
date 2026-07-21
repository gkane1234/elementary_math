"""Tests for factors-first cubes, quadratic form, and all-techniques mixer."""

from __future__ import annotations

import random

from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs
from question_engine.frameworks.primitives.expression_policy import polynomial_policy
from question_engine.frameworks.primitives.factor_poly import (
    sample_factoring_all_techniques,
    sample_quadratic_form,
    sample_sum_diff_cubes,
)
from question_engine.frameworks.primitives.registry import (
    PRIM_FACTOR_GCF,
    PRIM_FACTOR_POLY,
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
    resolve_primitive,
)
from question_engine.generators import GENERATORS


def _ctx(d: float, *, max_degree: int, leaf_id: str, seed: int = 0):
    return build_context(
        {
            "difficulty": d,
            "integers_only": True,
            "only_x": True,
            "seed": seed + int(d * 10),
        },
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY, PRIM_FACTOR_GCF],
        policy=polynomial_policy(max_degree=max_degree),
        leaf_id=leaf_id,
    )


def test_sum_diff_cubes_low_d_is_plain_cubic():
    reload_knobs()
    for seed in range(15):
        ctx = _ctx(0, max_degree=3, leaf_id="polynomial_factoring_sum_diff_cubes", seed=seed)
        ctx.rng = random.Random(seed)
        ctx.topic_d = 0.0
        item = sample_sum_diff_cubes(ctx)
        assert item.degree == 3
        assert item.method == "difference_of_cubes"
        assert "unsimplified" not in item.upgrades
        assert item.poly_coeffs is not None
        # a³x³ − b³ → only deg 3 and deg 0 terms
        assert set(k for k, v in item.poly_coeffs.items() if v != 0) <= {0, 3}
        assert item.poly_coeffs.get(3) == 1


def test_sum_diff_cubes_unsimplifies_above_d10():
    reload_knobs()
    hits = 0
    for seed in range(30):
        ctx = _ctx(18, max_degree=3, leaf_id="polynomial_factoring_sum_diff_cubes", seed=seed)
        ctx.rng = random.Random(seed)
        ctx.topic_d = 18.0
        item = sample_sum_diff_cubes(ctx)
        if "unsimplified" in item.upgrades:
            hits += 1
    assert hits >= 5


def test_quadratic_form_is_degree_4_not_plain_quadratic():
    reload_knobs()
    for seed in range(20):
        ctx = _ctx(2, max_degree=4, leaf_id="polynomial_factoring_quadratic_form", seed=seed)
        ctx.rng = random.Random(seed)
        ctx.topic_d = 2.0
        item = sample_quadratic_form(ctx)
        assert item.degree == 4
        assert item.method.startswith("quadratic_form")
        assert item.poly_coeffs is not None
        # Pure quadratic-in-x²: only even powers
        odd = [k for k, v in item.poly_coeffs.items() if v != 0 and k % 2]
        assert odd == []
        assert item.poly_coeffs.get(4) is not None


def test_quadratic_form_generator_not_alias_to_quadratic():
    reload_knobs()
    qs = GENERATORS["a2_polynomial_functions_factoring_quadratic_form"](
        "a2_polynomial_functions_factoring_quadratic_form",
        {
            "difficulty": 1,
            "count": 6,
            "seed": 21,
            "integers_only": True,
            "only_x": True,
            "include_answer_key": True,
        },
    )
    for q in qs:
        assert q.prompt_latex
        assert q.answer_latex
        meta = q.metadata or {}
        assert meta.get("primitive_engine") == "polynomial_factoring_quadratic_form"
        assert meta.get("degree") == 4
        assert "^{4}" in (q.prompt_latex or "") or "^4" in (q.prompt_latex or "")


def test_cubes_generator_uses_cube_methods():
    reload_knobs()
    qs = GENERATORS["a2_polynomial_functions_factoring_sum_difference_of_cubes"](
        "a2_polynomial_functions_factoring_sum_difference_of_cubes",
        {
            "difficulty": 4,
            "count": 8,
            "seed": 33,
            "integers_only": True,
            "only_x": True,
            "include_answer_key": True,
        },
    )
    methods = {q.metadata.get("method") for q in qs}
    assert methods <= {"sum_of_cubes", "difference_of_cubes"}
    assert methods  # non-empty
    for q in qs:
        assert q.metadata.get("degree") == 3
        assert q.answer_latex


def test_a2_all_techniques_mixes_and_can_include_cubes():
    reload_knobs()
    seen_picks: set[str] = set()
    cube_hits = 0
    for seed in range(40):
        ctx = _ctx(
            8,
            max_degree=3,
            leaf_id="a2_polynomial_functions_factoring_all_techniques",
            seed=seed,
        )
        ctx.rng = random.Random(seed)
        ctx.topic_d = 8.0
        item = sample_factoring_all_techniques(ctx)
        assert item.upgrades[0] == "all_techniques"
        pick = item.upgrades[1]
        seen_picks.add(str(pick))
        if pick == "cubes":
            cube_hits += 1
            assert item.method in ("all:sum_of_cubes", "all:difference_of_cubes")
    assert "quadratic" in seen_picks or "special" in seen_picks
    assert "gcf" in seen_picks or "grouping" in seen_picks
    assert cube_hits >= 1


def test_a1_general_strategy_excludes_cubes():
    reload_knobs()
    for seed in range(30):
        ctx = _ctx(
            8,
            max_degree=3,
            leaf_id="polynomial_factoring_general_strategy",
            seed=seed,
        )
        ctx.rng = random.Random(seed)
        ctx.topic_d = 8.0
        item = sample_factoring_all_techniques(ctx)
        assert item.upgrades[1] != "cubes"
        assert "cubes" not in item.method


def test_all_techniques_generators_registered():
    reload_knobs()
    for tid in (
        "a2_polynomial_functions_factoring_all_techniques",
        "polynomial_factoring_general_strategy",
    ):
        qs = GENERATORS[tid](
            tid,
            {
                "difficulty": 5,
                "count": 5,
                "seed": 9,
                "integers_only": True,
                "only_x": True,
                "include_answer_key": True,
            },
        )
        assert len(qs) == 5
        for q in qs:
            assert q.prompt_latex
            assert q.answer_latex
            assert not (q.prompt_latex or "").lower().startswith("\\text{factor")


def test_leaf_resolves_new_factor_poly_topics():
    assert resolve_primitive("a2_polynomial_functions_factoring_sum_difference_of_cubes") == (
        "factor_poly"
    )
    assert resolve_primitive("a2_polynomial_functions_factoring_quadratic_form") == "factor_poly"
    assert resolve_primitive("a2_polynomial_functions_factoring_all_techniques") == "factor_poly"
    assert resolve_primitive("polynomial_factoring_general_strategy") == "factor_poly"
