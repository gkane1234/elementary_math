"""Rational equation generators with structure-based difficulty tiers.

Easy   — single rational term equal to a constant (or a simple proportion).
Medium — fraction plus a constant, or a proportion with linear numerators.
Hard   — two rational terms (LCD), possibly with an extraneous candidate.

All tiers use integer coefficients. Solutions that make a denominator zero are
discarded as extraneous when they arise from clearing denominators.
"""

from __future__ import annotations

import random
from fractions import Fraction

from packages.polynomial_core import format_linear_latex

from ..settings.params import format_solution_value
from .utils import _make_questions, format_equation_latex


_FORM_KEYS = (
    ("simple_fraction", "allow_simple_fraction"),
    ("proportion", "allow_proportion"),
    ("fraction_plus_constant", "allow_fraction_plus_constant"),
    ("two_fractions", "allow_two_fractions"),
)


def _enabled_forms(settings: dict) -> list[str]:
    forms = [name for name, key in _FORM_KEYS if bool(settings.get(key, name == "simple_fraction"))]
    return forms or ["simple_fraction"]


def _coef_hi(settings: dict) -> int:
    return max(2, min(12, abs(int(settings.get("coef_max", 6))) or 6))


def _pick_int(lo: int, hi: int, *, nonzero: bool = False, positive: bool = False) -> int:
    if positive:
        lo = max(1, lo)
    if lo > hi:
        lo, hi = hi, lo
    for _ in range(40):
        value = random.randint(lo, hi)
        if nonzero and value == 0:
            continue
        return value
    if positive:
        return max(1, hi)
    if nonzero:
        return 1 if hi >= 1 else -1
    return lo


def _frac(num_latex: str, den_latex: str) -> str:
    return f"\\frac{{{num_latex}}}{{{den_latex}}}"


def _const_latex(value: int) -> str:
    return str(value)


def _format_answer(
    valid: list[int | Fraction],
    extraneous: list[int | Fraction],
    settings: dict,
    *,
    variable: str = "x",
) -> str | None:
    if not bool(settings.get("include_answer_key", False)):
        return None

    def _parts(values: list[int | Fraction]) -> list[str]:
        unique: list[int | Fraction] = []
        seen: set[Fraction] = set()
        for raw in values:
            frac = Fraction(raw).limit_denominator()
            if frac in seen:
                continue
            seen.add(frac)
            unique.append(int(frac) if frac.denominator == 1 else frac)
        unique.sort(key=lambda item: float(item))
        return [f"{variable} = {format_solution_value(v, settings)}" for v in unique]

    valid_parts = _parts(valid)
    extra_parts = _parts(extraneous)
    if not valid_parts:
        if extra_parts:
            discarded = r" \text{ or } ".join(extra_parts)
            return rf"\text{{no solution}};\ {discarded} \text{{ (extraneous)}}"
        return r"\text{no solution}"
    body = r" \text{ or } ".join(valid_parts)
    if extra_parts:
        discarded = r" \text{ or } ".join(extra_parts)
        return rf"{body};\ {discarded} \text{{ (extraneous)}}"
    return body


def _linear(a: int, b: int, *, variable: str = "x") -> str:
    return format_linear_latex(a, b, variable=variable)


