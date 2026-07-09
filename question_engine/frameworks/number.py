"""Number generator framework — rationals, decimals, percents."""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction

from .base import QuestionFramework
from ..generators.utils import frac_latex, random_fraction


@dataclass(frozen=True)
class NumberParams:
    num_min: int = -10
    num_max: int = 10
    denom_min: int = 2
    denom_max: int = 12


def number_params_from_settings(settings: dict) -> NumberParams:
    return NumberParams(
        num_min=int(settings.get("coef_min", settings.get("num_min", -10))),
        num_max=int(settings.get("coef_max", settings.get("num_max", 10))),
        denom_min=int(settings.get("denom_min", 2)),
        denom_max=int(settings.get("denom_max", 12)),
    )


class NumberFramework(QuestionFramework):
    """Shared batch generation for numeric expression types."""


class RationalFramework(NumberFramework):
    """Adding/subtracting/multiplying/dividing rational numbers."""

    def __init__(self, operation: str = "+"):
        self.operation = operation

    def _random_fraction(self, params: NumberParams) -> Fraction:
        return random_fraction(
            num_min=params.num_min,
            num_max=params.num_max,
            denom_min=params.denom_min,
            denom_max=params.denom_max,
        )

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        a, b = self._random_fraction(params), self._random_fraction(params)
        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }
        op = self.operation
        result = ops[op](a, b)
        latex_op = {"+": "+", "-": "-", "*": "\\cdot", "/": "\\div"}[op]
        prompt_latex = f"{frac_latex(a)} {latex_op} {frac_latex(b)}"
        return prompt_latex, f"{a} {op} {b}", frac_latex(result)


class PercentFramework(NumberFramework):
    """Percent-of and percent-change word prompts."""

    def __init__(self, *, percent_change: bool = False):
        self.percent_change = percent_change

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        if self.percent_change:
            original = random.randint(20, 200)
            change = random.randint(5, 40)
            increased = random.choice([True, False])
            new_value = original + change if increased else original - change
            pct = round(abs(change) / original * 100, 1)
            direction = "increase" if increased else "decrease"
            prompt = f"\\text{{From {original} to {new_value}, find the percent {direction}.}}"
            return prompt, f"From {original} to {new_value}", f"{pct}\\%"

        percent = random.choice([5, 10, 12, 15, 20, 25, 30, 40, 50, 75])
        base = random.randint(10, 200)
        result = percent * base / 100
        prompt = f"\\text{{What is {percent}\\% of {base}?}}"
        answer = str(result).rstrip("0").rstrip(".")
        return prompt, f"What is {percent}% of {base}?", answer
