import math
import random
import uuid
from fractions import Fraction
from typing import Callable

from packages.polynomial_core import (
    Polynomial,
    create_factorable_polynomial,
    create_special_product_problem,
    format_linear_latex,
    format_polynomial_latex,
    format_slope_intercept_latex,
    fraction_latex,
    square_root_latex,
)

from ..settings.common_settings import standard_question_settings
from ..settings.factoring_settings import build_factorable_options
from ..settings.enrichment import merge_enrichment_metadata
from ..settings.params import allowed_rational_operations, polynomial_params_from_settings, radical_params_from_settings
from ..core.metadata import scaffold_metadata
from ..core.models import Question, SettingField
from .utils import (
    _frac_latex,
    _make_questions,
    _random_fraction,
    pick_quadratic_leading_coef,
    settings_require_monic,
)


def _discrete_relations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x = random.randint(-5, 5)
        m = random.randint(-4, 4)
        b = random.randint(-6, 6)
        y = m * x + b
        prompt = (
            f"\\text{{If }} {format_slope_intercept_latex(m, b)}, "
            f"\\text{{ find }} y \\text{{ when }} x = {x}."
        )
        answer = str(y) if include_answer_key else None
        return prompt, f"y when x={x}", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _continuous_relations(topic: str, settings: dict) -> list[Question]:
    return _discrete_relations(topic, settings)


