"""Global expression sign formatting: no `5+-2`, no bare `2/-1`."""

from __future__ import annotations

import random
import re

from packages.polynomial_core import (
    format_binop_expression,
    format_slash_fraction,
    normalize_expression_signs,
    paren_if_negative,
)
from question_engine.core.models import Question
from question_engine.frameworks.equation import OneStepEquationsFramework
from question_engine.frameworks.graphing import _linear_function_expr, _poly_function_expr
from question_engine.frameworks.number import IntegerArithmeticFramework, RationalFramework


def test_normalize_collapses_plus_minus():
    assert normalize_expression_signs("5+-2") == "5-2"
    assert normalize_expression_signs("5 + -2") == "5 - 2"
    assert normalize_expression_signs("2*x+-3") == "2*x-3"
    assert normalize_expression_signs("5--2") == "5+2"
    assert normalize_expression_signs("5 - -2") == "5 + 2"


def test_normalize_parens_negative_slash_denom():
    assert normalize_expression_signs("2/-1") == "2/(-1)"
    assert normalize_expression_signs("2/ -3") == "2/(-3)"
    assert normalize_expression_signs("2/(-1)") == "2/(-1)"
    assert normalize_expression_signs("a/-2.5") == "a/(-2.5)"


def test_normalize_parens_div_mul_negative_operands():
    assert normalize_expression_signs(r"2 \div -1") == r"2 \div (-1)"
    assert normalize_expression_signs(r"3 \cdot -4") == r"3 \cdot (-4)"
    assert normalize_expression_signs("2*-3") == "2*(-3)"


def test_format_slash_and_binop_helpers():
    assert format_slash_fraction(2, -1) == "2/(-1)"
    assert format_slash_fraction(2, 3) == "2/3"
    assert paren_if_negative(-1) == "(-1)"
    assert format_binop_expression(5, "+", -2) == "5 - 2"
    assert format_binop_expression(5, "+", -2, spaced=False) == "5-2"
    assert format_binop_expression(2, "/", -1) == "2/(-1)"
    assert format_binop_expression(2, "\\div", -1) == r"2 \div (-1)"
    assert format_binop_expression(5, "-", -2) == "5 - (-2)"


def test_question_post_init_normalizes_fields():
    q = Question(
        id="t",
        topic="t",
        prompt_latex="5+-2",
        prompt_text="2/-1",
        answer_latex="3+-4",
    )
    assert q.prompt_latex == "5-2"
    assert q.prompt_text == "2/(-1)"
    assert q.answer_latex == "3-4"


def test_graph_sampler_exprs_never_emit_plus_minus():
    assert "+-" not in _linear_function_expr(2, -3)
    assert _linear_function_expr(2, -3) == "2*x-3"
    assert "+-" not in _poly_function_expr([1, -2, -3])
    assert _poly_function_expr([1, -2, -3]) == "1*x^2-2*x-3"


def test_integer_arithmetic_spot_check():
    fw = IntegerArithmeticFramework("+")
    random.seed(11)
    settings = {
        "num_min": -9,
        "num_max": 9,
        "allow_negative": True,
        "count": 1,
        "include_answer_key": True,
    }
    for _ in range(40):
        prompt, text, _ = fw.build_prompt(settings)
        assert "+-" not in prompt.replace(" ", "")
        assert "+-" not in text.replace(" ", "")
        assert " + -" not in prompt
        assert " + -" not in text


def test_integer_division_parens_negative_divisor():
    assert format_binop_expression(2, "/", -1) == "2/(-1)"
    assert format_binop_expression(2, "\\div", -1) == r"2 \div (-1)"


def test_one_step_and_fraction_spot_check():
    eq = OneStepEquationsFramework()
    rational = RationalFramework("+-")
    random.seed(42)
    eq_settings = {
        "coef_min": 2,
        "coef_max": 6,
        "solution_min": -5,
        "solution_max": 5,
        "allow_fraction_solutions": False,
        "count": 1,
        "include_answer_key": True,
    }
    frac_settings = {
        "num_min": -5,
        "num_max": 5,
        "denom_min": 2,
        "denom_max": 6,
        "allow_negative": True,
        "count": 1,
        "include_answer_key": True,
    }
    # Bare slash-negative like `/-3` (parenthesized `/(-3)` does not match).
    bare_slash_neg = re.compile(r"/\s*-\d")
    for _ in range(30):
        for prompt, text, answer in (
            eq.build_prompt(eq_settings),
            rational.build_prompt(frac_settings),
        ):
            for field in (prompt, text, answer or ""):
                assert "+-" not in field.replace(" ", "")
                assert not bare_slash_neg.search(field)
