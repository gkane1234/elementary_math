"""Number generator framework — rationals, decimals, percents, ratios, rates."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from typing import Any

from .base import QuestionFramework
from ..generators.utils import (
    format_binop_expression,
    format_fraction_division_latex,
    format_linear_latex,
    format_measurement_text,
    format_with_unit,
    frac_latex,
    frac_or_mixed_latex,
    normalize_expression_signs,
    random_fraction,
    random_int_range,
)
from ..settings.params import allowed_division_notations


@dataclass(frozen=True)
class NumberParams:
    num_min: int = -10
    num_max: int = 10
    denom_min: int = 2
    denom_max: int = 12
    allow_negative: bool = True
    allow_mixed: bool = False
    require_proper: bool = False


def _bounded_int(settings: dict, key: str, default: int) -> int:
    return int(settings.get(key, default))


def _int_range(settings: dict, min_key: str, max_key: str, *, lo_default: int, hi_default: int) -> tuple[int, int]:
    lo = _bounded_int(settings, min_key, lo_default)
    hi = _bounded_int(settings, max_key, hi_default)
    return min(lo, hi), max(lo, hi)


def number_params_from_settings(settings: dict) -> NumberParams:
    from ..settings.enrichment import apply_positive_coefficient_restriction, scaled_int_range

    allow_negative = bool(settings.get("allow_negative", True))
    if bool(settings.get("coefficients_positive_only", False)):
        allow_negative = False
    cont = continuous_abs_max(settings)
    if cont is not None:
        if allow_negative:
            num_min, num_max = -cont, cont
        else:
            num_min, num_max = 1, cont
    else:
        num_min = int(settings.get("coef_min", settings.get("num_min", -10)))
        num_max = int(settings.get("coef_max", settings.get("num_max", 10)))
        num_min, num_max = scaled_int_range(settings, num_min, num_max)
    num_min, num_max = apply_positive_coefficient_restriction(settings, num_min, num_max)
    if not allow_negative:
        num_min = max(1, num_min)
        num_max = max(num_min, num_max)
    # Denominators also widen slowly with continuous D.
    if cont is not None:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        d = settings_difficulty(settings, default=0.0)
        denom_min = 2
        denom_max = max(4, min(36, int(4 + d / 2)))
    else:
        denom_min, denom_max = _int_range(
            settings, "denom_min", "denom_max", lo_default=2, hi_default=12
        )
    return NumberParams(
        num_min=min(num_min, num_max),
        num_max=max(num_min, num_max),
        denom_min=denom_min,
        denom_max=denom_max,
        allow_negative=allow_negative,
        allow_mixed=bool(settings.get("allow_mixed", False)),
        require_proper=bool(settings.get("require_proper", False)),
    )


def _ratio_bounds(settings: dict) -> tuple[int, int]:
    cont = continuous_ratio_part_max(settings)
    if cont is not None:
        return 1, cont
    return _int_range(
        settings, "ratio_part_min", "ratio_part_max", lo_default=2, hi_default=15
    )


def _unit_rate_bounds(settings: dict) -> tuple[int, int, int, int]:
    """Legacy EMH bounds when continuous ``difficulty`` is absent."""
    rate_min, rate_max = _int_range(
        settings, "unit_rate_min", "unit_rate_max", lo_default=2, hi_default=12
    )
    mult_min, mult_max = _int_range(
        settings,
        "unit_rate_multiplier_min",
        "unit_rate_multiplier_max",
        lo_default=2,
        hi_default=8,
    )
    return rate_min, rate_max, mult_min, mult_max


def continuous_unit_rate_core_max(settings: dict) -> int | None:
    """Max size of the unit rate itself (miles/hour, $/lb).

    Cores stay relatively modest so skill demand comes from inflate-k /
    non-obvious equivalent-rate scales (same spirit as ratio cores).
    """
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    # D=0 → 4; D=10 → 7; D=20 → 12; D=40 → 28; D=1000 → huge
    return max(3, int(4 + 0.25 * d + 0.01 * d * d))


def continuous_unit_rate_qty_max(settings: dict) -> int | None:
    """Max given quantity (hours / pounds) — the inflate factor ``k``."""
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    # Same polynomial growth as ratio inflate-k.
    return max(2, int(2 + 0.4 * d + 0.02 * d * d))


def continuous_unit_rate_scale_max(settings: dict) -> int | None:
    """Max equivalence multiplier ``m`` for equivalent-rate prompts."""
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    return max(2, int(3 + 0.3 * d + 0.008 * d * d))


def _sample_unit_rate_core_and_qty(settings: dict) -> tuple[int, int]:
    """Factors-first: unit rate ``r``, quantity ``k`` → total ``r·k``.

    Low D: small friendly rates and short quantities (×2/×3).
    High D: larger rates and composite quantities that need canceling.
    """
    k_max = continuous_unit_rate_qty_max(settings)
    if k_max is None:
        rate_lo, rate_hi, mult_lo, mult_hi = _unit_rate_bounds(settings)
        return random.randint(rate_lo, rate_hi), random.randint(mult_lo, mult_hi)

    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    core_hi = continuous_unit_rate_core_max(settings) or 4
    if d < 3:
        rate = random.randint(2, min(6, core_hi))
        k = random.choice([2, 3])
    else:
        rate = random.randint(2, core_hi)
        k = _sample_ratio_inflate_k(d, k_max, min_k=2)
    return rate, k


def _sample_equivalent_rate_pair(settings: dict) -> tuple[int, int, int, int]:
    """Build an equivalent-rate scale: ``total1`` for ``q1`` ↔ ``total2`` for ``q2``.

    Returns ``(total1, q1, total2, q2)`` with common unit rate ``total1/q1``.
    Low D: obvious ×2/×3. High D: unreduced given rate and/or non-integer
    surface scale (reduce-then-scale).
    """
    k_max = continuous_unit_rate_qty_max(settings)
    if k_max is None:
        rate, q1 = _sample_unit_rate_core_and_qty(settings)
        m = random.randint(2, 5)
        return rate * q1, q1, rate * q1 * m, q1 * m

    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    core_hi = continuous_unit_rate_core_max(settings) or 4
    m_max = continuous_unit_rate_scale_max(settings) or 3
    rate = random.randint(2, min(6, core_hi) if d < 3 else core_hi)

    if d < 3:
        k = random.choice([2, 3])
        m = random.choice([2, 3])
        reduce_then_scale = False
    elif d < 10:
        k = _sample_ratio_inflate_k(d, min(k_max, 8), min_k=2)
        m = random.randint(2, min(5, m_max))
        reduce_then_scale = k > 1 and random.random() < 0.45
    else:
        k = _sample_ratio_inflate_k(d, k_max, min_k=2)
        m_lo = max(2, int(m_max * 0.35))
        m = random.randint(m_lo, m_max)
        reduce_then_scale = k > 1 and random.random() < 0.75

    q1 = k
    total1 = rate * k
    if reduce_then_scale and k > 1:
        hi = max(m_max + 4, m + 4)
        candidates = [x for x in range(2, hi + 1) if x % k != 0 and x != k]
        if d >= 12 and candidates:
            floor = max(2, int(m_max * 0.35))
            preferred = [x for x in candidates if x >= floor]
            m = random.choice(preferred or candidates)
        elif candidates:
            m = random.choice(candidates)
        q2 = m
        total2 = rate * m
    else:
        # Integer surface scale of the given rate.
        q2 = q1 * m
        total2 = total1 * m
    return total1, q1, total2, q2


def continuous_ratio_inflate_max(settings: dict) -> int | None:
    """Max common factor ``k`` for inflating a simplified core ratio.

    When continuous ``difficulty`` is set: D≈0 → k=1 (already simplified),
    D≈10 → tens-ish GCF budget, D≈40 → large composite inflate factors.
    """
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    # Polynomial growth — no soft asymptote (same spirit as continuous_abs_max).
    hi = int(1 + 0.4 * d + 0.02 * d * d)
    return max(1, hi)


def continuous_ratio_core_max(settings: dict) -> int | None:
    """Max part size for the simplified core ``(a:b)`` with gcd=1."""
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    # Keep cores modest so skill demand comes from inflate-k / scale-m.
    return max(3, int(5 + 0.2 * d))


def continuous_ratio_scale_max(settings: dict) -> int | None:
    """Max equivalence multiplier ``m`` for missing-value / proportion prompts."""
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    return max(2, int(3 + 0.3 * d + 0.008 * d * d))


def continuous_ratio_part_max(settings: dict) -> int | None:
    """Upper bound on a displayed ratio part (core × inflate)."""
    k_max = continuous_ratio_inflate_max(settings)
    core_max = continuous_ratio_core_max(settings)
    if k_max is None or core_max is None:
        return None
    return max(8, core_max * k_max)


def _sample_coprime_ratio_core(part_hi: int) -> tuple[int, int]:
    """Sample simplified core parts ``(a, b)`` with ``gcd(a, b) == 1``."""
    part_hi = max(2, int(part_hi))
    for _ in range(60):
        a = random.randint(1, part_hi)
        b = random.randint(1, part_hi)
        if a != b and math.gcd(a, b) == 1:
            return a, b
    return 2, 3


def _sample_ratio_inflate_k(d: float, k_max: int, *, min_k: int = 1) -> int:
    """Common factor ``k``; prefers already-simple at low D, composites at high D.

    ``min_k=1`` (ratios): often already-simplified at low D.
    ``min_k=2`` (simplify-fractions): always something to cancel; low D uses 2 or 3.
    """
    k_max = max(1, int(k_max))
    min_k = max(1, min(int(min_k), k_max))
    if k_max <= 1:
        return 1
    if d < 2.5:
        if min_k <= 1:
            return 1 if random.random() < 0.85 else min(2, k_max)
        pool = [k for k in (2, 3) if min_k <= k <= k_max]
        return random.choice(pool) if pool else min_k
    if d < 8:
        if min_k >= 2:
            hi = max(min_k, min(k_max, 12))
            return random.randint(min_k, hi)
        return random.randint(1, max(1, min(k_max, 4)))
    # Product of small primes → multi-step cancel (e.g. 12, 18, 24, 36).
    primes = (2, 2, 3, 3, 5, 5, 7)
    k = 1
    for _ in range(4 if d >= 20 else 3):
        p = random.choice(primes)
        if k * p <= k_max:
            k *= p
    if k < min_k:
        k = random.randint(min_k, k_max)
    floor = max(min_k, int(k_max * 0.35)) if d >= 15 else min_k
    if d >= 15 and k < floor:
        k = random.randint(floor, k_max)
    return min(max(k, min_k), k_max)


def continuous_simplify_frac_core_max(settings: dict) -> int | None:
    """Max size of reduced numerator/denominator parts (gcd=1)."""
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    # D=0 → 3; D=10 → ~6; D=20 → ~10; D=40 → ~21
    return max(2, int(3 + 0.25 * d + 0.005 * d * d))


def continuous_simplify_frac_inflate_max(settings: dict) -> int | None:
    """Max inflate factor ``k`` (GCF of the shown fraction)."""
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    # D=0 → 3; D=10 → ~11; D=20 → ~23; D=40 → ~63
    return max(3, int(3 + 0.5 * d + 0.025 * d * d))


def sample_unreduced_numeric_fraction(settings: dict) -> tuple[int, int]:
    """Build an unreduced fraction factors-first: reduced ``a/b``, then ×``k``.

    Returns ``(num, den)`` with ``gcd(num, den) = k >= 2`` when continuous
    difficulty is active. Legacy EMH / no-``difficulty`` uses a fixed small pool.
    """
    k_max = continuous_simplify_frac_inflate_max(settings)
    if k_max is None:
        g = random.randint(2, 12)
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        while math.gcd(a, b) != 1:
            b = random.randint(1, 12)
        num, den = a * g, b * g
        if random.choice([True, False]):
            num, den = den, num
        return num, den

    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    core_hi = continuous_simplify_frac_core_max(settings) or 3
    core_a, core_b = _sample_coprime_ratio_core(core_hi)
    k = _sample_ratio_inflate_k(d, k_max, min_k=2)
    num, den = core_a * k, core_b * k
    # Low D: prefer proper (4/6, 6/9). Higher D: improper is fine.
    if d < 5.0:
        if num > den:
            num, den = den, num
    elif random.random() < 0.45:
        num, den = den, num
    return num, den


def _sample_shown_ratio_parts(settings: dict) -> tuple[int, int]:
    """Displayed ratio parts, factors-first when continuous difficulty is active."""
    k_max = continuous_ratio_inflate_max(settings)
    if k_max is None:
        lo, hi = _int_range(
            settings, "ratio_part_min", "ratio_part_max", lo_default=2, hi_default=15
        )
        return random.randint(lo, hi), random.randint(lo, hi)
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    core_hi = continuous_ratio_core_max(settings) or 5
    core_a, core_b = _sample_coprime_ratio_core(core_hi)
    k = _sample_ratio_inflate_k(d, k_max)
    return core_a * k, core_b * k


def _sample_equivalent_ratio_missing(settings: dict) -> tuple[int, int, int, int]:
    """Build ``a:b = c:x`` with missing ``x``.

    Low D: small already-simplified left side and obvious ×2/×3.
    Mid/high D: unreduced left and/or reduce-then-scale (``c/a`` not an integer)
    so students must cancel a non-obvious factor rather than spot a tiny multiply.
    """
    k_max = continuous_ratio_inflate_max(settings)
    if k_max is None:
        lo, hi = _int_range(
            settings, "ratio_part_min", "ratio_part_max", lo_default=2, hi_default=15
        )
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        factor = random.randint(2, 5)
        return a, b, a * factor, b * factor

    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    core_hi = continuous_ratio_core_max(settings) or 5
    m_max = continuous_ratio_scale_max(settings) or 3
    core_a, core_b = _sample_coprime_ratio_core(core_hi)

    if d < 3:
        k = 1
        m = random.choice([2, 3])
        reduce_then_scale = False
    elif d < 10:
        k = _sample_ratio_inflate_k(d, min(k_max, 6))
        m = random.randint(2, min(5, m_max))
        reduce_then_scale = k > 1 and random.random() < 0.5
    else:
        k = _sample_ratio_inflate_k(d, k_max)
        m_lo = max(2, int(m_max * 0.4))
        m = random.randint(m_lo, m_max)
        reduce_then_scale = k > 1 and random.random() < 0.7

    a, b = core_a * k, core_b * k
    if reduce_then_scale and k > 1:
        # Prefer m not a multiple of k so left→right isn't an integer scale on
        # the unreduced surface (e.g. 12:20 = 15:x, not 12:20 = 36:x).
        hi = max(m_max + 4, m + 4)
        candidates = [x for x in range(2, hi + 1) if x % k != 0]
        if d >= 12 and candidates:
            # Bias toward larger non-multiples.
            floor = max(2, int(m_max * 0.35))
            preferred = [x for x in candidates if x >= floor]
            m = random.choice(preferred or candidates)
        elif candidates:
            m = random.choice(candidates)
        c = core_a * m
        missing = core_b * m
    else:
        c = a * m
        missing = b * m
    return a, b, c, missing


def _sci_exp_bounds(settings: dict) -> tuple[int, int]:
    lo, hi = _int_range(settings, "sci_exp_min", "sci_exp_max", lo_default=-8, hi_default=8)
    if not bool(settings.get("allow_negative_exponents", True)):
        lo = max(0, lo)
        hi = max(lo, hi)
    return lo, hi


def _sci_mantissa_decimals(settings: dict) -> int:
    return max(1, min(3, int(settings.get("mantissa_decimals", 1))))


def _random_sci_mantissa(settings: dict) -> float:
    """Return a mantissa in [1, 10) with the configured decimal places."""
    decimals = _sci_mantissa_decimals(settings)
    scale = 10**decimals
    # Integers from 1*scale .. 10*scale - 1 → [1.0, 10.0)
    return random.randint(scale, 10 * scale - 1) / scale


def _normalize_sci(mantissa: float, exponent: int) -> tuple[float, int]:
    if mantissa == 0:
        return 0.0, 0
    sign = 1 if mantissa > 0 else -1
    m = abs(mantissa)
    exp = exponent
    while m >= 10:
        m /= 10
        exp += 1
    while m < 1:
        m *= 10
        exp -= 1
    return sign * m, exp


def _format_sci_latex(mantissa: float, exponent: int) -> str:
    m, exp = _normalize_sci(mantissa, exponent)
    # Round to 6 significant figures to avoid float noise in answers.
    m_dec = Decimal(str(m)).normalize()
    # Quantize relative to magnitude: keep up to 6 significant digits.
    if m_dec == 0:
        return "0 \\times 10^{0}"
    sig = abs(m_dec)
    # Round to 6 significant figures via scientific quantization.
    rounded = float(f"{float(sig):.6g}")
    if m < 0:
        rounded = -rounded
    m_text = f"{rounded:g}"
    return f"{m_text} \\times 10^{{{exp}}}"


def _ordinary_number_latex(mantissa: float, exponent: int) -> str:
    """Plain decimal/integer form (avoids float for large |exponent|)."""
    value = Decimal(str(mantissa)) * (Decimal(10) ** exponent)
    text = format(value.normalize(), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _sci_exp_diff_bounds(settings: dict) -> tuple[int, int]:
    return _int_range(
        settings, "sci_exp_diff_min", "sci_exp_diff_max", lo_default=0, hi_default=0
    )


def _format_decimal(value: Decimal, *, places: int = 2) -> str:
    quantize = Decimal(10) ** -places
    normalized = value.quantize(quantize, rounding=ROUND_HALF_UP).normalize()
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _random_decimal(
    *,
    places: int = 1,
    minimum: float = 0.1,
    maximum: float = 99.9,
    allow_negative: bool = False,
) -> Decimal:
    scale = 10**places
    low = int(minimum * scale)
    high = int(maximum * scale)
    value = random.randint(low, high) / scale
    if allow_negative and random.choice([True, False]):
        value = -value
    return Decimal(str(value)).quantize(Decimal(10) ** -places)


class NumberFramework(QuestionFramework):
    """Shared batch generation for numeric expression types."""


class RationalFramework(NumberFramework):
    """Adding/subtracting/multiplying/dividing rational numbers."""

    def __init__(self, operation: str = "+"):
        self.operation = operation

    def _random_fraction(self, params: NumberParams) -> Fraction:
        return random_fraction(
            num_min=params.num_min,
            num_max=params.num_max,
            denom_min=params.denom_min,
            denom_max=params.denom_max,
            allow_negative=params.allow_negative,
            require_proper=params.require_proper,
            allow_mixed=params.allow_mixed,
        )

    def _format_operand(self, value: Fraction, params: NumberParams) -> str:
        # Mixed display only when enabled and the value is improper.
        show_mixed = params.allow_mixed and abs(value.numerator) > value.denominator
        return frac_or_mixed_latex(value, allow_mixed=show_mixed)

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        a = self._random_fraction(params)
        b = self._random_fraction(params)
        if self.operation == "/":
            while b == 0:
                b = self._random_fraction(params)

        op = self._resolve_operation()
        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }
        result = ops[op](a, b)
        if op == "/":
            notation = random.choice(allowed_division_notations(settings))
            prompt_latex = format_fraction_division_latex(a, b, notation)
        else:
            latex_op = {"+": "+", "-": "-", "*": "\\cdot"}[op]
            prompt_latex = format_binop_expression(
                self._format_operand(a, params),
                latex_op,
                self._format_operand(b, params),
            )
        prompt_text = normalize_expression_signs(f"{a} {op} {b}")
        return prompt_latex, prompt_text, frac_latex(result)


# Mental-math percents for Easy; Medium sticks to multiples of 5 when possible.
_EASY_PERCENTS = (5, 10, 20, 25, 40, 50, 75)
_MEDIUM_PERCENTS = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80)


def _difficulty_band(settings: dict) -> str:
    """Map continuous ``difficulty`` / EMH tier to easy|medium|hard."""
    from question_engine.frameworks.difficulty_budget import settings_difficulty_band

    return settings_difficulty_band(settings, default=8.0)


def _percent_difficulty_tier(settings: dict) -> str:
    return _difficulty_band(settings)


def _percent_step_for_exact(percent: int | float) -> int:
    """Smallest whole-step so ``whole * percent / 100`` is an integer."""
    pct = Fraction(percent).limit_denominator(1000)
    # whole * (pct/100) ∈ ℤ  ⇒  whole * pct.numerator / (100 * pct.denominator) ∈ ℤ
    denom = 100 * pct.denominator // math.gcd(pct.numerator, 100 * pct.denominator)
    return max(1, denom)


def _pick_exact_whole(
    percent: int | float,
    base_lo: int,
    base_hi: int,
    *,
    prefer_nice: bool = False,
) -> int:
    step = _percent_step_for_exact(percent)
    start = ((base_lo + step - 1) // step) * step
    if start < step:
        start = step
    candidates = list(range(start, base_hi + 1, step))
    if not candidates:
        # Fall back outside the requested band rather than invent an inconsistent triple.
        return max(step, (base_lo // step + 1) * step)
    if prefer_nice:
        nice = [w for w in candidates if w % 10 == 0 or w % 25 == 0]
        if nice:
            return random.choice(nice)
    return random.choice(candidates)


def _exact_part(whole: int, percent: int | float) -> int | float:
    value = Fraction(whole) * Fraction(percent) / 100
    if value.denominator == 1:
        return int(value)
    return float(value)


def _pick_percent_value(
    settings: dict,
    *,
    pct_lo: int,
    pct_hi: int,
    allow_decimal_pct: bool,
    prefer_exact: bool,
) -> int | float:
    tier = _percent_difficulty_tier(settings)
    if tier == "easy" or prefer_exact:
        pool = [p for p in _EASY_PERCENTS if pct_lo <= p <= pct_hi]
        if not pool:
            pool = [p for p in _EASY_PERCENTS if p <= max(pct_hi, 50)] or list(_EASY_PERCENTS)
        return random.choice(pool)
    if tier == "medium" or not allow_decimal_pct:
        pool = [p for p in _MEDIUM_PERCENTS if pct_lo <= p <= pct_hi]
        if pool:
            return random.choice(pool)
        return random.randint(pct_lo, pct_hi)
    # Hard + decimal percents: still prefer tenths that admit exact parts.
    if allow_decimal_pct and random.random() < 0.5:
        return round(random.uniform(pct_lo, pct_hi), 1)
    return random.randint(pct_lo, pct_hi)


def _format_percent_answer(settings: dict, percent: int | float, *, round_whole: bool) -> str:
    from ..settings.enrichment import format_answer_value

    return format_answer_value(
        {**settings, "round_answers_to_whole": round_whole},
        percent,
    )


def _soft_fail_independent_percent(part: int | float, whole: int, keyed_percent: int | float) -> None:
    """Reject the legacy bug: keying a percent chosen independently of part÷whole.

    Construction should make this a no-op. If it fires, part/whole and the keyed
    percent disagree (beyond float noise) — the old ``whole * pct // 100`` path.
    """
    if whole == 0:
        raise ValueError("percent whole must be nonzero")
    actual = Fraction(part) * 100 / Fraction(whole)
    keyed = Fraction(keyed_percent).limit_denominator(1000)
    if abs(float(actual - keyed)) > 1e-9:
        raise ValueError(
            f"inconsistent percent triple: {part} / {whole} = {float(actual)}%, "
            f"keyed {float(keyed)}% (choose percent+whole, then part)"
        )


class PercentFramework(NumberFramework):
    """Percent-of, find-percent, and percent-change prompts."""

    def __init__(self, *, percent_change: bool = False):
        self.percent_change = percent_change

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from ..settings.enrichment import format_answer_value

        pct_lo, pct_hi = _int_range(
            settings, "percent_min", "percent_max", lo_default=5, hi_default=75
        )
        base_lo, base_hi = _int_range(
            settings, "base_min", "base_max", lo_default=10, hi_default=200
        )
        round_whole = bool(settings.get("round_to_whole", settings.get("round_answers_to_whole", False)))
        allow_decimal_pct = bool(settings.get("allow_decimal_percents", False))
        tier = _percent_difficulty_tier(settings)
        # Easy / round-to-whole: keep mental-math exact triples (no invented rounding).
        prefer_exact = round_whole or tier == "easy" or not allow_decimal_pct
        prefer_nice = tier == "easy"

        if self.percent_change:
            percent = _pick_percent_value(
                settings,
                pct_lo=pct_lo,
                pct_hi=pct_hi,
                allow_decimal_pct=allow_decimal_pct,
                prefer_exact=prefer_exact,
            )
            original = _pick_exact_whole(
                percent, base_lo, base_hi, prefer_nice=prefer_nice
            )
            change = _exact_part(original, percent)
            if isinstance(change, float):
                change = int(round(change)) if round_whole else change
            if change == 0:
                change = max(1, int(original * Fraction(percent) / 100) or 1)
            increased = random.choice([True, False])
            new_value = original + change if increased else original - change
            if new_value <= 0:
                increased = True
                new_value = original + change
            # Answer from the actual change, never an independently chosen percent.
            actual_pct = Fraction(abs(change)) * 100 / Fraction(original)
            pct_value: int | float = (
                int(actual_pct) if actual_pct.denominator == 1 else float(actual_pct)
            )
            if round_whole and actual_pct.denominator != 1:
                pct_value = int(round(float(actual_pct)))
            direction = "increase" if increased else "decrease"
            prompt = f"\\text{{From {original} to {new_value}, find the percent {direction}.}}"
            answer_value = _format_percent_answer(settings, pct_value, round_whole=round_whole)
            return prompt, f"From {original} to {new_value}", f"{answer_value}\\%"

        mode = random.choice(["percent_of", "find_percent", "find_whole"])
        percent = _pick_percent_value(
            settings,
            pct_lo=pct_lo,
            pct_hi=pct_hi,
            allow_decimal_pct=allow_decimal_pct,
            prefer_exact=prefer_exact,
        )

        if mode == "percent_of":
            if prefer_exact:
                base = _pick_exact_whole(
                    percent, base_lo, base_hi, prefer_nice=prefer_nice
                )
            else:
                base = random.randint(base_lo, base_hi)
            result = Fraction(percent) * base / 100
            if prefer_exact and result.denominator != 1:
                base = _pick_exact_whole(
                    percent, base_lo, base_hi, prefer_nice=prefer_nice
                )
                result = Fraction(percent) * base / 100
            result_value: int | float = int(result) if result.denominator == 1 else float(result)
            if round_whole and result.denominator != 1:
                result_value = int(round(float(result)))
            prompt = f"\\text{{What is {percent}\\% of {base}?}}"
            answer = format_answer_value(
                {**settings, "round_answers_to_whole": round_whole},
                result_value,
            )
            return prompt, f"What is {percent}% of {base}?", answer

        if mode == "find_percent":
            # Choose percent + whole, then part = whole * percent / 100 (exact on Easy).
            whole = _pick_exact_whole(
                percent, base_lo, base_hi, prefer_nice=prefer_nice
            )
            part = _exact_part(whole, percent)
            if part == 0:
                whole = _pick_exact_whole(
                    percent,
                    max(base_lo, 20),
                    max(base_hi, 100),
                    prefer_nice=prefer_nice,
                )
                part = _exact_part(whole, percent)
            _soft_fail_independent_percent(part, whole, percent)
            prompt = f"\\text{{{part} is what percent of {whole}?}}"
            pct_answer = _format_percent_answer(settings, percent, round_whole=False)
            return prompt, f"{part} is what percent of {whole}?", f"{pct_answer}\\%"

        # find_whole: choose percent + part so whole = part * 100 / percent is exact.
        part_lo = max(1, base_lo // 10)
        part_hi = max(part_lo, min(60, base_hi // 3 or 60))
        if prefer_exact:
            # part must be a multiple of percent / gcd(percent, 100) so whole is integer.
            pct_frac = Fraction(percent).limit_denominator(1000)
            part_step = max(1, pct_frac.numerator // math.gcd(pct_frac.numerator, 100 * pct_frac.denominator))
            start = ((part_lo + part_step - 1) // part_step) * part_step
            if start == 0:
                start = part_step
            part_choices = list(range(start, part_hi + 1, part_step))
            if not part_choices:
                part_choices = [part_step]
            part = random.choice(part_choices)
            whole_frac = Fraction(part) * 100 / pct_frac
            result_value = int(whole_frac) if whole_frac.denominator == 1 else float(whole_frac)
        else:
            part = random.randint(part_lo, part_hi)
            whole_frac = Fraction(part) * 100 / Fraction(percent)
            result_value = int(whole_frac) if whole_frac.denominator == 1 else float(whole_frac)
            if round_whole and whole_frac.denominator != 1:
                result_value = int(round(float(whole_frac)))
        prompt = f"\\text{{{part} is {percent}\\% of what number?}}"
        answer = format_answer_value(
            {**settings, "round_answers_to_whole": round_whole},
            result_value,
        )
        return prompt, f"{part} is {percent}% of what number?", answer


class RatioFramework(NumberFramework):
    """Introduction to ratios and equivalent-ratio prompts."""

    def __init__(self, *, equivalent: bool = False):
        self.equivalent = equivalent

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.equivalent:
            a, b, c, missing = _sample_equivalent_ratio_missing(settings)
            form = random.choice(["colon", "fraction"])
            if form == "colon":
                prompt = f"\\text{{Find the missing value: }} {a}:{b} = {c}:x"
            else:
                prompt = f"\\frac{{{a}}}{{{b}}} = \\frac{{{c}}}{{x}}"
            return prompt, f"{a}:{b} = {c}:x", str(missing)

        a, b = _sample_shown_ratio_parts(settings)
        context = random.choice(["marbles", "apples", "books", "stickers"])
        color_a = random.choice(["red", "blue", "green"])
        color_b = random.choice(["yellow", "orange", "purple"])
        while color_b == color_a:
            color_b = random.choice(["yellow", "orange", "purple"])

        g = math.gcd(a, b)
        form = "word"
        if "difficulty" in settings and settings["difficulty"] is not None:
            from question_engine.frameworks.difficulty_budget import settings_difficulty

            d = max(0.0, settings_difficulty(settings, default=0.0))
            # Hardness is simplification: prefer simplest-form asks when unreduced
            # or once D leaves the introductory band.
            if g > 1 or d >= 6:
                form = "fraction" if random.random() < 0.8 else "word"
            else:
                form = random.choice(["word", "fraction"])
        else:
            form = random.choice(["word", "fraction"])

        if form == "word":
            prompt = (
                f"\\text{{There are {a} {color_a} {context} and {b} {color_b} {context}. "
                f"Write the ratio of {color_a} to {color_b}.}}"
            )
            answer = f"{a}:{b}"
        else:
            prompt = (
                f"\\text{{Write the ratio }} {a}:{b} "
                f"\\text{{ as a fraction in simplest form.}}"
            )
            answer = frac_latex(Fraction(a, b))
        return prompt, f"ratio {a} to {b}", answer


class UnitRateFramework(NumberFramework):
    """Unit rates and equivalent rates (factors-first under continuous D)."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        has_continuous = "difficulty" in settings and settings["difficulty"] is not None
        d = settings_difficulty(settings, default=0.0) if has_continuous else 0.0
        # Mix: low D mostly find-unit-rate; higher D more equivalent-rate scales.
        if has_continuous:
            equiv_p = 0.25 if d < 5 else (0.4 if d < 15 else 0.55)
            mode = "equivalent" if random.random() < equiv_p else "unit"
        else:
            mode = "unit"

        kind = random.choice(["speed", "reading rate", "unit price"])

        if mode == "equivalent":
            total1, q1, total2, q2 = _sample_equivalent_rate_pair(settings)
            if kind == "unit price":
                prompt = (
                    f"\\text{{\\${total1} for {q1} pounds of fruit. "
                    f"At the same rate, how much for {q2} pounds?}}"
                )
                return prompt, "equivalent rate (unit price)", f"\\${total2}"
            scenarios = {
                "speed": ("miles", "hours", "A car travels"),
                "reading rate": ("pages", "minutes", "A student reads"),
            }
            quantity, unit, subject = scenarios[kind]
            prompt = (
                f"\\text{{{subject} {total1} {quantity} in {q1} {unit}. "
                f"At the same rate, how many {quantity} in {q2} {unit}?}}"
            )
            return prompt, f"equivalent rate ({kind})", str(total2)

        rate, multiplier = _sample_unit_rate_core_and_qty(settings)
        if kind == "unit price":
            pounds = multiplier
            total_cost = rate * pounds
            prompt = (
                f"\\text{{\\${total_cost} for {pounds} pounds of fruit. "
                f"Find the unit price in dollars per pound.}}"
            )
            return prompt, "unit price", f"\\${rate}"

        scenarios = {
            "speed": ("miles", "hours", "A car travels"),
            "reading rate": ("pages", "minutes", "A student reads"),
        }
        quantity, unit, subject = scenarios[kind]
        total = rate * multiplier
        unit_singular = unit[:-1] if unit.endswith("s") else unit
        prompt = (
            f"\\text{{{subject} {total} {quantity} in {multiplier} {unit}. "
            f"Find the unit rate in {quantity} per {unit_singular}.}}"
        )
        return prompt, f"unit rate ({kind})", str(rate)


