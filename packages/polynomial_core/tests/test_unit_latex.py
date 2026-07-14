"""Unit labels in math mode must be upright (\\text), not italicized."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from packages.polynomial_core import (
    format_measurement_text,
    format_with_unit,
    unit_latex,
)

REPO_ROOT = Path(__file__).resolve().parents[3]


def _frac_latex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    if value.numerator < 0:
        return f"-\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"
    return f"\\frac{{{value.numerator}}}{{{value.denominator}}}"


def test_unit_latex_upright():
    assert unit_latex("cm") == r"\text{ cm}"
    assert unit_latex("cm", leading_space=False) == r"\text{cm}"
    assert unit_latex("") == ""
    assert unit_latex("  in  ") == r"\text{ in}"


def test_format_with_unit_basic():
    assert format_with_unit(3, "cm") == r"3\text{ cm}"
    assert format_with_unit(r"\frac{3}{2}", "cm") == r"\frac{3}{2}\text{ cm}"
    assert format_with_unit(5, "cm", power=2) == r"5\text{ cm}^{2}"
    assert format_with_unit(4, "cm", power=3) == r"4\text{ cm}^{3}"
    assert format_with_unit(Fraction(3, 2), "in") == r"\frac{3}{2}\text{ in}"


def test_format_with_unit_empty_unit_keeps_value():
    assert format_with_unit(7, "") == "7"
    assert format_with_unit(7, "", power=2) == r"7^{2}"


def test_format_measurement_text_plain():
    assert format_measurement_text(5, "cm") == "5 cm"
    assert format_measurement_text("3/2", "in") == "3/2 in"
    assert format_measurement_text(9, "cm", power=2) == "9 cm^2"
    assert format_measurement_text(3, "") == "3"


def test_example_before_after_documented():
    """Canonical before/after for the user-facing area prompt example."""
    # Before (bug): fraction left math mode, bare unit italicized.
    before = r"\text{Find the area of the rectangle with base } \frac{3}{2}cm"
    after_value = format_with_unit(r"\frac{3}{2}", "cm")
    after = rf"\text{{Find the area of the rectangle with base }} {after_value}"
    assert before.endswith(r"\frac{3}{2}cm")
    assert after_value == r"\frac{3}{2}\text{ cm}"
    assert after == (
        r"\text{Find the area of the rectangle with base } \frac{3}{2}\text{ cm}"
    )


def test_grade6_visual_style_area_prompt():
    """Same construction Grade6VisualFramework uses for fraction rectangles."""
    a, b, unit = Fraction(3, 2), Fraction(1, 4), "cm"
    latex = (
        f"\\text{{Find the area of the rectangle with base }} "
        f"{format_with_unit(_frac_latex(a), unit)} "
        f"\\text{{ and height }} {format_with_unit(_frac_latex(b), unit)}."
    )
    answer = format_with_unit(_frac_latex(a * b), unit, power=2)
    assert r"\frac{3}{2}\text{ cm}" in latex
    assert r"\frac{1}{4}\text{ cm}" in latex
    assert "}cm" not in latex
    assert answer == r"\frac{3}{8}\text{ cm}^{2}"


def test_grade6_source_uses_helpers_not_bare_units():
    src = REPO_ROOT / "question_engine" / "frameworks" / "number.py"
    text = src.read_text(encoding="utf-8")
    assert "format_with_unit(frac_latex(a), unit)" in text
    assert "{frac_latex(a)}{unit}" not in text
    assert r"{frac_latex(area)}\ {unit}^2" not in text
    assert "format_with_unit(frac_latex(area), unit, power=2)" in text
