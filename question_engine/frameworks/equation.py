"""Equation and inequality generator frameworks."""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any

from .base import QuestionFramework
from .graphing import (
    include_graph_metadata,
    metadata_from_number_line_spec,
    number_line_metadata,
    number_line_spec_from_symbol_and_value,
)
from ..core.metadata import question_metadata
from ..generators.utils import (
    format_equation_latex,
    format_linear_latex,
    format_monomial_latex,
    frac_latex,
    pick_operation,
    random_fraction,
    random_int_range,
)
from ..settings.params import (
    allowed_equation_operations,
    allowed_inequality_symbols,
    equation_params_from_settings,
    format_solution_value,
    pick_equation_solution,
)


def _normalize_inequality_symbol(symbol: str) -> str:
    """Keep answer-key inequality symbols in LaTeX (not ASCII ``<=`` / ``>=``)."""
    mapping = {
        "<=": r"\leq",
        ">=": r"\geq",
        r"\le": r"\leq",
        r"\ge": r"\geq",
    }
    return mapping.get(symbol, symbol)


def _flip_inequality_symbol(symbol: str) -> str:
    symbol = _normalize_inequality_symbol(symbol)
    return {
        "<": ">",
        ">": "<",
        r"\leq": r"\geq",
        r"\geq": r"\leq",
    }.get(symbol, symbol)


def _inequality_answer(
    symbol: str,
    value: int | Fraction,
    variable: str = "x",
    settings: dict | None = None,
) -> str:
    return (
        f"{variable} {_normalize_inequality_symbol(symbol)} "
        f"{format_solution_value(value, settings)}"
    )


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
                prompt = format_equation_latex(
                    format_monomial_latex(a, variable=var) or "0",
                    frac_latex(b),
                )
            else:
                b = int(x) * a
                prompt = format_equation_latex(
                    format_monomial_latex(a, variable=var) or "0",
                    str(b),
                )
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
        # Nonzero constant so the prompt is structurally two-step (not ax = c).
        b = random_int_range(params.coef_min, params.coef_max, exclude={0})

        if isinstance(x, Fraction):
            rhs = a * x + b
            prompt = format_equation_latex(
                format_linear_latex(a, b, variable=var),
                frac_latex(rhs),
            )
        else:
            rhs = a * int(x) + b
            prompt = format_equation_latex(format_linear_latex(a, b, variable=var), str(rhs))

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
        c = random_int_range(params.coef_min, params.coef_max, exclude={0})

        left = f"{a}({var} + {b})"
        if c > 0:
            left = f"{left} + {c}"
        else:
            left = f"{left} - {abs(c)}"

        if isinstance(x, Fraction):
            rhs = a * (x + b) + c
            prompt = format_equation_latex(left, frac_latex(rhs))
        else:
            rhs = a * (int(x) + b) + c
            prompt = format_equation_latex(left, str(rhs))

        return prompt, prompt, format_solution_value(x, settings)


class LiteralEquationsFramework(EquationFramework):
    """Solve a formula for a specified variable (true literal equations)."""

    steps = 2
    instruction_latex = r"\text{Solve for the indicated variable.}"
    instruction_text = "Solve for the indicated variable."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        tier = str(settings.get("difficulty_tier", "medium")).lower()
        params = equation_params_from_settings(settings)
        a = abs(_coef_in_range(params, settings, minimum=2)) or 2
        b = abs(_coef_in_range(params, settings, minimum=2)) or 2
        if a == b:
            b = a + 1

        if tier == "easy":
            form = random.choice(["area", "distance", "interest"])
            if form == "area":
                prompt = r"A = \ell w \quad \text{Solve for } w."
                answer = r"w = \frac{A}{\ell}"
            elif form == "distance":
                prompt = r"d = r t \quad \text{Solve for } t."
                answer = r"t = \frac{d}{r}"
            else:
                prompt = r"I = p r t \quad \text{Solve for } r."
                answer = r"r = \frac{I}{p t}"
        elif tier == "medium":
            form = random.choice(["standard", "slope_intercept"])
            if form == "standard":
                c = random_int_range(params.coef_min, params.coef_max, exclude={0})
                ax = format_monomial_latex(a, variable="x") or "0"
                by = format_monomial_latex(b, variable="y") or "0"
                prompt = f"{ax} + {by} = {c} \\quad \\text{{Solve for }} y."
                answer = f"y = \\frac{{{c} - {ax}}}{{{b}}}"
            else:
                prompt = (
                    f"y = {format_linear_latex(a, b)} \\quad \\text{{Solve for }} x."
                )
                answer = f"x = \\frac{{y - {b}}}{{{a}}}"
        else:
            form = random.choice(["triangle", "volume", "point_slope"])
            if form == "triangle":
                prompt = r"A = \frac{1}{2} b h \quad \text{Solve for } h."
                answer = r"h = \frac{2A}{b}"
            elif form == "volume":
                prompt = r"V = \ell w h \quad \text{Solve for } w."
                answer = r"w = \frac{V}{\ell h}"
            else:
                x1 = random.randint(1, min(6, max(1, params.coef_max)))
                y1 = random.randint(1, min(6, max(1, params.coef_max)))
                prompt = (
                    f"y - {y1} = {a}(x - {x1}) \\quad \\text{{Solve for }} y."
                )
                answer = f"y = {format_linear_latex(a, y1 - a * x1)}"

        return prompt, prompt, answer


def _nonzero_coef(params, settings: dict, *, minimum_abs: int = 1) -> int:
    lo = params.coef_min
    hi = params.coef_max
    if lo > hi:
        lo, hi = hi, lo
    candidates = [value for value in range(lo, hi + 1) if abs(value) >= minimum_abs]
    if bool(settings.get("exclude_zero_coefficients", True)):
        candidates = [value for value in candidates if value != 0]
    if candidates:
        return random.choice(candidates)
    if hi >= minimum_abs:
        return minimum_abs
    if lo <= -minimum_abs:
        return -minimum_abs
    return 1


