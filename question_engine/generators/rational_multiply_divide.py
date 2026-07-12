"""Multiply / divide rational expressions with tiered structure and division forms."""

from __future__ import annotations

import random
from typing import Sequence

from packages.polynomial_core import Polynomial

from ..core.models import Question
from ..settings.params import allowed_division_notations
from .utils import make_questions


def _coef_bounds(settings: dict) -> tuple[int, int]:
    lo = int(settings.get("coef_min", -5))
    hi = int(settings.get("coef_max", 5))
    if lo > hi:
        lo, hi = hi, lo
    return lo, hi


def _leading_one(settings: dict) -> bool:
    return bool(
        settings.get("leading_coefficient_one", settings.get("monic_only", True))
    )


def _allowed_operations(settings: dict) -> list[str]:
    ops: list[str] = []
    if bool(settings.get("allow_multiply", True)):
        ops.append("multiply")
    if bool(settings.get("allow_divide", True)):
        ops.append("divide")
    return ops or ["multiply", "divide"]


def _simple_linear(
    coef_min: int,
    coef_max: int,
    *,
    monic: bool,
    used: Sequence[Polynomial] = (),
) -> Polynomial:
    """Content-primitive linear distinct from ``used``."""
    from math import gcd

    bound = max(1, min(5, abs(coef_min), abs(coef_max) or 5))
    for _ in range(100):
        leading = 1 if monic else random.randint(1, max(2, bound))
        constant = int(Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True))
        if gcd(abs(leading), abs(constant)) != 1:
            continue
        factor = Polynomial([leading, constant])
        if any(factor == other for other in used):
            continue
        return factor
    # Fallback: monic with unused constant
    for const in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5):
        factor = Polynomial([1, const])
        if not any(factor == other for other in used):
            return factor
    return Polynomial([1, random.choice([1, -1])])


def _factor_latex(poly: Polynomial, *, in_product: bool) -> str:
    latex = poly.to_latex()
    if poly.deg() == 0:
        return latex
    terms = [t for t in poly.terms if abs(float(t[0])) > 1e-12]
    if in_product and len(terms) > 1:
        return f"\\left({latex}\\right)"
    return latex


def _product_latex(factors: Sequence[Polynomial], *, expand: bool) -> str:
    if not factors:
        return "1"
    if expand:
        product = Polynomial([1])
        for factor in factors:
            product *= factor
        return product.to_latex()
    if len(factors) == 1:
        return _factor_latex(factors[0], in_product=False)
    return "".join(_factor_latex(f, in_product=True) for f in factors)


def _rational_latex(
    num_factors: Sequence[Polynomial],
    den_factors: Sequence[Polynomial],
    *,
    expand: bool,
) -> str:
    num = _product_latex(num_factors, expand=expand)
    den = _product_latex(den_factors, expand=expand)
    return f"\\frac{{{num}}}{{{den}}}"


def _factors_equal(left: Polynomial, right: Polynomial) -> bool:
    return left == right


def _cancel_factors(
    num_factors: list[Polynomial],
    den_factors: list[Polynomial],
) -> tuple[list[Polynomial], list[Polynomial]]:
    nums = list(num_factors)
    dens = list(den_factors)
    i = 0
    while i < len(nums):
        matched = None
        for j, den in enumerate(dens):
            if _factors_equal(nums[i], den):
                matched = j
                break
        if matched is None:
            i += 1
            continue
        nums.pop(i)
        dens.pop(matched)
    return nums, dens


def _root_of_linear(factor: Polynomial) -> int | None:
    """Integer root of ax+b when it exists."""
    if factor.deg() != 1:
        return None
    a = int(round(float(factor.coef(1))))
    b = int(round(float(factor.coef(0))))
    if a == 0 or b % a != 0:
        return None
    return -b // a


def _excluded_from_factors(factors: Sequence[Polynomial]) -> list[int]:
    excluded: list[int] = []
    for factor in factors:
        root = _root_of_linear(factor)
        if root is not None:
            excluded.append(root)
        elif factor.deg() == 2:
            # Expanded quadratic: scan small integer roots.
            for candidate in range(-12, 13):
                if abs(float(factor.evaluate(candidate))) < 1e-8:
                    excluded.append(candidate)
    return sorted(set(excluded))


def _answer_latex(
    num_factors: Sequence[Polynomial],
    den_factors: Sequence[Polynomial],
    *,
    excluded: Sequence[int] | None = None,
) -> str:
    from packages.polynomial_core import rational_excluded_values_latex

    nums, dens = _cancel_factors(list(num_factors), list(den_factors))
    if not dens:
        if not nums:
            body = "1"
        else:
            body = _product_latex(nums, expand=True)
    elif not nums:
        body = f"\\frac{{1}}{{{_product_latex(dens, expand=True)}}}"
    else:
        body = (
            f"\\frac{{{_product_latex(nums, expand=True)}}}"
            f"{{{_product_latex(dens, expand=True)}}}"
        )
    note = rational_excluded_values_latex(list(excluded or []))
    if note:
        return f"{body},\\; {note}"
    return body


def _format_multiply(operands: Sequence[str]) -> str:
    return " \\cdot ".join(operands)


def _format_divide(left: str, right: str, settings: dict) -> str:
    notation = random.choice(allowed_division_notations(settings))
    if notation == "complex_fraction":
        return f"\\frac{{{left}}}{{{right}}}"
    if notation == "slash":
        return f"\\left({left}\\right) / \\left({right}\\right)"
    return f"{left} \\div {right}"


