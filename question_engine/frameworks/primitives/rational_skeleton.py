"""Rational skeleton patterns — A1 cancel family (goal → inflate → package).

Species
-------
- **AddSubCancel** — ± sum via PFD + optional 2D residual kernel.
- **SimplifyCancel** — single-fraction simplify (same inflate, no PFD split).
- **MulDivCancel** — product/quotient with cross-operand cancels.
- **ComplexFracCancel** — nested complex fraction (display opt-out).

Shared pipeline
---------------
1. Sample factors via ``factor_sampler`` (constraint box + D bias).
2. Assign k ∈ {0,1,2} factors to cancel vs remain (deg D ≤ 2).
3. Build goal G (fraction or constant if full cancel).
4. Inflate R = G · Π (cᵢ/cᵢ) (species-specific packaging of R).
5. **Display rules** (presentation only): default preset ``standard_rational``
   rewrites nested ``(p/q)/linear`` → ``p/(q·linear)`` without distributing
   when intent is missing/None/``atomic_pf_term``. Opt-out intents
   (``complex_fraction_skill`` / ``as_built``) skip structure-changing rules.

AddSubCancel extras
-------------------
5. Package via atomic PFD + optional **2D residual kernel** K(x)/D = (a+bx)/D.
6. Rebalance so packaged sum = R; flesh dens factored/expanded.
7. **Clear fractional PF/kernel coeffs**: if any packaged numerator coeff is
   non-integer, multiply every summand (and R, G, K) by
   ``M = lcm(denominators)`` so the student sees integer numerators.
   Packaged sum equals ``M·R``; after combine+cancel the answer is ``M·G``.
   When all coeffs are already integers, ``M = 1`` and answer remains ``G``.

Excluded values (answer ``x ≠ …`` note)
----------------------------------------
Only roots of **cancelled** factors (removable discontinuities): original den
zeros that do **not** appear in the final simplified denominator. Poles that
remain in the goal den are omitted — they are already visible in the answer.
With ``k=0`` (no cancel) the exclusion list is empty; with full cancel every
original den root is listed.

Kernel policy (multidimensional, simplicity-biased at low D)
-----------------------------------------------------------
Kernel is up to 2 parameters ``(a, b)`` for ``(a + b x)/D`` when deg D = 2
(when deg D = 1, only constant ``a`` is proper).

At easier D: nonzero / multidim kernel is **less likely**. When a nonzero
kernel is drawn, prefer simple options: ``K=0``, or ``b=0`` (constant-only),
or ``a=0`` (pure ``bx/D``) — simple as an option, not forced complex.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm
from typing import Any, Literal

from question_engine.frameworks.primitives._algebra_render import (
    join_signed_terms,
    num_latex,
)
from question_engine.frameworks.primitives.factor_sampler import (
    FactorConstraints,
    FactorDraw,
    LinearFactor,
    constraints_from_settings,
    render_factor,
    render_factor_product,
    sample_factor_product,
    sample_linear_factor,
)
from question_engine.frameworks.primitives.poly_helpers import (
    multiply_coeffs,
    poly_degree,
    render_poly,
    scale_coeffs,
)
from question_engine.frameworks.primitives.rational_display import (
    DisplayIntent,
    apply_leading_den_coef,
    plan_fraction_display,
    resolve_display_config,
)
from question_engine.frameworks.primitives.registry import PrimitiveContext

MAX_CANCEL_K = 2
MAX_DEN_DEGREE = 2


@dataclass(frozen=True)
class RationalSkeletonCaps:
    """Difficulty-scaled caps — low D keeps the phase-0/1 box; high D unlocks old-path richness."""

    max_cancel_k: int
    max_inventory_factors: int
    max_answer_den_degree: int
    prefer_factored_prompt: bool
    insert_cancel_pairs: bool


def rational_skeleton_caps(
    d: float,
    settings: dict[str, Any] | None = None,
) -> RationalSkeletonCaps:
    """Map D → cancel/inventory caps (answer den still ≤ ``MAX_DEN_DEGREE``).

    Format unlocks are tiered: low D keeps the phase-0/1 box with only numeric
    hardness; higher D adds one structural dimension at a time (see
    ``skeleton_difficulty.format_tier``).
    """
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        SkeletonDifficultyBands,
        format_bias_for_tier,
    )

    s = dict(settings or {})
    if str(s.get("skeleton_rational_caps", "")).strip().lower() in {"phase01", "strict"}:
        return RationalSkeletonCaps(
            max_cancel_k=MAX_CANCEL_K,
            max_inventory_factors=MAX_DEN_DEGREE,
            max_answer_den_degree=MAX_DEN_DEGREE,
            prefer_factored_prompt=False,
            insert_cancel_pairs=False,
        )
    bands = SkeletonDifficultyBands.from_d(d)
    ft = bands.format_tier
    fmt = format_bias_for_tier(ft)
    if ft <= 1:
        return RationalSkeletonCaps(
            max_cancel_k=MAX_CANCEL_K,
            max_inventory_factors=MAX_DEN_DEGREE,
            max_answer_den_degree=MAX_DEN_DEGREE,
            prefer_factored_prompt=bool(fmt["prefer_factored_prompt"]),
            insert_cancel_pairs=False,
        )
    if ft == 2:
        return RationalSkeletonCaps(
            max_cancel_k=3,
            max_inventory_factors=3,
            max_answer_den_degree=MAX_DEN_DEGREE,
            prefer_factored_prompt=True,
            insert_cancel_pairs=True,
        )
    return RationalSkeletonCaps(
        max_cancel_k=4,
        max_inventory_factors=4,
        max_answer_den_degree=MAX_DEN_DEGREE,
        prefer_factored_prompt=True,
        insert_cancel_pairs=True,
    )


def _widen_cons_for_caps(
    cons: FactorConstraints,
    caps: RationalSkeletonCaps,
) -> FactorConstraints:
    """Raise inventory box when high-D caps exceed the default rational-lane degree-2 box."""
    if caps.max_inventory_factors <= cons.max_factors:
        return cons
    cap = caps.max_inventory_factors
    from dataclasses import replace

    return replace(
        cons,
        min_factors=min(cons.min_factors, cap),
        max_factors=cap,
        max_product_degree=cap,
    ).clamped()


PackageMode = Literal["pure_pfd", "residual"]
GoalMode = Literal["fraction", "constant"]


# ---------------------------------------------------------------------------
# Poly helpers (local, Fraction maps)
# ---------------------------------------------------------------------------


def _poly_add(p: dict[int, Fraction], q: dict[int, Fraction]) -> dict[int, Fraction]:
    out = dict(p)
    for d, c in q.items():
        out[d] = out.get(d, Fraction(0)) + c
        if out[d] == 0:
            del out[d]
    return out


def _poly_sub(p: dict[int, Fraction], q: dict[int, Fraction]) -> dict[int, Fraction]:
    return _poly_add(p, {d: -c for d, c in q.items()})


def _poly_eval(p: dict[int, Fraction], x: Fraction) -> Fraction:
    total = Fraction(0)
    for d, c in p.items():
        total += c * (x**d)
    return total


def _poly_divmod(
    num: dict[int, Fraction], den: dict[int, Fraction]
) -> tuple[dict[int, Fraction], dict[int, Fraction]]:
    """Polynomial division num = q·den + r with deg r < deg den."""
    num = {d: Fraction(c) for d, c in num.items() if c != 0}
    den = {d: Fraction(c) for d, c in den.items() if c != 0}
    if not den:
        raise ZeroDivisionError("zero denominator polynomial")
    deg_d = poly_degree(den)
    lead_d = den[deg_d]
    q: dict[int, Fraction] = {}
    r = dict(num)
    guard = 0
    while r and poly_degree(r) >= deg_d and guard < 32:
        guard += 1
        deg_r = poly_degree(r)
        coeff = r[deg_r] / lead_d
        shift = deg_r - deg_d
        q[shift] = q.get(shift, Fraction(0)) + coeff
        for d, c in den.items():
            rd = d + shift
            r[rd] = r.get(rd, Fraction(0)) - c * coeff
            if r[rd] == 0:
                del r[rd]
    return ({d: c for d, c in q.items() if c != 0}, {d: c for d, c in r.items() if c != 0})


# ---------------------------------------------------------------------------
# Kernel sampling
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ResidualKernel:
    """Multidimensional residual ``(a + b x) / D`` (b≡0 when deg D < 2)."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)  # coef of x

    @property
    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    @property
    def dim(self) -> int:
        if self.is_zero:
            return 0
        if self.b == 0:
            return 1  # constant-only
        if self.a == 0:
            return 1  # pure bx
        return 2

    def coeffs(self) -> dict[int, Fraction]:
        out: dict[int, Fraction] = {}
        if self.a != 0:
            out[0] = Fraction(self.a)
        if self.b != 0:
            out[1] = Fraction(self.b)
        return out

    def as_dict(self) -> dict[str, Any]:
        return {
            "a": str(Fraction(self.a)),
            "b": str(Fraction(self.b)),
            "dim": self.dim,
            "is_zero": self.is_zero,
            "latex": self.latex("x"),
        }

    def latex(self, var: str = "x") -> str:
        if self.is_zero:
            return "0"
        parts: list[tuple[Fraction, str]] = []
        if self.b != 0:
            parts.append((Fraction(self.b), var))
        if self.a != 0:
            parts.append((Fraction(self.a), ""))
        # join_signed_terms expects high-degree first-ish; order ok
        latex, _ = join_signed_terms(parts)
        return latex


def sample_residual_kernel(
    ctx: PrimitiveContext,
    *,
    d: float,
    den_degree: int,
    cancel_count: int,
    force_mode: str | None = None,
) -> ResidualKernel:
    """Sample 2D kernel with low-D simplicity bias.

    ``force_mode``: ``zero`` | ``constant`` | ``linear_pure`` | ``full`` | None.
    """
    den_degree = max(0, int(den_degree))
    settings = getattr(ctx, "settings", None) or {}
    explicit = force_mode or settings.get("kernel_mode")
    if explicit in {"zero", "0", "none"}:
        return ResidualKernel()
    if explicit in {"constant", "const", "b0"}:
        return ResidualKernel(a=_small_kernel_coef(ctx, d=d), b=Fraction(0))
    if explicit in {"linear_pure", "a0", "bx"}:
        if den_degree < 2:
            return ResidualKernel(a=_small_kernel_coef(ctx, d=d), b=Fraction(0))
        return ResidualKernel(a=Fraction(0), b=_small_kernel_coef(ctx, d=d))
    if explicit in {"full", "2d", "ab"}:
        if den_degree < 2:
            return ResidualKernel(a=_small_kernel_coef(ctx, d=d), b=Fraction(0))
        return ResidualKernel(
            a=_small_kernel_coef(ctx, d=d), b=_small_kernel_coef(ctx, d=d)
        )

    # --- Auto policy ---
    # P(nonzero kernel): low at easy D; higher later; boosted if cancels need visibility.
    if d < 4:
        p_nonzero = 0.12
    elif d < 8:
        p_nonzero = 0.28
    elif d < 14:
        p_nonzero = 0.45
    else:
        p_nonzero = 0.55
    # Cancel factors only appear as atomic dens when K(r_cancel) ≠ 0.
    if cancel_count >= 1:
        p_nonzero = max(p_nonzero, 0.85 if d < 6 else 0.95)

    if ctx.rng.random() >= p_nonzero:
        return ResidualKernel()

    # Nonzero: prefer simple shapes at low D.
    # Options: constant (b=0), pure bx (a=0), full (a≠0,b≠0).
    if den_degree < 2:
        return ResidualKernel(a=_small_kernel_coef(ctx, d=d), b=Fraction(0))

    if d < 6:
        weights = {"constant": 0.55, "a0": 0.30, "full": 0.15}
    elif d < 12:
        weights = {"constant": 0.40, "a0": 0.30, "full": 0.30}
    else:
        weights = {"constant": 0.25, "a0": 0.25, "full": 0.50}

    kind = ctx.rng.choices(
        list(weights.keys()), weights=list(weights.values()), k=1
    )[0]
    if kind == "constant":
        return ResidualKernel(a=_small_kernel_coef(ctx, d=d), b=Fraction(0))
    if kind == "a0":
        return ResidualKernel(a=Fraction(0), b=_small_kernel_coef(ctx, d=d))
    return ResidualKernel(
        a=_small_kernel_coef(ctx, d=d), b=_small_kernel_coef(ctx, d=d)
    )


