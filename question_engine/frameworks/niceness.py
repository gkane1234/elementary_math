"""Niceness checks that scale with effective difficulty (finite bounds)."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any


@dataclass(frozen=True)
class NicenessBounds:
    max_abs_int: int
    max_denominator: int
    max_leaf_hint: int


def bounds_for_difficulty(effective_d: float, *, profile: str | None = None) -> NicenessBounds:
    """Finite caps that grow with D but stay classroom-bounded."""
    d = max(0.0, float(effective_d))
    max_abs = int(12 + 2 * d)
    max_den = int(4 + d)
    if profile in {"friendly_wholes", "signed_small"}:
        max_den = 1
        max_abs = int(6 + d) if profile == "friendly_wholes" else int(9 + 1.5 * d)
    elif profile == "unit_fractions":
        max_den = int(6 + d)
        max_abs = 1
    elif profile in {"simple_rations", "simple_rationals"}:
        max_den = int(6 + 0.75 * d)
        max_abs = int(9 + d)
    elif profile in {"difficult_rations", "ugly_rations", "difficult_rationals"}:
        max_den = int(12 + 1.5 * d)
        max_abs = int(20 + 2 * d)
    elif profile == "friendly_decimals":
        max_den = 100
        max_abs = int(8 + d)
    elif profile == "awkward_decimals":
        max_den = 1000
        max_abs = int(12 + 2 * d)
    max_leaf = int(4 + d)
    return NicenessBounds(
        max_abs_int=max(1, max_abs),
        max_denominator=max(1, max_den),
        max_leaf_hint=max(2, max_leaf),
    )


def fraction_is_nice(value: Fraction, bounds: NicenessBounds) -> bool:
    v = Fraction(value).limit_denominator()
    if abs(v.numerator) > bounds.max_abs_int * max(1, v.denominator):
        # Allow numerator a bit larger than abs bound when den > 1
        if abs(v.numerator) > bounds.max_abs_int * 4:
            return False
    if v.denominator > bounds.max_denominator:
        return False
    return True


def int_is_nice(value: int, bounds: NicenessBounds) -> bool:
    return abs(int(value)) <= bounds.max_abs_int


def assert_or_reject(ok: bool, reason: str) -> None:
    if not ok:
        raise NicenessError(reason)


class NicenessError(ValueError):
    """Raised when a sample violates niceness; callers degrade / retry."""
