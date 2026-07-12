"""Complex-fraction generators with structure-based difficulty tiers.

Easy   — single-variable complex fractions with monomial dens
         (e.g. (1 + a/x) / (b/x) or (a/x)/(b/c)).
Medium — binomial pieces in numerator and denominator
         (e.g. (a/x + b)/(c/x + d)).
Hard   — unlike linear dens / multi-term complex fractions
         (e.g. ((a/(x+p)) + (b/(x+q))) / (c/(x+r))).

Answers are simplified rational expressions with excluded values.
"""

from __future__ import annotations

import random
from math import gcd

from packages.polynomial_core import (
    Polynomial,
    format_linear_latex,
    fraction_latex,
    rational_excluded_values_latex,
)

from .utils import make_questions


def _pick_int(lo: int, hi: int, *, nonzero: bool = False) -> int:
    if lo > hi:
        lo, hi = hi, lo
    for _ in range(40):
        value = random.randint(lo, hi)
        if nonzero and value == 0:
            continue
        return value
    return 1 if nonzero else lo


def _frac(num: str, den: str) -> str:
    return fraction_latex(num, den)


def _linear(a: int, b: int, *, variable: str = "x") -> str:
    return format_linear_latex(a, b, variable=variable)


def _answer_with_excluded(
    num: Polynomial,
    den: Polynomial,
    excluded: list[int],
    settings: dict,
) -> str | None:
    if not bool(settings.get("include_answer_key", False)):
        return None
    if den.deg() == 0:
        lead = int(round(float(den.coef(0))))
        if lead == 1:
            body = num.to_latex()
        elif lead == -1:
            body = (num * -1).to_latex()
        else:
            body = fraction_latex(num.to_latex(), str(lead))
    else:
        body = fraction_latex(num.to_latex(), den.to_latex())
    note = rational_excluded_values_latex(sorted(set(excluded)))
    if note:
        return f"{body},\\; {note}"
    return body


def _reduce_rational(
    num: Polynomial,
    den: Polynomial,
) -> tuple[Polynomial, Polynomial]:
    """Cancel a linear GCD when present; reduce integer content."""
    from packages.polynomial_core.operations import polynomial_gcd
    from packages.polynomial_core.rational import (
        _integerize_polynomial,
        _make_content_primitive,
        _scale_fraction_to_integers,
    )

    num, den = _scale_fraction_to_integers(num, den)
    if den.is_zero():
        return num, Polynomial([1])
    g = _make_content_primitive(_integerize_polynomial(polynomial_gcd(num, den)))
    if g.deg() >= 1:
        from packages.polynomial_core.rational import _exact_divide

        try:
            num = _exact_divide(num, g)
            den = _exact_divide(den, g)
        except ValueError:
            pass
    return _scale_fraction_to_integers(num, den)