def _linear_latex(a: int, var: str, b: int) -> str:
    return format_linear_latex(a, b, variable=var)


def _abs_linear_latex(a: int, var: str, b: int) -> str:
    return f"|{_linear_latex(a, var, b)}|"


def _factored_abs_latex(a: int, var: str, shift: int) -> str:
    if shift == 0:
        return _abs_linear_latex(a, var, 0)
    inner = f"{var} + {shift}" if shift > 0 else f"{var} - {abs(shift)}"
    if a == 1:
        return f"|{inner}|"
    if a == -1:
        return f"|-({inner})|"
    return f"|{a}({inner})|"


def _value_latex(value: int | Fraction) -> str:
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(int(value))
        return frac_latex(value)
    return str(value)


def _solution_is_clean(value: Fraction, *, integer_only: bool) -> bool:
    return (not integer_only) or value.denominator == 1


def _normalize_solution(value: Fraction) -> int | Fraction:
    return int(value) if value.denominator == 1 else value


def _format_abs_equation_answer(
    solutions: list[int | Fraction],
    settings: dict,
    var: str,
) -> str:
    unique: list[int | Fraction] = []
    seen: set[Fraction] = set()
    for raw in solutions:
        frac = Fraction(raw).limit_denominator()
        if frac in seen:
            continue
        seen.add(frac)
        unique.append(_normalize_solution(frac))
    unique.sort(key=lambda item: float(item))
    if not unique:
        return r"\text{no solution}"
    parts = [f"{var} = {format_solution_value(value, settings)}" for value in unique]
    if len(parts) == 1:
        return parts[0]
    return r" \text{ or } ".join(parts)


def _solutions_for_abs_equals_const(
    a: int,
    b: int,
    rhs: int | Fraction,
    *,
    integer_only: bool,
) -> list[int | Fraction] | None:
    """Solve |ax + b| = rhs; return clean solutions or None if unusable."""
    if rhs < 0:
        return []
    if a == 0:
        return [_normalize_solution(Fraction(0))] if abs(b) == rhs else []
    candidates = [
        Fraction(rhs - b, a),
        Fraction(-rhs - b, a),
    ]
    if rhs == 0:
        candidates = [Fraction(-b, a)]
    solutions: list[int | Fraction] = []
    seen: set[Fraction] = set()
    for cand in candidates:
        if not _solution_is_clean(cand, integer_only=integer_only):
            return None
        if cand in seen:
            continue
        seen.add(cand)
        solutions.append(_normalize_solution(cand))
    return solutions


_ABS_FORM_KEYS = (
    ("basic", "allow_basic"),
    ("isolated_right", "allow_isolated_right"),
    ("simple", "allow_simple"),
    ("abs_plus_constant", "allow_abs_plus_constant"),
    ("factored_inside", "allow_factored_inside"),
    ("coeff_outside", "allow_coeff_outside"),
    ("abs_equals_abs", "allow_abs_equals_abs"),
    ("abs_equals_linear", "allow_abs_equals_linear"),
)


def _enabled_abs_forms(settings: dict) -> list[str]:
    forms = [name for name, key in _ABS_FORM_KEYS if bool(settings.get(key, name in {"basic", "isolated_right", "simple", "abs_plus_constant", "factored_inside"}))]
    return forms or ["basic"]


