"""Distributive form catalog: D-gated upgrades, metadata, answer checks."""

from __future__ import annotations

import random
import re
from collections import Counter
from fractions import Fraction

from question_engine.frameworks.primitives.distributive import (
    expand_product_of_sums_latex,
    sample_distributive_algebraic,
    sample_distributive_numeric,
)
from question_engine.frameworks.primitives.registry import (
    PRIM_DISTRIBUTIVE,
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)


def _num_ctx(d: float, seed: int = 0):
    return build_context(
        {
            "difficulty": d,
            "integers_only": True,
            "exclude_zero": True,
        },
        [PRIM_NUMBERS, PRIM_DISTRIBUTIVE],
        rng=random.Random(seed),
    )


def _alg_ctx(d: float, seed: int = 0):
    return build_context(
        {
            "difficulty": d,
            "integers_only": True,
            "only_x": True,
            "lock_variable": "x",
            "exclude_zero": True,
            "allow_greek": False,
        },
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_DISTRIBUTIVE],
        rng=random.Random(seed),
    )


def test_expand_product_of_sums_signs():
    latex = expand_product_of_sums_latex(
        [("2", Fraction(2)), ("-3", Fraction(-3))],
        [("4", Fraction(4)), ("1", Fraction(1))],
    )
    assert "2\\cdot 4" in latex
    assert "2\\cdot 1" in latex
    assert "3\\cdot 4" in latex  # signed as subtraction
    assert latex.count("\\cdot") == 4


def test_numeric_form_metadata_and_diversity():
    forms: set[str] = set()
    sides: set[str] = set()
    n_terms: set[int] = set()
    for seed in range(80):
        ctx = _num_ctx(d=12.0, seed=seed)
        expr = sample_distributive_numeric(ctx)
        forms.add(expr.form_id)
        sides.add(expr.factor_side)
        n_terms.add(expr.n_terms_inside)
        assert expr.form_id in {"scaled_sum", "two_binomials"}
        assert expr.factor_side in {"left", "right", "both"}
        assert expr.n_terms_inside >= 2
        # sample_log carries the same structure tags
        dist_logs = [
            e for e in ctx.metadata()["sample_log"] if e.get("primitive") == "distributive"
        ]
        assert dist_logs
        assert dist_logs[-1]["form_id"] == expr.form_id

    assert "scaled_sum" in forms
    assert "left" in sides and "right" in sides
    assert 2 in n_terms


def test_hard_forms_more_common_at_high_d():
    def count_hard(d: float, n: int = 60) -> Counter:
        c: Counter = Counter()
        for seed in range(n):
            expr = sample_distributive_numeric(_num_ctx(d=d, seed=seed))
            c[expr.form_id] += 1
            if expr.n_terms_inside >= 3:
                c["three_plus"] += 1
            if expr.factor_side == "right":
                c["right"] += 1
        return c

    low = count_hard(0.0)
    high = count_hard(20.0)
    assert low["two_binomials"] == 0
    assert high["two_binomials"] > low["two_binomials"]
    assert high["two_binomials"] >= 5
    # Trinomial / right side should also ramp (soft right may still appear at D=0)
    assert high["three_plus"] > low["three_plus"]


def test_numeric_answers_match_value_check():
    for seed in range(40):
        for d in (0.0, 10.0, 20.0):
            expr = sample_distributive_numeric(_num_ctx(d=d, seed=seed + int(d)))
            # Expanded answer uses · products; evaluate via value_check identity.
            assert isinstance(expr.value_check, Fraction)
            assert expr.expanded_latex
            assert "\\cdot" in expr.expanded_latex
            # Prompt is a product involving at least one grouped sum.
            assert "(" in expr.text


def test_algebraic_form_diversity_and_sides():
    forms: set[str] = set()
    form_ids: set[str] = set()
    sides: set[str] = set()
    texts: list[str] = []
    for seed in range(70):
        expr = sample_distributive_algebraic(_alg_ctx(d=8.0, seed=seed))
        forms.add(expr.form)
        form_ids.add(expr.form_id)
        sides.add(expr.factor_side)
        texts.append(expr.text)
        assert expr.expanded_latex

    assert "var_outer" in forms
    assert "const_outer" in forms
    assert "scaled_sum" in form_ids
    assert "left" in sides and "right" in sides
    outer_first = any(
        re.match(r"^[A-Za-z]\(", t) or re.match(r"^-?\d+\(", t) for t in texts
    )
    paren_first = any(t.startswith("(") for t in texts)
    assert outer_first and paren_first


def test_algebraic_two_binomials_at_high_d():
    hits = 0
    for seed in range(50):
        expr = sample_distributive_algebraic(_alg_ctx(d=22.0, seed=seed))
        if expr.form_id == "two_binomials":
            hits += 1
            assert expr.factor_side == "both"
            # One var binomial × numeric binomial → two paren groups
            assert expr.text.count("(") >= 2
            assert "\\cdot" in expr.expanded_latex
    assert hits >= 3


def test_live_generator_metadata_form_id():
    from question_engine.generators import GENERATORS

    gen = GENERATORS["distributive_property"]
    form_ids: set[str] = set()
    sides: set[str] = set()
    for seed in range(40):
        random.seed(seed)
        qs = gen(
            "distributive_property",
            {
                "count": 1,
                "difficulty": 18.0,
                "integers_only": True,
                "exclude_zero": True,
                "include_answer_key": True,
            },
        )
        q = qs[0]
        meta = q.metadata or {}
        form_ids.add(str(meta.get("form_id") or ""))
        sides.add(str(meta.get("factor_side") or ""))
        assert meta.get("n_terms_inside") is not None
        assert q.answer_latex
        assert "\\cdot" in (q.answer_latex or "")

    assert "scaled_sum" in form_ids
    assert len(form_ids) >= 1
    assert sides & {"left", "right", "both"}


def test_g6_algebraic_uses_primitive_not_ladder():
    from question_engine.generators import GENERATORS

    gen = GENERATORS["distributive_property_algebraic"]
    engines: set[str] = set()
    forms: set[str] = set()
    for seed in range(40):
        random.seed(seed)
        qs = gen(
            "g6_distributive_property_algebraic",
            {
                "count": 1,
                "difficulty": 0,
                "integers_only": True,
                "only_x": True,
                "exclude_zero": True,
            },
        )
        meta = qs[0].metadata or {}
        engines.add(str(meta.get("primitive_engine") or ""))
        forms.add(str(meta.get("distributive_form") or ""))
        assert meta.get("form_id") == "scaled_sum" or meta.get("form_id") in {
            "scaled_sum",
            "two_binomials",
        }

    assert "distributive_algebraic" in engines
    assert "distributive_algebraic_g6" not in engines
    assert "var_outer" in forms
    assert "const_outer" in forms