def _evaluating_graphing_functions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x = random.randint(-4, 4)
        a = random.randint(-3, 3)
        b = random.randint(-6, 6)
        value = a * x * x + b
        fn = f"f(x) = {format_polynomial_latex([a, 0, b])}" if a != 0 else f"f(x) = {b}"
        prompt = f"\\text{{Given }} {fn}, \\text{{ find }} f({x})."
        answer = str(value) if include_answer_key else None
        return prompt, f"f({x})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _writing_linear_equations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        m = random.randint(-5, 5)
        while m == 0:
            m = random.randint(-5, 5)
        b = random.randint(-8, 8)
        x1, y1 = random.randint(-4, 4), random.randint(-8, 8)
        prompt = (
            f"\\text{{Write the equation of the line with slope {m} "
            f"through }} ({x1}, {y1})."
        )
        answer = format_slope_intercept_latex(m, b) if include_answer_key else None
        return prompt, "Write linear equation", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _direct_inverse_variation(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        k = random.randint(2, 12)
        if random.choice([True, False]):
            prompt = f"\\text{{Write a direct variation equation with }} k = {k}."
            answer = format_slope_intercept_latex(k, 0) if include_answer_key else None
        else:
            prompt = f"\\text{{Write an inverse variation equation with }} k = {k}."
            answer = f"y = \\frac{{{k}}}{{x}}" if include_answer_key else None
        return prompt, "Variation equation", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _systems(topic: str, settings: dict, method: str) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x = random.randint(-5, 5)
        y = random.randint(-5, 5)
        a1, b1 = random.randint(1, 4), random.randint(1, 4)
        a2, b2 = random.randint(1, 4), random.randint(-4, -1)
        c1 = a1 * x + b1 * y
        c2 = a2 * x + b2 * y
        prompt = f"\\begin{{cases}} {a1}x + {b1}y = {c1} \\\\ {a2}x + {b2}y = {c2} \\end{{cases}}"
        answer = f"(x, y) = ({x}, {y})" if include_answer_key else None
        return prompt, f"system ({method})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _exponential_growth_decay(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 5))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        prompt, kind, answer_value = _build_exponential_growth_decay(settings)
        answer = answer_value if include_answer_key else None
        return prompt, kind, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


_NICE_RATES = (5, 10)
_MESSY_RATES = (3, 4, 6, 7, 8, 9, 12, 15, 16, 18, 20, 25)
_GROWTH_CONTEXTS = (
    ("population of {a0}", "people", "year"),
    ("account with \\${a0}", "dollars", "year"),
    ("bacterial culture of {a0}", "cells", "hour"),
    ("investment of \\${a0}", "dollars", "year"),
)
_DECAY_CONTEXTS = (
    ("population of {a0}", "people", "year"),
    ("sample of {a0} grams", "grams", "year"),
    ("medicine dose of {a0} mg", "mg", "hour"),
    ("car valued at \\${a0}", "dollars", "year"),
)


def _egd_int_setting(settings: dict, key: str, *aliases: str, default: int) -> int:
    for candidate in (key, *aliases):
        if candidate in settings and settings[candidate] is not None:
            return int(settings[candidate])
    return default


def _egd_bool(settings: dict, key: str, default: bool = False) -> bool:
    if key not in settings or settings[key] is None:
        return default
    return bool(settings[key])


def _egd_rate_choices(settings: dict, *, nice: bool) -> list[int]:
    lo = _egd_int_setting(settings, "rate_min", "growth_rate_min", default=5)
    hi = _egd_int_setting(settings, "rate_max", "growth_rate_max", default=20)
    if lo > hi:
        lo, hi = hi, lo
    pool = _NICE_RATES if nice else _NICE_RATES + _MESSY_RATES
    choices = [r for r in pool if lo <= r <= hi]
    if not choices:
        choices = list(range(lo, hi + 1)) or [lo]
    return choices


def _egd_periods(settings: dict) -> float:
    lo = _egd_int_setting(settings, "periods_min", "years_min", default=2)
    hi = _egd_int_setting(settings, "periods_max", "years_max", default=6)
    if lo > hi:
        lo, hi = hi, lo
    if _egd_bool(settings, "allow_fractional_periods") and random.random() < 0.35:
        whole = random.randint(lo, max(lo, hi - 1)) if hi > lo else lo
        return whole + 0.5
    return float(random.randint(lo, hi))


def _egd_initial(settings: dict) -> int:
    # Prefer round starting amounts that stay readable after compounding.
    return random.choice([50, 80, 100, 120, 150, 200, 250, 300, 400, 500, 800, 1000, 1200, 1500, 2000])


def _egd_growth_flag(settings: dict) -> bool:
    allow_growth = _egd_bool(settings, "allow_growth", True)
    allow_decay = _egd_bool(settings, "allow_decay", True)
    if allow_growth and allow_decay:
        return random.choice([True, False])
    if allow_growth:
        return True
    if allow_decay:
        return False
    return True


def _egd_factor(rate_pct: int, growth: bool) -> float:
    return (100 + rate_pct) / 100 if growth else (100 - rate_pct) / 100


def _egd_format_amount(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}"


def _egd_format_periods(n: float) -> str:
    if abs(n - round(n)) < 1e-9:
        return str(int(round(n)))
    return f"{n:g}"


def _egd_article(subject: str) -> str:
    first = subject.lstrip().lower()[:1]
    return "An" if first in "aeiou" else "A"


def _egd_context(growth: bool, a0: int) -> tuple[str, str, str]:
    template, unit, period_name = random.choice(_GROWTH_CONTEXTS if growth else _DECAY_CONTEXTS)
    subject = template.format(a0=a0)
    return subject, unit, period_name


def _egd_resolve_ask_mode(settings: dict) -> str:
    mode = str(settings.get("ask_mode", "find_final")).strip().lower()
    core = ["find_final", "find_rate", "find_periods", "find_initial"]
    extras: list[str] = []
    if _egd_bool(settings, "allow_how_much_more"):
        extras.append("how_much_more")
    if _egd_bool(settings, "allow_compare"):
        extras.append("compare")
    if _egd_bool(settings, "allow_threshold"):
        extras.append("threshold")
    if _egd_bool(settings, "allow_half_life"):
        extras.append("half_life")

    if mode == "mixed":
        pool = [m for m in core if m != "find_final"] or list(core)
        # Prefer structurally harder modes when extras are enabled.
        if extras:
            # Weight multi-step hard modes more heavily.
            hard_extras = [m for m in extras if m in {"compare", "threshold", "half_life"}]
            if hard_extras:
                pool = hard_extras * 2 + extras + pool
            else:
                pool = extras + pool
        return random.choice(pool)
    if mode in core:
        return mode
    return "find_final"


def _egd_final_value(a0: float, factor: float, n: float) -> float:
    return round(a0 * (factor**n), 2)


def _build_find_final(settings: dict, *, how_much_more: bool = False) -> tuple[str, str, str]:
    growth = _egd_growth_flag(settings)
    nice = not (
        _egd_bool(settings, "allow_compare")
        or _egd_bool(settings, "allow_threshold")
        or _egd_bool(settings, "allow_half_life")
    )
    rate = random.choice(_egd_rate_choices(settings, nice=nice))
    n = _egd_periods(settings)
    a0 = _egd_initial(settings)
    factor = _egd_factor(rate, growth)
    final = _egd_final_value(a0, factor, n)
    subject, unit, period_name = _egd_context(growth, a0)
    kind = "growth" if growth else "decay"
    n_txt = _egd_format_periods(n)
    article = _egd_article(subject)
    if how_much_more:
        change = abs(final - a0)
        direction = "more" if growth else "less"
        prompt = (
            f"\\text{{{article} {subject} changes by {rate}\\% {kind} each {period_name}. "
            f"How much {direction} (in {unit}) is it after {n_txt} {period_name}s?}}"
        )
        return prompt, f"exponential {kind} difference", _egd_format_amount(change)

    prompt = (
        f"\\text{{{article} {subject} changes by {rate}\\% {kind} each {period_name}. "
        f"Find the amount after {n_txt} {period_name}s.}}"
    )
    return prompt, f"exponential {kind}", _egd_format_amount(final)


def _build_find_rate(settings: dict) -> tuple[str, str, str]:
    growth = _egd_growth_flag(settings)
    rate = random.choice(_egd_rate_choices(settings, nice=False))
    n = _egd_periods(settings)
    # Integer periods keep rate recovery clean for students.
    if not abs(n - round(n)) < 1e-9:
        n = float(int(n) if n >= 1 else 2)
    a0 = _egd_initial(settings)
    factor = _egd_factor(rate, growth)
    final = _egd_final_value(a0, factor, n)
    subject, unit, period_name = _egd_context(growth, a0)
    kind = "growth" if growth else "decay"
    article = _egd_article(subject)
    prompt = (
        f"\\text{{{article} {subject} becomes {_egd_format_amount(final)} {unit} after "
        f"{_egd_format_periods(n)} {period_name}s of discrete {kind}. "
        f"Find the percent {kind} rate per {period_name}.}}"
    )
    return prompt, f"exponential find rate", str(rate)


def _build_find_periods(settings: dict) -> tuple[str, str, str]:
    growth = _egd_growth_flag(settings)
    rate = random.choice(_egd_rate_choices(settings, nice=True))
    lo = _egd_int_setting(settings, "periods_min", "years_min", default=2)
    hi = _egd_int_setting(settings, "periods_max", "years_max", default=6)
    if lo > hi:
        lo, hi = hi, lo
    n = random.randint(lo, hi)
    a0 = _egd_initial(settings)
    factor = _egd_factor(rate, growth)
    final = _egd_final_value(a0, factor, float(n))
    subject, unit, period_name = _egd_context(growth, a0)
    kind = "growth" if growth else "decay"
    article = _egd_article(subject)
    prompt = (
        f"\\text{{{article} {subject} changes by {rate}\\% {kind} each {period_name}. "
        f"After how many {period_name}s is it {_egd_format_amount(final)} {unit}?}}"
    )
    return prompt, f"exponential find periods", str(n)


def _build_find_initial(settings: dict) -> tuple[str, str, str]:
    growth = _egd_growth_flag(settings)
    rate = random.choice(_egd_rate_choices(settings, nice=True))
    n = _egd_periods(settings)
    a0 = _egd_initial(settings)
    factor = _egd_factor(rate, growth)
    final = _egd_final_value(a0, factor, n)
    _, unit, period_name = _egd_context(growth, a0)
    kind = "growth" if growth else "decay"
    prompt = (
        f"\\text{{An amount changes by {rate}\\% {kind} each {period_name}. "
        f"After {_egd_format_periods(n)} {period_name}s it is {_egd_format_amount(final)} {unit}. "
        f"Find the initial amount.}}"
    )
    return prompt, f"exponential find initial", _egd_format_amount(float(a0))


def _build_compare(settings: dict) -> tuple[str, str, str]:
    rate_a = random.choice(_egd_rate_choices(settings, nice=False))
    rate_b = random.choice([r for r in _egd_rate_choices(settings, nice=False) if r != rate_a] or [rate_a + 1])
    n = int(_egd_periods(settings))
    a0 = random.choice([500, 800, 1000, 1200, 1500, 2000])
    final_a = _egd_final_value(a0, _egd_factor(rate_a, True), float(n))
    final_b = _egd_final_value(a0, _egd_factor(rate_b, True), float(n))
    diff = abs(final_a - final_b)
    better = "A" if final_a >= final_b else "B"
    prompt = (
        f"\\text{{Investment A: \\${a0} at {rate_a}\\% growth per year for {n} years. "
        f"Investment B: \\${a0} at {rate_b}\\% growth per year for {n} years. "
        f"Which ends larger, and by how much?}}"
    )
    answer = f"{better}, {_egd_format_amount(diff)}"
    return prompt, "exponential compare", answer


def _build_threshold(settings: dict) -> tuple[str, str, str]:
    growth = True
    rate = random.choice(_egd_rate_choices(settings, nice=True))
    lo = _egd_int_setting(settings, "periods_min", "years_min", default=2)
    hi = _egd_int_setting(settings, "periods_max", "years_max", default=6)
    if lo > hi:
        lo, hi = hi, lo
    n = random.randint(max(2, lo), hi)
    a0 = _egd_initial(settings)
    factor = _egd_factor(rate, growth)
    final = _egd_final_value(a0, factor, float(n))
    # Threshold just below the amount at n periods so the first exceed year is n.
    threshold = round(final * 0.92, 2)
    if threshold <= a0:
        threshold = round((a0 + final) / 2, 2)
    subject, unit, period_name = _egd_context(growth, a0)
    # Walk forward to confirm the first exceed period.
    amount = float(a0)
    exceed_n = n
    for t in range(1, hi + 5):
        amount = round(amount * factor, 2)
        if amount > threshold:
            exceed_n = t
            break
    article = _egd_article(subject)
    prompt = (
        f"\\text{{{article} {subject} grows by {rate}\\% each {period_name}. "
        f"After how many {period_name}s does it first exceed {_egd_format_amount(threshold)} {unit}?}}"
    )
    return prompt, "exponential threshold", str(exceed_n)


def _build_half_life(settings: dict) -> tuple[str, str, str]:
    half_life = random.choice([2, 3, 4])
    cycles = random.randint(2, 4)
    a0 = random.choice([160, 200, 256, 320, 400, 512, 640, 800])
    final = a0 / (2**cycles)
    total_periods = half_life * cycles
    prompt = (
        f"\\text{{A sample of {a0} grams decays by half every {half_life} years "
        f"(discrete half-life). How much remains after {total_periods} years?}}"
    )
    return prompt, "exponential half-life", _egd_format_amount(float(final))


def _build_exponential_growth_decay(settings: dict) -> tuple[str, str, str]:
    # discrete_only is the discrete compound model A0*(1±r)^n (always used here).
    _ = _egd_bool(settings, "discrete_only", True)
    mode = _egd_resolve_ask_mode(settings)
    if mode == "how_much_more":
        return _build_find_final(settings, how_much_more=True)
    if mode == "find_rate":
        return _build_find_rate(settings)
    if mode == "find_periods":
        return _build_find_periods(settings)
    if mode == "find_initial":
        return _build_find_initial(settings)
    if mode == "compare":
        return _build_compare(settings)
    if mode == "threshold":
        return _build_threshold(settings)
    if mode == "half_life":
        return _build_half_life(settings)
    return _build_find_final(settings)


def _polynomial_add_subtract(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    ops = allowed_rational_operations(settings)

    def build() -> tuple[str, str, str | None]:
        degree = random.randint(params.min_degree, params.max_degree)
        p = Polynomial.random_polynomial(
            degree, params.coef_min, params.coef_max, positive_leading=params.positive_leading
        )
        q = Polynomial.random_polynomial(
            degree, params.coef_min, params.coef_max, positive_leading=params.positive_leading
        )
        op = random.choice(ops)
        result = p + q if op == "+" else p - q
        prompt = f"({p.to_latex()}) {op} ({q.to_latex()})"
        answer = result.to_latex() if include_answer_key else None
        return prompt, f"({p}) {op} ({q})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _random_sparse_factor(
    n_terms: int,
    *,
    min_degree: int,
    max_degree: int,
    coef_min: int,
    coef_max: int,
    leading_one: bool,
    positive_leading: bool,
    variable: str = "x",
) -> Polynomial:
    """Build a factor with exactly ``n_terms`` nonzero terms."""
    n_terms = max(1, int(n_terms))
    deg_lo = max(min_degree, n_terms - 1)
    deg_hi = max(max_degree, deg_lo)
    degree = random.randint(deg_lo, deg_hi)

    if n_terms == 1:
        exponents = [degree]
    else:
        lower = list(range(0, degree))
        # Prefer including a constant term for classic binomials/trinomials.
        chosen: list[int] = []
        if 0 in lower and n_terms >= 2 and random.random() < 0.75:
            chosen.append(0)
            lower.remove(0)
        needed = n_terms - 1 - len(chosen)
        if needed > 0:
            if len(lower) < needed:
                # Expand degree so we have enough distinct lower exponents.
                degree = max(degree, n_terms - 1)
                lower = [e for e in range(0, degree) if e not in chosen]
            chosen.extend(random.sample(lower, needed))
        exponents = [degree, *chosen]

    terms: list[tuple[int, int]] = []
    for index, exp in enumerate(exponents):
        if index == 0:
            if leading_one:
                coef = 1
            else:
                coef = Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)
                # Medium/hard: force leading coefficient away from ±1.
                attempts = 0
                while abs(coef) == 1 and attempts < 20:
                    coef = Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)
                    attempts += 1
                if abs(coef) == 1:
                    coef = 2 if coef_max >= 2 else (coef_min if coef_min <= -2 else 2)
                if positive_leading and coef < 0:
                    coef = abs(coef)
        else:
            coef = Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)
        terms.append((coef, exp))
    return Polynomial(tuple(terms), variable=variable)


