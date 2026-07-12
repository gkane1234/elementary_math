"""Calculus generators: limits, derivatives, integrals."""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from ..settings.params import calculus_params_from_settings
from .utils import (
    _make_questions,
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
    frac_latex,
    random_int_range,
)


def _format_coef(coef: int, power: int, variable: str) -> str:
    return format_monomial_latex(coef, variable=variable, degree=power) or "0"


def _sparse_to_dense(terms: list[tuple[int, int]]) -> list[int]:
    if not terms:
        return [0]
    max_power = max(power for _, power in terms)
    coeffs = [0] * (max_power + 1)
    for coef, power in terms:
        coeffs[max_power - power] += coef
    return coeffs


def _format_poly_terms(terms: list[tuple[int, int]], variable: str) -> str:
    return format_polynomial_latex(_sparse_to_dense(terms), variable=variable)


def _random_poly_terms(params) -> list[tuple[int, int]]:
    terms: list[tuple[int, int]] = []
    used_powers: set[int] = set()
    for _ in range(params.term_count):
        power = random.randint(params.power_min, params.power_max)
        while power in used_powers:
            power = random.randint(params.power_min, params.power_max)
        used_powers.add(power)
        coef = random_int_range(params.coef_min, params.coef_max, exclude={0})
        terms.append((coef, power))
    if params.include_constant_term and 0 not in used_powers and random.choice([True, False]):
        terms.append((random.randint(params.coef_min, params.coef_max), 0))
    return terms


def _eval_poly(terms: list[tuple[int, int]], x: int) -> int:
    return sum(coef * (x**power) for coef, power in terms)