_COMPARE_RATE_NAMES = (
    "Daniel",
    "Julio",
    "Mary",
    "Stefan",
    "Ava",
    "Liam",
    "Sofia",
    "Noah",
    "Maya",
    "Ethan",
    "Priya",
    "Omar",
)

_COMPARE_RATE_FOODS = (
    "almonds",
    "apples",
    "coffee",
    "cheese",
    "grapes",
    "rice",
)


def _dnl_tick_values(top: int, bottom: int, multiples: int) -> tuple[list[int], list[int]]:
    """Tick labels 0..k for a rate of ``top`` per ``bottom``."""
    k = max(1, int(multiples))
    return [top * i for i in range(k + 1)], [bottom * i for i in range(k + 1)]


def _common_dnl_multiples(
    top1: int,
    bottom1: int,
    top2: int,
    bottom2: int,
    *,
    max_steps: int,
) -> tuple[int, int] | None:
    """Return (k1, k2) so both DNLs meet on a shared bottom value, if small enough."""
    try:
        common = math.lcm(bottom1, bottom2)
    except AttributeError:  # pragma: no cover — py<3.9 fallback
        common = bottom1 * bottom2 // math.gcd(bottom1, bottom2)
    k1 = common // bottom1
    k2 = common // bottom2
    if k1 <= max_steps and k2 <= max_steps:
        return k1, k2
    return None


def _sample_one_comparing_rate(
    d: float,
    *,
    core_hi: int,
    k_max: int,
    prefer_unit_qty: bool,
) -> tuple[int, int]:
    """Factors-first ``(top, bottom)`` for one person's given rate.

    Low D: small cores; often a unit quantity on the bottom.
    Mid/high D: non-unit bottoms inflated by a composite GCF ``k`` that grows
    unboundedly with continuous difficulty (same spirit as unit rates / ratios).
    """
    core_hi = max(2, int(core_hi))
    k_max = max(1, int(k_max))

    if d < 8:
        # Small friendly cores; often already a unit quantity.
        for _ in range(30):
            num = random.randint(2, min(6, core_hi))
            if prefer_unit_qty and random.random() < 0.7:
                den = 1
                k = 1 if random.random() < 0.7 else random.randint(2, min(3, k_max))
            else:
                den = random.choice([1, 2, 3, 4])
                k = random.randint(1, min(5, k_max))
            g = math.gcd(num, den)
            cn, cd = num // g, den // g
            # Keep reduced unit-rate ≥ 2 (avoid "$1 for 1 pound").
            if cn >= 2:
                return cn * k, cd * k
        return 2, 1

    # Mid / high: simplified core a/b with b≥2, then × composite inflate-k.
    den_hi = max(2, min(core_hi, int(4 + 0.2 * d)))
    num, den = 5, 3
    for _ in range(40):
        n = random.randint(2, core_hi)
        b = random.randint(2, den_hi)
        if math.gcd(n, b) == 1:
            num, den = n, b
            break

    if d < 12:
        k = _sample_ratio_inflate_k(d, min(k_max, 10), min_k=2)
    else:
        k = _sample_ratio_inflate_k(d, k_max, min_k=2)
    return num * k, den * k


