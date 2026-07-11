"""Division notation settings for fraction / rational divide prompts."""

from __future__ import annotations

import random

from question_engine.frameworks.number import RationalFramework
from question_engine.generators.utils import format_fraction_division_latex
from question_engine.settings.generator_profiles import schema_for_generator
from question_engine.settings.params import allowed_division_notations
from fractions import Fraction


def test_allowed_division_notations_respects_toggles():
    assert allowed_division_notations(
        {"allow_obelus": False, "allow_complex_fraction": True, "allow_slash": False}
    ) == ["complex_fraction"]
    assert allowed_division_notations(
        {"allow_obelus": True, "allow_complex_fraction": False, "allow_slash": False}
    ) == ["obelus"]
    assert allowed_division_notations(
        {"allow_obelus": False, "allow_complex_fraction": False, "allow_slash": False}
    ) == ["obelus"]


def test_format_fraction_division_latex_forms():
    a = Fraction(1, 2)
    b = Fraction(3, 4)
    assert format_fraction_division_latex(a, b, "obelus") == r"\frac{1}{2} \div \frac{3}{4}"
    assert format_fraction_division_latex(a, b, "complex_fraction") == r"\frac{\frac{1}{2}}{\frac{3}{4}}"
    assert (
        format_fraction_division_latex(a, b, "slash")
        == r"\left(\frac{1}{2}\right) / \left(\frac{3}{4}\right)"
    )


def test_divide_schema_includes_notation_settings():
    for key in ("g6_fraction_divide", "rational_divide"):
        keys = {field.key for field in schema_for_generator(key)}
        assert {"allow_obelus", "allow_complex_fraction", "allow_slash"} <= keys


def test_multiply_schema_excludes_notation_settings():
    keys = {field.key for field in schema_for_generator("g6_fraction_multiply")}
    assert "allow_obelus" not in keys


def test_only_complex_fraction_never_uses_obelus():
    framework = RationalFramework("/")
    random.seed(42)
    settings = {
        "count": 1,
        "include_answer_key": True,
        "allow_obelus": False,
        "allow_complex_fraction": True,
        "allow_slash": False,
        "allow_negative": False,
        "num_min": 1,
        "num_max": 5,
        "denom_min": 2,
        "denom_max": 6,
    }
    for _ in range(30):
        prompt, _, _ = framework.build_prompt(settings)
        assert r"\div" not in prompt
        assert prompt.startswith(r"\frac{")


def test_only_obelus_always_uses_div():
    framework = RationalFramework("/")
    random.seed(7)
    settings = {
        "count": 1,
        "include_answer_key": True,
        "allow_obelus": True,
        "allow_complex_fraction": False,
        "allow_slash": False,
        "allow_negative": False,
        "num_min": 1,
        "num_max": 5,
        "denom_min": 2,
        "denom_max": 6,
    }
    for _ in range(20):
        prompt, _, _ = framework.build_prompt(settings)
        assert r"\div" in prompt


def test_mixed_notations_can_produce_each_form():
    framework = RationalFramework("/")
    random.seed(99)
    settings = {
        "count": 1,
        "include_answer_key": True,
        "allow_obelus": True,
        "allow_complex_fraction": True,
        "allow_slash": True,
        "allow_negative": False,
        "num_min": 1,
        "num_max": 5,
        "denom_min": 2,
        "denom_max": 6,
    }
    seen_obelus = seen_complex = seen_slash = False
    for _ in range(80):
        prompt, _, _ = framework.build_prompt(settings)
        if r"\div" in prompt:
            seen_obelus = True
        elif " / " in prompt:
            seen_slash = True
        else:
            seen_complex = True
        if seen_obelus and seen_complex and seen_slash:
            break
    assert seen_obelus and seen_complex and seen_slash
