"""Enriched calculus derivative-rule generators.

Overrides thin power/product/quotient/chain/trig/ln/exp/etc. builders with
expression-ordering + function-family variety (OpenStax Vol. 1 Ch. 3 patterns).
Also implements Differentiation stubs: instantaneous rates, inverse functions,
and true logarithmic differentiation.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from .calculus_pilot import _poly_display
from .utils import (
    _make_questions,
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
    frac_latex,
    random_int_range,
)


def _difficulty_tier(settings: dict) -> str:
    tier = str(settings.get("difficulty_tier", settings.get("difficulty", "easy"))).strip().lower()
    if tier in {"1", "e"}:
        return "easy"
    if tier in {"2", "m"}:
        return "medium"
    if tier in {"3", "h"}:
        return "hard"
    if tier in {"easy", "medium", "hard"}:
        return tier
    return "easy"


def _linear_pair(coef_hi: int = 5) -> tuple[int, int]:
    a = random_int_range(1, coef_hi, exclude=set())
    b = random_int_range(-coef_hi, coef_hi, exclude={0})
    return a, b


def _d_prefix(x: str, body: str) -> str:
    """Alternate d/dx vs f'(x) framing."""
    if random.choice([True, False]):
        return rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
    return rf"\text{{Find }}\frac{{d}}{{d{x}}}\left({body}\right)"


def _mono(coef: int, var: str, power: int = 1) -> str:
    return format_monomial_latex(coef, variable=var, degree=power) or (
        "0" if coef == 0 else str(coef)
    )


# ---------------------------------------------------------------------------
# Power rule
# ---------------------------------------------------------------------------


def _derivative_power_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            family = random.choice(["mono", "sum_two", "reversed"])
            if family == "mono":
                n = random.randint(2, 6)
                c = random_int_range(-5, 5, exclude={0})
                body = _mono(c, x, n) if c != 1 else f"{x}^{{{n}}}"
                if c == 1:
                    body = f"{x}^{{{n}}}"
                elif c == -1:
                    body = f"-{x}^{{{n}}}"
                else:
                    body = f"{c}{x}^{{{n}}}"
                answer = _mono(c * n, x, n - 1) if n > 1 else str(c * n)
                if n == 2:
                    answer = _mono(c * 2, x, 1)
            elif family == "sum_two":
                n = random.randint(2, 4)
                m = random.randint(0, n - 1)
                a = random_int_range(-4, 4, exclude={0})
                b = random_int_range(-4, 4, exclude={0})
                coeffs = [0] * (n + 1)
                coeffs[0] = a  # a x^n
                coeffs[n - m] = b  # b x^m — wait dense [a_n..a_0]
                coeffs = [0] * (n + 1)
                coeffs[0] = a
                coeffs[n - m] = b
                body = format_polynomial_latex(coeffs, variable=x)
                # derivative
                d_coeffs = []
                for i, c in enumerate(coeffs[:-1]):
                    p = n - i
                    d_coeffs.append(c * p)
                answer = format_polynomial_latex(d_coeffs, variable=x) if any(d_coeffs) else "0"
            else:
                # reversed display of ax^2+bx+c
                a = random.randint(1, 3)
                b = random_int_range(-4, 4, exclude={0})
                c = random.randint(-3, 3)
                coeffs = [a, b, c]
                body = _poly_display(coeffs, x, style="reversed")
                answer = format_linear_latex(2 * a, b, variable=x)
        elif tier == "medium":
            family = random.choice(["quad", "neg_power", "radical_power", "factored"])
            if family == "quad":
                a = random.randint(1, 3)
                b = random_int_range(-5, 5, exclude={0})
                c = random.randint(-4, 4)
                coeffs = [a, b, c]
                body = _poly_display(coeffs, x)
                answer = format_linear_latex(2 * a, b, variable=x)
            elif family == "neg_power":
                n = random.randint(1, 3)
                body = random.choice([rf"{x}^{{-{n}}}", rf"\frac{{1}}{{{x}^{{{n}}}}}"])
                # d/dx x^{-n} = -n x^{-n-1}
                answer = rf"-{n}{x}^{{-{n + 1}}}"
            elif family == "radical_power":
                # x^{1/2} or x^{3/2}
                p, q = random.choice([(1, 2), (3, 2), (2, 3)])
                body = rf"{x}^{{{p}/{q}}}"
                # (p/q) x^{p/q - 1} = (p/q) x^{(p-q)/q}
                coef = frac_latex(Fraction(p, q))
                num, den = p - q, q
                if den < 0:
                    num, den = -num, -den
                g = Fraction(num, den)
                if g.denominator == 1:
                    exp = str(g.numerator)
                else:
                    exp = rf"{g.numerator}/{g.denominator}"
                answer = rf"{coef}{x}^{{{exp}}}"
            else:
                b = random.randint(1, 5)
                coeffs = [1, b, 0]
                body = _poly_display(coeffs, x, style="factored_linear")
                answer = format_linear_latex(2, b, variable=x)
        else:
            family = random.choice(["cubic", "mixed_powers", "sum_neg"])
            if family == "cubic":
                a = random.randint(1, 2)
                b = random_int_range(-4, 4, exclude={0})
                c = random_int_range(-3, 3, exclude={0})
                d = random.randint(-3, 3)
                coeffs = [a, b, c, d]
                body = _poly_display(coeffs, x, style=random.choice(["standard", "reversed"]))
                answer = format_polynomial_latex([3 * a, 2 * b, c], variable=x)
            elif family == "mixed_powers":
                n = random.randint(3, 5)
                k = random.randint(1, 3)
                body = random.choice(
                    [
                        rf"{k}{x}^{{{n}}}+{x}^{{-1}}",
                        rf"{x}^{{-1}}+{k}{x}^{{{n}}}",
                        rf"\frac{{1}}{{{x}}}+{k}{x}^{{{n}}}",
                    ]
                )
                answer = rf"{k * n}{x}^{{{n - 1}}}-{x}^{{-2}}"
            else:
                n = random.randint(2, 4)
                body = rf"{x}^{{{n}}}-{n}{x}+{random.randint(1, 5)}"
                answer = rf"{n}{x}^{{{n - 1}}}-{n}"
        prompt = _d_prefix(x, body)
        return prompt, "power rule derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