def _build_simple_fraction(settings: dict) -> tuple[str, str, str | None] | None:
    """a/x = b, a/(x+c) = b, or (x+a)/b = c."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)
    style = random.choice(["over_x", "over_linear", "linear_over_const"])

    if style == "over_x":
        x = _pick_int(-hi, hi, nonzero=True)
        b = _pick_int(1, min(6, hi), nonzero=True)
        a = b * x
        if a == 0 or abs(a) > 36:
            return None
        prompt = format_equation_latex(_frac(_const_latex(a), var), _const_latex(b))
        return prompt, prompt, _format_answer([x], [], settings, variable=var)

    if style == "over_linear":
        # a/(x+c) = b  →  x = a/b - c
        b = _pick_int(1, min(6, hi), nonzero=True)
        x = _pick_int(-hi, hi, nonzero=True)
        c = _pick_int(-hi, hi, nonzero=True)
        a = b * (x + c)
        if a == 0 or abs(a) > 40 or x + c == 0:
            return None
        prompt = format_equation_latex(
            _frac(_const_latex(a), _linear(1, c, variable=var)),
            _const_latex(b),
        )
        return prompt, prompt, _format_answer([x], [], settings, variable=var)

    # (x+a)/b = c  →  x = bc - a
    b = _pick_int(2, min(8, hi), positive=True)
    c = _pick_int(-hi, hi, nonzero=True)
    a = _pick_int(-hi, hi, nonzero=True)
    x = b * c - a
    if abs(x) > 24:
        return None
    prompt = format_equation_latex(
        _frac(_linear(1, a, variable=var), _const_latex(b)),
        _const_latex(c),
    )
    return prompt, prompt, _format_answer([x], [], settings, variable=var)


def _build_proportion(settings: dict) -> tuple[str, str, str | None] | None:
    """a/x = b/c or (x+p)/q = r/s or a/(x+p) = b/(x+q)."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)
    style = random.choice(["const_over_x", "linear_over_const", "cross_linear"])

    if style == "const_over_x":
        # a/x = b/c  →  x = a*c/b
        b = _pick_int(1, min(6, hi), nonzero=True)
        c = _pick_int(2, min(8, hi), nonzero=True)
        k = _pick_int(1, min(5, hi), positive=True)
        a = b * k
        x = k * c
        if abs(x) > 30:
            return None
        rhs = _const_latex(b) if c == 1 else _frac(_const_latex(b), _const_latex(c))
        prompt = format_equation_latex(_frac(_const_latex(a), var), rhs)
        return prompt, prompt, _format_answer([x], [], settings, variable=var)

    if style == "linear_over_const":
        # (x+p)/q = r/s  →  s(x+p) = q r  →  x = (q r)/s - p
        q = _pick_int(2, min(8, hi), positive=True)
        s = _pick_int(1, min(6, hi), nonzero=True)
        r = _pick_int(-hi, hi, nonzero=True)
        p = _pick_int(-hi, hi)
        if (q * r) % s != 0:
            # Force integer solution.
            r = s * _pick_int(-3, 3, nonzero=True)
        x = (q * r) // s - p
        if abs(x) > 24:
            return None
        prompt = format_equation_latex(
            _frac(_linear(1, p, variable=var), _const_latex(q)),
            _frac(_const_latex(r), _const_latex(s)),
        )
        return prompt, prompt, _format_answer([x], [], settings, variable=var)

    # a/(x+p) = b/(x+q)  →  a(x+q) = b(x+p)  →  (a-b)x = b p - a q
    p = _pick_int(-hi, hi, nonzero=True)
    q = _pick_int(-hi, hi, nonzero=True)
    if p == q:
        q = p + _pick_int(1, 3, nonzero=True) * random.choice([-1, 1])
    a = _pick_int(1, min(6, hi), nonzero=True)
    b = _pick_int(1, min(6, hi), nonzero=True)
    if a == b:
        b = a + random.choice([-1, 1])
        if b == 0:
            b = a + 2
    # Choose x so dens are nonzero, then set consistency via cross-multiply.
    x = _pick_int(-hi, hi, nonzero=True)
    if x + p == 0 or x + q == 0:
        return None
    # Force a/(x+p) = b/(x+q) by choosing a from b and dens, or pick freely and solve.
    # Solve (a-b)x = bp - aq for integer x already chosen:
    # a(x+q) = b(x+p) ⇒ a = b(x+p)/(x+q) must be integer.
    den = x + q
    num = b * (x + p)
    if den == 0 or num % den != 0:
        return None
    a = num // den
    if a == 0 or a == b or abs(a) > 20:
        return None
    prompt = format_equation_latex(
        _frac(_const_latex(a), _linear(1, p, variable=var)),
        _frac(_const_latex(b), _linear(1, q, variable=var)),
    )
    # Extraneous if clearing dens produces the excluded root — not for this form
    # when a≠b (unique solution). Still report excluded dens if they somehow match.
    excluded = [-p, -q]
    extraneous = [e for e in excluded if e == x]
    valid = [] if x in extraneous else [x]
    return prompt, prompt, _format_answer(valid, extraneous, settings, variable=var)


