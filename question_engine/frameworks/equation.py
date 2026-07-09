"""Equation and inequality generator frameworks."""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any

from .base import QuestionFramework
from .graphing import (
    metadata_from_number_line_spec,
    number_line_metadata,
    number_line_spec_from_symbol_and_value,
)
from ..core.metadata import question_metadata
from ..generators.utils import format_equation_latex, frac_latex, pick_operation, random_fraction, random_int_range
from ..settings.params import (
    allowed_equation_operations,
    allowed_inequality_symbols,
    equation_params_from_settings,
    format_solution_value,
    pick_equation_solution,
)


def _inequality_symbol_text(symbol: str) -> str:
    return symbol.replace(r"\leq", "<=").replace(r"\geq", ">=")


def _inequality_answer(
    symbol: str,
    value: int | Fraction,
    variable: str = "x",
    settings: dict | None = None,
) -> str:
    return f"{variable} {_inequality_symbol_text(symbol)} {format_solution_value(value, settings)}"


def _inequality_metadata(settings: dict, *, steps: int) -> dict[str, Any]:
    return {"steps": steps}


def _pick_inequality_symbol(settings: dict) -> str:
    return pick_operation(allowed_inequality_symbols(settings))


def _coef_in_range(params, settings: dict, *, minimum: int = 1) -> int:
    lo = max(minimum, params.coef_min)
    hi = max(lo, params.coef_max)
    exclude: set[int] = set()
    if bool(settings.get("exclude_zero_coefficients", True)):
        exclude.add(0)
    return random.randint(lo, hi) if not exclude else random_int_range(lo, hi, exclude=exclude)


def _pick_solution(settings: dict, params) -> int | Fraction:
    return pick_equation_solution(settings, params)


class EquationFramework(QuestionFramework):
    """Shared batch generation for equation-solving question types."""

    steps: int = 1

    def build_metadata(self, settings: dict) -> dict:
        return {"steps": self.steps}


class OneStepEquationsFramework(EquationFramework):
    """One-step equations with +, -, *, / operations."""

    steps = 1
    instruction_latex = r"\text{Solve for } x."
    instruction_text = "Solve for x."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        x = _pick_solution(settings, params)
        if isinstance(x, Fraction) and x == 0:
            x = random_fraction(num_min=1, num_max=params.coef_max, denom_min=2, denom_max=6)

        ops = allowed_equation_operations(settings)
        op = pick_operation(ops)
        a = _coef_in_range(params, settings, minimum=1)

        if op == "+":
            if isinstance(x, Fraction):
                b = x + a
                prompt = format_equation_latex(f"{var} + {a}", frac_latex(b))
            else:
                b = int(x) + a
                prompt = format_equation_latex(f"{var} + {a}", str(b))
            answer = format_solution_value(x, settings)
        elif op == "-":
            if isinstance(x, Fraction):
                b = x - a
                prompt = format_equation_latex(f"{var} - {a}", frac_latex(b))
            else:
                b = int(x) - a
                prompt = format_equation_latex(f"{var} - {a}", str(b))
            answer = format_solution_value(x, settings)
        elif op == "*":
            if x == 0:
                x = _pick_solution(settings, params)
                if x == 0:
                    x = 1
            a = _coef_in_range(params, settings, minimum=2)
            if isinstance(x, Fraction):
                b = x * a
                prompt = format_equation_latex(f"{a}{var}", frac_latex(b))
            else:
                b = int(x) * a
                prompt = format_equation_latex(f"{a}{var}", str(b))
            answer = format_solution_value(x, settings)
        else:
            a = _coef_in_range(params, settings, minimum=2)
            if isinstance(x, Fraction):
                b = x * a
                prompt = f"\\frac{{{var}}}{{{a}}} = {frac_latex(b)}"
            else:
                b = int(x) * a
                prompt = f"\\frac{{{var}}}{{{a}}} = {b // a}"
            answer = format_solution_value(x, settings)

        prompt_text = prompt.replace("\\frac", "frac")
        return prompt, prompt_text, answer