def _choose_multiply_factor_term_counts(settings: dict) -> tuple[int, int]:
    """Pick (left_terms, right_terms) from multiply difficulty toggles."""
    max_terms = max(1, int(settings.get("max_factor_terms", 2)))
    allow_mb = bool(settings.get("allow_monomial_binomial", True))
    allow_bb = bool(settings.get("allow_binomial_binomial", True))
    allow_tri = bool(settings.get("allow_trinomial", False))

    if max_terms >= 4:
        # Hard: any length on either factor; bias toward longer products.
        left = random.randint(1, max_terms)
        right = random.randint(1, max_terms)
        if left < 3 and right < 3 and random.random() < 0.75:
            longer = random.randint(3, max_terms)
            if random.random() < 0.5:
                left = longer
            else:
                right = longer
        return left, right

    basic: list[tuple[int, int]] = []
    if allow_mb and max_terms >= 2:
        basic.append((1, 2))
        basic.append((2, 1))
    if allow_bb and max_terms >= 2:
        basic.append((2, 2))
    if not basic:
        basic = [(1, 2), (2, 2)]

    if allow_tri and max_terms >= 3 and random.random() < 0.35:
        tri_options = [
            (1, 3),
            (3, 1),
            (2, 3),
            (3, 2),
            (3, 3),
        ]
        return random.choice(tri_options)

    return random.choice(basic)