# ---------------------------------------------------------------------------
# Product / quotient / chain
# ---------------------------------------------------------------------------


def _derivative_product_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            a, b = _linear_pair(4)
            c, d = _linear_pair(4)
            f = format_linear_latex(a, b, variable=x)
            g = format_linear_latex(c, d, variable=x)
            answer = format_polynomial_latex([2 * a * c, a * d + b * c], variable=x)
            # orderings: (f)(g) vs f·g vs g·f
            form = random.choice(["paren", "cdot", "swapped"])
            if form == "paren":
                body = rf"\left({f}\right)\left({g}\right)"
            elif form == "cdot":
                body = rf"\left({f}\right)\cdot\left({g}\right)"
            else:
                body = rf"\left({g}\right)\left({f}\right)"
                # same product
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        elif tier == "medium":
            family = random.choice(["poly_linear", "x_trig", "x_exp"])
            if family == "poly_linear":
                a = random.randint(1, 3)
                b = random_int_range(-4, 4, exclude={0})
                c = random_int_range(-4, 4, exclude={0})
                d, e = _linear_pair(4)
                f = format_polynomial_latex([a, b, c], variable=x)
                g = format_linear_latex(d, e, variable=x)
                lead = 3 * a * d
                mid = 2 * a * e + 2 * b * d
                const = b * e + d * c
                answer = format_polynomial_latex([lead, mid, const], variable=x)
                body = random.choice(
                    [
                        rf"\left({f}\right)\left({g}\right)",
                        rf"\left({g}\right)\left({f}\right)",
                    ]
                )
            elif family == "x_trig":
                body = random.choice(
                    [rf"{x}\sin({x})", rf"\sin({x})\,{x}", rf"{x}\cdot\sin({x})"]
                )
                answer = rf"\sin({x})+{x}\cos({x})"
            else:
                body = random.choice(
                    [rf"{x}e^{{{x}}}", rf"e^{{{x}}}{x}", rf"{x}\cdot e^{{{x}}}"]
                )
                answer = rf"e^{{{x}}}+{x}e^{{{x}}}"
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        else:
            family = random.choice(["power_linear", "trig_trig", "ln_x"])
            if family == "power_linear":
                n = random.randint(2, 4)
                a, b = _linear_pair(4)
                f = f"{x}^{{{n}}}"
                g = format_linear_latex(a, b, variable=x)
                coeffs = [(n + 1) * a] + ([n * b] if n >= 1 else [])
                # (n+1)a x^n + n b x^{n-1}
                dense = [0] * (n + 1)
                dense[0] = (n + 1) * a
                if n >= 1:
                    dense[1] = n * b
                answer = format_polynomial_latex(dense, variable=x)
                body = random.choice(
                    [rf"{f}\left({g}\right)", rf"\left({g}\right){f}"]
                )
            elif family == "trig_trig":
                body = random.choice(
                    [rf"\sin({x})\cos({x})", rf"\cos({x})\sin({x})"]
                )
                answer = rf"\cos^{{2}}({x})-\sin^{{2}}({x})"
            else:
                body = random.choice(
                    [rf"{x}\ln({x})", rf"\ln({x})\,{x}"]
                )
                answer = rf"\ln({x})+1"
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        return prompt, "product rule", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_quotient_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            a, b = _linear_pair(4)
            c, d = _linear_pair(4)
            numer = a * d - b * c
            while numer == 0:
                a, b = _linear_pair(4)
                c, d = _linear_pair(4)
                numer = a * d - b * c
            num = format_linear_latex(a, b, variable=x)
            den = format_linear_latex(c, d, variable=x)
            answer = rf"\frac{{{numer}}}{{\left({den}\right)^{{2}}}}"
            form = random.choice(["frac", "cdot_inv"])
            if form == "frac":
                body = rf"\frac{{{num}}}{{{den}}}"
            else:
                body = rf"\left({num}\right)\left({den}\right)^{{-1}}"
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        elif tier == "medium":
            family = random.choice(["quad_over_linear", "sin_over_x", "x_over_exp"])
            if family == "quad_over_linear":
                a = random.randint(1, 3)
                b = random_int_range(-4, 4, exclude={0})
                c = random_int_range(-3, 3, exclude={0})
                d, e = _linear_pair(3)
                num = format_polynomial_latex([a, b, c], variable=x)
                den = format_linear_latex(d, e, variable=x)
                n2, n1, n0 = a * d, 2 * a * e, b * e - c * d
                numer = format_polynomial_latex([n2, n1, n0], variable=x)
                answer = rf"\frac{{{numer}}}{{\left({den}\right)^{{2}}}}"
                body = rf"\frac{{{num}}}{{{den}}}"
            elif family == "sin_over_x":
                body = random.choice(
                    [rf"\frac{{\sin({x})}}{{{x}}}", rf"\sin({x})\,{x}^{{-1}}"]
                )
                answer = rf"\frac{{{x}\cos({x})-\sin({x})}}{{{x}^{{2}}}}"
            else:
                body = rf"\frac{{{x}}}{{e^{{{x}}}}}"
                answer = rf"\frac{{1-{x}}}{{e^{{{x}}}}}"
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        else:
            a, b = _linear_pair(3)
            c = random.randint(1, 3)
            d = random_int_range(-3, 3, exclude={0})
            num = format_linear_latex(a, b, variable=x)
            den = _poly_display([c, 0, d], x, style=random.choice(["standard", "reversed"]))
            numer = format_polynomial_latex([-a * c, -2 * b * c, a * d], variable=x)
            answer = rf"\frac{{{numer}}}{{\left({den}\right)^{{2}}}}"
            body = random.choice(
                [
                    rf"\frac{{{num}}}{{{den}}}",
                    rf"\left({num}\right)\left({den}\right)^{{-1}}",
                ]
            )
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        return prompt, "quotient rule", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_chain_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            a, b = _linear_pair(4)
            n = random.randint(2, 5)
            # ax+b vs b+ax
            if random.choice([True, False]):
                inner = format_linear_latex(a, b, variable=x)
            else:
                mono = _mono(a, x, 1)
                inner = f"{b}+{mono}"
            body = rf"\left({inner}\right)^{{{n}}}"
            outer = n * a
            power = n - 1
            power_latex = (
                rf"\left({inner}\right)"
                if power == 1
                else rf"\left({inner}\right)^{{{power}}}"
            )
            if outer == 1:
                answer = power_latex
            elif outer == -1:
                answer = f"-{power_latex}"
            else:
                answer = f"{outer}{power_latex}"
            # rebuild answer with standard inner for consistency
            std = format_linear_latex(a, b, variable=x)
            power_latex = (
                rf"\left({std}\right)" if power == 1 else rf"\left({std}\right)^{{{power}}}"
            )
            answer = power_latex if outer == 1 else (
                f"-{power_latex}" if outer == -1 else f"{outer}{power_latex}"
            )
        elif tier == "medium":
            family = random.choice(["poly_power", "exp_inner", "sqrt_inner", "trig_linear"])
            if family == "poly_power":
                a = random.randint(1, 3)
                c = random_int_range(-4, 4, exclude={0})
                n = random.randint(2, 4)
                inner = _poly_display([a, 0, c], x)
                body = rf"\left({inner}\right)^{{{n}}}"
                coef = n * 2 * a
                answer = rf"{coef}{x}\left({inner}\right)^{{{n - 1}}}"
            elif family == "exp_inner":
                a, b = _linear_pair(4)
                inner = format_linear_latex(a, b, variable=x)
                body = random.choice([rf"e^{{{inner}}}", rf"\exp({inner})"])
                answer = rf"{a}e^{{{format_linear_latex(a, b, variable=x)}}}"
            elif family == "sqrt_inner":
                a = random.choice([1, 4, 9])
                b = random.randint(0, 5)
                inner = format_linear_latex(a, b, variable=x) if b else _mono(a, x, 1)
                if b == 0:
                    inner = _mono(a, x, 1)
                body = rf"\sqrt{{{inner}}}"
                # (1/2)(ax+b)^{-1/2} * a = a/(2 sqrt(ax+b))
                answer = rf"\frac{{{a}}}{{2\sqrt{{{format_linear_latex(a, b, variable=x)}}}}}"
            else:
                k = random.randint(2, 5)
                fn, der = random.choice(
                    [("\\sin", "\\cos"), ("\\cos", "-\\sin"), ("\\tan", "\\sec^{2}")]
                )
                arg = _mono(k, x, 1)
                body = rf"{fn}({arg})"
                if der.startswith("-"):
                    answer = rf"-{k}{der[1:]}({arg})"
                else:
                    answer = rf"{k}{der}({arg})"
        else:
            family = random.choice(["sin_power", "nested_power", "ln_inner", "comp_trig"])
            if family == "sin_power":
                a = random.randint(2, 5)
                n = random.randint(2, 4)
                body = rf"\sin\left({a}{x}^{{{n}}}\right)"
                answer = rf"{a * n}{x}^{{{n - 1}}}\cos\left({a}{x}^{{{n}}}\right)"
            elif family == "nested_power":
                a, b = _linear_pair(3)
                n = random.randint(2, 3)
                m = random.randint(2, 3)
                inner = format_linear_latex(a, b, variable=x)
                body = rf"\left(\left({inner}\right)^{{{n}}}\right)^{{{m}}}"
                # = (ax+b)^{nm}, deriv nm(ax+b)^{nm-1}*a
                p = n * m
                answer = rf"{p * a}\left({inner}\right)^{{{p - 1}}}"
            elif family == "ln_inner":
                a, b = _linear_pair(4)
                inner = format_linear_latex(a, b, variable=x)
                body = rf"\ln\left|{inner}\right|"
                answer = rf"\frac{{{a}}}{{{inner}}}"
            else:
                n = random.randint(2, 4)
                body = rf"\sin^{{{n}}}({x})"
                answer = rf"{n}\sin^{{{n - 1}}}({x})\cos({x})"
        prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        return prompt, "chain rule", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


