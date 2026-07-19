"""Shared polynomial helpers — degree targeting, monomial atoms, coeff maps.

Degree is a **policy hard cap**, never bought with leftover D on linear leaves.
Under polynomial policy, D may unlock higher degrees up to ``policy.max_degree``:

    target_degree(D) = min(policy.max_degree, 2 + floor(log2(1 + D / DEGREE_SCALE)))
    DEGREE_SCALE = 4.0

So D ∈ [0, 4) → 2; [4, 12) → 3; [12, 28) → 4; … capped by policy.
Linear policy (max_degree ≤ 1) always returns 1.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import TYPE_CHECKING

from question_engine.frameworks.primitives._algebra_render import (
    join_signed_terms,
    num_latex,
    sample_integerish,
)

if TYPE_CHECKING:
    from question_engine.frameworks.primitives.expression_policy import ExpressionPolicy
    from question_engine.frameworks.primitives.registry import PrimitiveContext
    from question_engine.frameworks.primitives.variables import SampledVariable

DEGREE_SCALE = 4.0
TERM_SCALE = 1.5  # n_terms growth for poly combine / evaluate


def target_poly_degree(d: float, policy: ExpressionPolicy) -> int:
    """Effective degree for this item (≤ policy.max_degree)."""
    from question_engine.frameworks.primitives.difficulty_knobs import fget, iget

    cap = max(0, int(policy.max_degree))
    if cap <= 1:
        return min(1, cap) if cap >= 0 else 0
    d = max(0.0, float(d))
    scale = fget("polynomial", "degree_scale", DEGREE_SCALE)
    base = iget("polynomial", "base_degree", 2)
    extra = int(math.floor(math.log2(1.0 + d / scale)))
    return min(cap, base + extra)


def min_d_for_degree(degree: int) -> float:
    """Smallest D with ``target_poly_degree`` ≥ ``degree`` (ignoring policy cap)."""
    degree = max(2, int(degree))
    extra = degree - 2
    if extra <= 0:
        return 0.0
    return DEGREE_SCALE * (2**extra - 1)


def target_n_terms(d: float) -> int:
    """Term count: ``1 + floor(log2(1 + D / TERM_SCALE))``."""
    d = max(0.0, float(d))
    return 1 + int(math.floor(math.log2(1.0 + d / TERM_SCALE)))


def power_atom(var_latex: str, degree: int) -> str:
    """Monomial atom for degree ``n`` (empty string for constant)."""
    degree = int(degree)
    if degree <= 0:
        return ""
    if degree == 1:
        return var_latex
    return f"{var_latex}^{{{degree}}}"


def coeffs_to_parts(
    coeffs: dict[int, Fraction],
    var: SampledVariable,
    *,
    descending: bool = True,
) -> list[tuple[Fraction, str]]:
    """Map degree→coeff to ``(coeff, atom)`` display parts."""
    degrees = sorted(coeffs.keys(), reverse=descending)
    parts: list[tuple[Fraction, str]] = []
    for deg in degrees:
        c = coeffs[deg]
        if c == 0:
            continue
        parts.append((c, power_atom(var.latex, deg)))
    return parts


def render_poly(
    coeffs: dict[int, Fraction],
    var: SampledVariable,
    *,
    descending: bool = True,
) -> tuple[str, str]:
    return join_signed_terms(coeffs_to_parts(coeffs, var, descending=descending))


def poly_degree(coeffs: dict[int, Fraction]) -> int:
    degs = [d for d, c in coeffs.items() if c != 0]
    return max(degs) if degs else 0


def evaluate_poly(coeffs: dict[int, Fraction], x: Fraction) -> Fraction:
    total = Fraction(0)
    for deg, c in coeffs.items():
        if c == 0:
            continue
        total += c * (x**deg)
    return total


def sample_coeff(ctx: PrimitiveContext, *, exclude_zero: bool = True) -> Fraction:
    n = sample_integerish(ctx, exclude_zero=exclude_zero)
    return n.value


def sample_poly_coeffs(
    ctx: PrimitiveContext,
    *,
    degree: int,
    n_terms: int | None = None,
    require_leading: bool = True,
) -> dict[int, Fraction]:
    """Sample a sparse univariate polynomial at exact ``degree``."""
    degree = max(0, int(degree))
    if n_terms is None:
        n_terms = min(degree + 1, max(2, target_n_terms(ctx.topic_d)))
    n_terms = max(1, min(n_terms, degree + 1))

    degrees: list[int] = [degree] if require_leading and degree > 0 else []
    pool = list(range(0, degree if require_leading else degree + 1))
    ctx.rng.shuffle(pool)
    for d in pool:
        if len(degrees) >= n_terms:
            break
        if d not in degrees:
            degrees.append(d)
    # Ensure constant sometimes for nicer combine/evaluate.
    if 0 not in degrees and n_terms >= 2 and degree >= 1 and ctx.rng.random() < 0.55:
        if len(degrees) < n_terms:
            degrees.append(0)
        else:
            # Swap a middle term for constant.
            for i, d in enumerate(degrees):
                if d != degree:
                    degrees[i] = 0
                    break

    coeffs: dict[int, Fraction] = {}
    for d in degrees:
        coeffs[d] = sample_coeff(ctx, exclude_zero=True)
    if require_leading and degree > 0:
        coeffs[degree] = sample_coeff(ctx, exclude_zero=True)
        # Prefer positive leading at low D for naming topics.
        if coeffs[degree] < 0 and ctx.rng.random() < 0.55:
            coeffs[degree] = abs(coeffs[degree])
    return coeffs


def combine_coeff_maps(*maps: dict[int, Fraction]) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for m in maps:
        for d, c in m.items():
            out[d] = out.get(d, Fraction(0)) + c
    return {d: c for d, c in out.items() if c != 0}


def scale_coeffs(coeffs: dict[int, Fraction], k: Fraction) -> dict[int, Fraction]:
    return {d: c * k for d, c in coeffs.items() if c * k != 0}


def multiply_coeffs(
    a: dict[int, Fraction],
    b: dict[int, Fraction],
) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for d1, c1 in a.items():
        for d2, c2 in b.items():
            d = d1 + d2
            out[d] = out.get(d, Fraction(0)) + c1 * c2
    return {d: c for d, c in out.items() if c != 0}


def degree_name(degree: int) -> tuple[str, str]:
    """Return (latex, text) classification for a polynomial degree."""
    names = {
        0: (r"\text{constant}", "constant"),
        1: (r"\text{linear}", "linear"),
        2: (r"\text{quadratic}", "quadratic"),
        3: (r"\text{cubic}", "cubic"),
        4: (r"\text{quartic}", "quartic"),
        5: (r"\text{quintic}", "quintic"),
    }
    if degree in names:
        return names[degree]
    return (rf"\text{{degree-{degree}}}", f"degree-{degree}")


def wrap_parens(latex: str, text: str) -> tuple[str, str]:
    return f"\\left({latex}\\right)", f"({text})"
