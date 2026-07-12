"""Generate expanded special-product polynomials for factoring practice.

Prompts are always the expanded form (e.g. ``x^3 - 8``, ``x^2 + 6x + 9``,
``x^8 - 1``). Answers are complete factorizations using special-product patterns.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Literal

from .latex import format_factor_product_latex
from .polynomial import Polynomial

SpecialPattern = Literal[
    "difference_of_squares",
    "perfect_square_trinomial",
    "sum_of_cubes",
    "difference_of_cubes",
    "higher_even_power",
]

_CUBES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
_SQUARES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)


@dataclass(frozen=True)
class SpecialProductResult:
    polynomial: Polynomial
    factors: tuple[Polynomial, ...]
    pattern: SpecialPattern
    gcf: int = 1

    @property
    def method(self) -> str:
        return self.pattern

    def answer_latex(self) -> str:
        return _format_complete_factorization(self.gcf, self.factors)


def _format_complete_factorization(gcf: int, factors: tuple[Polynomial, ...]) -> str:
    # Collapse identical linear factors into a square: (ax+b)^2
    if (
        len(factors) == 2
        and factors[0].deg() == 1
        and factors[1].deg() == 1
        and factors[0].terms == factors[1].terms
    ):
        body = f"({factors[0].to_latex()})^2"
    else:
        body = format_factor_product_latex(factors)
    if gcf == 1:
        return body
    if gcf == -1:
        return f"-{body}"
    return f"{gcf}{body}"


def _pick_positive(pool: tuple[int, ...], max_abs: int) -> int:
    candidates = [n for n in pool if 1 <= n <= max_abs]
    return random.choice(candidates or [1])


def _pick_coprime_pair(pool: tuple[int, ...], max_abs: int) -> tuple[int, int]:
    for _ in range(30):
        a = _pick_positive(pool, max_abs)
        b = _pick_positive(pool, max_abs)
        if math.gcd(a, b) == 1:
            return a, b
    return 1, _pick_positive(pool, max_abs)


def _linear(a: int, b: int) -> Polynomial:
    """ax + b."""
    return Polynomial([a, b])


def _maybe_gcf(settings: dict, hard: bool) -> int:
    if bool(settings.get("require_gcf", False)):
        return random.choice([2, 3, 4, 5, 6])
    if hard and random.random() < 0.35:
        return random.choice([2, 3, 4, 5])
    return 1


def _apply_gcf(
    poly: Polynomial,
    factors: tuple[Polynomial, ...],
    gcf: int,
) -> tuple[Polynomial, tuple[Polynomial, ...], int]:
    if gcf == 1:
        return poly, factors, 1
    return poly * gcf, factors, gcf


def _gen_difference_of_squares(
    coef_max: int,
    *,
    hard: bool,
    settings: dict,
) -> SpecialProductResult:
    monic = bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    )
    max_a = 1 if monic else min(coef_max, 6 if hard else 4)

    # Hard: composite bases such as x^4 - 16 = (x^2)^2 - 4^2
    if hard and not monic and random.random() < 0.35:
        b = _pick_positive(_SQUARES, max_a)
        # x^4 - b^2
        poly = Polynomial([1, 0, 0, 0, -(b * b)])
        root = int(round(b**0.5))
        if root * root == b:
            # e.g. x^4 - 16 → (x-2)(x+2)(x^2+4)
            factors = (
                _linear(1, -root),
                _linear(1, root),
                Polynomial([1, 0, b]),
            )
        else:
            factors = (
                Polynomial([1, 0, -b]),
                Polynomial([1, 0, b]),
            )
        gcf = _maybe_gcf(settings, hard)
        poly, factors, gcf = _apply_gcf(poly, factors, gcf)
        return SpecialProductResult(poly, factors, "difference_of_squares", gcf)

    if monic:
        a, b = 1, _pick_positive(_SQUARES, min(coef_max, 5 if hard else 4))
    else:
        a = _pick_positive(_SQUARES, max_a)
        b = _pick_positive(_SQUARES, max_a)
        if math.gcd(a, b) != 1:
            a, b = _pick_coprime_pair(_SQUARES, max_a)
    poly = Polynomial([a * a, 0, -(b * b)])
    factors = (_linear(a, -b), _linear(a, b))
    gcf = _maybe_gcf(settings, hard)
    poly, factors, gcf = _apply_gcf(poly, factors, gcf)
    return SpecialProductResult(poly, factors, "difference_of_squares", gcf)


def _gen_perfect_square_trinomial(
    coef_max: int,
    *,
    hard: bool,
    settings: dict,
) -> SpecialProductResult:
    monic = bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    )
    max_a = 1 if monic else min(coef_max, 5 if hard else 3)
    if monic:
        a, b = 1, _pick_positive(_SQUARES, min(coef_max, 5 if hard else 3))
    else:
        a, b = _pick_coprime_pair(_SQUARES, max_a)
    sign = random.choice([1, -1])
    poly = Polynomial([a * a, sign * 2 * a * b, b * b])
    factor = _linear(a, sign * b)
    factors = (factor, factor)
    gcf = _maybe_gcf(settings, hard)
    poly, factors, gcf = _apply_gcf(poly, factors, gcf)
    return SpecialProductResult(poly, factors, "perfect_square_trinomial", gcf)


def _gen_sum_of_cubes(
    coef_max: int,
    *,
    hard: bool,
    settings: dict,
) -> SpecialProductResult:
    monic = bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    )
    max_n = 1 if monic else min(coef_max, 6 if hard else 4)
    if monic:
        a, b = 1, _pick_positive(_CUBES, min(coef_max, 4))
    else:
        a, b = _pick_coprime_pair(_CUBES, max_n)
    poly = Polynomial([a * a * a, 0, 0, b * b * b])
    factors = (_linear(a, b), Polynomial([a * a, -(a * b), b * b]))
    gcf = _maybe_gcf(settings, hard)
    poly, factors, gcf = _apply_gcf(poly, factors, gcf)
    return SpecialProductResult(poly, factors, "sum_of_cubes", gcf)


def _gen_difference_of_cubes(
    coef_max: int,
    *,
    hard: bool,
    settings: dict,
) -> SpecialProductResult:
    monic = bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    )
    max_n = 1 if monic else min(coef_max, 6 if hard else 4)
    if monic:
        a, b = 1, _pick_positive(_CUBES, min(coef_max, 4))
    else:
        a, b = _pick_coprime_pair(_CUBES, max_n)
    poly = Polynomial([a * a * a, 0, 0, -(b * b * b)])
    factors = (_linear(a, -b), Polynomial([a * a, a * b, b * b]))
    gcf = _maybe_gcf(settings, hard)
    poly, factors, gcf = _apply_gcf(poly, factors, gcf)
    return SpecialProductResult(poly, factors, "difference_of_cubes", gcf)


def _factor_x_n_minus_one(n: int) -> tuple[Polynomial, ...]:
    """School-friendly complete factorization of ``x^n - 1``."""
    if n == 1:
        return (Polynomial([1, -1]),)
    if n == 2:
        return (Polynomial([1, -1]), Polynomial([1, 1]))
    if n == 3:
        return (Polynomial([1, -1]), Polynomial([1, 1, 1]))
    if n == 4:
        return (
            Polynomial([1, -1]),
            Polynomial([1, 1]),
            Polynomial([1, 0, 1]),
        )
    if n == 6:
        return (
            Polynomial([1, -1]),
            Polynomial([1, 1]),
            Polynomial([1, 1, 1]),
            Polynomial([1, -1, 1]),
        )
    if n == 8:
        return (
            Polynomial([1, -1]),
            Polynomial([1, 1]),
            Polynomial([1, 0, 1]),
            Polynomial([1, 0, 0, 0, 1]),
        )
    if n % 2 == 0:
        half = n // 2
        return _factor_x_n_minus_one(half) + _factor_x_n_plus_one(half)
    return (Polynomial([1, -1]), Polynomial([1] * n))


def _factor_x_n_plus_one(n: int) -> tuple[Polynomial, ...]:
    """School-friendly factorization of ``x^n + 1``."""
    if n == 1:
        return (Polynomial([1, 1]),)
    if n == 2:
        return (Polynomial([1, 0, 1]),)
    if n == 3:
        return (Polynomial([1, 1]), Polynomial([1, -1, 1]))
    if n == 4:
        # Irreducible over Q — leave as x^4 + 1
        return (Polynomial([1, 0, 0, 0, 1]),)
    if n % 2 == 1:
        coeffs = [1 if i % 2 == 0 else -1 for i in range(n)]
        return (Polynomial([1, 1]), Polynomial(coeffs))
    coeffs = [0] * (n + 1)
    coeffs[0] = 1
    coeffs[-1] = 1
    return (Polynomial(coeffs),)


def _factor_a_x_n_minus_b(a: int, b: int, n: int) -> tuple[Polynomial, ...]:
    """Factor ``a^n x^n - b^n`` completely with special products."""
    if a == 1 and b == 1:
        return _factor_x_n_minus_one(n)
    if n == 2:
        return (_linear(a, -b), _linear(a, b))
    if n == 3:
        return (_linear(a, -b), Polynomial([a * a, a * b, b * b]))
    if n == 4:
        return (
            _linear(a, -b),
            _linear(a, b),
            Polynomial([a * a, 0, b * b]),
        )
    if n == 6:
        return (
            _linear(a, -b),
            Polynomial([a * a, a * b, b * b]),
            _linear(a, b),
            Polynomial([a * a, -(a * b), b * b]),
        )
    if n == 8:
        return (
            _linear(a, -b),
            _linear(a, b),
            Polynomial([a * a, 0, b * b]),
            Polynomial([a**4, 0, 0, 0, b**4]),
        )
    # Even fallback: one difference-of-squares step
    half = n // 2
    A, B = a**half, b**half
    left = [0] * (half + 1)
    right = [0] * (half + 1)
    left[0], left[-1] = A, -B
    right[0], right[-1] = A, B
    return (Polynomial(left), Polynomial(right))


def _gen_higher_even_power(coef_max: int, *, settings: dict) -> SpecialProductResult:
    max_power = int(settings.get("max_even_power", 8))
    max_power = max(4, min(max_power, 8))
    power_choices = [p for p in (4, 6, 8) if p <= max_power] or [4]
    weights = [3 if p == 8 else 2 if p == 4 else 1 for p in power_choices]
    n = random.choices(power_choices, weights=weights, k=1)[0]

    # Prefer classic monic forms; sometimes 16x^4 - 1 style (not huge x^8 coeffs)
    roll = random.random()
    if roll < 0.7:
        a, b = 1, 1
    elif n >= 8:
        a, b = random.choice([(2, 1), (1, 1)])
    elif roll < 0.9:
        a = _pick_positive((2, 3), min(coef_max, 3))
        b = 1
    else:
        a, b = _pick_coprime_pair((1, 2, 3), min(coef_max, 3))

    coeffs = [0] * (n + 1)
    coeffs[0] = a**n
    coeffs[-1] = -(b**n)
    poly = Polynomial(coeffs)
    factors = _factor_a_x_n_minus_b(a, b, n)

    gcf = 1
    if bool(settings.get("require_gcf", False)):
        gcf = random.choice([2, 3, 4])
        poly = poly * gcf

    return SpecialProductResult(poly, factors, "higher_even_power", gcf)


def enabled_special_patterns(settings: dict) -> list[SpecialPattern]:
    """Resolve which special-product patterns are enabled from settings."""
    patterns: list[SpecialPattern] = []
    if bool(settings.get("factor_difference_of_squares", True)):
        patterns.append("difference_of_squares")
    if bool(settings.get("factor_perfect_square_trinomial", True)):
        patterns.append("perfect_square_trinomial")
    if bool(settings.get("factor_sum_of_cubes", True)):
        patterns.append("sum_of_cubes")
    if bool(settings.get("factor_difference_of_cubes", True)):
        patterns.append("difference_of_cubes")
    if bool(settings.get("allow_higher_even_powers", False)):
        patterns.append("higher_even_power")
    if not patterns:
        patterns = ["difference_of_squares", "perfect_square_trinomial"]
    return patterns


def create_special_product_problem(settings: dict) -> SpecialProductResult:
    """Build one expanded special-product factoring problem."""
    coef_min = int(settings.get("coef_min", settings.get("c_min", -8)))
    coef_max = int(settings.get("coef_max", settings.get("c_max", 8)))
    coef_max = max(abs(coef_min), abs(coef_max), 1)
    hard = str(settings.get("difficulty_tier", "")).lower() == "hard"
    if bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    ):
        coef_max = min(coef_max, 3)

    patterns = enabled_special_patterns(settings)
    pattern = random.choice(patterns)
    generators = {
        "difference_of_squares": lambda: _gen_difference_of_squares(
            coef_max, hard=hard, settings=settings
        ),
        "perfect_square_trinomial": lambda: _gen_perfect_square_trinomial(
            coef_max, hard=hard, settings=settings
        ),
        "sum_of_cubes": lambda: _gen_sum_of_cubes(coef_max, hard=hard, settings=settings),
        "difference_of_cubes": lambda: _gen_difference_of_cubes(
            coef_max, hard=hard, settings=settings
        ),
        "higher_even_power": lambda: _gen_higher_even_power(coef_max, settings=settings),
    }
    return generators[pattern]()