def _small_kernel_coef(ctx: PrimitiveContext, *, d: float = 0.0) -> Fraction:
    """Small nonzero integer — widens slightly at high D."""
    if d >= 14:
        pool = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5]
    else:
        pool = [1, -1, 2, -2, 3, -3]
    return Fraction(int(ctx.rng.choice(pool)))


# ---------------------------------------------------------------------------
# PFD solve
# ---------------------------------------------------------------------------


def pfd_atomic_coeffs(
    num: dict[int, Fraction],
    factors: tuple[LinearFactor, ...],
) -> list[Fraction]:
    """Return constant atomic coeffs Aᵢ for num / Π fᵢ (proper part assumed).

    Solves Aᵢ = num(rᵢ) / Π_{j≠i} fⱼ(rᵢ).
    """
    if not factors:
        return []
    coeffs: list[Fraction] = []
    for i, fi in enumerate(factors):
        ri = fi.root()
        num_ri = _poly_eval(num, ri)
        den_ri = Fraction(1)
        for j, fj in enumerate(factors):
            if j == i:
                continue
            den_ri *= fj.eval_at(ri)
        if den_ri == 0:
            raise ValueError("repeated root in PFD factors")
        coeffs.append(num_ri / den_ri)
    return coeffs


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PackagedTerm:
    num: dict[int, Fraction]
    den_factors: tuple[LinearFactor, ...]
    kind: Literal["atomic", "kernel", "polynomial"]

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "num": {str(d): str(c) for d, c in sorted(self.num.items())},
            "n_den_factors": len(self.den_factors),
            "den_roots": [str(f.root()) for f in self.den_factors],
        }


@dataclass(frozen=True)
class AddSubCancelResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    goal_mode: GoalMode
    cancel_count: int
    package_mode: PackageMode
    dens_style: str
    factors: FactorDraw
    cancel_factors: tuple[LinearFactor, ...]
    remain_factors: tuple[LinearFactor, ...]
    goal_num: dict[int, Fraction]
    r_num: dict[int, Fraction]
    r_den: dict[int, Fraction]
    kernel: ResidualKernel
    poly_part: dict[int, Fraction]
    terms: tuple[PackagedTerm, ...]
    effective_d: float
    metadata: dict[str, Any]
    clear_factor: int = 1
    goal_num_unscaled: dict[int, Fraction] | None = None

    def debug_dict(self) -> dict[str, Any]:
        unscaled = self.goal_num_unscaled
        if unscaled is None:
            unscaled = self.goal_num
        return {
            "pattern": "AddSubCancel",
            "effective_d": self.effective_d,
            "goal_mode": self.goal_mode,
            "cancel_count": self.cancel_count,
            "package_mode": self.package_mode,
            "dens_style": self.dens_style,
            "clear_factor": self.clear_factor,
            "goal_latex": self.answer_latex.split(",")[0].strip(),
            "goal_num": {str(k): str(v) for k, v in sorted(self.goal_num.items())},
            "goal_num_unscaled": {
                str(k): str(v) for k, v in sorted(unscaled.items())
            },
            "scaling_convention": (
                "answer=M*G (packaged sum = M*R; integer PF numerators)"
                if self.clear_factor > 1
                else "answer=G (M=1, no clear needed)"
            ),
            "kernel": self.kernel.as_dict(),
            "factors": self.factors.as_dict(),
            "cancel_factors": [f.as_dict() for f in self.cancel_factors],
            "remain_factors": [f.as_dict() for f in self.remain_factors],
            "r_num": {str(k): str(v) for k, v in sorted(self.r_num.items())},
            "r_den": {str(k): str(v) for k, v in sorted(self.r_den.items())},
            "poly_part": {str(k): str(v) for k, v in sorted(self.poly_part.items())},
            "terms": [t.as_dict() for t in self.terms],
            "prompt_latex": self.prompt_latex,
            "answer_latex": self.answer_latex,
            **self.metadata,
        }


# ---------------------------------------------------------------------------
# Goal / cancel assignment
# ---------------------------------------------------------------------------


def resolve_cancel_count(
    settings: dict[str, Any] | None,
    *,
    d: float,
    n_factors: int,
    rng,
) -> int:
    """k capped by inventory and difficulty-scaled ``RationalSkeletonCaps``."""
    s = settings or {}
    caps = rational_skeleton_caps(d, s)
    raw = s.get("cancel_factor_count", s.get("cancel_count"))
    n_factors = max(1, min(int(n_factors), caps.max_inventory_factors))
    if raw is not None and str(raw).strip().lower() not in {"", "auto", "random"}:
        try:
            k = int(raw)
        except (TypeError, ValueError):
            k = 0
        return max(0, min(k, caps.max_cancel_k, n_factors))
    hi = min(caps.max_cancel_k, n_factors)
    pool = list(range(0, hi + 1))
    if d < 4:
        weights = [3.0 if c == 0 else (2.0 if c == 1 else 0.8) for c in pool]
    elif d < 10:
        weights = [1.5 if c == 0 else (2.5 if c == 1 else 1.5) for c in pool]
    elif caps.max_inventory_factors >= 3:
        weights = []
        for c in pool:
            if c == 0:
                weights.append(0.5)
            elif c == 1:
                weights.append(1.2)
            elif c == 2:
                weights.append(1.6)
            else:
                weights.append(1.8)
    else:
        weights = [1.0 for _ in pool]
    return int(rng.choices(pool, weights=weights, k=1)[0])


def _sample_goal_num(
    ctx: PrimitiveContext,
    *,
    remain_deg: int,
    prefer_linear_over_linear: bool,
) -> dict[int, Fraction]:
    """Sample goal numerator. Allows x/(linear) style when remain_deg==1."""
    if remain_deg <= 0:
        # Full cancel → constant goal
        v = int(ctx.rng.choice([1, -1, 2, -2, 3, 4, 5, -3]))
        return {0: Fraction(v)}
    if remain_deg == 1 and prefer_linear_over_linear:
        # e.g. x/(x+2) or (2x+1)/(3x-1)
        if ctx.rng.random() < 0.55:
            return {1: Fraction(1)}  # x
        a = Fraction(int(ctx.rng.choice([1, 1, 2, 3])))
        b = Fraction(int(ctx.rng.choice([-3, -2, -1, 1, 2, 3])))
        return {1: a, 0: b} if b != 0 else {1: a}
    # Proper: constant (or linear if remain_deg≥2)
    if remain_deg >= 2 and ctx.rng.random() < 0.45:
        a = Fraction(int(ctx.rng.choice([1, 1, 2])))
        b = Fraction(int(ctx.rng.choice([-3, -2, -1, 0, 1, 2, 3])))
        out = {1: a}
        if b != 0:
            out[0] = b
        return out
    v = int(ctx.rng.choice([1, -1, 2, -2, 3, 4, 5, -3, -4]))
    return {0: Fraction(v)}


# ---------------------------------------------------------------------------
# Package + verify
# ---------------------------------------------------------------------------


def _render_fraction(
    num: dict[int, Fraction],
    den_factors: tuple[LinearFactor, ...],
    var,
    *,
    dens_style: str,
    display_normalize: bool = True,
    display_intent: DisplayIntent | str | None = None,
    display_rules: list[str] | tuple[str, ...] | None = None,
    display_preset: str | None = None,
    settings: dict[str, Any] | None = None,
) -> tuple[str, str]:
    """Print one rational summand from structured ``(num, dens)``.

    Applies ``rational_display`` rules (default preset ``standard_rational``).
    Missing/None intent polishes; ``complex_fraction_skill`` / ``as_built``
    skip structure-changing rules. Never distributes ``q(ax+b)``.
    """
    plan = plan_fraction_display(
        num,
        den_factors,
        display_normalize=display_normalize,
        display_intent=display_intent,
        display_rules=display_rules,
        display_preset=display_preset,
        settings=settings,
    )
    render_num = plan.num
    leading_q = plan.leading_den_coef
    cfg = plan.config

    if not render_num:
        nl, nt = "0", "0"
    elif set(render_num.keys()) == {0}:
        nl = num_latex(render_num[0])
        nt = str(render_num[0])
    else:
        nl, nt = render_poly(render_num, var)
    if not den_factors:
        return nl, nt
    if dens_style == "expanded" and len(den_factors) >= 2:
        den_poly: dict[int, Fraction] = {0: Fraction(1)}
        for f in den_factors:
            den_poly = multiply_coeffs(den_poly, f.coeffs())
        dl, dt = render_poly(den_poly, var)
        if leading_q != 1:
            # Keep q factored out; do not distribute into the expanded poly.
            dl = apply_leading_den_coef(leading_q, dl, config=cfg)
            dt = f"{leading_q}*({dt})"
    else:
        if len(den_factors) == 1:
            dl, dt = render_poly(den_factors[0].coeffs(), var)
        else:
            parts_l = []
            parts_t = []
            for f in den_factors:
                fl, ft = render_poly(f.coeffs(), var)
                parts_l.append(f"\\left({fl}\\right)")
                parts_t.append(f"({ft})")
            dl, dt = "".join(parts_l), "".join(parts_t)
        if leading_q != 1:
            dl = apply_leading_den_coef(leading_q, dl, config=cfg)
            dt = f"{leading_q}*({dt})" if len(den_factors) == 1 else f"{leading_q}*{dt}"
    return rf"\frac{{{nl}}}{{{dl}}}", f"({nt})/({dt})"


def package_with_kernel(
    *,
    r_num: dict[int, Fraction],
    factors: tuple[LinearFactor, ...],
    kernel: ResidualKernel,
) -> tuple[dict[int, Fraction], list[PackagedTerm]]:
    """Divide R, apply kernel, rebalance atomic PFD. Returns (poly_part, terms)."""
    den: dict[int, Fraction] = {0: Fraction(1)}
    for f in factors:
        den = multiply_coeffs(den, f.coeffs())

    poly_part, proper = _poly_divmod(r_num, den)
    # Subtract kernel from proper numerator, then PFD.
    k_coeffs = kernel.coeffs()
    adj = _poly_sub(proper, k_coeffs) if k_coeffs else dict(proper)

    terms: list[PackagedTerm] = []
    if poly_part:
        terms.append(
            PackagedTerm(num=dict(poly_part), den_factors=(), kind="polynomial")
        )

    if factors:
        atomics = pfd_atomic_coeffs(adj, factors)
        for A, fac in zip(atomics, factors):
            if A == 0:
                continue
            terms.append(
                PackagedTerm(
                    num={0: Fraction(A)},
                    den_factors=(fac,),
                    kind="atomic",
                )
            )

    if not kernel.is_zero and factors:
        terms.append(
            PackagedTerm(
                num=dict(k_coeffs),
                den_factors=tuple(factors),
                kind="kernel",
            )
        )

    return poly_part, terms