def _build_easy(settings: dict) -> tuple[str, str, str | None] | None:
    """(a + b/x)/(c/x) or (a/x)/(b/c) style."""
    var = str(settings.get("variable", "x"))
    hi = max(3, min(8, abs(int(settings.get("coef_max", 6))) or 6))
    style = random.choice(["outer_over_frac", "sum_over_frac", "frac_over_const"])

    if style == "outer_over_frac":
        # (a/x) / (b/c) = (a c)/(b x)
        a = _pick_int(1, hi, nonzero=True)
        b = _pick_int(2, hi, nonzero=True)
        c = _pick_int(2, hi, nonzero=True)
        if b == c:
            c = b + 1
        g = gcd(a * c, b)
        num = Polynomial([a * c // g])
        den = Polynomial([b // g, 0])  # (b/g) x
        prompt = _frac(_frac(str(a), var), _frac(str(b), str(c)))
        excluded = [0]
        num, den = _reduce_rational(num, den)
        return prompt, prompt, _answer_with_excluded(num, den, excluded, settings)

    if style == "sum_over_frac":
        # (k + a/x) / (b/x) = (k x + a)/b
        k = _pick_int(1, hi, nonzero=True)
        a = _pick_int(1, hi, nonzero=True)
        b = _pick_int(1, hi, nonzero=True)
        top = f"{k} + {_frac(str(a), var)}"
        prompt = _frac(top, _frac(str(b), var))
        num = Polynomial([k, a])
        den = Polynomial([b])
        num, den = _reduce_rational(num, den)
        return prompt, prompt, _answer_with_excluded(num, den, [0], settings)

    # (a/x + b) / c
    a = _pick_int(1, hi, nonzero=True)
    b = _pick_int(1, hi, nonzero=True)
    c = _pick_int(2, hi, nonzero=True)
    top = f"{_frac(str(a), var)} + {b}"
    prompt = _frac(top, str(c))
    num = Polynomial([b, a])  # b x + a
    den = Polynomial([c, 0])  # c x
    num, den = _reduce_rational(num, den)
    return prompt, prompt, _answer_with_excluded(num, den, [0], settings)


def _sum_frac_const(coef_over_x: int, constant: int, *, variable: str) -> str:
    """Render ±|a|/x ± |b| without a leading plus."""
    pieces: list[str] = []
    if coef_over_x != 0:
        abs_a = abs(coef_over_x)
        frag = _frac(str(abs_a), variable)
        pieces.append(frag if coef_over_x > 0 else f"-{frag}")
    if constant != 0:
        abs_b = abs(constant)
        if not pieces:
            pieces.append(str(constant))
        elif constant > 0:
            pieces.append(f"+ {abs_b}")
        else:
            pieces.append(f"- {abs_b}")
    return " ".join(pieces) if pieces else "0"


def _build_medium(settings: dict) -> tuple[str, str, str | None] | None:
    """(a/x + b)/(c/x + d)."""
    var = str(settings.get("variable", "x"))
    hi = max(4, min(10, abs(int(settings.get("coef_max", 8))) or 8))
    a = _pick_int(1, hi, nonzero=True) * random.choice([-1, 1])
    b = _pick_int(1, hi, nonzero=True) * random.choice([-1, 1])
    c = _pick_int(1, hi, nonzero=True) * random.choice([-1, 1])
    d = _pick_int(1, hi, nonzero=True) * random.choice([-1, 1])
    if b * c == a * d:
        d = d + (1 if d >= 0 else -1)

    prompt = _frac(
        _sum_frac_const(a, b, variable=var),
        _sum_frac_const(c, d, variable=var),
    )
    # (a + b x)/(c + d x)
    num = Polynomial([b, a])
    den = Polynomial([d, c])
    num, den = _reduce_rational(num, den)
    excluded = [0]
    # Denominator of the complex fraction vanishes when c/x + d = 0.
    if d != 0 and c % d == 0:
        excluded.append(-c // d)
    return prompt, prompt, _answer_with_excluded(num, den, excluded, settings)


def _build_hard(settings: dict) -> tuple[str, str, str | None] | None:
    """((a/(x+p)) + (b/(x+q))) / (c/(x+r))."""
    var = str(settings.get("variable", "x"))
    hi = max(4, min(10, abs(int(settings.get("coef_max", 10))) or 10))
    p = _pick_int(-hi, hi, nonzero=True)
    q = _pick_int(-hi, hi, nonzero=True)
    if p == q:
        q = p + random.choice([-2, -1, 1, 2])
    r = _pick_int(-hi, hi, nonzero=True)
    a = _pick_int(1, min(6, hi), nonzero=True) * random.choice([-1, 1])
    b = _pick_int(1, min(6, hi), nonzero=True) * random.choice([-1, 1])
    c = _pick_int(1, min(6, hi), nonzero=True)

    left = _frac(str(a), _linear(1, p, variable=var))
    right = _frac(str(abs(b)), _linear(1, q, variable=var))
    if b >= 0:
        top = f"{left} + {right}"
    else:
        top = f"{left} - {right}"
    bottom = _frac(str(c), _linear(1, r, variable=var))
    prompt = _frac(top, bottom)

    # Value = [(a(x+q)+b(x+p))/((x+p)(x+q))] * [(x+r)/c]
    #       = ( (a+b)x + (aq+bp) )(x+r) / (c (x+p)(x+q))
    num = Polynomial([a + b, a * q + b * p]) * Polynomial([1, r])
    den = Polynomial([c]) * Polynomial([1, p]) * Polynomial([1, q])
    num, den = _reduce_rational(num, den)
    excluded = sorted({-p, -q, -r})
    return prompt, prompt, _answer_with_excluded(num, den, excluded, settings)


def _choose_builder(settings: dict):
    tier = str(settings.get("difficulty_tier", "easy")).strip().lower()
    if tier == "hard":
        return _build_hard
    if tier == "medium":
        return _build_medium
    # Allow explicit form overrides.
    if bool(settings.get("allow_complex_hard", False)):
        return _build_hard
    if bool(settings.get("allow_complex_medium", False)):
        return _build_medium
    return _build_easy


def generate_complex_fractions(topic: str, settings: dict) -> list:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    builder = _choose_builder(settings)

    def build() -> tuple[str, str, str | None]:
        for _ in range(60):
            built = builder(settings)
            if built is None:
                continue
            prompt, text, answer = built
            if "." in prompt or (answer and "." in answer):
                continue
            if "\\sqrt" in prompt:
                continue
            return prompt, text, answer
        # Fallback: (1 + 2/x) / (3/x) → (x+2)/3
        var = str(settings.get("variable", "x"))
        prompt = _frac(f"1 + {_frac('2', var)}", _frac("3", var))
        answer = _answer_with_excluded(
            Polynomial([1, 2]),
            Polynomial([3]),
            [0],
            {**settings, "include_answer_key": include_answer_key},
        )
        return prompt, prompt, answer

    return make_questions(topic, count, include_answer_key, build, settings=settings)
