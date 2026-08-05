"""OpenStax form → skeleton pattern language + Diff(F(u)) hole fill.

Pipeline
--------
1. OpenStax ``form_id`` picks a **skeleton pattern** at varying precision
   (``Diff(F(u))`` vs ``Diff(Prod(F,G)(u))`` vs ``Diff(Pow(H,n))``, …).
2. Conceptual richness fills **open holes only** (shared inner ``u``, atomFNs).
3. Emit ``ExprAST`` for differentiate / render. Spec identity extras run later.

This module does **not** invent a different top-level structure than the pattern.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Mapping, Sequence

from question_engine.frameworks.primitives.poly_expression import (
    Add,
    Const,
    ExprAST,
    Fn,
    Mul,
    Pow,
    Var,
    differentiate,
    render_latex,
)

# ---------------------------------------------------------------------------
# Pattern language
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SkeletonPattern:
    """Curriculum-facing structure for one OpenStax form.

    ``kind`` values:
      - ``diff_f_of_u``     — Diff(F(u)); F filled under richness
      - ``diff_prod_fg_u``  — Diff(Prod(F,G)(u)); product fixed
      - ``diff_sum_fg_u``   — Diff(Sum(F,G)(u))
      - ``diff_quot_fg_u``  — Diff(Quot(F,G)(u)); quotient as F·G^{-1}
      - ``diff_pow_h_n``    — Diff(Pow(H, n)); power fixed
      - ``diff_apply_fn_u`` — Diff(Apply(fn, u)); optional locked outer fn
    """

    kind: str
    atom_fns: tuple[str, ...] = ("poly",)
    atom_fns_g: tuple[str, ...] | None = None
    locked_fn: str | None = None
    prefer_roots: bool = False
    prefer_negative_power: bool = False
    force_affine_or_nest: bool = False
    pattern_label: str = ""

    def label(self) -> str:
        if self.pattern_label:
            return self.pattern_label
        return {
            "diff_f_of_u": "Diff(F(u))",
            "diff_prod_fg_u": "Diff(Prod(F,G)(u))",
            "diff_sum_fg_u": "Diff(Sum(F,G)(u))",
            "diff_quot_fg_u": "Diff(Quot(F,G)(u))",
            "diff_pow_h_n": "Diff(Pow(H,n))",
            "diff_apply_fn_u": "Diff(Apply(fn,u))",
        }.get(self.kind, self.kind)


@dataclass(frozen=True)
class Richness:
    """Conceptual knobs that only elaborate open holes."""

    conceptual_d: float = 0.0
    nest_budget: int = 0
    allow_affine_u: bool = True
    allow_poly_u: bool = False
    coef_abs_max: int = 5
    power_max: int = 4


def richness_from_conceptual(
    d: float,
    *,
    allow_roots: bool = False,
) -> Richness:
    d = max(0.0, float(d))
    nest = 0
    if d >= 12:
        nest = 1
    if d >= 20:
        nest = 2
    return Richness(
        conceptual_d=d,
        nest_budget=nest,
        allow_affine_u=True,
        allow_poly_u=d >= 6 or allow_roots,
        coef_abs_max=3 if d < 4 else (5 if d < 12 else 8),
        power_max=2 if d < 4 else (3 if d < 10 else (5 if d < 18 else 7)),
    )


# OpenStax form_id → pattern (stubs like implicit_basic intentionally omitted).
FORM_PATTERNS: dict[str, SkeletonPattern] = {
    "power_poly": SkeletonPattern(
        kind="diff_pow_h_n", atom_fns=("poly",), pattern_label="Diff(Pow(H,n))"
    ),
    "power_root": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        prefer_roots=True,
        pattern_label="Diff(Pow(H,n)) roots",
    ),
    "power_negative": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        prefer_negative_power=True,
        pattern_label="Diff(Pow(H,n)) neg",
    ),
    "product_two_poly": SkeletonPattern(
        kind="diff_prod_fg_u",
        atom_fns=("poly",),
        pattern_label="Diff(Prod(F,G)(u))",
    ),
    "product_poly_trig": SkeletonPattern(
        kind="diff_prod_fg_u",
        atom_fns=("poly",),
        atom_fns_g=("sin", "cos"),
        pattern_label="Diff(Prod(F,G)(u)) poly×trig",
    ),
    "product_poly_exp": SkeletonPattern(
        kind="diff_prod_fg_u",
        atom_fns=("poly",),
        atom_fns_g=("exp",),
        pattern_label="Diff(Prod(F,G)(u)) poly×exp",
    ),
    "quotient_poly": SkeletonPattern(
        kind="diff_quot_fg_u",
        atom_fns=("poly",),
        pattern_label="Diff(Quot(F,G)(u))",
    ),
    "quotient_trig_poly": SkeletonPattern(
        kind="diff_quot_fg_u",
        atom_fns=("sin", "cos", "tan"),
        atom_fns_g=("poly",),
        pattern_label="Diff(Quot(F,G)(u)) trig/poly",
    ),
    "quotient_exp_poly": SkeletonPattern(
        kind="diff_quot_fg_u",
        atom_fns=("exp",),
        atom_fns_g=("poly",),
        pattern_label="Diff(Quot(F,G)(u)) exp/poly",
    ),
    "quotient_log_poly": SkeletonPattern(
        kind="diff_quot_fg_u",
        atom_fns=("ln",),
        atom_fns_g=("poly", "sin", "cos"),
        pattern_label="Diff(Quot(F,G)(u)) log/…",
    ),
    "quotient_mixed_special": SkeletonPattern(
        kind="diff_quot_fg_u",
        atom_fns=("sin", "cos", "exp", "ln"),
        atom_fns_g=("sin", "cos", "exp", "ln", "poly"),
        pattern_label="Diff(Quot(F,G)(u)) mixed",
    ),
    "chain_power_linear": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        force_affine_or_nest=True,
        pattern_label="Diff(Pow(H,n)) chain-linear",
    ),
    "chain_trig_poly": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("sin", "cos"),
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(fn,u)) chain",
    ),
    "chain_nested": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("sin", "cos", "exp", "ln"),
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(fn,u)) nested",
    ),
    "trig_basic": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("sin", "cos", "tan"),
        pattern_label="Diff(Apply(fn,u))",
    ),
    "trig_product_chain": SkeletonPattern(
        kind="diff_prod_fg_u",
        atom_fns=("sin", "cos"),
        pattern_label="Diff(Prod(F,G)(u)) trig×trig",
    ),
    "ln_basic": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("ln",),
        locked_fn="ln",
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(ln,u))",
    ),
    "exp_basic": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("exp",),
        locked_fn="exp",
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(exp,u))",
    ),
    "ln_exp_product": SkeletonPattern(
        kind="diff_prod_fg_u",
        atom_fns=("ln",),
        atom_fns_g=("exp",),
        pattern_label="Diff(Prod(F,G)(u)) ln×exp",
    ),
    "invtrig_arcsin": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("arcsin",),
        locked_fn="arcsin",
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(arcsin,u))",
    ),
    "invtrig_arctan": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("arctan",),
        locked_fn="arctan",
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(arctan,u))",
    ),
    "invtrig_chained": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("arcsin", "arctan"),
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(invtrig,u)) chain",
    ),
    "higher_order_2": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        pattern_label="Diff(Pow(H,n)) order2",
    ),
    "higher_order_3": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        pattern_label="Diff(Pow(H,n)) order3",
    ),
    "general_mixed": SkeletonPattern(
        kind="diff_f_of_u",
        atom_fns=("poly", "sin", "cos", "exp", "ln"),
        pattern_label="Diff(F(u))",
    ),
}


def has_form_pattern(form_id: str | None) -> bool:
    return bool(form_id) and str(form_id) in FORM_PATTERNS


def pattern_for_form(form_id: str) -> SkeletonPattern | None:
    return FORM_PATTERNS.get(str(form_id))


def _coef(rng: random.Random, hi: int, *, nonzero: bool = True) -> int:
    hi = max(1, int(hi))
    choices = (
        [i for i in range(-hi, hi + 1) if i != 0]
        if nonzero
        else list(range(-hi, hi + 1))
    )
    if not choices:
        return 1
    return int(rng.choice(choices))


def _sample_inner(
    var: str,
    richness: Richness,
    rng: random.Random,
    *,
    nest_left: int,
    atom_pool: Sequence[str],
) -> ExprAST:
    v = Var(var)
    if nest_left > 0 and atom_pool and rng.random() < 0.45:
        fn = rng.choice([a for a in atom_pool if a != "poly"] or list(atom_pool))
        if fn != "poly":
            inner = _sample_inner(
                var, richness, rng, nest_left=nest_left - 1, atom_pool=atom_pool
            )
            return Fn(fn, inner)

    if richness.allow_affine_u and rng.random() < (
        0.7 if richness.conceptual_d >= 2 else 0.35
    ):
        a = _coef(rng, min(4, richness.coef_abs_max))
        b = _coef(rng, min(4, richness.coef_abs_max), nonzero=False)
        ax: ExprAST = Mul((Const(Fraction(a)), v)) if a != 1 else v
        if b == 0:
            return ax
        return Add((ax, Const(Fraction(b))))

    if richness.allow_poly_u and rng.random() < 0.4:
        deg = int(rng.randint(1, min(3, richness.power_max)))
        terms: list[ExprAST] = []
        for k in range(deg, -1, -1):
            if k == 0:
                c = _coef(rng, richness.coef_abs_max, nonzero=False)
                if c:
                    terms.append(Const(Fraction(c)))
                continue
            if k < deg and rng.random() < 0.35:
                continue
            c = _coef(rng, richness.coef_abs_max)
            pk: ExprAST = Pow(v, Fraction(k)) if k != 1 else v
            terms.append(Mul((Const(Fraction(c)), pk)) if c != 1 else pk)
        if not terms:
            return v
        if len(terms) == 1:
            return terms[0]
        return Add(tuple(terms))

    return v


def _poly_of_u(u: ExprAST, richness: Richness, rng: random.Random) -> ExprAST:
    deg = int(rng.randint(1, max(1, min(3, richness.power_max))))
    if isinstance(u, Var) and rng.random() < 0.55:
        c = _coef(rng, richness.coef_abs_max)
        body: ExprAST = Pow(u, Fraction(deg)) if deg != 1 else u
        return Mul((Const(Fraction(c)), body)) if c != 1 else body
    if rng.random() < 0.5:
        c = _coef(rng, richness.coef_abs_max)
        body = Pow(u, Fraction(deg)) if deg != 1 else u
        return Mul((Const(Fraction(c)), body)) if c != 1 else body
    c = _coef(rng, richness.coef_abs_max)
    d = _coef(rng, min(3, richness.coef_abs_max), nonzero=False)
    cu = Mul((Const(Fraction(c)), u)) if c != 1 else u
    if d == 0:
        return cu
    return Add((cu, Const(Fraction(d))))


def _apply_fn_of_u(fn: str, u: ExprAST) -> ExprAST:
    if fn == "poly":
        raise ValueError("poly is not an Apply fn")
    return Fn(fn, u)


def _sample_f_hole(
    atom_choices: Sequence[str],
    u: ExprAST,
    richness: Richness,
    rng: random.Random,
    *,
    prefer_non_poly: bool = False,
) -> ExprAST:
    pool = list(atom_choices) or ["poly"]
    if prefer_non_poly:
        non = [a for a in pool if a != "poly"]
        if non:
            pool = non
    fn = rng.choice(pool)
    if fn == "poly":
        return _poly_of_u(u, richness, rng)
    return _apply_fn_of_u(fn, u)


def _filter_atom_fns(
    atoms: Sequence[str],
    allows: Mapping[str, bool],
) -> list[str]:
    out: list[str] = []
    for a in atoms:
        if a == "poly":
            out.append(a)
        elif a in ("sin", "cos", "tan") and allows.get("allow_trig", True):
            out.append(a)
        elif a == "exp" and allows.get("allow_exp", True):
            out.append(a)
        elif a == "ln" and allows.get("allow_log", True):
            out.append(a)
        elif a in ("arcsin", "arctan") and allows.get("allow_invtrig", True):
            out.append(a)
    return out or ["poly"]


def _build_pow(
    pattern: SkeletonPattern,
    u: ExprAST,
    richness: Richness,
    rng: random.Random,
) -> ExprAST:
    if pattern.prefer_roots:
        num = int(rng.choice([1, 1, 3, 5]))
        den = int(rng.choice([2, 2, 3]))
        if num == den:
            num, den = 1, 2
        return Pow(u, Fraction(num, den))
    if pattern.prefer_negative_power:
        n = -int(rng.randint(1, min(4, richness.power_max)))
        return Pow(u, Fraction(n))
    n = int(rng.randint(2, max(2, min(richness.power_max, 5))))
    if "chain" in pattern.pattern_label or not isinstance(u, Var):
        return Pow(u, Fraction(n))
    if rng.random() < 0.55:
        return _poly_of_u(u, richness, rng)
    c = _coef(rng, richness.coef_abs_max)
    body: ExprAST = Pow(u, Fraction(n))
    return Mul((Const(Fraction(c)), body)) if c != 1 else body


def sample_expr_from_pattern(
    pattern: SkeletonPattern,
    *,
    richness: Richness,
    allows: Mapping[str, bool] | None = None,
    rng: random.Random | None = None,
    var: str = "x",
) -> tuple[ExprAST, dict[str, Any]]:
    """Fill holes in ``pattern``; return ExprAST + inventory meta."""
    rng = rng or random.Random()
    allows = dict(allows or {})
    for key, default in (
        ("allow_trig", True),
        ("allow_exp", True),
        ("allow_log", True),
        ("allow_roots", True),
        ("allow_invtrig", True),
    ):
        allows.setdefault(key, default)

    atoms = _filter_atom_fns(pattern.atom_fns, allows)
    atoms_g = _filter_atom_fns(pattern.atom_fns_g or pattern.atom_fns, allows)
    nest = int(richness.nest_budget)
    rich = richness
    if pattern.force_affine_or_nest or (
        pattern.kind in ("diff_apply_fn_u", "diff_pow_h_n")
        and "chain" in pattern.label()
    ):
        nest_use = nest
        if pattern.force_affine_or_nest and "nested" in pattern.label():
            nest_use = max(nest, 1)
        rich = Richness(
            conceptual_d=richness.conceptual_d,
            nest_budget=nest_use,
            allow_affine_u=True,
            allow_poly_u=True,
            coef_abs_max=richness.coef_abs_max,
            power_max=richness.power_max,
        )
        nest = nest_use

    pool_u = atoms + [a for a in atoms_g if a not in atoms]
    u = _sample_inner(var, rich, rng, nest_left=nest, atom_pool=pool_u)
    if pattern.force_affine_or_nest and isinstance(u, Var):
        a = _coef(rng, min(4, rich.coef_abs_max))
        b = _coef(rng, min(4, rich.coef_abs_max), nonzero=False)
        ax: ExprAST = Mul((Const(Fraction(a)), Var(var))) if a != 1 else Var(var)
        u = ax if b == 0 else Add((ax, Const(Fraction(b))))

    meta: dict[str, Any] = {
        "skeleton_pattern": pattern.label(),
        "skeleton_kind": pattern.kind,
        "shared_inner": True,
    }

    if pattern.kind == "diff_prod_fg_u":
        f = _sample_f_hole(atoms, u, rich, rng, prefer_non_poly=("poly" not in atoms))
        g = _sample_f_hole(
            atoms_g, u, rich, rng, prefer_non_poly=("poly" not in atoms_g)
        )
        for _ in range(4):
            if render_latex(f) != render_latex(g):
                break
            g = _sample_f_hole(atoms_g, u, rich, rng)
        expr: ExprAST = Mul((f, g))
        meta["productions"] = ["Prod", "F", "G", "u"]
    elif pattern.kind == "diff_quot_fg_u":
        f = _sample_f_hole(atoms, u, rich, rng, prefer_non_poly=("poly" not in atoms))
        g = _sample_f_hole(atoms_g, u, rich, rng)
        for _ in range(6):
            if render_latex(g) not in {"0", render_latex(f)} and not (
                isinstance(g, Const) and g.value == 0
            ):
                break
            g = _sample_f_hole(atoms_g, u, rich, rng)
        expr = Mul((f, Pow(g, -1)))
        meta["productions"] = ["Quot", "F", "G", "u"]
        meta["methods_hint"] = ["quotient"]
    elif pattern.kind == "diff_sum_fg_u":
        f = _sample_f_hole(atoms, u, rich, rng)
        g = _sample_f_hole(atoms_g, u, rich, rng)
        expr = Add((f, g))
        meta["productions"] = ["Sum", "F", "G", "u"]
    elif pattern.kind == "diff_pow_h_n":
        expr = _build_pow(pattern, u, rich, rng)
        meta["productions"] = ["Pow", "H", "n", "u"]
    elif pattern.kind == "diff_apply_fn_u":
        fn = pattern.locked_fn
        if fn is None:
            pool = [a for a in atoms if a != "poly"] or atoms
            fn = rng.choice(pool)
            if fn == "poly":
                expr = _poly_of_u(u, rich, rng)
                meta["productions"] = ["Poly", "u"]
                return expr, meta
        expr = _apply_fn_of_u(fn, u)
        meta["productions"] = ["Apply", fn, "u"]
    elif pattern.kind == "diff_f_of_u":
        expr = _sample_f_hole(atoms, u, rich, rng)
        meta["productions"] = ["F", "u"]
    else:
        raise ValueError(f"unknown skeleton kind: {pattern.kind}")

    return expr, meta


def sample_from_form(
    form_id: str,
    *,
    conceptual_d: float = 0.0,
    allows: Mapping[str, bool] | None = None,
    rng: random.Random | None = None,
    var: str = "x",
    derivative_order: int = 1,
) -> tuple[ExprAST, ExprAST, str, str, dict[str, Any]]:
    """OpenStax form_id → pattern → filled ExprAST + derivative latex.

    Returns ``(expr, d_expr, body_latex, deriv_latex, inventory)``.
    """
    pattern = pattern_for_form(form_id)
    if pattern is None:
        raise KeyError(f"no skeleton pattern for form_id={form_id!r}")
    rng = rng or random.Random()
    allows = dict(allows or {})
    rich = richness_from_conceptual(
        conceptual_d,
        allow_roots=bool(allows.get("allow_roots")) or pattern.prefer_roots,
    )
    expr, meta = sample_expr_from_pattern(
        pattern, richness=rich, allows=allows, rng=rng, var=var
    )
    order = max(1, int(derivative_order))
    d_expr = expr
    for _ in range(order):
        d_expr = differentiate(d_expr, var)
    body = render_latex(expr, paren_style="minimal")
    deriv = render_latex(d_expr, paren_style="minimal")
    from question_engine.frameworks.primitives import poly_expression as poly_expr

    methods_hint = set(meta.pop("methods_hint", []) or [])
    inv: dict[str, Any] = {
        "core_form_id": form_id,
        "skeleton_source": "expr_skeleton",
        "function_classes": sorted(poly_expr.function_classes_of(expr)),
        "methods_used": sorted(set(poly_expr.methods_used_of(expr)) | methods_hint),
        "chain_depth": int(poly_expr.chain_depth_of(expr)),
        "derivative_order": order,
        **meta,
    }
    return expr, d_expr, body, deriv, inv