def clear_factor_from_coeffs(*coeffs: Fraction) -> int:
    """Positive integer ``M`` = LCM of denominators of nonzero coeffs (or 1)."""
    dens = [abs(Fraction(c).denominator) for c in coeffs if Fraction(c) != 0]
    if not dens:
        return 1
    m = 1
    for d in dens:
        m = lcm(m, int(d))
    return max(1, int(m))


def _scale_poly(p: dict[int, Fraction], m: Fraction) -> dict[int, Fraction]:
    if m == 1:
        return {d: Fraction(c) for d, c in p.items() if c != 0}
    out: dict[int, Fraction] = {}
    for d, c in p.items():
        v = Fraction(c) * m
        if v != 0:
            out[d] = v
    return out


def clear_fractional_package(
    terms: list[PackagedTerm],
    *,
    r_num: dict[int, Fraction],
    goal_num: dict[int, Fraction],
    kernel: ResidualKernel,
    poly_part: dict[int, Fraction],
) -> tuple[
    list[PackagedTerm],
    dict[int, Fraction],
    dict[int, Fraction],
    ResidualKernel,
    dict[int, Fraction],
    int,
]:
    """Classroom clear-denominators move on packaged PF + kernel.

    If any atomic / kernel / poly numerator coeff is fractional, multiply every
    summand, ``r_num``, ``goal_num``, and ``kernel`` by
    ``M = lcm(denominators)`` so packaged numerators are integers.

    Scaling convention
    ------------------
    Packaged sum becomes ``M · R``; after combine+cancel the answer is
    ``M · G``. When ``M = 1``, values are unchanged (answer stays ``G``).
    """
    coeffs: list[Fraction] = []
    for t in terms:
        coeffs.extend(Fraction(c) for c in t.num.values())
    m = clear_factor_from_coeffs(*coeffs)
    if m == 1:
        return terms, r_num, goal_num, kernel, poly_part, 1

    mf = Fraction(m)
    scaled_terms = [
        PackagedTerm(
            num=_scale_poly(t.num, mf),
            den_factors=t.den_factors,
            kind=t.kind,
        )
        for t in terms
    ]
    scaled_r = _scale_poly(r_num, mf)
    scaled_goal = _scale_poly(goal_num, mf)
    scaled_poly = _scale_poly(poly_part, mf)
    scaled_kernel = ResidualKernel(a=Fraction(kernel.a) * mf, b=Fraction(kernel.b) * mf)
    return scaled_terms, scaled_r, scaled_goal, scaled_kernel, scaled_poly, m


def verify_packaged_equals_r(
    terms: list[PackagedTerm],
    r_num: dict[int, Fraction],
    factors: tuple[LinearFactor, ...],
) -> bool:
    """Recombine packaged terms over D and compare to r_num."""
    den: dict[int, Fraction] = {0: Fraction(1)}
    for f in factors:
        den = multiply_coeffs(den, f.coeffs())
    combined = {}
    for t in terms:
        if t.kind == "polynomial":
            # P * D
            combined = _poly_add(combined, multiply_coeffs(t.num, den))
            continue
        # t.num / Π(t.den)  →  t.num * (D / Π t.den)
        cofactor = dict(den)
        for f in t.den_factors:
            # divide cofactor by f via exact division
            q, rem = _poly_divmod(cofactor, f.coeffs())
            if rem:
                return False
            cofactor = q
        combined = _poly_add(combined, multiply_coeffs(t.num, cofactor))
    return combined == {d: Fraction(c) for d, c in r_num.items() if c != 0} or (
        not combined and not r_num
    )


def _join_term_latex(parts: list[str]) -> str:
    if not parts:
        return "0"
    out = parts[0]
    for p in parts[1:]:
        if p.startswith("-"):
            out = f"{out} - {p[1:]}"
        else:
            out = f"{out} + {p}"
    return out


def _excluded_root_values(factors: tuple[LinearFactor, ...]) -> list[Fraction]:
    """Unique roots of *factors* (order-preserving). Used for cancel-only exclusions."""
    seen: set[Fraction] = set()
    out: list[Fraction] = []
    for f in factors:
        r = f.root()
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def _excluded_values_meta(roots: list[Fraction]) -> list:
    """JSON-friendly excluded roots (int or ``\"p/q\"`` string)."""
    out: list = []
    for r in roots:
        if r.denominator == 1:
            out.append(int(r.numerator))
        else:
            out.append(f"{r.numerator}/{r.denominator}")
    return out


def _excluded_note(factors: tuple[LinearFactor, ...], var_latex: str) -> str:
    """LaTeX ``x \\neq …`` for cancelled-factor roots only (see module docstring)."""
    roots = _excluded_root_values(factors)
    if not roots:
        return ""
    joined = ", ".join(num_latex(r) for r in roots)
    return rf"{var_latex} \neq {joined}"


# ---------------------------------------------------------------------------
# Main sampler
# ---------------------------------------------------------------------------


def sample_add_sub_cancel(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    cancel_count: int | None = None,
    n_factors: int | None = None,
    kernel_mode: str | None = None,
    constraints: FactorConstraints | None = None,
) -> AddSubCancelResult:
    """Generate one AddSubCancel item (goal → inflate → PFD + 2D kernel)."""
    settings = dict(getattr(ctx, "settings", None) or {})
    eff = float(d if d is not None else getattr(ctx, "topic_d", 0.0) or 0.0)
    cons = constraints or constraints_from_settings(settings, d=eff)
    caps = rational_skeleton_caps(eff, settings)
    cons = _widen_cons_for_caps(cons, caps)
    inv_cap = caps.max_inventory_factors

    # Inventory widens with D; answer den stays ≤ max_answer_den_degree via k/remain split.
    requested_k = cancel_count
    if requested_k is None:
        raw = settings.get("cancel_factor_count", settings.get("cancel_count"))
        if raw is not None and str(raw).strip().lower() not in {"", "auto", "random"}:
            try:
                requested_k = int(raw)
            except (TypeError, ValueError):
                requested_k = None

    if n_factors is None:
        from question_engine.frameworks.primitives.skeleton_difficulty import (
            skeleton_format_tier,
        )

        ft = skeleton_format_tier(eff)
        choices = [2, 2, 2, 1]
        if inv_cap >= 3 and ft >= 2:
            choices = [2, 2, 3, 3, 1]
        if inv_cap >= 4 and ft >= 3:
            choices = [2, 3, 3, 4, 4]
        n_fac = int(ctx.rng.choice(choices)) if cons.max_factors >= 2 else 1
        n_fac = max(cons.min_factors, min(n_fac, cons.max_factors, inv_cap))
        if requested_k is not None:
            n_fac = max(n_fac, min(int(requested_k), inv_cap, cons.max_factors))
    else:
        n_fac = max(1, min(int(n_factors), inv_cap))
        if requested_k is not None:
            n_fac = max(n_fac, min(int(requested_k), inv_cap))

    if requested_k is not None:
        n_fac = min(n_fac, int(requested_k) + caps.max_answer_den_degree)

    last_err: Exception | None = None
    for _attempt in range(40):
        try:
            return _sample_once(
                ctx,
                eff=eff,
                n_fac=n_fac,
                cancel_count=cancel_count,
                kernel_mode=kernel_mode,
                cons=cons,
                settings=settings,
            )
        except (ValueError, ZeroDivisionError) as exc:
            last_err = exc
            continue
    raise RuntimeError(f"sample_add_sub_cancel failed: {last_err}")