class TwoStepEquationsFramework(EquationFramework):
    """Two-step linear equations of the form ax + b = c."""

    steps = 2
    instruction_latex = r"\text{Solve for } x."
    instruction_text = "Solve for x."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        x = _pick_solution(settings, params)
        a = _coef_in_range(params, settings, minimum=2)
        b = random.randint(params.coef_min, params.coef_max)

        if isinstance(x, Fraction):
            rhs = a * x + b
            sign = "+" if b >= 0 else "-"
            prompt = format_equation_latex(
                f"{a}{var} {sign} {abs(b)}",
                frac_latex(rhs),
            )
        else:
            rhs = a * int(x) + b
            sign = "+" if b >= 0 else "-"
            prompt = format_equation_latex(f"{a}{var} {sign} {abs(b)}", str(rhs))

        return prompt, prompt, format_solution_value(x, settings)


class MultiStepEquationsFramework(EquationFramework):
    """Multi-step equations of the form a(x + b) + c = rhs."""

    steps = 3
    instruction_latex = r"\text{Solve for } x."
    instruction_text = "Solve for x."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        x = _pick_solution(settings, params)
        a = random.randint(2, min(5, max(2, params.coef_max)))
        b = random.randint(1, min(6, max(1, params.coef_max)))
        c = random.randint(params.coef_min, params.coef_max)

        if isinstance(x, Fraction):
            rhs = a * (x + b) + c
            sign = "+" if c >= 0 else "-"
            prompt = format_equation_latex(
                f"{a}({var} + {b}) {sign} {abs(c)}",
                frac_latex(rhs),
            )
        else:
            rhs = a * (int(x) + b) + c
            sign = "+" if c >= 0 else "-"
            prompt = format_equation_latex(
                f"{a}({var} + {b}) {sign} {abs(c)}",
                str(rhs),
            )

        return prompt, prompt, format_solution_value(x, settings)


class AbsoluteValueEquationsFramework(EquationFramework):
    """Absolute value equations |ax + b| = |ax + b|."""

    steps = 2
    instruction_latex = r"\text{Solve for } x."
    instruction_text = "Solve for x."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        x = _pick_solution(settings, params)
        a = _coef_in_range(params, settings, minimum=1)
        b = random.randint(params.coef_min, params.coef_max)

        if isinstance(x, Fraction):
            inner = a * x + b
            rhs = abs(inner)
            b_sign = "+" if b >= 0 else "-"
            lhs = f"|{a}{var} {b_sign} {abs(b)}|" if b != 0 else f"|{a}{var}|"
            prompt = format_equation_latex(lhs, frac_latex(rhs))
        else:
            inner = a * int(x) + b
            rhs = abs(inner)
            b_sign = "+" if b >= 0 else "-"
            lhs = f"|{a}{var} {b_sign} {abs(b)}|" if b != 0 else f"|{a}{var}|"
            prompt = format_equation_latex(lhs, str(rhs))

        return prompt, prompt, format_solution_value(x, settings)


class SolvingInequalityFramework(EquationFramework):
    """Base for symbolic inequality-solving frameworks."""

    instruction_latex = r"\text{Solve the inequality.}"
    instruction_text = "Solve the inequality."

    def __init__(self) -> None:
        self._inequality_graph: tuple[str, float, float | None] | None = None

    def _record_inequality_graph(
        self,
        symbol: str,
        boundary: float,
        *,
        boundary_high: float | None = None,
    ) -> None:
        self._inequality_graph = (symbol, boundary, boundary_high)

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        graph = self._inequality_graph
        self._inequality_graph = None
        if graph is not None:
            symbol, boundary, boundary_high = graph
            spec = number_line_spec_from_symbol_and_value(
                symbol,
                boundary,
                settings,
                boundary_high=boundary_high,
            )
            return metadata_from_number_line_spec(spec)
        return number_line_metadata(answer, settings)


def _record_solution_boundary(
    framework: SolvingInequalityFramework,
    symbol: str,
    value: int | Fraction,
) -> None:
    framework._record_inequality_graph(symbol, float(value))


class OneStepInequalitiesFramework(SolvingInequalityFramework):
    """One-step inequalities (x + a symbol rhs)."""

    steps = 1

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _inequality_metadata(settings, steps=self.steps)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        symbol = _pick_inequality_symbol(settings)
        x = _pick_solution(settings, params)
        a = _coef_in_range(params, settings, minimum=1)

        if isinstance(x, Fraction):
            rhs = x + a
            prompt = format_equation_latex(f"{var} + {a}", frac_latex(rhs), relation=symbol)
        else:
            rhs = int(x) + a
            prompt = format_equation_latex(f"{var} + {a}", str(rhs), relation=symbol)

        answer = _inequality_answer(symbol, x, var, settings)
        _record_solution_boundary(self, symbol, x)
        return prompt, prompt, answer


