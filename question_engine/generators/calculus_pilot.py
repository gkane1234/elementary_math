"""Pilot calculus generators emphasizing expression ordering + function variety.

These replace thin ``calculus_foundations`` stubs for a small set of topics so
we can review sample quality before wiring the full remaining stub list.
Patterns generalized from OpenStax Calculus Vol. 1 §§3.1, 4.2, 5.5–5.6.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from .utils import (
    _make_questions,
    format_linear_latex,
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


def _poly_display(coeffs: list[int], variable: str, *, style: str | None = None) -> str:
    """Render a polynomial with alternate term orderings / factorizations."""
    style = style or random.choice(["standard", "reversed", "factored_linear"])
    standard = format_polynomial_latex(coeffs, variable=variable)
    if style == "standard":
        return standard

    # Dense coeffs: [a_n, ..., a_0]
    terms: list[tuple[int, int]] = []
    deg = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        if c:
            terms.append((c, deg - i))

    if style == "reversed" and len(terms) >= 2:
        # Low degree first: e.g. 3 + 2x + x^2
        parts: list[str] = []
        for i, (c, p) in enumerate(sorted(terms, key=lambda t: t[1])):
            if p == 0:
                piece = str(c)
            elif p == 1:
                if c == 1:
                    piece = variable
                elif c == -1:
                    piece = f"-{variable}"
                else:
                    piece = f"{c}{variable}"
            else:
                if c == 1:
                    piece = f"{variable}^{{{p}}}"
                elif c == -1:
                    piece = f"-{variable}^{{{p}}}"
                else:
                    piece = f"{c}{variable}^{{{p}}}"
            if i == 0:
                parts.append(piece)
            elif piece.startswith("-"):
                parts.append(f" - {piece[1:]}")
            else:
                parts.append(f" + {piece}")
        return "".join(parts)

    # Factored-ish for quadratics like x^2 + bx = x(x+b) when constant is 0
    if (
        style == "factored_linear"
        and len(coeffs) == 3
        and coeffs[0] == 1
        and coeffs[2] == 0
        and coeffs[1] != 0
    ):
        inner = format_linear_latex(1, coeffs[1], variable=variable)
        return rf"{variable}\left({inner}\right)"

    return standard


def _point_eval_poly(coeffs: list[int], a: int) -> int:
    value = 0
    for c in coeffs:
        value = value * a + c
    return value


def _deriv_coeffs(coeffs: list[int]) -> list[int]:
    deg = len(coeffs) - 1
    if deg <= 0:
        return [0]
    out = []
    for i, c in enumerate(coeffs[:-1]):
        power = deg - i
        out.append(c * power)
    return out if any(out) else [0]


# ---------------------------------------------------------------------------
# Pilot 1: tangent / normal lines (OpenStax 3.1: f=x^2, f=1/x, poly)
# ---------------------------------------------------------------------------


def _tangent_normal_line(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))
    want_normal = False
    if tier == "medium":
        want_normal = random.random() < 0.25
    elif tier == "hard":
        want_normal = random.choice([True, False])

    def build() -> tuple[str, str, str | None]:
        family = {
            "easy": random.choice(["poly_mono", "poly_quad", "reciprocal"]),
            "medium": random.choice(["poly_quad", "reciprocal", "radical", "trig"]),
            "hard": random.choice(["poly_cubic", "exp", "ln", "rational_linear", "trig_chain"]),
        }[tier]

        if family == "poly_mono":
            n = random.randint(2, 4)
            a = random.randint(1, 4)
            f_latex = f"{x}^{{{n}}}"
            y0 = a**n
            m = n * a ** (n - 1)
        elif family == "poly_quad":
            # Textbook-like 3x^2-4x+1, plus reordered / factored forms
            A = random.randint(1, 3)
            B = random_int_range(-4, 4, exclude={0})
            C = random.randint(-3, 3)
            coeffs = [A, B, C]
            a = random.randint(1, 3)
            f_latex = _poly_display(coeffs, x)
            y0 = _point_eval_poly(coeffs, a)
            m = _point_eval_poly(_deriv_coeffs(coeffs), a)
        elif family == "poly_cubic":
            A = random.randint(1, 2)
            B = random_int_range(-3, 3, exclude={0})
            coeffs = [A, 0, B, 0]  # A x^3 + B x
            a = random.randint(1, 2)
            f_latex = _poly_display(coeffs, x, style=random.choice(["standard", "reversed"]))
            y0 = _point_eval_poly(coeffs, a)
            m = _point_eval_poly(_deriv_coeffs(coeffs), a)
        elif family == "reciprocal":
            # OpenStax Ex 3.3: f=1/x; also x^{-1} ordering
            a = random.choice([1, 2, 3, 4])
            f_latex = random.choice([rf"\frac{{1}}{{{x}}}", rf"{x}^{{-1}}"])
            y0_frac = Fraction(1, a)
            m_frac = Fraction(-1, a * a)
            y0_tex = frac_latex(y0_frac)
            m = m_frac  # type: ignore[assignment]
            if want_normal:
                # normal slope = -1/m = a^2
                ns = a * a
                prompt = (
                    rf"\text{{Find the normal line to }}y={f_latex}"
                    rf"\text{{ at }}{x}={a}."
                )
                answer = rf"y-{y0_tex}={ns}\left({x}-{a}\right)"
                return prompt, "normal line", answer if include_answer_key else None
            prompt = (
                rf"\text{{Find the tangent line to }}y={f_latex}"
                rf"\text{{ at }}{x}={a}."
            )
            answer = rf"y-{y0_tex}={frac_latex(m_frac)}\left({x}-{a}\right)"
            return prompt, "tangent line", answer if include_answer_key else None
        elif family == "radical":
            # sqrt(ax+b) with a chosen so value at integer is nice when possible
            a_coef = random.choice([1, 4, 9])
            b = random.choice([0, 5, 7, 12])
            # pick x0 so ax0+b is a perfect square
            squares = [k * k for k in range(1, 6)]
            candidates = [t for t in range(0, 6) if a_coef * t + b in squares]
            x0 = random.choice(candidates) if candidates else 0
            inside = a_coef * x0 + b
            root = int(inside**0.5)
            f_latex = (
                rf"\sqrt{{{a_coef}{x}}}"
                if b == 0
                else rf"\sqrt{{{format_linear_latex(a_coef, b, variable=x)}}}"
            )
            y0 = root
            # f' = a/(2 sqrt(ax+b))
            m_frac = Fraction(a_coef, 2 * root)
            if want_normal and m_frac != 0:
                ns = -Fraction(1) / m_frac
                prompt = (
                    rf"\text{{Find the normal line to }}y={f_latex}"
                    rf"\text{{ at }}{x}={x0}."
                )
                answer = rf"y-{y0}={frac_latex(ns)}\left({x}-{x0}\right)"
                return prompt, "normal line", answer if include_answer_key else None
            prompt = (
                rf"\text{{Find the tangent line to }}y={f_latex}"
                rf"\text{{ at }}{x}={x0}."
            )
            answer = rf"y-{y0}={frac_latex(m_frac)}\left({x}-{x0}\right)"
            return prompt, "tangent line", answer if include_answer_key else None
        elif family == "trig":
            # f=sin x or cos x at 0 or π/6-friendly points → use 0
            fn = random.choice(["sin", "cos"])
            a = 0
            if fn == "sin":
                f_latex = rf"\sin({x})"
                y0, m = 0, 1
            else:
                f_latex = rf"\cos({x})"
                y0, m = 1, 0
            if m == 0:
                # vertical normal / horizontal tangent
                prompt = (
                    rf"\text{{Find the tangent line to }}y={f_latex}"
                    rf"\text{{ at }}{x}={a}."
                )
                answer = rf"y={y0}"
                return prompt, "tangent line", answer if include_answer_key else None
        elif family == "trig_chain":
            k = random.randint(2, 4)
            f_latex = random.choice(
                [rf"\sin({k}{x})", rf"\cos({k}{x})", rf"\sin({x}^{{2}})"]
            )
            a = 0
            if "sin" in f_latex and "^{" not in f_latex:
                y0, m = 0, k
            elif "cos" in f_latex:
                y0, m = 1, 0
                prompt = (
                    rf"\text{{Find the tangent line to }}y={f_latex}"
                    rf"\text{{ at }}{x}={a}."
                )
                answer = rf"y={y0}"
                return prompt, "tangent line", answer if include_answer_key else None
            else:
                # sin(x^2) at 0: y=0, m=0
                y0, m = 0, 0
                prompt = (
                    rf"\text{{Find the tangent line to }}y={f_latex}"
                    rf"\text{{ at }}{x}={a}."
                )
                answer = r"y=0"
                return prompt, "tangent line", answer if include_answer_key else None
        elif family == "exp":
            k = random.randint(1, 3)
            a = 0
            form = random.choice(["e^{kx}", "exp rewritten"])
            if form == "e^{kx}":
                f_latex = rf"e^{{{k}{x}}}" if k != 1 else rf"e^{{{x}}}"
            else:
                # alternate ordering: exp(kx)
                f_latex = rf"\exp({k}{x})" if k != 1 else rf"\exp({x})"
            y0 = 1
            m = k
        elif family == "ln":
            a = random.choice([1, 2])
            f_latex = random.choice([rf"\ln({x})", rf"\ln({x}^{{2}})", rf"\ln(2{x})"])
            if f_latex == rf"\ln({x})":
                y0_tex = r"0" if a == 1 else rf"\ln({a})"
                m_frac = Fraction(1, a)
            elif f_latex == rf"\ln({x}^{{2}})":
                y0_tex = r"0" if a == 1 else rf"\ln({a * a})"
                m_frac = Fraction(2, a)
            else:
                y0_tex = r"\ln(2)" if a == 1 else rf"\ln({2 * a})"
                m_frac = Fraction(1, a)
            if want_normal:
                ns = -Fraction(1) / m_frac
                prompt = (
                    rf"\text{{Find the normal line to }}y={f_latex}"
                    rf"\text{{ at }}{x}={a}."
                )
                answer = rf"y-{y0_tex}={frac_latex(ns)}\left({x}-{a}\right)"
                return prompt, "normal line", answer if include_answer_key else None
            prompt = (
                rf"\text{{Find the tangent line to }}y={f_latex}"
                rf"\text{{ at }}{x}={a}."
            )
            answer = rf"y-{y0_tex}={frac_latex(m_frac)}\left({x}-{a}\right)"
            return prompt, "tangent line", answer if include_answer_key else None
        else:  # rational_linear (ax+b)/(cx+d) simplified: (x+1)/(x+2) style
            p = random.randint(1, 3)
            q = random.randint(1, 4)
            if p == q:
                q = p + 1
            a = 0
            # f=(x+p)/(x+q); f(0)=p/q; f'=(q-p)/(x+q)^2 → f'(0)=(q-p)/q^2
            order = random.choice(["fraction", "factored_num"])
            if order == "fraction":
                f_latex = rf"\frac{{{x}+{p}}}{{{x}+{q}}}"
            else:
                f_latex = rf"\frac{{{format_linear_latex(1, p, variable=x)}}}{{{format_linear_latex(1, q, variable=x)}}}"
            y0_tex = frac_latex(Fraction(p, q))
            m_frac = Fraction(q - p, q * q)
            prompt = (
                rf"\text{{Find the tangent line to }}y={f_latex}"
                rf"\text{{ at }}{x}={a}."
            )
            answer = rf"y-{y0_tex}={frac_latex(m_frac)}\left({x}-{a}\right)"
            return prompt, "tangent line", answer if include_answer_key else None

        # Generic poly / mono / exp / trig path with integer slope
        assert isinstance(m, int)
        assert isinstance(y0, int)
        a_pt = a  # type: ignore[name-defined]
        if want_normal and m != 0:
            ns = frac_latex(Fraction(-1, m))
            prompt = (
                rf"\text{{Find the normal line to }}y={f_latex}"
                rf"\text{{ at }}{x}={a_pt}."
            )
            answer = rf"y-{y0}={ns}\left({x}-{a_pt}\right)"
            return prompt, "normal line", answer if include_answer_key else None
        if want_normal and m == 0:
            prompt = (
                rf"\text{{Find the normal line to }}y={f_latex}"
                rf"\text{{ at }}{x}={a_pt}."
            )
            answer = rf"{x}={a_pt}"
            return prompt, "normal line", answer if include_answer_key else None
        prompt = (
            rf"\text{{Find the tangent line to }}y={f_latex}"
            rf"\text{{ at }}{x}={a_pt}."
        )
        answer = rf"y-{y0}={m}\left({x}-{a_pt}\right)"
        return prompt, "tangent line", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


# ---------------------------------------------------------------------------
# Pilot 2: differentials (OpenStax 4.2 Ex 4.8: y=x^2+2x and y=cos x)
# ---------------------------------------------------------------------------


def _differentials(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        family = {
            "easy": random.choice(["poly_power", "poly_quad", "trig"]),
            "medium": random.choice(["poly_quad", "trig", "exp", "radical", "reciprocal"]),
            "hard": random.choice(["product", "quotient", "chain_exp", "ln", "eval_dx"]),
        }[tier]

        if family == "poly_power":
            n = random.randint(2, 5)
            y = f"{x}^{{{n}}}"
            dy = rf"{n}{x}^{{{n - 1}}}\,d{x}" if n - 1 != 1 else rf"{n}{x}\,d{x}"
            if n - 1 == 0:
                dy = rf"{n}\,d{x}"
        elif family == "poly_quad":
            # OpenStax: y = x^2 + 2x — also reversed / factored
            b = random.randint(1, 5)
            coeffs = [1, b, 0]
            y = _poly_display(coeffs, x)
            # dy = (2x+b) dx
            inner = format_linear_latex(2, b, variable=x)
            dy = rf"\left({inner}\right)\,d{x}"
        elif family == "trig":
            fn = random.choice(["sin", "cos", "tan"])
            # alternate: sin x vs \sin(x)
            if fn == "sin":
                y = random.choice([rf"\sin({x})", rf"\sin {x}"])
                dy = rf"\cos({x})\,d{x}"
            elif fn == "cos":
                y = random.choice([rf"\cos({x})", rf"\cos {x}"])
                dy = rf"-\sin({x})\,d{x}"
            else:
                y = rf"\tan({x})"
                dy = rf"\sec^{{2}}({x})\,d{x}"
        elif family == "exp":
            k = random.randint(1, 4)
            y = random.choice(
                [
                    rf"e^{{{k}{x}}}" if k != 1 else rf"e^{{{x}}}",
                    rf"\exp({k}{x})" if k != 1 else rf"\exp({x})",
                ]
            )
            dy = (
                rf"{k}e^{{{k}{x}}}\,d{x}"
                if k != 1
                else rf"e^{{{x}}}\,d{x}"
            )
        elif family == "radical":
            y = random.choice([rf"\sqrt{{{x}}}", rf"{x}^{{1/2}}"])
            dy = rf"\frac{{1}}{{2\sqrt{{{x}}}}}\,d{x}"
        elif family == "reciprocal":
            y = random.choice([rf"\frac{{1}}{{{x}}}", rf"{x}^{{-1}}"])
            dy = rf"-\frac{{1}}{{{x}^{{2}}}}\,d{x}"
        elif family == "product":
            # y = x sin x
            y = random.choice(
                [rf"{x}\sin({x})", rf"\sin({x})\,{x}", rf"{x}\cdot\sin({x})"]
            )
            dy = rf"\left(\sin({x})+{x}\cos({x})\right)\,d{x}"
        elif family == "quotient":
            y = random.choice(
                [
                    rf"\frac{{{x}}}{{{x}+1}}",
                    rf"{x}({x}+1)^{{-1}}",
                ]
            )
            dy = rf"\frac{{1}}{{\left({x}+1\right)^{{2}}}}\,d{x}"
        elif family == "chain_exp":
            # y = e^{x^2}
            y = random.choice([rf"e^{{{x}^{{2}}}}", rf"\exp({x}^{{2}})"])
            dy = rf"2{x}e^{{{x}^{{2}}}}\,d{x}"
        elif family == "ln":
            y = random.choice([rf"\ln({x})", rf"\ln|{x}|", rf"\log({x})"])
            dy = rf"\frac{{1}}{{{x}}}\,d{x}"
        else:  # eval_dx — OpenStax style: find dy when x=a, dx=h
            a = random.randint(2, 5)
            h = random.choice([Fraction(1, 10), Fraction(1, 5), Fraction(1, 2)])
            b = random.randint(1, 4)
            coeffs = [1, b, 0]
            y = _poly_display(coeffs, x, style=random.choice(["standard", "reversed", "factored_linear"]))
            # dy = (2x+b) dx at x=a
            slope = 2 * a + b
            dy_val = frac_latex(Fraction(slope) * h)
            prompt = (
                rf"\text{{For }}y={y},\text{{ find }}dy\text{{ when }}"
                rf"{x}={a}\text{{ and }}d{x}={frac_latex(h)}."
            )
            answer = dy_val
            return prompt, "differential evaluation", answer if include_answer_key else None

        prompt = rf"\text{{For }}y={y},\text{{ find }}dy."
        answer = rf"dy={dy}"
        return prompt, "differential", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


# ---------------------------------------------------------------------------
# Pilot 3: log/exp with substitution (OpenStax 5.5–5.6)
# ---------------------------------------------------------------------------


def _integral_log_exp_substitution(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        family = {
            "easy": random.choice(["exp_linear", "reciprocal_linear", "plain_exp"]),
            "medium": random.choice(
                ["log_du_over_u", "exp_chain_poly", "exp_over_one_plus_exp"]
            ),
            "hard": random.choice(
                ["exp_chain_poly", "log_du_over_u_reordered", "mixed_rewrite"]
            ),
        }[tier]

        if family == "plain_exp":
            # OpenStax 5.37: ∫ e^{-x} dx — also e^{kx}
            k = random.choice([-1, 1, 2, 3, -2])
            if k == 1:
                integrand = rf"e^{{{x}}}"
                answer = rf"e^{{{x}}}+C"
            elif k == -1:
                integrand = random.choice([rf"e^{{-{x}}}", rf"e^{{(-1){x}}}"])
                answer = rf"-e^{{-{x}}}+C"
            else:
                integrand = rf"e^{{{k}{x}}}"
                answer = rf"\frac{{1}}{{{k}}}e^{{{k}{x}}}+C"
        elif family == "exp_linear":
            a = random.randint(2, 5)
            b = random_int_range(-4, 4, exclude={0})
            # ∫ e^{ax+b} dx — standard ax+b vs constant-first b+ax
            std = format_linear_latex(a, b, variable=x)
            if random.choice([True, False]):
                exponent = std
            else:
                mono = format_monomial_safe(a, x)
                exponent = f"{b}+{mono}" if b > 0 else f"{b}+{mono}"
            integrand = rf"e^{{{exponent}}}"
            answer = rf"\frac{{1}}{{{a}}}e^{{{std}}}+C"
        elif family == "reciprocal_linear":
            # ∫ 1/(ax+b) dx = (1/a) ln|ax+b|
            a = random.randint(1, 5)
            b = random_int_range(-5, 5, exclude={0})
            inner = format_linear_latex(a, b, variable=x)
            form = random.choice(["frac", "recip_power", "reversed_inner"])
            if form == "frac":
                integrand = rf"\frac{{1}}{{{inner}}}"
            elif form == "recip_power":
                integrand = rf"\left({inner}\right)^{{-1}}"
            else:
                mono = format_monomial_safe(a, x)
                inner_rev = f"{b}+{mono}"
                integrand = rf"\frac{{1}}{{{inner_rev}}}"
            if a == 1:
                answer = rf"\ln\left|{inner}\right|+C"
            else:
                answer = rf"\frac{{1}}{{{a}}}\ln\left|{inner}\right|+C"
        elif family == "log_du_over_u":
            # ∫ 2x/(x^2+1) dx = ln|x^2+1|
            # orderings: 2x/(x^2+1), (x^2+1)^{-1}·2x, left-multiplied inverse
            c = random.randint(1, 4)
            # ∫ n x^{n-1} / (x^n + c)  or specifically 2x/(x^2+c)
            power = random.choice([2, 3]) if tier != "easy" else 2
            coef = power  # so du matches
            den = rf"{x}^{{{power}}}+{c}"
            form = random.choice(["frac", "right_mul", "left_mul"])
            if form == "frac":
                integrand = rf"\frac{{{coef}{x}^{{{power - 1}}}}}{{{den}}}"
            elif form == "right_mul":
                integrand = rf"{coef}{x}^{{{power - 1}}}\left({den}\right)^{{-1}}"
            else:
                integrand = rf"\left({den}\right)^{{-1}}({coef}{x}^{{{power - 1}}})"
            answer = rf"\ln\left|{den}\right|+C"
        elif family == "log_du_over_u_reordered":
            # Same skill, harder rewrite: \frac{x}{x^2+4} needs factor 1/2
            c = random.choice([1, 4, 9])
            form = random.choice(["half_missing", "three_x", "reversed_den"])
            if form == "half_missing":
                integrand = rf"\frac{{{x}}}{{{x}^{{2}}+{c}}}"
                answer = rf"\frac{{1}}{{2}}\ln\left|{x}^{{2}}+{c}\right|+C"
            elif form == "three_x":
                integrand = rf"\frac{{3{x}}}{{{x}^{{2}}+{c}}}"
                answer = rf"\frac{{3}}{{2}}\ln\left|{x}^{{2}}+{c}\right|+C"
            else:
                integrand = rf"\frac{{2{x}}}{{{c}+{x}^{{2}}}}"
                answer = rf"\ln\left|{x}^{{2}}+{c}\right|+C"
        elif family == "exp_chain_poly":
            # OpenStax 5.39: ∫ 3x^2 e^{2x^3} dx
            # variants: 2x e^{x^2}, x e^{x^2}, e^{x^2}·2x (order)
            choice = random.choice(["x2", "x3", "reordered"])
            if choice == "x2":
                integrand = random.choice(
                    [
                        rf"2{x}e^{{{x}^{{2}}}}",
                        rf"e^{{{x}^{{2}}}}\cdot 2{x}",
                        rf"2{x}\exp({x}^{{2}})",
                    ]
                )
                answer = rf"e^{{{x}^{{2}}}}+C"
            elif choice == "x3":
                integrand = random.choice(
                    [
                        rf"3{x}^{{2}}e^{{{x}^{{3}}}}",
                        rf"e^{{{x}^{{3}}}}\cdot 3{x}^{{2}}",
                    ]
                )
                answer = rf"e^{{{x}^{{3}}}}+C"
            else:
                # 6x^2 e^{2x^3}
                integrand = random.choice(
                    [
                        rf"6{x}^{{2}}e^{{2{x}^{{3}}}}",
                        rf"e^{{2{x}^{{3}}}}\cdot 6{x}^{{2}}",
                    ]
                )
                answer = rf"e^{{2{x}^{{3}}}}+C"
        elif family == "exp_over_one_plus_exp":
            # OpenStax 5.38 pattern: e^x / (1+e^x)
            form = random.choice(["frac", "rewrite"])
            if form == "frac":
                integrand = rf"\frac{{e^{{{x}}}}}{{1+e^{{{x}}}}}"
            else:
                integrand = rf"e^{{{x}}}\left(1+e^{{{x}}}\right)^{{-1}}"
            answer = rf"\ln\left|1+e^{{{x}}}\right|+C"
        else:  # mixed_rewrite
            # ∫ e^{2x}/(e^{2x}+5) or (2e^{2x})/(e^{2x}+5)
            c = random.randint(2, 6)
            form = random.choice(["exact_du", "half_factor", "reordered"])
            if form == "exact_du":
                integrand = rf"\frac{{2e^{{2{x}}}}}{{e^{{2{x}}}+{c}}}"
                answer = rf"\ln\left|e^{{2{x}}}+{c}\right|+C"
            elif form == "half_factor":
                integrand = rf"\frac{{e^{{2{x}}}}}{{e^{{2{x}}}+{c}}}"
                answer = rf"\frac{{1}}{{2}}\ln\left|e^{{2{x}}}+{c}\right|+C"
            else:
                integrand = rf"\left(e^{{2{x}}}+{c}\right)^{{-1}}\cdot 2e^{{2{x}}}"
                answer = rf"\ln\left|e^{{2{x}}}+{c}\right|+C"

        prompt = rf"\int {integrand}\,d{x}"
        return prompt, "log/exp substitution integral", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def format_monomial_safe(coef: int, variable: str) -> str:
    if coef == 1:
        return variable
    if coef == -1:
        return f"-{variable}"
    return f"{coef}{variable}"


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "tangent_normal_line": _tangent_normal_line,
    "differentials": _differentials,
    "integral_log_exp_substitution": _integral_log_exp_substitution,
}