def _sample_once(
    ctx: PrimitiveContext,
    *,
    eff: float,
    n_fac: int,
    cancel_count: int | None,
    kernel_mode: str | None,
    cons: FactorConstraints,
    settings: dict[str, Any],
) -> AddSubCancelResult:
    caps = rational_skeleton_caps(eff, settings)
    draw = sample_factor_product(
        ctx, n_factors=n_fac, d=eff, constraints=cons
    )
    factors = draw.factors
    k = (
        max(0, min(int(cancel_count), caps.max_cancel_k, len(factors)))
        if cancel_count is not None
        else resolve_cancel_count(
            settings, d=eff, n_factors=len(factors), rng=ctx.rng
        )
    )
    # Keep simplified answer denominator degree honest (auto k only).
    if cancel_count is None and len(factors) - k > caps.max_answer_den_degree:
        k = max(k, len(factors) - caps.max_answer_den_degree)
        k = min(k, caps.max_cancel_k, len(factors))

    # Assign: first k → cancel, rest → remain (shuffle for variety).
    order = list(factors)
    ctx.rng.shuffle(order)
    cancel_facs = tuple(order[:k])
    remain_facs = tuple(order[k:])

    prefer_x_over_linear = bool(settings.get("prefer_linear_goal", True))
    goal_num = _sample_goal_num(
        ctx,
        remain_deg=len(remain_facs),
        prefer_linear_over_linear=prefer_x_over_linear and len(remain_facs) == 1,
    )
    goal_mode: GoalMode = "constant" if not remain_facs else "fraction"

    # Inflate: R_num = goal_num * Π cancel; R_den = Π all factors
    r_num = dict(goal_num)
    for f in cancel_facs:
        r_num = multiply_coeffs(r_num, f.coeffs())
    r_den: dict[int, Fraction] = {0: Fraction(1)}
    for f in factors:
        r_den = multiply_coeffs(r_den, f.coeffs())

    if poly_degree(r_den) > caps.max_inventory_factors:
        raise ValueError("den degree exceeds cap")
    if len(remain_facs) > caps.max_answer_den_degree:
        raise ValueError("answer den degree exceeds cap")

    kernel = sample_residual_kernel(
        ctx,
        d=eff,
        den_degree=poly_degree(r_den),
        cancel_count=k,
        force_mode=kernel_mode or settings.get("kernel_mode"),
    )
    # If cancels present and kernel still zero, force a simple nonzero
    # (constant) so cancel dens can appear atomically — unless caller forced zero.
    forced = kernel_mode or settings.get("kernel_mode")
    if k >= 1 and kernel.is_zero and forced not in {"zero", "0", "none"}:
        kernel = ResidualKernel(a=_small_kernel_coef(ctx, d=eff), b=Fraction(0))

    poly_part, terms = package_with_kernel(
        r_num=r_num, factors=factors, kernel=kernel
    )
    if not verify_packaged_equals_r(terms, r_num, factors):
        raise ValueError("package recombine mismatch")

    package_mode: PackageMode = "pure_pfd" if kernel.is_zero else "residual"

    # Same-den fallback: single factor, need ± → split constant num into two.
    if len(factors) == 1 and sum(1 for t in terms if t.kind != "polynomial") < 2:
        terms = _split_same_den(ctx, r_num=r_num, fac=factors[0], poly_part=poly_part)
        if not verify_packaged_equals_r(terms, r_num, factors):
            raise ValueError("same-den split mismatch")

    # Classroom clear-denominators: integer PF numerators; answer = M·G.
    goal_num_unscaled = dict(goal_num)
    terms, r_num, goal_num, kernel, poly_part, clear_m = clear_fractional_package(
        terms,
        r_num=r_num,
        goal_num=goal_num,
        kernel=kernel,
        poly_part=poly_part,
    )
    if clear_m > 1 and not verify_packaged_equals_r(terms, r_num, factors):
        raise ValueError("clear-factor package recombine mismatch")

    var = ctx.sample_variable()
    dens_style = draw.dens_style
    display_cfg = resolve_display_config(settings=settings)
    display_normalize = display_cfg.display_normalize
    display_intent = display_cfg.display_intent

    prompt_parts_l: list[str] = []
    prompt_parts_t: list[str] = []
    for t in terms:
        if t.kind == "polynomial":
            pl, pt = render_poly(t.num, var)
            prompt_parts_l.append(pl)
            prompt_parts_t.append(pt)
            continue
        # Packaged PF/kernel atoms: default polish unless tagged CF / as_built.
        pl, pt = _render_fraction(
            t.num,
            t.den_factors,
            var,
            dens_style=dens_style,
            settings=settings,
            display_intent=display_intent,
            display_normalize=display_normalize,
        )
        prompt_parts_l.append(pl)
        prompt_parts_t.append(pt)

    prompt_l = _join_term_latex(prompt_parts_l)
    prompt_t = " + ".join(prompt_parts_t)

    # Answer = M·G (M=1 ⇒ G). Goal uses same normalize gate (not a CF skill).
    if goal_mode == "constant":
        ans_l, ans_t = render_poly(goal_num, var)
    else:
        ans_l, ans_t = _render_fraction(
            goal_num,
            remain_facs,
            var,
            dens_style="factored",
            settings=settings,
            display_intent=display_intent,
            display_normalize=display_normalize,
        )
    # Exclusions = cancelled roots only (not remain / final-den poles).
    excl_roots = _excluded_root_values(cancel_facs)
    excl = _excluded_note(cancel_facs, var.latex)
    if excl:
        ans_l = rf"{ans_l},\; {excl}"
        roots_txt = ", ".join(str(r) for r in excl_roots)
        ans_t = f"{ans_t}, {var.name} ≠ {roots_txt}"

    meta = {
        "skeleton_pattern": "AddSubCancel",
        "skeleton_source": "rational_skeleton",
        "cancel_factor_count": k,
        "kernel_dim": kernel.dim,
        "kernel_a": str(kernel.a),
        "kernel_b": str(kernel.b),
        "goal_mode": goal_mode,
        "package_mode": package_mode,
        "dens_style": dens_style,
        "display_normalize": display_normalize,
        "display_intent": display_intent,
        "display_preset": display_cfg.preset,
        "display_rules": list(display_cfg.active_rules),
        "factor_bias": draw.as_dict().get("bias_label"),
        "n_factors": len(factors),
        "den_degree": poly_degree(r_den),
        "clear_factor": clear_m,
        "scaling_convention": (
            "answer=M*G"
            if clear_m > 1
            else "answer=G"
        ),
        "excluded_values": _excluded_values_meta(excl_roots),
    }

    return AddSubCancelResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        goal_mode=goal_mode,
        cancel_count=k,
        package_mode=package_mode,
        dens_style=dens_style,
        factors=draw,
        cancel_factors=cancel_facs,
        remain_factors=remain_facs,
        goal_num=goal_num,
        r_num=r_num,
        r_den=r_den,
        kernel=kernel,
        poly_part=poly_part,
        terms=tuple(terms),
        effective_d=eff,
        metadata=meta,
        clear_factor=clear_m,
        goal_num_unscaled=goal_num_unscaled,
    )


def _split_same_den(
    ctx: PrimitiveContext,
    *,
    r_num: dict[int, Fraction],
    fac: LinearFactor,
    poly_part: dict[int, Fraction],
) -> list[PackagedTerm]:
    """Split a single-den rational into two same-den summands."""
    # After removing poly_part contribution: proper num over fac.
    den = fac.coeffs()
    _, proper = _poly_divmod(r_num, den)
    # proper should be constant for deg1 den
    total = proper.get(0, Fraction(0))
    if poly_degree(proper) > 0:
        # rare: treat whole as two pieces via kernel-style not needed
        total = _poly_eval(proper, Fraction(0))  # fallback — shouldn't happen
    a1 = Fraction(int(ctx.rng.choice([1, 2, 3, -1, -2])))
    a2 = total - a1
    terms: list[PackagedTerm] = []
    if poly_part:
        terms.append(PackagedTerm(num=dict(poly_part), den_factors=(), kind="polynomial"))
    terms.append(
        PackagedTerm(num={0: a1}, den_factors=(fac,), kind="atomic")
    )
    terms.append(
        PackagedTerm(num={0: a2}, den_factors=(fac,), kind="atomic")
    )
    return terms


def generate_add_sub_cancel_question(
    settings: dict[str, Any] | None = None,
) -> AddSubCancelResult:
    """Demo / gallery API: build context and sample one AddSubCancel item."""
    from question_engine.frameworks.primitives import (
        PRIM_NUMBERS,
        PRIM_VARIABLE,
        build_context,
    )
    from question_engine.frameworks.primitives.expression_policy import (
        POLYNOMIAL_POLICY_DEFAULT,
    )

    settings = dict(settings or {})
    settings.setdefault("count", 1)
    ctx = build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
        leaf_id=str(settings.get("_leaf_id") or "rational_expression_simplification"),
    )
    return sample_add_sub_cancel(ctx)


# ---------------------------------------------------------------------------
# Shared goal → inflate core (SimplifyCancel / helpers)
# ---------------------------------------------------------------------------


def _assign_cancel_remain(
    ctx: PrimitiveContext,
    factors: tuple[LinearFactor, ...],
    k: int,
) -> tuple[tuple[LinearFactor, ...], tuple[LinearFactor, ...]]:
    order = list(factors)
    ctx.rng.shuffle(order)
    return tuple(order[:k]), tuple(order[k:])


def _inflate_from_goal(
    goal_num: dict[int, Fraction],
    cancel_facs: tuple[LinearFactor, ...],
    all_factors: tuple[LinearFactor, ...],
) -> tuple[dict[int, Fraction], dict[int, Fraction]]:
    r_num = dict(goal_num)
    for f in cancel_facs:
        r_num = multiply_coeffs(r_num, f.coeffs())
    r_den: dict[int, Fraction] = {0: Fraction(1)}
    for f in all_factors:
        r_den = multiply_coeffs(r_den, f.coeffs())
    return r_num, r_den


def _sample_simplify_insert_cancel(
    ctx: PrimitiveContext,
    *,
    eff: float,
    cancel_count: int | None,
    cons: FactorConstraints,
    settings: dict[str, Any],
    caps: RationalSkeletonCaps,
) -> SimplifyCancelResult:
    """Constructive-style simplify: cancel pairs visible in both num and den (high D)."""
    from question_engine.frameworks.primitives.factor_sampler import sample_linear_factor

    k_hi = caps.max_cancel_k
    if cancel_count is not None:
        k = max(0, min(int(cancel_count), k_hi))
    else:
        k = resolve_cancel_count(
            settings, d=eff, n_factors=max(1, k_hi), rng=ctx.rng
        )

    n_remain_num = (
        int(ctx.rng.choice([0, 1, 1, 2])) if eff >= 8 else int(ctx.rng.choice([0, 1]))
    )
    n_remain_num = max(0, min(n_remain_num, caps.max_answer_den_degree))
    n_remain_den = int(ctx.rng.choice([1, 1, 2]))
    n_remain_den = max(1, min(n_remain_den, caps.max_answer_den_degree))

    roots: set[Fraction] = set()
    remain_num: list[LinearFactor] = []
    for _ in range(n_remain_num):
        fac = sample_linear_factor(ctx, constraints=cons, d=eff, used_roots=roots)
        remain_num.append(fac)
        roots.add(fac.root())
    remain_den: list[LinearFactor] = []
    for _ in range(n_remain_den):
        fac = sample_linear_factor(ctx, constraints=cons, d=eff, used_roots=roots)
        remain_den.append(fac)
        roots.add(fac.root())
    cancel_facs: list[LinearFactor] = []
    for _ in range(k):
        fac = sample_linear_factor(ctx, constraints=cons, d=eff, used_roots=roots)
        cancel_facs.append(fac)
        roots.add(fac.root())

    lead = Fraction(int(ctx.rng.choice([1, 2, 3, 4, 5, 6, 7, -1, -2, -3])))
    goal_num = {0: lead}
    for f in remain_num:
        goal_num = multiply_coeffs(goal_num, f.coeffs())
    goal_mode: GoalMode = "constant" if not remain_den else "fraction"
    remain_facs = tuple(remain_den)

    prompt_num_facs = tuple(remain_num + cancel_facs)
    prompt_den_facs = tuple(remain_den + cancel_facs)

    r_num = dict(goal_num)
    for f in cancel_facs:
        r_num = multiply_coeffs(r_num, f.coeffs())
    r_den: dict[int, Fraction] = {0: Fraction(1)}
    for f in prompt_den_facs:
        r_den = multiply_coeffs(r_den, f.coeffs())

    var = ctx.sample_variable()
    dens_style = "factored"
    if bool(settings.get("expand_polynomials")):
        dens_style = "expanded"
    display_cfg = resolve_display_config(settings=settings)
    display_normalize = display_cfg.display_normalize
    display_intent = display_cfg.display_intent

    num_l, num_t = _render_scaled_factor_product(
        prompt_num_facs, var, const=lead, dens_style=dens_style
    )
    den_l, den_t = _render_factor_list(prompt_den_facs, var, dens_style=dens_style)
    prompt_l = rf"\frac{{{num_l}}}{{{den_l}}}"
    prompt_t = f"({num_t})/({den_t})"

    ans_l, ans_t, excl_meta = _answer_from_goal(
        goal_num=goal_num,
        remain_facs=remain_facs,
        cancel_facs=tuple(cancel_facs),
        var=var,
        settings=settings,
        display_normalize=display_normalize,
        display_intent=display_intent,
    )

    meta = {
        "skeleton_pattern": "SimplifyCancel",
        "skeleton_source": "rational_skeleton",
        "cancel_factor_count": k,
        "goal_mode": goal_mode,
        "dens_style": dens_style,
        "display_normalize": display_normalize,
        "display_intent": display_intent,
        "display_preset": display_cfg.preset,
        "display_rules": list(display_cfg.active_rules),
        "factor_bias": "insert_cancel_pairs",
        "n_factors": len(prompt_den_facs),
        "insert_cancel_pairs": True,
        "excluded_values": excl_meta,
    }

    empty_draw = sample_factor_product(ctx, n_factors=1, d=eff, constraints=cons)
    return SimplifyCancelResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        goal_mode=goal_mode,
        cancel_count=k,
        dens_style=dens_style,
        factors=empty_draw,
        cancel_factors=tuple(cancel_facs),
        remain_factors=remain_facs,
        goal_num=goal_num,
        r_num=r_num,
        r_den=r_den,
        effective_d=eff,
        metadata=meta,
    )


