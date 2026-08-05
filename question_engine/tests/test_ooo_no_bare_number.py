"""OOO / numeric-expression stems must never be a lone number."""

from __future__ import annotations

import random
import re

import pytest

from question_engine.frameworks.primitives import (
    PRIM_NUMBERS,
    PRIM_OOO,
    build_context,
    sample_structured_expression,
)
from question_engine.frameworks.primitives.constructive import construct_numeric
from question_engine.frameworks.primitives.ooo import sample_ooo_expression
from question_engine.generators import GENERATORS

_DIFFICULTIES = (0, 5, 10, 15, 20)
_SAMPLES_PER_D = 40

# Binary ops (LaTeX or text). Unary leading minus alone is not enough.
_OP_LATEX = re.compile(
    r"(\\times|\\div|\\cdot|\\frac|\+)|"
    r"([\d\)\}]\s*-\s*-?[\d\(\{\\a-zA-Z])"
)
_BARE_NUMBER = re.compile(
    r"^(\\text\{Evaluate:\s*\}\\s*)?"
    r"-?(\d+(\.\d+)?)$"
)


def _assert_has_binary_op(prompt: str) -> None:
    body = prompt.strip()
    if body.startswith(r"\text{Evaluate:"):
        body = body.split("}", 1)[-1].strip()
    body_compact = body.replace(" ", "")
    assert not _BARE_NUMBER.match(body_compact), f"bare number stem: {prompt!r}"
    assert _OP_LATEX.search(body), f"no binary op in stem: {prompt!r}"


@pytest.mark.parametrize("d", _DIFFICULTIES)
def test_order_of_operations_generator_never_bare(d: float):
    gen = GENERATORS["order_of_operations"]
    for i in range(_SAMPLES_PER_D):
        qs = gen(
            "order_of_operations",
            {
                "count": 1,
                "include_answer_key": True,
                "difficulty": d,
                "integers_only": True,
                "seed": 9000 + int(d) * 100 + i,
            },
        )
        assert len(qs) == 1
        _assert_has_binary_op(qs[0].prompt_latex or "")


@pytest.mark.parametrize("d", _DIFFICULTIES)
def test_g6_numeric_expressions_with_exponents_never_bare(d: float):
    gen = GENERATORS["g6_numeric_expressions_with_exponents"]
    for i in range(_SAMPLES_PER_D):
        qs = gen(
            "g6_numeric_expressions_with_exponents",
            {
                "count": 1,
                "include_answer_key": True,
                "difficulty": d,
                "integers_only": True,
                "seed": 11000 + int(d) * 100 + i,
            },
        )
        _assert_has_binary_op(qs[0].prompt_latex or "")
        assert "^{" in (qs[0].prompt_latex or "")


@pytest.mark.parametrize("d", _DIFFICULTIES)
def test_sample_ooo_expression_never_bare(d: float):
    for i in range(_SAMPLES_PER_D):
        ctx = build_context(
            {
                "difficulty": d,
                "integers_only": True,
                "prereq_cap_numbers": 4,
                "prereq_cap_ooo": 40,
            },
            [PRIM_NUMBERS, PRIM_OOO],
            rng=random.Random(2000 + int(d) * 50 + i),
        )
        expr = sample_ooo_expression(ctx)
        _assert_has_binary_op(expr.latex)
        assert expr.n_ops >= 1


@pytest.mark.parametrize("d", _DIFFICULTIES)
def test_structured_expression_numeric_never_bare(d: float):
    for i in range(_SAMPLES_PER_D):
        ctx = build_context(
            {
                "difficulty": d,
                "integers_only": True,
                "prereq_cap_numbers": 4,
                "prereq_cap_ooo": 40,
            },
            [PRIM_NUMBERS, PRIM_OOO],
            rng=random.Random(3000 + int(d) * 50 + i),
        )
        expr = sample_structured_expression(ctx, mode="numeric", d=float(d))
        _assert_has_binary_op(expr.latex)
        binary = sum(1 for op in expr.ops_used if op in {"+", "-", "*", "/"})
        assert binary >= (2 if d >= 10 else 1), (expr.latex, expr.ops_used)
        assert expr.n_leaves >= 2


@pytest.mark.parametrize("d", _DIFFICULTIES)
def test_construct_numeric_top_level_never_bare(d: float):
    for i in range(_SAMPLES_PER_D):
        ctx = build_context(
            {
                "difficulty": d,
                "integers_only": True,
            },
            [PRIM_NUMBERS, PRIM_OOO],
            rng=random.Random(4000 + int(d) * 50 + i),
        )
        surface = construct_numeric(ctx, d=float(d))
        _assert_has_binary_op(surface.latex)
        assert "seed" in surface.inflators_applied
        assert any(
            tag in surface.inflators_applied
            for tag in (
                "split_add",
                "split_sub",
                "scale_div",
                "parens_sum",
                "mul_add",
                "scale_mul_div",
            )
        )