# ---------------------------------------------------------------------------
# Trig / inverse trig / ln-exp / other base / logarithmic
# ---------------------------------------------------------------------------


def _derivative_trigonometric(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            fn, deriv = random.choice(
                [
                    ("\\sin", "\\cos"),
                    ("\\cos", "-\\sin"),
                    ("\\tan", "\\sec^{2}"),
                    ("\\cot", "-\\csc^{2}"),
                ]
            )
            # sin x vs sin(x)
            arg = random.choice([x, rf"({x})"])
            body = f"{fn}{arg}" if arg == x else f"{fn}{arg}"
            # normalize: always use (x) in answer
            answer = f"{deriv}({x})"
            prompt = rf"\frac{{d}}{{d{x}}}{fn}({x})"
        elif tier == "medium":
            k = random.randint(2, 6)
            fn, deriv = random.choice(
                [
                    ("\\sin", "\\cos"),
                    ("\\cos", "-\\sin"),
                    ("\\tan", "\\sec^{2}"),
                    ("\\sec", None),
                ]
            )
            # kx vs x*k display
            arg = random.choice([f"{k}{x}", rf"{k}\cdot {x}"])
            if fn == "\\sec":
                prompt = rf"\frac{{d}}{{d{x}}}\sec({arg})"
                answer = rf"{k}\sec({k}{x})\tan({k}{x})"
            elif deriv.startswith("-"):
                prompt = rf"\frac{{d}}{{d{x}}}{fn}({arg})"
                answer = rf"-{k}{deriv[1:]}({k}{x})"
            else:
                prompt = rf"\frac{{d}}{{d{x}}}{fn}({arg})"
                answer = rf"{k}{deriv}({k}{x})"
        else:
            choice = random.choice(["product", "sec", "power", "sum", "csc"])
            if choice == "product":
                body = random.choice(
                    [rf"{x}\sin({x})", rf"\sin({x}){x}", rf"{x}\cos({x})"]
                )
                if "sin" in body:
                    answer = rf"\sin({x})+{x}\cos({x})"
                else:
                    answer = rf"\cos({x})-{x}\sin({x})"
                prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
            elif choice == "sec":
                k = random.randint(2, 5)
                prompt = rf"\frac{{d}}{{d{x}}}\sec({k}{x})"
                answer = rf"{k}\sec({k}{x})\tan({k}{x})"
            elif choice == "power":
                prompt = rf"\frac{{d}}{{d{x}}}\sin^{{2}}({x})"
                answer = random.choice(
                    [rf"2\sin({x})\cos({x})", rf"\sin(2{x})"]
                )
            elif choice == "csc":
                k = random.randint(2, 4)
                prompt = rf"\frac{{d}}{{d{x}}}\csc({k}{x})"
                answer = rf"-{k}\csc({k}{x})\cot({k}{x})"
            else:
                prompt = rf"\frac{{d}}{{d{x}}}\left[\sin({x})+\cos({x})\right]"
                answer = rf"\cos({x})-\sin({x})"
        return prompt, "trigonometric derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_inverse_trig(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            fn, deriv = random.choice(
                [
                    ("\\arcsin", rf"\frac{{1}}{{\sqrt{{1-{x}^{{2}}}}}}"),
                    ("\\arccos", rf"-\frac{{1}}{{\sqrt{{1-{x}^{{2}}}}}}"),
                    ("\\arctan", rf"\frac{{1}}{{1+{x}^{{2}}}}"),
                ]
            )
            # arcsin x vs arcsin(x) vs sin^{-1}(x)
            name = random.choice([fn, fn])  # keep standard; alt:
            if fn == "\\arcsin" and random.random() < 0.35:
                prompt = rf"\frac{{d}}{{d{x}}}\sin^{{-1}}({x})"
            elif fn == "\\arccos" and random.random() < 0.35:
                prompt = rf"\frac{{d}}{{d{x}}}\cos^{{-1}}({x})"
            elif fn == "\\arctan" and random.random() < 0.35:
                prompt = rf"\frac{{d}}{{d{x}}}\tan^{{-1}}({x})"
            else:
                prompt = rf"\frac{{d}}{{d{x}}}{fn}({x})"
            answer = deriv
        elif tier == "medium":
            k = random.randint(2, 5)
            fn = random.choice(["\\arcsin", "\\arctan", "\\arccos"])
            arg = random.choice([f"{k}{x}", rf"{k}\cdot {x}"])
            prompt = rf"\frac{{d}}{{d{x}}}{fn}({arg})"
            if fn == "\\arcsin":
                answer = rf"\frac{{{k}}}{{\sqrt{{1-({k}{x})^{{2}}}}}}"
            elif fn == "\\arccos":
                answer = rf"-\frac{{{k}}}{{\sqrt{{1-({k}{x})^{{2}}}}}}"
            else:
                answer = rf"\frac{{{k}}}{{1+({k}{x})^{{2}}}}"
        else:
            choice = random.choice(["power", "linear_shift", "sqrt_form"])
            if choice == "power":
                k = random.randint(2, 4)
                prompt = rf"\frac{{d}}{{d{x}}}\arctan({x}^{{{k}}})"
                answer = rf"\frac{{{k}{x}^{{{k - 1}}}}}{{1+{x}^{{{2 * k}}}}}"
            elif choice == "linear_shift":
                a, b = _linear_pair(3)
                inner = format_linear_latex(a, b, variable=x)
                prompt = rf"\frac{{d}}{{d{x}}}\arcsin({inner})"
                answer = rf"\frac{{{a}}}{{\sqrt{{1-\left({inner}\right)^{{2}}}}}}"
            else:
                # arctan(sqrt(x)) style kept simple: arcsin(x^2)
                prompt = rf"\frac{{d}}{{d{x}}}\arcsin({x}^{{2}})"
                answer = rf"\frac{{2{x}}}{{\sqrt{{1-{x}^{{4}}}}}}"
        return prompt, "inverse trigonometric derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_ln_exp(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            if random.choice([True, False]):
                n = random.randint(2, 5)
                body = random.choice(
                    [rf"\ln({x}^{{{n}}})", rf"\ln|{x}^{{{n}}}|", rf"n\ln({x})".replace("n", str(n))]
                )
                # if body is n ln(x), answer n/x; if ln(x^n), n/x
                answer = rf"\frac{{{n}}}{{{x}}}"
                prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
            else:
                k = random.randint(1, 5)
                body = (
                    rf"e^{{{x}}}"
                    if k == 1
                    else random.choice([rf"e^{{{k}{x}}}", rf"\exp({k}{x})"])
                )
                answer = rf"e^{{{x}}}" if k == 1 else rf"{k}e^{{{k}{x}}}"
                prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        elif tier == "medium":
            family = random.choice(["ln_linear", "exp_linear", "e_over", "ln_abs"])
            if family == "ln_linear":
                a, b = _linear_pair(4)
                inner = format_linear_latex(a, b, variable=x)
                body = random.choice([rf"\ln({inner})", rf"\ln|{inner}|"])
                answer = rf"\frac{{{a}}}{{{format_linear_latex(a, b, variable=x)}}}"
            elif family == "exp_linear":
                a, b = _linear_pair(4)
                std = format_linear_latex(a, b, variable=x)
                mono = _mono(a, x, 1)
                exp = random.choice([std, f"{b}+{mono}"])
                body = random.choice([rf"e^{{{exp}}}", rf"\exp({exp})"])
                answer = rf"{a}e^{{{std}}}"
            elif family == "e_over":
                body = random.choice(
                    [rf"\frac{{e^{{{x}}}}}{{{x}}}", rf"e^{{{x}}}{x}^{{-1}}"]
                )
                answer = rf"\frac{{{x}e^{{{x}}}-e^{{{x}}}}}{{{x}^{{2}}}}"
            else:
                body = rf"\ln|{x}|"
                answer = rf"\frac{{1}}{{{x}}}"
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        else:
            family = random.choice(["chain_exp", "product_ln", "ln_quad", "exp_power"])
            if family == "chain_exp":
                body = random.choice([rf"e^{{{x}^{{2}}}}", rf"\exp({x}^{{2}})"])
                answer = rf"2{x}e^{{{x}^{{2}}}}"
            elif family == "product_ln":
                body = random.choice([rf"{x}\ln({x})", rf"\ln({x})\,{x}"])
                answer = rf"\ln({x})+1"
            elif family == "ln_quad":
                a = random.randint(1, 3)
                c = random.randint(1, 4)
                inner = _poly_display([a, 0, c], x)
                body = rf"\ln({inner})"
                answer = rf"\frac{{{2 * a}{x}}}{{{inner}}}"
            else:
                n = random.randint(2, 4)
                body = rf"e^{{{x}^{{{n}}}}}"
                answer = rf"{n}{x}^{{{n - 1}}}e^{{{x}^{{{n}}}}}"
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
        return prompt, "ln/exp derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_other_base(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        base = random.randint(2, 5)
        if tier == "easy":
            if random.choice([True, False]):
                body = random.choice([rf"{base}^{{{x}}}", rf"\exp({x}\ln({base}))"])
                # keep answer in a^x ln a form
                answer = rf"{base}^{{{x}}}\ln({base})"
                prompt = rf"\frac{{d}}{{d{x}}}\left[{base}^{{{x}}}\right]"
            else:
                prompt = rf"\frac{{d}}{{d{x}}}\log_{{{base}}}({x})"
                answer = rf"\frac{{1}}{{{x}\ln({base})}}"
        elif tier == "medium":
            k = random.randint(2, 5)
            if random.choice([True, False]):
                arg = random.choice([f"{k}{x}", rf"{k}\cdot {x}"])
                prompt = rf"\frac{{d}}{{d{x}}}{base}^{{{arg}}}"
                answer = rf"{k}{base}^{{{k}{x}}}\ln({base})"
            else:
                a, b = _linear_pair(3)
                inner = format_linear_latex(a, b, variable=x)
                prompt = rf"\frac{{d}}{{d{x}}}\log_{{{base}}}({inner})"
                answer = rf"\frac{{{a}}}{{{inner}\ln({base})}}"
        else:
            k = random.randint(2, 4)
            choice = random.choice(["log_power", "a_poly", "change_order"])
            if choice == "log_power":
                body = random.choice(
                    [rf"\log_{{{base}}}({x}^{{{k}}})", rf"{k}\log_{{{base}}}({x})"]
                )
                prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
                answer = rf"\frac{{{k}}}{{{x}\ln({base})}}"
            elif choice == "a_poly":
                prompt = rf"\frac{{d}}{{d{x}}}{base}^{{{x}^{{2}}}}"
                answer = rf"2{x}{base}^{{{x}^{{2}}}}\ln({base})"
            else:
                prompt = rf"\frac{{d}}{{d{x}}}\left[{x}\cdot {base}^{{{x}}}\right]"
                answer = rf"{base}^{{{x}}}+{x}{base}^{{{x}}}\ln({base})"
        return prompt, "other-base log/exp derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_logarithmic(topic: str, settings: dict) -> list[Question]:
    """Logarithmic differentiation (not plain ln/exp rules)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            # y = x^n via log diff framing, or product of powers
            n = random.randint(2, 5)
            body = f"{x}^{{{n}}}"
            prompt = (
                rf"\text{{Use logarithmic differentiation to find }}"
                rf"\frac{{d}}{{d{x}}}\left[{body}\right]."
            )
            answer = rf"{n}{x}^{{{n - 1}}}"
        elif tier == "medium":
            family = random.choice(["product_powers", "quotient_powers", "root"])
            if family == "product_powers":
                n = random.randint(2, 4)
                m = random.randint(2, 4)
                # (x^n)(x+1)^m — answer via log: y'/y = n/x + m/(x+1)
                body = rf"{x}^{{{n}}}({x}+1)^{{{m}}}"
                prompt = (
                    rf"\text{{Use logarithmic differentiation: }}"
                    rf"y={body}.\ \text{{Find }}y'."
                )
                answer = (
                    rf"{x}^{{{n}}}({x}+1)^{{{m}}}"
                    rf"\left(\frac{{{n}}}{{{x}}}+\frac{{{m}}}{{{x}+1}}\right)"
                )
            elif family == "quotient_powers":
                n = random.randint(2, 4)
                body = rf"\frac{{{x}^{{{n}}}}}{{{x}+1}}"
                prompt = (
                    rf"\text{{Use logarithmic differentiation: }}"
                    rf"y={body}.\ \text{{Find }}y'."
                )
                answer = (
                    rf"\frac{{{x}^{{{n}}}}}{{{x}+1}}"
                    rf"\left(\frac{{{n}}}{{{x}}}-\frac{{1}}{{{x}+1}}\right)"
                )
            else:
                body = rf"\sqrt{{{x}({x}+1)}}"
                prompt = (
                    rf"\text{{Use logarithmic differentiation: }}"
                    rf"y={body}.\ \text{{Find }}y'."
                )
                answer = (
                    rf"\sqrt{{{x}({x}+1)}}"
                    rf"\cdot\frac{{1}}{{2}}\left(\frac{{1}}{{{x}}}+\frac{{1}}{{{x}+1}}\right)"
                )
        else:
            # classic x^x or (sin x)^x style
            choice = random.choice(["x_x", "a_x_x", "trig_x"])
            if choice == "x_x":
                body = rf"{x}^{{{x}}}"
                prompt = (
                    rf"\text{{Use logarithmic differentiation: }}"
                    rf"y={body}.\ \text{{Find }}y'."
                )
                answer = rf"{x}^{{{x}}}\left(\ln({x})+1\right)"
            elif choice == "a_x_x":
                body = rf"({x}+1)^{{{x}}}"
                prompt = (
                    rf"\text{{Use logarithmic differentiation: }}"
                    rf"y={body}.\ \text{{Find }}y'."
                )
                answer = (
                    rf"({x}+1)^{{{x}}}"
                    rf"\left(\ln({x}+1)+\frac{{{x}}}{{{x}+1}}\right)"
                )
            else:
                body = rf"\left(\sin({x})\right)^{{{x}}}"
                prompt = (
                    rf"\text{{Use logarithmic differentiation: }}"
                    rf"y={body}.\ \text{{Find }}y'."
                )
                answer = (
                    rf"\left(\sin({x})\right)^{{{x}}}"
                    rf"\left(\ln(\sin({x}))+{x}\cot({x})\right)"
                )
        return prompt, "logarithmic differentiation", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_implicit(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(2, 9)
        if tier == "easy":
            # circle: x^2+y^2=a vs y^2+x^2=a
            eq = random.choice(
                [rf"{x}^{{2}}+y^{{2}}={a}", rf"y^{{2}}+{x}^{{2}}={a}"]
            )
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{{x}}}{{y}}"
        elif tier == "medium":
            family = random.choice(["xy_term", "ellipse", "line_prod"])
            if family == "xy_term":
                eq = random.choice(
                    [rf"{x}^{{2}}+{x}y={a}", rf"{x}y+{x}^{{2}}={a}"]
                )
                answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{2{x}+y}}{{{x}}}"
            elif family == "ellipse":
                b = random.randint(2, 5)
                eq = rf"{b}{x}^{{2}}+y^{{2}}={a}"
                answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{{2 * b}{x}}}{{y}}"
            else:
                eq = rf"{x}y={a}"
                answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{y}}{{{x}}}"
        else:
            family = random.choice(["cubes", "trig", "exp_y"])
            if family == "cubes":
                eq = random.choice(
                    [rf"{x}^{{3}}+y^{{3}}={a}", rf"y^{{3}}+{x}^{{3}}={a}"]
                )
                answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{{x}^{{2}}}}{{y^{{2}}}}"
            elif family == "trig":
                eq = rf"\sin({x})+\cos(y)={a % 2}"  # keep small RHS
                # cos x - sin(y) y' = 0 → y' = cos x / sin y
                eq = rf"\sin({x})+\cos(y)=0"
                answer = rf"\frac{{dy}}{{d{x}}}=\frac{{\cos({x})}}{{\sin(y)}}"
            else:
                eq = rf"e^{{y}}+{x}={a}"
                answer = rf"\frac{{dy}}{{d{x}}}=-e^{{-y}}"
        prompt = (
            rf"\text{{Differentiate implicitly: }}{eq}."
            rf"\text{{ Solve for }}\frac{{dy}}{{d{x}}}."
        )
        return prompt, "implicit differentiation", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_higher_order(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 4)
        b = random_int_range(-5, 5, exclude={0})
        c = random_int_range(-5, 5, exclude={0})
        d = random.randint(-5, 5)
        if tier == "easy":
            coeffs = [a, b, c, d]
            f = _poly_display(coeffs, x)
            prompt = rf"\text{{Find }}f''({x})\text{{ for }}f({x})={f}."
            answer = format_linear_latex(6 * a, 2 * b, variable=x)
        elif tier == "medium":
            family = random.choice(["poly4", "trig", "exp"])
            if family == "poly4":
                e = random_int_range(-4, 4, exclude={0})
                f = _poly_display([a, b, c, d, e], x)
                prompt = rf"\text{{Find }}f'''({x})\text{{ for }}f({x})={f}."
                answer = format_linear_latex(24 * a, 6 * b, variable=x)
            elif family == "trig":
                prompt = rf"\text{{Find }}\frac{{d^{{2}}}}{{d{x}^{{2}}}}\sin({x})."
                answer = rf"-\sin({x})"
            else:
                prompt = rf"\text{{Find }}\frac{{d^{{2}}}}{{d{x}^{{2}}}}e^{{{x}}}."
                answer = rf"e^{{{x}}}"
        else:
            family = random.choice(["eval", "trig_k", "exp_k"])
            if family == "eval":
                f = _poly_display([a, b, c, d], x, style=random.choice(["standard", "reversed"]))
                t = random.randint(1, 4)
                prompt = rf"\text{{Find }}f''({t})\text{{ for }}f({x})={f}."
                answer = str(6 * a * t + 2 * b)
            elif family == "trig_k":
                k = random.randint(2, 4)
                prompt = rf"\text{{Find }}\frac{{d^{{2}}}}{{d{x}^{{2}}}}\sin({k}{x})."
                answer = rf"-{k * k}\sin({k}{x})"
            else:
                k = random.randint(2, 4)
                prompt = rf"\text{{Find }}\frac{{d^{{2}}}}{{d{x}^{{2}}}}e^{{{k}{x}}}."
                answer = rf"{k * k}e^{{{k}{x}}}"
        return prompt, "higher order derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


# ---------------------------------------------------------------------------
# Rates + definition + inverse functions (stubs / enrichment)
# ---------------------------------------------------------------------------


def _average_rate_of_change(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a0 = random.randint(0, 3)
        width = random.randint(1, 4) if tier == "easy" else random.randint(2, 5)
        b0 = a0 + width
        if tier == "easy":
            f = f"{x}^{{2}}"
            fa, fb = a0 * a0, b0 * b0
            a, b = a0, b0
        elif tier == "medium":
            family = random.choice(["cubic", "quad_const", "linear"])
            a, b = a0, b0
            if family == "cubic":
                k = random.randint(1, 3)
                f = _mono(k, x, 3)
                fa, fb = k * a**3, k * b**3
            elif family == "quad_const":
                p = random.randint(1, 3)
                q = random_int_range(-4, 4, exclude={0})
                f = _poly_display([p, 0, q], x)
                fa, fb = p * a * a + q, p * b * b + q
            else:
                m = random_int_range(-5, 5, exclude={0})
                c = random.randint(-3, 3)
                f = format_linear_latex(m, c, variable=x)
                fa, fb = m * a + c, m * b + c
        else:
            family = random.choice(["poly", "reciprocal", "shifted"])
            if family == "reciprocal":
                a = random.randint(1, 3)
                b = a + random.randint(1, 3)
                f = random.choice([rf"\frac{{1}}{{{x}}}", rf"{x}^{{-1}}"])
                fa, fb = Fraction(1, a), Fraction(1, b)
            elif family == "shifted":
                a, b = a0, b0
                f = rf"{x}^{{3}}+{x}"
                fa, fb = a**3 + a, b**3 + b
            else:
                a, b = a0, b0
                p = random.randint(1, 2)
                q = random_int_range(-3, 3, exclude={0})
                r = random.randint(-2, 2)
                f = _poly_display([p, q, r], x)
                fa = p * a * a + q * a + r
                fb = p * b * b + q * b + r
        rate = Fraction(fb - fa, b - a)
        prompt = (
            rf"\text{{Find the average rate of change of }}f({x})={f}"
            rf"\text{{ on }}[{a},{b}]."
        )
        return prompt, "average rate of change", (
            frac_latex(rate) if include_answer_key else None
        )

    return _make_questions(topic, count, include_answer_key, build)


def _instantaneous_rate_of_change(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 4)
        if tier == "easy":
            n = random.randint(2, 4)
            f = f"{x}^{{{n}}}"
            answer = str(n * a ** (n - 1))
        elif tier == "medium":
            family = random.choice(["poly", "sqrt", "reciprocal"])
            if family == "poly":
                p = random.randint(1, 3)
                q = random_int_range(-4, 4, exclude={0})
                f = _poly_display([p, 0, q], x)
                answer = str(2 * p * a)
            elif family == "sqrt":
                # f=sqrt(x) at perfect square
                a = random.choice([1, 4, 9])
                f = random.choice([rf"\sqrt{{{x}}}", rf"{x}^{{1/2}}"])
                answer = frac_latex(Fraction(1, 2 * int(a**0.5)))
            else:
                a = random.randint(1, 4)
                f = random.choice([rf"\frac{{1}}{{{x}}}", rf"{x}^{{-1}}"])
                answer = frac_latex(Fraction(-1, a * a))
        else:
            family = random.choice(["trig", "exp", "cubic"])
            if family == "trig":
                a = 0
                f = random.choice([rf"\sin({x})", rf"\cos({x})"])
                answer = "1" if "sin" in f else "0"
            elif family == "exp":
                a = 0
                k = random.randint(1, 3)
                f = rf"e^{{{k}{x}}}" if k != 1 else rf"e^{{{x}}}"
                answer = str(k)
            else:
                p = random.randint(1, 2)
                q = random_int_range(-3, 3, exclude={0})
                f = _poly_display([p, 0, q, 0], x)
                # p x^3 + q x → f' = 3p x^2 + q
                answer = str(3 * p * a * a + q)
        prompt = (
            rf"\text{{Find the instantaneous rate of change of }}"
            rf"f({x})={f}\text{{ at }}{x}={a}."
        )
        return prompt, "instantaneous rate of change", (
            answer if include_answer_key else None
        )

    return _make_questions(topic, count, include_answer_key, build)


def _definition_of_derivative(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 5)
        if tier == "easy":
            form = random.choice(["limit_h", "limit_x"])
            if form == "limit_h":
                prompt = rf"\lim_{{h\to 0}}\frac{{({a}+h)^{{2}}-{a * a}}}{{h}}"
            else:
                prompt = rf"\lim_{{{x}\to {a}}}\frac{{{x}^{{2}}-{a * a}}}{{{x}-{a}}}"
            answer = str(2 * a)
        elif tier == "medium":
            form = random.choice(["cube", "linear_coef", "named"])
            if form == "cube":
                prompt = rf"\lim_{{h\to 0}}\frac{{({a}+h)^{{3}}-{a ** 3}}}{{h}}"
                answer = str(3 * a * a)
            elif form == "linear_coef":
                k = random.randint(2, 4)
                prompt = rf"\lim_{{h\to 0}}\frac{{{k}({a}+h)^{{2}}-{k * a * a}}}{{h}}"
                answer = str(2 * k * a)
            else:
                k = random.randint(2, 4)
                prompt = (
                    rf"\text{{Use the definition to find }}f'({a})"
                    rf"\text{{ for }}f({x})={k}{x}^{{2}}."
                )
                answer = str(2 * k * a)
        else:
            family = random.choice(["reciprocal", "sqrt", "poly"])
            if family == "reciprocal":
                prompt = (
                    rf"\lim_{{h\to 0}}\frac{{\frac{{1}}{{{a}+h}}-\frac{{1}}{{{a}}}}}{{h}}"
                )
                answer = frac_latex(Fraction(-1, a * a))
            elif family == "sqrt":
                # pick a perfect square for nicer answer optional
                a = random.choice([1, 4, 9])
                prompt = (
                    rf"\lim_{{h\to 0}}\frac{{\sqrt{{{a}+h}}-\sqrt{{{a}}}}}{{h}}"
                )
                answer = frac_latex(Fraction(1, 2 * int(a**0.5)))
            else:
                p = random.randint(1, 3)
                q = random_int_range(-3, 3, exclude={0})
                f = _poly_display([p, 0, q], x)
                prompt = (
                    rf"\text{{Use the definition to find }}f'({a})"
                    rf"\text{{ for }}f({x})={f}."
                )
                answer = str(2 * p * a)
        return prompt, "definition of the derivative", (
            answer if include_answer_key else None
        )

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_inverse_functions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            n = random.randint(2, 4)
            a = random.randint(1, 3)
            # f(x)=x^n, f(a)=a^n, (f^{-1})'(a^n)=1/(n a^{n-1})
            fp = n * a ** (n - 1)
            prompt = (
                rf"f({x})={x}^{{{n}}};\quad f'({a})={fp}."
                rf"\quad\text{{Find }}(f^{{-1}})'({a ** n})."
            )
            answer = frac_latex(Fraction(1, fp))
        elif tier == "medium":
            # f(x)=x^3+x or linear-ish with table values
            family = random.choice(["power", "table", "linear"])
            if family == "power":
                n = random.randint(2, 3)
                a = random.randint(1, 2)
                fp = n * a ** (n - 1)
                prompt = (
                    rf"f({x})={x}^{{{n}}};\quad f'({a})={fp}."
                    rf"\quad\text{{Find }}(f^{{-1}})'({a ** n})."
                )
                answer = frac_latex(Fraction(1, fp))
            elif family == "table":
                b = random.randint(1, 5)
                y = random.randint(2, 8)
                fp = random_int_range(-6, 6, exclude={0})
                prompt = (
                    rf"f({b})={y},\ f'({b})={fp}."
                    rf"\quad\text{{Find }}(f^{{-1}})'({y})."
                )
                answer = frac_latex(Fraction(1, fp))
            else:
                m = random.randint(2, 5)
                c = random.randint(-3, 3)
                # f(x)=mx+c, (f^{-1})'=1/m everywhere
                prompt = (
                    rf"f({x})={format_linear_latex(m, c, variable=x)}."
                    rf"\quad\text{{Find }}(f^{{-1}})'({x})."
                )
                answer = frac_latex(Fraction(1, m))
        else:
            # f(x)=e^x or ln, or cubic at a point
            family = random.choice(["exp", "ln", "cubic"])
            if family == "exp":
                # f(x)=e^x, f(0)=1, f'(0)=1 → (f^{-1})'(1)=1
                prompt = (
                    rf"f({x})=e^{{{x}}};\quad f(0)=1,\ f'(0)=1."
                    rf"\quad\text{{Find }}(f^{{-1}})'(1)."
                )
                answer = "1"
            elif family == "ln":
                prompt = (
                    rf"f({x})=\ln({x});\quad f(e)=1,\ f'(e)=\frac{{1}}{{e}}."
                    rf"\quad\text{{Find }}(f^{{-1}})'(1)."
                )
                answer = "e"
            else:
                a = random.randint(1, 2)
                # f(x)=x^3+x, f'(x)=3x^2+1
                fp = 3 * a * a + 1
                y = a**3 + a
                prompt = (
                    rf"f({x})={x}^{{3}}+{x};\quad f'({a})={fp}."
                    rf"\quad\text{{Find }}(f^{{-1}})'({y})."
                )
                answer = frac_latex(Fraction(1, fp))
        return prompt, "inverse function derivative", (
            answer if include_answer_key else None
        )

    return _make_questions(topic, count, include_answer_key, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "derivative_power_rule": _derivative_power_rule,
    "derivative_product_rule": _derivative_product_rule,
    "derivative_quotient_rule": _derivative_quotient_rule,
    "derivative_chain_rule": _derivative_chain_rule,
    "derivative_trigonometric": _derivative_trigonometric,
    "derivative_inverse_trig": _derivative_inverse_trig,
    "derivative_ln_exp": _derivative_ln_exp,
    "derivative_other_base": _derivative_other_base,
    "derivative_logarithmic": _derivative_logarithmic,
    "derivative_implicit": _derivative_implicit,
    "derivative_higher_order": _derivative_higher_order,
    "average_rate_of_change": _average_rate_of_change,
    "instantaneous_rate_of_change": _instantaneous_rate_of_change,
    "definition_of_derivative": _definition_of_derivative,
    "derivative_inverse_functions": _derivative_inverse_functions,
}