def _limit_direct_evaluation(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        terms = _random_poly_terms(params)
        approach = random.randint(params.limit_approach_min, params.limit_approach_max)
        value = _eval_poly(terms, approach)
        poly = _format_poly_terms(terms, params.variable)
        prompt = (
            f"\\lim_{{{params.variable} \\to {approach}}} "
            f"\\left({poly}\\right)"
        )
        answer = str(value) if include_answer_key else None
        return prompt, f"limit at {approach}", answer

    return _make_questions(topic, count, include_answer_key, build)


def _limit_at_infinity(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        lead_coef = random_int_range(params.coef_min, params.coef_max, exclude={0})
        lead_power = random.randint(max(1, params.power_min), params.power_max)
        lower_power = random.randint(0, max(0, lead_power - 1))
        lower_coef = random_int_range(params.coef_min, params.coef_max, exclude={0})
        num = _format_poly_terms([(lead_coef, lead_power), (lower_coef, lower_power)], params.variable)
        den_power = random.randint(0, lead_power)
        den_coef = random_int_range(1, max(1, params.coef_max))
        den = _format_coef(den_coef, den_power, params.variable)
        infinity = random.choice([r"\infty", r"-\infty"])
        prompt = (
            f"\\lim_{{{params.variable} \\to {infinity}}} "
            f"\\frac{{{num}}}{{{den}}}"
        )
        if lead_power > den_power:
            answer = r"\infty" if (lead_coef > 0) == (infinity == r"\infty") else r"-\infty"
        elif lead_power < den_power:
            answer = "0"
        else:
            answer = frac_latex(Fraction(lead_coef, den_coef))
        if not include_answer_key:
            answer = None
        return prompt, "limit at infinity", answer

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_power_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        terms = _random_poly_terms(params)
        poly = _format_poly_terms(terms, params.variable)
        deriv_terms: list[tuple[int, int]] = []
        for coef, power in terms:
            if power == 0:
                continue
            deriv_terms.append((coef * power, power - 1))
        deriv = _format_poly_terms(deriv_terms, params.variable) if deriv_terms else "0"
        prompt = (
            f"\\frac{{d}}{{d{params.variable}}} "
            f"\\left({poly}\\right)"
        )
        answer = deriv if include_answer_key else None
        return prompt, "power rule derivative", answer

    return _make_questions(topic, count, include_answer_key, build)


def _integral_power_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        terms = _random_poly_terms(params)
        if params.require_positive_power:
            terms = [(coef, max(1, power)) for coef, power in terms if power != 0]
            if not terms:
                terms = [(random_int_range(params.coef_min, params.coef_max, exclude={0}), 1)]
        poly = _format_poly_terms(terms, params.variable)
        integral_terms: list[str] = []
        for coef, power in terms:
            new_power = power + 1
            new_coef = Fraction(coef, new_power)
            coef_latex = frac_latex(new_coef)
            if coef_latex == "1":
                term = f"{params.variable}^{{{new_power}}}"
            elif coef_latex == "-1":
                term = f"-{params.variable}^{{{new_power}}}"
            else:
                term = f"{coef_latex}{params.variable}^{{{new_power}}}"
            integral_terms.append(term)
        if params.include_constant_term and random.choice([True, False]):
            integral_terms.append("C")
        answer_body = " + ".join(integral_terms) if integral_terms else "C"
        prompt = f"\\int {poly} \\, d{params.variable}"
        answer = answer_body if include_answer_key else None
        return prompt, "power rule integral", answer

    return _make_questions(topic, count, include_answer_key, build)


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
            # (fg)' = a(cx+d) + c(ax+b) = 2ac x + (ad+bc)
            answer = format_polynomial_latex([2 * a * c, a * d + b * c], variable=x)
            prompt = rf"\frac{{d}}{{d{x}}}\left[\left({f}\right)\left({g}\right)\right]"
        elif tier == "medium":
            a = random.randint(1, 3)
            b = random_int_range(-4, 4, exclude={0})
            c = random_int_range(-4, 4, exclude={0})
            d, e = _linear_pair(4)
            f = format_polynomial_latex([a, b, c], variable=x)
            g = format_linear_latex(d, e, variable=x)
            # f' = 2ax+b, g'=d
            # (fg)' = (2ax+b)(dx+e) + d(ax^2+bx+c)
            # = (2a d)x^2 + (2a e + b d)x + b e + d a x^2 + d b x + d c
            # = (2ad + ad)x^2 + (2ae + bd + db)x + (be + dc)
            # = 3ad x^2 + (2ae + 2bd)x + (be + dc)
            lead = 3 * a * d
            mid = 2 * a * e + 2 * b * d
            const = b * e + d * c
            answer = format_polynomial_latex([lead, mid, const], variable=x)
            prompt = rf"\frac{{d}}{{d{x}}}\left[\left({f}\right)\left({g}\right)\right]"
        else:
            n = random.randint(2, 4)
            a, b = _linear_pair(4)
            f = format_monomial_latex(1, variable=x, degree=n) or f"{x}^{{{n}}}"
            g = format_linear_latex(a, b, variable=x)
            # (x^n (ax+b))' = n x^{n-1}(ax+b) + a x^n = (n+1)a x^n + n b x^{n-1}
            coeffs = [(n + 1) * a, n * b] + [0] * (n - 1)
            answer = format_polynomial_latex(coeffs, variable=x)
            prompt = rf"\frac{{d}}{{d{x}}}\left[{f}\left({g}\right)\right]"
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
            num = format_linear_latex(a, b, variable=x)
            den = format_linear_latex(c, d, variable=x)
            # ((ax+b)/(cx+d))' = (a(cx+d) - c(ax+b))/(cx+d)^2 = (ad-bc)/(cx+d)^2
            numer = a * d - b * c
            while numer == 0:
                a, b = _linear_pair(4)
                c, d = _linear_pair(4)
                num = format_linear_latex(a, b, variable=x)
                den = format_linear_latex(c, d, variable=x)
                numer = a * d - b * c
            answer = rf"\frac{{{numer}}}{{\left({den}\right)^{{2}}}}"
            prompt = rf"\frac{{d}}{{d{x}}}\left[\frac{{{num}}}{{{den}}}\right]"
        elif tier == "medium":
            a = random.randint(1, 3)
            b = random_int_range(-4, 4, exclude={0})
            c = random_int_range(-3, 3, exclude={0})
            d, e = _linear_pair(3)
            num = format_polynomial_latex([a, b, c], variable=x)
            den = format_linear_latex(d, e, variable=x)
            # f=ax^2+bx+c, g=dx+e; f'=2ax+b, g'=d
            # (f'g-fg')/g^2 = ((2ax+b)(dx+e) - d(ax^2+bx+c))/(dx+e)^2
            # num = (2ad)x^2+(2ae+bd)x+be - (ad x^2 + bd x + cd)
            #     = ad x^2 + (2ae)x + (be - cd)
            n2, n1, n0 = a * d, 2 * a * e, b * e - c * d
            numer = format_polynomial_latex([n2, n1, n0], variable=x)
            answer = rf"\frac{{{numer}}}{{\left({den}\right)^{{2}}}}"
            prompt = rf"\frac{{d}}{{d{x}}}\left[\frac{{{num}}}{{{den}}}\right]"
        else:
            a, b = _linear_pair(3)
            c = random.randint(1, 3)
            d = random_int_range(-3, 3, exclude={0})
            num = format_linear_latex(a, b, variable=x)
            den = format_polynomial_latex([c, 0, d], variable=x)  # cx^2 + d
            # f=ax+b, g=cx^2+d; f'=a, g'=2cx
            # (a(cx^2+d) - (ax+b)(2cx))/(cx^2+d)^2 = (a c x^2 + a d - 2 a c x^2 - 2 b c x)/(...)
            # = (-a c x^2 - 2 b c x + a d)/(cx^2+d)^2
            numer = format_polynomial_latex([-a * c, -2 * b * c, a * d], variable=x)
            answer = rf"\frac{{{numer}}}{{\left({den}\right)^{{2}}}}"
            prompt = rf"\frac{{d}}{{d{x}}}\left[\frac{{{num}}}{{{den}}}\right]"
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
            n = random.randint(2, 4)
            inner = format_linear_latex(a, b, variable=x)
            prompt = rf"\frac{{d}}{{d{x}}}\left({inner}\right)^{{{n}}}"
            # n(ax+b)^{n-1} * a
            outer = n * a
            power = n - 1
            power_latex = f"\\left({inner}\\right)" if power == 1 else rf"\left({inner}\right)^{{{power}}}"
            if outer == 1:
                answer = power_latex
            elif outer == -1:
                answer = f"-{power_latex}"
            else:
                answer = f"{outer}{power_latex}"
        elif tier == "medium":
            a = random.randint(1, 3)
            c = random_int_range(-4, 4, exclude={0})
            n = random.randint(2, 4)
            inner = format_polynomial_latex([a, 0, c], variable=x)  # ax^2+c
            prompt = rf"\frac{{d}}{{d{x}}}\left({inner}\right)^{{{n}}}"
            # n(ax^2+c)^{n-1} * 2ax
            coef = n * 2 * a
            answer = rf"{coef}{x}\left({inner}\right)^{{{n - 1}}}"
        else:
            a = random.randint(2, 5)
            n = random.randint(2, 4)
            prompt = rf"\frac{{d}}{{d{x}}}\sin\left({a}{x}^{{{n}}}\right)"
            # cos(a x^n) * a n x^{n-1}
            answer = rf"{a * n}{x}^{{{n - 1}}}\cos\left({a}{x}^{{{n}}}\right)"
        return prompt, "chain rule", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


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
                ]
            )
            prompt = rf"\frac{{d}}{{d{x}}}{fn}({x})"
            answer = f"{deriv}({x})"
        elif tier == "medium":
            k = random.randint(2, 6)
            fn, deriv = random.choice(
                [
                    ("\\sin", "\\cos"),
                    ("\\cos", "-\\sin"),
                    ("\\tan", "\\sec^{2}"),
                ]
            )
            arg = format_monomial_latex(k, variable=x) or f"{k}{x}"
            prompt = rf"\frac{{d}}{{d{x}}}{fn}({arg})"
            if deriv.startswith("-"):
                answer = rf"-{k}{deriv[1:]}({arg})"
            else:
                answer = rf"{k}{deriv}({arg})"
        else:
            k = random.randint(2, 5)
            choice = random.choice(["product", "sec", "chain"])
            if choice == "product":
                prompt = rf"\frac{{d}}{{d{x}}}\left[{x}\sin({x})\right]"
                answer = rf"\sin({x})+{x}\cos({x})"
            elif choice == "sec":
                prompt = rf"\frac{{d}}{{d{x}}}\sec({k}{x})"
                answer = rf"{k}\sec({k}{x})\tan({k}{x})"
            else:
                prompt = rf"\frac{{d}}{{d{x}}}\sin^{{2}}({x})"
                answer = rf"2\sin({x})\cos({x})"
        return prompt, "trigonometric derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_implicit(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(2, 9)
        if tier == "easy":
            prompt = rf"{x}^{{2}}+y^{{2}}={a}"
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{{x}}}{{y}}"
        elif tier == "medium":
            prompt = rf"{x}^{{2}}+{x}y={a}"
            # 2x + y + x y' = 0 → y' = -(2x+y)/x
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{2{x}+y}}{{{x}}}"
        else:
            prompt = rf"{x}^{{3}}+y^{{3}}={a}"
            # 3x^2 + 3y^2 y' = 0 → y' = -x^2/y^2
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{{x}^{{2}}}}{{y^{{2}}}}"
        instruction = rf"\text{{Differentiate implicitly: }}{prompt}.\text{{ Solve for }}\frac{{dy}}{{d{x}}}."
        return instruction, "implicit differentiation", answer if include_answer_key else None

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
            # cubic → second derivative linear
            f = format_polynomial_latex([a, b, c, d], variable=x)
            prompt = rf"\text{{Find }}f''({x})\text{{ for }}f({x})={f}."
            answer = format_linear_latex(6 * a, 2 * b, variable=x)
        elif tier == "medium":
            e = random_int_range(-4, 4, exclude={0})
            f = format_polynomial_latex([a, b, c, d, e], variable=x)
            prompt = rf"\text{{Find }}f'''({x})\text{{ for }}f({x})={f}."
            # f = a x^4 + b x^3 + c x^2 + d x + e
            # f''' = 24a x + 6b
            answer = format_linear_latex(24 * a, 6 * b, variable=x)
        else:
            f = format_polynomial_latex([a, b, c, d], variable=x)
            t = random.randint(1, 4)
            prompt = rf"\text{{Find }}f''({t})\text{{ for }}f({x})={f}."
            answer = str(6 * a * t + 2 * b)
        return prompt, "higher order derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _average_rate_of_change(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(0, 3)
        width = random.randint(1, 4) if tier == "easy" else random.randint(2, 5)
        b = a + width
        if tier == "easy":
            f = format_polynomial_latex([1, 0, 0], variable=x)  # x^2
            fa, fb = a * a, b * b
        elif tier == "medium":
            k = random.randint(1, 3)
            f = format_polynomial_latex([k, 0, 0, 0], variable=x)  # k x^3
            fa, fb = k * a**3, k * b**3
        else:
            p = random.randint(1, 3)
            q = random_int_range(-4, 4, exclude={0})
            f = format_polynomial_latex([p, 0, q], variable=x)  # p x^2 + q
            fa, fb = p * a * a + q, p * b * b + q
        rate = Fraction(fb - fa, b - a)
        prompt = (
            rf"\text{{Find the average rate of change of }}f({x})={f}"
            rf"\text{{ on }}[{a},{b}]."
        )
        answer = frac_latex(rate)
        return prompt, "average rate of change", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _definition_of_derivative(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 5)
        if tier == "easy":
            prompt = rf"\lim_{{h\to 0}}\frac{{({a}+h)^{{2}}-{a * a}}}{{h}}"
            answer = str(2 * a)
        elif tier == "medium":
            prompt = rf"\lim_{{h\to 0}}\frac{{({a}+h)^{{3}}-{a ** 3}}}{{h}}"
            answer = str(3 * a * a)
        else:
            k = random.randint(2, 4)
            prompt = (
                rf"\text{{Use the definition to find }}f'({a})"
                rf"\text{{ for }}f({x})={k}{x}^{{2}}."
            )
            answer = str(2 * k * a)
        return prompt, "definition of the derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _integral_trigonometric(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            fn, antider = random.choice(
                [
                    ("\\sin", "-\\cos"),
                    ("\\cos", "\\sin"),
                ]
            )
            prompt = rf"\int {fn}({x})\,d{x}"
            answer = rf"{antider}({x})+C"
        elif tier == "medium":
            k = random.randint(2, 6)
            fn, antider, sign = random.choice(
                [
                    ("\\sin", "\\cos", -1),
                    ("\\cos", "\\sin", 1),
                ]
            )
            arg = format_monomial_latex(k, variable=x) or f"{k}{x}"
            prompt = rf"\int {fn}({arg})\,d{x}"
            coef = frac_latex(Fraction(sign, k))
            if coef == "1":
                answer = rf"{antider}({arg})+C"
            elif coef == "-1":
                answer = rf"-{antider}({arg})+C"
            else:
                answer = rf"{coef}{antider}({arg})+C"
        else:
            k = random.randint(2, 5)
            choice = random.choice(["sec2", "csc2", "sec_tan"])
            if choice == "sec2":
                prompt = rf"\int \sec^{{2}}({k}{x})\,d{x}"
                answer = rf"\frac{{1}}{{{k}}}\tan({k}{x})+C"
            elif choice == "csc2":
                prompt = rf"\int \csc^{{2}}({k}{x})\,d{x}"
                answer = rf"-\frac{{1}}{{{k}}}\cot({k}{x})+C"
            else:
                prompt = rf"\int \sec({k}{x})\tan({k}{x})\,d{x}"
                answer = rf"\frac{{1}}{{{k}}}\sec({k}{x})+C"
        return prompt, "trigonometric integral", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _integral_substitution(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            a, b = _linear_pair(4)
            n = random.randint(2, 4)
            inner = format_linear_latex(a, b, variable=x)
            # ∫ (ax+b)^n dx = (ax+b)^{n+1}/(a(n+1)) + C
            prompt = rf"\int \left({inner}\right)^{{{n}}}\,d{x}"
            den = a * (n + 1)
            answer = rf"\frac{{1}}{{{den}}}\left({inner}\right)^{{{n + 1}}}+C"
        elif tier == "medium":
            n = random.randint(2, 4)
            # ∫ 2x (x^2+1)^n dx = (x^2+1)^{n+1}/(n+1) + C
            prompt = rf"\int 2{x}\left({x}^{{2}}+1\right)^{{{n}}}\,d{x}"
            answer = rf"\frac{{1}}{{{n + 1}}}\left({x}^{{2}}+1\right)^{{{n + 1}}}+C"
        else:
            a = random.randint(2, 4)
            n = random.randint(2, 4)
            # ∫ a x^{a-1} (x^a + 1)^n dx
            prompt = rf"\int {a}{x}^{{{a - 1}}}\left({x}^{{{a}}}+1\right)^{{{n}}}\,d{x}"
            answer = rf"\frac{{1}}{{{n + 1}}}\left({x}^{{{a}}}+1\right)^{{{n + 1}}}+C"
        return prompt, "power rule with substitution", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _riemann_approximate_area(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        # f(x)=x on [0, L] with n equal intervals, midpoint Riemann sum
        if tier == "easy":
            n_intervals, L = 2, 4
        elif tier == "medium":
            n_intervals, L = 4, 4
        else:
            n_intervals, L = 4, 8
        dx = Fraction(L, n_intervals)
        # midpoints of [i*dx, (i+1)*dx] are (i+1/2)*dx; f(mid)=mid
        total = sum((Fraction(2 * i + 1, 2) * dx) * dx for i in range(n_intervals))
        prompt = (
            rf"\text{{Use a midpoint Riemann sum with }}{n_intervals}"
            rf"\text{{ equal intervals to approximate the area under }}"
            rf"f({x})={x}\text{{ on }}[0,{L}]."
        )
        answer = frac_latex(total)
        return prompt, "approximate area", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _first_fundamental_theorem(topic: str, settings: dict) -> list[Question]:
    """Evaluate definite integrals via antiderivatives (FTC I)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = 0
        if tier == "easy":
            b = random.randint(2, 5)
            prompt = rf"\int_{{{a}}}^{{{b}}} {x}\,d{x}"
            answer = frac_latex(Fraction(b * b, 2))
        elif tier == "medium":
            b = random.randint(2, 4)
            k = random.randint(2, 4)
            f = format_monomial_latex(k, variable=x, degree=2) or f"{k}{x}^{{2}}"
            prompt = rf"\int_{{{a}}}^{{{b}}} {f}\,d{x}"
            # ∫ k x^2 = k/3 x^3 from 0 to b
            answer = frac_latex(Fraction(k * b**3, 3))
        else:
            b = random.randint(2, 4)
            p = random.randint(1, 3)
            q = random_int_range(-3, 3, exclude={0})
            f = format_polynomial_latex([p, 0, q], variable=x)
            prompt = rf"\int_{{{a}}}^{{{b}}} \left({f}\right)\,d{x}"
            # ∫ (p x^2 + q) = p/3 x^3 + q x from 0 to b
            answer = frac_latex(Fraction(p * b**3, 3) + q * b)
        return prompt, "first fundamental theorem", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _area_under_curve(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        b = random.randint(2, 5) if tier != "hard" else random.randint(3, 6)
        if tier == "easy":
            f = x
            area = Fraction(b * b, 2)
        elif tier == "medium":
            f = f"{x}^{{2}}"
            area = Fraction(b**3, 3)
        else:
            k = random.randint(2, 4)
            f = format_monomial_latex(k, variable=x, degree=2) or f"{k}{x}^{{2}}"
            area = Fraction(k * b**3, 3)
        prompt = (
            rf"\text{{Find the area under }}y={f}"
            rf"\text{{ from }}{x}=0\text{{ to }}{x}={b}."
        )
        answer = frac_latex(area)
        return prompt, "area under a curve", answer if include_answer_key else None

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
            prompt = rf"\frac{{d}}{{d{x}}}{fn}({x})"
            answer = deriv
        elif tier == "medium":
            k = random.randint(2, 5)
            fn, template = random.choice(
                [
                    ("\\arcsin", "arcsin"),
                    ("\\arctan", "arctan"),
                ]
            )
            arg = format_monomial_latex(k, variable=x) or f"{k}{x}"
            prompt = rf"\frac{{d}}{{d{x}}}{fn}({arg})"
            if template == "arcsin":
                answer = rf"\frac{{{k}}}{{\sqrt{{1-({arg})^{{2}}}}}}"
            else:
                answer = rf"\frac{{{k}}}{{1+({arg})^{{2}}}}"
        else:
            k = random.randint(2, 4)
            prompt = rf"\frac{{d}}{{d{x}}}\arctan({x}^{{{k}}})"
            answer = rf"\frac{{{k}{x}^{{{k - 1}}}}}{{1+{x}^{{{2 * k}}}}}"
        return prompt, "inverse trigonometric derivative", answer if include_answer_key else None

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
                prompt = rf"\frac{{d}}{{d{x}}}{base}^{{{x}}}"
                answer = rf"{base}^{{{x}}}\ln({base})"
            else:
                prompt = rf"\frac{{d}}{{d{x}}}\log_{{{base}}}({x})"
                answer = rf"\frac{{1}}{{{x}\ln({base})}}"
        elif tier == "medium":
            k = random.randint(2, 5)
            prompt = rf"\frac{{d}}{{d{x}}}{base}^{{{k}{x}}}"
            answer = rf"{k}{base}^{{{k}{x}}}\ln({base})"
        else:
            k = random.randint(2, 4)
            prompt = rf"\frac{{d}}{{d{x}}}\log_{{{base}}}({x}^{{{k}}})"
            answer = rf"\frac{{{k}}}{{{x}\ln({base})}}"
        return prompt, "other-base log/exp derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_from_tables(topic: str, settings: dict) -> list[Question]:
    """Product / quotient / chain using tabulated f,g values (no interactive UI)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 4)
        f_a = random.randint(-6, 6)
        fp_a = random_int_range(-6, 6, exclude={0})
        g_a = random_int_range(-6, 6, exclude={0})
        gp_a = random_int_range(-6, 6, exclude={0})
        table = (
            rf"f({a})={f_a},\ f'({a})={fp_a},\ g({a})={g_a},\ g'({a})={gp_a}."
        )
        if tier == "easy" or (tier == "medium" and random.random() < 0.5):
            prompt = rf"{table}\quad\text{{Find }}(fg)'({a})."
            answer = str(fp_a * g_a + f_a * gp_a)
        elif tier == "medium":
            prompt = rf"{table}\quad\text{{Find }}\left(\frac{{f}}{{g}}\right)'({a})."
            numer = fp_a * g_a - f_a * gp_a
            answer = frac_latex(Fraction(numer, g_a * g_a))
        else:
            # (f∘g)'(a) = f'(g(a)) g'(a) — need f' at g(a)
            # Reuse table with an extra f'(g(a)) value when g(a) ≠ a
            u = g_a
            fp_u = random_int_range(-5, 5, exclude={0})
            prompt = (
                rf"f'({u})={fp_u},\ g({a})={g_a},\ g'({a})={gp_a}."
                rf"\quad\text{{Find }}(f\circ g)'({a})."
            )
            answer = str(fp_u * gp_a)
        return prompt, "derivative from tables", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _rolles_theorem(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            n = random.randint(2, 5)
            prompt = (
                rf"\text{{Find }}c\text{{ guaranteed by Rolle's Theorem for }}"
                rf"f({x})={x}^{{2}}-{n * n}\text{{ on }}[-{n},{n}]."
            )
            answer = "0"
        elif tier == "medium":
            # f(x)=(x-a)(x-b)=x^2-(a+b)x+ab on [a,b]; c midpoint
            a = random.randint(-4, 1)
            b = a + random.randint(2, 5)
            mid = Fraction(a + b, 2)
            f = format_polynomial_latex([1, -(a + b), a * b], variable=x)
            prompt = (
                rf"\text{{Find }}c\text{{ guaranteed by Rolle's Theorem for }}"
                rf"f({x})={f}\text{{ on }}[{a},{b}]."
            )
            answer = frac_latex(mid)
        else:
            # f(x)=x^3 - n^2 x on [-n,n]; f'=3x^2-n^2=0 → x=±n/√3
            n = random.choice([2, 3, 4])
            prompt = (
                rf"\text{{Find all }}c\text{{ guaranteed by Rolle's Theorem for }}"
                rf"f({x})={x}^{{3}}-{n * n}{x}\text{{ on }}[-{n},{n}]."
            )
            answer = rf"c=\pm\frac{{{n}}}{{\sqrt{{3}}}}"
        return prompt, "Rolle's Theorem", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _mean_value_theorem(topic: str, settings: dict) -> list[Question]:
    """Differentiation MVT: find c with f'(c)=(f(b)-f(a))/(b-a)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = 0
        width = random.randint(2, 5) if tier == "easy" else random.randint(3, 6)
        b = a + width
        if tier == "easy":
            f = format_polynomial_latex([1, 0, 0], variable=x)  # x^2
            # f'=2x = (b^2-a^2)/(b-a)=a+b → c=(a+b)/2
            answer = frac_latex(Fraction(a + b, 2))
        elif tier == "medium":
            k = random.randint(1, 3)
            f = format_polynomial_latex([k, 0, 0, 0], variable=x)  # k x^3
            # 3k c^2 = k b^2 → c = b/√3
            answer = rf"\frac{{{b}}}{{\sqrt{{3}}}}"
        else:
            p = random.randint(1, 2)
            q = random_int_range(-3, 3, exclude={0})
            f = format_polynomial_latex([p, 0, q], variable=x)  # p x^2 + q
            answer = frac_latex(Fraction(a + b, 2))
        prompt = (
            rf"\text{{Find }}c\text{{ guaranteed by the Mean Value Theorem for }}"
            rf"f({x})={f}\text{{ on }}[{a},{b}]."
        )
        return prompt, "Mean Value Theorem", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _pi_frac(numer: int, denom: int) -> str:
    """Format (numer/denom)·π as tidy LaTeX."""
    value = Fraction(numer, denom)
    if value.denominator == 1:
        if value.numerator == 1:
            return r"\pi"
        if value.numerator == -1:
            return r"-\pi"
        return rf"{value.numerator}\pi"
    if value.numerator == 1:
        return rf"\frac{{\pi}}{{{value.denominator}}}"
    if value.numerator == -1:
        return rf"-\frac{{\pi}}{{{value.denominator}}}"
    return rf"\frac{{{value.numerator}\pi}}{{{value.denominator}}}"


def _volume_disk_washer(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        n = random.randint(2, 4) if tier == "easy" else random.randint(2, 5)
        if tier == "easy":
            # Disk: y=x on [0,n] about x-axis → V = π∫x^2 = π n^3/3
            prompt = (
                rf"\text{{Find the volume of the solid formed by rotating }}"
                rf"y={x}\text{{ on }}[0,{n}]\text{{ about the }}{x}\text{{-axis (disk method).}}"
            )
            answer = _pi_frac(n**3, 3)
        elif tier == "medium":
            # Disk: y=x^2 on [0,n] → π∫x^4 = π n^5/5
            prompt = (
                rf"\text{{Find the volume of the solid formed by rotating }}"
                rf"y={x}^{{2}}\text{{ on }}[0,{n}]\text{{ about the }}{x}\text{{-axis (disk method).}}"
            )
            answer = _pi_frac(n**5, 5)
        else:
            # Washer: region between y=n and y=x on [0,n] about x-axis
            # V = π∫_0^n (n^2 - x^2) dx = π(n^3 - n^3/3) = 2π n^3/3
            prompt = (
                rf"\text{{Find the volume of the solid formed by rotating the region between }}"
                rf"y={n}\text{{ and }}y={x}\text{{ on }}[0,{n}]"
                rf"\text{{ about the }}{x}\text{{-axis (washer method).}}"
            )
            answer = _pi_frac(2 * n**3, 3)
        return prompt, "volume disk/washer", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _volume_shell(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        n = random.randint(2, 4) if tier != "hard" else random.randint(2, 5)
        if tier == "easy":
            # Shell: y=x on [0,n] about y-axis → V = 2π∫ x·x dx = 2π n^3/3
            prompt = (
                rf"\text{{Find the volume of the solid formed by rotating }}"
                rf"y={x}\text{{ on }}[0,{n}]\text{{ about the }}y\text{{-axis (shell method).}}"
            )
            answer = _pi_frac(2 * n**3, 3)
        elif tier == "medium":
            # Shell: y=x^2 on [0,n] about y-axis → 2π∫ x·x^2 = 2π n^4/4 = π n^4/2
            prompt = (
                rf"\text{{Find the volume of the solid formed by rotating }}"
                rf"y={x}^{{2}}\text{{ on }}[0,{n}]\text{{ about the }}y\text{{-axis (shell method).}}"
            )
            answer = _pi_frac(n**4, 2)
        else:
            # Shell: y=n-x on [0,n] about y-axis → 2π∫ x(n-x) = 2π(n·n^2/2 - n^3/3)=2π(n^3/6)=π n^3/3
            prompt = (
                rf"\text{{Find the volume of the solid formed by rotating }}"
                rf"y={n}-{x}\text{{ on }}[0,{n}]\text{{ about the }}y\text{{-axis (shell method).}}"
            )
            answer = _pi_frac(n**3, 3)
        return prompt, "volume by shells", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _volume_cross_sections(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        n = random.randint(2, 5)
        if tier == "easy":
            prompt = (
                rf"\text{{A solid has square cross sections of side length }}{x}"
                rf"\text{{ for }}0\le {x}\le {n}.\text{{ Find its volume.}}"
            )
            answer = frac_latex(Fraction(n**3, 3))
        elif tier == "medium":
            prompt = (
                rf"\text{{A solid has equilateral-triangle cross sections of side }}{x}"
                rf"\text{{ for }}0\le {x}\le {n}.\text{{ Find its volume.}}"
            )
            # Area = √3/4 s^2 → V = (√3/4)∫x^2 = √3 n^3 / 12
            answer = rf"\frac{{{n**3}\sqrt{{3}}}}{{12}}"
        else:
            prompt = (
                rf"\text{{Cross sections perpendicular to the }}{x}\text{{-axis on }}[0,{n}]"
                rf"\text{{ are semicircles with diameter }}{x}.\text{{ Find the volume.}}"
            )
            # radius x/2, area = (1/2)π(x/2)^2 = π x^2/8 → V = π n^3/24
            answer = _pi_frac(n**3, 24)
        return prompt, "volume cross sections", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _integral_log_exp(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        k = random.randint(2, 5)
        if tier == "easy":
            choice = random.choice(["reciprocal", "exp"])
            if choice == "reciprocal":
                prompt = rf"\int \frac{{1}}{{{x}}}\,d{x}"
                answer = rf"\ln|{x}|+C"
            else:
                prompt = rf"\int e^{{{x}}}\,d{x}"
                answer = rf"e^{{{x}}}+C"
        elif tier == "medium":
            if random.choice([True, False]):
                prompt = rf"\int e^{{{k}{x}}}\,d{x}"
                answer = rf"\frac{{1}}{{{k}}}e^{{{k}{x}}}+C"
            else:
                prompt = rf"\int \frac{{{k}}}{{{x}}}\,d{x}"
                answer = rf"{k}\ln|{x}|+C"
        else:
            base = random.randint(2, 5)
            prompt = rf"\int {base}^{{{x}}}\,d{x}"
            answer = rf"\frac{{{base}^{{{x}}}}}{{\ln({base})}}+C"
        return prompt, "log/exp integral", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _integral_inverse_trig(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            prompt = rf"\int \frac{{1}}{{\sqrt{{1-{x}^{{2}}}}}}\,d{x}"
            answer = rf"\arcsin({x})+C"
        elif tier == "medium":
            prompt = rf"\int \frac{{1}}{{1+{x}^{{2}}}}\,d{x}"
            answer = rf"\arctan({x})+C"
        else:
            a = random.randint(2, 4)
            prompt = rf"\int \frac{{1}}{{{a * a}+{x}^{{2}}}}\,d{x}"
            answer = rf"\frac{{1}}{{{a}}}\arctan\left(\frac{{{x}}}{{{a}}}\right)+C"
        return prompt, "inverse trig integral", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _integration_by_parts(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            prompt = rf"\int {x}e^{{{x}}}\,d{x}"
            answer = rf"{x}e^{{{x}}}-e^{{{x}}}+C"
        elif tier == "medium":
            prompt = rf"\int {x}\sin({x})\,d{x}"
            answer = rf"-{x}\cos({x})+\sin({x})+C"
        else:
            prompt = rf"\int {x}^{{2}}e^{{{x}}}\,d{x}"
            answer = rf"e^{{{x}}}({x}^{{2}}-2{x}+2)+C"
        return prompt, "integration by parts", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _riemann_sum_tables(topic: str, settings: dict) -> list[Question]:
    """Left/right/midpoint Riemann sums from a short value table."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)

    def build() -> tuple[str, str, str | None]:
        # Uniform partitions with integer Δx for clean arithmetic.
        if tier == "easy":
            xs = [0, 1, 2]
            ys = [random.randint(1, 5) for _ in xs]
            table = ", ".join(rf"f({x})={y}" for x, y in zip(xs, ys))
            total = sum(ys[:-1])  # left, Δx=1
            prompt = (
                rf"{table}.\quad\text{{Approximate }}\int_{{{xs[0]}}}^{{{xs[-1]}}} f(x)\,dx"
                rf"\text{{ with a left Riemann sum.}}"
            )
        elif tier == "medium":
            xs = [0, 1, 2, 3]
            ys = [random.randint(1, 6) for _ in xs]
            table = ", ".join(rf"f({x})={y}" for x, y in zip(xs, ys))
            if random.choice([True, False]):
                total = sum(ys[:-1])
                kind = "left"
            else:
                total = sum(ys[1:])
                kind = "right"
            prompt = (
                rf"{table}.\quad\text{{Approximate }}\int_{{{xs[0]}}}^{{{xs[-1]}}} f(x)\,dx"
                rf"\text{{ with a {kind} Riemann sum.}}"
            )
        else:
            mid_vals = [random.randint(1, 6), random.randint(1, 6)]
            prompt = (
                rf"\text{{On }}[0,4]\text{{ with }}\Delta x=2,\text{{ the midpoint values are }}"
                rf"f(1)={mid_vals[0]}\text{{ and }}f(3)={mid_vals[1]}."
                rf"\quad\text{{Find the midpoint Riemann sum.}}"
            )
            total = sum(mid_vals) * 2
        answer = str(total)
        return prompt, "Riemann sum from table", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _second_fundamental_theorem(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(0, 3)
        if tier == "easy":
            prompt = rf"\frac{{d}}{{d{x}}}\int_{{{a}}}^{{{x}}} t^{{2}}\,dt"
            answer = rf"{x}^{{2}}"
        elif tier == "medium":
            prompt = rf"\frac{{d}}{{d{x}}}\int_{{{a}}}^{{{x}}} \sin(t)\,dt"
            answer = rf"\sin({x})"
        else:
            # chain: d/dx ∫_a^{g(x)} f = f(g(x)) g'(x)
            k = random.randint(2, 4)
            prompt = rf"\frac{{d}}{{d{x}}}\int_{{{a}}}^{{{k}{x}}} e^{{t}}\,dt"
            answer = rf"{k}e^{{{k}{x}}}"
        return prompt, "second fundamental theorem", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _def_int_mean_value(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)
    x = str(settings.get("variable", "x"))

    def build() -> tuple[str, str, str | None]:
        b = random.randint(2, 5) if tier != "hard" else random.randint(3, 6)
        if tier == "easy":
            f = x
            avg = Fraction(b, 2)
        elif tier == "medium":
            f = rf"{x}^{{2}}"
            avg = Fraction(b**2, 3)
        else:
            k = random.randint(2, 4)
            f = format_monomial_latex(k, variable=x, degree=2) or f"{k}{x}^{{2}}"
            avg = Fraction(k * b**2, 3)
        prompt = (
            rf"\text{{Find the average value of }}f({x})={f}"
            rf"\text{{ on }}[0,{b}]."
        )
        answer = frac_latex(avg)
        return prompt, "average value (integral MVT)", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _slope_field_interpret(topic: str, settings: dict) -> list[Question]:
    """Interpret slope fields by evaluating dy/dx at a point (no sketch UI)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)

    def build() -> tuple[str, str, str | None]:
        px = random.randint(-3, 3)
        py = random.randint(-3, 3)
        if tier == "easy":
            prompt = rf"\text{{For }}y'=x,\text{{ what is the slope at }}({px},{py})?"
            answer = str(px)
        elif tier == "medium":
            prompt = rf"\text{{For }}y'=x+y,\text{{ what is the slope at }}({px},{py})?"
            answer = str(px + py)
        else:
            prompt = rf"\text{{For }}y'=xy,\text{{ what is the slope at }}({px},{py})?"
            answer = str(px * py)
        return prompt, "slope field interpret", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _separable_diff_eq(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    tier = _difficulty_tier(settings)

    def build() -> tuple[str, str, str | None]:
        if tier == "easy":
            prompt = r"\text{Solve }\frac{dy}{dx}=2x,\ y(0)=3."
            answer = r"y=x^2+3"
        elif tier == "medium":
            k = random.randint(2, 4)
            c0 = random.randint(1, 5)
            prompt = rf"\text{{Solve }}\frac{{dy}}{{dx}}={k}y,\ y(0)={c0}."
            answer = rf"y={c0}e^{{{k}x}}"
        else:
            prompt = r"\text{Solve }\frac{dy}{dx}=\frac{y}{x}\text{ for }x>0,\ y(1)=4."
            answer = r"y=4x"
        return prompt, "separable DE", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _calculus_foundations(topic: str, settings: dict) -> list[Question]:
    """Fallback for remaining thin calc topics not yet given dedicated generators."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)
    tier = _difficulty_tier(settings)

    def build() -> tuple[str, str, str | None]:
        n, a = random.randint(2, 5), random.randint(1, 4)
        x = params.variable
        if "instantaneous" in topic:
            prompt, answer = (
                rf"\text{{Find the instantaneous rate of change of }}f({x})={x}^{{{n}}}"
                rf"\text{{ at }}{x}={a}.",
                str(n * a ** (n - 1)),
            )
        elif "inverse_functions" in topic:
            fp = n * a ** (n - 1)
            prompt, answer = (
                rf"f({x})={x}^{{{n}}};\quad f'({a})={fp}."
                rf"\quad\text{{Find }}(f^{{-1}})'({a**n}).",
                frac_latex(Fraction(1, fp)),
            )
        elif "slope_tangent" in topic:
            y = a * a
            if tier == "hard":
                prompt, answer = (
                    rf"\text{{Find the normal line to }}y={x}^{{2}}\text{{ at }}{x}={a}.",
                    rf"y-{y}=-\frac{{1}}{{{2 * a}}}({x}-{a})",
                )
            else:
                prompt, answer = (
                    rf"\text{{Find the tangent line to }}y={x}^{{2}}\text{{ at }}{x}={a}.",
                    rf"y-{y}={2 * a}({x}-{a})",
                )
        elif "concavity" in topic:
            power = n if n % 2 else n + 1
            prompt, answer = (
                rf"\text{{Determine the concavity of }}f({x})={x}^{{{power}}}"
                rf"\text{{ on }}(0,\infty).",
                r"\text{concave up}",
            )
        elif "relative_extrema" in topic or "absolute_extrema" in topic:
            prompt, answer = (
                rf"\text{{Find the minimum of }}f({x})=({x}-{a})^{{2}}-{n}.",
                rf"\text{{minimum }}-{n}\text{{ at }}{x}={a}",
            )
        elif "optimization" in topic:
            prompt, answer = (
                rf"\text{{A rectangle has perimeter }}{4 * n}."
                rf"\text{{ What dimensions maximize area?}}",
                f"{n} by {n}",
            )
        elif "motion_along" in topic:
            prompt, answer = (rf"s(t)=t^{{2}}-{n}t.\quad\text{{Find }}v({n}).", str(n))
        elif "differentials" in topic:
            if tier == "hard":
                # Product-style differential of a power times constant
                c = random.randint(2, 5)
                prompt, answer = (
                    rf"\text{{For }}y={c}{x}^{{{n}}},\text{{ find }}dy.",
                    rf"dy={c * n}{x}^{{{n - 1}}}d{x}",
                )
            else:
                prompt, answer = (
                    rf"\text{{For }}y={x}^{{{n}}},\text{{ find }}dy.",
                    rf"dy={n}{x}^{{{n - 1}}}d{x}",
                )
        elif "newtons" in topic:
            # One Newton step: x1 = x0 - f(x0)/f'(x0) with integer-friendly choices.
            if tier == "hard":
                a = random.choice([2, 3, 5, 7, 10])
                x0 = random.choice([1, 2])
                # Avoid exact roots (x0^3 == a)
                if x0**3 == a:
                    x0 = 1 if a != 1 else 2
                fx = x0**3 - a
                fpx = 3 * x0 * x0
                prompt = (
                    rf"\text{{Use one Newton step for }}f(x)=x^3-{a}"
                    rf"\text{{ from }}x_0={x0}."
                )
                answer = rf"x_1={frac_latex(Fraction(x0) - Fraction(fx, fpx))}"
            elif tier == "medium":
                a = random.choice([2, 3, 5, 7, 10])
                x0 = random.choice([1, 2, 3])
                if x0 * x0 == a:
                    x0 = x0 + 1 if x0 < 3 else x0 - 1
                fx = x0 * x0 - a
                fpx = 2 * x0
                prompt = (
                    rf"\text{{Use one Newton step for }}f(x)=x^2-{a}"
                    rf"\text{{ from }}x_0={x0}."
                )
                answer = rf"x_1={frac_latex(Fraction(x0) - Fraction(fx, fpx))}"
            else:
                a = random.choice([2, 3, 5])
                x0 = 1
                fx = x0 * x0 - a
                fpx = 2 * x0
                prompt = (
                    rf"\text{{Use one Newton step for }}f(x)=x^2-{a}"
                    rf"\text{{ from }}x_0={x0}."
                )
                answer = rf"x_1={frac_latex(Fraction(x0) - Fraction(fx, fpx))}"
        elif "definition_of_derivative" in topic or "limits_in_form" in topic:
            prompt, answer = (
                rf"\lim_{{h\to0}}\frac{{({a}+h)^{{2}}-{a * a}}}{{h}}",
                str(2 * a),
            )
        elif "trigonometric_with" in topic and "inverse" not in topic:
            prompt, answer = (
                rf"\int \cos({n}{x})\,d{x}",
                rf"\frac{{1}}{{{n}}}\sin({n}{x})+C",
            )
        elif "logarithmic" in topic and "substitution" in topic:
            prompt, answer = (
                rf"\int \frac{{{n}}}{{{n}{x}+1}}\,d{x}",
                rf"\ln|{n}{x}+1|+C",
            )
        elif "substitution_with_change" in topic:
            prompt, answer = (rf"\int_0^1 {2 * n}{x}^{{{2 * n - 1}}}\,d{x}", "1")
        elif "limit_of_sums" in topic:
            prompt, answer = (
                rf"\int_0^{{{n}}} {x}\,d{x}",
                frac_latex(Fraction(n * n, 2)),
            )
        elif "diff_eq_introduction" in topic:
            k = random.randint(2, 4) if tier != "hard" else random.randint(2, 5)
            if tier == "hard":
                prompt, answer = (
                    rf"\text{{Verify that }}y=Cx^{{{k}}}\text{{ solves }}"
                    rf"x\,y'={k}y\text{{ for }}x>0.",
                    rf"y'={k}Cx^{{{k - 1}}}\Rightarrow x y'={k}y",
                )
            else:
                prompt, answer = (
                    rf"\text{{Verify that }}y=Ce^{{{k}x}}\text{{ solves }}y'={k}y.",
                    rf"y'={k}Ce^{{{k}x}}={k}y",
                )
        else:
            prompt, answer = (rf"\frac{{d}}{{d{x}}}({x}^{{{n}}})", f"{n}{x}^{{{n - 1}}}")
        return prompt, topic, answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "limit_direct_evaluation": _limit_direct_evaluation,
    "limit_at_infinity": _limit_at_infinity,
    "derivative_power_rule": _derivative_power_rule,
    "integral_power_rule": _integral_power_rule,
    "derivative_product_rule": _derivative_product_rule,
    "derivative_quotient_rule": _derivative_quotient_rule,
    "derivative_chain_rule": _derivative_chain_rule,
    "derivative_trigonometric": _derivative_trigonometric,
    "derivative_inverse_trig": _derivative_inverse_trig,
    "derivative_other_base": _derivative_other_base,
    "derivative_from_tables": _derivative_from_tables,
    "derivative_implicit": _derivative_implicit,
    "derivative_higher_order": _derivative_higher_order,
    "average_rate_of_change": _average_rate_of_change,
    "definition_of_derivative": _definition_of_derivative,
    "rolles_theorem": _rolles_theorem,
    "mean_value_theorem": _mean_value_theorem,
    "integral_trigonometric": _integral_trigonometric,
    "integral_substitution": _integral_substitution,
    "integral_log_exp": _integral_log_exp,
    "integral_inverse_trig": _integral_inverse_trig,
    "integration_by_parts": _integration_by_parts,
    "riemann_approximate_area": _riemann_approximate_area,
    "riemann_sum_tables": _riemann_sum_tables,
    "first_fundamental_theorem": _first_fundamental_theorem,
    "second_fundamental_theorem": _second_fundamental_theorem,
    "def_int_mean_value": _def_int_mean_value,
    "area_under_curve": _area_under_curve,
    "volume_disk_washer": _volume_disk_washer,
    "volume_shell": _volume_shell,
    "volume_cross_sections": _volume_cross_sections,
    "slope_field_interpret": _slope_field_interpret,
    "separable_diff_eq": _separable_diff_eq,
    "calculus_foundations": _calculus_foundations,
}
