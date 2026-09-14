"""Trig identity / equation skeletons — OpenStax Precalc §7.1–7.5.

Species
-------
- **TrigRewrite** — fundamental identities (§7.1): simplify / verify.
- **TrigSumDiff** — sum/difference expand + exact eval unlock (§7.2).
- **TrigDoubleAngle** — double-angle rewrite (§7.3; half-angle deferred).
- **TrigProductToSum** — product→sum rewrite (§7.4; sum→product stub).
- **TrigFactorEq** — factor / quadratic / double-angle equations (§7.5).

Pipeline
--------
1. Select ``form_id`` from PC trig catalogs for PC leaves.
2. Map continuous D → numeric/format tiers (structure unlocks lag numeric).
3. Sample a rule / template from the D-gated pool.
4. Package as Expand / Rewrite / Simplify / Solve / Verify.

Opt-out
-------
Identities: ``use_sample_trig_identities=True``, ``use_trig_identity_skeleton=False``,
or ``skeleton_pattern`` matching the old generator name / ``hand`` / ``precalc``.
Equations: ``use_sample_trig_equations=True``, ``use_trig_equation_skeleton=False``,
or ``skeleton_pattern`` = ``trig_factoring_equations``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from question_engine.frameworks.primitives.registry import PrimitiveContext
from question_engine.frameworks.primitives.skeleton_difficulty import (
    SkeletonDifficultyBands,
)

Mode = Literal["simplify", "rewrite", "verify"]
Family = Literal[
    "pythagorean",
    "reciprocal",
    "product",
    "verify",
    "sum_difference",
    "double_angle",
    "product_to_sum",
    "quadratic_in_trig",
    "factor_fundamental",
    "double_angle_equation",
]

CATALOG_NAME = "precalculus_trig_identities"

# form_id → construction knobs
_FORM_KNOBS: dict[str, dict[str, Any]] = {
    "pythagorean_basic": {"family": "pythagorean", "min_steps": 1, "max_steps": 2},
    "reciprocal_quotient": {"family": "reciprocal", "min_steps": 1, "max_steps": 1},
    "verify_fundamental": {"family": "verify", "min_steps": 1, "max_steps": 2},
}

_LEGACY_PATTERNS = {
    "trig_basic_identities",
    "trig_sum_difference",
    "trig_multiple_angle",
    "trig_product_to_sum",
    "trig_factoring_equations",
    "simple_trig_equations",
    "hand",
    "precalc",
    "constructive",
    "legacy",
}


@dataclass(frozen=True)
class TrigRule:
    """One identity step: prompt expression simplifies to answer."""

    prompt: str
    answer: str
    family: Family
    rule_id: str
    steps: int = 1


# Single-step fundamental identities (D=0 box).
_PYTHAGOREAN: tuple[TrigRule, ...] = (
    TrigRule(r"\sin^2 \theta + \cos^2 \theta", "1", "pythagorean", "sin2_cos2"),
    TrigRule(r"\sec^2 \theta - \tan^2 \theta", "1", "pythagorean", "sec2_tan2"),
    TrigRule(r"1 + \cot^2 \theta", r"\csc^2 \theta", "pythagorean", "1_cot2"),
    TrigRule(r"1 - \cos^2 \theta", r"\sin^2 \theta", "pythagorean", "1_minus_cos2"),
    TrigRule(r"\sec^2 \theta - 1", r"\tan^2 \theta", "pythagorean", "sec2_minus_1"),
    TrigRule(r"\csc^2 \theta - 1", r"\cot^2 \theta", "pythagorean", "csc2_minus_1"),
)

_RECIPROCAL: tuple[TrigRule, ...] = (
    TrigRule(r"\tan \theta", r"\frac{\sin \theta}{\cos \theta}", "reciprocal", "tan_quotient"),
    TrigRule(r"\cot \theta", r"\frac{\cos \theta}{\sin \theta}", "reciprocal", "cot_quotient"),
    TrigRule(r"\sec \theta", r"\frac{1}{\cos \theta}", "reciprocal", "sec_recip"),
    TrigRule(r"\csc \theta", r"\frac{1}{\sin \theta}", "reciprocal", "csc_recip"),
)

_PRODUCT: tuple[TrigRule, ...] = (
    TrigRule(r"\tan \theta \cot \theta", "1", "product", "tan_cot"),
    TrigRule(r"\sec \theta \cos \theta", "1", "product", "sec_cos"),
    TrigRule(r"\csc \theta \sin \theta", "1", "product", "csc_sin"),
)

# Multi-step compound shapes (format tier ≥ 1).
_COMPOUND: tuple[TrigRule, ...] = (
    TrigRule(
        r"(1 - \cos^2 \theta)(1 + \cot^2 \theta)",
        "1",
        "pythagorean",
        "sin2_times_csc2",
        steps=2,
    ),
    TrigRule(
        r"\frac{\sec^2 \theta - 1}{\sec^2 \theta}",
        r"\sin^2 \theta",
        "pythagorean",
        "sec_frac_sin2",
        steps=2,
    ),
    TrigRule(
        r"\frac{\cot \theta}{\csc \theta}",
        r"\cos \theta",
        "reciprocal",
        "cot_over_csc",
        steps=1,
    ),
    TrigRule(
        r"\csc \theta \cos \theta \tan \theta",
        "1",
        "product",
        "csc_cos_tan",
        steps=2,
    ),
    TrigRule(
        r"\sin^2 \theta \sec^2 \theta",
        r"\tan^2 \theta",
        "pythagorean",
        "sin2_sec2",
        steps=2,
    ),
    TrigRule(
        r"\cos^2 \theta \csc^2 \theta",
        r"\cot^2 \theta",
        "pythagorean",
        "cos2_csc2",
        steps=2,
    ),
)

_VERIFY: tuple[TrigRule, ...] = (
    TrigRule(
        r"\tan \theta \cos \theta",
        r"\sin \theta",
        "verify",
        "tan_cos_sin",
    ),
    TrigRule(
        r"\csc \theta \cos \theta \tan \theta",
        "1",
        "verify",
        "csc_cos_tan_one",
        steps=2,
    ),
    TrigRule(
        r"\frac{\cot \theta}{\csc \theta}",
        r"\cos \theta",
        "verify",
        "cot_over_csc",
    ),
    TrigRule(
        r"\sec \theta \cos \theta",
        "1",
        "verify",
        "sec_cos_one",
    ),
)


@dataclass(frozen=True)
class TrigRewriteResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    mode: Mode
    family: str
    n_steps: int
    rule_id: str
    form_id: str | None
    effective_d: float
    metadata: dict[str, Any]

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": self.metadata.get("skeleton_pattern") or "TrigRewrite",
            "mode": self.mode,
            "family": self.family,
            "n_steps": self.n_steps,
            "rule_id": self.rule_id,
            "form_id": self.form_id,
            **self.metadata,
        }


def _opt_out_identity(settings: dict[str, Any] | None) -> bool:
    """True when caller wants the old precalc identity path."""
    s = dict(settings or {})
    if bool(s.get("use_sample_trig_identities")):
        return True
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_PATTERNS:
        return True
    if "use_trig_identity_skeleton" in s and not bool(s.get("use_trig_identity_skeleton")):
        return True
    return False


def use_trig_identity_skeleton(settings: dict[str, Any] | None) -> bool:
    """TrigRewrite is the live default for ``trig_basic_identities`` PC leaves."""
    if _opt_out_identity(settings):
        return False
    pat = str((settings or {}).get("skeleton_pattern", "")).strip()
    if pat in {"TrigRewrite", "trig_rewrite"}:
        return True
    return True


def use_trig_sum_diff_skeleton(settings: dict[str, Any] | None) -> bool:
    if _opt_out_identity(settings):
        return False
    pat = str((settings or {}).get("skeleton_pattern", "")).strip()
    if pat in {"TrigSumDiff", "trig_sum_diff"}:
        return True
    return True


def use_trig_double_angle_skeleton(settings: dict[str, Any] | None) -> bool:
    if _opt_out_identity(settings):
        return False
    pat = str((settings or {}).get("skeleton_pattern", "")).strip()
    if pat in {"TrigDoubleAngle", "trig_double_angle"}:
        return True
    return True


def use_trig_product_to_sum_skeleton(settings: dict[str, Any] | None) -> bool:
    if _opt_out_identity(settings):
        return False
    pat = str((settings or {}).get("skeleton_pattern", "")).strip()
    if pat in {"TrigProductToSum", "trig_product_to_sum_skel"}:
        return True
    return True


def use_trig_factor_eq_skeleton(settings: dict[str, Any] | None) -> bool:
    """TrigFactorEq live default for ``trig_factoring_equations`` PC leaves."""
    s = dict(settings or {})
    if bool(s.get("use_sample_trig_equations")):
        return False
    if bool(s.get("use_sample_trig_identities")):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_PATTERNS:
        return False
    if "use_trig_equation_skeleton" in s:
        return bool(s.get("use_trig_equation_skeleton"))
    if pat in {"TrigFactorEq", "trig_factor_eq"}:
        return True
    return True


def knobs_from_form_id(form_id: str) -> dict[str, Any]:
    return dict(_FORM_KNOBS.get(str(form_id or ""), {}))


def _rules_for_family(family: str, *, format_tier: int) -> tuple[TrigRule, ...]:
    fam = str(family or "pythagorean")
    if fam == "verify":
        return _VERIFY
    if fam == "reciprocal":
        pool: list[TrigRule] = list(_RECIPROCAL)
        if format_tier >= 1:
            pool.extend(r for r in _COMPOUND if r.family == "reciprocal")
        return tuple(pool)
    if fam == "product":
        return _PRODUCT + (
            tuple(r for r in _COMPOUND if r.family == "product") if format_tier >= 1 else ()
        )
    pool = list(_PYTHAGOREAN)
    if format_tier >= 1:
        pool.extend(r for r in _COMPOUND if r.family == "pythagorean")
    if format_tier >= 2:
        pool.extend(r for r in _PRODUCT)
    return tuple(pool)


def _max_steps_for_d(format_tier: int, *, min_steps: int, max_steps: int) -> int:
    cap = max(min_steps, max_steps)
    if format_tier <= 0:
        return min(1, cap)
    if format_tier == 1:
        return min(2, cap)
    return cap


def _scale_expr(expr: str, coeff: int) -> tuple[str, str]:
    if coeff == 1:
        return expr, expr.replace(r"\theta", "theta").replace("\\", "")
    wrapped = rf"{coeff}\left({expr}\right)"
    text = f"{coeff}({expr.replace(r'\\', '').replace(' ', '')})"
    return wrapped, text


def _package_prompt(mode: Mode, expr: str, *, rhs: str | None = None) -> tuple[str, str]:
    plain = (
        expr.replace(r"\sin", "sin")
        .replace(r"\cos", "cos")
        .replace(r"\tan", "tan")
        .replace(r"\cot", "cot")
        .replace(r"\sec", "sec")
        .replace(r"\csc", "csc")
        .replace(r"\theta", "θ")
        .replace(r"\frac", "frac")
        .replace("\\", "")
    )
    if mode == "verify" and rhs is not None:
        return (
            rf"\text{{Verify: }} {expr} = {rhs}",
            f"Verify: {plain} = {rhs.replace(chr(92), '')}",
        )
    if mode == "rewrite":
        return (
            rf"\text{{Rewrite using a fundamental identity: }} {expr} = {rhs}",
            f"Rewrite: {plain} = {rhs}",
        )
    return rf"\text{{Simplify: }} {expr}", f"Simplify: {plain}"


def _select_form(ctx: PrimitiveContext, leaf_id: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    if not str(leaf_id or "").startswith("pc_"):
        return None, {}
    from question_engine.frameworks.primitives.openstax_precalc import select_pc_form

    form, meta = select_pc_form(
        CATALOG_NAME,
        d=float(getattr(ctx, "topic_d", 0.0) or 0.0),
        rng=ctx.rng,
        leaf_id=leaf_id,
    )
    return form, meta


def sample_trig_rewrite_item(
    ctx: PrimitiveContext,
    *,
    leaf_id: str | None = None,
) -> TrigRewriteResult:
    """Generate one TrigRewrite item (form → rule pool → package)."""
    settings = dict(getattr(ctx, "settings", None) or {})
    leaf = leaf_id or str(getattr(ctx, "leaf_id", "") or "")
    d = float(getattr(ctx, "topic_d", 0.0) or settings.get("difficulty") or 0.0)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier

    form, form_meta = _select_form(ctx, leaf)
    form_id = str(form.get("form_id") or "") if form else None
    constraints = dict((form or {}).get("constraints") or {})
    family = str(constraints.get("family") or "pythagorean")
    fk = knobs_from_form_id(form_id or "")
    min_steps = int(fk.get("min_steps") or 1)
    max_steps = int(fk.get("max_steps") or 1)
    max_steps = _max_steps_for_d(ft, min_steps=min_steps, max_steps=max_steps)

    pool = _rules_for_family(family, format_tier=ft)
    eligible = [r for r in pool if r.steps <= max_steps]
    if not eligible:
        eligible = list(pool) or list(_PYTHAGOREAN)
    rule = ctx.rng.choice(eligible)

    coeff = 1
    if nt >= 2 and family != "verify" and ctx.rng.random() < 0.35:
        coeff = ctx.rng.choice([2, 3])

    prompt_expr, prompt_plain = _scale_expr(rule.prompt, coeff)
    answer_expr, answer_plain = _scale_expr(rule.answer, coeff)

    mode: Mode = "simplify"
    if family == "verify" or (form_id == "verify_fundamental" and d >= 8.0):
        mode = "verify"
    elif ctx.rng.random() < 0.12 and ft == 0 and family != "verify":
        mode = "rewrite"

    if mode == "rewrite":
        pl, pt = _package_prompt("rewrite", answer_expr, rhs=prompt_expr)
        ans_l, ans_t = prompt_expr, prompt_plain
    elif mode == "verify":
        pl, pt = _package_prompt("verify", rule.prompt, rhs=rule.answer)
        ans_l, ans_t = rule.answer, answer_plain
        if coeff != 1:
            ans_l, ans_t = _scale_expr(rule.answer, coeff)[0], _scale_expr(rule.answer, coeff)[1]
    else:
        pl, pt = _package_prompt("simplify", prompt_expr)
        ans_l, ans_t = answer_expr, answer_plain

    meta: dict[str, Any] = {
        "skeleton_pattern": "TrigRewrite",
        "primitive_engine": "trig_skeleton",
        "mode": mode,
        "family": rule.family,
        "n_steps": rule.steps,
        "rule_id": rule.rule_id,
        "effective_d": d,
        "numeric_tier": nt,
        "format_tier": ft,
        "coeff": coeff,
        "function_classes": ["trig", "algebraic"],
        "methods_used": ["trig_identity", rule.family],
        **form_meta,
    }
    if form_id:
        meta.setdefault("form_id", form_id)

    return TrigRewriteResult(
        prompt_latex=pl,
        prompt_text=pt,
        answer_latex=ans_l,
        answer_text=ans_t,
        mode=mode,
        family=rule.family,
        n_steps=rule.steps,
        rule_id=rule.rule_id,
        form_id=form_id,
        effective_d=d,
        metadata=meta,
    )


# ---------------------------------------------------------------------------
# TrigSumDiff — §7.2 expand (D=0 sin/cos; tan + exact-eval unlock)
# ---------------------------------------------------------------------------

_SUM_DIFF_EXPAND: tuple[TrigRule, ...] = (
    TrigRule(
        r"\sin(\alpha+\beta)",
        r"\sin\alpha\cos\beta+\cos\alpha\sin\beta",
        "sum_difference",
        "sin_plus",
    ),
    TrigRule(
        r"\sin(\alpha-\beta)",
        r"\sin\alpha\cos\beta-\cos\alpha\sin\beta",
        "sum_difference",
        "sin_minus",
    ),
    TrigRule(
        r"\cos(\alpha+\beta)",
        r"\cos\alpha\cos\beta-\sin\alpha\sin\beta",
        "sum_difference",
        "cos_plus",
    ),
    TrigRule(
        r"\cos(\alpha-\beta)",
        r"\cos\alpha\cos\beta+\sin\alpha\sin\beta",
        "sum_difference",
        "cos_minus",
    ),
)

_SUM_DIFF_TAN: tuple[TrigRule, ...] = (
    TrigRule(
        r"\tan(\alpha+\beta)",
        r"\frac{\tan\alpha+\tan\beta}{1-\tan\alpha\tan\beta}",
        "sum_difference",
        "tan_plus",
    ),
    TrigRule(
        r"\tan(\alpha-\beta)",
        r"\frac{\tan\alpha-\tan\beta}{1+\tan\alpha\tan\beta}",
        "sum_difference",
        "tan_minus",
    ),
)

# OpenStax §7.2 exact-value shapes (format unlock).
_SUM_DIFF_EXACT: tuple[TrigRule, ...] = (
    TrigRule(
        r"\cos\left(\frac{\pi}{3}-\frac{\pi}{4}\right)",
        r"\frac{\sqrt{6}+\sqrt{2}}{4}",
        "sum_difference",
        "cos_pi3_minus_pi4",
        steps=2,
    ),
    TrigRule(
        r"\cos 75^\circ",
        r"\frac{\sqrt{6}-\sqrt{2}}{4}",
        "sum_difference",
        "cos_75",
        steps=2,
    ),
    TrigRule(
        r"\sin\left(45^\circ+30^\circ\right)",
        r"\frac{\sqrt{6}+\sqrt{2}}{4}",
        "sum_difference",
        "sin_45_plus_30",
        steps=2,
    ),
    TrigRule(
        r"\sin 15^\circ",
        r"\frac{\sqrt{6}-\sqrt{2}}{4}",
        "sum_difference",
        "sin_15",
        steps=2,
    ),
)


def _select_form_catalog(
    ctx: PrimitiveContext,
    leaf_id: str,
    catalog: str,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    if not str(leaf_id or "").startswith("pc_"):
        return None, {}
    from question_engine.frameworks.primitives.openstax_precalc import select_pc_form

    form, meta = select_pc_form(
        catalog,
        d=float(getattr(ctx, "topic_d", 0.0) or 0.0),
        rng=ctx.rng,
        leaf_id=leaf_id,
    )
    return form, meta


def _plain_trig(expr: str) -> str:
    return (
        expr.replace(r"\sin", "sin")
        .replace(r"\cos", "cos")
        .replace(r"\tan", "tan")
        .replace(r"\cot", "cot")
        .replace(r"\sec", "sec")
        .replace(r"\csc", "csc")
        .replace(r"\theta", "θ")
        .replace(r"\alpha", "α")
        .replace(r"\beta", "β")
        .replace(r"\pi", "π")
        .replace(r"\frac", "frac")
        .replace(r"\left", "")
        .replace(r"\right", "")
        .replace(r"\sqrt", "sqrt")
        .replace("\\", "")
    )


def _pack_result(
    *,
    pattern: str,
    prompt_latex: str,
    prompt_text: str,
    answer_latex: str,
    answer_text: str,
    mode: Mode,
    family: str,
    n_steps: int,
    rule_id: str,
    form_id: str | None,
    effective_d: float,
    meta: dict[str, Any],
) -> TrigRewriteResult:
    meta = {
        "skeleton_pattern": pattern,
        "primitive_engine": "trig_skeleton",
        "mode": mode,
        "family": family,
        "n_steps": n_steps,
        "rule_id": rule_id,
        "effective_d": effective_d,
        "function_classes": ["trig", "algebraic"],
        **meta,
    }
    if form_id:
        meta.setdefault("form_id", form_id)
    return TrigRewriteResult(
        prompt_latex=prompt_latex,
        prompt_text=prompt_text,
        answer_latex=answer_latex,
        answer_text=answer_text,
        mode=mode,
        family=family,
        n_steps=n_steps,
        rule_id=rule_id,
        form_id=form_id,
        effective_d=effective_d,
        metadata=meta,
    )


def sample_trig_sum_diff_item(
    ctx: PrimitiveContext,
    *,
    leaf_id: str | None = None,
) -> TrigRewriteResult:
    """§7.2 sum/difference — Expand at D=0; tan + exact eval at higher D."""
    settings = dict(getattr(ctx, "settings", None) or {})
    leaf = leaf_id or str(getattr(ctx, "leaf_id", "") or "")
    d = float(getattr(ctx, "topic_d", 0.0) or settings.get("difficulty") or 0.0)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier

    form, form_meta = _select_form_catalog(ctx, leaf, CATALOG_NAME)
    form_id = str(form.get("form_id") or "") if form else "sum_difference_expand"

    pool: list[TrigRule] = list(_SUM_DIFF_EXPAND)
    # Tan unlocks with numeric hardness (matches old allow_tan around D≥4).
    if nt >= 1 or d >= 4.0:
        pool.extend(_SUM_DIFF_TAN)
    # Exact-eval format unlock (OpenStax §7.2 Examples 1–3).
    if ft >= 1 or d >= 10.0:
        pool.extend(_SUM_DIFF_EXACT)

    rule = ctx.rng.choice(pool)
    if rule.rule_id in {r.rule_id for r in _SUM_DIFF_EXACT}:
        pl = rf"\text{{Find the exact value of }}{rule.prompt}."
        pt = f"Find the exact value of {_plain_trig(rule.prompt)}."
        mode: Mode = "simplify"
        methods = ["sum_difference", "exact_eval"]
    else:
        pl = rf"\text{{Expand }}{rule.prompt}."
        pt = f"Expand {_plain_trig(rule.prompt)}."
        mode = "rewrite"
        methods = ["sum_difference"]

    return _pack_result(
        pattern="TrigSumDiff",
        prompt_latex=pl,
        prompt_text=pt,
        answer_latex=rule.answer,
        answer_text=_plain_trig(rule.answer),
        mode=mode,
        family="sum_difference",
        n_steps=rule.steps,
        rule_id=rule.rule_id,
        form_id=form_id,
        effective_d=d,
        meta={
            "numeric_tier": nt,
            "format_tier": ft,
            "methods_used": methods,
            **form_meta,
        },
    )


# ---------------------------------------------------------------------------
# TrigDoubleAngle — §7.3 double-angle rewrite (half-angle deferred)
# ---------------------------------------------------------------------------

_DOUBLE_BASIC: tuple[TrigRule, ...] = (
    TrigRule(r"\sin(2\theta)", r"2\sin\theta\cos\theta", "double_angle", "sin_2"),
    TrigRule(
        r"\cos(2\theta)",
        r"\cos^2\theta-\sin^2\theta",
        "double_angle",
        "cos_2_diff",
    ),
)

_DOUBLE_EXTRA: tuple[TrigRule, ...] = (
    TrigRule(
        r"\tan(2\theta)",
        r"\frac{2\tan\theta}{1-\tan^2\theta}",
        "double_angle",
        "tan_2",
    ),
    TrigRule(
        r"\sin\theta\cos\theta",
        r"\frac{1}{2}\sin(2\theta)",
        "double_angle",
        "half_sin_2",
    ),
    TrigRule(
        r"\cos(2\theta)",
        r"2\cos^2\theta-1",
        "double_angle",
        "cos_2_cos",
    ),
    TrigRule(
        r"\cos(2\theta)",
        r"1-2\sin^2\theta",
        "double_angle",
        "cos_2_sin",
    ),
)


def sample_trig_double_angle_item(
    ctx: PrimitiveContext,
    *,
    leaf_id: str | None = None,
) -> TrigRewriteResult:
    """§7.3 double-angle rewrite — D=0 sin/cos(2θ); tan / alt forms unlock."""
    settings = dict(getattr(ctx, "settings", None) or {})
    leaf = leaf_id or str(getattr(ctx, "leaf_id", "") or "")
    d = float(getattr(ctx, "topic_d", 0.0) or settings.get("difficulty") or 0.0)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier

    form, form_meta = _select_form_catalog(ctx, leaf, CATALOG_NAME)
    form_id = str(form.get("form_id") or "") if form else "double_angle"

    pool: list[TrigRule] = list(_DOUBLE_BASIC)
    if nt >= 1 or d >= 4.0:
        pool.append(_DOUBLE_EXTRA[0])  # tan(2θ)
    if ft >= 1 or d >= 10.0:
        pool.extend(_DOUBLE_EXTRA[1:])

    rule = ctx.rng.choice(pool)
    pl = rf"\text{{Rewrite }}{rule.prompt}\text{{ using a double-angle identity.}}"
    pt = f"Rewrite {_plain_trig(rule.prompt)} using a double-angle identity."

    return _pack_result(
        pattern="TrigDoubleAngle",
        prompt_latex=pl,
        prompt_text=pt,
        answer_latex=rule.answer,
        answer_text=_plain_trig(rule.answer),
        mode="rewrite",
        family="double_angle",
        n_steps=rule.steps,
        rule_id=rule.rule_id,
        form_id=form_id,
        effective_d=d,
        meta={
            "numeric_tier": nt,
            "format_tier": ft,
            "methods_used": ["double_angle"],
            **form_meta,
        },
    )


# ---------------------------------------------------------------------------
# TrigProductToSum — §7.4 product→sum (sum→product remains stub)
# ---------------------------------------------------------------------------

_PTS_EASY: tuple[TrigRule, ...] = (
    TrigRule(
        r"\sin A\cos B",
        r"\frac{1}{2}\left[\sin(A+B)+\sin(A-B)\right]",
        "product_to_sum",
        "sin_cos",
    ),
)

_PTS_FULL: tuple[TrigRule, ...] = (
    TrigRule(
        r"\cos A\cos B",
        r"\frac{1}{2}\left[\cos(A+B)+\cos(A-B)\right]",
        "product_to_sum",
        "cos_cos",
    ),
    TrigRule(
        r"\sin A\sin B",
        r"\frac{1}{2}\left[\cos(A-B)-\cos(A+B)\right]",
        "product_to_sum",
        "sin_sin",
    ),
    TrigRule(
        r"\cos A\sin B",
        r"\frac{1}{2}\left[\sin(A+B)-\sin(A-B)\right]",
        "product_to_sum",
        "cos_sin",
    ),
)


def sample_trig_product_to_sum_item(
    ctx: PrimitiveContext,
    *,
    leaf_id: str | None = None,
) -> TrigRewriteResult:
    """§7.4 product→sum — D=0 sin A cos B; fuller product pool at higher D."""
    settings = dict(getattr(ctx, "settings", None) or {})
    leaf = leaf_id or str(getattr(ctx, "leaf_id", "") or "")
    d = float(getattr(ctx, "topic_d", 0.0) or settings.get("difficulty") or 0.0)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier

    form, form_meta = _select_form_catalog(ctx, leaf, CATALOG_NAME)
    form_id = str(form.get("form_id") or "") if form else "product_to_sum"

    pool: list[TrigRule] = list(_PTS_EASY)
    # Old path unlocked fuller pool around D≥12 via allow_product_to_sum.
    if nt >= 2 or d >= 12.0 or ft >= 1:
        pool.extend(_PTS_FULL)

    rule = ctx.rng.choice(pool)
    pl = rf"\text{{Rewrite }}{rule.prompt}\text{{ as a sum.}}"
    pt = f"Rewrite {_plain_trig(rule.prompt)} as a sum."

    return _pack_result(
        pattern="TrigProductToSum",
        prompt_latex=pl,
        prompt_text=pt,
        answer_latex=rule.answer,
        answer_text=_plain_trig(rule.answer),
        mode="rewrite",
        family="product_to_sum",
        n_steps=rule.steps,
        rule_id=rule.rule_id,
        form_id=form_id,
        effective_d=d,
        meta={
            "numeric_tier": nt,
            "format_tier": ft,
            "methods_used": ["product_to_sum"],
            **form_meta,
        },
    )


# ---------------------------------------------------------------------------
# TrigFactorEq — §7.5 factor / quadratic / double-angle equations
# ---------------------------------------------------------------------------

EQ_CATALOG = "precalculus_trig_equations"

_FACTOR_EQ_TEMPLATES: dict[str, tuple[str, str, str, int]] = {
    # key → (prompt, answer, mode, min_format_tier)
    "quadratic_in_trig": (
        r"\text{Solve }2\sin^2\theta-\sin\theta=0\text{ for }0\le\theta<2\pi.",
        r"\theta=0,\frac{\pi}{6},\pi,\frac{5\pi}{6}",
        "quadratic_in_trig",
        0,
    ),
    "quadratic_cos": (
        r"\text{Solve }2\cos^2\theta-1=0\text{ for }0\le\theta<2\pi.",
        r"\theta=\frac{\pi}{4},\frac{3\pi}{4},\frac{5\pi}{4},\frac{7\pi}{4}",
        "quadratic_in_trig",
        0,
    ),
    "factor_fundamental": (
        r"\text{Solve }2\sin\theta\cos\theta=0\text{ for }0\le\theta<2\pi.",
        r"\theta=0,\frac{\pi}{2},\pi,\frac{3\pi}{2}",
        "factor_fundamental",
        0,
    ),
    "double_angle_equation": (
        r"\text{Solve }\cos(2\theta)=0\text{ for }0\le\theta<\pi.",
        r"\theta=\frac{\pi}{4},\frac{3\pi}{4}",
        "double_angle_equation",
        0,
    ),
    "double_angle_sin": (
        r"\text{Solve }\sin(2\theta)=0\text{ for }0\le\theta<\pi.",
        r"\theta=0,\frac{\pi}{2}",
        "double_angle_equation",
        1,
    ),
}


def sample_trig_factor_eq_item(
    ctx: PrimitiveContext,
    *,
    leaf_id: str | None = None,
) -> TrigRewriteResult:
    """§7.5 factoring / multiple-angle equations — D=0 quadratic; unlocks later."""
    settings = dict(getattr(ctx, "settings", None) or {})
    leaf = leaf_id or str(getattr(ctx, "leaf_id", "") or "")
    d = float(getattr(ctx, "topic_d", 0.0) or settings.get("difficulty") or 0.0)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier

    form, form_meta = _select_form_catalog(ctx, leaf, EQ_CATALOG)
    form_id = str(form.get("form_id") or "") if form else None
    constraints = dict((form or {}).get("constraints") or {})
    choice = str(constraints.get("choice") or "")

    # Prefer form_id over ambiguous constraint ``choice`` (quadratic also uses choice=factor).
    if form_id == "double_angle_equation" or choice == "cos2":
        keys = ["double_angle_equation"]
        if ft >= 1:
            keys.append("double_angle_sin")
    elif form_id == "factor_fundamental" or choice == "sin2":
        keys = ["factor_fundamental"]
    elif form_id == "quadratic_in_trig":
        keys = ["quadratic_in_trig"]
        if nt >= 1 or d >= 6.0:
            keys.append("quadratic_cos")
    else:
        # D-gated default pool when form is ambiguous / missing.
        keys = ["quadratic_in_trig"]
        if d >= 6.0:
            keys.append("quadratic_cos")
        if d >= 8.0:
            keys.extend(["factor_fundamental", "double_angle_equation"])
        if ft >= 1 and d >= 8.0:
            keys.append("double_angle_sin")

    eligible = [
        k
        for k in keys
        if k in _FACTOR_EQ_TEMPLATES and _FACTOR_EQ_TEMPLATES[k][3] <= ft
    ]
    if not eligible:
        eligible = ["quadratic_in_trig"]
    key = ctx.rng.choice(eligible)
    prompt, answer, mode, _min_ft = _FACTOR_EQ_TEMPLATES[key]
    pt = _plain_trig(prompt.replace(r"\text{", "").replace("}", ""))

    return _pack_result(
        pattern="TrigFactorEq",
        prompt_latex=prompt,
        prompt_text=pt,
        answer_latex=answer,
        answer_text=_plain_trig(answer),
        mode="simplify",
        family=mode,  # type: ignore[arg-type]
        n_steps=1 if key.startswith("quadratic") else 2,
        rule_id=key,
        form_id=form_id or key,
        effective_d=d,
        meta={
            "numeric_tier": nt,
            "format_tier": ft,
            "mode": mode,
            "methods_used": ["trig_equation", mode],
            **form_meta,
        },
    )