class AbsoluteValueEquationsFramework(EquationFramework):
    """Absolute value equations with selectable prompt forms."""

    steps = 2
    instruction_latex = r"\text{Solve.}"
    instruction_text = "Solve."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        forms = _enabled_abs_forms(settings)
        for _ in range(80):
            form = random.choice(forms)
            built = self._try_build_form(form, settings, params)
            if built is not None:
                return built
        for form in forms:
            built = self._try_build_form(form, settings, params)
            if built is not None:
                return built
        var = params.variable
        prompt = format_equation_latex(f"|{var}|", "1")
        return prompt, prompt, f"{var} = -1 \\text{{ or }} {var} = 1"

    def _try_build_form(
        self,
        form: str,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        builders = {
            "basic": self._build_basic,
            "isolated_right": self._build_isolated_right,
            "simple": self._build_simple,
            "abs_plus_constant": self._build_abs_plus_constant,
            "factored_inside": self._build_factored_inside,
            "coeff_outside": self._build_coeff_outside,
            "abs_equals_abs": self._build_abs_equals_abs,
            "abs_equals_linear": self._build_abs_equals_linear,
        }
        builder = builders.get(form)
        if builder is None:
            return None
        return builder(settings, params)

    def _build_basic(self, settings: dict, params) -> tuple[str, str, str | None] | None:
        var = params.variable
        a = _nonzero_coef(params, settings)
        if params.integer_only:
            # b multiple of a ⇒ both ± branches stay integer.
            mult = random.randint(-4, 4)
            b = a * mult
        else:
            b = random.randint(params.coef_min, params.coef_max)
        x = _pick_solution(settings, params)
        inner = a * Fraction(x) + b
        rhs = abs(inner)
        solutions = _solutions_for_abs_equals_const(a, b, rhs, integer_only=params.integer_only)
        if solutions is None:
            return None
        lhs = _abs_linear_latex(a, var, b)
        prompt = format_equation_latex(lhs, _value_latex(rhs))
        return prompt, prompt, _format_abs_equation_answer(solutions, settings, var)

    def _build_isolated_right(
        self,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        built = self._build_basic(settings, params)
        if built is None:
            return None
        prompt, _, answer = built
        left, right = prompt.split(" = ", 1)
        swapped = format_equation_latex(right, left)
        return swapped, swapped, answer

    def _build_simple(self, settings: dict, params) -> tuple[str, str, str | None] | None:
        var = params.variable
        raw = _pick_solution(settings, params)
        c = abs(int(Fraction(raw)))
        if c == 0 and bool(settings.get("exclude_zero_solutions", False)):
            c = random.randint(1, max(1, abs(params.coef_max)))
        prompt = format_equation_latex(f"|{var}|", str(c))
        solutions: list[int | Fraction] = [0] if c == 0 else [c, -c]
        return prompt, prompt, _format_abs_equation_answer(solutions, settings, var)

    def _build_abs_plus_constant(
        self,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        var = params.variable
        a = _nonzero_coef(params, settings)
        if params.integer_only:
            b = a * random.randint(-4, 4)
        else:
            b = random.randint(params.coef_min, params.coef_max)
        x = _pick_solution(settings, params)
        inner_abs = abs(a * Fraction(x) + b)
        k = random.randint(1, max(1, min(8, abs(params.coef_max) or 8)))
        use_plus = random.choice([True, False])
        if use_plus:
            d = inner_abs + k
            lhs = f"{_abs_linear_latex(a, var, b)} + {k}"
            rhs_abs = d - k
        else:
            d = inner_abs - k
            lhs = f"{_abs_linear_latex(a, var, b)} - {k}"
            rhs_abs = d + k
        if rhs_abs < 0:
            return None
        solutions = _solutions_for_abs_equals_const(
            a, b, rhs_abs, integer_only=params.integer_only
        )
        if solutions is None:
            return None
        prompt = format_equation_latex(lhs, _value_latex(d))
        return prompt, prompt, _format_abs_equation_answer(solutions, settings, var)

    def _build_factored_inside(
        self,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        var = params.variable
        a = _nonzero_coef(params, settings, minimum_abs=2)
        shift = random.randint(1, max(1, min(6, abs(params.coef_max) or 6)))
        if random.choice([True, False]):
            shift = -shift
        x = _pick_solution(settings, params)
        # |a(x + shift)| = |a|·|x + shift|
        rhs = abs(a) * abs(Fraction(x) + shift)
        # Equivalent linear form: a x + a*shift
        b = a * shift
        solutions = _solutions_for_abs_equals_const(a, b, rhs, integer_only=params.integer_only)
        if solutions is None:
            return None
        lhs = _factored_abs_latex(a, var, shift)
        prompt = format_equation_latex(lhs, _value_latex(rhs))
        return prompt, prompt, _format_abs_equation_answer(solutions, settings, var)

    def _build_coeff_outside(
        self,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        var = params.variable
        # Keep outside coefficient positive so RHS stays non-negative.
        a = abs(_nonzero_coef(params, settings, minimum_abs=2))
        b = random.randint(params.coef_min, params.coef_max)
        x = _pick_solution(settings, params)
        inner_abs = abs(Fraction(x) + b)
        c = a * inner_abs
        # a|x + b| = c  ⇒  |x + b| = c/a
        solutions = _solutions_for_abs_equals_const(1, b, Fraction(c, a), integer_only=params.integer_only)
        if solutions is None:
            return None
        abs_part = _abs_linear_latex(1, var, b)
        lhs = f"{a}{abs_part}"
        prompt = format_equation_latex(lhs, _value_latex(c))
        return prompt, prompt, _format_abs_equation_answer(solutions, settings, var)

    def _build_abs_equals_abs(
        self,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        var = params.variable
        a = _nonzero_coef(params, settings)
        c = _nonzero_coef(params, settings)
        b = random.randint(params.coef_min, params.coef_max)
        d = random.randint(params.coef_min, params.coef_max)
        # Reject identities / all-real / empty special cases.
        if a == c and b == d:
            return None
        if a == -c and b == -d:
            return None
        solutions: list[int | Fraction] = []
        seen: set[Fraction] = set()
        # |ax+b| = |cx+d|  ⇔  ax+b = cx+d  or  ax+b = -(cx+d)
        if a != c:
            cand = Fraction(d - b, a - c)
            if not _solution_is_clean(cand, integer_only=params.integer_only):
                return None
            if cand not in seen:
                seen.add(cand)
                solutions.append(_normalize_solution(cand))
        if a != -c:
            cand = Fraction(-d - b, a + c)
            if not _solution_is_clean(cand, integer_only=params.integer_only):
                return None
            if cand not in seen:
                seen.add(cand)
                solutions.append(_normalize_solution(cand))
        if not solutions:
            return None
        lhs = _abs_linear_latex(a, var, b)
        rhs = _abs_linear_latex(c, var, d)
        prompt = format_equation_latex(lhs, rhs)
        return prompt, prompt, _format_abs_equation_answer(solutions, settings, var)

    def _build_abs_equals_linear(
        self,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        """|ax + b| = cx + d — keep only candidates with cx + d ≥ 0."""
        var = params.variable
        integer_only = params.integer_only
        a = _nonzero_coef(params, settings)
        c_coef = _nonzero_coef(params, settings)
        if a == c_coef or a == -c_coef:
            return None

        x0 = _pick_solution(settings, params)
        if integer_only:
            x0_i = int(Fraction(x0))
            d = random.randint(0, max(3, abs(params.coef_max)))
            linear_at = c_coef * x0_i + d
            if linear_at < 0:
                d = -c_coef * x0_i + random.randint(0, 5)
                linear_at = c_coef * x0_i + d
            if linear_at < 0:
                return None
            if random.choice([True, False]):
                b = linear_at - a * x0_i
            else:
                b = -linear_at - a * x0_i
        else:
            b = random.randint(params.coef_min, params.coef_max)
            linear_at = abs(a * Fraction(x0) + b)
            d = linear_at - c_coef * Fraction(x0)

        if Fraction(b).denominator != 1:
            return None
        b_int = int(b)

        solutions: list[int | Fraction] = []
        seen: set[Fraction] = set()
        for cand in (
            Fraction(Fraction(d) - b_int, a - c_coef),
            Fraction(-Fraction(d) - b_int, a + c_coef),
        ):
            if not _solution_is_clean(cand, integer_only=integer_only):
                return None
            linear = c_coef * cand + Fraction(d)
            if linear < 0:
                continue
            if abs(a * cand + b_int) != linear:
                continue
            if cand in seen:
                continue
            seen.add(cand)
            solutions.append(_normalize_solution(cand))

        if not solutions:
            return None

        d_disp = _normalize_solution(Fraction(d))
        if isinstance(d_disp, int):
            rhs = _linear_latex(c_coef, var, d_disp)
        else:
            base = _linear_latex(c_coef, var, 0)
            if d_disp > 0:
                rhs = f"{base} + {_value_latex(d_disp)}"
            elif d_disp < 0:
                rhs = f"{base} - {_value_latex(-d_disp)}"
            else:
                rhs = base

        lhs = _abs_linear_latex(a, var, b_int)
        prompt = format_equation_latex(lhs, rhs)
        return prompt, prompt, _format_abs_equation_answer(solutions, settings, var)


class SolvingInequalityFramework(EquationFramework):
    """Base for symbolic inequality-solving frameworks."""

    instruction_latex = r"\text{Solve the inequality.}"
    instruction_text = "Solve the inequality."

    def __init__(self) -> None:
        self._inequality_graph: dict[str, Any] | None = None

    def _record_inequality_graph(
        self,
        symbol: str,
        boundary: float,
        *,
        boundary_high: float | None = None,
        outside: bool = False,
        inclusive: bool | None = None,
        inclusive_high: bool | None = None,
    ) -> None:
        self._inequality_graph = {
            "symbol": symbol,
            "boundary": boundary,
            "boundary_high": boundary_high,
            "outside": outside,
            "inclusive": inclusive,
            "inclusive_high": inclusive_high,
        }

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
        if graph is not None and include_graph_metadata(settings):
            spec = number_line_spec_from_symbol_and_value(
                str(graph["symbol"]),
                float(graph["boundary"]),
                settings,
                boundary_high=graph.get("boundary_high"),
                outside=bool(graph.get("outside", False)),
                inclusive=graph.get("inclusive"),
                inclusive_high=graph.get("inclusive_high"),
            )
            return metadata_from_number_line_spec(spec, prompt="blank")
        return number_line_metadata(answer, settings)


def _record_solution_boundary(
    framework: SolvingInequalityFramework,
    symbol: str,
    value: int | Fraction,
) -> None:
    framework._record_inequality_graph(symbol, float(value))


class OneStepInequalitiesFramework(SolvingInequalityFramework):
    """One-step inequalities with +, -, *, / (same op family as one-step equations)."""

    steps = 1

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _inequality_metadata(settings, steps=self.steps)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        var = params.variable
        symbol = _pick_inequality_symbol(settings)
        x = _pick_solution(settings, params)
        ops = allowed_equation_operations(settings)
        op = pick_operation(ops)
        a = _coef_in_range(params, settings, minimum=1)
        answer_symbol = symbol

        if op == "+":
            if isinstance(x, Fraction):
                rhs = x + a
                prompt = format_equation_latex(
                    f"{var} + {a}", frac_latex(rhs), relation=symbol
                )
            else:
                rhs = int(x) + a
                prompt = format_equation_latex(f"{var} + {a}", str(rhs), relation=symbol)
        elif op == "-":
            if isinstance(x, Fraction):
                rhs = x - a
                prompt = format_equation_latex(
                    f"{var} - {a}", frac_latex(rhs), relation=symbol
                )
            else:
                rhs = int(x) - a
                prompt = format_equation_latex(f"{var} - {a}", str(rhs), relation=symbol)
        elif op == "*":
            a = _coef_in_range(params, settings, minimum=2)
            # Keep multipliers positive on integer tiers so direction flips are rare.
            if bool(settings.get("integer_only", True)):
                a = abs(a) or 2
            if a < 0:
                answer_symbol = _flip_inequality_symbol(symbol)
            if isinstance(x, Fraction):
                rhs = a * x
                prompt = format_equation_latex(
                    format_monomial_latex(a, variable=var) or "0",
                    frac_latex(rhs),
                    relation=symbol,
                )
            else:
                rhs = a * int(x)
                prompt = format_equation_latex(
                    format_monomial_latex(a, variable=var) or "0",
                    str(rhs),
                    relation=symbol,
                )
        else:
            a = _coef_in_range(params, settings, minimum=2)
            if bool(settings.get("integer_only", True)):
                a = abs(a) or 2
                k = _pick_solution(settings, params)
                if isinstance(k, Fraction):
                    k = int(k) if k.denominator == 1 else random.randint(1, 5)
                x = a * int(k)
                rhs = int(k)
                prompt = f"\\frac{{{var}}}{{{a}}} {symbol} {rhs}"
            else:
                if a < 0:
                    answer_symbol = _flip_inequality_symbol(symbol)
                if isinstance(x, Fraction):
                    rhs = x / a
                    prompt = f"\\frac{{{var}}}{{{a}}} {symbol} {frac_latex(rhs)}"
                else:
                    rhs = Fraction(int(x), a)
                    prompt = f"\\frac{{{var}}}{{{a}}} {symbol} {frac_latex(rhs)}"

        answer = _inequality_answer(answer_symbol, x, var, settings)
        _record_solution_boundary(self, answer_symbol, x)
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
        a = abs(_coef_in_range(params, settings, minimum=2)) or 2
        b = random_int_range(params.coef_min, params.coef_max, exclude={0})

        if isinstance(x, Fraction):
            rhs = a * x + b
            prompt = format_equation_latex(
                format_linear_latex(a, b, variable=var),
                frac_latex(rhs),
                relation=symbol,
            )
        else:
            rhs = a * int(x) + b
            prompt = format_equation_latex(
                format_linear_latex(a, b, variable=var),
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
        c = random_int_range(params.coef_min, params.coef_max, exclude={0})

        left = f"{a}({var} + {b})"
        if c > 0:
            left = f"{left} + {c}"
        else:
            left = f"{left} - {abs(c)}"

        if isinstance(x, Fraction):
            rhs = a * (x + b) + c
            prompt = format_equation_latex(left, frac_latex(rhs), relation=symbol)
        else:
            rhs = a * (int(x) + b) + c
            prompt = format_equation_latex(left, str(rhs), relation=symbol)

        answer = _inequality_answer(symbol, x, var, settings)
        _record_solution_boundary(self, symbol, x)
        return prompt, prompt, answer


class CompoundInequalitiesFramework(SolvingInequalityFramework):
    """Compound inequalities with Easy / Medium / Hard structural tiers via ``steps``."""

    steps = 2

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        steps = int(settings.get("steps", self.steps))
        return _inequality_metadata(settings, steps=steps)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        steps = int(settings.get("steps", self.steps))
        style = _compound_style(settings)
        if steps <= 1:
            return self._build_isolated(settings, params, style)
        if steps == 2:
            return self._build_middle_expression(settings, params, style)
        return self._build_hard(settings, params, style)

    def _record_interval(
        self,
        low: float,
        high: float,
        *,
        left_sym: str,
        right_sym: str,
        outside: bool = False,
    ) -> None:
        if outside:
            # left_sym is < / ≤ for the left ray; right_sym is > / ≥ for the right ray.
            self._record_inequality_graph(
                left_sym,
                low,
                boundary_high=high,
                outside=True,
                inclusive=left_sym in {r"\leq", "<="},
                inclusive_high=right_sym in {r"\geq", ">=", r"\leq", "<="},
            )
            return
        self._record_inequality_graph(
            left_sym,
            low,
            boundary_high=high,
            outside=False,
            inclusive=left_sym in {r"\leq", "<="},
            inclusive_high=right_sym in {r"\leq", "<="},
        )

    def _build_isolated(
        self,
        settings: dict,
        params,
        style: str,
    ) -> tuple[str, str, str | None]:
        var = params.variable
        low, high = _pick_ordered_bounds(params)
        left_sym, right_sym = _pick_chain_symbols(settings)
        if style == "or":
            left, right = _or_ray_symbols(settings, left_sym, right_sym)
            prompt = (
                f"{var} {_sym_text(left)} {low} \\text{{ or }} "
                f"{var} {_sym_text(right)} {high}"
            )
            self._record_interval(
                float(low), float(high), left_sym=left, right_sym=right, outside=True
            )
            return prompt, prompt, prompt

        prompt = f"{low} {_sym_text(left_sym)} {var} {_sym_text(right_sym)} {high}"
        self._record_interval(float(low), float(high), left_sym=left_sym, right_sym=right_sym)
        return prompt, prompt, prompt

    def _build_middle_expression(
        self,
        settings: dict,
        params,
        style: str,
    ) -> tuple[str, str, str | None]:
        var = params.variable
        a = abs(_coef_in_range(params, settings, minimum=2))
        b = random.randint(params.coef_min, params.coef_max)
        sol_low, sol_high = _pick_ordered_bounds(params, span_min=2)
        left_bound = a * sol_low + b
        right_bound = a * sol_high + b
        left_sym, right_sym = _pick_chain_symbols(settings)
        middle = _linear_latex(a, var, b)

        if style == "or":
            left, right = _or_ray_symbols(settings, left_sym, right_sym)
            prompt = (
                f"{middle} {_sym_text(left)} {left_bound} \\text{{ or }} "
                f"{middle} {_sym_text(right)} {right_bound}"
            )
            answer = (
                f"{var} {_sym_text(left)} {sol_low} \\text{{ or }} "
                f"{var} {_sym_text(right)} {sol_high}"
            )
            self._record_interval(
                float(sol_low),
                float(sol_high),
                left_sym=left,
                right_sym=right,
                outside=True,
            )
            return prompt, prompt, answer

        prompt = (
            f"{left_bound} {_sym_text(left_sym)} {middle} "
            f"{_sym_text(right_sym)} {right_bound}"
        )
        answer = (
            f"{sol_low} {_sym_text(left_sym)} {var} "
            f"{_sym_text(right_sym)} {sol_high}"
        )
        self._record_interval(
            float(sol_low), float(sol_high), left_sym=left_sym, right_sym=right_sym
        )
        return prompt, prompt, answer

    def _build_hard(
        self,
        settings: dict,
        params,
        style: str,
    ) -> tuple[str, str, str | None]:
        if random.choice([True, False]):
            return self._build_distributed_chain(settings, params, style)
        return self._build_joined_pair(settings, params, style)

    def _build_distributed_chain(
        self,
        settings: dict,
        params,
        style: str,
    ) -> tuple[str, str, str | None]:
        """``L ⊙ a(x ± b) ± c ⊙ R`` — distribute then isolate."""
        if style == "or":
            return self._build_middle_expression(settings, params, "or")

        var = params.variable
        a = abs(_coef_in_range(params, settings, minimum=2))
        shift = random.randint(1, max(1, min(6, abs(params.coef_max) or 6)))
        if random.choice([True, False]):
            shift = -shift
        c = random.randint(params.coef_min, params.coef_max)
        sol_low, sol_high = _pick_ordered_bounds(params, span_min=2)
        left_bound = a * (sol_low + shift) + c
        right_bound = a * (sol_high + shift) + c
        left_sym, right_sym = _pick_chain_symbols(settings)
        inner = f"{var} + {shift}" if shift > 0 else f"{var} - {abs(shift)}"
        if c == 0:
            middle = f"{a}({inner})"
        else:
            c_sign = "+" if c >= 0 else "-"
            middle = f"{a}({inner}) {c_sign} {abs(c)}"

        prompt = (
            f"{left_bound} {_sym_text(left_sym)} {middle} "
            f"{_sym_text(right_sym)} {right_bound}"
        )
        answer = (
            f"{sol_low} {_sym_text(left_sym)} {var} "
            f"{_sym_text(right_sym)} {sol_high}"
        )
        self._record_interval(
            float(sol_low), float(sol_high), left_sym=left_sym, right_sym=right_sym
        )
        return prompt, prompt, answer

    def _build_joined_pair(
        self,
        settings: dict,
        params,
        style: str,
    ) -> tuple[str, str, str | None]:
        """Two inequalities joined by and/or; each side needs solving."""
        var = params.variable
        a1 = abs(_coef_in_range(params, settings, minimum=2))
        a2 = abs(_coef_in_range(params, settings, minimum=2))
        b1 = random.randint(params.coef_min, params.coef_max)
        b2 = random.randint(params.coef_min, params.coef_max)
        sol_low, sol_high = _pick_ordered_bounds(params, span_min=2)
        left_sym, right_sym = _pick_chain_symbols(settings)
        left_expr = _linear_latex(a1, var, b1)
        right_expr = _linear_latex(a2, var, b2)

        if style == "and":
            upper_bound = a1 * sol_high + b1
            lower_bound = a2 * sol_low + b2
            upper = right_sym
            lower = ">" if left_sym == "<" else r"\geq"
            prompt = (
                f"{left_expr} {_sym_text(upper)} {upper_bound} \\text{{ and }} "
                f"{right_expr} {_sym_text(lower)} {lower_bound}"
            )
            answer = (
                f"{sol_low} {_sym_text(left_sym)} {var} "
                f"{_sym_text(right_sym)} {sol_high}"
            )
            self._record_interval(
                float(sol_low), float(sol_high), left_sym=left_sym, right_sym=right_sym
            )
            return prompt, prompt, answer

        left, right = _or_ray_symbols(settings, left_sym, right_sym)
        left_bound = a1 * sol_low + b1
        right_bound = a2 * sol_high + b2
        prompt = (
            f"{left_expr} {_sym_text(left)} {left_bound} \\text{{ or }} "
            f"{right_expr} {_sym_text(right)} {right_bound}"
        )
        answer = (
            f"{var} {_sym_text(left)} {sol_low} \\text{{ or }} "
            f"{var} {_sym_text(right)} {sol_high}"
        )
        self._record_interval(
            float(sol_low), float(sol_high), left_sym=left, right_sym=right, outside=True
        )
        return prompt, prompt, answer


def _compound_style(settings: dict) -> str:
    style = str(settings.get("compound_style", "and")).strip().lower()
    if style == "mixed":
        return random.choice(["and", "or"])
    if style in {"and", "or"}:
        return style
    return "and"


def _compound_allow_inclusive(settings: dict) -> bool:
    if "allow_inclusive" in settings:
        return bool(settings.get("allow_inclusive"))
    return bool(settings.get("allow_lte", True) or settings.get("allow_gte", True))


def _pick_chain_symbols(settings: dict) -> tuple[str, str]:
    """Pick left/right symbols for L ⊙ expr ⊙ R (both less-than oriented)."""
    inclusive = _compound_allow_inclusive(settings)
    left_choices = [r"\leq", "<"] if inclusive else ["<"]
    right_choices = [r"\leq", "<"] if inclusive else ["<"]
    if not bool(settings.get("allow_lt", True)):
        left_choices = [s for s in left_choices if s != "<"]
        right_choices = [s for s in right_choices if s != "<"]
    if not bool(settings.get("allow_lte", True)):
        left_choices = [s for s in left_choices if s != r"\leq"]
        right_choices = [s for s in right_choices if s != r"\leq"]
    if not left_choices:
        left_choices = ["<"]
    if not right_choices:
        right_choices = ["<"]
    return random.choice(left_choices), random.choice(right_choices)


def _or_ray_symbols(settings: dict, left_sym: str, right_sym: str) -> tuple[str, str]:
    """Map chain symbols onto left/right rays for an ``or`` compound."""
    if not _compound_allow_inclusive(settings):
        return "<", ">"
    left = "<" if left_sym == "<" else r"\leq"
    right = ">" if right_sym == "<" else r"\geq"
    return left, right


def _sym_text(symbol: str) -> str:
    """Keep LaTeX inequality symbols for prompt/answer rendering."""
    return symbol


def _pick_ordered_bounds(params, *, span_min: int = 2) -> tuple[int, int]:
    lo_cap = min(0, params.coef_max - span_min)
    high_floor = max(1, params.coef_min + span_min)
    low = random.randint(params.coef_min, max(params.coef_min, lo_cap))
    high = random.randint(
        max(high_floor, low + span_min),
        max(params.coef_max, low + span_min),
    )
    if high <= low:
        high = low + span_min
    return low, high


class AbsoluteValueInequalitiesFramework(SolvingInequalityFramework):
    """Absolute value inequalities with selectable prompt forms."""

    steps = 2

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _inequality_metadata(settings, steps=self.steps)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = equation_params_from_settings(settings)
        forms = _enabled_abs_inequality_forms(settings)
        for _ in range(80):
            form = random.choice(forms)
            built = self._try_build_form(form, settings, params)
            if built is not None:
                return built
        fallback = self._try_build_form("simple", settings, params)
        if fallback is not None:
            return fallback
        var = params.variable
        prompt = format_equation_latex(f"|{var}|", "1", relation="<")
        answer = f"-1 < {var} < 1"
        self._record_inequality_graph("<", -1.0, boundary_high=1.0)
        return prompt, prompt, answer

    def _try_build_form(
        self,
        form: str,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        builders = {
            "simple": self._build_simple,
            "shifted": self._build_shifted,
            "linear": self._build_linear,
            "abs_plus_constant": self._build_abs_plus_constant,
            "abs_vs_linear": self._build_abs_vs_linear,
        }
        builder = builders.get(form)
        if builder is None:
            return None
        return builder(settings, params)

    def _pick_relation(self, settings: dict, *, prefer_non_strict: bool | None = None) -> str:
        symbols = allowed_inequality_symbols(settings)
        if prefer_non_strict is True:
            non_strict = [s for s in symbols if s in {r"\leq", r"\geq"}]
            if non_strict:
                return random.choice(non_strict)
        if prefer_non_strict is False:
            strict = [s for s in symbols if s in {"<", ">"}]
            if strict:
                return random.choice(strict)
        return pick_operation(symbols)

    def _emit_abs_const_solution(
        self,
        *,
        a: int,
        b: int,
        radius: int | Fraction,
        relation: str,
        var: str,
        settings: dict,
        params,
        lhs: str,
        rhs_latex: str | None = None,
    ) -> tuple[str, str, str | None] | None:
        solved = _solve_abs_linear_vs_const(
            a, b, radius, relation, integer_only=params.integer_only
        )
        if solved is None:
            return None
        kind, lo, hi, symbol = solved
        prompt = format_equation_latex(lhs, rhs_latex or _value_latex(radius), relation=relation)
        if kind == "between":
            lo_s = format_solution_value(lo, settings)
            hi_s = format_solution_value(hi, settings)
            if symbol in {r"\leq", "<="}:
                answer = f"{lo_s} \\leq {var} \\leq {hi_s}"
                graph_symbol = r"\leq"
            else:
                answer = f"{lo_s} < {var} < {hi_s}"
                graph_symbol = "<"
            self._record_inequality_graph(
                graph_symbol, float(lo), boundary_high=float(hi), outside=False
            )
        else:
            lo_s = format_solution_value(lo, settings)
            hi_s = format_solution_value(hi, settings)
            if symbol in {r"\geq", ">="}:
                answer = f"{var} \\leq {lo_s} \\text{{ or }} {var} \\geq {hi_s}"
                graph_symbol = r"\geq"
            else:
                answer = f"{var} < {lo_s} \\text{{ or }} {var} > {hi_s}"
                graph_symbol = ">"
            self._record_inequality_graph(
                graph_symbol, float(lo), boundary_high=float(hi), outside=True
            )
        return prompt, prompt, answer

    def _build_simple(self, settings: dict, params) -> tuple[str, str, str | None] | None:
        var = params.variable
        relation = self._pick_relation(settings, prefer_non_strict=False)
        c = random.randint(1, max(2, min(8, abs(params.coef_max) or 8)))
        return self._emit_abs_const_solution(
            a=1,
            b=0,
            radius=c,
            relation=relation,
            var=var,
            settings=settings,
            params=params,
            lhs=f"|{var}|",
        )

    def _build_shifted(self, settings: dict, params) -> tuple[str, str, str | None] | None:
        var = params.variable
        # Easy-friendly: prefer interior solutions (|x - a| < c).
        relation = self._pick_relation(settings, prefer_non_strict=False)
        if relation in {">", r"\geq"} and random.random() < 0.55:
            relation = "<" if "<" in allowed_inequality_symbols(settings) else relation
        center = random.randint(params.coef_min, params.coef_max)
        if center == 0:
            center = random.choice([-3, -2, -1, 1, 2, 3])
        radius = random.randint(1, max(2, min(6, abs(params.coef_max) or 6)))
        # |x - center| = |1·x + (-center)|
        return self._emit_abs_const_solution(
            a=1,
            b=-center,
            radius=radius,
            relation=relation,
            var=var,
            settings=settings,
            params=params,
            lhs=_abs_linear_latex(1, var, -center),
        )

    def _build_linear(self, settings: dict, params) -> tuple[str, str, str | None] | None:
        var = params.variable
        # Medium: prefer ≤ / ≥ so students practice non-strict compound answers.
        relation = self._pick_relation(settings, prefer_non_strict=True)
        a = _nonzero_coef(params, settings, minimum_abs=2)
        if params.integer_only:
            b = a * random.randint(-3, 3)
        else:
            b = random.randint(params.coef_min, params.coef_max)
        radius = random.randint(2, max(3, min(12, abs(params.coef_max) or 12)))
        # Keep radius large enough that division by |a| still yields a gap.
        if radius < abs(a):
            radius = abs(a) * random.randint(1, 3)
        return self._emit_abs_const_solution(
            a=a,
            b=b,
            radius=radius,
            relation=relation,
            var=var,
            settings=settings,
            params=params,
            lhs=_abs_linear_latex(a, var, b),
        )

    def _build_abs_plus_constant(
        self,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        var = params.variable
        relation = self._pick_relation(settings)
        a = _nonzero_coef(params, settings, minimum_abs=1)
        if params.integer_only:
            b = a * random.randint(-3, 3)
        else:
            b = random.randint(params.coef_min, params.coef_max)
        k = random.randint(1, max(1, min(6, abs(params.coef_max) or 6)))
        # |ax+b| + k ⋈ d  with d > k so the reduced radius stays positive.
        reduced = random.randint(1, max(2, min(8, abs(params.coef_max) or 8)))
        d = reduced + k
        use_plus = random.choice([True, False])
        if use_plus:
            lhs = f"{_abs_linear_latex(a, var, b)} + {k}"
            effective_radius: int | Fraction = d - k
            # For minus form we would add k; plus form subtracts k from RHS.
        else:
            # |ax+b| - k ⋈ d  ⇒  |ax+b| ⋈ d+k (same relation)
            lhs = f"{_abs_linear_latex(a, var, b)} - {k}"
            effective_radius = d + k
            # Keep displayed RHS as d (can be smaller than k).
            if d <= 0:
                d = random.randint(1, 5)
                effective_radius = d + k
        return self._emit_abs_const_solution(
            a=a,
            b=b,
            radius=effective_radius,
            relation=relation,
            var=var,
            settings=settings,
            params=params,
            lhs=lhs,
            rhs_latex=_value_latex(d),
        )

    def _build_abs_vs_linear(
        self,
        settings: dict,
        params,
    ) -> tuple[str, str, str | None] | None:
        """|ax + b| ≥ cx + d with a clean two-ray solution (when possible)."""
        var = params.variable
        symbols = allowed_inequality_symbols(settings)
        non_strict_or = [s for s in symbols if s in {r"\geq", ">"}]
        if not non_strict_or:
            return None
        relation = random.choice(non_strict_or)
        inclusive = relation in {r"\geq", r"\leq"}

        # Keep endpoints modest so the constructed linear RHS stays readable.
        span = max(2, min(6, abs(params.coef_max) or 6))
        lo = random.randint(-span, -1)
        hi = random.randint(1, span)
        if hi - lo < 2:
            return None

        a = _nonzero_coef(params, settings, minimum_abs=2)
        # Prefer |a| not too large relative to the span.
        if abs(a) > 8:
            a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        c_coef = random.choice([1, -1])
        if a == c_coef or a == -c_coef:
            return None

        # Intersections on opposite V arms: left with -, right with +.
        # a*lo + b = -(c*lo + d)  and  a*hi + b = c*hi + d
        # ⇒ 2b = -lo(a+c) + hi(c-a),  2d = -lo(a+c) - hi(c-a)
        two_b = -lo * (a + c_coef) + hi * (c_coef - a)
        two_d = -lo * (a + c_coef) - hi * (c_coef - a)
        if two_b % 2 != 0 or two_d % 2 != 0:
            return None
        b = two_b // 2
        d = two_d // 2
        if abs(b) > 30 or abs(d) > 30:
            return None

        # Line must stay non-negative on [lo, hi] so the gap stays empty.
        for x in (lo, hi, (lo + hi) // 2):
            if c_coef * x + d < 0:
                return None
        # Spot-check the gap: abs should be strictly below the line inside.
        mid = Fraction(lo + hi, 2)
        if abs(a * mid + b) >= c_coef * mid + d:
            return None

        lhs = _abs_linear_latex(a, var, b)
        rhs = _linear_latex(c_coef, var, d)
        prompt = format_equation_latex(lhs, rhs, relation=relation)
        lo_s = format_solution_value(lo, settings)
        hi_s = format_solution_value(hi, settings)
        if inclusive:
            answer = f"{var} \\leq {lo_s} \\text{{ or }} {var} \\geq {hi_s}"
            graph_symbol = r"\geq"
        else:
            answer = f"{var} < {lo_s} \\text{{ or }} {var} > {hi_s}"
            graph_symbol = ">"
        self._record_inequality_graph(
            graph_symbol, float(lo), boundary_high=float(hi), outside=True
        )
        return prompt, prompt, answer


_ABS_INEQ_FORM_KEYS = (
    ("simple", "allow_simple"),
    ("shifted", "allow_shifted"),
    ("linear", "allow_linear"),
    ("abs_plus_constant", "allow_abs_plus_constant"),
    ("abs_vs_linear", "allow_abs_vs_linear"),
)


def _enabled_abs_inequality_forms(settings: dict) -> list[str]:
    defaults_on = {"simple", "shifted", "linear"}
    forms = [
        name
        for name, key in _ABS_INEQ_FORM_KEYS
        if bool(settings.get(key, name in defaults_on))
    ]
    return forms or ["simple"]


def _solve_abs_linear_vs_const(
    a: int,
    b: int,
    radius: int | Fraction,
    relation: str,
    *,
    integer_only: bool,
) -> tuple[str, int | Fraction, int | Fraction, str] | None:
    """Solve |ax + b| ⋈ radius.

    Returns ``(kind, lo, hi, boundary_symbol)`` where kind is ``between`` or
    ``outside``, or ``None`` when the solution is empty/all-reals/unclean.
    """
    if a == 0 or radius <= 0:
        return None

    between = relation in {"<", r"\leq", "<="}
    inclusive = relation in {r"\leq", r"\geq", "<=", ">="}
    # Critical points of |ax+b| = radius
    left = Fraction(-radius - b, a)
    right = Fraction(radius - b, a)
    if not _solution_is_clean(left, integer_only=integer_only):
        return None
    if not _solution_is_clean(right, integer_only=integer_only):
        return None
    lo_raw, hi_raw = (left, right) if left <= right else (right, left)
    if lo_raw == hi_raw:
        return None
    lo = _normalize_solution(lo_raw)
    hi = _normalize_solution(hi_raw)
    if between:
        return ("between", lo, hi, r"\leq" if inclusive else "<")
    return ("outside", lo, hi, r"\geq" if inclusive else ">")