def _answer_from_goal(
    *,
    goal_num: dict[int, Fraction],
    remain_facs: tuple[LinearFactor, ...],
    cancel_facs: tuple[LinearFactor, ...],
    var,
    settings: dict[str, Any],
    display_normalize: bool,
    display_intent: DisplayIntent | str | None,
) -> tuple[str, str, list]:
    """Render M·G-style answer (here M=1) with cancel-only exclusions."""
    goal_mode: GoalMode = "constant" if not remain_facs else "fraction"
    if goal_mode == "constant":
        ans_l, ans_t = render_poly(goal_num, var)
    else:
        ans_l, ans_t = _render_fraction(
            goal_num,
            remain_facs,
            var,
            dens_style="factored",
            settings=settings,
            display_intent=display_intent,
            display_normalize=display_normalize,
        )
    excl_roots = _excluded_root_values(cancel_facs)
    excl = _excluded_note(cancel_facs, var.latex)
    if excl:
        ans_l = rf"{ans_l},\; {excl}"
        roots_txt = ", ".join(str(r) for r in excl_roots)
        ans_t = f"{ans_t}, {var.name} ≠ {roots_txt}"
    return ans_l, ans_t, _excluded_values_meta(excl_roots)


def _build_rational_ctx(settings: dict[str, Any], *, leaf_id: str):
    from question_engine.frameworks.primitives import (
        PRIM_NUMBERS,
        PRIM_VARIABLE,
        build_context,
    )
    from question_engine.frameworks.primitives.expression_policy import (
        POLYNOMIAL_POLICY_DEFAULT,
    )

    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
        leaf_id=leaf_id,
    )


# ---------------------------------------------------------------------------
# SimplifyCancel — single-fraction surface
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SimplifyCancelResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    goal_mode: GoalMode
    cancel_count: int
    dens_style: str
    factors: FactorDraw
    cancel_factors: tuple[LinearFactor, ...]
    remain_factors: tuple[LinearFactor, ...]
    goal_num: dict[int, Fraction]
    r_num: dict[int, Fraction]
    r_den: dict[int, Fraction]
    effective_d: float
    metadata: dict[str, Any]

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "SimplifyCancel",
            "effective_d": self.effective_d,
            "goal_mode": self.goal_mode,
            "cancel_count": self.cancel_count,
            "dens_style": self.dens_style,
            "goal_num": {str(k): str(v) for k, v in sorted(self.goal_num.items())},
            "factors": self.factors.as_dict(),
            "cancel_factors": [f.as_dict() for f in self.cancel_factors],
            "remain_factors": [f.as_dict() for f in self.remain_factors],
            "r_num": {str(k): str(v) for k, v in sorted(self.r_num.items())},
            "r_den": {str(k): str(v) for k, v in sorted(self.r_den.items())},
            "prompt_latex": self.prompt_latex,
            "answer_latex": self.answer_latex,
            **self.metadata,
        }


def sample_simplify_cancel(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    cancel_count: int | None = None,
    n_factors: int | None = None,
    constraints: FactorConstraints | None = None,
) -> SimplifyCancelResult:
    """Generate one SimplifyCancel item (goal → inflate → single fraction)."""
    settings = dict(getattr(ctx, "settings", None) or {})
    eff = float(d if d is not None else getattr(ctx, "topic_d", 0.0) or 0.0)
    cons = constraints or constraints_from_settings(settings, d=eff)
    caps = rational_skeleton_caps(eff, settings)
    cons = _widen_cons_for_caps(cons, caps)
    inv_cap = caps.max_inventory_factors

    if n_factors is None:
        from question_engine.frameworks.primitives.skeleton_difficulty import (
            skeleton_format_tier,
        )

        ft = skeleton_format_tier(eff)
        choices = [2, 2, 2, 1]
        if inv_cap >= 3 and ft >= 2:
            choices = [2, 3, 3, 4]
        if inv_cap >= 4 and ft >= 3:
            choices = [3, 3, 4, 4]
        n_fac = int(ctx.rng.choice(choices)) if cons.max_factors >= 2 else 1
        n_fac = max(cons.min_factors, min(n_fac, cons.max_factors, inv_cap))
        raw = settings.get("cancel_factor_count", settings.get("cancel_count"))
        if cancel_count is not None:
            n_fac = max(n_fac, min(int(cancel_count), inv_cap, cons.max_factors))
        elif raw is not None and str(raw).strip().lower() not in {"", "auto", "random"}:
            try:
                n_fac = max(n_fac, min(int(raw), inv_cap, cons.max_factors))
            except (TypeError, ValueError):
                pass
    else:
        n_fac = max(1, min(int(n_factors), inv_cap))

    last_err: Exception | None = None
    for _attempt in range(40):
        try:
            return _sample_simplify_once(
                ctx,
                eff=eff,
                n_fac=n_fac,
                cancel_count=cancel_count,
                cons=cons,
                settings=settings,
            )
        except (ValueError, ZeroDivisionError) as exc:
            last_err = exc
            continue
    raise RuntimeError(f"sample_simplify_cancel failed: {last_err}")


def _sample_simplify_once(
    ctx: PrimitiveContext,
    *,
    eff: float,
    n_fac: int,
    cancel_count: int | None,
    cons: FactorConstraints,
    settings: dict[str, Any],
) -> SimplifyCancelResult:
    caps = rational_skeleton_caps(eff, settings)
    if caps.insert_cancel_pairs:
        return _sample_simplify_insert_cancel(
            ctx,
            eff=eff,
            cancel_count=cancel_count,
            cons=cons,
            settings=settings,
            caps=caps,
        )

    draw = sample_factor_product(ctx, n_factors=n_fac, d=eff, constraints=cons)
    factors = draw.factors
    k = (
        max(0, min(int(cancel_count), caps.max_cancel_k, len(factors)))
        if cancel_count is not None
        else resolve_cancel_count(
            settings, d=eff, n_factors=len(factors), rng=ctx.rng
        )
    )
    if cancel_count is None and len(factors) - k > caps.max_answer_den_degree:
        k = max(k, len(factors) - caps.max_answer_den_degree)
        k = min(k, caps.max_cancel_k, len(factors))
    cancel_facs, remain_facs = _assign_cancel_remain(ctx, factors, k)

    prefer_x_over_linear = bool(settings.get("prefer_linear_goal", True))
    goal_num = _sample_goal_num(
        ctx,
        remain_deg=len(remain_facs),
        prefer_linear_over_linear=prefer_x_over_linear and len(remain_facs) == 1,
    )
    goal_mode: GoalMode = "constant" if not remain_facs else "fraction"

    r_num, r_den = _inflate_from_goal(goal_num, cancel_facs, factors)
    if poly_degree(r_den) > caps.max_inventory_factors:
        raise ValueError("den degree exceeds cap")
    if len(remain_facs) > caps.max_answer_den_degree:
        raise ValueError("answer den degree exceeds cap")

    var = ctx.sample_variable()
    dens_style = draw.dens_style
    if caps.prefer_factored_prompt and dens_style == "auto":
        dens_style = "factored"
    display_cfg = resolve_display_config(settings=settings)
    display_normalize = display_cfg.display_normalize
    display_intent = display_cfg.display_intent

    # Prompt = inflated single fraction (factored or expanded dens).
    prompt_l, prompt_t = _render_fraction(
        r_num,
        factors,
        var,
        dens_style=dens_style,
        settings=settings,
        display_intent=display_intent,
        display_normalize=display_normalize,
    )

    ans_l, ans_t, excl_meta = _answer_from_goal(
        goal_num=goal_num,
        remain_facs=remain_facs,
        cancel_facs=cancel_facs,
        var=var,
        settings=settings,
        display_normalize=display_normalize,
        display_intent=display_intent,
    )

    meta = {
        "skeleton_pattern": "SimplifyCancel",
        "skeleton_source": "rational_skeleton",
        "cancel_factor_count": k,
        "goal_mode": goal_mode,
        "dens_style": dens_style,
        "display_normalize": display_normalize,
        "display_intent": display_intent,
        "display_preset": display_cfg.preset,
        "display_rules": list(display_cfg.active_rules),
        "factor_bias": draw.as_dict().get("bias_label"),
        "n_factors": len(factors),
        "den_degree": poly_degree(r_den),
        "excluded_values": excl_meta,
        "form_id": "simplify_cancel",
        "openstax_form": "simplify_cancel",
        "shape_id": "simplify_cancel",
    }

    return SimplifyCancelResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        goal_mode=goal_mode,
        cancel_count=k,
        dens_style=dens_style,
        factors=draw,
        cancel_factors=cancel_facs,
        remain_factors=remain_facs,
        goal_num=goal_num,
        r_num=r_num,
        r_den=r_den,
        effective_d=eff,
        metadata=meta,
    )


def generate_simplify_cancel_question(
    settings: dict[str, Any] | None = None,
) -> SimplifyCancelResult:
    """Demo / gallery API: build context and sample one SimplifyCancel item."""
    settings = dict(settings or {})
    settings.setdefault("count", 1)
    ctx = _build_rational_ctx(
        settings,
        leaf_id=str(settings.get("_leaf_id") or "rational_simplification"),
    )
    return sample_simplify_cancel(ctx)


# ---------------------------------------------------------------------------
# MulDivCancel — product / quotient surface
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MulDivCancelResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    operation: Literal["multiply", "divide"]
    cancel_count: int
    dens_style: str
    cancel_factors: tuple[LinearFactor, ...]
    remain_num_factors: tuple[LinearFactor, ...]
    remain_den_factors: tuple[LinearFactor, ...]
    effective_d: float
    metadata: dict[str, Any]

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "MulDivCancel",
            "effective_d": self.effective_d,
            "operation": self.operation,
            "cancel_count": self.cancel_count,
            "dens_style": self.dens_style,
            "cancel_factors": [f.as_dict() for f in self.cancel_factors],
            "remain_num_factors": [f.as_dict() for f in self.remain_num_factors],
            "remain_den_factors": [f.as_dict() for f in self.remain_den_factors],
            "prompt_latex": self.prompt_latex,
            "answer_latex": self.answer_latex,
            **self.metadata,
        }


def _render_factor_list(
    factors: tuple[LinearFactor, ...] | list[LinearFactor],
    var,
    *,
    dens_style: str,
    empty: str = "1",
) -> tuple[str, str]:
    facs = tuple(factors)
    if not facs:
        return empty, empty
    if dens_style == "expanded" and len(facs) >= 2:
        poly: dict[int, Fraction] = {0: Fraction(1)}
        for f in facs:
            poly = multiply_coeffs(poly, f.coeffs())
        return render_poly(poly, var)
    if len(facs) == 1:
        return render_poly(facs[0].coeffs(), var)
    parts_l: list[str] = []
    parts_t: list[str] = []
    for f in facs:
        fl, ft = render_poly(f.coeffs(), var)
        parts_l.append(f"\\left({fl}\\right)")
        parts_t.append(f"({ft})")
    return "".join(parts_l), "".join(parts_t)