def _sample_comparing_rate_amounts(
    settings: dict,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Two (top, bottom) amount pairs with distinct unit rates, scaled by D.

    Continuous ``difficulty`` drives core rate size and inflate-k unboundedly
    (no soft cap at D≈18). Legacy EMH / missing difficulty keeps a small pool.
    """
    has_continuous = "difficulty" in settings and settings["difficulty"] is not None
    if not has_continuous:
        # Legacy EMH: small pedagogical pool from unit_rate_* presets.
        rate_lo, rate_hi, mult_lo, mult_hi = _unit_rate_bounds(settings)
        for _ in range(40):
            r1 = random.randint(rate_lo, rate_hi)
            r2 = random.randint(rate_lo, rate_hi)
            if r1 == r2:
                continue
            m1 = random.randint(mult_lo, mult_hi)
            m2 = random.randint(mult_lo, mult_hi)
            # Occasionally keep one as a unit quantity on easy presets.
            if mult_lo <= 1 and random.random() < 0.4:
                m1 = 1
            t1, b1 = r1 * m1, m1
            t2, b2 = r2 * m2, m2
            if (t1, b1) != (t2, b2):
                return (t1, b1), (t2, b2)
        return (2, 1), (9, 4)

    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    core_hi = continuous_unit_rate_core_max(settings) or 4
    k_max = continuous_unit_rate_qty_max(settings) or 2

    for _ in range(80):
        # At low D, bias the first person toward a unit quantity.
        t1, b1 = _sample_one_comparing_rate(
            d, core_hi=core_hi, k_max=k_max, prefer_unit_qty=(d < 8)
        )
        t2, b2 = _sample_one_comparing_rate(
            d, core_hi=core_hi, k_max=k_max, prefer_unit_qty=False
        )
        if b1 <= 0 or b2 <= 0 or t1 <= 0 or t2 <= 0:
            continue
        if Fraction(t1, b1) == Fraction(t2, b2):
            continue
        if (t1, b1) == (t2, b2):
            continue
        # High D: never ship "unit quantity = 1" friendly cases.
        if d >= 12 and (b1 == 1 or b2 == 1):
            continue
        return (t1, b1), (t2, b2)

    # Deterministic pedagogical fallback (Daniel $2/lb vs Julio $9/4 lb).
    return (2, 1), (9, 4)


class ComparingRatesFramework(NumberFramework):
    """Compare two rates (unit price / speed) with double-number-line stimuli."""

    def __init__(self) -> None:
        self._metadata: dict[str, object] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        from ..diagrams.grade6_figures import comparing_rates_double_number_lines_svg

        d = max(0.0, settings_difficulty(settings, default=8.0))
        name1, name2 = random.sample(_COMPARE_RATE_NAMES, 2)
        kind = random.choice(["unit_price", "speed"])
        ask_higher = random.choice([True, False])
        (t1, b1), (t2, b2) = _sample_comparing_rate_amounts(settings)

        rate1 = Fraction(t1, b1)
        rate2 = Fraction(t2, b2)
        if ask_higher:
            winner = name1 if rate1 > rate2 else name2
        else:
            winner = name1 if rate1 < rate2 else name2

        if kind == "unit_price":
            food = random.choice(_COMPARE_RATE_FOODS)

            def _lb_phrase(n: int) -> str:
                return f"{n} pound" if n == 1 else f"{n} pounds"

            q = (
                "Who paid the higher unit price?"
                if ask_higher
                else "Who paid the lower unit price?"
            )
            prompt = (
                f"\\text{{{name1} paid \\${t1} for {_lb_phrase(b1)} of {food}. "
                f"{name2} paid \\${t2} for {_lb_phrase(b2)} of {food}. {q}}}"
            )
            text = (
                f"{name1} paid ${t1} for {_lb_phrase(b1)} of {food}. "
                f"{name2} paid ${t2} for {_lb_phrase(b2)} of {food}. {q}"
            )
            top_label, bottom_label = "dollars", "pounds"
        else:
            q = "Whose car went faster?" if ask_higher else "Whose car went slower?"
            prompt = (
                f"\\text{{{name1}'s car went {t1} miles in {b1} minutes. "
                f"{name2}'s car went {t2} miles in {b2} minutes. {q}}}"
            )
            text = (
                f"{name1}'s car went {t1} miles in {b1} minutes. "
                f"{name2}'s car went {t2} miles in {b2} minutes. {q}"
            )
            top_label, bottom_label = "miles", "minutes"

        # Extend DNLs toward a shared bottom value when the LCM is small enough.
        # At high D amounts are huge — keep given-amount ticks only.
        amount_hi = max(t1, b1, t2, b2)
        if d < 8:
            max_steps = 5
        elif d < 18 and amount_hi <= 80:
            max_steps = 6
        elif d < 40 and amount_hi <= 120:
            max_steps = 8
        else:
            max_steps = 1
        common = _common_dnl_multiples(t1, b1, t2, b2, max_steps=max_steps)
        if common is not None:
            k1, k2 = common
        else:
            # Short independent lines: given amount only, or 2–3 multiples on easy.
            k1 = 1 if d >= 8 else min(4, max(1, 4 // max(1, b1)))
            k2 = 1 if d >= 8 else min(4, max(1, 4 // max(1, b2)))
            k1 = max(1, k1)
            k2 = max(1, k2)

        tops1, bots1 = _dnl_tick_values(t1, b1, k1)
        tops2, bots2 = _dnl_tick_values(t2, b2, k2)

        self._metadata = {
            "diagram_svg": comparing_rates_double_number_lines_svg(
                {
                    "title": name1,
                    "top_label": top_label,
                    "bottom_label": bottom_label,
                    "top_values": tops1,
                    "bottom_values": bots1,
                },
                {
                    "title": name2,
                    "top_label": top_label,
                    "bottom_label": bottom_label,
                    "top_values": tops2,
                    "bottom_values": bots2,
                },
            ),
            "stimulus_kind": "double_number_line",
            "compare_kind": kind,
            "rate_a": {"name": name1, "top": t1, "bottom": b1},
            "rate_b": {"name": name2, "top": t2, "bottom": b2},
        }
        answer = rf"\text{{{winner}}}"
        return prompt, text, answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        return dict(self._metadata)


# ---------------------------------------------------------------------------
# Unit conversion (metric / approximate customary) + double number line
# ---------------------------------------------------------------------------

_CONVERT_METRIC: tuple[dict[str, Any], ...] = (
    {
        "from_u": "mm",
        "to_u": "cm",
        "from_step": 10,
        "to_step": 1,
        "approx": False,
        "band": "easy",
        "scenarios": (
            ("Frame", "A picture frame is {a} mm tall.", "How tall is the frame in cm?"),
            ("Ribbon", "A ribbon is {a} mm long.", "What is the length in cm?"),
            ("Beetle", "A beetle is {a} mm long.", "How long is the beetle in cm?"),
        ),
    },
    {
        "from_u": "cm",
        "to_u": "m",
        "from_step": 100,
        "to_step": 1,
        "approx": False,
        "band": "easy",
        "scenarios": (
            ("Rope", "A rope is {a} cm long.", "What is the length in m?"),
            ("Desk", "A desk is {a} cm wide.", "What is the width in m?"),
            ("Track", "A hallway is {a} cm long.", "What is the length in m?"),
        ),
    },
    {
        "from_u": "m",
        "to_u": "km",
        "from_step": 1000,
        "to_step": 1,
        "approx": False,
        "band": "mid",
        "scenarios": (
            ("Trail", "A trail is {a} m long.", "What is the length in km?"),
            ("Race", "A race is {a} m long.", "How long is the race in km?"),
            ("Road", "A road segment is {a} m long.", "What is the length in km?"),
        ),
    },
    {
        "from_u": "g",
        "to_u": "kg",
        "from_step": 1000,
        "to_step": 1,
        "approx": False,
        "band": "mid",
        "scenarios": (
            ("Bag", "A bag of flour has a mass of {a} g.", "What is the mass in kg?"),
            ("Package", "A package has a mass of {a} g.", "What is the mass in kg?"),
        ),
    },
    {
        "from_u": "mL",
        "to_u": "L",
        "from_step": 1000,
        "to_step": 1,
        "approx": False,
        "band": "mid",
        "scenarios": (
            ("Bottle", "A bottle holds {a} mL of water.", "How many liters is that?"),
            ("Jug", "A jug holds {a} mL of juice.", "How many liters is that?"),
        ),
    },
)

_CONVERT_APPROX: tuple[dict[str, Any], ...] = (
    {
        "from_u": "kg",
        "to_u": "pounds",
        "from_step": 10,
        "to_step": 22,
        "approx": True,
        "band": "hard",
        "scenarios": (
            ("Ball", "A bowling ball has a mass of {a} kg.", "What is the mass in pounds?"),
            ("Dog", "A dog has a mass of {a} kg.", "About how many pounds is that?"),
        ),
    },
    {
        "from_u": "km",
        "to_u": "miles",
        "from_step": 8,
        "to_step": 5,
        "approx": True,
        "band": "hard",
        "scenarios": (
            ("Drive", "A drive is {a} km long.", "About how many miles is that?"),
            ("Hike", "A hike is {a} km long.", "About how many miles is that?"),
        ),
    },
    {
        "from_u": "cm",
        "to_u": "inches",
        "from_step": 5,
        "to_step": 2,
        "approx": True,
        "band": "hard",
        "scenarios": (
            ("Board", "A board is {a} cm long.", "About how many inches is that?"),
            ("Photo", "A photo is {a} cm wide.", "About how many inches is that?"),
        ),
    },
    {
        "from_u": "liters",
        "to_u": "gallons",
        "from_step": 15,
        "to_step": 4,
        "approx": True,
        "band": "hard",
        "scenarios": (
            ("Tank", "A tank holds {a} liters of water.", "About how many gallons is that?"),
            ("Bucket", "A bucket holds {a} liters.", "About how many gallons is that?"),
        ),
    },
    {
        "from_u": "meters",
        "to_u": "feet",
        "from_step": 5,
        "to_step": 16,
        "approx": True,
        "band": "hard",
        "scenarios": (
            ("Fence", "A fence is {a} meters long.", "About how many feet is that?"),
            ("Pool", "A pool is {a} meters long.", "About how many feet is that?"),
        ),
    },
)


def _convert_tick_pair(
    from_step: int,
    to_step: int,
    amount: int,
    *,
    max_ticks: int = 9,
) -> tuple[list[int | float], list[int | float]]:
    """Build paired DNL tick labels covering the given amount (and rate fact)."""
    f_step = int(from_step)
    t_step = int(to_step)
    amt = int(amount)
    if f_step <= 0 or t_step <= 0 or amt <= 0:
        return [0, amt], [0, float(Fraction(amt * t_step, f_step))]

    # Prefer a fine tick that hits both the conversion fact and the given amount.
    end = max(amt, f_step)
    g = math.gcd(amt, f_step) if amt else f_step
    if g > 0 and (t_step * g) % f_step == 0:
        ft = g
        tt = (t_step * g) // f_step
        n = end // ft
        if tt > 0 and n >= 1 and n + 1 <= max_ticks:
            return [ft * i for i in range(n + 1)], [tt * i for i in range(n + 1)]
        if tt > 0 and n + 1 > max_ticks:
            step_n = max(1, math.ceil(n / (max_ticks - 1)))
            idxs = list(range(0, n, step_n))
            if idxs[-1] != n:
                idxs.append(n)
            # Ensure the given amount appears when it lands on the fine grid.
            amt_idx = amt // ft
            if amt % ft == 0 and amt_idx not in idxs:
                idxs.append(amt_idx)
                idxs.sort()
            return [ft * i for i in idxs], [tt * i for i in idxs]

    if amt % f_step == 0:
        n = amt // f_step
        if 1 <= n and n + 1 <= max_ticks:
            return [f_step * i for i in range(n + 1)], [t_step * i for i in range(n + 1)]

    ans = Fraction(amt * t_step, f_step)
    ans_disp: int | float = int(ans) if ans.denominator == 1 else float(ans)
    if amt < f_step:
        return [0, amt, f_step], [0, ans_disp, t_step]
    if amt == f_step:
        return [0, f_step], [0, t_step]
    return [0, f_step, amt], [0, t_step, ans_disp]


def _format_convert_answer(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    places = _terminating_decimal_places(value)
    if places is not None and places <= 2:
        return _exact_terminating_decimal(value)
    return frac_latex(value)


def _convert_multiples_hi(d: float) -> int:
    """Max conversion-fact multiples; polynomial growth (no soft asymptote).

    Same spirit as ``continuous_ratio_inflate_max`` / ``continuous_abs_max``:
    D≈0 → a few steps, D≈40 → hard-but-doable dozens, D=1000 → absurd.
    """
    d = max(0.0, float(d))
    return max(2, int(3 + 0.4 * d + 0.02 * d * d))


def _sample_convert_amount(from_step: int, d: float, *, allow_partial: bool) -> int:
    """Choose a starting amount in the from-unit, scaled by difficulty."""
    f = max(1, int(from_step))
    n_hi = _convert_multiples_hi(d)
    if d < 6:
        n_lo, n_hi = 2, min(5, n_hi)
        allow_partial = False
    elif d < 14:
        n_lo, n_hi = 2, min(8, n_hi)
        allow_partial = False
    elif d < 24:
        n_lo = 2
    else:
        # High D: stay in the large-magnitude band (no collapse to ½-step alone).
        n_lo = max(2, n_hi // 5)

    n = random.randint(n_lo, max(n_lo, n_hi))
    partial_p = 0.35 if d < 24 else 0.55
    if allow_partial and random.random() < partial_p:
        # Off-multiple of the conversion fact, same order of magnitude as n·f.
        if f % 2 == 0:
            return max(1, (2 * n - 1) * (f // 2))  # (n − ½)·f
        if f % 5 == 0:
            return max(1, (5 * n - 2) * (f // 5))
        if f % 4 == 0:
            return max(1, (4 * n - 1) * (f // 4))
    return n * f


class ConvertingUnitsFramework(NumberFramework):
    """Unit conversion word problems with a given equivalence + DNL stimulus."""

    def __init__(self) -> None:
        self._metadata: dict[str, object] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        from ..diagrams.grade6_figures import double_number_line_svg

        d = max(0.0, settings_difficulty(settings, default=0.0))
        if d < 6:
            pool = [c for c in _CONVERT_METRIC if c["band"] == "easy"]
            allow_partial = False
            max_ticks = 6
        elif d < 14:
            pool = list(_CONVERT_METRIC)
            allow_partial = False
            max_ticks = 8
        elif d < 24:
            pool = list(_CONVERT_METRIC) + list(_CONVERT_APPROX)
            allow_partial = True
            max_ticks = 8
        else:
            # Prefer messier approximate rates; keep some metric large-scale.
            pool = list(_CONVERT_APPROX) + [
                c for c in _CONVERT_METRIC if c["band"] == "mid"
            ]
            allow_partial = True
            max_ticks = 9

        conv = random.choice(pool)
        from_u = str(conv["from_u"])
        to_u = str(conv["to_u"])
        from_step = int(conv["from_step"])
        to_step = int(conv["to_step"])
        approx = bool(conv["approx"])
        title, stem, question = random.choice(conv["scenarios"])
        amount = _sample_convert_amount(from_step, d, allow_partial=allow_partial and approx)
        # Guard: answer should be positive and representable.
        answer_val = Fraction(amount * to_step, from_step)
        if answer_val <= 0:
            amount = from_step
            answer_val = Fraction(to_step)

        tops, bots = _convert_tick_pair(
            from_step, to_step, amount, max_ticks=max_ticks
        )
        # Prefer integer tick labels when possible.
        top_labels = [int(v) if float(v) == int(v) else v for v in tops]
        bot_labels: list[int | float | str] = []
        for v in bots:
            if isinstance(v, float) and not v.is_integer():
                bot_labels.append(v)
            else:
                bot_labels.append(int(v))

        stem_filled = stem.format(a=amount)
        eq_sym = "≈" if approx else "="
        given = f"{from_step} {from_u} {eq_sym} {to_step} {to_u}"
        if approx:
            prompt = (
                f"\\text{{{stem_filled} Given that {from_step} {from_u} }}"
                f"\\approx\\text{{ {to_step} {to_u}. {question}}}"
            )
        else:
            prompt = (
                f"\\text{{{stem_filled} Given that {from_step} {from_u} $=$ "
                f"{to_step} {to_u}. {question}}}"
            )
        text = f"{stem_filled} Given that {given}. {question}"
        answer = _format_convert_answer(answer_val)

        self._metadata = {
            "diagram_svg": double_number_line_svg(
                title=str(title),
                top_label=from_u,
                bottom_label=to_u,
                top_values=top_labels,
                bottom_values=bot_labels,
            ),
            "stimulus_kind": "double_number_line",
            "double_number_line_spec": {
                "title": title,
                "top": {"unit": from_u, "values": top_labels},
                "bottom": {"unit": to_u, "values": bot_labels},
            },
            "conversion": {
                "from_unit": from_u,
                "to_unit": to_u,
                "from_step": from_step,
                "to_step": to_step,
                "amount": amount,
                "approx": approx,
            },
        }
        return prompt, text, answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        return dict(self._metadata)


def _terminating_decimal_places(frac: Fraction) -> int | None:
    """Places needed for an exact decimal, or None if the decimal repeats."""
    denom = frac.denominator
    twos = fives = 0
    while denom % 2 == 0:
        denom //= 2
        twos += 1
    while denom % 5 == 0:
        denom //= 5
        fives += 1
    if denom != 1:
        return None
    return max(twos, fives)


def _exact_terminating_decimal(frac: Fraction) -> str:
    """Format a terminating fraction as an exact decimal string (no rounding)."""
    places = _terminating_decimal_places(frac)
    if places is None:
        raise ValueError(f"non-terminating fraction: {frac}")
    if places == 0:
        return str(frac.numerator // frac.denominator)
    quantized = (Decimal(frac.numerator) / Decimal(frac.denominator)).quantize(
        Decimal(10) ** -places
    )
    text = format(quantized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


class DecimalArithmeticFramework(NumberFramework):
    """Decimal addition, subtraction, multiplication, and division."""

    def __init__(self, operation: str = "+"):
        self.operation = operation

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        places = int(settings.get("decimal_places", 2))
        allow_negative = bool(settings.get("allow_negative", False))
        minimum = 0.1 if not allow_negative else -99.9
        a_places = places
        b_places = places
        a = _random_decimal(places=places, minimum=minimum, maximum=99.9, allow_negative=allow_negative)
        b = _random_decimal(places=places, minimum=minimum, maximum=99.9, allow_negative=allow_negative)
        if self.operation == "-":
            if not allow_negative:
                while b > a:
                    b = _random_decimal(places=places, minimum=0.1, maximum=float(a))
            elif random.choice([True, False]):
                while b > a:
                    a, b = b, a
        if self.operation == "*":
            a, b, a_places, b_places = self._multiplication_factors(settings)
        if self.operation == "/":
            divisor = random.randint(2, 9)
            quotient = _random_decimal(places=places, minimum=0.5, maximum=9.5)
            a = (quotient * Decimal(divisor)).quantize(Decimal(10) ** -places)
            b = Decimal(divisor)
            b_places = 0

        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }
        result = ops[self.operation](a, b)
        latex_op = {"+": "+", "-": "-", "*": "\\cdot", "/": "\\div"}[self.operation]
        answer_places = a_places + b_places if self.operation == "*" else places
        prompt_latex = format_binop_expression(
            _format_decimal(a, places=a_places),
            latex_op,
            _format_decimal(b, places=b_places),
        )
        prompt_text = format_binop_expression(
            _format_decimal(a, places=a_places),
            self.operation,
            _format_decimal(b, places=b_places),
        )
        return prompt_latex, prompt_text, _format_decimal(result, places=answer_places)

    def _multiplication_factors(
        self, settings: dict
    ) -> tuple[Decimal, Decimal, int, int]:
        """Build multiplication factors shaped by difficulty settings.

        - whole_times_decimal: whole number × decimal (tenths when decimal_places=1)
        - otherwise both factors are decimals with 1..max_decimal_places places
        """
        places = max(1, int(settings.get("decimal_places", 2)))
        max_places = max(1, int(settings.get("max_decimal_places", places)))
        allow_negative = bool(settings.get("allow_negative", False))
        whole_times = bool(settings.get("whole_times_decimal", False))

        def fractional_decimal(factor_places: int) -> Decimal:
            while True:
                value = _random_decimal(
                    places=factor_places,
                    minimum=0.1,
                    maximum=9.9,
                    allow_negative=False,
                )
                if value != value.to_integral_value():
                    if allow_negative and random.choice([True, False]):
                        value = -value
                    return value

        if whole_times:
            whole = Decimal(random.randint(2, 20))
            decimal_places = min(places, max_places)
            # Tenths-only easy items look like 7 × 0.3, not 17 × 7.5.
            while True:
                decimal = _random_decimal(
                    places=decimal_places,
                    minimum=0.1,
                    maximum=0.9 if decimal_places == 1 else 9.9,
                    allow_negative=False,
                )
                if decimal != decimal.to_integral_value():
                    break
            if allow_negative and random.choice([True, False]):
                whole = -whole
            # Prefer whole × decimal (matches grade-6 presentation).
            return whole, decimal, 0, decimal_places

        a_places = random.randint(1, max_places)
        b_places = random.randint(1, max_places)
        return fractional_decimal(a_places), fractional_decimal(b_places), a_places, b_places


class WholeDivideToDecimalFramework(NumberFramework):
    """Whole ÷ whole with a terminating non-integer decimal quotient."""

    _DIVISORS_BY_PLACES: dict[int, tuple[int, ...]] = {
        1: (2, 4, 5, 10),
        2: (4, 5, 8, 10, 16, 20, 25, 40, 50),
        3: (8, 16, 20, 25, 40, 50, 80, 100, 125, 200),
    }

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        places = max(1, min(3, int(settings.get("decimal_places", 2))))
        max_places = settings.get("max_decimal_places")
        if max_places is not None:
            places = max(1, min(places, int(max_places)))
        num_max = max(4, int(settings.get("num_max", 50)))
        dividend_hi = max(num_max, 10)
        divisors = [d for d in self._DIVISORS_BY_PLACES[places] if d <= max(num_max, 10)]
        if not divisors:
            divisors = list(self._DIVISORS_BY_PLACES[places])

        # Prefer quotients that use the full place budget on harder tiers.
        prefer_exact_places = places >= 2

        for _ in range(120):
            divisor = random.choice(divisors)
            dividend = random.randint(1, dividend_hi)
            if dividend % divisor == 0:
                continue
            frac = Fraction(dividend, divisor)
            needed = _terminating_decimal_places(frac)
            if needed is None or needed < 1 or needed > places:
                continue
            if prefer_exact_places and needed < places and random.random() < 0.65:
                continue
            answer = _exact_terminating_decimal(frac)
            prompt_latex = f"{dividend} \\div {divisor}"
            return prompt_latex, f"{dividend} / {divisor}", answer

        # Guaranteed terminating fallbacks by place budget.
        fallbacks = {1: (5, 2), 2: (7, 4), 3: (3, 8)}
        dividend, divisor = fallbacks[places]
        answer = _exact_terminating_decimal(Fraction(dividend, divisor))
        return f"{dividend} \\div {divisor}", f"{dividend} / {divisor}", answer


def _whole_by_decimal_ladder(settings: dict) -> dict[str, Any]:
    """Continuous-D / EMH controls for whole ÷ decimal."""
    from question_engine.frameworks.difficulty_budget import (
        settings_difficulty,
        settings_difficulty_band,
    )

    d = settings_difficulty(settings, default=0.0)
    band = settings_difficulty_band(settings, default=0.0)
    allow_negative = bool(settings.get("allow_negative", False))
    # Hard band (and high continuous D) unlocks signed operands.
    if band == "hard" or d >= 12.0 - 1e-9:
        allow_negative = bool(settings.get("allow_negative", True))

    divisor_ge_one_setting = settings.get("divisor_ge_one")
    if divisor_ge_one_setting is None:
        # Low D: only (0,1). Mid/high: unlock divisors ≥ 1.
        divisor_ge_one = band != "easy" and d > 4.0 + 1e-9
    else:
        divisor_ge_one = bool(divisor_ge_one_setting)

    places = max(1, min(3, int(settings.get("decimal_places", 1))))
    max_places = settings.get("max_decimal_places")
    if max_places is not None:
        places = max(1, min(places, int(max_places)))
    if band == "easy" or d <= 4.0 + 1e-9:
        places = 1
    elif band == "medium" or d <= 11.0 + 1e-9:
        places = max(places, 1)
        places = min(places, 2)
    else:
        places = max(places, 2)
        places = min(3, places)

    cont = continuous_abs_max(settings, base=16, floor=8)
    if cont is not None:
        # Floor high enough that tenths like 0.1 still have several quotients.
        quot_max = max(20, cont)
    else:
        quot_max = max(20, int(settings.get("num_max", 40)))

    return {
        "d": d,
        "band": band,
        "allow_negative": allow_negative,
        "divisor_ge_one": divisor_ge_one,
        "places": places,
        "quot_max": quot_max,
    }


# Friendly terminating decimal divisors (construct-backwards keeps whole dividends).
_WHOLE_BY_DEC_LT1_TENTHS: tuple[Decimal, ...] = tuple(
    Decimal(x) for x in ("0.1", "0.2", "0.4", "0.5", "0.8")
)
_WHOLE_BY_DEC_LT1_MID: tuple[Decimal, ...] = tuple(
    Decimal(x) for x in ("0.05", "0.16", "0.25", "0.4", "0.5", "0.75", "0.8")
)
_WHOLE_BY_DEC_GE1_MID: tuple[Decimal, ...] = tuple(
    Decimal(x)
    for x in ("1.2", "1.25", "1.5", "1.6", "2.4", "2.5", "3.2", "3.5", "4.5", "5.5")
)
_WHOLE_BY_DEC_LT1_HARD: tuple[Decimal, ...] = tuple(
    Decimal(x)
    for x in (
        "0.08",
        "0.125",
        "0.16",
        "0.25",
        "0.375",
        "0.4",
        "0.625",
        "0.75",
        "0.875",
    )
)
_WHOLE_BY_DEC_GE1_HARD: tuple[Decimal, ...] = tuple(
    Decimal(x)
    for x in (
        "1.25",
        "1.5",
        "1.6",
        "1.75",
        "2.4",
        "2.5",
        "2.75",
        "3.2",
        "3.75",
        "4.8",
        "5.25",
        "6.4",
        "7.5",
        "8.5",
        "12.5",
    )
)


def _divisor_pool(cfg: dict[str, Any], *, use_ge1: bool) -> tuple[Decimal, ...]:
    band = cfg["band"]
    if use_ge1:
        if band == "hard" or float(cfg["d"]) >= 12.0 - 1e-9:
            return _WHOLE_BY_DEC_GE1_HARD
        return _WHOLE_BY_DEC_GE1_MID
    if band == "easy" or float(cfg["d"]) <= 4.0 + 1e-9:
        return _WHOLE_BY_DEC_LT1_TENTHS
    if band == "hard" or float(cfg["d"]) >= 12.0 - 1e-9:
        return _WHOLE_BY_DEC_LT1_HARD
    return _WHOLE_BY_DEC_LT1_MID


def _compatible_integer_quotient_for_decimal(
    divisor: Decimal, quot_max: int
) -> tuple[int, int]:
    """Return (quotient, whole_dividend) for divisor × quotient = whole dividend."""
    frac = Fraction(divisor).limit_denominator(1000)
    # q * n / d ∈ ℤ with gcd(n,d)=1 ⇒ q multiple of d.
    step = frac.denominator
    max_mult = max(1, quot_max // step)
    # Prefer a spread of quotients, not only the minimum step.
    mult = random.randint(1, max_mult)
    quotient = mult * step
    dividend = quotient * frac.numerator // frac.denominator
    return quotient, dividend


class WholeByDecimalDivideFramework(NumberFramework):
    """Whole number ÷ non-integer decimal (construct quotient × divisor → dividend).

    Ladder:
    - Low D: divisor in (0, 1), tenths, positive, integer quotients
    - Mid D: unlocks divisors ≥ 1 (e.g. 1.2, 2.5) with terminating answers
    - High D: more places, larger magnitudes, signed dividends/divisors
    """

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        cfg = _whole_by_decimal_ladder(settings)
        quot_max = max(4, int(cfg["quot_max"]))
        allow_ge1 = bool(cfg["divisor_ge_one"])
        allow_negative = bool(cfg["allow_negative"])

        # At mid/high, bias toward ≥1 so the unlock is visible in samples.
        if allow_ge1:
            use_ge1 = random.random() < (0.55 if cfg["band"] == "medium" else 0.7)
        else:
            use_ge1 = False

        pool = _divisor_pool(cfg, use_ge1=use_ge1)
        divisor_pos = abs(random.choice(pool))
        _quotient, dividend = _compatible_integer_quotient_for_decimal(
            divisor_pos, quot_max
        )

        div_sign = d_sign = 1
        if allow_negative:
            mode = random.choices(
                ["none", "neg_dividend", "neg_divisor", "both_neg"],
                weights=[0.2, 0.3, 0.3, 0.2],
                k=1,
            )[0]
            if mode in ("neg_dividend", "both_neg"):
                div_sign = -1
            if mode in ("neg_divisor", "both_neg"):
                d_sign = -1

        signed_dividend = div_sign * dividend
        signed_divisor = d_sign * divisor_pos
        signed_q = Fraction(signed_dividend) / Fraction(signed_divisor)
        assert signed_q.denominator == 1

        places = max(1, int(cfg["places"]))
        # Display enough places for the chosen divisor (e.g. 0.125 needs 3).
        needed = _terminating_decimal_places(Fraction(divisor_pos)) or places
        disp_places = max(places, needed)

        a_s = _format_decimal(Decimal(signed_dividend), places=0)
        b_s = _format_decimal(Decimal(signed_divisor), places=disp_places)
        ans_s = _format_decimal(Decimal(signed_q.numerator), places=0)
        prompt_latex = format_binop_expression(a_s, "\\div", b_s)
        prompt_text = format_binop_expression(a_s, "/", b_s)
        return prompt_latex, prompt_text, ans_s


class DistributiveFramework(NumberFramework):
    """Numeric and simple algebraic distributive property."""

    def __init__(self, *, algebraic: bool = False):
        self.algebraic = algebraic

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        allow_negative = bool(settings.get("allow_negative", True))
        coef_lo = int(settings.get("coef_min", -9))
        coef_hi = int(settings.get("coef_max", 9))
        if not allow_negative:
            coef_lo = max(1, coef_lo)
            coef_hi = max(coef_lo, coef_hi)
        outer = random_int_range(min(coef_lo, coef_hi), max(coef_lo, coef_hi), exclude={0})
        inner_a = random.randint(1, 9)
        inner_b = random.randint(1, 9)
        op = random.choice(["+", "-"])

        if self.algebraic:
            inner = f"x {op} {inner_b}" if op == "+" else f"x - {inner_b}"
            prompt_latex = f"{outer}({inner})"
            if op == "+":
                answer = format_linear_latex(outer, outer * inner_b)
            else:
                answer = format_linear_latex(outer, -outer * inner_b)
            return prompt_latex, prompt_latex, answer

        result = outer * (inner_a + inner_b) if op == "+" else outer * (inner_a - inner_b)
        prompt_latex = f"{outer}({inner_a} {op} {inner_b})"
        return prompt_latex, prompt_latex, str(result)


# ---------------------------------------------------------------------------
# Identify the property (commutative / associative / identity / zero / distributive)
# ---------------------------------------------------------------------------

_PROPERTY_LABELS: tuple[str, ...] = (
    "commutative property of addition",
    "commutative property of multiplication",
    "associative property of addition",
    "associative property of multiplication",
    "identity property of addition",
    "identity property of multiplication",
    "zero property of multiplication",
    "distributive property",
)


def _property_answer_latex(name: str) -> str:
    return rf"\text{{{name}}}"


def _property_int(settings: dict, *, lo_default: int = 2, hi_default: int = 12) -> int:
    lo = int(settings.get("coef_min", settings.get("num_min", lo_default)))
    hi = int(settings.get("coef_max", settings.get("num_max", hi_default)))
    lo = max(1, min(lo, hi))
    hi = max(lo, hi)
    # Grade-6 property examples stay positive and small even if presets go wider.
    lo = max(lo_default, min(lo, hi_default))
    hi = min(max(hi, lo), max(hi_default, lo + 4))
    return random.randint(lo, hi)


class IdentifyPropertyFramework(NumberFramework):
    """Show an equation that illustrates a basic property; answer is the property name."""

    instruction_latex = r"\text{Identify the property.}"
    instruction_text = "Identify the property."

    def __init__(self) -> None:
        self._last_distractors: list[str] = []

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        self._last_distractors = []
        name, prompt_latex, prompt_text = self._build_example(settings)
        answer = _property_answer_latex(name)
        distractors = [
            _property_answer_latex(other)
            for other in _PROPERTY_LABELS
            if other != name
        ]
        random.shuffle(distractors)
        self._last_distractors = distractors[:3]
        return prompt_latex, prompt_text, answer

    def _build_example(self, settings: dict) -> tuple[str, str, str]:
        tier = _difficulty_band(settings)
        if tier == "easy":
            pool = [
                "commutative property of addition",
                "commutative property of multiplication",
                "identity property of addition",
                "identity property of multiplication",
                "zero property of multiplication",
            ]
        else:
            pool = list(_PROPERTY_LABELS)

        name = random.choice(pool)
        a = _property_int(settings)
        b = _property_int(settings)
        while b == a:
            b = _property_int(settings)
        c = _property_int(settings)

        if name == "commutative property of addition":
            latex = f"{a} + {b} = {b} + {a}"
        elif name == "commutative property of multiplication":
            latex = f"{a} \\cdot {b} = {b} \\cdot {a}"
        elif name == "associative property of addition":
            latex = f"({a} + {b}) + {c} = {a} + ({b} + {c})"
        elif name == "associative property of multiplication":
            latex = f"({a} \\cdot {b}) \\cdot {c} = {a} \\cdot ({b} \\cdot {c})"
        elif name == "identity property of addition":
            latex = f"{a} + 0 = {a}" if random.random() < 0.5 else f"0 + {a} = {a}"
        elif name == "identity property of multiplication":
            latex = f"{a} \\cdot 1 = {a}" if random.random() < 0.5 else f"1 \\cdot {a} = {a}"
        elif name == "zero property of multiplication":
            latex = f"{a} \\cdot 0 = 0" if random.random() < 0.5 else f"0 \\cdot {a} = 0"
        else:  # distributive property
            if random.random() < 0.5:
                latex = (
                    f"{a}({b} + {c}) = {a} \\cdot {b} + {a} \\cdot {c}"
                    if random.random() < 0.5
                    else f"{a} \\cdot {b} + {a} \\cdot {c} = {a}({b} + {c})"
                )
            else:
                larger = max(b, c) + random.randint(1, 4)
                smaller = min(b, c)
                latex = (
                    f"{a}({larger} - {smaller}) = {a} \\cdot {larger} - {a} \\cdot {smaller}"
                    if random.random() < 0.5
                    else (
                        f"{a} \\cdot {larger} - {a} \\cdot {smaller}"
                        f" = {a}({larger} - {smaller})"
                    )
                )

        return name, latex, latex

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, object]:
        meta: dict[str, object] = {}
        if self._last_distractors:
            meta["mc_distractors"] = list(self._last_distractors)
        # Always present as multiple choice among property names.
        if answer is not None:
            from ..settings.multiple_choice import build_multiple_choice_metadata

            meta.update(
                build_multiple_choice_metadata(
                    answer, distractors=list(self._last_distractors)
                )
            )
        return meta


def _pemdas_rand(lo: int, hi: int, *, cap: int | None = None) -> int:
    upper = min(hi, cap) if cap is not None else hi
    return random.randint(lo, max(lo, upper))


def _pemdas_divisible_pair(lo: int, hi: int) -> tuple[int, int] | None:
    """Return (dividend, divisor) both within [lo, hi], or None if impossible."""
    candidates: list[tuple[int, int]] = []
    for divisor in range(max(lo, 2), hi + 1):
        for quot in range(2, hi + 1):
            dividend = divisor * quot
            if lo <= dividend <= hi:
                candidates.append((dividend, divisor))
    if not candidates:
        return None
    return random.choice(candidates)


def _build_pemdas_basic(lo: int, hi: int) -> tuple[str, int]:
    forms = [
        "a_plus_b_times_c",
        "a_times_b_plus_c",
        "a_minus_b_times_c",
        "a_times_b_minus_c",
        "a_plus_b_times_c_minus_d",
        "a_times_b_plus_c_times_d",
        "a_minus_b_plus_c_times_d",
        "a_plus_b_minus_c_times_d",
    ]
    if _pemdas_divisible_pair(lo, hi) is not None:
        forms.extend(
            [
                "a_div_b_plus_c",
                "a_plus_b_div_c",
                "a_times_b_div_c",
                "a_div_b_times_c",
            ]
        )
    form = random.choice(forms)
    if form == "a_plus_b_times_c":
        a, b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi), _pemdas_rand(lo, hi, cap=8)
        return f"{a} + {b} \\cdot {c}", a + b * c
    if form == "a_times_b_plus_c":
        a, b, c = _pemdas_rand(lo, hi, cap=8), _pemdas_rand(lo, hi, cap=8), _pemdas_rand(lo, hi)
        return f"{a} \\cdot {b} + {c}", a * b + c
    if form == "a_minus_b_times_c":
        for _ in range(40):
            b, c = _pemdas_rand(lo, hi, cap=6), _pemdas_rand(lo, hi, cap=6)
            product = b * c
            if product < lo:
                continue
            # Prefer non-negative results using an a within range when possible.
            a_lo = max(lo, product)
            if a_lo <= hi:
                a = _pemdas_rand(a_lo, hi)
                return f"{a} - {b} \\cdot {c}", a - product
        a, b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi, cap=4), _pemdas_rand(lo, hi, cap=4)
        return f"{a} + {b} \\cdot {c}", a + b * c
    if form == "a_times_b_minus_c":
        for _ in range(40):
            a, b = _pemdas_rand(lo, hi, cap=8), _pemdas_rand(lo, hi, cap=8)
            product = a * b
            if product <= lo:
                continue
            c = _pemdas_rand(lo, min(hi, product - 1))
            return f"{a} \\cdot {b} - {c}", product - c
        a, b, c = _pemdas_rand(lo, hi, cap=8), _pemdas_rand(lo, hi, cap=8), _pemdas_rand(lo, hi)
        return f"{a} \\cdot {b} + {c}", a * b + c
    if form == "a_plus_b_times_c_minus_d":
        for _ in range(40):
            a, b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi, cap=7), _pemdas_rand(lo, hi, cap=7)
            total = a + b * c
            if total <= lo:
                continue
            d = _pemdas_rand(lo, min(hi, total - 1))
            return f"{a} + {b} \\cdot {c} - {d}", total - d
        a, b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi, cap=7), _pemdas_rand(lo, hi, cap=7)
        return f"{a} + {b} \\cdot {c}", a + b * c
    if form == "a_times_b_plus_c_times_d":
        a, b = _pemdas_rand(lo, hi, cap=6), _pemdas_rand(lo, hi, cap=6)
        c, d = _pemdas_rand(lo, hi, cap=6), _pemdas_rand(lo, hi, cap=6)
        return f"{a} \\cdot {b} + {c} \\cdot {d}", a * b + c * d
    if form == "a_div_b_plus_c":
        pair = _pemdas_divisible_pair(lo, hi)
        assert pair is not None
        a, b = pair
        c = _pemdas_rand(lo, hi)
        return f"{a} \\div {b} + {c}", a // b + c
    if form == "a_plus_b_div_c":
        pair = _pemdas_divisible_pair(lo, hi)
        assert pair is not None
        b, c = pair
        a = _pemdas_rand(lo, hi)
        return f"{a} + {b} \\div {c}", a + b // c
    if form == "a_minus_b_plus_c_times_d":
        for _ in range(40):
            b = _pemdas_rand(lo, hi)
            a = _pemdas_rand(b, hi) if b <= hi else _pemdas_rand(lo, hi)
            if a < b:
                continue
            c, d = _pemdas_rand(lo, hi, cap=6), _pemdas_rand(lo, hi, cap=6)
            return f"{a} - {b} + {c} \\cdot {d}", a - b + c * d
        a, b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi), _pemdas_rand(lo, hi, cap=6)
        return f"{a} + {b} \\cdot {c}", a + b * c
    if form == "a_times_b_div_c":
        for _ in range(40):
            c = _pemdas_rand(max(2, lo), hi, cap=8)
            quot = _pemdas_rand(lo, hi, cap=6)
            b = c * quot
            if not (lo <= b <= hi):
                continue
            a = _pemdas_rand(lo, hi, cap=8)
            return f"{a} \\cdot {b} \\div {c}", a * b // c
        a, b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi), _pemdas_rand(lo, hi, cap=6)
        return f"{a} + {b} \\cdot {c}", a + b * c
    if form == "a_div_b_times_c":
        pair = _pemdas_divisible_pair(lo, hi)
        assert pair is not None
        a, b = pair
        c = _pemdas_rand(lo, hi, cap=8)
        return f"{a} \\div {b} \\cdot {c}", (a // b) * c
    # a_plus_b_minus_c_times_d
    for _ in range(40):
        c, d = _pemdas_rand(lo, hi, cap=5), _pemdas_rand(lo, hi, cap=5)
        a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        if a + b >= c * d:
            return f"{a} + {b} - {c} \\cdot {d}", a + b - c * d
    a, b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi), _pemdas_rand(lo, hi, cap=5)
    return f"{a} + {b} \\cdot {c}", a + b * c


def _build_pemdas_parentheses(lo: int, hi: int) -> tuple[str, int]:
    forms = [
        "sum_times",
        "times_sum",
        "diff_times",
        "times_diff",
        "minus_sum",
        "sum_times_minus",
        "times_sum_minus",
        "juxtaposed_sum",
        "sum_times_sum",
    ]
    # Division-with-parentheses only when clean in-range dividends exist.
    if any(
        lo <= k * d <= hi
        for d in range(max(lo, 2), hi + 1)
        for k in range(2, hi + 1)
    ):
        forms.extend(["sum_div", "div_sum", "diff_div"])
    form = random.choice(forms)
    if form == "sum_times":
        a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        c = _pemdas_rand(lo, hi, cap=8)
        return f"({a} + {b}) \\cdot {c}", (a + b) * c
    if form == "times_sum":
        a = _pemdas_rand(lo, hi, cap=8)
        b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        return f"{a} \\cdot ({b} + {c})", a * (b + c)
    if form == "diff_times":
        for _ in range(40):
            b = _pemdas_rand(lo, hi)
            a = _pemdas_rand(b, hi) if b <= hi else b
            if a <= b:
                continue
            c = _pemdas_rand(lo, hi, cap=8)
            return f"({a} - {b}) \\cdot {c}", (a - b) * c
        a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        c = _pemdas_rand(lo, hi, cap=8)
        return f"({a} + {b}) \\cdot {c}", (a + b) * c
    if form == "times_diff":
        for _ in range(40):
            c = _pemdas_rand(lo, hi)
            b = _pemdas_rand(c, hi) if c <= hi else c
            if b <= c:
                continue
            a = _pemdas_rand(lo, hi, cap=8)
            return f"{a} \\cdot ({b} - {c})", a * (b - c)
        a = _pemdas_rand(lo, hi, cap=8)
        b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        return f"{a} \\cdot ({b} + {c})", a * (b + c)
    if form == "minus_sum":
        for _ in range(40):
            b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
            need = b + c
            if need > hi:
                continue
            a = _pemdas_rand(need, hi)
            return f"{a} - ({b} + {c})", a - (b + c)
        a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        c = _pemdas_rand(lo, hi, cap=8)
        return f"({a} + {b}) \\cdot {c}", (a + b) * c
    if form == "sum_div":
        for _ in range(40):
            c = _pemdas_rand(max(2, lo), hi, cap=8)
            total = c * _pemdas_rand(2, max(2, min(hi, 9)))
            if total > 2 * hi:
                continue
            a = _pemdas_rand(lo, min(hi, total - lo))
            b = total - a
            if not (lo <= a <= hi and lo <= b <= hi):
                continue
            return f"({a} + {b}) \\div {c}", (a + b) // c
        a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        c = _pemdas_rand(lo, hi, cap=8)
        return f"({a} + {b}) \\cdot {c}", (a + b) * c
    if form == "div_sum":
        for _ in range(40):
            b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
            denom = b + c
            quot = _pemdas_rand(2, max(2, min(hi, 8)))
            a = denom * quot
            if lo <= a <= hi * max(3, hi):
                # Allow dividend slightly above hi so division stays interesting,
                # but keep it modest for worksheet size.
                if a <= max(hi * 3, 24):
                    return f"{a} \\div ({b} + {c})", a // denom
        a = _pemdas_rand(lo, hi, cap=8)
        b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        return f"{a} \\cdot ({b} + {c})", a * (b + c)
    if form == "sum_times_minus":
        for _ in range(40):
            a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
            c = _pemdas_rand(lo, hi, cap=6)
            product = (a + b) * c
            if product <= lo:
                continue
            d = _pemdas_rand(lo, min(hi, product - 1))
            return f"({a} + {b}) \\cdot {c} - {d}", product - d
        a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        c = _pemdas_rand(lo, hi, cap=6)
        return f"({a} + {b}) \\cdot {c}", (a + b) * c
    if form == "times_sum_minus":
        for _ in range(40):
            a = _pemdas_rand(lo, hi, cap=6)
            b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
            product = a * (b + c)
            if product <= lo:
                continue
            d = _pemdas_rand(lo, min(hi, product - 1))
            return f"{a} \\cdot ({b} + {c}) - {d}", product - d
        a = _pemdas_rand(lo, hi, cap=6)
        b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        return f"{a} \\cdot ({b} + {c})", a * (b + c)
    if form == "juxtaposed_sum":
        a = _pemdas_rand(lo, hi, cap=8)
        b, c = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
        return f"{a}({b} + {c})", a * (b + c)
    if form == "sum_times_sum":
        a, b = _pemdas_rand(lo, hi, cap=6), _pemdas_rand(lo, hi, cap=6)
        c, d = _pemdas_rand(lo, hi, cap=6), _pemdas_rand(lo, hi, cap=6)
        return f"({a} + {b})({c} + {d})", (a + b) * (c + d)
    # diff_div
    for _ in range(40):
        c = _pemdas_rand(max(2, lo), hi, cap=8)
        diff = c * _pemdas_rand(2, max(2, min(hi, 8)))
        b = _pemdas_rand(lo, hi)
        a = b + diff
        if a > max(hi * 3, 24):
            continue
        return f"({a} - {b}) \\div {c}", (a - b) // c
    a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi)
    c = _pemdas_rand(lo, hi, cap=8)
    return f"({a} + {b}) \\cdot {c}", (a + b) * c


def _build_pemdas_exponent(lo: int, hi: int) -> tuple[str, int]:
    form = random.choice(
        [
            "power_plus",
            "power_minus",
            "power_times",
            "times_power",
            "plus_power",
            "power_plus_product",
            "times_power_plus",
            "sum_squared",
            "product_of_power_and_sum",
            "power_minus_product",
            "plus_times_power",
            "diff_squared",
            "square_plus_square",
            "power_div",
        ]
    )
    base = _pemdas_rand(lo, min(hi, 5), cap=5)
    exp = random.choice([2, 3]) if base <= 4 else 2
    power = base**exp

    if form == "power_plus":
        c = _pemdas_rand(lo, hi)
        return f"{base}^{{{exp}}} + {c}", power + c
    if form == "power_minus":
        c = _pemdas_rand(lo, min(hi, max(lo, power - 1)))
        c = min(c, max(lo, power - 1))
        return f"{base}^{{{exp}}} - {c}", power - c
    if form == "power_times":
        c = _pemdas_rand(lo, hi, cap=8)
        return f"{base}^{{{exp}}} \\cdot {c}", power * c
    if form == "times_power":
        a = _pemdas_rand(lo, hi, cap=8)
        return f"{a} \\cdot {base}^{{{exp}}}", a * power
    if form == "plus_power":
        a = _pemdas_rand(lo, hi)
        return f"{a} + {base}^{{{exp}}}", a + power
    if form == "power_plus_product":
        a, b = _pemdas_rand(lo, hi, cap=6), _pemdas_rand(lo, hi, cap=6)
        return f"{base}^{{{exp}}} + {a} \\cdot {b}", power + a * b
    if form == "times_power_plus":
        a = _pemdas_rand(lo, hi, cap=6)
        b = _pemdas_rand(lo, hi)
        return f"{a} \\cdot {base}^{{{exp}}} + {b}", a * power + b
    if form == "sum_squared":
        a = _pemdas_rand(lo, min(hi, 6), cap=6)
        b = _pemdas_rand(lo, min(hi, 6), cap=6)
        while a + b > 9:
            a = _pemdas_rand(lo, min(hi, 5), cap=5)
            b = _pemdas_rand(lo, min(hi, 4), cap=4)
        return f"({a} + {b})^{{2}}", (a + b) ** 2
    if form == "product_of_power_and_sum":
        a, b = _pemdas_rand(lo, hi, cap=5), _pemdas_rand(lo, hi, cap=5)
        return f"{base}^{{{exp}}}({a} + {b})", power * (a + b)
    if form == "power_minus_product":
        a, b = _pemdas_rand(lo, hi, cap=5), _pemdas_rand(lo, hi, cap=5)
        while power < a * b:
            base = _pemdas_rand(lo, min(hi, 5), cap=5)
            exp = 2 if base > 4 else random.choice([2, 3])
            power = base**exp
            a, b = _pemdas_rand(lo, hi, cap=5), _pemdas_rand(lo, hi, cap=5)
        return f"{base}^{{{exp}}} - {a} \\cdot {b}", power - a * b
    if form == "plus_times_power":
        a, b = _pemdas_rand(lo, hi), _pemdas_rand(lo, hi, cap=6)
        return f"{a} + {b} \\cdot {base}^{{{exp}}}", a + b * power
    if form == "diff_squared":
        b = _pemdas_rand(lo, min(hi, 5), cap=5)
        a = b + _pemdas_rand(1, max(1, min(hi, 6)))
        while a - b > 9 or a > max(hi, b + 6):
            b = _pemdas_rand(lo, min(hi, 4), cap=4)
            a = b + _pemdas_rand(1, max(1, min(hi, 5)))
            if a > hi and hi >= b + 1:
                a = _pemdas_rand(b + 1, hi)
                break
        return f"({a} - {b})^{{2}}", (a - b) ** 2
    if form == "square_plus_square":
        a = _pemdas_rand(lo, min(hi, 6), cap=6)
        b = _pemdas_rand(lo, min(hi, 6), cap=6)
        return f"{a}^{{2}} + {b}^{{2}}", a**2 + b**2
    # power_div — power divisible by small divisor within bounds
    divisors = [d for d in range(max(2, lo), min(hi, power) + 1) if power % d == 0]
    if not divisors:
        return f"{base}^{{{exp}}} + {_pemdas_rand(lo, hi)}", power + _pemdas_rand(lo, hi)
    d = random.choice(divisors)
    return f"{base}^{{{exp}}} \\div {d}", power // d


class OrderOfOperationsFramework(NumberFramework):
    """Evaluate numeric expressions using order of operations."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        complexity = str(settings.get("pemdas_complexity", "mixed"))
        lo, hi = _int_range(settings, "num_min", "num_max", lo_default=2, hi_default=9)
        lo = max(1, lo)
        hi = max(lo, hi)
        # Parentheses tier still includes some plain forms so worksheets aren't uniform.
        patterns = {
            "basic": ["pemdas_basic"],
            "parentheses": ["pemdas_basic", "parentheses"],
            "exponent": ["exponent"],
            "mixed": ["pemdas_basic", "parentheses", "exponent"],
        }
        pattern = random.choice(patterns.get(complexity, patterns["mixed"]))
        if pattern == "pemdas_basic":
            prompt, value = _build_pemdas_basic(lo, hi)
        elif pattern == "parentheses":
            prompt, value = _build_pemdas_parentheses(lo, hi)
        else:
            prompt, value = _build_pemdas_exponent(lo, hi)
        return prompt, "order of operations", str(value)


class ProportionFramework(NumberFramework):
    """Solve proportions for an unknown."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        a, b, c, missing = _sample_equivalent_ratio_missing(settings)
        if random.choice([True, False]):
            prompt = f"\\frac{{{a}}}{{{b}}} = \\frac{{{c}}}{{x}}"
            return prompt, f"{a}/{b} = {c}/x", str(missing)
        prompt = f"\\frac{{{a}}}{{{b}}} = \\frac{{x}}{{{missing}}}"
        return prompt, f"{a}/{b} = x/{missing}", str(c)


class ScientificNotationFramework(NumberFramework):
    """Write and operate with numbers in scientific notation."""

    def __init__(self, *, mode: str = "write"):
        self.mode = mode

    def _random_sci_pair(self, settings: dict) -> tuple[float, int]:
        exp_lo, exp_hi = _sci_exp_bounds(settings)
        exponent = random.randint(exp_lo, exp_hi)
        return _random_sci_mantissa(settings), exponent

    def _pick_operation(self, settings: dict) -> str:
        mode = str(settings.get("sci_operation", "mixed")).strip().lower()
        if mode == "multiply":
            return "\\times"
        if mode == "divide":
            return "\\div"
        return random.choice(["\\times", "\\div"])

    def _ops_pair(
        self, settings: dict, *, op: str, require_norm: bool
    ) -> tuple[float, int, float, int]:
        a, a_exp = self._random_sci_pair(settings)
        b, b_exp = self._random_sci_pair(settings)
        if not require_norm:
            return a, a_exp, b, b_exp

        decimals = _sci_mantissa_decimals(settings)
        scale = 10**decimals
        if op == "\\times":
            # Force product mantissa ≥ 10 so the result needs renormalization.
            lo = max(scale, 5 * scale)
            a = random.randint(lo, 10 * scale - 1) / scale
            b = random.randint(lo, 10 * scale - 1) / scale
        else:
            # Force quotient mantissa < 1 so the result needs renormalization.
            b = random.randint(5 * scale, 10 * scale - 1) / scale
            a_hi = min(4 * scale, int(b * scale) - 1)
            a = random.randint(scale, max(scale, a_hi)) / scale
        return a, a_exp, b, b_exp

    def _write_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        direction = str(settings.get("sci_write_direction", "to_sci")).strip().lower()
        allow_compare = bool(settings.get("allow_magnitude_compare", False))
        if direction == "compare" or (allow_compare and random.random() < 0.35):
            return self._compare_prompt(settings)

        if direction == "both":
            direction = random.choice(["to_sci", "from_sci"])

        mantissa, exponent = self._random_sci_pair(settings)
        sci = _format_sci_latex(mantissa, exponent)
        ordinary = _ordinary_number_latex(mantissa, exponent)

        if direction == "from_sci":
            prompt = f"\\text{{Write in standard form: }} {sci}"
            return prompt, f"standard form of {sci}", ordinary

        prompt = f"\\text{{Write in scientific notation: }} {ordinary}"
        return prompt, f"scientific notation of {ordinary}", sci

    def _compare_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        a, a_exp = self._random_sci_pair(settings)
        b, b_exp = self._random_sci_pair(settings)
        # Ensure distinct magnitudes.
        for _ in range(20):
            if (a, a_exp) != (b, b_exp):
                break
            b, b_exp = self._random_sci_pair(settings)
        a_m, a_e = _normalize_sci(a, a_exp)
        b_m, b_e = _normalize_sci(b, b_exp)
        if a_e > b_e or (a_e == b_e and a_m >= b_m):
            larger = "first"
        else:
            larger = "second"
        prompt = (
            f"\\text{{Which is greater? }} "
            f"{_format_sci_latex(a, a_exp)} \\text{{ or }} {_format_sci_latex(b, b_exp)}"
        )
        answer = (
            _format_sci_latex(a, a_exp)
            if larger == "first"
            else _format_sci_latex(b, b_exp)
        )
        return prompt, "compare scientific notation", answer

    def _operations_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        op = self._pick_operation(settings)
        require_norm = bool(settings.get("require_normalization", False))
        a, a_exp, b, b_exp = self._ops_pair(settings, op=op, require_norm=require_norm)
        a_dec, b_dec = Decimal(str(a)), Decimal(str(b))
        if op == "\\times":
            raw_m = float(a_dec * b_dec)
            result_m, result_e = _normalize_sci(raw_m, a_exp + b_exp)
        else:
            raw_m = float(a_dec / b_dec)
            result_m, result_e = _normalize_sci(raw_m, a_exp - b_exp)
        prompt = (
            f"({a:g} \\times 10^{{{a_exp}}}) {op} "
            f"({b:g} \\times 10^{{{b_exp}}})"
        )
        return prompt, "scientific notation operation", _format_sci_latex(result_m, result_e)

    def _add_subtract_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        exp_lo, exp_hi = _sci_exp_bounds(settings)
        diff_lo, diff_hi = _sci_exp_diff_bounds(settings)
        diff = random.randint(diff_lo, diff_hi)

        # Keep both exponents inside the configured range when possible.
        if diff == 0:
            exp_a = random.randint(exp_lo, exp_hi)
            exp_b = exp_a
        else:
            max_start = exp_hi
            min_start = exp_lo + diff
            if min_start > max_start:
                exp_a = exp_hi
                exp_b = exp_hi - diff
            else:
                exp_a = random.randint(min_start, max_start)
                exp_b = exp_a - diff

        a = _random_sci_mantissa(settings)
        b = _random_sci_mantissa(settings)
        op = random.choice(["+", "-"])

        a_dec, b_dec = Decimal(str(a)), Decimal(str(b))
        if exp_a >= exp_b:
            aligned_a = a_dec
            aligned_b = b_dec / (Decimal(10) ** (exp_a - exp_b))
            base_exp = exp_a
        else:
            aligned_a = a_dec / (Decimal(10) ** (exp_b - exp_a))
            aligned_b = b_dec
            base_exp = exp_b

        combined = aligned_a + aligned_b if op == "+" else aligned_a - aligned_b
        if combined == 0:
            op = "+"
            combined = aligned_a + aligned_b

        result_m, result_e = _normalize_sci(float(combined), base_exp)
        # Same-exponent hard items: nudge so the sum needs renormalization.
        if (
            bool(settings.get("require_normalization", False))
            and diff == 0
            and abs(float(combined)) < 10
        ):
            a = random.randint(55, 99) / 10
            b = random.randint(55, 99) / 10
            combined_f = a + b if op == "+" else a - b
            if abs(combined_f) < 1:
                op = "+"
                combined_f = a + b
            result_m, result_e = _normalize_sci(combined_f, base_exp)

        prompt = (
            f"({a:g} \\times 10^{{{exp_a}}}) {op} "
            f"({b:g} \\times 10^{{{exp_b}}})"
        )
        return prompt, "scientific notation add/subtract", _format_sci_latex(result_m, result_e)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.mode == "write":
            return self._write_prompt(settings)
        if self.mode == "operations":
            return self._operations_prompt(settings)
        return self._add_subtract_prompt(settings)


def continuous_abs_max(
    settings: dict,
    *,
    base: int = 8,
    floor: int = 3,
) -> int | None:
    """Unbounded |n| ceiling from continuous ``difficulty``, else ``None``.

    When the slider is present we ignore EMH ``num_min``/``num_max`` caps so
    magnitude keeps growing (D=0 ≈ base, D=10 ≈ tens, D=20 ≈ hundreds, …).
    """
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))
    # Polynomial growth — no soft asymptote.
    hi = int(base + 2.5 * d + 0.2 * d * d)
    return max(floor, hi)


def _int_bounds(settings: dict, *, lo_default: int = -20, hi_default: int = 20) -> tuple[int, int]:
    cont = continuous_abs_max(settings)
    if cont is not None:
        allow_negative = bool(settings.get("allow_negative", True))
        if allow_negative:
            return -cont, cont
        return 1, cont
    return _int_range(settings, "num_min", "num_max", lo_default=lo_default, hi_default=hi_default)


def _factor_bounds(settings: dict) -> tuple[int, int]:
    cont = continuous_abs_max(settings, base=12, floor=4)
    if cont is not None:
        return 2, cont
    return _int_range(settings, "factor_min", "factor_max", lo_default=4, hi_default=60)


def _require_gcf_greater_than_one(settings: dict) -> bool:
    return bool(settings.get("require_gcf_greater_than_one", True))


def _ensure_distinct_range(lo: int, hi: int, count: int) -> tuple[int, int]:
    """Widen ``hi`` if needed so ``[lo, hi]`` can hold ``count`` distinct ints."""
    lo = max(2, lo)
    hi = max(lo, hi)
    if hi - lo + 1 < count:
        hi = lo + count - 1
    return lo, hi


def _sample_distinct_ints(lo: int, hi: int, count: int) -> list[int]:
    """Sample ``count`` distinct integers in [lo, hi] (each ≥ 2)."""
    lo, hi = _ensure_distinct_range(lo, hi, count)
    return random.sample(range(lo, hi + 1), count)


def _sample_values_for_gcf(lo: int, hi: int, count: int, *, require_gt_one: bool) -> list[int]:
    """Sample ``count`` distinct integers in [lo, hi]; optionally force GCF ≥ 2."""
    lo, hi = _ensure_distinct_range(lo, hi, count)
    if not require_gt_one:
        return _sample_distinct_ints(lo, hi, count)

    max_g = max(2, min(hi // 2, 12))
    for _ in range(40):
        g = random.randint(2, max_g)
        mult_hi = hi // g
        mult_lo = max(1, (lo + g - 1) // g)
        if mult_lo > mult_hi:
            continue
        multipliers = list(range(mult_lo, mult_hi + 1))
        if len(multipliers) < count:
            continue
        chosen = random.sample(multipliers, count)
        values = [g * m for m in chosen]
        if len(set(values)) == count and math.gcd(*values) >= 2:
            return values

    # Deterministic distinct fallback with non-trivial GCF.
    fallback = [12, 18, 30, 42]
    return fallback[:count]


def _sample_gcf_pair(lo: int, hi: int, *, require_gt_one: bool) -> tuple[int, int, int]:
    """Return (a, b, gcf) with distinct a, b and optional GCF ≥ 2 constraint."""
    lo = max(2, lo)
    hi = max(lo, hi)
    g_lo = 2 if require_gt_one else 1
    max_g = max(g_lo, min(hi // 2, 12))
    for _ in range(40):
        g = random.randint(g_lo, max_g)
        mult_hi = hi // g
        mult_lo = max(1, (lo + g - 1) // g)
        if mult_lo > mult_hi:
            continue
        multipliers = list(range(mult_lo, mult_hi + 1))
        if len(multipliers) < 2:
            continue
        m1, m2 = random.sample(multipliers, 2)
        # Keep multipliers coprime so the GCF of the pair is exactly g.
        if math.gcd(m1, m2) != 1:
            continue
        a, b = g * m1, g * m2
        if a == b:
            continue
        return a, b, g
    # Fallback pair that always shares factor 2 when required.
    if require_gt_one:
        return 12, 18, 6
    return 8, 15, 1


def _sample_lcm_pair(lo: int, hi: int) -> tuple[int, int]:
    """Return distinct (a, b) for an LCM word problem."""
    a, b = _sample_distinct_ints(lo, hi, 2)
    return a, b


class IntegerArithmeticFramework(NumberFramework):
    """Integer addition, subtraction, multiplication, and division.

    Division is constructed factors-first: low D always yields an integer
    quotient; the chance of a non-integer (exact Fraction) quotient rises with D.
    """

    def __init__(self, operation: str = "+-"):
        self.operation = operation

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def _signed(self, n: int, *, allow_negative: bool) -> int:
        if not allow_negative or n == 0:
            return abs(n) if n != 0 else n
        return -n if random.choice([True, False]) else n

    def _division_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        lo, hi = _int_bounds(settings)
        allow_negative = bool(settings.get("allow_negative", True))
        if not allow_negative:
            lo = max(1, lo)
            hi = max(lo, hi)
        d = settings_difficulty(settings, default=8.0)
        # Easy: always divides evenly. Non-integer chance ramps after D≈5.
        p_nonint = 0.0 if d < 5.0 else min(0.85, (d - 5.0) / 18.0)
        if not bool(settings.get("allow_noninteger_quotient", True)):
            p_nonint = 0.0

        # Keep divisors classroom-sized relative to magnitude (harder D → larger).
        div_hi = max(2, min(abs(hi), max(2, int(3 + 0.6 * d + 0.05 * d * d))))
        divisor = random.randint(2, div_hi)

        if random.random() < p_nonint:
            # Non-integer exact quotient: dividend not a multiple of divisor.
            for _ in range(40):
                quot_hi = max(1, abs(hi) // max(divisor, 1))
                # Pick a nearby non-multiple so the quotient is a proper fraction-ish.
                base_q = random.randint(1, max(1, quot_hi))
                dividend = divisor * base_q + random.randint(1, divisor - 1)
                if abs(dividend) <= max(abs(hi), divisor * base_q + divisor):
                    break
            else:
                dividend = divisor * 2 + 1
            dividend = self._signed(dividend, allow_negative=allow_negative)
            divisor_s = self._signed(divisor, allow_negative=allow_negative)
            if divisor_s == 0:
                divisor_s = divisor
            result = Fraction(dividend, divisor_s)
            answer = frac_latex(result)
        else:
            # Integer quotient: choose q and divisor, multiply out.
            quot_hi = max(1, abs(hi) // max(divisor, 1))
            # At low D prefer small quotients (mental math).
            if d < 4.0:
                quot_hi = min(quot_hi, 10)
            elif d < 10.0:
                quot_hi = min(quot_hi, 20)
            q = random.randint(1, max(1, quot_hi))
            # Avoid n÷n = 1 as the default easy item — prefer a real quotient.
            if quot_hi >= 2 and q == 1 and random.random() < 0.85:
                q = random.randint(2, quot_hi)
            q = self._signed(q, allow_negative=allow_negative)
            divisor_s = self._signed(divisor, allow_negative=allow_negative)
            if divisor_s == 0:
                divisor_s = divisor
            dividend = q * divisor_s
            result = q
            answer = str(result)

        latex_op = "\\div"
        prompt_latex = format_binop_expression(dividend, latex_op, divisor_s)
        prompt_text = format_binop_expression(dividend, "/", divisor_s)
        return prompt_latex, prompt_text, answer

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        op = self._resolve_operation()
        if op == "/":
            return self._division_prompt(settings)

        lo, hi = _int_bounds(settings)
        allow_negative = bool(settings.get("allow_negative", True))
        if not allow_negative:
            lo = max(1, lo)
            hi = max(lo, hi)

        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        if op == "-" and not allow_negative and b > a:
            a, b = b, a
        elif op == "*":
            if not allow_negative:
                a = abs(a) or random.randint(1, hi)
                b = abs(b) or random.randint(1, hi)
            # Keep products from exploding unreadably at very high D: shrink
            # one factor when both are huge.
            from question_engine.frameworks.difficulty_budget import settings_difficulty

            d = settings_difficulty(settings, default=8.0)
            if abs(a) * abs(b) > 50_000 and d < 40:
                b = self._signed(
                    random.randint(2, max(2, int(3 + d))),
                    allow_negative=allow_negative,
                ) or 2

        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
        }
        result = ops[op](a, b)
        latex_op = {"+": "+", "-": "-", "*": "\\cdot"}[op]
        prompt_latex = format_binop_expression(a, latex_op, b)
        prompt_text = format_binop_expression(a, op, b)
        return prompt_latex, prompt_text, str(result)


def _enabled_number_forms(settings: dict) -> list[str]:
    """Forms for mixed integer/decimal/fraction arithmetic (PA unit scope)."""
    forms: list[str] = []
    if bool(settings.get("allow_integers", True)):
        forms.append("integer")
    if bool(settings.get("allow_decimals", False)):
        forms.append("decimal")
    if bool(settings.get("allow_fractions", False)):
        forms.append("fraction")
    return forms or ["integer"]


class MixedNumberArithmeticFramework(NumberFramework):
    """Add/subtract using integers, decimals, and/or fractions per settings.

    For true mixed FDP add/subtract topics. Integer-only PA topics should use
    IntegerArithmeticFramework instead.
    """

    def __init__(self, operation: str = "+-"):
        self.operation = operation
        self._integer = IntegerArithmeticFramework(operation)
        self._fraction_like = LikeDenominatorFractionFramework(operation)
        self._fraction_unlike = UnlikeDenominatorFractionFramework(operation)
        self._fraction_any = RationalFramework(operation)

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def _decimal_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        """Decimal add/subtract scaled to num_min/num_max (not fixed 0..99.9)."""
        places = max(1, int(settings.get("decimal_places", 2)))
        allow_negative = bool(settings.get("allow_negative", True))
        lo, hi = _int_bounds(settings)
        # Keep decimals in the same magnitude band as integer operands.
        magnitude = max(1.0, float(max(abs(lo), abs(hi), 1)))
        minimum = 0.1 if not allow_negative else -magnitude
        maximum = magnitude
        a = _random_decimal(
            places=places, minimum=minimum, maximum=maximum, allow_negative=allow_negative
        )
        b = _random_decimal(
            places=places, minimum=minimum, maximum=maximum, allow_negative=allow_negative
        )
        # Avoid trivial integer-looking decimals when possible.
        for _ in range(8):
            if a != a.to_integral_value() or b != b.to_integral_value():
                break
            a = _random_decimal(
                places=places, minimum=minimum, maximum=maximum, allow_negative=allow_negative
            )
            b = _random_decimal(
                places=places, minimum=minimum, maximum=maximum, allow_negative=allow_negative
            )
        op = self._resolve_operation()
        if op == "-" and not allow_negative and b > a:
            a, b = b, a
        result = a + b if op == "+" else a - b
        latex_op = "+" if op == "+" else "-"
        a_s = _format_decimal(a, places=places)
        b_s = _format_decimal(b, places=places)
        prompt_latex = format_binop_expression(a_s, latex_op, b_s)
        prompt_text = format_binop_expression(a_s, op, b_s)
        return prompt_latex, prompt_text, _format_decimal(result, places=places)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        form = random.choice(_enabled_number_forms(settings))
        if form == "integer":
            return self._integer.build_prompt(settings)
        if form == "decimal":
            return self._decimal_prompt(settings)
        if bool(settings.get("require_common_denominator", False)):
            return self._fraction_like.build_prompt(settings)
        if bool(settings.get("require_unlike_denominators", False)):
            return self._fraction_unlike.build_prompt(settings)
        return self._fraction_any.build_prompt(settings)


class LongDivisionWithRemaindersFramework(NumberFramework):
    """Whole-number long division with a nonzero remainder."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        dividend_min = max(1, int(settings.get("dividend_min", 10)))
        dividend_max = max(dividend_min, int(settings.get("dividend_max", 99)))
        divisor_min = max(2, int(settings.get("divisor_min", 2)))
        divisor_max = max(divisor_min, int(settings.get("divisor_max", 9)))

        dividend = dividend_min
        divisor = divisor_min
        quotient = 0
        remainder = 1
        for _ in range(60):
            divisor = random.randint(divisor_min, divisor_max)
            if divisor < 2:
                continue
            rem = random.randint(1, divisor - 1)
            max_q = (dividend_max - rem) // divisor
            min_q = max(1, (dividend_min - rem + divisor - 1) // divisor)
            if min_q > max_q or max_q < 1:
                continue
            quotient = random.randint(min_q, max_q)
            dividend = quotient * divisor + rem
            if dividend_min <= dividend <= dividend_max:
                remainder = rem
                break
        else:
            # Deterministic fallback within easy-scale bounds.
            divisor = min(divisor_max, max(divisor_min, 3))
            remainder = 1
            quotient = max(1, dividend_min // divisor)
            dividend = quotient * divisor + remainder
            if dividend > dividend_max:
                quotient = max(1, (dividend_max - remainder) // divisor)
                dividend = quotient * divisor + remainder

        prompt_latex = f"{dividend} \\div {divisor}"
        answer = f"{quotient} \\text{{ R }} {remainder}"
        return prompt_latex, f"{dividend} ÷ {divisor}", answer


class LikeDenominatorFractionFramework(NumberFramework):
    """Add or subtract fractions with a common denominator."""

    def __init__(self, operation: str = "+-"):
        self.operation = operation

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        op = self._resolve_operation()
        denominator = random.randint(params.denom_min, params.denom_max)
        lo = max(1, params.num_min) if not params.allow_negative else params.num_min
        hi = params.num_max
        n1 = random.randint(lo, hi)
        n2 = random.randint(lo, hi)
        while n1 == 0 or n2 == 0:
            n1 = random.randint(lo, hi)
            n2 = random.randint(lo, hi)
        if op == "-" and not params.allow_negative and n2 > n1:
            n1, n2 = n2, n1

        a = Fraction(n1, denominator)
        b = Fraction(n2, denominator)
        result = a + b if op == "+" else a - b
        latex_op = "+" if op == "+" else "-"
        prompt_latex = f"{frac_latex(a)} {latex_op} {frac_latex(b)}"
        return prompt_latex, f"{a} {op} {b}", frac_latex(result)


class UnlikeDenominatorFractionFramework(NumberFramework):
    """Add or subtract fractions with unlike denominators."""

    def __init__(self, operation: str = "+-"):
        self.operation = operation

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def _random_unlike_pair(self, params: NumberParams) -> tuple[Fraction, Fraction]:
        a = random_fraction(
            num_min=params.num_min,
            num_max=params.num_max,
            denom_min=params.denom_min,
            denom_max=params.denom_max,
            allow_negative=params.allow_negative,
        )
        b = random_fraction(
            num_min=params.num_min,
            num_max=params.num_max,
            denom_min=params.denom_min,
            denom_max=params.denom_max,
            allow_negative=params.allow_negative,
        )
        while a.denominator == b.denominator:
            b = random_fraction(
                num_min=params.num_min,
                num_max=params.num_max,
                denom_min=params.denom_min,
                denom_max=params.denom_max,
                allow_negative=params.allow_negative,
            )
        return a, b

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        op = self._resolve_operation()
        a, b = self._random_unlike_pair(params)
        if op == "-" and not params.allow_negative and a < b:
            a, b = b, a
        result = a + b if op == "+" else a - b
        latex_op = "+" if op == "+" else "-"
        prompt_latex = f"{frac_latex(a)} {latex_op} {frac_latex(b)}"
        return prompt_latex, f"{a} {op} {b}", frac_latex(result)


class FractionDivideWordFramework(NumberFramework):
    """Fraction division word problems (how many groups, how much per group).

    Tier shape is driven by presets:
      - dividend_form / divisor_form: ``whole`` | ``fraction`` | ``any``
      - require_whole_quotient / require_non_whole_quotient
    """

    def __init__(self, *, mode: str = "groups"):
        self.mode = mode

    def _format_value(self, value: Fraction, params: NumberParams) -> str:
        show_mixed = params.allow_mixed and abs(value.numerator) > value.denominator
        return frac_or_mixed_latex(value, allow_mixed=show_mixed)

    def _sample_whole(self, params: NumberParams, *, lo: int = 2, hi: int | None = None) -> Fraction:
        upper = hi if hi is not None else max(lo, min(24, abs(params.num_max) or 12))
        upper = max(lo, upper)
        return Fraction(random.randint(lo, upper))

    def _sample_non_whole(self, params: NumberParams) -> Fraction:
        return random_fraction(
            num_min=max(1, params.num_min),
            num_max=max(3, abs(params.num_max) or 12),
            denom_min=params.denom_min,
            denom_max=min(12, max(params.denom_min + 1, params.denom_max)),
            allow_negative=False,
            require_proper=params.require_proper,
            allow_mixed=params.allow_mixed,
        )

    def _sample_operand(self, form: str, params: NumberParams) -> Fraction:
        kind = (form or "fraction").strip().lower()
        if kind == "whole":
            return self._sample_whole(params)
        if kind == "any":
            if random.random() < 0.5:
                return self._sample_whole(params)
            return self._sample_non_whole(params)
        return self._sample_non_whole(params)

    def _pair_for_tier(self, settings: dict, params: NumberParams) -> tuple[Fraction, Fraction]:
        """Return (dividend, divisor) matching preset operand / quotient constraints."""
        dividend_form = str(settings.get("dividend_form", "fraction")).strip().lower()
        divisor_form = str(settings.get("divisor_form", "fraction")).strip().lower()
        require_whole_q = bool(settings.get("require_whole_quotient", False))
        require_non_whole_q = bool(settings.get("require_non_whole_quotient", False))

        # Easy: whole ÷ whole with whole quotient (constructively).
        if dividend_form == "whole" and divisor_form == "whole" and require_whole_q:
            divisor_n = random.randint(2, 6)
            quotient_n = random.randint(2, 8)
            return Fraction(divisor_n * quotient_n), Fraction(divisor_n)

        for _ in range(80):
            # Medium: whole dividend; divisor whole (non-int quot) or fraction.
            if dividend_form == "whole" and divisor_form in {"any", "fraction", "mixed"}:
                if divisor_form == "fraction" or (
                    divisor_form in {"any", "mixed"} and random.random() < 0.55
                ):
                    divisor = self._sample_non_whole(params)
                    # Prefer a modest whole quotient so the dividend stays whole.
                    if require_non_whole_q and random.random() < 0.45:
                        quot = Fraction(random.randint(1, 5), random.randint(2, 4))
                        while quot.denominator == 1:
                            quot = Fraction(random.randint(1, 5), random.randint(2, 4))
                    else:
                        quot = Fraction(random.randint(2, 8))
                    dividend = divisor * quot
                    if dividend.denominator != 1 or dividend <= 0:
                        continue
                    dividend = Fraction(dividend.numerator)
                else:
                    divisor_n = random.randint(2, 9)
                    dividend_n = random.randint(divisor_n + 1, max(divisor_n + 2, 24))
                    while dividend_n % divisor_n == 0:
                        dividend_n = random.randint(divisor_n + 1, max(divisor_n + 2, 24))
                    dividend = Fraction(dividend_n)
                    divisor = Fraction(divisor_n)
            elif dividend_form == "fraction" and divisor_form == "fraction":
                # Build from a modest quotient so hard stays grade-6 friendly.
                divisor = self._sample_non_whole(params)
                if self.mode == "groups" or random.random() < 0.55:
                    quot = Fraction(random.randint(2, 6))
                else:
                    quot = Fraction(random.randint(1, 5), random.randint(2, 5))
                    while quot.denominator == 1:
                        quot = Fraction(random.randint(1, 5), random.randint(2, 5))
                dividend = divisor * quot
                if dividend.denominator == 1:
                    continue
            else:
                dividend = self._sample_operand(dividend_form, params)
                divisor = self._sample_operand(divisor_form, params)

            if divisor == 0 or dividend <= 0 or divisor <= 0:
                continue
            if dividend_form == "whole" and dividend.denominator != 1:
                continue
            if dividend_form == "fraction" and dividend.denominator == 1:
                continue
            if divisor_form == "whole" and divisor.denominator != 1:
                continue
            if divisor_form == "fraction" and divisor.denominator == 1:
                continue

            quot = dividend / divisor
            if require_whole_q and quot.denominator != 1:
                continue
            if require_non_whole_q and quot.denominator == 1 and divisor.denominator == 1:
                # Whole ÷ fraction with whole quot is allowed on medium; only reject
                # whole÷whole that accidentally lands on a whole answer.
                continue
            return dividend, divisor

        # Deterministic fallbacks by intended shape.
        if dividend_form == "whole" and divisor_form == "whole":
            return Fraction(10), Fraction(4)
        if dividend_form == "whole":
            return Fraction(6), Fraction(1, 2)
        return Fraction(5, 6), Fraction(2, 3)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        if self.mode == "whole":
            dividend = self._sample_operand(
                str(settings.get("dividend_form", "fraction")), params
            )
            portion = Fraction(1, 2)
            prompt = (
                f"\\text{{What fraction of a whole is }} {self._format_value(portion, params)} "
                f"\\text{{ of }} {self._format_value(dividend, params)}\\text{{?}}"
            )
            return prompt, "fraction of a whole", self._format_value(portion * dividend, params)

        dividend, divisor = self._pair_for_tier(settings, params)
        answer = dividend / divisor
        if self.mode == "groups":
            prompt = (
                f"\\text{{How many groups of }} {self._format_value(divisor, params)} "
                f"\\text{{ are in }} {self._format_value(dividend, params)}\\text{{?}}"
            )
        else:
            # Partitive / per-time: whole group counts keep the classic wording;
            # fractional "groups" use a per-period framing that still asks ÷.
            if divisor.denominator == 1:
                prompt = (
                    f"\\text{{If }} {self._format_value(dividend, params)} "
                    f"\\text{{ is shared equally into }} {self._format_value(divisor, params)} "
                    f"\\text{{ groups, how much is in each group?}}"
                )
            else:
                prompt = (
                    f"\\text{{If }} {self._format_value(dividend, params)} "
                    f"\\text{{ is used in }} {self._format_value(divisor, params)} "
                    f"\\text{{ of a period, how much is used in one full period?}}"
                )
        return prompt, f"fraction division ({self.mode})", self._format_value(answer, params)


class GcfLcmFramework(NumberFramework):
    """Greatest common factor and least common multiple."""

    def __init__(self, *, mode: str = "gcf"):
        self.mode = mode

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _factor_bounds(settings)
        count = random.choice([2, 2, 3])
        if self.mode == "gcf":
            values = _sample_values_for_gcf(
                lo,
                hi,
                count,
                require_gt_one=_require_gcf_greater_than_one(settings),
            )
            result = math.gcd(*values)
            label = "GCF"
        else:
            values = _sample_distinct_ints(lo, hi, count)
            result = math.lcm(*values)
            label = "LCM"
        numbers = ", ".join(str(v) for v in values)
        prompt = f"\\text{{Find the {label} of }} {numbers}"
        return prompt, f"{label} of {numbers}", str(result)


class GcfLcmWordFramework(NumberFramework):
    """GCF/LCM word problems."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty
        from question_engine.word_problems.things import (
            SAME_LETTER_MIN_DIFFICULTY,
            pick_things,
        )

        lo, hi = _factor_bounds(settings)
        # High continuous D: allow same-first-letter nouns for extra confusion.
        prefer_same_letter = False
        if "difficulty" in settings and settings["difficulty"] is not None:
            d = settings_difficulty(settings, default=0.0)
            prefer_same_letter = d >= SAME_LETTER_MIN_DIFFICULTY - 1e-9
        item_a, item_b = pick_things(2, prefer_same_first_letter=prefer_same_letter)

        use_gcf = random.choice([True, False])
        if use_gcf:
            a, b, g = _sample_gcf_pair(
                lo,
                hi,
                require_gt_one=_require_gcf_greater_than_one(settings),
            )
            text = (
                f"You have {a} {item_a} and {b} {item_b}. "
                f"What is the greatest number of identical bags you can make?"
            )
            prompt = f"\\text{{{text}}}"
            return prompt, text, str(g)
        a, b = _sample_lcm_pair(lo, hi)
        lcm_val = math.lcm(a, b)
        # Pack story needs two distinct items (classic hot-dogs / buns pattern).
        text = (
            f"{item_a.capitalize()} come in packs of {a} and {item_b} come in packs of {b}. "
            f"What is the least number of each needed so there are no leftovers?"
        )
        prompt = f"\\text{{{text}}}"
        return prompt, text, str(lcm_val)


_SMALL_PRIMES: tuple[int, ...] = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def _prime_factorization_latex(n: int) -> str:
    factors: dict[int, int] = {}
    d = 2
    value = n
    while d * d <= value:
        while value % d == 0:
            factors[d] = factors.get(d, 0) + 1
            value //= d
        d += 1
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    parts = []
    for prime in sorted(factors):
        exp = factors[prime]
        if exp == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{{{exp}}}")
    return " \\cdot ".join(parts)


def _count_prime_factors(n: int) -> int:
    """Total number of prime factors counting multiplicity."""
    count = 0
    value = n
    d = 2
    while d * d <= value:
        while value % d == 0:
            count += 1
            value //= d
        d += 1
    if value > 1:
        count += 1
    return count


def _sample_prime_product(settings: dict) -> int:
    """Build a composite from prime factors honoring count / size presets."""
    count_min, count_max = _int_range(
        settings, "prime_factor_count_min", "prime_factor_count_max", lo_default=2, hi_default=4
    )
    prime_max = max(3, int(settings.get("prime_max", 13)))
    product_max = max(6, int(settings.get("factor_product_max", settings.get("factor_max", 999))))
    primes = [p for p in _SMALL_PRIMES if p <= prime_max]
    if len(primes) < 2:
        primes = [2, 3, 5, 7]

    for _ in range(80):
        count = random.randint(count_min, count_max)
        factors = [random.choice(primes) for _ in range(count)]
        product = 1
        for p in factors:
            if product > product_max // p:
                product = 0
                break
            product *= p
        if product < 4 or product > product_max:
            continue
        if _count_prime_factors(product) < count_min:
            continue
        return product

    # Deterministic fallback: two distinct small primes under the product cap.
    for a in primes:
        for b in primes:
            if a * b <= product_max and a * b >= 4:
                return a * b
    return 6


class PrimeFactorizationFramework(NumberFramework):
    """Prime factorization of a composite whole number."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        # Prefer factor-count presets when present; otherwise fall back to range sampling.
        if "prime_factor_count_min" in settings or "prime_factor_count_max" in settings:
            n = _sample_prime_product(settings)
        else:
            lo, hi = _factor_bounds(settings)
            lo = max(lo, 4)
            n = random.randint(lo, hi)
            while n < 4 or _count_prime_factors(n) < 2:
                n = random.randint(lo, hi)
        prompt = f"\\text{{Write the prime factorization of }} {n}"
        return prompt, f"prime factorization of {n}", _prime_factorization_latex(n)


class DivisibilityFramework(NumberFramework):
    """Divisibility rules for 2, 3, 4, 5, 6, 9, and 10."""

    _RULES: dict[int, str] = {
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        9: "9",
        10: "10",
    }

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _factor_bounds(settings)
        divisor = random.choice(list(self._RULES))
        if random.choice([True, False]):
            base = random.randint(lo, hi)
            if base % divisor == 0:
                n = base
            else:
                n = base + (divisor - base % divisor) % divisor
                if n == base:
                    n = base + divisor
        else:
            base = random.randint(lo, hi)
            n = base if base % divisor != 0 else base + 1
        divisible = n % divisor == 0
        prompt = f"\\text{{Is }} {n} \\text{{ divisible by {divisor}?}}"
        answer = "\\text{Yes}" if divisible else "\\text{No}"
        return prompt, f"divisible by {divisor}?", answer


def _compare_form_menu(d: float) -> list[tuple[str, str, str, float]]:
    """D-gated weighted menu of compare form pairs.

    Bands (primary ladder):
      whole_whole → whole_decimal → decimal_decimal → decimal_frac/frac_whole → frac_frac
    """
    d = max(0.0, float(d))
    menu: list[tuple[str, str, str, float]] = [
        ("int", "int", "whole_whole", max(0.05, 14.0 - 1.5 * d)),
    ]
    if d >= 2.0:
        w = min(8.0, 0.8 + 0.45 * d)
        if d >= 16.0:
            w *= max(0.15, 1.0 - (d - 16.0) / 30.0)
        menu.append(("int", "decimal", "whole_decimal", w))
    if d >= 5.5:
        w = min(10.0, 0.6 + 0.55 * (d - 5.5))
        if d >= 22.0:
            w *= max(0.25, 1.0 - (d - 22.0) / 35.0)
        menu.append(("decimal", "decimal", "decimal_decimal", w))
    if d >= 10.0:
        menu.append(
            ("decimal", "frac", "decimal_frac", min(12.0, 0.8 + 0.7 * (d - 10.0)))
        )
        menu.append(("frac", "int", "frac_whole", min(10.0, 0.6 + 0.55 * (d - 10.0))))
    if d >= 15.0:
        menu.append(
            ("frac", "frac", "frac_frac", min(22.0, 1.5 + 1.1 * (d - 15.0)))
        )
    return [(a, b, band, w) for a, b, band, w in menu if w > 1e-9]


def _pick_compare_form_pair(d: float) -> tuple[str, str, str]:
    menu = _compare_form_menu(d)
    weights = [w for *_rest, w in menu]
    choice = random.choices(menu, weights=weights, k=1)[0]
    return choice[0], choice[1], choice[2]


def _compare_separation(d: float, *, scale: float) -> float:
    """Absolute gap between two values: far at low D, near at high D."""
    t = min(1.0, max(0.0, float(d) / 40.0))
    mag = max(1.0, abs(float(scale)))
    # Relative targets — primary closeness signal (independent of mag growth).
    far_rel, near_rel = 0.65, 0.02
    blend = 1.0 - (1.0 - t) ** 1.2
    rel = far_rel * (1.0 - blend) + near_rel * blend
    gap = mag * rel
    if d < 4.0:
        # Whole–whole: force a few units of separation.
        gap = max(gap, 3.0 + random.uniform(0, 2))
    else:
        gap = max(0.03, gap)
    # Cap absolute gap so large magnitudes at high D stay "close".
    if d >= 12.0:
        gap = min(gap, max(0.06, mag * (0.15 - 0.08 * min(1.0, (d - 12) / 28))))
    return max(0.02, gap * random.uniform(0.8, 1.2))


def _compare_value_bounds(settings: dict, d: float) -> tuple[float, float]:
    """Readable magnitude band for compare/order (not unbounded abs growth)."""
    allow_neg = bool(settings.get("allow_negative", True))
    # Keep compare/order about telling values apart, not huge magnitudes.
    hi = max(6.0, min(40.0, 8.0 + 0.55 * d + 0.006 * d * d))
    if allow_neg:
        return -hi, hi
    return 0.05, hi


def _compare_den_max(d: float) -> int:
    return max(3, min(24, int(4 + d / 2.2)))


def _compare_decimal_places(d: float, *, other_places: int | None = None) -> int:
    """Pick decimal length; at mid/high D often differ from a paired value."""
    if d < 6.0:
        return 1
    if other_places is None:
        if d < 12.0:
            return random.choice([1, 1, 2])
        return random.choice([1, 2, 2, 3])
    # Prefer a different length when D is high enough.
    pool = [1, 2] if d < 14 else [1, 2, 3]
    if d >= 8.0 and random.random() < min(0.85, 0.35 + d / 40.0):
        alt = [p for p in pool if p != other_places]
        if alt:
            return random.choice(alt)
    return other_places if other_places in pool else random.choice(pool)


def _render_compare_value(
    kind: str,
    target: float,
    *,
    d: float,
    lo: float,
    hi: float,
    allow_negative: bool,
    places: int | None = None,
) -> tuple[str, float]:
    """Render ``target`` as int / decimal / fraction (exact when possible)."""
    target = max(lo, min(hi, float(target)))
    if not allow_negative and target < 0:
        target = abs(target)

    if kind == "int":
        v = int(round(target))
        if v == 0 and abs(target) > 0.4:
            v = 1 if target > 0 else -1
        v = int(max(lo, min(hi, v)))
        if not allow_negative:
            v = max(0, v)
        return str(v), float(v)

    if kind == "decimal":
        p = places if places is not None else _compare_decimal_places(d)
        p = max(1, min(3, p))
        quant = 10**p
        v = round(target * quant) / quant
        v = max(lo, min(hi, v))
        if abs(v) < 10 ** (-p) and target != 0:
            v = (1 if target >= 0 else -1) / quant
        text = _format_decimal(Decimal(str(v)), places=p)
        # Avoid accidental integers looking like wholes when we want a decimal.
        if "." not in text and p >= 1:
            text = f"{int(round(v))}.{('0' * p)}"
            v = float(Decimal(text))
        return text, float(v)

    # fraction
    den_hi = _compare_den_max(d)
    # Prefer dens that make a close approximation when target is awkward.
    dens = list(range(2, den_hi + 1))
    random.shuffle(dens)
    best: Fraction | None = None
    best_err = float("inf")
    for den in dens[: min(12, len(dens))]:
        num = int(round(target * den))
        if num == 0:
            num = 1 if target >= 0 else -1
        if not allow_negative and num < 0:
            num = abs(num)
        # Keep magnitude in band.
        if abs(num / den) > max(abs(lo), abs(hi)) + 1:
            continue
        frac = Fraction(num, den)
        err = abs(float(frac) - target)
        if err < best_err:
            best_err = err
            best = frac
    if best is None:
        den = random.randint(2, den_hi)
        num = max(1, int(round(abs(target) * den)))
        if allow_negative and target < 0:
            num = -num
        best = Fraction(num, den)
    return frac_latex(best), float(best)


def _sample_anchor_value(
    kind: str,
    *,
    d: float,
    lo: float,
    hi: float,
    allow_negative: bool,
    places: int | None = None,
) -> tuple[str, float]:
    """Sample a free-standing value of the given form."""
    if kind == "int":
        ilo, ihi = int(math.floor(lo)), int(math.ceil(hi))
        if not allow_negative:
            ilo = max(0, ilo)
        if ilo >= ihi:
            ihi = ilo + 5
        v = random.randint(ilo, ihi)
        return str(v), float(v)
    if kind == "decimal":
        p = places if places is not None else _compare_decimal_places(d)
        mag_lo = 0.1 if not allow_negative else max(lo, -hi)
        dec = _random_decimal(
            places=p,
            minimum=max(0.05, abs(mag_lo) * 0.05) if not allow_negative else lo,
            maximum=hi if hi > 0 else 10.0,
            allow_negative=allow_negative and lo < 0,
        )
        text = _format_decimal(dec, places=p)
        if "." not in text:
            text = f"{text}.{('0' * p)}"
        return text, float(dec)
    # fraction — prefer proper / simple at low D
    den_hi = _compare_den_max(d)
    den = random.randint(2, den_hi)
    if d < 8:
        num = random.randint(1, den)
    else:
        num = random.randint(1, max(den, int(den * min(3, 1 + d / 20))))
    if allow_negative and random.random() < 0.35:
        num = -num
    frac = Fraction(num, den)
    return frac_latex(frac), float(frac)


def _sample_compare_pair(
    settings: dict, d: float
) -> tuple[str, float, str, float, str]:
    """Pick a form pair from the D menu and two unequals with controlled gap."""
    allow_neg = bool(settings.get("allow_negative", True))
    lo, hi = _compare_value_bounds(settings, d)
    kind_a, kind_b, band = _pick_compare_form_pair(d)
    if random.random() < 0.5:
        kind_a, kind_b = kind_b, kind_a

    places_a = _compare_decimal_places(d) if kind_a == "decimal" else None
    places_b = (
        _compare_decimal_places(d, other_places=places_a)
        if kind_b == "decimal"
        else None
    )

    for _ in range(40):
        latex_a, val_a = _sample_anchor_value(
            kind_a,
            d=d,
            lo=lo,
            hi=hi,
            allow_negative=allow_neg,
            places=places_a,
        )
        gap = _compare_separation(d, scale=val_a if abs(val_a) > 0.5 else 3.0)
        # Low D: push farther; high D already near via gap formula.
        direction = random.choice([-1.0, 1.0])
        target_b = val_a + direction * gap
        if target_b < lo or target_b > hi:
            target_b = val_a - direction * gap
        target_b = max(lo, min(hi, target_b))
        latex_b, val_b = _render_compare_value(
            kind_b,
            target_b,
            d=d,
            lo=lo,
            hi=hi,
            allow_negative=allow_neg,
            places=places_b,
        )
        if abs(val_a - val_b) < 1e-9:
            # Nudge away from a tie.
            nudge = max(gap, 0.05) * (1 if val_b >= val_a else -1)
            latex_b, val_b = _render_compare_value(
                kind_b,
                val_a + nudge,
                d=d,
                lo=lo,
                hi=hi,
                allow_negative=allow_neg,
                places=places_b,
            )
        if abs(val_a - val_b) >= 1e-9:
            return latex_a, val_a, latex_b, val_b, band

    # Deterministic fallback: two distinct ints.
    a = random.randint(1, 9)
    b = a + max(2, int(4 - d / 10))
    return str(a), float(a), str(b), float(b), "whole_whole"


def _order_form_weights(d: float) -> dict[str, float]:
    """Relative form mix for ordering sets (hardest unlocked forms dominate at high D)."""
    w = {"int": max(0.1, 10.0 - 1.1 * d)}
    if d >= 2.0:
        w["decimal"] = min(9.0, 0.7 + 0.5 * d)
    if d >= 10.0:
        w["frac"] = min(14.0, 0.5 + 0.6 * (d - 10.0))
    return w


def _order_count(d: float) -> int:
    if d < 7.0:
        return 3
    if d < 16.0:
        return 4
    return 5


def _sample_order_entries(
    settings: dict, d: float
) -> list[tuple[str, float]]:
    """Build an ordered-set of mixed forms; pack closer at high D."""
    allow_neg = bool(settings.get("allow_negative", True))
    lo, hi = _compare_value_bounds(settings, d)
    count = _order_count(d)
    weights = _order_form_weights(d)
    kinds = list(weights.keys())
    wts = [weights[k] for k in kinds]

    # Ensure the set's hardest unlocked form actually appears.
    forced: list[str] = []
    if "frac" in weights and d >= 15.0:
        forced.append("frac")
        if "decimal" in weights and random.random() < 0.7:
            forced.append("decimal")
    elif "decimal" in weights and d >= 5.5:
        forced.append("decimal")

    chosen: list[str] = list(forced)
    while len(chosen) < count:
        chosen.append(random.choices(kinds, weights=wts, k=1)[0])
    random.shuffle(chosen)

    # Shared center + controlled spreads (far → near with D).
    center = random.uniform(lo * 0.4, hi * 0.4) if allow_neg else random.uniform(0.5, hi * 0.5)
    if abs(center) < 0.5:
        center = random.uniform(1.0, max(3.0, hi * 0.25))
    base_gap = _compare_separation(d, scale=center)

    entries: list[tuple[str, float]] = []
    for i, kind in enumerate(chosen):
        # Spread offsets across the set; tighter overall at high D.
        offset = (i - (count - 1) / 2.0) * base_gap * random.uniform(0.85, 1.2)
        # Extra jitter shrinks with D.
        t = min(1.0, d / 40.0)
        jitter = base_gap * (0.35 * (1 - t) + 0.05 * t) * random.uniform(-1, 1)
        target = center + offset + jitter
        places = _compare_decimal_places(d) if kind == "decimal" else None
        latex, val = _render_compare_value(
            kind,
            target,
            d=d,
            lo=lo,
            hi=hi,
            allow_negative=allow_neg,
            places=places,
        )
        # Resolve collisions / ties.
        bump = 0
        while any(abs(val - e[1]) < 1e-9 for e in entries) and bump < 12:
            bump += 1
            target = target + (base_gap * 0.5 + 0.05) * (1 if bump % 2 else -1)
            latex, val = _render_compare_value(
                kind,
                target,
                d=d,
                lo=lo,
                hi=hi,
                allow_negative=allow_neg,
                places=places,
            )
        if not any(abs(val - e[1]) < 1e-9 for e in entries):
            entries.append((latex, val))

    # Fill if collisions ate slots.
    guard = 0
    while len(entries) < count and guard < 40:
        guard += 1
        kind = random.choices(kinds, weights=wts, k=1)[0]
        target = center + random.uniform(-base_gap * count, base_gap * count)
        latex, val = _render_compare_value(
            kind, target, d=d, lo=lo, hi=hi, allow_negative=allow_neg
        )
        if not any(abs(val - e[1]) < 1e-9 for e in entries):
            entries.append((latex, val))
    return entries


def _abs_mag_hi(d: float) -> int:
    """Modest |n| ceiling — closeness drives difficulty, not huge magnitudes."""
    return max(8, int(10 + 0.4 * d + 0.005 * d * d))


def _abs_separation(d: float, mag_hi: int) -> int:
    """Gap between absolute values: far at low D, near-ties at high D."""
    d = max(0.0, float(d))
    if d < 3.0:
        gap = random.choice([4, 5, 6])
    elif d < 8.0:
        gap = random.choice([3, 4])
    elif d < 16.0:
        gap = random.choice([2, 3])
    elif d < 28.0:
        gap = random.choice([1, 2])
    else:
        gap = 1
    return max(1, min(mag_hi - 1, gap))


def _abs_apply_sign(mag: int, *, d: float, prefer_opposite_of: int | None = None) -> int:
    """Assign a sign; higher D mixes signs so students must take abs."""
    if mag == 0:
        return 0
    if prefer_opposite_of is not None and prefer_opposite_of != 0 and d >= 4.0:
        # Often opposite the reference so |−7| vs |8|-style items appear.
        if random.random() < min(0.85, 0.35 + d / 50.0):
            return -mag if prefer_opposite_of > 0 else mag
    # Low D: mostly positive; high D: ~50/50.
    p_neg = 0.12 if d < 4 else min(0.55, 0.2 + d / 60.0)
    return -mag if random.random() < p_neg else mag


def _sample_abs_compare_pair(d: float) -> tuple[int, int]:
    mag_hi = _abs_mag_hi(d)
    for _ in range(40):
        a_abs = random.randint(1, mag_hi)
        gap = _abs_separation(d, mag_hi)
        candidates = [a_abs + gap, a_abs - gap]
        candidates = [c for c in candidates if 1 <= c <= mag_hi and c != a_abs]
        if not candidates:
            b_abs = a_abs + 1 if a_abs < mag_hi else max(1, a_abs - 1)
            if b_abs == a_abs:
                b_abs = 1 if a_abs != 1 else 2
        else:
            b_abs = random.choice(candidates)
        a = _abs_apply_sign(a_abs, d=d)
        b = _abs_apply_sign(b_abs, d=d, prefer_opposite_of=a)
        if abs(a) != abs(b):
            return a, b
    return -3, 8


def _sample_abs_order_values(d: float) -> list[int]:
    mag_hi = _abs_mag_hi(d)
    count = 3 if d < 8 else (4 if d < 16 else 5)
    gap = _abs_separation(d, mag_hi)
    # Ensure the arithmetic progression fits inside [1, mag_hi].
    max_gap = max(1, (mag_hi - 1) // max(1, count - 1))
    gap = min(gap, max_gap)
    start_hi = max(1, mag_hi - gap * (count - 1))
    start = random.randint(1, start_hi)
    abs_vals: list[int] = []
    for i in range(count):
        m = start + i * gap
        # Tiny jitter only when there is spare room and gap > 1.
        if gap > 1 and i not in (0, count - 1) and random.random() < 0.25:
            m += random.choice([-1, 1])
        m = max(1, min(mag_hi, m))
        bump = 0
        while m in abs_vals and bump < 12:
            bump += 1
            m = max(1, min(mag_hi, m + bump))
        if m not in abs_vals:
            abs_vals.append(m)
    while len(abs_vals) < count:
        m = random.randint(1, mag_hi)
        if m not in abs_vals:
            abs_vals.append(m)

    values: list[int] = []
    prev = None
    for m in abs_vals:
        v = _abs_apply_sign(m, d=d, prefer_opposite_of=prev)
        values.append(v)
        prev = v
    # At mid/high D, guarantee at least one negative so abs is required.
    if d >= 5.0 and all(v >= 0 for v in values):
        idx = random.randrange(len(values))
        values[idx] = -abs(values[idx])
    return values


class AbsoluteValueFramework(NumberFramework):
    """Evaluate, compare, or order absolute values.

    Compare/order difficulty = how hard it is to tell the absolute values apart:
    far |·| gaps at low D; near-ties + mixed signs at high D. Magnitude grows
    only modestly — closeness is the primary driver.
    """

    def __init__(self, *, mode: str = "evaluate"):
        self.mode = mode

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        d = max(0.0, settings_difficulty(settings, default=8.0))
        if self.mode == "evaluate":
            lo, hi = _int_bounds(settings, lo_default=-15, hi_default=15)
            n = random.randint(lo, hi)
            while n == 0 and d < 3:
                n = random.randint(lo, hi)
            prompt = f"\\left| {n} \\right|"
            return prompt, f"|{n}|", str(abs(n))

        if self.mode == "compare":
            a, b = _sample_abs_compare_pair(d)
            prompt = f"\\left| {a} \\right| \\; ? \\; \\left| {b} \\right|"
            if abs(a) > abs(b):
                answer = ">"
            elif abs(a) < abs(b):
                answer = "<"
            else:
                answer = "="
            return prompt, f"|{a}| vs |{b}|", answer

        values = _sample_abs_order_values(d)
        ordered = sorted(values, key=abs)
        labels = ", ".join(str(v) for v in values)
        prompt = (
            f"\\text{{Order from least to greatest absolute value: }} "
            f"{labels}"
        )
        answer = ", ".join(str(v) for v in ordered)
        return prompt, "order by absolute value", answer


class OppositeFramework(NumberFramework):
    """Find the opposite of an integer."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _int_bounds(settings, lo_default=-20, hi_default=20)
        n = random.randint(lo, hi)
        while n == 0:
            n = random.randint(lo, hi)
        prompt = f"\\text{{Find the opposite of }} {n}"
        return prompt, f"opposite of {n}", str(-n)


class CompareOrderFramework(NumberFramework):
    """Compare or order integers, fractions, and decimals.

    Continuous difficulty uses a **form-mix ladder** (primary) plus **closeness**
    (secondary):

    1. whole–whole → 2. whole–decimal → 3. decimal–decimal (esp. different
       lengths) → 4. decimal–fraction / fraction–whole → 5. fraction–fraction.

    Within a band, low D keeps values far apart; high D packs them close.
    Ordering: the set's hardest unlocked forms drive the band; count grows
    with D (3 → 4 → 5).
    """

    def __init__(self, *, mode: str = "compare"):
        self.mode = mode

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        d = max(0.0, settings_difficulty(settings, default=8.0))

        if self.mode == "compare":
            latex_a, val_a, latex_b, val_b, _band = _sample_compare_pair(settings, d)
            prompt = f"{latex_a} \\; ? \\; {latex_b}"
            if val_a > val_b:
                answer = ">"
            elif val_a < val_b:
                answer = "<"
            else:
                answer = "="
            return prompt, "compare numbers", answer

        entries = _sample_order_entries(settings, d)
        ordered = sorted(entries, key=lambda e: e[1])
        labels = ", ".join(e[0] for e in entries)
        prompt = f"\\text{{Order from least to greatest: }} {labels}"
        answer = ", ".join(e[0] for e in ordered)
        return prompt, "order numbers", answer


# Grade-appropriate F↔D↔P triples (exact). Easy sticks to the first bank.
_EASY_FDP_TRIPLES: tuple[tuple[Fraction, str, int | float], ...] = (
    (Fraction(1, 2), "0.5", 50),
    (Fraction(1, 4), "0.25", 25),
    (Fraction(3, 4), "0.75", 75),
    (Fraction(1, 5), "0.2", 20),
    (Fraction(2, 5), "0.4", 40),
    (Fraction(3, 5), "0.6", 60),
    (Fraction(4, 5), "0.8", 80),
    (Fraction(1, 10), "0.1", 10),
    (Fraction(3, 10), "0.3", 30),
    (Fraction(7, 10), "0.7", 70),
    (Fraction(1, 20), "0.05", 5),
)
_MEDIUM_FDP_TRIPLES: tuple[tuple[Fraction, str, int | float], ...] = _EASY_FDP_TRIPLES + (
    (Fraction(1, 8), "0.125", 12.5),
    (Fraction(3, 8), "0.375", 37.5),
    (Fraction(1, 25), "0.04", 4),
    (Fraction(3, 20), "0.15", 15),
    (Fraction(1, 50), "0.02", 2),
)


class FractionDecimalConvertFramework(NumberFramework):
    """Convert between fractions, decimals, and optionally percents."""

    def __init__(self, *, to_decimal: bool | None = None, include_percent: bool = False):
        self.to_decimal = to_decimal
        self.include_percent = include_percent

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        include_pct = self.include_percent or bool(
            settings.get("include_percent_conversions", False)
        )
        if include_pct:
            return self._build_fdp_prompt(settings)
        params = number_params_from_settings(settings)
        denom = random.choice([2, 4, 5, 8, 10, 20, 25, 50, 100])
        num = random.randint(1, denom - 1)
        while math.gcd(num, denom) != 1:
            num = random.randint(1, denom - 1)
        frac = Fraction(num, denom)
        to_decimal = self.to_decimal if self.to_decimal is not None else random.choice([True, False])
        if to_decimal:
            prompt = f"\\text{{Write }} {frac_latex(frac)} \\text{{ as a decimal.}}"
            answer = _format_decimal(Decimal(frac.numerator) / Decimal(frac.denominator), places=3)
        else:
            dec = Decimal(frac.numerator) / Decimal(frac.denominator)
            prompt = f"\\text{{Write }} {_format_decimal(dec, places=3)} \\text{{ as a fraction.}}"
            answer = frac_latex(frac)
        return prompt, "fraction-decimal conversion", answer

    def _build_fdp_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        tier = _percent_difficulty_tier(settings)
        triples = _EASY_FDP_TRIPLES if tier == "easy" else _MEDIUM_FDP_TRIPLES
        frac, dec_text, percent = random.choice(triples)
        modes = [
            "frac_to_pct",
            "pct_to_frac",
            "dec_to_pct",
            "pct_to_dec",
            "frac_to_dec",
            "dec_to_frac",
        ]
        if tier == "easy":
            # Favor percent forms so the topic isn't a fraction↔decimal-only loop.
            modes = [
                "frac_to_pct",
                "frac_to_pct",
                "pct_to_frac",
                "dec_to_pct",
                "pct_to_dec",
                "frac_to_dec",
                "dec_to_frac",
            ]
        mode = random.choice(modes)
        pct_latex = (
            f"{percent:g}\\%"
            if isinstance(percent, float)
            else f"{percent}\\%"
        )
        pct_text = f"{percent:g}%" if isinstance(percent, float) else f"{percent}%"

        if mode == "frac_to_pct":
            prompt = f"\\text{{Write }} {frac_latex(frac)} \\text{{ as a percent.}}"
            return prompt, f"Write {frac} as a percent", pct_latex
        if mode == "pct_to_frac":
            prompt = f"\\text{{Write }} {pct_latex} \\text{{ as a fraction in simplest form.}}"
            return prompt, f"Write {pct_text} as a fraction", frac_latex(frac)
        if mode == "dec_to_pct":
            prompt = f"\\text{{Write }} {dec_text} \\text{{ as a percent.}}"
            return prompt, f"Write {dec_text} as a percent", pct_latex
        if mode == "pct_to_dec":
            prompt = f"\\text{{Write }} {pct_latex} \\text{{ as a decimal.}}"
            return prompt, f"Write {pct_text} as a decimal", dec_text
        if mode == "frac_to_dec":
            prompt = f"\\text{{Write }} {frac_latex(frac)} \\text{{ as a decimal.}}"
            return prompt, f"Write {frac} as a decimal", dec_text
        prompt = f"\\text{{Write }} {dec_text} \\text{{ as a fraction in simplest form.}}"
        return prompt, f"Write {dec_text} as a fraction", frac_latex(frac)


# Grid for grade6_figures.grid_polygon_svg: x in 0..8, y in 0..5.
_GRID_X_MAX = 8
_GRID_Y_MAX = 5


def _shoelace_area(points: list[tuple[int, int]]) -> Fraction:
    double = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        double += x1 * y2 - x2 * y1
    return Fraction(abs(double), 2)


def _points_on_grid(points: list[tuple[int, int]]) -> bool:
    return all(0 <= x <= _GRID_X_MAX and 0 <= y <= _GRID_Y_MAX for x, y in points)


def _format_grid_area_answer(area: Fraction) -> str:
    if area.denominator == 1:
        body = str(area.numerator)
    else:
        body = frac_latex(area)
    return f"{body}\\text{{ square units}}"


def _grid_polygon_shape_kinds(settings: dict) -> list[str]:
    """Shape mix for polygons / shaded regions on a grid.

    Returns a weighted list (with repetition) so rectangles are not predominant.
    """
    raw = settings.get("polygon_shapes")
    if isinstance(raw, (list, tuple)) and raw:
        return [str(s) for s in raw]
    tier = _difficulty_band(settings)
    if tier == "easy":
        return [
            "square",
            "rectangle",
            "triangle",
            "triangle",
            "parallelogram",
            "parallelogram",
        ]
    if tier == "hard":
        return [
            "square",
            "rectangle",
            "triangle",
            "triangle",
            "parallelogram",
            "parallelogram",
            "trapezoid",
            "trapezoid",
            "l_shape",
            "l_shape",
            "irregular_quad",
            "irregular_quad",
        ]
    return [
        "square",
        "rectangle",
        "triangle",
        "triangle",
        "parallelogram",
        "parallelogram",
        "trapezoid",
        "trapezoid",
    ]


def _place_origin(width: int, height: int) -> tuple[int, int]:
    """Origin for an axis-aligned bounding box that fits the drawn grid."""
    max_x0 = _GRID_X_MAX - width
    max_y0 = _GRID_Y_MAX - height
    x = random.randint(0, max(0, max_x0))
    y = random.randint(0, max(0, max_y0))
    # Prefer an inset when there is room, matching prior figures.
    if max_x0 >= 1:
        x = random.randint(1, max_x0)
    if max_y0 >= 1:
        y = random.randint(1, max_y0)
    return x, y


def _make_grid_square() -> list[tuple[int, int]]:
    side = random.randint(2, 4)
    x, y = _place_origin(side, side)
    return [(x, y), (x + side, y), (x + side, y + side), (x, y + side)]


def _make_grid_rectangle(*, non_square: bool = True) -> list[tuple[int, int]]:
    width = random.randint(2, 5)
    height = random.randint(2, 4)
    if non_square and width == height:
        height = height + 1 if height < 4 else height - 1
    x, y = _place_origin(width, height)
    return [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]


def _make_grid_triangle() -> list[tuple[int, int]]:
    base = random.randint(2, 5)
    height = random.randint(2, 4)
    x, y = _place_origin(base, height)
    apex_x = random.choice([x, x + base, x + base // 2])
    if apex_x == x + base // 2 and base % 2 == 1:
        apex_x = x + (base // 2) + random.choice([0, 1])
    return [(x, y), (x + base, y), (apex_x, y + height)]


def _make_grid_parallelogram() -> list[tuple[int, int]]:
    width = random.randint(2, 4)
    height = random.randint(2, 3)
    shear = random.choice([-2, -1, 1, 2])
    # Translate so every vertex lands in [0, GRID].
    raw = [
        (0, 0),
        (width, 0),
        (width + shear, height),
        (shear, height),
    ]
    min_x = min(p[0] for p in raw)
    max_x = max(p[0] for p in raw)
    span_x = max_x - min_x
    ox = random.randint(0, max(0, _GRID_X_MAX - span_x))
    if _GRID_X_MAX - span_x >= 1:
        ox = random.randint(1, _GRID_X_MAX - span_x)
    oy = random.randint(0, max(0, _GRID_Y_MAX - height))
    if _GRID_Y_MAX - height >= 1:
        oy = random.randint(1, _GRID_Y_MAX - height)
    return [(x - min_x + ox, y + oy) for x, y in raw]


def _make_grid_trapezoid() -> list[tuple[int, int]]:
    bottom = random.randint(3, 5)
    top = random.randint(1, bottom - 1)
    height = random.randint(2, 3)
    max_offset = bottom - top
    offset = random.randint(0, max_offset)
    if offset == 0 and max_offset > 0 and random.random() < 0.5:
        offset = random.randint(1, max_offset)
    x, y = _place_origin(bottom, height)
    return [
        (x, y),
        (x + bottom, y),
        (x + offset + top, y + height),
        (x + offset, y + height),
    ]


def _make_grid_l_shape() -> list[tuple[int, int]]:
    outer_w = random.randint(3, 5)
    outer_h = random.randint(3, 4)
    cut_w = random.randint(1, outer_w - 1)
    cut_h = random.randint(1, outer_h - 1)
    x, y = _place_origin(outer_w, outer_h)
    return [
        (x, y),
        (x + outer_w, y),
        (x + outer_w, y + cut_h),
        (x + cut_w, y + cut_h),
        (x + cut_w, y + outer_h),
        (x, y + outer_h),
    ]


def _make_grid_irregular_quad() -> list[tuple[int, int]]:
    """Convex quad that is not an axis-aligned rectangle."""
    for _ in range(40):
        x = random.randint(1, 2)
        y = random.randint(1, 2)
        w = random.randint(3, 5)
        h = random.randint(2, 3)
        dx = random.randint(1, max(1, w - 2))
        dy = random.randint(0, 1)
        points = [
            (x, y),
            (x + w, y + dy),
            (x + w - dx, y + h),
            (x + 1, y + h - (0 if dy else 1)),
        ]
        if not _points_on_grid(points):
            continue
        if len(set(points)) < 4:
            continue
        area = _shoelace_area(points)
        if area <= 0:
            continue
        ys_set = {p[1] for p in points}
        xs_set = {p[0] for p in points}
        if len(ys_set) == 2 and len(xs_set) == 2:
            continue
        return points
    return [(1, 1), (6, 1), (5, 3), (2, 4)]


def _random_grid_polygon(settings: dict) -> tuple[list[tuple[int, int]], Fraction]:
    makers = {
        "square": _make_grid_square,
        "rectangle": lambda: _make_grid_rectangle(non_square=True),
        "triangle": _make_grid_triangle,
        "parallelogram": _make_grid_parallelogram,
        "trapezoid": _make_grid_trapezoid,
        "l_shape": _make_grid_l_shape,
        "irregular_quad": _make_grid_irregular_quad,
    }
    kinds = [k for k in _grid_polygon_shape_kinds(settings) if k in makers]
    if not kinds:
        kinds = ["rectangle", "triangle", "parallelogram"]
    for _ in range(30):
        kind = random.choice(kinds)
        points = makers[kind]()
        if not _points_on_grid(points):
            continue
        area = _shoelace_area(points)
        if area > 0:
            return points, area
    points = _make_grid_rectangle(non_square=True)
    return points, _shoelace_area(points)


class Grade6VisualFramework(NumberFramework):
    """Grade 6 measurement and visual-model prompts with rendered SVG figures."""

    def __init__(self, mode: str):
        self.mode = mode
        self._metadata: dict[str, object] = {}

    @staticmethod
    def _positive_fraction() -> Fraction:
        denominator = random.choice([2, 3, 4, 5, 6, 8])
        numerator = random.randint(1, denominator * 2 - 1)
        return Fraction(numerator, denominator)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from ..diagrams.charts import dot_plot_svg, histogram_svg
        from ..diagrams.grade6_figures import (
            POLYHEDRON_KINDS,
            area_model_svg,
            cube_net_svg,
            grid_polygon_svg,
            hanger_svg,
            polyhedron_svg,
            prism_svg,
            rectangle_measure_svg,
            triangle_measure_svg,
        )

        unit = random.choice(["cm", "in"])
        if self.mode in {"fraction_rectangle", "fraction_triangle", "fraction_prism"}:
            a, b = self._positive_fraction(), self._positive_fraction()
            if self.mode == "fraction_prism":
                c = self._positive_fraction()
                volume = a * b * c
                self._metadata = {
                    "diagram_svg": prism_svg(
                        format_measurement_text(str(a), unit),
                        format_measurement_text(str(b), unit),
                        format_measurement_text(str(c), unit),
                    )
                }
                return (
                    f"\\text{{Find the volume of the right rectangular prism with side lengths }} "
                    f"{format_with_unit(frac_latex(a), unit)},\\ "
                    f"{format_with_unit(frac_latex(b), unit)},\\ "
                    f"{format_with_unit(frac_latex(c), unit)}.",
                    f"Volume of prism with sides {a}, {b}, and {c} {unit}",
                    format_with_unit(frac_latex(volume), unit, power=3),
                )
            area = a * b if self.mode == "fraction_rectangle" else a * b / 2
            shape = "rectangle" if self.mode == "fraction_rectangle" else "right triangle"
            figure = (
                rectangle_measure_svg(
                    format_measurement_text(str(a), unit),
                    format_measurement_text(str(b), unit),
                )
                if self.mode == "fraction_rectangle"
                else triangle_measure_svg(
                    format_measurement_text(str(a), unit),
                    format_measurement_text(str(b), unit),
                )
            )
            self._metadata = {"diagram_svg": figure}
            return (
                f"\\text{{Find the area of the {shape} with base }} "
                f"{format_with_unit(frac_latex(a), unit)} "
                f"\\text{{ and height }} {format_with_unit(frac_latex(b), unit)}.",
                f"Area of {shape}: base {a} {unit}, height {b} {unit}",
                format_with_unit(frac_latex(area), unit, power=2),
            )

        if self.mode in {"tape", "hanger", "inequality_hanger"}:
            inequality = self.mode == "inequality_hanger"
            if self.mode == "tape":
                return self._build_tape_diagram(settings)

            parts = random.randint(2, 5)
            solution = random.randint(2, 12)
            total = parts * solution
            self._metadata = {
                "diagram_svg": hanger_svg(parts, total, inequality=inequality)
            }
            relation = "\\le" if inequality else "="
            answer_relation = "\\le" if inequality else "="
            return (
                f"\\text{{Use the diagram to solve }} {parts}x {relation} {total}.",
                f"Solve {parts}x {'<=' if inequality else '='} {total}",
                f"x {answer_relation} {solution}" if inequality else str(solution),
            )

        if self.mode == "area_model_algebraic":
            outer = random.randint(2, 8)
            constant = random.randint(2, 9)
            self._metadata = {"diagram_svg": area_model_svg(str(outer), "x", str(constant))}
            return (
                f"\\text{{Use the area model to expand }} {outer}(x + {constant}).",
                f"Expand {outer}(x + {constant})",
                f"{format_linear_latex(outer, outer * constant)}",
            )

        if self.mode in {"grid_polygon", "shaded_polygon"}:
            points, area = _random_grid_polygon(settings)
            self._metadata = {
                "diagram_svg": grid_polygon_svg(
                    points, shaded=self.mode == "shaded_polygon"
                )
            }
            noun = "shaded region" if self.mode == "shaded_polygon" else "polygon"
            return (
                f"\\text{{Find the area of the {noun} on the grid.}}",
                f"Area of the {noun} on the grid ({points})",
                _format_grid_area_answer(area),
            )

        if self.mode in {"nets", "net_surface", "net_grid", "invalid_net"}:
            invalid = self.mode == "invalid_net"
            side = random.randint(2, 8)
            self._metadata = {"diagram_svg": cube_net_svg(side, invalid=invalid)}
            if self.mode == "invalid_net":
                return (
                    "\\text{Does this arrangement form a valid net for a cube?}",
                    "Is this a valid cube net?",
                    "\\text{No}",
                )
            if self.mode == "nets":
                return (
                    "\\text{This net folds to make what solid?}",
                    "Identify the solid made by this net",
                    "\\text{cube}",
                )
            return (
                f"\\text{{The net is for a cube with edge length }} {side}\\text{{ units. Find its surface area.}}",
                f"Surface area of cube net with edge {side}",
                f"{6 * side * side}\\text{{ square units}}",
            )

        if self.mode in {"isometric", "isometric_measure"}:
            length, width, height = (random.randint(2, 5) for _ in range(3))
            self._metadata = {"diagram_svg": prism_svg(str(length), str(width), str(height))}
            if self.mode == "isometric":
                return (
                    "\\text{Sketch/copy the rectangular prism shown in the isometric drawing.}",
                    "Sketch the rectangular prism shown",
                    None,
                )
            volume = length * width * height
            surface = 2 * (length * width + length * height + width * height)
            ask_volume = random.choice([True, False])
            return (
                f"\\text{{Use the drawing to find the {'volume' if ask_volume else 'surface area'}.}}",
                "Measure the rectangular prism shown",
                f"{volume}\\text{{ cubic units}}" if ask_volume else f"{surface}\\text{{ square units}}",
            )

        if self.mode == "classify_polyhedron":
            kind = random.choice(POLYHEDRON_KINDS)
            answer = rf"\text{{{kind}}}"
            distractors = [
                rf"\text{{{other}}}" for other in POLYHEDRON_KINDS if other != kind
            ]
            random.shuffle(distractors)
            self._metadata = {
                "diagram_svg": polyhedron_svg(kind),
                "mc_distractors": distractors[:3],
            }
            return (
                "\\text{Classify the polyhedron shown.}",
                f"Classify the polyhedron ({kind})",
                answer,
            )

        if self.mode in {"draw_dot_plot", "draw_histogram"}:
            values = [random.randint(1, 12) for _ in range(random.randint(6, 10))]
            listed = ",\\ ".join(str(v) for v in values)
            include_axis = bool(settings.get("include_axis", True))
            lo, hi = min(values), max(values)
            bins = [(float(i), float(i + 2)) for i in range(lo - lo % 2, hi + 2, 2)]

            if self.mode == "draw_dot_plot":
                label = "dot plot"
                completed = dot_plot_svg(values, title="Dot plot")
                if include_axis:
                    self._metadata = {
                        "diagram_svg": dot_plot_svg(
                            values,
                            title="Dot plot",
                            blank=True,
                            tick_min=lo,
                            tick_max=hi,
                        ),
                        "answer_diagram_svg": completed,
                    }
                else:
                    self._metadata = {"answer_diagram_svg": completed}
            else:
                label = "histogram"
                completed = histogram_svg(values, bins, title="Histogram")
                if include_axis:
                    self._metadata = {
                        "diagram_svg": histogram_svg(
                            values, bins, title="Histogram", blank=True
                        ),
                        "answer_diagram_svg": completed,
                    }
                else:
                    self._metadata = {"answer_diagram_svg": completed}

            axis_hint = (
                r" \text{Use the blank axis provided.}"
                if include_axis
                else ""
            )
            return (
                f"\\text{{Create a {label} for the data set }} \\{{{listed}\\}}."
                f"{axis_hint}",
                f"Create a {label} for {values}",
                r"\text{(see figure)}",
            )
        raise ValueError(f"Unknown Grade 6 visual mode: {self.mode}")

    def _build_tape_diagram(self, settings: dict) -> tuple[str, str, str | None]:
        """Uniform equal-x boxes or non-uniform segments with one missing piece."""
        from ..diagrams.grade6_figures import tape_svg

        tier = _difficulty_band(settings)
        forced = str(settings.get("tape_style") or "").strip().lower()
        if forced in {"uniform", "nonuniform"}:
            style = forced
        elif forced == "mixed" or tier == "medium":
            style = random.choice(["uniform", "nonuniform"])
        elif tier == "easy":
            style = "uniform"
        elif tier == "hard":
            style = "nonuniform"
        else:
            style = random.choice(["uniform", "nonuniform"])

        if style == "uniform":
            if tier == "easy":
                parts = random.randint(2, 3)
                solution = random.randint(2, 8)
            elif tier == "hard":
                parts = random.randint(3, 6)
                solution = random.randint(4, 15)
            else:
                parts = random.randint(2, 5)
                solution = random.randint(2, 12)
            total = parts * solution
            self._metadata = {
                "diagram_svg": tape_svg(
                    labels=["x"] * parts,
                    total=total,
                    weights=[1.0] * parts,
                    title="Equal-size parts",
                )
            }
            return (
                f"\\text{{Use the tape diagram to find }} x.",
                f"Solve {parts}x = {total}",
                str(solution),
            )

        # Non-uniform: known sizes inside segments, one missing piece.
        if tier == "hard":
            n_segs = random.randint(3, 5)
            value_lo, value_hi = 4, 28
        else:
            n_segs = random.randint(3, 4)
            value_lo, value_hi = 2, 16

        values = [random.randint(value_lo, value_hi) for _ in range(n_segs)]
        # Keep segments visibly distinct so proportional widths read clearly.
        for i in range(1, n_segs):
            while values[i] == values[i - 1]:
                values[i] = random.randint(value_lo, value_hi)
        missing_i = random.randrange(n_segs)
        missing = values[missing_i]
        total = sum(values)
        labels = ["?" if i == missing_i else str(v) for i, v in enumerate(values)]
        self._metadata = {
            "diagram_svg": tape_svg(
                labels=labels,
                total=total,
                weights=[float(v) for v in values],
                title="Find the missing part",
            )
        }
        return (
            "\\text{Use the tape diagram to find the missing value.}",
            f"Missing part in tape totaling {total}",
            str(missing),
        )

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None
    ) -> dict[str, object]:
        return dict(self._metadata)


_INTRO_PERCENT_BENCHMARK = (10, 25, 50, 75)
_INTRO_PERCENT_EASY = (10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90)
_INTRO_PERCENT_MID = tuple(range(5, 101, 5))
_INTRO_PERCENT_AWKWARD = tuple(p for p in range(1, 100) if p % 5 != 0)
# Non-100 grids used at hard-but-doable D: (rows, cols) where many exact %-cell pairs exist.
_INTRO_PERCENT_PROP_GRIDS = ((5, 5), (4, 5), (5, 4), (5, 8), (8, 5), (2, 10))


def _intro_exact_grid_percents(rows: int, cols: int) -> list[int]:
    """Integer percents that land on a whole number of cells of an R×C grid."""
    total = rows * cols
    out: list[int] = []
    for k in range(1, total):
        if (100 * k) % total == 0:
            pct = (100 * k) // total
            if 1 <= pct <= 99:
                out.append(pct)
    return out


def _intro_percent_pick_awkward() -> int:
    return random.choice(_INTRO_PERCENT_AWKWARD)


def _intro_percent_ladder(settings: dict) -> dict[str, Any]:
    """Visual intro-to-percents ladder by continuous D.

    - D≈0: benchmark % on a hundred grid
    - mid: awkward % on a hundred grid / simple bar (classroom shade-46%)
    - D≈40: hard-but-doable — non-100 grids (proportion) / awkward circle-bar
    - D≫40 (incl. 1000): multi-panel + weird grids / no helpful ticks (not a
      normal classroom item). Shade-% does not grow forever; extreme D escalates
      *structure*, not the percent value itself.
    """
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = max(0.0, settings_difficulty(settings, default=0.0))

    # --- Easy: benchmarks on hundred grid ---------------------------------
    if d <= 4.0 + 1e-9:
        percent = random.choice(_INTRO_PERCENT_BENCHMARK)
        return {
            "mode": "single",
            "percent": percent,
            "figure": "hundred_grid",
            "rows": 10,
            "cols": 10,
        }

    # --- Low-mid: familiar multiples of 5 on grid/bar ---------------------
    if d <= 8.0 + 1e-9:
        mid_pool = [p for p in _INTRO_PERCENT_MID if p not in {10, 25, 50, 75, 100}]
        percent = random.choice(mid_pool or list(_INTRO_PERCENT_EASY))
        figure = random.choice(["hundred_grid", "hundred_grid", "bar"])
        return {
            "mode": "single",
            "percent": percent,
            "figure": figure,
            "rows": 10,
            "cols": 10,
            "segments": 10,
        }

    # --- Mid classroom: awkward % on hundred grid / bar -------------------
    if d <= 16.0 + 1e-9:
        percent = _intro_percent_pick_awkward()
        figure = random.choice(["hundred_grid", "hundred_grid", "bar"])
        return {
            "mode": "single",
            "percent": percent,
            "figure": figure,
            "rows": 10,
            "cols": 10,
            "segments": 10,
        }

    # --- Hard classroom (~D20): awkward % + circle estimation -------------
    if d <= 28.0 + 1e-9:
        percent = _intro_percent_pick_awkward()
        figure = random.choice(["bar", "circle", "circle", "hundred_grid"])
        segments = random.choice([8, 10, 10]) if figure == "bar" else 10
        return {
            "mode": "single",
            "percent": percent,
            "figure": figure,
            "rows": 10,
            "cols": 10,
            "segments": segments,
            "show_ticks": True,
        }

    # --- Hard-but-doable (~D40): non-100 grids requiring proportion -------
    if d <= 80.0 + 1e-9:
        roll = random.random()
        if roll < 0.55:
            rows, cols = random.choice(_INTRO_PERCENT_PROP_GRIDS)
            pool = _intro_exact_grid_percents(rows, cols)
            # Prefer percents that are not the easy benchmarks.
            awkwardish = [p for p in pool if p not in {10, 20, 25, 50, 75}]
            percent = random.choice(awkwardish or pool or [40])
            return {
                "mode": "single",
                "percent": percent,
                "figure": "grid",
                "rows": rows,
                "cols": cols,
            }
        percent = _intro_percent_pick_awkward()
        figure = random.choice(["circle", "circle", "bar"])
        return {
            "mode": "single",
            "percent": percent,
            "figure": figure,
            "segments": random.choice([7, 8, 9]) if figure == "bar" else 10,
            "show_ticks": True,
            "label_ticks": figure != "bar" or random.random() < 0.5,
        }

    # --- Extreme / unreasonable: multi-panel + hostile figures ------------
    n_panels = 3 if d >= 200 else 2
    panels: list[dict[str, Any]] = []
    used_pcts: set[int] = set()
    for i in range(n_panels):
        kind_roll = random.random()
        pct = _intro_percent_pick_awkward()
        # Prefer distinct panel targets so extreme items aren't a repeated shade-N%.
        for _ in range(12):
            if pct not in used_pcts:
                break
            pct = _intro_percent_pick_awkward()
        used_pcts.add(pct)
        if kind_roll < 0.4:
            # Weird grids where % rarely lands on a whole cell.
            rows, cols = random.choice(((7, 9), (7, 11), (6, 11), (8, 9), (13, 7)))
            panels.append(
                {
                    "figure": "grid",
                    "percent": pct,
                    "rows": rows,
                    "cols": cols,
                    "label": f"{pct}%",
                    "title": f"Figure {i + 1}: {rows}×{cols}",
                }
            )
        elif kind_roll < 0.7:
            panels.append(
                {
                    "figure": "circle",
                    "percent": pct,
                    "show_ticks": False,
                    "label": f"{pct}%",
                }
            )
        else:
            panels.append(
                {
                    "figure": "bar",
                    "percent": pct,
                    "segments": random.choice([7, 11, 13]),
                    "label_ticks": False,
                    "label": f"{pct}%",
                }
            )
    return {
        "mode": "multi",
        "percent": int(panels[0]["percent"]),
        "panels": panels,
        "figure": "multi",
    }


class IntroductionToPercentsFramework(NumberFramework):
    """Shade a blank figure to represent a given percent (visual percent meaning)."""

    def __init__(self) -> None:
        self._metadata: dict[str, object] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from ..diagrams.grade6_figures import (
            percent_bar_svg,
            percent_circle_svg,
            percent_grid_svg,
            percent_hundred_grid_svg,
            percent_multi_panel_svg,
        )

        spec = _intro_percent_ladder(settings)
        mode = str(spec.get("mode", "single"))

        if mode == "multi":
            panels = list(spec["panels"])  # type: ignore[arg-type]
            blank_svg = percent_multi_panel_svg(panels, blank=True)
            shaded_svg = percent_multi_panel_svg(panels, blank=False)
            pcts = [int(p["percent"]) for p in panels]
            pct_latex = ";\\,".join(f"{p}\\%" for p in pcts)
            pct_text = "; ".join(f"{p}%" for p in pcts)
            self._metadata = {
                "diagram_svg": blank_svg,
                "answer_diagram_svg": shaded_svg,
                "diagram_spec": {
                    "kind": "percent_shade",
                    "figure": "multi",
                    "panels": panels,
                    "percent": pcts[0],
                    "percents": pcts,
                },
                "stimulus": {
                    "kind": "percent_shade",
                    "figure": "multi",
                    "percent": pcts[0],
                    "percents": pcts,
                    "panels": panels,
                },
            }
            return (
                r"\text{Shade each figure to represent the labeled percent.}",
                f"Shade each figure to represent {pct_text}",
                pct_latex,
            )

        percent = int(spec["percent"])
        figure = str(spec.get("figure", "hundred_grid"))
        rows = int(spec.get("rows", 10))
        cols = int(spec.get("cols", 10))
        segments = int(spec.get("segments", 10))
        show_ticks = bool(spec.get("show_ticks", True))
        label_ticks = bool(spec.get("label_ticks", True))

        if figure in {"grid", "hundred_grid"}:
            if figure == "hundred_grid" or (rows == 10 and cols == 10):
                blank_svg = percent_hundred_grid_svg(percent, blank=True)
                shaded_svg = percent_hundred_grid_svg(percent, blank=False)
                figure_out = "hundred_grid"
                figure_label = "100-square grid"
            else:
                blank_svg = percent_grid_svg(
                    percent, blank=True, rows=rows, cols=cols
                )
                shaded_svg = percent_grid_svg(
                    percent, blank=False, rows=rows, cols=cols
                )
                figure_out = "grid"
                figure_label = f"{rows}×{cols} grid"
        elif figure == "bar":
            blank_svg = percent_bar_svg(
                percent, blank=True, segments=segments, label_ticks=label_ticks
            )
            shaded_svg = percent_bar_svg(
                percent, blank=False, segments=segments, label_ticks=label_ticks
            )
            figure_out = "bar"
            figure_label = "percent bar"
        else:
            blank_svg = percent_circle_svg(
                percent, blank=True, show_ticks=show_ticks
            )
            shaded_svg = percent_circle_svg(
                percent, blank=False, show_ticks=show_ticks
            )
            figure_out = "circle"
            figure_label = "circle"

        stimulus: dict[str, object] = {
            "kind": "percent_shade",
            "figure": figure_out,
            "percent": percent,
        }
        if figure_out in {"grid", "hundred_grid"}:
            stimulus["rows"] = rows
            stimulus["cols"] = cols
        if figure_out == "bar":
            stimulus["segments"] = segments

        self._metadata = {
            "diagram_svg": blank_svg,
            "answer_diagram_svg": shaded_svg,
            "diagram_spec": {
                "kind": "percent_shade",
                "figure": figure_out,
                "percent": percent,
                **(
                    {"rows": rows, "cols": cols}
                    if figure_out in {"grid", "hundred_grid"}
                    else {}
                ),
            },
            "stimulus": stimulus,
        }
        return (
            f"\\text{{Shade the figure to represent }} {percent}\\%.",
            f"Shade the {figure_label} to represent {percent}%",
            f"{percent}\\%",
        )

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None
    ) -> dict[str, object]:
        return dict(self._metadata)


# ---------------------------------------------------------------------------
# Sets of numbers (natural / whole / integer / rational / irrational / real)
# ---------------------------------------------------------------------------

_SET_ORDER = ("natural", "whole", "integer", "rational", "irrational", "real")

_SET_DISPLAY = {
    "natural": "natural",
    "whole": "whole",
    "integer": "integer",
    "rational": "rational",
    "irrational": "irrational",
    "real": "real",
}

_IRRATIONAL_POOL: tuple[tuple[str, str], ...] = (
    (r"\sqrt{2}", "√2"),
    (r"\sqrt{3}", "√3"),
    (r"\sqrt{5}", "√5"),
    (r"\sqrt{7}", "√7"),
    (r"\sqrt{11}", "√11"),
    (r"\pi", "π"),
    (r"2\pi", "2π"),
    (r"\frac{\pi}{2}", "π/2"),
    (r"e", "e"),
    (r"\sqrt[3]{2}", "∛2"),
    (r"1 + \sqrt{2}", "1 + √2"),
    (r"-\sqrt{2}", "-√2"),
)


@dataclass(frozen=True)
class _NumberExample:
    """A concrete number plus its most-specific kind."""

    latex: str
    text: str
    # Most specific: natural | whole | integer | rational | irrational
    kind: str


def _enabled_sets(settings: dict) -> list[str]:
    enabled = [
        name
        for name in _SET_ORDER
        if bool(settings.get(f"include_{name}", True))
    ]
    if not enabled:
        return ["integer", "rational", "real"]
    return enabled


def _membership(example: _NumberExample, set_name: str) -> bool:
    kind = example.kind
    if set_name == "natural":
        return kind == "natural"
    if set_name == "whole":
        return kind in {"natural", "whole"}
    if set_name == "integer":
        return kind in {"natural", "whole", "integer"}
    if set_name == "rational":
        return kind != "irrational"
    if set_name == "irrational":
        return kind == "irrational"
    if set_name == "real":
        return True
    return False


def _sets_for_example(example: _NumberExample, enabled: list[str]) -> list[str]:
    return [name for name in enabled if _membership(example, name)]


def _format_set_list(names: list[str]) -> str:
    labels = [_SET_DISPLAY[n] for n in names]
    if not labels:
        return r"\text{(none)}"
    return r"\text{" + ", ".join(labels) + "}"


def _make_natural(settings: dict) -> _NumberExample:
    lo, hi = _int_bounds(settings)
    lo = max(1, lo)
    hi = max(lo, hi)
    n = random.randint(lo, hi)
    return _NumberExample(str(n), str(n), "natural")


def _make_whole(settings: dict) -> _NumberExample:
    if random.random() < 0.4:
        return _NumberExample("0", "0", "whole")
    return _make_natural(settings)


def _make_integer(settings: dict) -> _NumberExample:
    lo, hi = _int_bounds(settings)
    allow_negative = bool(settings.get("allow_negative", True))
    if allow_negative and lo < 0:
        # Prefer a non-whole integer so classification is interesting.
        n = random.randint(min(lo, -1), -1)
        return _NumberExample(str(n), str(n), "integer")
    # Fall back to a whole number if negatives are off.
    return _make_whole(settings)


def _make_rational(settings: dict) -> _NumberExample:
    allow_negative = bool(settings.get("allow_negative", True))
    if bool(settings.get("allow_fractions", True)) and random.random() < 0.65:
        frac = random_fraction(
            num_min=-9 if allow_negative else 1,
            num_max=9,
            denom_min=2,
            denom_max=9,
            allow_negative=allow_negative,
        )
        # Ensure non-integer.
        while frac.denominator == 1:
            frac = random_fraction(
                num_min=-9 if allow_negative else 1,
                num_max=9,
                denom_min=2,
                denom_max=9,
                allow_negative=allow_negative,
            )
        return _NumberExample(frac_latex(frac), str(frac), "rational")

    # Terminating / repeating decimal that is rational but not an integer.
    tenths = random.randint(1, 9)
    sign = -1 if allow_negative and random.random() < 0.35 else 1
    whole = random.randint(0, 8)
    value = sign * (whole + tenths / 10)
    text = f"{value:g}"
    if "." not in text:
        text = f"{value:.1f}"
    latex = text
    return _NumberExample(latex, text, "rational")


def _make_irrational(settings: dict) -> _NumberExample:
    allow_negative = bool(settings.get("allow_negative", True))
    pool = list(_IRRATIONAL_POOL)
    if not allow_negative:
        pool = [(latex, text) for latex, text in pool if not latex.startswith("-")]
    latex, text = random.choice(pool)
    return _NumberExample(latex, text, "irrational")


def _example_factories(settings: dict) -> list[tuple[str, Any]]:
    """Return (kind, factory) pairs that settings currently allow."""
    factories: list[tuple[str, Any]] = [
        ("natural", lambda: _make_natural(settings)),
        ("whole", lambda: _make_whole(settings)),
        ("integer", lambda: _make_integer(settings)),
    ]
    if bool(settings.get("allow_fractions", True)):
        factories.append(("rational", lambda: _make_rational(settings)))
    if bool(settings.get("allow_irrationals", True)) and bool(
        settings.get("include_irrational", True)
    ):
        factories.append(("irrational", lambda: _make_irrational(settings)))
    return factories


def _random_example(settings: dict, *, prefer_kind: str | None = None) -> _NumberExample:
    factories = _example_factories(settings)
    if prefer_kind:
        matched = [f for kind, f in factories if kind == prefer_kind]
        if matched:
            return matched[0]()
    return random.choice(factories)[1]()


def _resolve_ask_mode(settings: dict) -> str:
    mode = str(settings.get("ask_mode", "mixed")).strip().lower()
    if mode == "mixed":
        return random.choice(["classify", "pick", "membership"])
    if mode in {"classify", "pick", "membership"}:
        return mode
    return "classify"


class SetsOfNumbersFramework(NumberFramework):
    """Classify numbers into standard number sets."""

    instruction_latex = r"\text{To which set(s) of numbers does each number belong?}"
    instruction_text = "To which set(s) of numbers does each number belong?"

    def __init__(self) -> None:
        self._last_distractors: list[str] = []

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        self._last_distractors = []
        mode = _resolve_ask_mode(settings)
        enabled = _enabled_sets(settings)

        if mode == "pick":
            return self._build_pick(settings, enabled)
        if mode == "membership":
            return self._build_membership(settings, enabled)
        return self._build_classify(settings, enabled)

    def _build_classify(
        self, settings: dict, enabled: list[str]
    ) -> tuple[str, str, str | None]:
        example = _random_example(settings)
        belonging = _sets_for_example(example, enabled)
        answer = _format_set_list(belonging)
        # Distractors: other plausible set-list answers.
        distractors: list[str] = []
        for _ in range(8):
            other = _random_example(settings)
            other_sets = _format_set_list(_sets_for_example(other, enabled))
            if other_sets != answer and other_sets not in distractors:
                distractors.append(other_sets)
            if len(distractors) >= 3:
                break
        self._last_distractors = distractors
        prompt_latex = example.latex
        prompt_text = f"Classify {example.text}"
        return prompt_latex, prompt_text, answer

    def _build_pick(
        self, settings: dict, enabled: list[str]
    ) -> tuple[str, str, str | None]:
        allow_fractions = bool(settings.get("allow_fractions", True))
        allow_irrationals = bool(settings.get("allow_irrationals", True)) and bool(
            settings.get("include_irrational", True)
        )
        allow_negative = bool(settings.get("allow_negative", True))

        # Only ask about sets where we can also generate clear counterexamples.
        candidates: list[str] = []
        if "irrational" in enabled and allow_irrationals:
            candidates.append("irrational")
        if "natural" in enabled and (allow_negative or allow_fractions or allow_irrationals):
            # Counterexamples: 0, negatives, fractions, irrationals.
            candidates.append("natural")
        if "whole" in enabled and (allow_negative or allow_fractions or allow_irrationals):
            candidates.append("whole")
        if "integer" in enabled and (allow_fractions or allow_irrationals):
            candidates.append("integer")
        if "rational" in enabled and allow_irrationals:
            # Without irrationals every generated value is rational.
            candidates.append("rational")
        if not candidates:
            # Fall back to classify-style when pick cannot produce contrast.
            return self._build_classify(settings, enabled)

        target_set = random.choice(candidates)

        if target_set == "irrational":
            target = _make_irrational(settings)
        elif target_set == "natural":
            target = _make_natural(settings)
        elif target_set == "whole":
            target = _make_whole(settings)
        elif target_set == "integer":
            target = _make_integer(settings)
        else:
            target = _make_rational(settings)

        options = [target]
        for _ in range(60):
            if len(options) >= 4:
                break
            candidate = _random_example(settings)
            if _membership(candidate, target_set):
                continue
            if any(c.latex == candidate.latex for c in options):
                continue
            options.append(candidate)

        # Guaranteed counterexamples if the random pool was unlucky.
        fallbacks: list[_NumberExample] = []
        if target_set == "irrational":
            fallbacks = [_make_natural(settings), _make_integer(settings), _make_rational(settings)]
        elif target_set == "rational":
            fallbacks = [_make_irrational(settings)] * 3
        elif target_set == "integer":
            if allow_fractions:
                fallbacks.append(_make_rational(settings))
            if allow_irrationals:
                fallbacks.append(_make_irrational(settings))
        elif target_set == "natural":
            fallbacks.append(_NumberExample("0", "0", "whole"))
            if allow_negative:
                fallbacks.append(_make_integer(settings))
            if allow_fractions:
                fallbacks.append(_make_rational(settings))
        elif target_set == "whole":
            if allow_negative:
                fallbacks.append(_make_integer(settings))
            if allow_fractions:
                fallbacks.append(_make_rational(settings))

        for filler in fallbacks:
            if len(options) >= 4:
                break
            if _membership(filler, target_set):
                continue
            if any(c.latex == filler.latex for c in options):
                continue
            options.append(filler)

        while len(options) < 4:
            # Last resort: distinct copies of a safe non-member label.
            options.append(_NumberExample(r"\pi", "π", "irrational") if allow_irrationals else _NumberExample("0.5", "0.5", "rational"))

        options = options[:4]
        random.shuffle(options)
        lines = [
            rf"\text{{{chr(65 + i)}. }} {opt.latex}"
            for i, opt in enumerate(options)
        ]
        prompt_latex = (
            rf"\text{{Which of the following is {_SET_DISPLAY[target_set]}?}}"
            + r" \\ "
            + r" \\ ".join(lines)
        )
        prompt_text = (
            f"Which of the following is {_SET_DISPLAY[target_set]}? "
            + "; ".join(f"{chr(65 + i)}. {opt.text}" for i, opt in enumerate(options))
        )
        answer = target.latex
        self._last_distractors = [o.latex for o in options if o.latex != target.latex]
        return prompt_latex, prompt_text, answer

    def _build_membership(
        self, settings: dict, enabled: list[str]
    ) -> tuple[str, str, str | None]:
        example = _random_example(settings)
        # Prefer a set that yields a non-trivial true/false (not always true for reals).
        claim_pool = [s for s in enabled if s != "real"] or enabled
        claim_set = random.choice(claim_pool)
        is_member = _membership(example, claim_set)
        # Occasionally force a false claim for variety when the random pick is true.
        if is_member and random.random() < 0.45 and len(claim_pool) > 1:
            false_sets = [s for s in claim_pool if not _membership(example, s)]
            if false_sets:
                claim_set = random.choice(false_sets)
                is_member = False

        truth = "True" if is_member else "False"
        set_label = _SET_DISPLAY[claim_set]
        article = "an" if set_label[0] in "aeiou" else "a"
        prompt_latex = (
            rf"\text{{True or false: }} {example.latex}"
            rf"\text{{ is {article} {set_label} number.}}"
        )
        prompt_text = f"True or false: {example.text} is {article} {set_label} number."
        answer = rf"\text{{{truth}}}"
        self._last_distractors = [r"\text{True}" if truth == "False" else r"\text{False}"]
        return prompt_latex, prompt_text, answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, object]:
        meta: dict[str, object] = {}
        if self._last_distractors:
            meta["mc_distractors"] = list(self._last_distractors)
        return meta