class TwoStepInequalitiesFramework(SolvingInequalityFramework):
    """Two-step inequalities (ax + b symbol rhs)."""

    steps = 2

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _inequality_metadata(settings, steps=self.steps)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        symbol = _pick_inequality_symbol(settings)
        x = _pick_solution(settings, params)
        a = _coef_in_range(params, settings, minimum=2)
        b = random.randint(params.coef_min, params.coef_max)

        if isinstance(x, Fraction):
            rhs = a * x + b
            sign = "+" if b >= 0 else "-"
            prompt = format_equation_latex(
                f"{a}{var} {sign} {abs(b)}",
                frac_latex(rhs),
                relation=symbol,
            )
        else:
            rhs = a * int(x) + b
            sign = "+" if b >= 0 else "-"
            prompt = format_equation_latex(
                f"{a}{var} {sign} {abs(b)}",
                str(rhs),
                relation=symbol,
            )

        answer = _inequality_answer(symbol, x, var, settings)
        _record_solution_boundary(self, symbol, x)
        return prompt, prompt, answer


class MultiStepInequalitiesFramework(SolvingInequalityFramework):
    """Multi-step inequalities (a(x + b) + c symbol rhs)."""

    steps = 3

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _inequality_metadata(settings, steps=self.steps)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        symbol = _pick_inequality_symbol(settings)
        x = _pick_solution(settings, params)
        a = random.randint(2, min(4, max(2, params.coef_max)))
        b = random.randint(1, min(5, max(1, params.coef_max)))
        c = random.randint(params.coef_min, params.coef_max)

        if isinstance(x, Fraction):
            rhs = a * (x + b) + c
            sign = "+" if c >= 0 else "-"
            prompt = format_equation_latex(
                f"{a}({var} + {b}) {sign} {abs(c)}",
                frac_latex(rhs),
                relation=symbol,
            )
        else:
            rhs = a * (int(x) + b) + c
            sign = "+" if c >= 0 else "-"
            prompt = format_equation_latex(
                f"{a}({var} + {b}) {sign} {abs(c)}",
                str(rhs),
                relation=symbol,
            )

        answer = _inequality_answer(symbol, x, var, settings)
        _record_solution_boundary(self, symbol, x)
        return prompt, prompt, answer


class CompoundInequalitiesFramework(SolvingInequalityFramework):
    """Compound inequalities (and/or chains)."""

    steps = 2

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _inequality_metadata(settings, steps=self.steps)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        a = _coef_in_range(params, settings, minimum=1)
        style = str(settings.get("compound_style", "and"))

        if style == "or":
            low = random.randint(params.coef_min, 0)
            high = random.randint(1, params.coef_max)
            prompt = f"{var} < {low} \\text{{ or }} {var} > {high}"
            answer = f"{var} < {low} \\text{{ or }} {var} > {high}"
            return prompt, prompt, answer

        low = random.randint(params.coef_min, 0)
        high = random.randint(1, params.coef_max)
        prompt = f"{low} < {a}{var} < {high}"
        answer = f"{low / a:.2g} < {var} < {high / a:.2g}"
        self._record_inequality_graph("<", low / a, boundary_high=high / a)
        return prompt, prompt, answer


class AbsoluteValueInequalitiesFramework(SolvingInequalityFramework):
    """Absolute value inequalities |x - c| < r or > r."""

    steps = 2

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _inequality_metadata(settings, steps=self.steps)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        center = random.randint(params.coef_min, params.coef_max)
        radius = random.randint(2, max(3, abs(params.coef_max)))

        symbols = allowed_inequality_symbols(settings)
        strict = "<" in symbols or ">" in symbols
        if strict and (r"\leq" in symbols or r"\geq" in symbols):
            use_strict = random.choice([True, False])
        else:
            use_strict = "<" in symbols or ">" in symbols

        if use_strict:
            relation = "<"
            prompt = f"|{var} - {center}| {relation} {radius}"
            answer = f"{center - radius} < {var} < {center + radius}"
            self._record_inequality_graph("<", float(center - radius), boundary_high=float(center + radius))
        else:
            relation = r"\leq"
            prompt = f"|{var} - {center}| {relation} {radius}"
            answer = f"{center - radius} \\leq {var} \\leq {center + radius}"
            self._record_inequality_graph("<", float(center - radius), boundary_high=float(center + radius))

        return prompt, prompt, answer