def _render_scaled_factor_product(
    factors: tuple[LinearFactor, ...] | list[LinearFactor],
    var,
    *,
    const: Fraction = Fraction(1),
    dens_style: str = "factored",
) -> tuple[str, str]:
    """Render ``const · Π factors`` without gluing ``2`` onto ``y-4`` as ``2y-4``."""
    facs = tuple(factors)
    c = Fraction(const)
    if dens_style == "expanded":
        poly: dict[int, Fraction] = {0: c}
        for f in facs:
            poly = multiply_coeffs(poly, f.coeffs())
        return render_poly(poly, var)
    if not facs:
        return num_latex(c), str(c)
    body_l, body_t = _render_factor_list(facs, var, dens_style=dens_style)
    if c == 1:
        return body_l, body_t
    if len(facs) == 1:
        fl, ft = render_poly(facs[0].coeffs(), var)
        coeffs = facs[0].coeffs()
        # Monomial a·x (no constant term): fold coef; else wrap.
        if set(coeffs.keys()) == {1}:
            return render_poly(scale_coeffs(coeffs, c), var)
        return f"{num_latex(c)}\\left({fl}\\right)", f"({c})*({ft})"
    return f"{num_latex(c)}{body_l}", f"({c})*{body_t}"


def _render_operand_rational(
    num_facs: list[LinearFactor],
    den_facs: list[LinearFactor],
    var,
    *,
    dens_style: str,
    num_const: Fraction | None = None,
) -> tuple[str, str]:
    """Render one A/B operand; optional constant multiplier on the numerator."""
    c = Fraction(num_const) if num_const is not None else Fraction(1)
    nl, nt = _render_scaled_factor_product(
        num_facs, var, const=c, dens_style=dens_style
    )
    dl, dt = _render_factor_list(tuple(den_facs), var, dens_style=dens_style)
    return rf"\frac{{{nl}}}{{{dl}}}", f"({nt})/({dt})"


def sample_mul_div_cancel(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    cancel_count: int | None = None,
    operation: Literal["multiply", "divide"] | None = None,
    constraints: FactorConstraints | None = None,
) -> MulDivCancelResult:
    """Generate one MulDivCancel item (cross-operand cancels; deg remain ≤ 2)."""
    settings = dict(getattr(ctx, "settings", None) or {})
    eff = float(d if d is not None else getattr(ctx, "topic_d", 0.0) or 0.0)
    cons = constraints or constraints_from_settings(settings, d=eff)
    caps = rational_skeleton_caps(eff, settings)
    cons = _widen_cons_for_caps(cons, caps)
    operand_count = max(2, int(settings.get("operand_count", 2)))
    ops_ok = bool(settings.get("allow_multiply", True))
    if (
        operand_count >= 3
        and ops_ok
        and operation != "divide"
        and (operation is None or operation == "multiply")
    ):
        last_err: Exception | None = None
        for _attempt in range(48):
            try:
                return _sample_mul_div_three_operand(
                    ctx,
                    eff=eff,
                    cancel_count=cancel_count,
                    cons=cons,
                    settings=settings,
                    operand_count=operand_count,
                )
            except (ValueError, ZeroDivisionError) as exc:
                last_err = exc
                continue
        raise RuntimeError(f"sample_mul_div_three_operand failed: {last_err}")

    last_err: Exception | None = None
    for _attempt in range(48):
        try:
            return _sample_mul_div_once(
                ctx,
                eff=eff,
                cancel_count=cancel_count,
                operation=operation,
                cons=cons,
                settings=settings,
            )
        except (ValueError, ZeroDivisionError) as exc:
            last_err = exc
            continue
    raise RuntimeError(f"sample_mul_div_cancel failed: {last_err}")


def _sample_mul_div_once(
    ctx: PrimitiveContext,
    *,
    eff: float,
    cancel_count: int | None,
    operation: Literal["multiply", "divide"] | None,
    cons: FactorConstraints,
    settings: dict[str, Any],
) -> MulDivCancelResult:
    ops: list[str] = []
    if bool(settings.get("allow_multiply", True)):
        ops.append("multiply")
    if bool(settings.get("allow_divide", True)):
        ops.append("divide")
    if not ops:
        ops = ["multiply", "divide"]
    op: Literal["multiply", "divide"]
    if operation in {"multiply", "divide"}:
        op = operation  # type: ignore[assignment]
    else:
        op = ctx.rng.choice(ops)  # type: ignore[assignment]

    # Final remain dens deg ≤ 2; remain nums also ≤ 2 linears.
    # No leftover fillers — remain pieces ARE the operand content.
    n_remain_den = int(ctx.rng.choice([1, 1, 2]) if cons.max_factors >= 2 else 1)
    n_remain_den = max(1, min(n_remain_den, MAX_DEN_DEGREE))
    n_remain_num = int(ctx.rng.choice([0, 1, 1, 2]))
    n_remain_num = max(0, min(n_remain_num, MAX_DEN_DEGREE))

    caps = rational_skeleton_caps(eff, settings)
    k_hi = min(caps.max_cancel_k, MAX_DEN_DEGREE)
    if cancel_count is not None:
        k = max(0, min(int(cancel_count), k_hi))
    else:
        k = resolve_cancel_count(settings, d=eff, n_factors=max(1, k_hi), rng=ctx.rng)

    n_total = k + n_remain_num + n_remain_den
    from question_engine.frameworks.primitives.factor_sampler import sample_linear_factor

    roots: set[Fraction] = set()
    pool: list[LinearFactor] = []
    for i in range(max(1, n_total)):
        fac = sample_linear_factor(
            ctx,
            constraints=cons,
            d=eff,
            used_roots=roots,
            force_nonmonic=cons.allow_nonmonic and cons.nonmonic_weight >= 0.5 and i == 0,
        )
        pool.append(fac)
        roots.add(fac.root())

    cancel_facs = tuple(pool[:k])
    rest = pool[k:]
    remain_num: list[LinearFactor] = list(rest[:n_remain_num])
    remain_den: list[LinearFactor] = list(rest[n_remain_num : n_remain_num + n_remain_den])

    left_num: list[LinearFactor] = []
    left_den: list[LinearFactor] = []
    right_num: list[LinearFactor] = []
    right_den: list[LinearFactor] = []

    for i, fac in enumerate(remain_num):
        if i % 2 == 0:
            left_num.append(fac)
        elif op == "multiply":
            right_num.append(fac)
        else:
            right_den.append(fac)
    for i, fac in enumerate(remain_den):
        if i % 2 == 0:
            left_den.append(fac)
        elif op == "multiply":
            right_den.append(fac)
        else:
            right_num.append(fac)

    for i, fac in enumerate(cancel_facs):
        if i % 2 == 0:
            left_num.append(fac)
            if op == "multiply":
                right_den.append(fac)
            else:
                right_num.append(fac)
        else:
            left_den.append(fac)
            if op == "multiply":
                right_num.append(fac)
            else:
                right_den.append(fac)

    # Ensure each operand has a dens (render over 1 only if truly empty).
    def _force_den(slot: list[LinearFactor]) -> None:
        if slot or len(remain_den) >= MAX_DEN_DEGREE:
            return
        fac = sample_linear_factor(ctx, constraints=cons, d=eff, used_roots=roots)
        roots.add(fac.root())
        slot.append(fac)
        remain_den.append(fac)

    _force_den(left_den)
    if op == "multiply":
        _force_den(right_den)
    else:
        # After reciprocal, right_num becomes a dens — ensure non-empty dens side.
        if not right_num and not right_den:
            _force_den(right_den)

    if len(remain_den) > MAX_DEN_DEGREE:
        raise ValueError("remain den degree exceeds cap")

    style_draw = sample_factor_product(ctx, n_factors=1, d=eff, constraints=cons)
    dens_style = style_draw.dens_style
    if "expand_polynomials" in settings:
        dens_style = "expanded" if bool(settings.get("expand_polynomials")) else "factored"
    elif bool(settings.get("expand_polynomials", False)):
        dens_style = "expanded"

    var = ctx.sample_variable()
    goal_const = Fraction(int(ctx.rng.choice([1, 1, 1, 2, 3, -1, -2])))
    left_l, left_t = _render_operand_rational(
        left_num, left_den, var, dens_style=dens_style, num_const=goal_const
    )
    right_l, right_t = _render_operand_rational(
        right_num, right_den, var, dens_style=dens_style
    )

    if op == "multiply":
        prompt_l = f"{left_l} \\cdot {right_l}"
        prompt_t = f"{left_t} * {right_t}"
    else:
        from question_engine.settings.params import allowed_division_notations

        notation = ctx.rng.choice(allowed_division_notations(settings) or ["obelus"])
        if notation == "complex_fraction":
            prompt_l = rf"\frac{{{left_l}}}{{{right_l}}}"
            prompt_t = f"({left_t})/({right_t})"
        elif notation == "slash":
            prompt_l = rf"\left({left_l}\right) / \left({right_l}\right)"
            prompt_t = f"({left_t}) / ({right_t})"
        else:
            prompt_l = f"{left_l} \\div {right_l}"
            prompt_t = f"{left_t} ÷ {right_t}"

    ans_num = list(remain_num)
    ans_den = list(remain_den)
    display_cfg = resolve_display_config(settings=settings)

    if not ans_den:
        ans_l, ans_t = _render_scaled_factor_product(
            ans_num, var, const=goal_const, dens_style="factored"
        )
    else:
        num_l, num_t = _render_scaled_factor_product(
            ans_num, var, const=goal_const, dens_style="factored"
        )
        den_l, den_t = _render_factor_list(tuple(ans_den), var, dens_style="factored")
        ans_l = rf"\frac{{{num_l}}}{{{den_l}}}"
        ans_t = f"({num_t})/({den_t})"

    excl_roots = _excluded_root_values(cancel_facs)
    excl = _excluded_note(cancel_facs, var.latex)
    if excl:
        ans_l = rf"{ans_l},\; {excl}"
        roots_txt = ", ".join(str(r) for r in excl_roots)
        ans_t = f"{ans_t}, {var.name} ≠ {roots_txt}"

    display_intent = display_cfg.display_intent
    if "\\frac{\\frac" in prompt_l:
        display_intent = "complex_fraction_skill"

    meta = {
        "skeleton_pattern": "MulDivCancel",
        "skeleton_source": "rational_skeleton",
        "cancel_factor_count": k,
        "operation": op,
        "dens_style": dens_style,
        "display_normalize": display_cfg.display_normalize,
        "display_intent": display_intent,
        "display_preset": (
            "none" if display_intent == "complex_fraction_skill" else display_cfg.preset
        ),
        "n_factors": k + len(ans_num) + len(ans_den),
        "den_degree": len(ans_den),
        "excluded_values": _excluded_values_meta(excl_roots),
        "operand_count": 2,
    }

    return MulDivCancelResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        operation=op,
        cancel_count=k,
        dens_style=dens_style,
        cancel_factors=cancel_facs,
        remain_num_factors=tuple(ans_num),
        remain_den_factors=tuple(ans_den),
        effective_d=eff,
        metadata=meta,
    )