def _unique_linears(
    count: int,
    settings: dict,
    *,
    seed: Sequence[Polynomial] = (),
) -> list[Polynomial]:
    coef_min, coef_max = _coef_bounds(settings)
    monic = _leading_one(settings)
    factors = list(seed)
    while len(factors) < count:
        factors.append(_simple_linear(coef_min, coef_max, monic=monic, used=factors))
    return factors


def _build_two_operand_problem(settings: dict) -> tuple[str, str]:
    """Build A/B ⋆ C/D with controlled shared cancellations."""
    cancel_count = max(0, int(settings.get("cancel_factor_count", 1)))
    expand = bool(settings.get("expand_polynomials", False))
    max_degree = max(1, int(settings.get("max_factor_degree", 1)))
    op = random.choice(_allowed_operations(settings))

    # Shared cancel factors + unique pieces.
    needed = cancel_count + 4  # leftovers for each of 4 slots
    pool = _unique_linears(needed, settings)
    shared = pool[:cancel_count]
    rest = pool[cancel_count:]

    # Left num / left den  and  right num / right den
    left_num = [rest[0]]
    left_den = [rest[1]]
    right_num = [rest[2]]
    right_den = [rest[3]]

    # Place shared factors so they cancel under multiply (or after reciprocal for divide).
    for i, shared_factor in enumerate(shared):
        if i % 2 == 0:
            # Cancels across: left_num with right_den (multiply) / left_num with right_num (divide)
            left_num.append(shared_factor)
            if op == "multiply":
                right_den.append(shared_factor)
            else:
                right_num.append(shared_factor)
        else:
            left_den.append(shared_factor)
            if op == "multiply":
                right_num.append(shared_factor)
            else:
                right_den.append(shared_factor)

    # Hard tier: optionally bundle two linears into an expanded quadratic display.
    if max_degree >= 2 and expand and len(left_num) >= 2:
        # Keep factors for answer math; display left num as expanded product of first two.
        pass  # handled by expand flag in latex

    left = _rational_latex(left_num, left_den, expand=expand and max_degree >= 2)
    right = _rational_latex(right_num, right_den, expand=expand and max_degree >= 2)

    if op == "multiply":
        prompt = _format_multiply([left, right])
        ans_num = left_num + right_num
        ans_den = left_den + right_den
        excluded = _excluded_from_factors(left_den + right_den)
    else:
        prompt = _format_divide(left, right, settings)
        # a/b ÷ c/d = (a/b)·(d/c)
        ans_num = left_num + right_den
        ans_den = left_den + right_num
        # Original dens plus the divisor numerator (becomes a denominator).
        excluded = _excluded_from_factors(left_den + right_den + right_num)

    return prompt, _answer_latex(ans_num, ans_den, excluded=excluded)


def _build_three_operand_multiply(settings: dict) -> tuple[str, str]:
    """Three rational factors multiplied; at least one shared cancellation."""
    cancel_count = max(1, int(settings.get("cancel_factor_count", 2)))
    expand = bool(settings.get("expand_polynomials", False))
    max_degree = max(1, int(settings.get("max_factor_degree", 1)))

    pool = _unique_linears(cancel_count + 6, settings)
    shared = pool[:cancel_count]
    rest = pool[cancel_count:]

    a_num, a_den = [rest[0]], [rest[1]]
    b_num, b_den = [rest[2]], [rest[3]]
    c_num, c_den = [rest[4]], [rest[5]]

    # Wire shared factors across consecutive pairs.
    for i, shared_factor in enumerate(shared):
        if i % 3 == 0:
            a_num.append(shared_factor)
            b_den.append(shared_factor)
        elif i % 3 == 1:
            b_num.append(shared_factor)
            c_den.append(shared_factor)
        else:
            a_den.append(shared_factor)
            c_num.append(shared_factor)

    use_expand = expand and max_degree >= 2
    operands = [
        _rational_latex(a_num, a_den, expand=use_expand),
        _rational_latex(b_num, b_den, expand=use_expand),
        _rational_latex(c_num, c_den, expand=use_expand),
    ]
    prompt = _format_multiply(operands)
    answer = _answer_latex(
        a_num + b_num + c_num,
        a_den + b_den + c_den,
        excluded=_excluded_from_factors(a_den + b_den + c_den),
    )
    return prompt, answer


def build_rational_multiply_divide_prompt(settings: dict) -> tuple[str, str, str | None]:
    """Return (prompt_latex, kind, answer_latex|None)."""
    include_answer_key = bool(settings.get("include_answer_key", False))
    operand_count = max(2, min(3, int(settings.get("operand_count", 2))))
    ops = _allowed_operations(settings)

    # Three-operand form is multiply-only; fall back to two if divide-only.
    if operand_count >= 3 and "multiply" in ops and (
        "divide" not in ops or random.random() < 0.7
    ):
        prompt, answer = _build_three_operand_multiply(settings)
    else:
        prompt, answer = _build_two_operand_problem(settings)

    return prompt, "rational multiply/divide", answer if include_answer_key else None


def generate_rational_expression_multiply_divide(
    topic: str, settings: dict
) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        return build_rational_multiply_divide_prompt(settings)

    return make_questions(topic, count, include_answer_key, build, settings=settings)