def _build_fraction_plus_constant(settings: dict) -> tuple[str, str, str | None] | None:
    """a/x + b = c  or  a/(x+d) + b = c."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)
    use_shift = random.choice([True, False])

    b = _pick_int(-hi, hi, nonzero=True)
    c = _pick_int(-hi, hi, nonzero=True)
    if b == c:
        c = b + random.choice([-2, -1, 1, 2])
    # a/den + b = c  →  a/den = c-b  →  den = a/(c-b)
    diff = c - b
    if diff == 0:
        return None
    k = _pick_int(1, min(5, hi), positive=True)
    a = diff * k
    den_value = k  # den evaluates to k at the solution

    if use_shift:
        d = _pick_int(-hi, hi, nonzero=True)
        x = den_value - d
        if x + d == 0 or abs(x) > 24:
            return None
        lhs = f"{_frac(_const_latex(a), _linear(1, d, variable=var))} {_signed(b)}"
        prompt = format_equation_latex(lhs, _const_latex(c))
        return prompt, prompt, _format_answer([x], [], settings, variable=var)

    x = den_value
    if x == 0 or abs(a) > 36:
        return None
    lhs = f"{_frac(_const_latex(a), var)} {_signed(b)}"
    prompt = format_equation_latex(lhs, _const_latex(c))
    return prompt, prompt, _format_answer([x], [], settings, variable=var)


def _signed(value: int) -> str:
    if value >= 0:
        return f"+ {value}"
    return f"- {abs(value)}"


def _build_two_fractions(settings: dict) -> tuple[str, str, str | None] | None:
    """a/(x+p) + b/(x+q) = c, built from a chosen valid root."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)

    p = _pick_int(-hi, hi, nonzero=True)
    q = _pick_int(-hi, hi, nonzero=True)
    if p == q:
        q = p + _pick_int(1, 4, positive=True) * random.choice([-1, 1])

    x = _pick_int(-hi, hi, nonzero=True)
    left_den = x + p
    right_den = x + q
    if left_den == 0 or right_den == 0:
        return None

    # Choose integer c and a, then solve for integer b:
    # a/(x+p) + b/(x+q) = c  ⇒  b = c(x+q) - a(x+q)/(x+p)
    a = _pick_int(1, min(6, hi), nonzero=True) * random.choice([-1, 1])
    c = _pick_int(-5, 5, nonzero=True)
    if (a * right_den) % left_den != 0:
        return None
    b = c * right_den - (a * right_den) // left_den
    if b == 0 or abs(b) > 20:
        return None

    if b >= 0:
        lhs = (
            f"{_frac(_const_latex(a), _linear(1, p, variable=var))} + "
            f"{_frac(_const_latex(b), _linear(1, q, variable=var))}"
        )
    else:
        lhs = (
            f"{_frac(_const_latex(a), _linear(1, p, variable=var))} - "
            f"{_frac(_const_latex(abs(b)), _linear(1, q, variable=var))}"
        )
    prompt = format_equation_latex(lhs, _const_latex(c))

    # Cleared dens: a(x+q) + b(x+p) = c(x+p)(x+q)
    # -c x^2 + (a+b-c(p+q)) x + (aq+bp-cpq) = 0
    excluded = {-p, -q}
    valid: list[int | Fraction] = [x]
    extraneous: list[int | Fraction] = []
    A_coef = -c
    B_coef = a + b - c * (p + q)
    C_coef = a * q + b * p - c * p * q
    if A_coef != 0:
        disc = B_coef * B_coef - 4 * A_coef * C_coef
        root = int(disc**0.5) if disc >= 0 else -1
        if disc >= 0 and root * root == disc:
            for sign in (1, -1):
                num = -B_coef + sign * root
                den = 2 * A_coef
                if den != 0 and num % den == 0:
                    cand = Fraction(num, den)
                    if cand in excluded or (cand + p == 0 or cand + q == 0):
                        extraneous.append(cand)
                    elif cand != Fraction(x):
                        left = Fraction(a, cand + p) + Fraction(b, cand + q)
                        if left == c:
                            valid.append(cand)
                        else:
                            extraneous.append(cand)

    return prompt, prompt, _format_answer(valid, extraneous, settings, variable=var)


def _try_build(form: str, settings: dict) -> tuple[str, str, str | None] | None:
    builders = {
        "simple_fraction": _build_simple_fraction,
        "proportion": _build_proportion,
        "fraction_plus_constant": _build_fraction_plus_constant,
        "two_fractions": _build_two_fractions,
    }
    builder = builders.get(form)
    if builder is None:
        return None
    for _ in range(40):
        built = builder(settings)
        if built is not None:
            prompt, text, answer = built
            if "\\sqrt" in prompt or "sqrt" in prompt.lower():
                continue
            if "." in prompt:
                continue
            return prompt, text, answer
    return None


def generate_rational_equations(topic: str, settings: dict) -> list:
    """Generate rational-equation questions for *topic*."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    forms = _enabled_forms(settings)

    def _choose_form() -> str:
        # Hard unlocks two-fraction LCD work — prefer it so Easy ≠ Hard is obvious.
        if "two_fractions" in forms and len(forms) > 1 and random.random() < 0.72:
            return "two_fractions"
        # Medium should lean on fraction+constant when available.
        if (
            "fraction_plus_constant" in forms
            and "two_fractions" not in forms
            and len(forms) > 1
            and random.random() < 0.55
        ):
            return "fraction_plus_constant"
        return random.choice(forms)

    def build() -> tuple[str, str, str | None]:
        for _ in range(80):
            form = _choose_form()
            built = _try_build(form, settings)
            if built is not None:
                return built
        # Absolute fallback: 6/x = 2 → x = 3
        var = str(settings.get("variable", "x"))
        prompt = format_equation_latex(_frac("6", var), "2")
        answer = _format_answer(
            [3],
            [],
            {**settings, "include_answer_key": include_answer_key},
            variable=var,
        )
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)