def _polynomial_multiply(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    leading_one = bool(settings.get("leading_coefficient_one", False))

    def build() -> tuple[str, str, str | None]:
        left_terms, right_terms = _choose_multiply_factor_term_counts(settings)
        p = _random_sparse_factor(
            left_terms,
            min_degree=params.min_degree,
            max_degree=params.max_degree,
            coef_min=params.coef_min,
            coef_max=params.coef_max,
            leading_one=leading_one,
            positive_leading=params.positive_leading,
            variable=params.variable,
        )
        q = _random_sparse_factor(
            right_terms,
            min_degree=params.min_degree,
            max_degree=params.max_degree,
            coef_min=params.coef_min,
            coef_max=params.coef_max,
            leading_one=leading_one,
            positive_leading=params.positive_leading,
            variable=params.variable,
        )
        result = p * q
        prompt = f"({p.to_latex()})({q.to_latex()})"
        answer = result.to_latex() if include_answer_key else None
        return prompt, f"({p})({q})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _polynomial_multiply_special(topic: str, settings: dict) -> list[Question]:
    """Expand special products: squares and sum/difference patterns.

    easy   — monic (x±n)² / (x+a)(x−a)
    medium — monic mixed (x+a)(x±b) and squares
    hard   — non-monic (ax±b)² / (ax+b)(ax−b)
    """
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    monic = settings_require_monic(settings)
    coef_max = max(2, abs(int(settings.get("coef_max", 9))) or 9)
    bound = min(9, coef_max) if monic else min(8, max(3, coef_max // 2))

    def build() -> tuple[str, str, str | None]:
        if monic:
            a = random.randint(1, bound)
            pattern = random.choice(["square", "diff_squares", "sum_diff"])
            if pattern == "square":
                sign = random.choice(["+", "-"])
                inner = f"x {sign} {a}"
                prompt = f"({inner})^2"
                mid = 2 * a if sign == "+" else -2 * a
                answer = (
                    format_polynomial_latex([1, mid, a * a]) if include_answer_key else None
                )
            elif pattern == "diff_squares":
                prompt = f"(x + {a})(x - {a})"
                answer = format_polynomial_latex([1, 0, -(a * a)]) if include_answer_key else None
            else:
                b = random.randint(1, bound)
                while b == a:
                    b = random.randint(1, bound)
                op = random.choice(["+", "-"])
                prompt = f"(x + {a})(x {op} {b})"
                if op == "+":
                    answer = (
                        format_polynomial_latex([1, a + b, a * b]) if include_answer_key else None
                    )
                else:
                    answer = (
                        format_polynomial_latex([1, a - b, -a * b]) if include_answer_key else None
                    )
            return prompt, prompt, answer

        # Hard: non-monic special products
        lead = random.randint(2, max(2, bound))
        a = random.randint(1, bound)
        if random.random() < 0.5:
            sign = random.choice(["+", "-"])
            inner = f"{lead}x {sign} {a}"
            prompt = f"({inner})^2"
            mid = 2 * lead * a if sign == "+" else -2 * lead * a
            answer = (
                format_polynomial_latex([lead * lead, mid, a * a])
                if include_answer_key
                else None
            )
        else:
            prompt = f"({lead}x + {a})({lead}x - {a})"
            answer = (
                format_polynomial_latex([lead * lead, 0, -(a * a)])
                if include_answer_key
                else None
            )
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _primitive_random_polynomial(
    degree: int,
    coef_min: int,
    coef_max: int,
    *,
    positive_leading: bool = True,
    leading_one: bool = False,
) -> Polynomial:
    """Random polynomial with content 1 (no numeric GCF)."""
    for _ in range(40):
        if leading_one:
            lead = 1
            lower = [
                Polynomial.randomCoefficient(coef_min, coef_max, nonZero=False)
                for _ in range(degree)
            ]
            # Ensure at least one nonzero lower term so degree is honest after GCF.
            if all(c == 0 for c in lower):
                lower[-1] = Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)
            coeffs = [lead, *lower]
            poly = Polynomial(coeffs)
        else:
            poly = Polynomial.random_polynomial(
                degree, coef_min, coef_max, positive_leading=positive_leading
            )
        content = abs(int(poly.content_gcd() or 1))
        if content <= 1:
            return poly
        scaled = [int(c) // content for c in poly.coef_list()]
        return Polynomial(scaled)
    return Polynomial([1, 1, 1][: degree + 1] if degree >= 1 else [1])


def _format_gcf_prefix(g: int, var_power: int, variable: str = "x") -> str:
    if var_power <= 0:
        return str(g) if g != 1 else ""
    if var_power == 1:
        body = variable
    else:
        body = f"{variable}^{{{var_power}}}"
    if g == 1:
        return body
    if g == -1:
        return f"-{body}"
    return f"{g}{body}"


def _polynomial_factoring_common_factor_only(topic: str, settings: dict) -> list[Question]:
    """Factor out a monomial GCF only — leave the remaining polynomial unfactored."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    monic = settings_require_monic(settings)
    coef_hi = max(2, abs(int(params.coef_max)) or 5)

    def build() -> tuple[str, str, str | None]:
        remaining_degree = random.randint(max(1, params.min_degree), max(1, params.max_degree))
        remaining = _primitive_random_polynomial(
            remaining_degree,
            params.coef_min,
            params.coef_max,
            positive_leading=params.positive_leading,
            leading_one=monic,
        )
        g_choices = [v for v in range(2, min(coef_hi, 9) + 1)]
        g = random.choice(g_choices or [2, 3, 4])
        # Easy: numeric GCF only; medium/hard may include x^k.
        if monic:
            var_power = 0
        elif random.random() < 0.55:
            var_power = random.randint(1, 2 if remaining_degree >= 2 else 1)
        else:
            var_power = 0
        gcf = Polynomial(((g, var_power),))
        poly = remaining * gcf
        prefix = _format_gcf_prefix(g, var_power, params.variable)
        answer = f"{prefix}({remaining.to_latex()})" if include_answer_key else None
        return poly.to_latex(), str(poly), answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _polynomial_factoring(topic: str, settings: dict, method_overrides: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    merged = {**settings, **method_overrides}
    params = polynomial_params_from_settings(merged)

    questions: list[Question] = []
    for _ in range(count):
        options = build_factorable_options(merged, params.min_degree, params.max_degree)
        result = create_factorable_polynomial(options)
        poly = result.polynomial
        factors = "".join(f"({factor.to_latex()})" for factor in result.factors)
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=poly.to_latex(),
                prompt_text=str(poly),
                answer_latex=factors if include_answer_key else None,
                metadata=merge_enrichment_metadata(
                    settings,
                    {"factoring_method": result.method},
                    answer=factors if include_answer_key else None,
                ),
            )
        )
    return questions


def _special_case_settings_for_topic(topic: str, settings: dict) -> dict:
    """Apply type-specific pattern defaults without clobbering explicit toggles."""
    merged = dict(settings)
    tid = topic.lower()

    def _set_default(key: str, value: bool | int) -> None:
        if key not in merged:
            merged[key] = value

    def _force(key: str, value: bool | int) -> None:
        merged[key] = value

    if "sum_difference_of_cubes" in tid or tid.endswith("factoring_sum_difference_of_cubes"):
        _force("factor_difference_of_squares", False)
        _force("factor_perfect_square_trinomial", False)
        _force("factor_difference_of_cubes", True)
        _force("factor_sum_of_cubes", True)
        _force("allow_higher_even_powers", False)
    elif "special_case_quadratic" in tid:
        _force("factor_difference_of_squares", True)
        _force("factor_perfect_square_trinomial", True)
        _force("factor_difference_of_cubes", False)
        _force("factor_sum_of_cubes", False)
        _force("allow_higher_even_powers", False)
    else:
        _set_default("factor_difference_of_squares", True)
        _set_default("factor_perfect_square_trinomial", True)
        _set_default("factor_difference_of_cubes", True)
        _set_default("factor_sum_of_cubes", True)

    return merged


def _polynomial_factoring_special_cases(topic: str, settings: dict) -> list[Question]:
    """Factor expanded special products (DOS, PST, cubes, higher even powers)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    merged = _special_case_settings_for_topic(topic, settings)

    questions: list[Question] = []
    for _ in range(count):
        result = create_special_product_problem(merged)
        poly = result.polynomial
        answer = result.answer_latex() if include_answer_key else None
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=poly.to_latex(),
                prompt_text=str(poly),
                answer_latex=answer,
                metadata=merge_enrichment_metadata(
                    settings,
                    {
                        "factoring_method": result.method,
                        "special_pattern": result.pattern,
                        "gcf": result.gcf,
                    },
                    answer=answer,
                ),
            )
        )
    return questions


def _quadratic_square_roots(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    integer_only = bool(settings.get("integer_only", True))

    form_keys = (
        ("isolated", "allow_isolated"),
        ("vertex", "allow_vertex"),
        ("complete_square", "allow_complete_square"),
    )
    enabled = [name for name, key in form_keys if bool(settings.get(key, name != "complete_square"))]
    if not enabled:
        enabled = ["isolated"]

    def _coef_bound() -> int:
        return max(2, min(6, abs(int(params.coef_max)) or 6))

    def _pick_a(*, prefer_nonunit: bool = False) -> int:
        if settings_require_monic(settings):
            return 1
        hi = _coef_bound()
        if prefer_nonunit:
            choices = [v for v in range(2, hi + 1)]
            return random.choice(choices or [2, 3])
        if random.random() < 0.55:
            return 1
        return random.randint(1, hi)

    def _pick_h(*, allow_zero: bool = True) -> int:
        hi = _coef_bound()
        lo = -hi
        for _ in range(20):
            h = random.randint(lo, hi)
            if allow_zero or h != 0:
                return h
        return random.choice([-3, -2, -1, 1, 2, 3])

    def _pick_radicand() -> int:
        """Positive value under the square root after isolating the square."""
        if integer_only:
            root = random.randint(2, max(2, _coef_bound()))
            return root * root
        if random.random() < 0.45:
            root = random.randint(2, max(2, _coef_bound()))
            return root * root
        return random.choice([2, 3, 5, 6, 7, 8, 10, 12, 13, 18, 20])

    def _radius_latex(radicand: int) -> str:
        coeff, simplified = Polynomial.simplify_square_root(radicand)
        return square_root_latex(coeff, simplified)

    def _answer(h: int, radicand: int) -> str | None:
        if not include_answer_key:
            return None
        if radicand < 0:
            return "\\text{no real solutions}"
        if radicand == 0:
            return f"x = {h}"
        radius = _radius_latex(radicand)
        if h == 0:
            return f"x = \\pm {radius}"
        return f"x = {h} \\pm {radius}"

    def _binom_square(h: int) -> str:
        if h == 0:
            return format_polynomial_latex([1, 0, 0])
        inner = format_linear_latex(1, -h)
        return f"({inner})^{{2}}"

    def _scaled_binom_square(a: int, h: int) -> str:
        body = _binom_square(h)
        if a == 1:
            return body
        if a == -1:
            return f"-{body}"
        return f"{a}{body}"

    def _signed_term(value: int) -> str:
        if value >= 0:
            return f"+ {value}"
        return f"- {abs(value)}"

    def _build_isolated() -> tuple[str, str, str | None]:
        radicand = _pick_radicand()
        # Mostly ax^2 = k; occasionally a simple already-isolated (x±h)^2 = k.
        if random.random() < 0.22:
            h = _pick_h(allow_zero=False)
            prompt = f"{_binom_square(h)} = {radicand}"
            return prompt, prompt, _answer(h, radicand)
        a = _pick_a(prefer_nonunit=False)
        rhs = a * radicand
        prompt = f"{format_polynomial_latex([a, 0, 0])} = {rhs}"
        return prompt, prompt, _answer(0, radicand)

    def _build_vertex(*, messy: bool = False) -> tuple[str, str, str | None]:
        a = _pick_a(prefer_nonunit=messy or random.random() < 0.35)
        h = _pick_h(allow_zero=False)
        radicand = _pick_radicand()
        # a(x-h)^2 = a * radicand  ⇒  (x-h)^2 = radicand
        m = a * radicand
        style = random.choice(["equals_m", "plus_k"])
        scaled = _scaled_binom_square(a, h)
        if style == "equals_m":
            prompt = f"{scaled} = {m}"
        else:
            k = -m
            prompt = f"{scaled} {_signed_term(k)} = 0"
        return prompt, prompt, _answer(h, radicand)

    def _build_complete_square() -> tuple[str, str, str | None]:
        a = _pick_a(prefer_nonunit=random.random() < 0.7)
        h = _pick_h(allow_zero=False)
        radicand = _pick_radicand()
        m = a * radicand
        # a(x-h)^2 = m  →  ax^2 - 2ah x + (a h^2 - m) = 0
        b = -2 * a * h
        c = a * h * h - m
        poly = format_polynomial_latex([a, b, c])
        if c != 0 and random.random() < 0.4:
            prompt = f"{format_polynomial_latex([a, b, 0])} = {-c}"
        else:
            prompt = f"{poly} = 0"
        return prompt, prompt, _answer(h, radicand)

    builders = {
        "isolated": _build_isolated,
        "vertex": lambda: _build_vertex(messy=False),
        "complete_square": _build_complete_square,
    }

    def build() -> tuple[str, str, str | None]:
        form = random.choice(enabled)
        if form == "vertex":
            # Hard presets unlock CTS; prefer messier a≠1 vertex when both are on.
            messy = bool(settings.get("allow_complete_square", False))
            return _build_vertex(messy=messy)
        return builders[form]()

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _format_fraction_value(value: Fraction) -> str:
    value = Fraction(value).limit_denominator()
    if value.denominator == 1:
        return str(value.numerator)
    return fraction_latex(str(value.numerator), str(value.denominator))


def _linear_factor_root_latex(factor: Polynomial) -> str | None:
    """Root of ax + b = 0 as LaTeX, or None if not degree 1."""
    if factor.deg() != 1:
        return None
    a = int(factor.coef(1))
    b = int(factor.coef(0))
    if a == 0:
        return None
    return _format_fraction_value(Fraction(-b, a))


def _quadratic_roots_from_factors(factors: tuple | list) -> list[str]:
    roots: list[str] = []
    for factor in factors:
        root = _linear_factor_root_latex(factor)
        if root is not None:
            roots.append(root)
    return roots


def _quadratic_formula_answer_latex(a: int, b: int, c: int) -> str:
    """Exact quadratic-formula answer (no float rounding), content-reduced."""
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return "\\text{no real solutions}"
    two_a = 2 * a
    if discriminant == 0:
        return f"x = {_format_fraction_value(Fraction(-b, two_a))}"

    coeff, rad = Polynomial.simplify_square_root(discriminant)
    if rad == 1:
        r1 = Fraction(-b + coeff, two_a)
        r2 = Fraction(-b - coeff, two_a)
        return f"x = {_format_fraction_value(r1)}, {_format_fraction_value(r2)}"

    # Reduce (-b ± coeff√rad) / (2a) by gcd(|b|, |coeff|, |2a|).
    g = math.gcd(math.gcd(abs(b), abs(coeff)), abs(two_a))
    if g > 1:
        b = b // g
        coeff = coeff // g
        two_a = two_a // g

    radius = square_root_latex(coeff, rad)
    if b == 0:
        num = f"\\pm {radius}"
    else:
        num = f"{-b} \\pm {radius}"
    if two_a == 1:
        return f"x = {num}"
    if two_a == -1:
        return f"x = -\\left({num}\\right)"
    return f"x = {fraction_latex(num, str(two_a))}"


def _quadratic_factoring_equations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    questions: list[Question] = []
    for _ in range(count):
        options = build_factorable_options(settings, 2, 2)
        result = create_factorable_polynomial(options)
        poly = result.polynomial
        roots = _quadratic_roots_from_factors(result.factors)
        answer = ", ".join(f"x = {root}" for root in roots) if include_answer_key else None
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=f"{poly.to_latex()} = 0",
                prompt_text=f"{poly} = 0",
                answer_latex=answer,
                metadata=merge_enrichment_metadata(settings, {"factoring_method": result.method}, answer=answer),
            )
        )
    return questions