def _sample_mul_div_three_operand(
    ctx: PrimitiveContext,
    *,
    eff: float,
    cancel_count: int | None,
    cons: FactorConstraints,
    settings: dict[str, Any],
    operand_count: int,
) -> MulDivCancelResult:
    """Three-or-more operand multiply chain with cross-operand cancels (high D)."""
    from question_engine.frameworks.primitives.factor_sampler import sample_linear_factor
    from question_engine.frameworks.primitives.rational_cancel import (
        resolve_rational_cancel_count,
    )

    n_ops = max(3, int(operand_count))
    caps = rational_skeleton_caps(eff, settings)
    if cancel_count is not None:
        k = max(1, min(int(cancel_count), caps.max_cancel_k))
    else:
        k = max(1, resolve_rational_cancel_count(settings, d=eff, rng=ctx.rng))
        k = min(k, caps.max_cancel_k)

    pool_size = k + 2 * n_ops
    roots: set[Fraction] = set()
    pool: list[LinearFactor] = []
    for i in range(pool_size):
        fac = sample_linear_factor(
            ctx,
            constraints=cons,
            d=eff,
            used_roots=roots,
            force_nonmonic=cons.allow_nonmonic and i == 0,
        )
        pool.append(fac)
        roots.add(fac.root())

    shared = pool[:k]
    rest = pool[k:]
    slots: list[tuple[list[LinearFactor], list[LinearFactor]]] = []
    idx = 0
    for _ in range(n_ops):
        slots.append(([rest[idx]], [rest[idx + 1]]))
        idx += 2

    for i, fac in enumerate(shared):
        a_num, a_den = slots[i % n_ops]
        b_num, b_den = slots[(i + 1) % n_ops]
        if i % 3 == 0:
            a_num.append(fac)
            b_den.append(fac)
        elif i % 3 == 1:
            b_num.append(fac)
            slots[(i + 2) % n_ops][1].append(fac)
        else:
            a_den.append(fac)
            slots[(i + 2) % n_ops][0].append(fac)

    style_draw = sample_factor_product(ctx, n_factors=1, d=eff, constraints=cons)
    dens_style = style_draw.dens_style
    if caps.prefer_factored_prompt and dens_style == "auto":
        dens_style = "factored"
    elif bool(settings.get("expand_polynomials")):
        dens_style = "expanded"

    var = ctx.sample_variable()
    goal_const = Fraction(int(ctx.rng.choice([1, 1, 2, 3, -1, -2])))
    pieces_l: list[str] = []
    pieces_t: list[str] = []
    all_num: list[LinearFactor] = []
    all_den: list[LinearFactor] = []
    for i, (num_f, den_f) in enumerate(slots):
        nl, nt = _render_operand_rational(
            num_f,
            den_f,
            var,
            dens_style=dens_style,
            num_const=goal_const if i == 0 else None,
        )
        pieces_l.append(nl)
        pieces_t.append(nt)
        all_num.extend(num_f)
        all_den.extend(den_f)

    prompt_l = " \\cdot ".join(pieces_l)
    prompt_t = " * ".join(pieces_t)

    # Cancel shared factors for answer
    ans_num = list(all_num)
    ans_den = list(all_den)
    for fac in shared:
        for side in (ans_num, ans_den):
            for j, f in enumerate(side):
                if f.a == fac.a and f.b == fac.b:
                    side.pop(j)
                    break

    if len(ans_den) > MAX_DEN_DEGREE:
        raise ValueError("remain den degree exceeds cap")

    if not ans_den:
        ans_l, ans_t = _render_scaled_factor_product(
            ans_num, var, const=goal_const, dens_style="factored"
        )
    else:
        num_l, num_t = _render_scaled_factor_product(
            ans_num, var, const=goal_const, dens_style="factored"
        )
        den_l, den_t = _render_factor_list(tuple(ans_den), var, dens_style="factored")
        ans_l = rf"\frac{{{num_l}}}{{{den_l}}}"
        ans_t = f"({num_t})/({den_t})"

    excl_roots = _excluded_root_values(tuple(shared))
    excl = _excluded_note(tuple(shared), var.latex)
    if excl:
        ans_l = rf"{ans_l},\; {excl}"
        roots_txt = ", ".join(str(r) for r in excl_roots)
        ans_t = f"{ans_t}, {var.name} ≠ {roots_txt}"

    meta = {
        "skeleton_pattern": "MulDivCancel",
        "skeleton_source": "rational_skeleton",
        "cancel_factor_count": k,
        "operation": "multiply",
        "dens_style": dens_style,
        "n_factors": k + len(ans_num) + len(ans_den),
        "den_degree": len(ans_den),
        "excluded_values": _excluded_values_meta(excl_roots),
        "operand_count": n_ops,
    }

    return MulDivCancelResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        operation="multiply",
        cancel_count=k,
        dens_style=dens_style,
        cancel_factors=tuple(shared),
        remain_num_factors=tuple(ans_num),
        remain_den_factors=tuple(ans_den),
        effective_d=eff,
        metadata=meta,
    )


def generate_mul_div_cancel_question(
    settings: dict[str, Any] | None = None,
) -> MulDivCancelResult:
    settings = dict(settings or {})
    settings.setdefault("count", 1)
    ctx = _build_rational_ctx(
        settings,
        leaf_id=str(settings.get("_leaf_id") or "rational_expression_multiply_divide"),
    )
    return sample_mul_div_cancel(ctx)


# ---------------------------------------------------------------------------
# ComplexFracCancel — nested complex fraction skill
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ComplexFracCancelResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    style: str
    cancel_count: int
    cancel_factors: tuple[LinearFactor, ...]
    remain_factors: tuple[LinearFactor, ...]
    effective_d: float
    metadata: dict[str, Any]

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "ComplexFracCancel",
            "effective_d": self.effective_d,
            "style": self.style,
            "cancel_count": self.cancel_count,
            "cancel_factors": [f.as_dict() for f in self.cancel_factors],
            "remain_factors": [f.as_dict() for f in self.remain_factors],
            "prompt_latex": self.prompt_latex,
            "answer_latex": self.answer_latex,
            **self.metadata,
        }


def sample_complex_frac_cancel(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    constraints: FactorConstraints | None = None,
) -> ComplexFracCancelResult:
    """Generate one ComplexFracCancel item; stamps complex_fraction_skill intent."""
    settings = dict(getattr(ctx, "settings", None) or {})
    eff = float(d if d is not None else getattr(ctx, "topic_d", 0.0) or 0.0)
    cons = constraints or constraints_from_settings(settings, d=eff)

    last_err: Exception | None = None
    for _attempt in range(40):
        try:
            return _sample_complex_frac_once(ctx, eff=eff, cons=cons, settings=settings)
        except (ValueError, ZeroDivisionError) as exc:
            last_err = exc
            continue
    raise RuntimeError(f"sample_complex_frac_cancel failed: {last_err}")


def _sample_complex_frac_once(
    ctx: PrimitiveContext,
    *,
    eff: float,
    cons: FactorConstraints,
    settings: dict[str, Any],
) -> ComplexFracCancelResult:
    from question_engine.frameworks.primitives.factor_sampler import sample_linear_factor
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        SkeletonDifficultyBands,
        complex_fraction_tier_from_format,
    )
    from question_engine.settings.params import complex_fraction_structure_from_continuous

    structure = complex_fraction_structure_from_continuous(settings)
    bands = SkeletonDifficultyBands.from_d(eff)
    tier = complex_fraction_tier_from_format(bands.format_tier)
    # ``structure`` may still supply coef spans elsewhere; band follows format tier.
    _ = structure
    if bool(settings.get("allow_complex_hard", False)):
        tier = "hard"
    elif bool(settings.get("allow_complex_medium", False)) and tier == "easy":
        tier = "medium"

    var = ctx.sample_variable()
    vl = var.latex

    def _lin_tex(fac: LinearFactor) -> tuple[str, str]:
        return render_poly(fac.coeffs(), var)

    if tier == "hard":
        # ((a/L1)+(b/L2)) / (c/L3) → [(a L2 + b L1) L3] / [c L1 L2]
        # Keep final den deg ≤ 2 after cancel: choose L3 = L1 or L2 so one cancels.
        f1 = sample_linear_factor(ctx, constraints=cons, d=eff)
        f2 = sample_linear_factor(
            ctx, constraints=cons, d=eff, used_roots={f1.root()}
        )
        # Cancel one of the dens with the bottom linear.
        cancel_with = f1 if ctx.rng.random() < 0.5 else f2
        f3 = cancel_with
        a = Fraction(int(ctx.rng.choice([1, 2, 3, -1, -2])))
        b = Fraction(int(ctx.rng.choice([1, 2, 3, -1, -2])))
        c = Fraction(int(ctx.rng.choice([1, 2, 3])))
        l1l, l1t = _lin_tex(f1)
        l2l, l2t = _lin_tex(f2)
        l3l, l3t = _lin_tex(f3)
        top = (
            rf"\frac{{{num_latex(a)}}}{{{l1l}}} + \frac{{{num_latex(abs(b))}}}{{{l2l}}}"
            if b >= 0
            else rf"\frac{{{num_latex(a)}}}{{{l1l}}} - \frac{{{num_latex(abs(b))}}}{{{l2l}}}"
        )
        top_t = f"({a})/({l1t}) + ({b})/({l2t})"
        bot = rf"\frac{{{num_latex(c)}}}{{{l3l}}}"
        bot_t = f"({c})/({l3t})"
        prompt_l = rf"\frac{{{top}}}{{{bot}}}"
        prompt_t = f"(({top_t})/({bot_t}))"

        # Value = (a/L1 + b/L2) * (L3/c) = (a L2 + b L1)/(c L1 L2) * L3
        # With L3=L1: (a L2 + b L1)/(c L2)  — cancel L1
        # With L3=L2: (a L2 + b L1)/(c L1)  — cancel L2
        # Num poly: a*L2 + b*L1
        num_poly = _poly_add(
            scale_coeffs(f2.coeffs(), a),
            scale_coeffs(f1.coeffs(), b),
        )
        if f3.root() == f1.root():
            cancel_facs = (f1,)
            remain = (f2,)
            # (a L2 + b L1) / (c L2)
            # Keep structured: num stays poly, den = c * L2
        else:
            cancel_facs = (f2,)
            remain = (f1,)
        den_leading = c
        # Answer: num_poly / (c * remain)
        nl, nt = render_poly(num_poly, var)
        rl, rt = _lin_tex(remain[0])
        if den_leading == 1:
            den_l, den_t = rl, rt
        else:
            den_l = f"{num_latex(den_leading)}\\left({rl}\\right)"
            den_t = f"{den_leading}*({rt})"
        ans_l = rf"\frac{{{nl}}}{{{den_l}}}"
        ans_t = f"({nt})/({den_t})"
        style = "hard_unlike_linears"
        k = 1
    elif tier == "medium":
        # (a/L + b) / (c/L + d) with same L → ((a + b L)/(c + d L))
        # No cancel of L (it remains) unless a+bL and c+dL share a factor — keep simple:
        # Use form that cancels nothing from dens of CF but still nested skill.
        # Better medium with cancel: (a/L + b) / (c/L) = (a + b L)/c , cancel L in dens.
        fac = sample_linear_factor(ctx, constraints=cons, d=eff)
        a = Fraction(int(ctx.rng.choice([1, 2, 3, -1, -2])))
        b = Fraction(int(ctx.rng.choice([1, 2, 3, -1, -2])))
        c = Fraction(int(ctx.rng.choice([1, 2, 3, 4])))
        ll, lt = _lin_tex(fac)
        # (a/L + b) / (c/L)
        top = rf"\frac{{{num_latex(a)}}}{{{ll}}} + {num_latex(b)}"
        if b < 0:
            top = rf"\frac{{{num_latex(a)}}}{{{ll}}} - {num_latex(abs(b))}"
        prompt_l = rf"\frac{{{top}}}{{\frac{{{num_latex(c)}}}{{{ll}}}}}"
        prompt_t = f"(({a})/({lt}) + {b}) / (({c})/({lt}))"
        # = (a + b L)/c
        num_poly = _poly_add({0: a}, scale_coeffs(fac.coeffs(), b))
        nl, nt = render_poly(num_poly, var)
        if c == 1:
            ans_l, ans_t = nl, nt
        else:
            ans_l = rf"\frac{{{nl}}}{{{num_latex(c)}}}"
            ans_t = f"({nt})/({c})"
        cancel_facs = (fac,)
        remain = ()
        style = "medium_sum_over_frac"
        k = 1
    else:
        # Easy: (p + q/L) / (r/L) = (p L + q)/r
        fac = sample_linear_factor(ctx, constraints=cons, d=eff)
        p = Fraction(int(ctx.rng.choice([1, 2, 3])))
        q = Fraction(int(ctx.rng.choice([1, 2, 3, 4, 5])))
        r = Fraction(int(ctx.rng.choice([1, 2, 3, 4])))
        ll, lt = _lin_tex(fac)
        top = rf"{num_latex(p)} + \frac{{{num_latex(q)}}}{{{ll}}}"
        prompt_l = rf"\frac{{{top}}}{{\frac{{{num_latex(r)}}}{{{ll}}}}}"
        prompt_t = f"({p} + ({q})/({lt})) / (({r})/({lt}))"
        num_poly = _poly_add(scale_coeffs(fac.coeffs(), p), {0: q})
        nl, nt = render_poly(num_poly, var)
        if r == 1:
            ans_l, ans_t = nl, nt
        else:
            ans_l = rf"\frac{{{nl}}}{{{num_latex(r)}}}"
            ans_t = f"({nt})/({r})"
        cancel_facs = (fac,)
        remain = ()
        style = "easy_sum_over_frac"
        k = 1

    excl_roots = _excluded_root_values(cancel_facs)
    excl = _excluded_note(cancel_facs, vl)
    if excl:
        ans_l = rf"{ans_l},\; {excl}"
        roots_txt = ", ".join(str(r) for r in excl_roots)
        ans_t = f"{ans_t}, {var.name} ≠ {roots_txt}"

    meta = {
        "skeleton_pattern": "ComplexFracCancel",
        "skeleton_source": "rational_skeleton",
        "cancel_factor_count": k,
        "style": style,
        "display_intent": "complex_fraction_skill",
        "display_normalize": True,
        "display_preset": "none",
        "display_rules": [],
        "excluded_values": _excluded_values_meta(excl_roots),
        "tier": tier,
    }

    return ComplexFracCancelResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        style=style,
        cancel_count=k,
        cancel_factors=cancel_facs,
        remain_factors=remain,
        effective_d=eff,
        metadata=meta,
    )


