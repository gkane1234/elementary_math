"""AffineInflate — like terms / distribute / expand from a simplified affine.

Not SolveLinear. Goal is the simplified ``a x + b``; the prompt is inflated.

Term counts copy the **legacy** samplers at the same slider D (measured live):

- **like_terms** (``sample_like_terms``): D=0 stays ``3x+2x`` (AffineInflate
  classroom seed). D=8 extra likes/constants (~4–5). D=16 can reach 8
  (``many_terms``). D=22 can reach 10 with a second variable. Old max is 8–10.
- **distribute** (``sample_distributive_algebraic``): D=0 ``2(x+3)``. Then 3
  terms inside one factor, then two-binomials. Old max is ~4 display terms —
  not an 8-term sum of distributes.
- **expand** (``construct_affine``): D=0 one factor; then leftover remainder.
  Old max is ~5–6 display terms.
- **evaluate** (``construct_affine`` + substitute): D=0 is already-simplified
  ``ax+b`` (old ``3+x`` / ``1-3x``), then leftover distribute. Not expand's
  D=0 ``2(x+3)``.

Numeric hardness (coeff size, signs) before those format unlocks.
Opt-out: ``use_sample_like_terms=True``, ``use_sample_distributive=True``,
``use_sample_expand_simplify=True``, ``use_sample_evaluate=True``, or
``use_affine_inflate_skeleton=False``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.primitives._algebra_render import (
    join_signed_terms,
    num_latex,
    sample_integerish,
)
from question_engine.frameworks.primitives.constructive import (
    AffineTarget,
    construct_affine,
    verify_affine,
)
from question_engine.frameworks.primitives.registry import PrimitiveContext
from question_engine.frameworks.primitives.skeleton_difficulty import SkeletonDifficultyBands

Mode = Literal["like_terms", "distribute", "expand", "evaluate"]

_LEGACY = {
    "like_terms",
    "distributive",
    "expand_simplify",
    "hand",
    "constructive",
    "legacy",
}


@dataclass(frozen=True)
class AffineInflateResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    mode: Mode
    coeff_a: Fraction
    coeff_b: Fraction
    upgrades: tuple[str, ...]
    effective_d: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "AffineInflate",
            "mode": self.mode,
            "coeff_a": str(self.coeff_a),
            "coeff_b": str(self.coeff_b),
            **self.metadata,
        }


def use_affine_inflate_skeleton(
    settings: dict[str, Any] | None,
    *,
    mode: Mode = "like_terms",
) -> bool:
    s = dict(settings or {})
    if bool(s.get("use_affine_inflate_skeleton") is False):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY:
        return False
    if mode == "like_terms" and bool(s.get("use_sample_like_terms")):
        return False
    if mode == "distribute" and bool(
        s.get("use_sample_distributive") or s.get("use_sample_distributive_algebraic")
    ):
        return False
    if mode == "expand" and bool(s.get("use_sample_expand_simplify")):
        return False
    if mode == "evaluate" and bool(s.get("use_sample_evaluate")):
        return False
    if "use_affine_inflate_skeleton" in s:
        return bool(s.get("use_affine_inflate_skeleton"))
    if pat in {"AffineInflate", "affine_inflate"}:
        return True
    return True


def _hi(nt: int) -> int:
    return (4, 8, 14, 22, 32)[max(0, min(4, nt))]


def _like_coeff_hi(nt: int) -> int:
    """Per-term |coeff| cap from live old like-terms samples (max 3 / 6 / 14 / 12 / 27)."""
    return (3, 6, 8, 12, 16)[max(0, min(4, nt))]


def _split_positive(total: int, rng, *, n: int = 2) -> list[int]:
    total = max(2, int(total))
    n = max(2, min(n, total))
    parts = [1] * n
    left = total - n
    for _ in range(left):
        parts[rng.randrange(n)] += 1
    rng.shuffle(parts)
    return parts


def _term_coeff(rng, hi: int, *, allow_neg: bool) -> Fraction:
    """Classroom integer coeff; signs only when the old sampler had negatives."""
    v = int(rng.randint(1, max(1, int(hi))))
    if allow_neg and rng.random() < 0.4:
        v = -v
    return Fraction(v)


def _like_term_plan(nt: int, ft: int, d: float, rng) -> tuple[int, int, int]:
    """(n_x, n_const, n_y) matching live ``sample_like_terms`` at this slider D.

    Measured (g6, integers_only, 20 seeds): D=0 → 4; D=8 → 4–5; D=16 → med 8
    (max 8); D=22 → med 10 (max 10). AffineInflate D=0 stays 2 likes (``3x+2x``).
    """
    if d <= 1e-12:
        return 2, 0, 0
    # D≈4–7 (nt≤1, ft=0): one extra constant — old mid band 3–4, not 8.
    if ft <= 0 and nt <= 1:
        return 2, 1, 0
    # D≈8 (nt≥2, ft=0): old more_like — 4 or 5 terms.
    if ft <= 0:
        return (3, 2, 0) if rng.random() < 0.65 else (2, 2, 0)
    # D≥10 ft=1: still extra likes/constants, not many_terms yet.
    if ft == 1:
        return 3, 2, 0
    # D≥16 ft=2: old many_terms majority 8; not every seed.
    if ft == 2:
        r = rng.random()
        if r < 0.65:
            return 5, 3, 0
        if r < 0.95:
            return 3, 2, 0
        return 2, 2, 0
    # D≥22 ft≥3: old second_variable majority 10.
    r = rng.random()
    if r < 0.55:
        return 5, 3, 2
    if r < 0.85:
        return 5, 3, 0
    if r < 0.95:
        return 3, 2, 0
    return 2, 2, 0


def _k_times_group(k: int, inner_l: str, inner_t: str) -> tuple[str, str]:
    kl = num_latex(Fraction(k))
    if k == -1:
        return f"-\\left({inner_l}\\right)", f"-({inner_t})"
    if k == 1:
        return f"\\left({inner_l}\\right)", f"({inner_t})"
    return f"{kl}\\left({inner_l}\\right)", f"{k}({inner_t})"


def _like_terms(ctx: PrimitiveContext) -> AffineInflateResult:
    rng = ctx.rng
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    var = ctx.sample_variable()
    hi = _like_coeff_hi(nt)
    n_x, n_const, n_y = _like_term_plan(nt, ft, d, rng)
    allow_neg = nt >= 1

    if d <= 1e-12:
        # D=0 classroom: 3x+2x, not x+x.
        sampled = sample_integerish(ctx, exclude_zero=True, prefer_positive=True)
        a_tot = abs(int(sampled.value))
        a_tot = max(3, min(max(hi, 3), max(a_tot, 3)))
        parts_a = _split_positive(a_tot, rng, n=2)
        terms: list[tuple[Fraction, str]] = [(Fraction(p), var.latex) for p in parts_a]
        a = Fraction(a_tot)
        b = Fraction(0)
        y_var = None
        y_coeffs: list[Fraction] = []
    else:
        x_coeffs = [_term_coeff(rng, hi, allow_neg=allow_neg) for _ in range(n_x)]
        const_coeffs = [
            _term_coeff(rng, max(2, hi // 2), allow_neg=allow_neg)
            for _ in range(n_const)
        ]
        y_var = None
        y_coeffs = []
        if n_y > 0 and getattr(ctx.policy, "max_variables", 1) >= 2:
            for _ in range(8):
                cand = ctx.sample_variable()
                if cand.name != var.name:
                    y_var = cand
                    break
            if y_var is not None:
                y_coeffs = [
                    _term_coeff(rng, hi, allow_neg=allow_neg) for _ in range(n_y)
                ]
        terms = [(c, var.latex) for c in x_coeffs]
        terms.extend((c, "") for c in const_coeffs)
        if y_var is not None:
            terms.extend((c, y_var.latex) for c in y_coeffs)
        rng.shuffle(terms)
        a = sum(x_coeffs, Fraction(0))
        b = sum(const_coeffs, Fraction(0))

    prompt_l, prompt_t = join_signed_terms(terms)
    simp: list[tuple[Fraction, str]] = []
    if a != 0:
        simp.append((a, var.latex))
    if y_var is not None:
        total_y = sum(y_coeffs, Fraction(0))
        if total_y != 0:
            simp.append((total_y, y_var.latex))
    if b != 0:
        simp.append((b, ""))
    ans_l, ans_t = join_signed_terms(simp)
    if not ans_l:
        ans_l, ans_t = "0", "0"
    n_terms = len([c for c, _ in terms if c != 0])
    meta = {
        "skeleton_pattern": "AffineInflate",
        "skeleton_source": "affine_skeleton",
        "mode": "like_terms",
        "species": "like_terms",
        "numeric_tier": nt,
        "format_tier": ft,
        "n_likes": n_x,
        "n_const": n_const,
        "n_terms": n_terms,
        "form_id": "like_terms_split",
    }
    return AffineInflateResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        mode="like_terms",
        coeff_a=Fraction(a),
        coeff_b=b,
        upgrades=("like_terms", f"likes:{n_x}", f"terms:{n_terms}"),
        effective_d=d,
        metadata=meta,
    )


def _simple_distribute(
    ctx: PrimitiveContext,
    *,
    var,
    k: int,
    inner_a: Fraction,
    n: int,
) -> tuple[str, str, str, str, Fraction, Fraction, tuple[str, ...]]:
    a = Fraction(k) * inner_a
    b = Fraction(k) * Fraction(n)
    inner_l, inner_t = join_signed_terms(
        [(inner_a, var.latex), (Fraction(n), "")]
    )
    prompt_l, prompt_t = _k_times_group(k, inner_l, inner_t)
    ans_l, ans_t = join_signed_terms([(a, var.latex), (b, "")])
    return prompt_l, prompt_t, ans_l, ans_t, a, b, ("distribute",)


def _three_inside_distribute(
    ctx: PrimitiveContext,
    *,
    var,
    k: int,
    hi: int,
    allow_neg: bool,
) -> tuple[str, str, str, str, Fraction, Fraction, tuple[str, ...]]:
    """Old ``three_terms``: ``k(x+n1+n2)``. Max ~3 display terms."""
    rng = ctx.rng
    n1 = _term_coeff(rng, max(1, min(hi, 6)), allow_neg=allow_neg)
    n2 = _term_coeff(rng, max(1, min(hi, 6)), allow_neg=allow_neg)
    inner_l, inner_t = join_signed_terms(
        [(Fraction(1), var.latex), (n1, ""), (n2, "")]
    )
    prompt_l, prompt_t = _k_times_group(k, inner_l, inner_t)
    a = Fraction(k)
    b = Fraction(k) * (n1 + n2)
    ans_l, ans_t = join_signed_terms([(a, var.latex), (b, "")])
    return prompt_l, prompt_t, ans_l, ans_t, a, b, ("distribute", "three_inside")


def _two_binomials_distribute(
    ctx: PrimitiveContext,
    *,
    var,
    hi: int,
    allow_neg: bool,
) -> tuple[str, str, str, str, Fraction, Fraction, tuple[str, ...]]:
    """Old ``two_binomials``: ``(x+p)(q+r)``. Max ~4 display terms."""
    rng = ctx.rng
    cap = max(1, min(int(hi), 6))
    p = _term_coeff(rng, cap, allow_neg=allow_neg)
    q = _term_coeff(rng, cap, allow_neg=False)
    r = _term_coeff(rng, cap, allow_neg=allow_neg)
    left_l, left_t = join_signed_terms([(Fraction(1), var.latex), (p, "")])
    right_l, right_t = join_signed_terms([(q, ""), (r, "")])
    prompt_l = f"\\left({left_l}\\right)\\left({right_l}\\right)"
    prompt_t = f"({left_t})({right_t})"
    outer = q + r
    a = outer
    b = p * outer
    ans_l, ans_t = join_signed_terms(
        ([(a, var.latex)] if a != 0 else []) + ([(b, "")] if b != 0 else [])
    )
    if not ans_l:
        ans_l, ans_t = "0", "0"
    return prompt_l, prompt_t, ans_l, ans_t, a, b, ("two_binomials",)


def _construct_expand(
    ctx: PrimitiveContext,
    *,
    var,
    target: AffineTarget,
    d: float,
    min_inflators: int,
    fallback,
) -> tuple[str, str, str, str, Fraction, Fraction, tuple[str, ...]]:
    surface = construct_affine(
        ctx,
        d=max(1.0, d),
        var=var,
        target=target,
        prefer_distribute=True,
        min_inflators=min_inflators,
    )
    if not verify_affine(surface, target):
        return fallback
    prompt_l, prompt_t = surface.latex, surface.text
    if surface.simplified_latex and surface.simplified_text:
        ans_l, ans_t = surface.simplified_latex, surface.simplified_text
    else:
        ans_l, ans_t = join_signed_terms(
            ([(target.a, var.latex)] if target.a != 0 else [])
            + ([(target.b, "")] if target.b != 0 else [])
        )
    return (
        prompt_l,
        prompt_t,
        ans_l,
        ans_t,
        target.a,
        target.b,
        tuple(surface.inflators_applied),
    )


def _distribute_or_expand(ctx: PrimitiveContext, *, mode: Mode) -> AffineInflateResult:
    rng = ctx.rng
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    var = ctx.sample_variable()
    hi = _hi(nt)
    k_cap = _like_coeff_hi(nt)
    sampled = sample_integerish(ctx, exclude_zero=True, prefer_positive=nt == 0)
    k = abs(int(sampled.value))
    k = max(2, min(k_cap, max(k, 2)))
    if nt >= 2 and rng.random() < 0.3:
        k = -k
    n = rng.randint(1, max(1, min(hi, 4 + nt)))
    if nt >= 1 and rng.random() < 0.25:
        n = -n
    inner_a = Fraction(1)
    if ft >= 2 and nt >= 1:
        inner_a = Fraction(rng.choice([1, 1, 2, -1]))
    a = Fraction(k) * inner_a
    b = Fraction(k) * Fraction(n)
    target = AffineTarget(a=a, b=b)
    min_inflators = 1 if mode == "distribute" else (
        1 + (1 if ft >= 2 else 0) + (1 if ft >= 3 else 0)
    )
    simple = _simple_distribute(
        ctx, var=var, k=k, inner_a=inner_a, n=n
    )
    form_id = "distribute_binomial" if mode == "distribute" else "expand_affine"

    if d <= 1e-12:
        prompt_l, prompt_t, ans_l, ans_t, a, b, tags = simple
    elif mode == "distribute" and ft >= 2 and rng.random() < 0.45:
        # Old D=16+ two_binomials (~half of samples).
        prompt_l, prompt_t, ans_l, ans_t, a, b, tags = _two_binomials_distribute(
            ctx, var=var, hi=hi, allow_neg=nt >= 1
        )
        form_id = "two_binomials"
    elif mode == "distribute" and (ft >= 1 or nt >= 2):
        # Old three_terms at D=8: k(x+n1+n2).
        prompt_l, prompt_t, ans_l, ans_t, a, b, tags = _three_inside_distribute(
            ctx, var=var, k=k, hi=hi, allow_neg=nt >= 1
        )
        form_id = "distribute_trinomial"
    else:
        # Expand (and leftover distribute): old construct_affine path.
        prompt_l, prompt_t, ans_l, ans_t, a, b, tags = _construct_expand(
            ctx,
            var=var,
            target=target,
            d=d,
            min_inflators=min_inflators,
            fallback=simple,
        )

    meta = {
        "skeleton_pattern": "AffineInflate",
        "skeleton_source": "affine_skeleton",
        "mode": mode,
        "species": mode,
        "numeric_tier": nt,
        "format_tier": ft,
        "form_id": form_id,
    }
    return AffineInflateResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        mode=mode,
        coeff_a=a,
        coeff_b=b,
        upgrades=tags,
        effective_d=d,
        metadata=meta,
    )


def _evaluate_affine(ctx: PrimitiveContext) -> AffineInflateResult:
    """Old evaluate leaf: D=0 is ``ax+b``; leftover distribute later.

    Not expand's D=0 ``2(x+3)``. Value is ``a·subst + b`` of the seeded target.
    """
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    var = ctx.sample_variable()
    min_inflators = 0 if d <= 1e-12 else 1
    surface = construct_affine(
        ctx,
        d=d,
        var=var,
        prefer_distribute=True,
        min_inflators=min_inflators,
    )
    a = Fraction(surface.coeff_a)
    b = Fraction(surface.coeff_b)
    subst_hi = (4, 6, 8, 10, 12)[max(0, min(4, nt))]
    try:
        sampled = ctx.sample_number(exclude_zero=True)
        subst = Fraction(sampled.value)
        if abs(int(subst)) > subst_hi and subst.denominator == 1:
            subst = Fraction(ctx.rng.choice([-subst_hi, -2, -1, 1, 2, subst_hi]))
    except Exception:
        subst_n = int(ctx.rng.randint(-subst_hi, subst_hi))
        if subst_n == 0:
            subst_n = int(ctx.rng.choice([-3, -2, -1, 1, 2, 3]))
        subst = Fraction(subst_n)
    if subst == 0:
        subst = Fraction(ctx.rng.choice([-3, -2, -1, 1, 2, 3]))
    value = a * subst + b
    subst_l = num_latex(subst)
    prompt_l = f"{surface.latex} \\text{{ when }} {var.latex} = {subst_l}"
    prompt_t = f"{surface.text} when {var.name} = {subst_l}"
    ans_l = num_latex(value)
    meta = {
        "skeleton_pattern": "AffineInflate",
        "skeleton_source": "affine_skeleton",
        "mode": "evaluate",
        "species": "evaluate",
        "numeric_tier": nt,
        "format_tier": ft,
        "form_id": "evaluate_affine",
        "subst": str(subst),
        "inflators": list(surface.inflators_applied),
    }
    return AffineInflateResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_l,
        mode="evaluate",
        coeff_a=a,
        coeff_b=b,
        upgrades=tuple(surface.inflators_applied) + ("evaluate",),
        effective_d=d,
        metadata=meta,
    )


def sample_affine_inflate(
    ctx: PrimitiveContext,
    *,
    mode: Mode | None = None,
) -> AffineInflateResult:
    """Inflate a simplified affine into a classroom unsimplified prompt."""
    leaf = str(getattr(ctx, "leaf_id", "") or "")
    resolved: Mode = mode or "like_terms"
    if mode is None:
        if "evaluat" in leaf:
            resolved = "evaluate"
        elif "distribut" in leaf:
            resolved = "distribute"
        elif "expand" in leaf or "simplifying_algebraic" in leaf:
            resolved = "expand"
        else:
            resolved = "like_terms"
    if resolved == "like_terms":
        return _like_terms(ctx)
    if resolved == "evaluate":
        return _evaluate_affine(ctx)
    return _distribute_or_expand(ctx, mode=resolved)