def _quadratic_formula(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    monic = settings_require_monic(settings)
    integer_only = bool(settings.get("integer_only", True))

    def build() -> tuple[str, str, str | None]:
        if integer_only:
            # Integer roots: a(x − r)(x − s) so answer keys stay exact / pedagogically clean.
            a = 1 if monic else pick_quadratic_leading_coef(
                settings,
                coef_max=params.coef_max,
                max_a=4,
                prefer_nonunit=True,
            )
            r = random.randint(params.coef_min, params.coef_max)
            s = random.randint(params.coef_min, params.coef_max)
            b = -a * (r + s)
            c = a * r * s
        else:
            a = pick_quadratic_leading_coef(
                settings,
                coef_max=params.coef_max,
                max_a=5,
                prefer_nonunit=not monic,
            )
            b = random.randint(params.coef_min, params.coef_max)
            c = random.randint(params.coef_min, params.coef_max)
            if b == 0 and c == 0:
                c = random.choice([-3, -2, -1, 1, 2, 3])
        prompt = f"{format_polynomial_latex([a, b, c])} = 0"
        answer = _quadratic_formula_answer_latex(a, b, c) if include_answer_key else None
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _quadratic_discriminant(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a = pick_quadratic_leading_coef(
            settings,
            coef_max=params.coef_max,
            max_a=4,
            prefer_nonunit=not settings_require_monic(settings),
        )
        b = random.randint(params.coef_min, params.coef_max)
        c = random.randint(params.coef_min, params.coef_max)
        # Avoid degenerate x²-only prompts (still valid, but poor worksheet filler).
        if b == 0 and c == 0:
            c = random.choice([-3, -2, -1, 1, 2, 3])
        d = b * b - 4 * a * c
        poly = format_polynomial_latex([a, b, c])
        prompt = f"\\text{{Find the discriminant of }} {poly}."
        if not include_answer_key:
            answer = None
        elif d > 0:
            answer = f"D = {d}; \\text{{two real roots}}"
        elif d == 0:
            answer = "D = 0; \\text{one real root}"
        else:
            answer = f"D = {d}; \\text{{no real roots}}"
        return prompt, f"discriminant of {poly}", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _quadratic_completing_square_constant(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    integer_only = bool(settings.get("integer_only", True))

    def build() -> tuple[str, str, str | None]:
        # x² + b x + c is a PST when c = (b/2)².
        hi = max(1, abs(int(params.coef_max)) or 5)
        if integer_only:
            h = random.randint(-hi, hi)
            while h == 0:
                h = random.randint(-hi, hi)
            b = 2 * h
            c_value: Fraction | int = h * h
        else:
            b = random.randint(-hi, hi)
            while b == 0:
                b = random.randint(-hi, hi)
            c_value = Fraction(b * b, 4)
        prompt = (
            f"{format_polynomial_latex([1, b, 0])} + c "
            f"\\text{{ is a perfect square trinomial. Find }} c."
        )
        if not include_answer_key:
            answer = None
        elif isinstance(c_value, Fraction) and c_value.denominator != 1:
            answer = _format_fraction_value(c_value)
        else:
            answer = str(int(c_value))
        return prompt, f"find c for square with b={b}", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _quadratic_completing_square_solve(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    monic = settings_require_monic(settings)
    integer_only = bool(settings.get("integer_only", True))

    def build() -> tuple[str, str, str | None]:
        a = 1 if monic else pick_quadratic_leading_coef(
            settings,
            coef_max=params.coef_max,
            max_a=4,
            prefer_nonunit=True,
        )
        hi = max(1, min(8, abs(int(params.coef_max)) or 5))
        h = random.randint(-hi, hi)
        while h == 0:
            h = random.randint(-hi, hi)
        # a(x + h)² + k = 0  ⇒  (x + h)² = -k/a
        if integer_only:
            # Prefer integer/perfect-square radicands after dividing by a.
            root = random.randint(0, max(1, hi))
            # k = -a * root²  so solutions are x = -h ± root (or none if we flip sign)
            if random.random() < 0.75 or root == 0:
                k = -a * (root * root)
            else:
                k = a * (root * root)  # forces no real solutions
        else:
            k = random.randint(-hi * hi, hi * hi)
            while k == 0:
                k = random.randint(-hi * hi, hi * hi)

        # Expanded: a x² + 2 a h x + (a h² + k) = 0
        b = 2 * a * h
        c = a * h * h + k
        prompt = f"{format_polynomial_latex([a, b, c])} = 0"

        if not include_answer_key:
            answer = None
        else:
            # (x + h)² = -k/a
            rhs_num = -k
            # Compare signs carefully with integer a > 0 typically.
            if a < 0:
                # Divide inequality/equation carefully: rhs = -k/a
                pass
            radicand_frac = Fraction(rhs_num, a)
            if radicand_frac < 0:
                answer = "\\text{no real solutions}"
            elif radicand_frac == 0:
                answer = f"x = {-h}"
            else:
                # radicand_frac = p/q in lowest terms; write √(p/q) = √(p q)/q if needed,
                # or keep as single radicand when denominator is 1.
                if radicand_frac.denominator == 1:
                    radius = square_root_latex(
                        *Polynomial.simplify_square_root(radicand_frac.numerator)
                    )
                else:
                    # √(n/d) = √(n d) / d after clearing denominator when d square-free.
                    n, d = radicand_frac.numerator, radicand_frac.denominator
                    coeff, simp = Polynomial.simplify_square_root(n * d)
                    # √(n/d) = √(n d)/d = (coeff √simp) / d
                    if simp == 1:
                        radius = _format_fraction_value(Fraction(coeff, d))
                    else:
                        radius = fraction_latex(square_root_latex(coeff, simp), str(d))
                answer = f"x = {-h} \\pm {radius}"
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_distance_formula(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x1, y1 = random.randint(-6, 6), random.randint(-6, 6)
        x2, y2 = random.randint(-6, 6), random.randint(-6, 6)
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        prompt = f"\\text{{Find the distance between }} ({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        answer = f"{dist:.3g}" if include_answer_key else None
        return prompt, f"distance ({x1},{y1}) to ({x2},{y2})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_midpoint_formula(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x1, y1 = random.randint(-8, 8), random.randint(-8, 8)
        x2, y2 = random.randint(-8, 8), random.randint(-8, 8)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        prompt = f"\\text{{Find the midpoint of }} ({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        answer = f"\\left({mx:g}, {my:g}\\right)" if include_answer_key else None
        return prompt, f"midpoint ({x1},{y1}) to ({x2},{y2})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


_SQUARE_FREE_RADICAL_BASES = (2, 3, 5, 6, 7, 10, 11, 13, 14, 15)
_LIGHT_PERFECT_SQUARES = (4, 9, 16)
_HEAVY_PERFECT_SQUARES = (4, 9, 16, 25, 36, 49)


def _radical_term_count(settings: dict) -> int:
    min_terms = max(2, int(settings.get("min_terms", 2)))
    max_terms = max(min_terms, int(settings.get("max_terms", min_terms)))
    return random.randint(min_terms, max_terms)


def _radical_coef_range(settings: dict) -> tuple[int, int]:
    coef_min = max(1, int(settings.get("coef_min", 1)))
    coef_max = max(coef_min, int(settings.get("coef_max", 6)))
    return coef_min, coef_max


def _join_radical_terms(term_latexes: list[str]) -> str:
    from packages.polynomial_core import join_algebra_terms

    return join_algebra_terms(term_latexes)


def _build_like_radical_expression(settings: dict, ops: list[str]) -> tuple[str, str, int, int]:
    """Already-simplified like radicals: a√r ± b√r (± …)."""
    coef_min, coef_max = _radical_coef_range(settings)
    base = random.choice(_SQUARE_FREE_RADICAL_BASES)
    n_terms = _radical_term_count(settings)
    signed_coeffs: list[int] = []
    term_latexes: list[str] = []

    for index in range(n_terms):
        coeff = random.randint(coef_min, coef_max)
        if index == 0:
            signed = coeff
        else:
            op = random.choice(ops)
            signed = coeff if op == "+" else -coeff
        signed_coeffs.append(signed)
        term_latexes.append(square_root_latex(signed, base))

    total = sum(signed_coeffs)
    # Avoid a trivial zero answer when possible.
    if total == 0 and n_terms >= 2:
        signed_coeffs[-1] += 1 if signed_coeffs[-1] >= 0 else -1
        term_latexes[-1] = square_root_latex(signed_coeffs[-1], base)
        total = sum(signed_coeffs)

    prompt = _join_radical_terms(term_latexes)
    return prompt, prompt, total, base


def _build_unsimplified_radical_expression(
    settings: dict,
    ops: list[str],
    *,
    with_outer_coeffs: bool,
) -> tuple[str, str, int, int]:
    """Terms that share a simplified radical after factoring perfect squares."""
    coef_min, coef_max = _radical_coef_range(settings)
    base = random.choice(_SQUARE_FREE_RADICAL_BASES)
    n_terms = _radical_term_count(settings)
    squares = list(_HEAVY_PERFECT_SQUARES if with_outer_coeffs else _LIGHT_PERFECT_SQUARES)

    for _ in range(40):
        factors = [random.choice(squares) for _ in range(n_terms)]
        # At least one term must need simplification.
        factors[random.randrange(n_terms)] = random.choice(squares)
        # Medium: often leave one term already simplified (√base).
        if not with_outer_coeffs and n_terms >= 2 and random.random() < 0.45:
            factors[random.randrange(n_terms)] = 1
            if all(f == 1 for f in factors):
                factors[0] = random.choice(squares)

        outers: list[int] = []
        for _ in range(n_terms):
            if with_outer_coeffs:
                outer = random.randint(coef_min, coef_max)
                if n_terms >= 3 and random.random() < 0.25:
                    outer = 1
            else:
                outer = 1
            outers.append(outer)

        signed_outers: list[int] = []
        for index, outer in enumerate(outers):
            if index == 0:
                signed_outers.append(outer)
            else:
                op = random.choice(ops)
                signed_outers.append(outer if op == "+" else -outer)

        roots = [int(round(square**0.5)) for square in factors]
        signed_simplified = [signed * root for signed, root in zip(signed_outers, roots)]
        total = sum(signed_simplified)
        if total != 0:
            term_latexes = [
                square_root_latex(signed, square * base)
                for signed, square in zip(signed_outers, factors)
            ]
            prompt = _join_radical_terms(term_latexes)
            return prompt, prompt, total, base

    # Deterministic fallback if random trials keep canceling.
    factors = [4, 1] if n_terms == 2 else [4, 9, 1][:n_terms]
    while len(factors) < n_terms:
        factors.append(4)
    signed_outers = [1] + [-1] * (n_terms - 1)
    roots = [int(round(square**0.5)) for square in factors]
    total = sum(s * r for s, r in zip(signed_outers, roots))
    if total == 0:
        signed_outers[0] = 2 if with_outer_coeffs else 1
        if not with_outer_coeffs:
            factors[0] = 9
            roots[0] = 3
            total = sum(s * r for s, r in zip(signed_outers, roots))
        else:
            total = sum(s * r for s, r in zip(signed_outers, roots))
    term_latexes = [
        square_root_latex(signed, square * base)
        for signed, square in zip(signed_outers, factors)
    ]
    prompt = _join_radical_terms(term_latexes)
    return prompt, prompt, total, base


def _radical_add_subtract_modes(settings: dict) -> list[str]:
    modes: list[str] = []
    if bool(settings.get("allow_like_radicals", True)):
        modes.append("like")
    if bool(settings.get("allow_unsimplified_radicals", False)):
        modes.append("unsimplified")
    if bool(settings.get("allow_coeff_unsimplified", False)):
        modes.append("coeff_unsimplified")
    if not modes:
        # Fall back by difficulty tier when form flags are absent.
        tier = str(settings.get("difficulty_tier", "easy")).strip().lower()
        if tier == "hard":
            return ["coeff_unsimplified"]
        if tier == "medium":
            return ["unsimplified"]
        return ["like"]
    return modes


def _radical_add_subtract(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    ops = allowed_rational_operations(settings)

    def build() -> tuple[str, str, str | None]:
        mode = random.choice(_radical_add_subtract_modes(settings))
        if mode == "like":
            prompt, text, total, base = _build_like_radical_expression(settings, ops)
        elif mode == "coeff_unsimplified":
            prompt, text, total, base = _build_unsimplified_radical_expression(
                settings, ops, with_outer_coeffs=True
            )
        else:
            prompt, text, total, base = _build_unsimplified_radical_expression(
                settings, ops, with_outer_coeffs=False
            )
        answer = square_root_latex(total, base) if include_answer_key else None
        return prompt, text, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_multiply_modes(settings: dict) -> list[str]:
    modes: list[str] = []
    if bool(settings.get("allow_simple_product", True)):
        modes.append("simple")
    if bool(settings.get("allow_coeff_product", False)):
        modes.append("coeff")
    if bool(settings.get("allow_binomial_product", False)):
        modes.append("binomial")
    if modes:
        return modes
    tier = str(settings.get("difficulty_tier", "easy")).strip().lower()
    if tier == "hard":
        return ["binomial"]
    if tier == "medium":
        return ["coeff"]
    return ["simple"]


def _build_simple_radical_product(settings: dict) -> tuple[str, str, str]:
    """Easy: √a · √b with small square-free / light factors."""
    bases = list(_SQUARE_FREE_RADICAL_BASES)
    # Mix in a few small composites so some products simplify.
    pool = bases + [4, 8, 9, 12, 18]
    a = random.choice(pool)
    b = random.choice(pool)
    # Avoid perfect-square-only prompts like √4 · √9.
    if a in (4, 9) and b in (4, 9):
        b = random.choice(bases)
    prompt = f"\\sqrt{{{a}}} \\cdot \\sqrt{{{b}}}"
    coeff, simplified = Polynomial.simplify_square_root(a * b)
    return prompt, f"sqrt({a}) * sqrt({b})", square_root_latex(coeff, simplified)


def _build_coeff_radical_product(settings: dict) -> tuple[str, str, str]:
    """Medium: k√a · m√b with simplification."""
    coef_min, coef_max = _radical_coef_range(settings)
    a = random.choice(_SQUARE_FREE_RADICAL_BASES + (8, 12, 18, 20, 27, 32))
    b = random.choice(_SQUARE_FREE_RADICAL_BASES + (8, 12, 18, 20, 27, 32))
    k = random.randint(coef_min, max(coef_min, coef_max))
    m = random.randint(coef_min, max(coef_min, coef_max))
    left = square_root_latex(k, a)
    right = square_root_latex(m, b)
    prompt = f"{left} \\cdot {right}"
    coeff, simplified = Polynomial.simplify_square_root(a * b)
    answer = square_root_latex(k * m * coeff, simplified)
    return prompt, f"{k}sqrt({a}) * {m}sqrt({b})", answer


def _build_binomial_radical_product(settings: dict) -> tuple[str, str, str]:
    """Hard: (p√a ± q√b)(r√a ± s√b) style FOIL."""
    coef_min, coef_max = _radical_coef_range(settings)
    a, b = random.sample(list(_SQUARE_FREE_RADICAL_BASES[:10]), 2)
    p = random.randint(coef_min, max(coef_min, min(coef_max, 5)))
    q = random.randint(coef_min, max(coef_min, min(coef_max, 5)))
    r = random.randint(coef_min, max(coef_min, min(coef_max, 5)))
    s = random.randint(coef_min, max(coef_min, min(coef_max, 5)))
    sign_q = random.choice([1, -1])
    sign_s = random.choice([1, -1])
    left = f"\\left({square_root_latex(p, a)} {'+' if sign_q > 0 else '-'} {square_root_latex(q, b)}\\right)"
    right = f"\\left({square_root_latex(r, a)} {'+' if sign_s > 0 else '-'} {square_root_latex(s, b)}\\right)"
    prompt = f"{left}{right}"
    # (p√a + σq√b)(r√a + τs√b) = pr a + στ qs b + (pτs + σq r)√(ab)
    rational_part = p * r * a + (sign_q * sign_s) * q * s * b
    radical_coef = p * sign_s * s + sign_q * q * r
    product_rad = a * b
    extracted, leftover = Polynomial.simplify_square_root(product_rad)
    radical_coef *= extracted
    parts: list[str] = []
    if rational_part != 0:
        parts.append(str(rational_part))
    if radical_coef != 0 and leftover > 1:
        parts.append(square_root_latex(radical_coef, leftover))
    elif radical_coef != 0 and leftover == 1:
        parts.append(str(radical_coef))
    if not parts:
        answer = "0"
    elif len(parts) == 1:
        answer = parts[0]
    else:
        # Join with + / - based on second part sign already in square_root_latex.
        second = parts[1]
        if second.startswith("-"):
            answer = f"{parts[0]} - {second[1:]}"
        else:
            answer = f"{parts[0]} + {second}"
    return prompt, prompt, answer


def _radical_multiply(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        mode = random.choice(_radical_multiply_modes(settings))
        if mode == "coeff":
            prompt, text, answer = _build_coeff_radical_product(settings)
        elif mode == "binomial":
            prompt, text, answer = _build_binomial_radical_product(settings)
        else:
            prompt, text, answer = _build_simple_radical_product(settings)
        return prompt, text, answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_quotient_prompt(a: int, n: int, b: int, m: int) -> str:
    """Format (a√n)/(b√m). When n or m is 1, omit that radical."""
    if n <= 1:
        num = str(a)
    else:
        num = square_root_latex(a, n)
    if m <= 1:
        den = str(b)
    else:
        den = square_root_latex(b, m)
    return fraction_latex(num, den)


def _radical_quotient_answer(a: int, n: int, b: int, m: int) -> str:
    """Fully simplify (a√n)/(b√m), rationalizing the denominator."""
    # (a√n)/(b√m) = a√(n m) / (b m), then simplify √(n m).
    extracted, rad = Polynomial.simplify_square_root(n * m)
    num = a * extracted
    den = b * m
    g = math.gcd(abs(num), abs(den))
    num //= g
    den //= g
    if den < 0:
        num = -num
        den = -den
    if rad <= 1:
        if den == 1:
            return str(num)
        return fraction_latex(str(num), str(den))
    num_latex = square_root_latex(num, rad)
    if den == 1:
        return num_latex
    return fraction_latex(num_latex, str(den))


def _build_reduced_radical_quotient(settings: dict) -> tuple[str, str, str]:
    """Easy: already-reduced divisions like √12/√3 or 6√5/2√5."""
    coef_min, coef_max = _radical_coef_range(settings)
    if random.random() < 0.5:
        # Coefficient cancellation of like radicals: (k b)√r / b√r = k.
        base = random.choice(_SQUARE_FREE_RADICAL_BASES)
        b = random.randint(coef_min, coef_max)
        k = random.randint(2, max(2, min(6, coef_max)))
        a = b * k
        prompt = _radical_quotient_prompt(a, base, b, base)
        return prompt, f"{a}sqrt({base})/{b}sqrt({base})", _radical_quotient_answer(a, base, b, base)

    # Immediate quotient property: √(k² m) / √m = k.
    m = random.choice(_SQUARE_FREE_RADICAL_BASES)
    k = random.randint(2, 5)
    n = k * k * m
    prompt = _radical_quotient_prompt(1, n, 1, m)
    return prompt, f"sqrt({n})/sqrt({m})", _radical_quotient_answer(1, n, 1, m)


def _build_simplify_radical_quotient(settings: dict) -> tuple[str, str, str]:
    """Medium: simplify perfect squares / cancel after rewriting → c√r with r>1."""
    coef_min, coef_max = _radical_coef_range(settings)
    leftover = random.choice(_SQUARE_FREE_RADICAL_BASES)
    cancel = random.choice([b for b in _SQUARE_FREE_RADICAL_BASES if b != leftover] or [2])
    square = random.choice(_LIGHT_PERFECT_SQUARES)
    # √(square · leftover · cancel) / √cancel = √(square · leftover) → outer √leftover
    n = square * leftover * cancel
    m = cancel
    a = 1
    b = 1
    if coef_max > 1 and random.random() < 0.4:
        b = random.randint(coef_min, max(coef_min, min(coef_max, 3)))
        a = b * random.randint(1, 3)
    elif coef_max > 1 and random.random() < 0.35:
        a = random.randint(coef_min, max(coef_min, min(coef_max, 3)))
    prompt = _radical_quotient_prompt(a, n, b, m)
    return prompt, f"{a}sqrt({n})/{b}sqrt({m})", _radical_quotient_answer(a, n, b, m)


def _build_rationalize_radical_quotient(settings: dict) -> tuple[str, str, str]:
    """Hard: rationalize denominator and/or multi-factor coeffs + radicals."""
    coef_min, coef_max = _radical_coef_range(settings)
    kind = random.choice(["rationalize_plain", "rationalize_num", "coeff_multi"])

    if kind == "rationalize_plain":
        # a / √m → a√m / m
        a = random.randint(max(2, coef_min), max(coef_min, coef_max))
        m = random.choice(_SQUARE_FREE_RADICAL_BASES)
        prompt = _radical_quotient_prompt(a, 1, 1, m)
        return prompt, f"{a}/sqrt({m})", _radical_quotient_answer(a, 1, 1, m)

    if kind == "rationalize_num":
        # √n / √m with m not dividing n, so the denominator must be rationalized.
        bases = list(_SQUARE_FREE_RADICAL_BASES)
        n_base = random.choice(bases)
        m = random.choice([b for b in bases if b != n_base and n_base % b != 0 and b % n_base != 0])
        square = random.choice(_LIGHT_PERFECT_SQUARES + _HEAVY_PERFECT_SQUARES[:3])
        n = square * n_base
        # Reject accidental clean division (n multiple of m).
        if n % m == 0:
            m = random.choice([b for b in bases if n % b != 0] or [bases[0]])
        a = random.randint(coef_min, max(coef_min, min(coef_max, 5)))
        prompt = _radical_quotient_prompt(a, n, 1, m)
        return prompt, f"{a}sqrt({n})/sqrt({m})", _radical_quotient_answer(a, n, 1, m)

    # Coefficients on multi-factor unsimplified radicands.
    r1 = random.choice(_SQUARE_FREE_RADICAL_BASES)
    r2 = random.choice(_SQUARE_FREE_RADICAL_BASES)
    s1 = random.choice(_HEAVY_PERFECT_SQUARES)
    s2 = random.choice(_HEAVY_PERFECT_SQUARES)
    n = s1 * r1
    m = s2 * r2
    b = random.randint(coef_min, max(coef_min, coef_max))
    a = random.randint(coef_min, max(coef_min, coef_max))
    # Prefer a divisible by b sometimes for cleaner answers, but not required.
    if random.random() < 0.4:
        a = b * random.randint(1, 4)
    prompt = _radical_quotient_prompt(a, n, b, m)
    return prompt, f"{a}sqrt({n})/{b}sqrt({m})", _radical_quotient_answer(a, n, b, m)


def _radical_divide_modes(settings: dict) -> list[str]:
    modes: list[str] = []
    if bool(settings.get("allow_reduced_quotients", True)):
        modes.append("reduced")
    if bool(settings.get("allow_simplify_quotients", False)):
        modes.append("simplify")
    if bool(settings.get("allow_rationalize_divide", False)):
        modes.append("rationalize")
    if not modes:
        tier = str(settings.get("difficulty_tier", "easy")).strip().lower()
        if tier == "hard":
            return ["rationalize"]
        if tier == "medium":
            return ["simplify"]
        return ["reduced"]
    return modes


def _radical_divide(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        mode = random.choice(_radical_divide_modes(settings))
        if mode == "simplify":
            prompt, text, answer = _build_simplify_radical_quotient(settings)
        elif mode == "rationalize":
            prompt, text, answer = _build_rationalize_radical_quotient(settings)
        else:
            prompt, text, answer = _build_reduced_radical_quotient(settings)
        return prompt, text, answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_equations(topic: str, settings: dict) -> list[Question]:
    from .radical_equations import generate_radical_equations

    return generate_radical_equations(topic, settings)


def _rational_equations(topic: str, settings: dict) -> list[Question]:
    from .rational_equations import generate_rational_equations

    return generate_rational_equations(topic, settings)


def _complex_fractions(topic: str, settings: dict) -> list[Question]:
    from .complex_fractions import generate_complex_fractions

    return generate_complex_fractions(topic, settings)


def _rational_expression_multiply_divide(topic: str, settings: dict) -> list[Question]:
    from .rational_multiply_divide import generate_rational_expression_multiply_divide

    return generate_rational_expression_multiply_divide(topic, settings)


def _scaffold(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    questions: list[Question] = []
    for index in range(count):
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        prompt_latex = f"{a} + {b}"
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt_latex,
                prompt_text=f"{a} + {b}",
                answer_latex=str(a + b) if include_answer_key else None,
                metadata=scaffold_metadata(),
            )
        )
    return questions


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "scaffold": _scaffold,
    "exponential_growth_decay": _exponential_growth_decay,
    "polynomial_add_subtract": _polynomial_add_subtract,
    "polynomial_multiply": _polynomial_multiply,
    "polynomial_multiply_special": _polynomial_multiply_special,
    "polynomial_factoring_common_factor": _polynomial_factoring_common_factor_only,
    "polynomial_factoring_special_cases": _polynomial_factoring_special_cases,
    "polynomial_factoring_grouping": lambda topic, settings: _polynomial_factoring(
        topic,
        settings,
        {
            "factor_normal": False,
            "factor_grouping": True,
            "factor_substitution": False,
            "factor_difference_of_squares": False,
            "factor_perfect_square_trinomial": False,
            "factor_difference_of_cubes": False,
            "factor_sum_of_cubes": False,
            "factor_rrt": False,
        },
    ),
    "quadratic_square_roots": _quadratic_square_roots,
    "quadratic_factoring_equations": _quadratic_factoring_equations,
    "quadratic_formula": _quadratic_formula,
    "quadratic_discriminant": _quadratic_discriminant,
    "quadratic_completing_square_constant": _quadratic_completing_square_constant,
    "quadratic_completing_square_solve": _quadratic_completing_square_solve,
    "radical_distance_formula": _radical_distance_formula,
    "radical_midpoint_formula": _radical_midpoint_formula,
    "radical_add_subtract": _radical_add_subtract,
    "radical_multiply": _radical_multiply,
    "radical_divide": _radical_divide,
    "radical_equations": _radical_equations,
    "rational_equations": _rational_equations,
    "rational_expression_multiply_divide": _rational_expression_multiply_divide,
    "complex_fractions": _complex_fractions,
}