def generate_complex_frac_cancel_question(
    settings: dict[str, Any] | None = None,
) -> ComplexFracCancelResult:
    settings = dict(settings or {})
    settings.setdefault("count", 1)
    ctx = _build_rational_ctx(
        settings,
        leaf_id=str(settings.get("_leaf_id") or "complex_fractions"),
    )
    return sample_complex_frac_cancel(ctx)


# ---------------------------------------------------------------------------
# EqCancel — clear dens + check extraneous (Phase 1.5)
# ---------------------------------------------------------------------------

_LEGACY_EQ_CANCEL = {
    "hand",
    "constructive",
    "legacy",
    "rational_equations",
    "sample_rational_equation",
}


def use_eq_cancel_skeleton(settings: dict[str, Any] | None) -> bool:
    """EqCancel is the live default for rational-equation leaves."""
    s = dict(settings or {})
    if bool(s.get("use_hand_rational_equations")) or bool(
        s.get("use_constructive_rational")
    ):
        return False
    if bool(s.get("use_eq_cancel_skeleton") is False):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_EQ_CANCEL:
        return False
    if "use_eq_cancel_skeleton" in s:
        return bool(s.get("use_eq_cancel_skeleton"))
    if pat in {"EqCancel", "eq_cancel"}:
        return True
    return True


@dataclass(frozen=True)
class EqCancelResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    style: str
    excluded: tuple[Fraction, ...]
    solution: Fraction | None
    upgrades: tuple[str, ...]
    effective_d: float
    metadata: dict[str, Any]

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "EqCancel",
            "style": self.style,
            "excluded": [str(x) for x in self.excluded],
            **self.metadata,
        }


def sample_eq_cancel(ctx: PrimitiveContext) -> EqCancelResult:
    """Clear denominators, solve, reject extraneous roots.

    D=0 is a proportion ``a/b = x/c``. Format unlocks one linear den, then
    two dens / LCD, then a planted extraneous root.
    """
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        SkeletonDifficultyBands,
    )

    rng = ctx.rng
    d = float(getattr(ctx, "topic_d", 0.0) or 0.0)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    var = ctx.sample_variable()
    settings = dict(getattr(ctx, "settings", None) or {})
    cons = constraints_from_settings(settings, d=d)
    hi = (4, 7, 11, 16, 24)[max(0, min(4, nt))]

    def _finish_eq(
        prompt_l: str,
        prompt_t: str,
        ans_l: str,
        ans_t: str,
        *,
        style: str,
        excluded: tuple[Fraction, ...],
        solution: Fraction | None,
        tags: tuple[str, ...],
    ) -> EqCancelResult:
        meta = {
            "skeleton_pattern": "EqCancel",
            "skeleton_source": "rational_skeleton",
            "style": style,
            "numeric_tier": nt,
            "format_tier": ft,
            "form_id": "rational_equation",
            "openstax_form": "rational_equation",
            "excluded_values": [str(x) for x in excluded],
            "construction": "clear_dens",
        }
        return EqCancelResult(
            prompt_latex=prompt_l,
            prompt_text=prompt_t,
            answer_latex=ans_l,
            answer_text=ans_t,
            style=style,
            excluded=excluded,
            solution=solution,
            upgrades=tags,
            effective_d=d,
            metadata=meta,
        )

    if ft == 0:
        a = rng.randint(1, max(2, hi // 2))
        b = rng.randint(2, max(3, hi // 2 + 1))
        c = rng.randint(2, max(3, hi // 2 + 1))
        if nt == 0:
            a, b, c = rng.choice([(2, 3, 4), (1, 2, 3), (3, 5, 4), (2, 5, 6)])
        sol = Fraction(a * c, b)
        left = rf"\frac{{{num_latex(Fraction(a))}}}{{{num_latex(Fraction(b))}}}"
        right = rf"\frac{{{var.latex}}}{{{num_latex(Fraction(c))}}}"
        prompt_l = f"{left} = {right}"
        prompt_t = f"({a})/({b}) = ({var.name})/({c})"
        ans_l = f"{var.latex} = {num_latex(sol)}"
        return _finish_eq(
            prompt_l,
            prompt_t,
            ans_l,
            f"{var.name} = {sol}",
            style="proportion",
            excluded=(),
            solution=sol,
            tags=("eq_cancel", "proportion"),
        )

    if ft == 1:
        # a / (x - r) = b   →  x = r + a/b, exclude x = r
        fac = sample_linear_factor(ctx, constraints=cons, d=d)
        r = fac.root()
        a = Fraction(rng.randint(1, max(2, hi // 2)))
        b = Fraction(rng.randint(1, max(2, hi // 3 + 1)))
        den_l, den_t = render_factor(fac, var.latex)
        prompt_l = rf"\frac{{{num_latex(a)}}}{{{den_l}}} = {num_latex(b)}"
        prompt_t = f"({a})/({den_t}) = {b}"
        sol = r + (a / b)
        if sol == r:
            b = b + Fraction(1)
            sol = r + (a / b)
            prompt_l = rf"\frac{{{num_latex(a)}}}{{{den_l}}} = {num_latex(b)}"
        ans_l = f"{var.latex} = {num_latex(sol)}"
        note = rf"{var.latex} \neq {num_latex(r)}"
        ans_l = rf"{ans_l},\; {note}"
        return _finish_eq(
            prompt_l,
            prompt_t,
            ans_l,
            f"{var.name} = {sol}, {var.name} != {r}",
            style="one_linear_den",
            excluded=(r,),
            solution=sol,
            tags=("eq_cancel", "one_den"),
        )

    if ft >= 3 and rng.random() < 0.55:
        # Plant extraneous: x/(x-p) = p/(x-p) → x = p excluded → empty
        p = Fraction(rng.randint(1, max(2, hi // 3 + 1)))
        den_l, den_t = join_signed_terms(
            [(Fraction(1), var.latex), (Fraction(-p), "")]
        )
        prompt_l = (
            rf"\frac{{{var.latex}}}{{{den_l}}} = \frac{{{num_latex(p)}}}{{{den_l}}}"
        )
        prompt_t = f"({var.name})/({den_t}) = ({p})/({den_t})"
        return _finish_eq(
            prompt_l,
            prompt_t,
            r"\emptyset",
            "empty set",
            style="extraneous",
            excluded=(p,),
            solution=None,
            tags=("eq_cancel", "extraneous"),
        )

    # Two linear dens: a/(x-p) = b/(x-q)
    f1 = sample_linear_factor(ctx, constraints=cons, d=d)
    f2 = sample_linear_factor(ctx, constraints=cons, d=d, used_roots={f1.root()})
    a = Fraction(rng.randint(1, max(2, hi // 3 + 1)))
    b = Fraction(rng.randint(1, max(2, hi // 3 + 1)))
    p, q = f1.root(), f2.root()
    l1, t1 = render_factor(f1, var.latex)
    l2, t2 = render_factor(f2, var.latex)
    prompt_l = (
        rf"\frac{{{num_latex(a)}}}{{{l1}}} = \frac{{{num_latex(b)}}}{{{l2}}}"
    )
    prompt_t = f"({a})/({t1}) = ({b})/({t2})"
    # a (x-q) = b (x-p)  if dens are monic x-p, x-q
    # a x - a q = b x - b p  →  (a-b)x = a q - b p
    # General: a * f2(x) = b * f1(x) for dens f1, f2
    # a (a2 x + b2) = b (a1 x + b1)
    a1, b1c = f1.a, f1.b
    a2, b2c = f2.a, f2.b
    left_lead = a * a2 - b * a1
    left_const = a * b2c - b * b1c
    excluded = tuple(sorted({p, q}, key=lambda z: float(z)))
    if left_lead == 0:
        # either identity or empty
        if left_const == 0:
            ans_l = r"\text{all real numbers except excluded}"
            sol: Fraction | None = None
            style = "identity_holes"
        else:
            ans_l = r"\emptyset"
            sol = None
            style = "no_solution"
        return _finish_eq(
            prompt_l,
            prompt_t,
            ans_l,
            ans_l,
            style=style,
            excluded=excluded,
            solution=sol,
            tags=("eq_cancel", "two_den", style),
        )
    sol = -left_const / left_lead
    if sol in {p, q}:
        return _finish_eq(
            prompt_l,
            prompt_t,
            r"\emptyset",
            "empty set",
            style="extraneous",
            excluded=excluded,
            solution=None,
            tags=("eq_cancel", "two_den", "extraneous"),
        )
    note = ", ".join(num_latex(x) for x in excluded)
    ans_l = rf"{var.latex} = {num_latex(sol)},\; {var.latex} \neq {note}"
    return _finish_eq(
        prompt_l,
        prompt_t,
        ans_l,
        f"{var.name} = {sol}",
        style="two_linear_dens",
        excluded=excluded,
        solution=sol,
        tags=("eq_cancel", "two_den"),
    )
