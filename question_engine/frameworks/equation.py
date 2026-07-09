"""Equation generator framework — base for one/two/multi-step linear equations."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

from .base import QuestionFramework
from ..generators.utils import format_equation_latex, pick_operation


@dataclass(frozen=True)
class EquationParams:
    variable: str = "x"
    coef_min: int = -12
    coef_max: int = 12


def equation_params_from_settings(settings: dict, *, variable: str = "x") -> EquationParams:
    return EquationParams(
        variable=variable,
        coef_min=int(settings.get("coef_min", -12)),
        coef_max=int(settings.get("coef_max", 12)),
    )


class EquationFramework(QuestionFramework):
    """Shared batch generation for equation-solving question types."""

    steps: int = 1

    def build_metadata(self, settings: dict) -> dict:
        return {"steps": self.steps}


class LinearEquationFramework(EquationFramework):
    """Configurable linear equation builder (1–3 step variants)."""

    def __init__(self, steps: int = 1, builder: Callable[[], tuple[str, str, str]] | None = None):
        self.steps = steps
        self._builder = builder

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self._builder:
            prompt_latex, prompt_text, answer = self._builder()
            return prompt_latex, prompt_text, answer

        params = equation_params_from_settings(settings, variable="x")
        x = random.randint(params.coef_min, params.coef_max)
        a = random.randint(1, max(2, params.coef_max // 2))
        if self.steps == 1:
            op = pick_operation(["+", "-"])
            b = x + a if op == "+" else x - a
            prompt = format_equation_latex(f"{params.variable} {op} {a}", str(b))
            return prompt, prompt, str(x)

        b = random.randint(-15, 15)
        rhs = a * x + b
        sign = "+" if b >= 0 else "-"
        prompt = format_equation_latex(f"{a}{params.variable} {sign} {abs(b)}", str(rhs))
        return prompt, prompt, str(x)


class OneStepEquationsFramework(EquationFramework):
    """One-step equations with +, -, *, / operations."""

    steps = 1
    instruction_latex = r"\text{Solve for } x."
    instruction_text = "Solve for x."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        x = random.randint(params.coef_min, params.coef_max)
        a = random.randint(1, 15)
        op = pick_operation(["+", "-", "*", "/"])
        if op == "+":
            b = x + a
            prompt = format_equation_latex(f"x + {a}", str(b))
            answer = str(x)
        elif op == "-":
            b = x - a
            prompt = format_equation_latex(f"x - {a}", str(b))
            answer = str(x)
        elif op == "*":
            if x == 0:
                x = random.randint(1, 12)
            a = random.randint(2, 9)
            b = x * a
            prompt = format_equation_latex(f"{a}x", str(b))
            answer = str(x)
        else:
            a = random.randint(2, 9)
            b = x * a
            prompt = f"\\frac{{x}}{{{a}}} = {b // a if b % a == 0 else b}"
            if b % a != 0:
                b = a * x
                prompt = f"\\frac{{x}}{{{a}}} = {x}"
            answer = str(x)
        prompt_text = prompt.replace("\\frac", "frac")
        return prompt, prompt_text, answer
