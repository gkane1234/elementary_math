"""OpenStax form → skeleton pattern language + Diff(F(u)) hole fill.

Pipeline
--------
1. OpenStax ``form_id`` picks a **skeleton pattern** at varying precision
   (``Diff(F(u))`` vs ``Diff(Prod(F,G)(u))`` vs ``Diff(Prod(F,G))``, …).
2. Conceptual richness fills **open holes only** (inners, atomFNs).
3. Emit ``ExprAST`` for differentiate / render. Spec identity extras run later.

This module does **not** invent a different top-level structure than the pattern.

Conceptual difficulty scale (skeleton richness)
-----------------------------------------------
``conceptual_difficulty`` / ``richness_from_conceptual`` elaborates holes only:

| Band   | C (approx) | Inner ``u`` / factors      | Hole F/G / powers              | Nest / structure              |
|--------|------------|----------------------------|--------------------------------|-------------------------------|
| Low    | 0–4        | Var / Affine; simple fn×fn | Apply / simple poly of x       | nest 0; low |n|               |
| Mid    | 4–12       | Affine → **Poly**          | denser poly; wider |n|         | nest 0 (poly is the unlock)   |
| High   | 12–20      | Messier poly / Apply nest  | higher |n|; denser coefs       | nest 1 for Apply/chain forms  |
| Elite  | 20+        | richest poly / deeper Apply| richest |n| / coefs            | nest 2 for Apply/chain forms  |

**Power-rule forms** (``power_poly`` / roots / negative / higher-order): nest
cap is **0** — hardness is a harder inner poly and/or a single larger |n|,
never compose-pow towers like ``((u)^a)^b``.

**Product / quotient**: top-level factors are **fn×fn** (Apply/fn-like), never
a baked-in raw-poly × trig shape. Poly may appear *inside* an argument.
``allow_*`` + catalog ``d_min`` gate specials. Mid/high **product+chain**
forms (``product_one_chain``, ``product_chain_powers``,
``product_trig_exp_chain``) keep the product skeleton and compose **a factor**
(OpenStax §3.6 Example 3.54 ``(ax+b)^n(cx+d)^m``, §3.9 ``sin x·e^{g}``) —
not a 3-deep ``f(g(h(x)))`` dump onto the chain leaf.

**Power + chain**: ``allow_chain`` / ``require_chain`` (default off on power
leaf) gate outer powers of affine/poly. Without chain: ``x^n``, ``k x^n``,
or an expanded poly sum — not ``(ax+b)^n``.

**General / mixed**: low C = one conceptual skill (power *or* product *or*
chain *or* a single Apply). High C unlocks multi-method entanglement.

Pattern choice (shared vs independent Prod, Quot, Pow, Apply) is owned by the
OpenStax form map, not by C.
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
      - ``diff_prod_fg_u``  — Diff(Prod(F,G)(u)); product of two F-of-**shared**-u
      - ``diff_prod_fg``    — Diff(Prod(F,G)); product with **independent** inners
      - ``diff_sum_fg_u``   — Diff(Sum(F,G)(u))
      - ``diff_quot_fg_u``  — Diff(Quot(F,G)(u)); AST as F·G^{-1}, render as F/G
      - ``diff_quot_fg``    — Diff(Quot(F,G)); independent inners
      - ``diff_pow_h_n``    — Diff(Pow(H, n)); power fixed
      - ``diff_apply_fn_u`` — Diff(Apply(fn, u)); optional locked outer fn

    ``forbid_pow_nest``: when True (pure power-rule forms), nest budget is
    capped at 0 — harden via poly degree / |n|, never compose-pow towers.
    """

    kind: str
    atom_fns: tuple[str, ...] = ("poly",)
    atom_fns_g: tuple[str, ...] | None = None
    locked_fn: str | None = None
    prefer_roots: bool = False
    prefer_negative_power: bool = False
    force_affine_or_nest: bool = False
    forbid_pow_nest: bool = False
    expand_from_allows: bool = False
    force_fn_power: bool = False
    require_composed_factor: bool = False
    both_factors_pow: bool = False
    pattern_label: str = ""

    def label(self) -> str:
        if self.pattern_label:
            return self.pattern_label
        return {
            "diff_f_of_u": "Diff(F(u))",
            "diff_prod_fg_u": "Diff(Prod(F,G)(u))",
            "diff_prod_fg": "Diff(Prod(F,G))",
            "diff_sum_fg_u": "Diff(Sum(F,G)(u))",
            "diff_quot_fg_u": "Diff(Quot(F,G)(u))",
            "diff_quot_fg": "Diff(Quot(F,G))",
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
    prefer_poly_u: bool = False
    force_min_nest: int = 0
    allow_form_min_nest: bool = True
    power_min: int = 2
    poly_degree_min: int = 1
    coef_abs_max: int = 5
    power_max: int = 4
    band: str = "low"

    def as_knobs(self) -> dict[str, Any]:
        """Serializable knob snapshot for gallery / inventory debug."""
        return {
            "conceptual_d": self.conceptual_d,
            "band": self.band,
            "nest_budget": self.nest_budget,
            "force_min_nest": self.force_min_nest,
            "allow_form_min_nest": self.allow_form_min_nest,
            "allow_affine_u": self.allow_affine_u,
            "allow_poly_u": self.allow_poly_u,
            "prefer_poly_u": self.prefer_poly_u,
            "power_min": self.power_min,
            "power_max": self.power_max,
            "poly_degree_min": self.poly_degree_min,
            "coef_abs_max": self.coef_abs_max,
        }


def richness_from_conceptual(
    d: float,
    *,
    allow_roots: bool = False,
    derivative_order: int = 1,
) -> Richness:
    """Map conceptual difficulty onto hole-fill richness (not pattern choice).

    See module docstring for the Low / Mid / High / Elite bands.
    Higher C densifies holes: poly unlock → forced nest → deeper nest / exponents.
    ``derivative_order≥2`` caps nest / poly so expanded answers stay tractable.
    """
    d = max(0.0, float(d))
    order = max(1, int(derivative_order))
    if d < 4:
        band, nest, force_nest = "low", 0, 0
        power_min, poly_deg_min = 2, 1
        prefer_poly = False
    elif d < 12:
        band, nest, force_nest = "mid", 0, 0
        power_min = 2 if d < 8 else 3
        poly_deg_min = 1 if d < 8 else 2
        prefer_poly = d >= 6 or allow_roots
    elif d < 20:
        band, nest, force_nest = "high", 1, 1
        power_min, poly_deg_min = 3, 2
        prefer_poly = True
    else:
        band, nest, force_nest = "elite", 2, 2
        power_min, poly_deg_min = 4, 2
        prefer_poly = True
    allow_form_min_nest = True
    # Higher-order: shallow holes only (2nd/3rd derivatives explode with nests).
    if order >= 2:
        nest, force_nest = 0, 0
        prefer_poly = False
        poly_deg_min = 1
        power_min = min(power_min, 2)
        allow_form_min_nest = False
        if order >= 3:
            power_min = 2
    return Richness(
        conceptual_d=d,
        nest_budget=nest,
        allow_affine_u=True,
        allow_poly_u=(d >= 6 or allow_roots or prefer_poly) and order == 1,
        prefer_poly_u=prefer_poly,
        force_min_nest=force_nest,
        allow_form_min_nest=allow_form_min_nest,
        power_min=power_min,
        poly_degree_min=poly_deg_min,
        coef_abs_max=3 if d < 4 else (5 if d < 12 else (8 if d < 20 else 10)),
        power_max=2 if d < 4 else (3 if d < 10 else (5 if d < 18 else 7)),
        band=band,
    )


# OpenStax form_id → pattern (stubs like implicit_basic intentionally omitted).
#
# Product / quotient mapping policy:
#   - Classic OpenStax product examples (poly×poly, poly×trig, poly×exp) use
#     **independent** inners: Diff(Prod(F,G)) — e.g. x·sin(x), (2x+1)(x²−3).
#   - Shared-u products Diff(Prod(F,G)(u)) are reserved for forms that teach
#     product-of-composites with one inner (trig×trig of u, ln(u)·exp(u)).
#   - Quotients similarly: poly/trig textbook cases are independent; keep
#     shared-u only when both sides are clearly F(u)/G(u).
FORM_PATTERNS: dict[str, SkeletonPattern] = {
    "power_poly": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        forbid_pow_nest=True,
        pattern_label="Diff(Pow(H,n))",
    ),
    "power_root": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        prefer_roots=True,
        forbid_pow_nest=True,
        pattern_label="Diff(Pow(H,n)) roots",
    ),
    "power_negative": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        prefer_negative_power=True,
        forbid_pow_nest=True,
        pattern_label="Diff(Pow(H,n)) neg",
    ),
    "product_two_poly": SkeletonPattern(
        kind="diff_prod_fg",
        atom_fns=("poly",),
        pattern_label="Diff(Prod(F,G)) fn×fn",
    ),
    "product_poly_trig": SkeletonPattern(
        kind="diff_prod_fg",
        atom_fns=("sin", "cos"),
        atom_fns_g=("sin", "cos", "tan"),
        pattern_label="Diff(Prod(F,G)) trig×trig",
    ),
    "product_poly_exp": SkeletonPattern(
        kind="diff_prod_fg",
        atom_fns=("sin", "cos", "exp", "ln"),
        atom_fns_g=("exp",),
        pattern_label="Diff(Prod(F,G)) fn×exp",
    ),
    "product_one_chain": SkeletonPattern(
        # OpenStax §3.6 combining rules: one easy factor × (affine)^n.
        kind="diff_prod_fg",
        atom_fns=("poly",),
        require_composed_factor=True,
        pattern_label="Diff(Prod(F,G)) poly×(u)^n",
    ),
    "product_chain_powers": SkeletonPattern(
        # OpenStax Calc Vol.1 §3.6 Example 3.54: (2x+1)^5 (3x-2)^7.
        kind="diff_prod_fg",
        atom_fns=("poly",),
        require_composed_factor=True,
        both_factors_pow=True,
        pattern_label="Diff(Prod(F,G)) (u)^n(v)^m",
    ),
    "product_trig_exp_chain": SkeletonPattern(
        # OpenStax §3.9-style: sin x · e^{g(x)} (one simple × one composed).
        kind="diff_prod_fg",
        atom_fns=("sin", "cos"),
        atom_fns_g=("exp",),
        require_composed_factor=True,
        pattern_label="Diff(Prod(F,G)) trig×e^{g}",
    ),
    "quotient_poly": SkeletonPattern(
        kind="diff_quot_fg",
        atom_fns=("poly",),
        pattern_label="Diff(Quot(F,G)) poly/poly",
    ),
    "quotient_trig_poly": SkeletonPattern(
        kind="diff_quot_fg",
        atom_fns=("sin", "cos", "tan"),
        atom_fns_g=("poly",),
        pattern_label="Diff(Quot(F,G)) trig/poly",
    ),
    "quotient_exp_poly": SkeletonPattern(
        kind="diff_quot_fg",
        atom_fns=("exp",),
        atom_fns_g=("poly",),
        pattern_label="Diff(Quot(F,G)) exp/poly",
    ),
    "quotient_log_poly": SkeletonPattern(
        kind="diff_quot_fg",
        atom_fns=("ln",),
        atom_fns_g=("poly", "sin", "cos"),
        pattern_label="Diff(Quot(F,G)) log/…",
    ),
    "quotient_mixed_special": SkeletonPattern(
        kind="diff_quot_fg",
        atom_fns=("sin", "cos", "exp", "ln"),
        atom_fns_g=("sin", "cos", "exp", "ln", "poly"),
        pattern_label="Diff(Quot(F,G)) mixed",
    ),
    "chain_power_linear": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        force_affine_or_nest=True,
        pattern_label="Diff(Pow(H,n)) chain-linear",
    ),

    "chain_trig_poly": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("sin", "cos", "tan"),
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(fn,u)) chain-trig",
    ),
    "chain_exp_poly": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("exp",),
        locked_fn="exp",
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(exp,u)) chain",
    ),
    "chain_ln_poly": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("ln",),
        locked_fn="ln",
        force_affine_or_nest=True,
        pattern_label="Diff(Apply(ln,u)) chain",
    ),
    "chain_power_trig": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("sin", "cos", "tan"),
        force_affine_or_nest=True,
        force_fn_power=True,
        pattern_label="Diff(Pow(Apply(fn,u),n)) power-trig",
    ),
    "chain_nested": SkeletonPattern(
        kind="diff_apply_fn_u",
        atom_fns=("sin", "cos", "tan", "exp", "ln"),
        force_affine_or_nest=True,
        expand_from_allows=True,
        pattern_label="Diff(Apply(fn,u)) nested unlike",
    ),
    "chain_nested_power": SkeletonPattern(
        # Optional algebraic nest for power/general — not the chain-leaf default.
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        force_affine_or_nest=True,
        forbid_pow_nest=False,
        pattern_label="Diff(Pow(H,n)) nested",
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
        forbid_pow_nest=True,
        pattern_label="Diff(Pow(H,n)) order2",
    ),
    "higher_order_3": SkeletonPattern(
        kind="diff_pow_h_n",
        atom_fns=("poly",),
        forbid_pow_nest=True,
        pattern_label="Diff(Pow(H,n)) order3",
    ),
    "general_mixed": SkeletonPattern(
        # High-C multi-method mix; low-C general uses single-skill forms instead.
        kind="diff_prod_fg",
        atom_fns=("sin", "cos", "exp", "ln"),
        atom_fns_g=("sin", "cos", "exp", "ln"),
        pattern_label="Diff(Prod(F,G)) mixed fn×fn",
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


def _affine_of_var(
    var: str,
    richness: Richness,
    rng: random.Random,
    *,
    prefer_kx: bool = False,
    require_compound: bool = False,
) -> ExprAST:
    """Affine ``ax+b`` (or ``ax``).

    ``require_compound``: never return bare ``x`` (needed for chain bases).
    """
    v = Var(var)
    a = _coef(rng, min(4, richness.coef_abs_max))
    if require_compound and a == 1:
        a = int(rng.choice([-3, -2, 2, 3]))
    # Low-C trig / power pedagogy: prefer kx over ax+b.
    if prefer_kx or (richness.band == "low" and richness.conceptual_d < 3 and not require_compound):
        if rng.random() < (0.85 if prefer_kx else 0.55):
            if a == 1 and require_compound:
                a = int(rng.choice([-3, -2, 2, 3]))
            return Mul((Const(Fraction(a)), v)) if a != 1 else v
    b = _coef(rng, min(4, richness.coef_abs_max), nonzero=False)
    if require_compound and a == 1 and b == 0:
        b = int(rng.choice([-2, -1, 1, 2, 3]))
    ax: ExprAST = Mul((Const(Fraction(a)), v)) if a != 1 else v
    if b == 0:
        if require_compound and isinstance(ax, Var):
            a2 = int(rng.choice([-3, -2, 2, 3]))
            return Mul((Const(Fraction(a2)), v))
        return ax
    return Add((ax, Const(Fraction(b))))


def _simple_apply_inner(var: str, richness: Richness, rng: random.Random) -> ExprAST:
    """Low-C Apply inner: x, kx, or lightly kx+b — never a dense poly."""
    roll = rng.random()
    if roll < 0.45:
        return Var(var)
    if roll < 0.85:
        return _affine_of_var(var, richness, rng, prefer_kx=True)
    return _affine_of_var(var, richness, rng)


def _intish_exp(exp: Any) -> int | None:
    if isinstance(exp, int):
        return exp
    if isinstance(exp, Fraction) and exp.denominator == 1:
        return int(exp.numerator)
    return None


def _classify_inner_kind(u: ExprAST) -> str:
    """Honest label for what kind of inner was produced."""
    if isinstance(u, Var):
        return "var"
    if isinstance(u, Fn):
        return "nested_apply"
    if isinstance(u, Pow) and not isinstance(u.base, Var):
        return "nested_pow"
    if isinstance(u, Add):
        # Affine ax+b vs denser poly
        degish = 1
        for t in u.terms:
            if isinstance(t, Pow) and isinstance(t.base, Var):
                e = _intish_exp(t.exp)
                degish = max(degish, e if e is not None else 2)
            elif isinstance(t, Mul):
                for f in t.factors:
                    if isinstance(f, Pow) and isinstance(f.base, Var):
                        e = _intish_exp(f.exp)
                        degish = max(degish, e if e is not None else 2)
                    elif isinstance(f, (Fn, Add, Pow)) and not isinstance(f, Const):
                        return "poly_compound"
        return "affine" if degish <= 1 else "poly"
    if isinstance(u, Mul):
        if any(isinstance(f, (Fn, Add)) for f in u.factors):
            return "poly_compound"
        if any(isinstance(f, Pow) and not isinstance(f.base, Var) for f in u.factors):
            return "nested_pow"
        return "affine"
    if isinstance(u, Pow) and isinstance(u.base, Var):
        return "monomial"
    return "other"


def _count_applies(expr: ExprAST) -> int:
    if isinstance(expr, Fn):
        return 1 + _count_applies(expr.arg)
    if isinstance(expr, Pow):
        return _count_applies(expr.base)
    if isinstance(expr, Mul):
        return sum(_count_applies(f) for f in expr.factors)
    if isinstance(expr, Add):
        return sum(_count_applies(t) for t in expr.terms)
    return 0


def _poly_degree_of(expr: ExprAST) -> int:
    """Max integer power of the free variable / compound base (approx)."""
    from question_engine.frameworks.primitives.poly_expression import structure_inventory

    inv = structure_inventory(expr)
    return int(inv.get("degree_max") or 0)


def _sample_inner(
    var: str,
    richness: Richness,
    rng: random.Random,
    *,
    nest_left: int,
    atom_pool: Sequence[str],
    nest_spent: int = 0,
    allow_pow_compose: bool = True,
) -> ExprAST:
    """Sample an inner ``u``; band + nest budget drive structure (not soft collapse)."""
    non_poly = [a for a in atom_pool if a != "poly"]
    # Force / prefer nest while budget remains and force_min_nest not yet met.
    need_force = nest_spent < int(richness.force_min_nest) and nest_left > 0
    nest_p = {
        "low": 0.0,
        "mid": 0.15,
        "high": 0.55,
        "elite": 0.8,
    }.get(richness.band, 0.0)
    if nest_left > 0 and (need_force or rng.random() < nest_p):
        sub = _sample_inner(
            var,
            richness,
            rng,
            nest_left=nest_left - 1,
            atom_pool=atom_pool,
            nest_spent=nest_spent + 1,
            allow_pow_compose=allow_pow_compose,
        )
        if non_poly:
            return Fn(_pick_unlike_fn(non_poly, _fn_names_in(sub), rng), sub)
        # Poly-only: prefer poly-of-sub over Pow(sub,n) to avoid compose towers.
        if allow_pow_compose and richness.band in ("high", "elite") and rng.random() < 0.35:
            n_lo = max(2, int(richness.power_min))
            n_hi = max(n_lo, min(int(richness.power_max), 5))
            return Pow(sub, Fraction(int(rng.randint(n_lo, n_hi))))
        return _poly_of_u(sub, richness, rng)

    # Mid+: simple special-of-x/affine leaf so e^{sin x} / ln(cos x) are
    # f(g(x)) — not a spent nest slot and not a power tower.
    if (
        nest_left == 0
        and non_poly
        and richness.band in ("mid", "high", "elite")
        and rng.random() < (0.50 if richness.band == "mid" else 0.22)
    ):
        leaf = (
            _simple_apply_inner(var, richness, rng)
            if richness.band == "mid"
            else (
                _affine_of_var(var, richness, rng)
                if rng.random() < 0.55
                else _poly_leaf(var, richness, rng)
            )
        )
        return Fn(_pick_unlike_fn(non_poly, set(), rng), leaf)

    # Leaf modes by band — mid+ prefer poly; low stays var/affine.
    if richness.prefer_poly_u and richness.allow_poly_u:
        if rng.random() < (0.85 if richness.band in ("high", "elite") else 0.65):
            return _poly_leaf(var, richness, rng)
        return _affine_of_var(var, richness, rng)

    if richness.allow_poly_u and rng.random() < 0.45:
        return _poly_leaf(var, richness, rng)

    if richness.allow_affine_u and rng.random() < (
        0.75 if richness.conceptual_d >= 2 else 0.4
    ):
        return _affine_of_var(var, richness, rng)

    return Var(var)


def _poly_leaf(var: str, richness: Richness, rng: random.Random) -> ExprAST:
    """Polynomial in the free variable (not poly-of-compound-u)."""
    v = Var(var)
    deg_lo = max(1, int(richness.poly_degree_min))
    deg_hi = max(deg_lo, min(4, int(richness.power_max) + (1 if richness.band in ("high", "elite") else 0)))
    if richness.band == "low":
        deg_hi = max(deg_lo, min(2, deg_hi))
    deg = int(rng.randint(deg_lo, deg_hi))
    terms: list[ExprAST] = []
    for k in range(deg, -1, -1):
        if k == 0:
            c = _coef(rng, richness.coef_abs_max, nonzero=False)
            if c:
                terms.append(Const(Fraction(c)))
            continue
        if k < deg and rng.random() < (0.2 if richness.band in ("high", "elite") else 0.35):
            continue
        c = _coef(rng, richness.coef_abs_max)
        pk: ExprAST = Pow(v, Fraction(k)) if k != 1 else v
        terms.append(Mul((Const(Fraction(c)), pk)) if c != 1 else pk)
    if not terms:
        return _affine_of_var(var, richness, rng)
    if len(terms) == 1:
        return terms[0]
    return Add(tuple(terms))


def _poly_of_u(u: ExprAST, richness: Richness, rng: random.Random) -> ExprAST:
    """Polynomial in the shared inner ``u`` (not a free poly of x).

    When ``u`` is already a compound expression, always wrap as ``c·u^n`` or
    ``c·u+d`` so the shared-u invariant stays visible after render.
    """
    deg_lo = max(1, int(richness.poly_degree_min))
    deg_hi = max(deg_lo, min(3, int(richness.power_max)))
    deg = int(rng.randint(deg_lo, deg_hi))
    # Free poly of x only when the hole's inner is the bare variable and poly unlocked.
    if isinstance(u, Var) and richness.allow_poly_u and rng.random() < 0.55:
        return _poly_leaf(u.name, richness, rng)
    if isinstance(u, Var) and rng.random() < 0.55:
        c = _coef(rng, richness.coef_abs_max)
        body: ExprAST = Pow(u, Fraction(deg)) if deg != 1 else u
        return Mul((Const(Fraction(c)), body)) if c != 1 else body
    # Honest poly-of-u: keep ``u`` as a structural unit (render wraps Add).
    # Low band: prefer linear-in-u (c·u+d), never high powers of compound u.
    if richness.band == "low":
        c = _coef(rng, richness.coef_abs_max)
        d = _coef(rng, min(3, richness.coef_abs_max), nonzero=False)
        cu = Mul((Const(Fraction(c)), u)) if c != 1 else u
        if d == 0:
            return cu
        return Add((cu, Const(Fraction(d))))
    if rng.random() < 0.55 or richness.band in ("high", "elite"):
        c = _coef(rng, richness.coef_abs_max)
        body = Pow(u, Fraction(deg)) if deg != 1 else u
        return Mul((Const(Fraction(c)), body)) if c != 1 else body
    c = _coef(rng, richness.coef_abs_max)
    d = _coef(rng, min(3, richness.coef_abs_max), nonzero=False)
    cu = Mul((Const(Fraction(c)), u)) if c != 1 else u
    if d == 0:
        return cu
    return Add((cu, Const(Fraction(d))))


def _unwrap_scale(expr: ExprAST) -> ExprAST:
    """Peel a leading constant multiplier."""
    if (
        isinstance(expr, Mul)
        and len(expr.factors) == 2
        and isinstance(expr.factors[0], Const)
        and not isinstance(expr.factors[1], Const)
    ):
        return expr.factors[1]
    return expr


def _factor_is_composed(expr: ExprAST) -> bool:
    """True when a product factor needs the chain rule (not x^n / f(x))."""
    core = _unwrap_scale(expr)
    if isinstance(core, Pow) and not isinstance(core.base, Var):
        return True
    if isinstance(core, Fn) and not isinstance(core.arg, Var):
        return True
    return False


def _sample_pow_chain_factor(
    var: str, richness: Richness, rng: random.Random
) -> ExprAST:
    """(ax+b)^n — OpenStax Example 3.54 factor; affine base, never f(g(h))."""
    base = _affine_of_var(var, richness, rng, require_compound=True)
    if not isinstance(base, Add):
        # Example 3.54 is (2x+1), not kx alone.
        b = _coef(rng, min(4, richness.coef_abs_max))
        base = Add((base, Const(Fraction(b))))
    n_lo = max(2, int(richness.power_min))
    n_hi = max(n_lo, min(int(richness.power_max), 7 if richness.band == "elite" else 5))
    n = int(rng.randint(n_lo, n_hi))
    return Pow(base, Fraction(n))


def _sample_trig_simple_factor(
    atoms: Sequence[str],
    var: str,
    richness: Richness,
    rng: random.Random,
) -> ExprAST:
    """sin x / cos(kx) — simple left factor for sin x · e^{g(x)}."""
    pool = [a for a in atoms if a in ("sin", "cos", "tan")] or ["sin"]
    fn = str(rng.choice(pool))
    if richness.band == "low" or rng.random() < 0.6:
        u: ExprAST = Var(var)
    else:
        u = _affine_of_var(var, richness, rng, prefer_kx=True)
    return Fn(fn, u)


def _sample_exp_composed_factor(
    var: str, richness: Richness, rng: random.Random
) -> ExprAST:
    """e^{g(x)} with g affine (mid) or poly (high) — not e^{sin(h)}."""
    if richness.band in ("high", "elite") and richness.allow_poly_u and rng.random() < 0.4:
        u: ExprAST = _poly_leaf(var, richness, rng)
    else:
        u = _affine_of_var(var, richness, rng, require_compound=True)
    return Fn("exp", u)


def _sample_poly_factor(
    var: str,
    richness: Richness,
    rng: random.Random,
    *,
    force_plain: bool = False,
) -> ExprAST:
    """One product/quotient poly side: fn-like, not compose-pow towers.

    Low C: monomial / affine / scaled var.
    Mid: denser poly; rare single (affine)^n.
    High+: messy poly; occasional Pow(poly, n) as the *factor itself*.
    ``force_plain``: never emit (affine/poly)^n (the other factor owns chain).
    """
    if richness.band == "low":
        roll = rng.random()
        if roll < 0.4:
            c = _coef(rng, min(3, richness.coef_abs_max))
            return Mul((Const(Fraction(c)), Var(var))) if c != 1 else Var(var)
        if roll < 0.75:
            return _affine_of_var(var, richness, rng)
        # Mild monomial cx^2
        c = _coef(rng, min(3, richness.coef_abs_max))
        body: ExprAST = Pow(Var(var), Fraction(2))
        return Mul((Const(Fraction(c)), body)) if c != 1 else body

    if richness.band == "mid":
        if richness.allow_poly_u and rng.random() < 0.7:
            return _poly_leaf(var, richness, rng)
        if not force_plain and rng.random() < 0.2:
            n_lo = max(2, int(richness.power_min))
            n_hi = max(n_lo, min(int(richness.power_max), 3))
            base = _affine_of_var(var, richness, rng)
            return Pow(base, Fraction(int(rng.randint(n_lo, n_hi))))
        return _affine_of_var(var, richness, rng)

    # high / elite
    if force_plain or rng.random() < 0.75:
        return _poly_leaf(var, richness, rng)
    n_lo = max(2, int(richness.power_min))
    n_hi = max(n_lo, min(int(richness.power_max), 5))
    base = _poly_leaf(var, richness, rng) if richness.allow_poly_u else _affine_of_var(
        var, richness, rng
    )
    powered = Pow(base, Fraction(int(rng.randint(n_lo, n_hi))))
    c = _coef(rng, richness.coef_abs_max)
    return Mul((Const(Fraction(c)), powered)) if c != 1 else powered


def _sample_apply_factor(
    fn: str,
    var: str,
    richness: Richness,
    rng: random.Random,
    *,
    nest_left: int,
    atom_pool: Sequence[str],
) -> ExprAST:
    """Apply(fn, u) factor; low C keeps u = x / kx / light affine."""
    if richness.band == "low":
        return _apply_fn_of_u(fn, _simple_apply_inner(var, richness, rng))
    u = _sample_inner(
        var,
        richness,
        rng,
        nest_left=nest_left,
        atom_pool=atom_pool,
        allow_pow_compose=False,
    )
    if richness.band == "mid" and isinstance(u, Var) and rng.random() < 0.6:
        u = _affine_of_var(var, richness, rng)
    return _apply_fn_of_u(fn, u)


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
    independent_factor: bool = False,
    var: str = "x",
    nest_left: int = 0,
) -> ExprAST:
    pool = list(atom_choices) or ["poly"]
    if prefer_non_poly:
        non = [a for a in pool if a != "poly"]
        if non:
            pool = non
    fn = rng.choice(pool)
    if fn == "poly":
        if independent_factor:
            return _sample_poly_factor(var, richness, rng)
        # Shared-u poly hole — keep structural link to u.
        if richness.band == "low" and not isinstance(u, Var):
            c = _coef(rng, richness.coef_abs_max)
            return Mul((Const(Fraction(c)), u)) if c != 1 else u
        return _poly_of_u(u, richness, rng)
    if independent_factor:
        return _sample_apply_factor(
            fn, var, richness, rng, nest_left=nest_left, atom_pool=pool
        )
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


def _compose_atoms_from_allows(
    allows: Mapping[str, bool],
    base: Sequence[str] | None = None,
) -> list[str]:
    """Allowed function-class tokens for nest slots (OpenStax compose pool)."""
    pool: list[str] = []
    for a in base or ():
        if a not in pool:
            pool.append(a)
    extras: list[str] = []
    if allows.get("allow_trig"):
        extras.extend(("sin", "cos", "tan"))
    if allows.get("allow_exp"):
        extras.append("exp")
    if allows.get("allow_log"):
        extras.append("ln")
    if allows.get("allow_invtrig"):
        extras.extend(("arcsin", "arctan"))
    for a in extras:
        if a not in pool:
            pool.append(a)
    return pool or ["poly"]


def _fn_names_in(expr: ExprAST) -> set[str]:
    names: set[str] = set()
    if isinstance(expr, Fn):
        names.add(expr.name)
        names |= _fn_names_in(expr.arg)
    elif isinstance(expr, Pow):
        names |= _fn_names_in(expr.base)
    elif isinstance(expr, Mul):
        for f in expr.factors:
            names |= _fn_names_in(f)
    elif isinstance(expr, Add):
        for t in expr.terms:
            names |= _fn_names_in(t)
    return names


def _pick_unlike_fn(
    pool: Sequence[str],
    used: set[str],
    rng: random.Random,
) -> str:
    """Prefer a function class not already used in the nest."""
    unlike = [a for a in pool if a != "poly" and a not in used]
    if unlike:
        return str(rng.choice(unlike))
    non_poly = [a for a in pool if a != "poly"]
    if non_poly:
        return str(rng.choice(non_poly))
    return "poly"


def _compose_layers(expr: ExprAST) -> list[str]:
    """Outer-to-inner layer tags: sin / exp / ln / pow / …"""
    layers: list[str] = []
    cur: ExprAST = expr
    while True:
        if (
            isinstance(cur, Mul)
            and len(cur.factors) == 2
            and isinstance(cur.factors[0], Const)
            and not isinstance(cur.factors[1], Const)
        ):
            cur = cur.factors[1]
            continue
        if isinstance(cur, Fn):
            layers.append(cur.name)
            cur = cur.arg
            continue
        if isinstance(cur, Pow) and not isinstance(cur.base, Var):
            layers.append("pow")
            cur = cur.base
            continue
        break
    return layers


def _schedule_atoms(
    filtered: Sequence[str],
    pattern_atoms: Sequence[str],
    richness: Richness,
    allows: Mapping[str, bool],
    rng: random.Random,
) -> list[str]:
    """Hard gate already applied; at low C prefer core atoms over every allowed class.

    Pattern-declared atoms that are topic-primary (e.g. sin for trig_basic) stay.
    Cross-class extras that happen to be allowed stay rare until mid/high C.
    """
    pool = list(filtered) or ["poly"]
    if richness.band in ("high", "elite"):
        return pool
    # Core = atoms the pattern lists that passed the allow gate.
    core = [a for a in pattern_atoms if a in pool]
    if not core:
        core = pool
    if richness.band == "low":
        # Stick to pattern core; only rarely admit an extra allowed class.
        extras = [a for a in pool if a not in core]
        if extras and rng.random() < 0.08:
            return list(dict.fromkeys([*core, rng.choice(extras)]))
        return core or pool
    # Mid: sometimes include one extra allowed class.
    extras = [a for a in pool if a not in core]
    if extras and rng.random() < 0.35:
        return list(dict.fromkeys([*core, rng.choice(extras)]))
    return core or pool


def _monomial_power(
    var: str,
    richness: Richness,
    rng: random.Random,
    *,
    prefer_roots: bool = False,
    prefer_negative: bool = False,
) -> ExprAST:
    """Pure power-rule leaf: ``x^n`` / ``k x^n`` (or root / negative n)."""
    h: ExprAST = Var(var)
    if prefer_roots:
        num = int(rng.choice([1, 1, 3, 5]))
        den = int(rng.choice([2, 2, 3]))
        if num == den:
            num, den = 1, 2
        body: ExprAST = Pow(h, Fraction(num, den))
    elif prefer_negative:
        n_hi = max(1, min(4, int(richness.power_max)))
        n_lo = 1 if richness.band == "low" else min(2, n_hi)
        body = Pow(h, Fraction(-int(rng.randint(n_lo, n_hi))))
    else:
        n_lo = max(2, int(richness.power_min))
        n_hi = max(n_lo, min(int(richness.power_max), 7 if richness.band == "elite" else 5))
        body = Pow(h, Fraction(int(rng.randint(n_lo, n_hi))))
    if rng.random() < 0.45:
        c = _coef(rng, richness.coef_abs_max)
        return Mul((Const(Fraction(c)), body)) if c != 1 else body
    return body


def _build_pow(
    pattern: SkeletonPattern,
    u: ExprAST,
    richness: Richness,
    rng: random.Random,
    *,
    var: str = "x",
    allows: Mapping[str, bool] | None = None,
) -> ExprAST:
    """Single outer power Pow(H, n) — never a compose-pow tower.

    Chain gating (``allow_chain`` / ``require_chain``):
      - checkbox off: never ``(ax+b)^n`` on pure power forms
      - checkbox on: C schedules rarity (rare low → common high)
      - require / chain form: always chain base
    Without chain: ``x^n``, ``k x^n``, or expanded poly sum.
    """
    allows = dict(allows or {})
    allow_chain = bool(allows.get("allow_chain", False))
    require_chain = bool(allows.get("require_chain", False))
    is_chain_form = bool(pattern.force_affine_or_nest) or (
        "chain" in (pattern.pattern_label or "")
    )

    use_chain_base = False
    if is_chain_form or require_chain:
        use_chain_base = True
    elif pattern.forbid_pow_nest and allow_chain:
        # Allowed but scheduled by C — uncommon at low, common at high.
        p = {
            "low": 0.08,
            "mid": 0.35,
            "high": 0.7,
            "elite": 0.9,
        }.get(richness.band, 0.2)
        use_chain_base = rng.random() < p
    elif not pattern.forbid_pow_nest and allow_chain:
        use_chain_base = richness.band != "low" and rng.random() < 0.4

    if not use_chain_base and pattern.forbid_pow_nest:
        # No chain: densify via |n| / poly *sum*, never outer power of affine.
        # Root / negative-power forms must keep that flesh (not a plain poly sum)
        # so form_id matches what the student sees.
        if pattern.prefer_roots or pattern.prefer_negative_power:
            return _monomial_power(
                var,
                richness,
                rng,
                prefer_roots=pattern.prefer_roots,
                prefer_negative=pattern.prefer_negative_power,
            )
        if richness.band != "low" and richness.allow_poly_u and rng.random() < (
            0.7 if richness.prefer_poly_u else 0.4
        ):
            return _poly_leaf(var, richness, rng)
        return _monomial_power(
            var,
            richness,
            rng,
            prefer_roots=False,
            prefer_negative=False,
        )

    if use_chain_base:
        # Nested chain forms: prefer an already-composed inner (Pow / Fn)
        # from the nest sampler so we get (poly)^n inside an outer power.
        nested_form = "nested" in (pattern.pattern_label or "")
        if nested_form and (
            isinstance(u, Pow)
            or isinstance(u, Fn)
            or (
                isinstance(u, Mul)
                and any(isinstance(f, (Pow, Fn)) for f in u.factors)
            )
        ):
            h = u
        elif richness.allow_poly_u and (
            richness.prefer_poly_u or richness.band in ("high", "elite")
        ):
            if rng.random() < (0.85 if richness.prefer_poly_u else 0.45):
                h = _poly_leaf(var, richness, rng)
            else:
                h = _affine_of_var(var, richness, rng, require_compound=True)
        else:
            h = _affine_of_var(var, richness, rng, require_compound=True)
        # Belt-and-suspenders: chain base must not collapse to bare x.
        if isinstance(h, Var):
            # Nested forms: synthesize (affine)^k then outer power below.
            if nested_form and richness.force_min_nest >= 1:
                inner = _affine_of_var(var, richness, rng, require_compound=True)
                k = int(rng.randint(2, max(2, min(4, int(richness.power_max)))))
                h = Pow(inner, Fraction(k))
            else:
                h = _affine_of_var(var, richness, rng, require_compound=True)
    elif not isinstance(u, Var):
        h = u
    else:
        h = u if isinstance(u, Var) else Var(var)

    if pattern.prefer_roots:
        num = int(rng.choice([1, 1, 3, 5]))
        den = int(rng.choice([2, 2, 3]))
        if num == den:
            num, den = 1, 2
        return Pow(h, Fraction(num, den))
    if pattern.prefer_negative_power:
        n_hi = max(1, min(4, int(richness.power_max)))
        n_lo = 1 if richness.band == "low" else min(2, n_hi)
        n = -int(rng.randint(n_lo, n_hi))
        return Pow(h, Fraction(n))
    n_lo = max(2, int(richness.power_min))
    n_hi = max(n_lo, min(int(richness.power_max), 7 if richness.band == "elite" else 5))
    n = int(rng.randint(n_lo, n_hi))
    body = Pow(h, Fraction(n))
    if is_chain_form or isinstance(h, Var):
        if isinstance(h, Var) and rng.random() < 0.45:
            c = _coef(rng, richness.coef_abs_max)
            return Mul((Const(Fraction(c)), body)) if c != 1 else body
        return body
    if rng.random() < 0.35:
        c = _coef(rng, richness.coef_abs_max)
        return Mul((Const(Fraction(c)), body)) if c != 1 else body
    return body


def _expr_contains_u(expr: ExprAST, u: ExprAST) -> bool:
    """True if ``u`` appears as a structural subtree of ``expr``."""
    if expr == u:
        return True
    if isinstance(expr, Fn):
        return _expr_contains_u(expr.arg, u)
    if isinstance(expr, Pow):
        return _expr_contains_u(expr.base, u)
    if isinstance(expr, Mul):
        return any(_expr_contains_u(f, u) for f in expr.factors)
    if isinstance(expr, Add):
        return any(_expr_contains_u(t, u) for t in expr.terms)
    return False


def _hole_uses_shared_u(expr: ExprAST, u: ExprAST) -> bool:
    """Hole is Apply(fn,u), poly-of-u, or otherwise structurally contains ``u``."""
    if isinstance(expr, Fn):
        return expr.arg == u or _expr_contains_u(expr.arg, u)
    return _expr_contains_u(expr, u)


def _spend_breakdown(
    expr: ExprAST,
    *,
    richness: Richness,
    pattern: SkeletonPattern,
    u: ExprAST | None,
    atoms: Sequence[str],
    atoms_g: Sequence[str],
    nest_budget_used: int,
) -> dict[str, Any]:
    """Honest accounting of structure spent — no padding."""
    from question_engine.frameworks.primitives.poly_expression import (
        chain_depth_of,
        structure_inventory,
    )

    inv = structure_inventory(expr)
    inner_kind = _classify_inner_kind(u) if u is not None else "n/a"
    return {
        "nest_budget": int(richness.nest_budget),
        "nest_budget_forced_min": int(richness.force_min_nest),
        "nest_left_at_sample": int(nest_budget_used),
        "nest_depth_expr": int(inv.get("nest_depth") or 0),
        "chain_depth": int(chain_depth_of(expr)),
        "degree_max": int(inv.get("degree_max") or 0),
        "n_applies": _count_applies(expr),
        "n_terms": int(inv.get("n_terms") or 0),
        "n_factors": int(inv.get("n_factors") or 0),
        "inner_kind": inner_kind,
        "inner_degree": _poly_degree_of(u) if u is not None else 0,
        "atom_fn_candidates": list(atoms),
        "atom_fn_candidates_g": list(atoms_g),
        "shared_vs_independent": (
            "shared_u"
            if pattern.kind
            in {
                "diff_prod_fg_u",
                "diff_sum_fg_u",
                "diff_quot_fg_u",
                "diff_pow_h_n",
                "diff_apply_fn_u",
                "diff_f_of_u",
            }
            else "independent"
        ),
        "pattern_locks_top_structure": True,
        "note": (
            "power: nest capped — harden poly/|n|"
            if pattern.forbid_pow_nest
            else "C densifies holes only; pattern kind is form-locked"
        ),
    }


def sample_expr_from_pattern(
    pattern: SkeletonPattern,
    *,
    richness: Richness,
    allows: Mapping[str, bool] | None = None,
    rng: random.Random | None = None,
    var: str = "x",
    seed: int | None = None,
) -> tuple[ExprAST, dict[str, Any]]:
    """Fill holes in ``pattern``; return ExprAST + inventory meta."""
    if rng is None:
        rng = random.Random(seed) if seed is not None else random.Random()
    allows = dict(allows or {})
    # Method gates default OFF so pure forms stay pure unless the leaf opts in.
    for key, default in (
        ("allow_trig", True),
        ("allow_exp", True),
        ("allow_log", True),
        ("allow_roots", True),
        ("allow_invtrig", True),
        ("allow_chain", False),
        ("require_chain", False),
        ("allow_product", True),
        ("allow_quotient", True),
    ):
        allows.setdefault(key, default)

    atoms = _filter_atom_fns(pattern.atom_fns, allows)
    atoms_g = _filter_atom_fns(pattern.atom_fns_g or pattern.atom_fns, allows)
    if pattern.expand_from_allows:
        # Nested unlike: outer may also pick any allowed class.
        atoms = _filter_atom_fns(_compose_atoms_from_allows(allows, atoms), allows)
        atoms_g = _filter_atom_fns(_compose_atoms_from_allows(allows, atoms_g), allows)
    # Soft schedule: even when specials are allowed, low C prefers the form's
    # core atoms (poly / locked fn) over dumping every allowed class.
    atoms = _schedule_atoms(atoms, pattern.atom_fns, richness, allows, rng)
    atoms_g = _schedule_atoms(
        atoms_g, pattern.atom_fns_g or pattern.atom_fns, richness, allows, rng
    )
    nest = int(richness.nest_budget)
    rich = richness

    # Pure power-rule forms: never spend nest as compose-pow towers.
    if pattern.forbid_pow_nest:
        rich = Richness(
            conceptual_d=richness.conceptual_d,
            nest_budget=0,
            allow_affine_u=True,
            allow_poly_u=richness.allow_poly_u
            or richness.band in ("mid", "high", "elite"),
            prefer_poly_u=richness.prefer_poly_u
            or richness.band in ("high", "elite")
            or (richness.band == "mid" and richness.conceptual_d >= 6),
            force_min_nest=0,
            allow_form_min_nest=False,
            power_min=richness.power_min,
            poly_degree_min=richness.poly_degree_min,
            coef_abs_max=richness.coef_abs_max,
            power_max=richness.power_max,
            band=richness.band,
        )
        nest = 0
    elif pattern.force_affine_or_nest or (
        pattern.kind in ("diff_apply_fn_u", "diff_pow_h_n")
        and "chain" in pattern.label()
    ):
        nest_use = nest
        force_min = int(richness.force_min_nest)
        if (
            pattern.force_affine_or_nest
            and "nested" in pattern.label()
            and richness.allow_form_min_nest
        ):
            nest_use = max(nest, 1)
            force_min = max(force_min, 1)
        rich = Richness(
            conceptual_d=richness.conceptual_d,
            nest_budget=nest_use,
            allow_affine_u=True,
            allow_poly_u=richness.allow_poly_u
            or (richness.band != "low" and richness.allow_form_min_nest),
            prefer_poly_u=richness.prefer_poly_u
            or (
                richness.allow_form_min_nest
                and richness.band in ("high", "elite")
            ),
            force_min_nest=force_min if nest_use else 0,
            allow_form_min_nest=richness.allow_form_min_nest,
            power_min=richness.power_min,
            poly_degree_min=richness.poly_degree_min,
            coef_abs_max=richness.coef_abs_max,
            power_max=richness.power_max,
            band=richness.band,
        )
        nest = nest_use

    # Product / quotient: keep low-C sides simple (no forced nest densify).
    # Independent Apply factors: never deep Fn∘Fn towers — harden via poly args.
    if pattern.kind in ("diff_prod_fg", "diff_quot_fg", "diff_prod_fg_u", "diff_quot_fg_u"):
        if rich.band == "low":
            rich = Richness(
                conceptual_d=rich.conceptual_d,
                nest_budget=0,
                allow_affine_u=True,
                allow_poly_u=False,
                prefer_poly_u=False,
                force_min_nest=0,
                allow_form_min_nest=False,
                power_min=2,
                poly_degree_min=1,
                coef_abs_max=min(3, rich.coef_abs_max),
                power_max=2,
                band="low",
            )
            nest = 0
        elif pattern.kind in ("diff_prod_fg", "diff_quot_fg"):
            # Cap Apply-nest on independent sides (0 mid, 1 high/elite).
            nest = 0 if rich.band == "mid" else min(nest, 1)
            rich = Richness(
                conceptual_d=rich.conceptual_d,
                nest_budget=nest,
                allow_affine_u=rich.allow_affine_u,
                allow_poly_u=rich.allow_poly_u,
                prefer_poly_u=rich.prefer_poly_u,
                force_min_nest=0,
                allow_form_min_nest=False,
                power_min=rich.power_min,
                poly_degree_min=rich.poly_degree_min,
                coef_abs_max=rich.coef_abs_max,
                power_max=rich.power_max,
                band=rich.band,
            )

    # ln/exp / invtrig basics: at most one Apply nest (never ln∘ln∘ln towers).
    if pattern.locked_fn in {"ln", "exp", "arcsin", "arctan"}:
        nest = min(nest, 1 if rich.band in ("high", "elite") else 0)
        rich = Richness(
            conceptual_d=rich.conceptual_d,
            nest_budget=nest,
            allow_affine_u=rich.allow_affine_u,
            allow_poly_u=rich.allow_poly_u,
            prefer_poly_u=rich.prefer_poly_u,
            force_min_nest=min(rich.force_min_nest, nest),
            allow_form_min_nest=rich.allow_form_min_nest,
            power_min=rich.power_min,
            poly_degree_min=rich.poly_degree_min,
            coef_abs_max=rich.coef_abs_max,
            power_max=rich.power_max,
            band=rich.band,
        )
    pool_u = atoms + [a for a in atoms_g if a not in atoms]
    if pattern.expand_from_allows or (
        pattern.force_affine_or_nest and richness.band != "low"
    ):
        # Inner nest slots use the full allowed class pool (not poly-only).
        pool_u = _filter_atom_fns(_compose_atoms_from_allows(allows, pool_u), allows)
        # Locked outer (e^{·} / ln(·)): prefer an unlike inner when one exists.
        if pattern.locked_fn:
            unlike_u = [a for a in pool_u if a != pattern.locked_fn]
            if any(a != "poly" for a in unlike_u):
                pool_u = unlike_u
    shared_kinds = {
        "diff_prod_fg_u",
        "diff_sum_fg_u",
        "diff_quot_fg_u",
        "diff_pow_h_n",
        "diff_apply_fn_u",
        "diff_f_of_u",
    }
    independent_kinds = {"diff_prod_fg", "diff_quot_fg"}
    allow_pow_compose = not pattern.forbid_pow_nest

    u = _sample_inner(
        var,
        rich,
        rng,
        nest_left=nest,
        atom_pool=pool_u,
        allow_pow_compose=allow_pow_compose,
    )
    # Low-C basic Apply (trig/ln/exp table): prefer x / kx / light affine.
    if (
        pattern.kind == "diff_apply_fn_u"
        and not pattern.force_affine_or_nest
        and rich.band == "low"
    ):
        u = _simple_apply_inner(var, rich, rng)
    elif pattern.force_affine_or_nest and isinstance(u, Var):
        # Bare x is too flat for chain pedagogy except low-C ln/exp basics.
        is_basic_apply = pattern.locked_fn in {
            "ln",
            "exp",
            "arcsin",
            "arctan",
        }
        if rich.band == "low" and is_basic_apply:
            u = _simple_apply_inner(var, rich, rng)
        elif rich.allow_poly_u and rich.prefer_poly_u and rich.band != "low":
            u = _poly_leaf(var, rich, rng)
        else:
            u = _affine_of_var(var, rich, rng)

    meta: dict[str, Any] = {
        "skeleton_pattern": pattern.label(),
        "skeleton_kind": pattern.kind,
        "shared_inner": pattern.kind in shared_kinds
        and pattern.kind not in independent_kinds,
        "richness_band": rich.band,
        "richness_knobs": rich.as_knobs(),
        "atom_fn_candidates": list(atoms),
        "atom_fn_candidates_g": list(atoms_g),
    }
    if seed is not None:
        meta["rng_seed"] = int(seed)

    if pattern.kind == "diff_prod_fg_u":
        f = _sample_f_hole(atoms, u, rich, rng, prefer_non_poly=("poly" not in atoms))
        g = _sample_f_hole(
            atoms_g, u, rich, rng, prefer_non_poly=("poly" not in atoms_g)
        )
        for _ in range(4):
            if render_latex(f) != render_latex(g):
                break
            g = _sample_f_hole(atoms_g, u, rich, rng)
        # Soft invariant: each hole must still contain the shared u.
        if not _hole_uses_shared_u(f, u):
            f = _apply_fn_of_u(
                rng.choice([a for a in atoms if a != "poly"] or ["sin"]), u
            )
        if not _hole_uses_shared_u(g, u):
            g = _apply_fn_of_u(
                rng.choice([a for a in atoms_g if a != "poly"] or ["cos"]), u
            )
        expr: ExprAST = Mul((f, g))
        meta["productions"] = ["Prod", "F", "G", "u"]
        meta["shared_inner"] = True
    elif pattern.kind == "diff_prod_fg":
        # Independent factors. Product+chain forms compose a *factor* (OpenStax
        # §3.6 Example 3.54 / §3.9 sin x · e^{g}); they do not dump f(g(h)).
        g_atoms = tuple(pattern.atom_fns_g or pattern.atom_fns)
        if pattern.both_factors_pow:
            f = _sample_pow_chain_factor(var, rich, rng)
            g = _sample_pow_chain_factor(var, rich, rng)
            for _ in range(8):
                if render_latex(f) != render_latex(g):
                    break
                g = _sample_pow_chain_factor(var, rich, rng)
        elif pattern.require_composed_factor and g_atoms == ("exp",):
            f = _sample_trig_simple_factor(atoms, var, rich, rng)
            g = _sample_exp_composed_factor(var, rich, rng)
        elif pattern.require_composed_factor:
            f = _sample_poly_factor(var, rich, rng, force_plain=True)
            g = _sample_pow_chain_factor(var, rich, rng)
            for _ in range(6):
                if render_latex(f) != render_latex(g):
                    break
                g = _sample_pow_chain_factor(var, rich, rng)
        else:
            f = _sample_f_hole(
                atoms,
                Var(var),
                rich,
                rng,
                prefer_non_poly=("poly" not in atoms),
                independent_factor=True,
                var=var,
                nest_left=nest,
            )
            g = _sample_f_hole(
                atoms_g,
                Var(var),
                rich,
                rng,
                prefer_non_poly=("poly" not in atoms_g),
                independent_factor=True,
                var=var,
                nest_left=nest,
            )
            for _ in range(6):
                if render_latex(f) != render_latex(g):
                    break
                g = _sample_f_hole(
                    atoms_g,
                    Var(var),
                    rich,
                    rng,
                    independent_factor=True,
                    var=var,
                    nest_left=nest,
                )
            if pattern.require_composed_factor and not (
                _factor_is_composed(f) or _factor_is_composed(g)
            ):
                g = _sample_pow_chain_factor(var, rich, rng)
        expr = Mul((f, g))
        meta["productions"] = ["Prod", "F", "G"]
        meta["shared_inner"] = False
        meta["methods_hint"] = ["product"]
        if pattern.require_composed_factor or pattern.both_factors_pow:
            meta["methods_hint"] = ["product", "chain"]
        u = f  # primary for spend label
        meta["independent_inners"] = {
            "u_f_kind": _classify_inner_kind(f),
            "u_g_kind": _classify_inner_kind(g),
            "u_f_latex": render_latex(f),
            "u_g_latex": render_latex(g),
        }
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
        meta["shared_inner"] = True
    elif pattern.kind == "diff_quot_fg":
        f = _sample_f_hole(
            atoms,
            Var(var),
            rich,
            rng,
            prefer_non_poly=("poly" not in atoms),
            independent_factor=True,
            var=var,
            nest_left=nest,
        )
        g = _sample_f_hole(
            atoms_g,
            Var(var),
            rich,
            rng,
            independent_factor=True,
            var=var,
            nest_left=nest,
        )
        for _ in range(8):
            if render_latex(g) not in {"0", render_latex(f)} and not (
                isinstance(g, Const) and g.value == 0
            ):
                break
            g = _sample_f_hole(
                atoms_g,
                Var(var),
                rich,
                rng,
                independent_factor=True,
                var=var,
                nest_left=nest,
            )
        expr = Mul((f, Pow(g, -1)))
        meta["productions"] = ["Quot", "F", "G"]
        meta["methods_hint"] = ["quotient"]
        meta["shared_inner"] = False
        u = f
        meta["independent_inners"] = {
            "u_f_kind": _classify_inner_kind(f),
            "u_g_kind": _classify_inner_kind(g),
            "u_f_latex": render_latex(f),
            "u_g_latex": render_latex(g),
        }
    elif pattern.kind == "diff_sum_fg_u":
        f = _sample_f_hole(atoms, u, rich, rng)
        g = _sample_f_hole(atoms_g, u, rich, rng)
        expr = Add((f, g))
        meta["productions"] = ["Sum", "F", "G", "u"]
        meta["shared_inner"] = True
    elif pattern.kind == "diff_pow_h_n":
        expr = _build_pow(pattern, u, rich, rng, var=var, allows=allows)
        meta["productions"] = ["Pow", "H", "n", "u"]
        meta["shared_inner"] = True
    elif pattern.kind == "diff_apply_fn_u":
        fn = pattern.locked_fn
        if fn is None:
            pool = [a for a in atoms if a != "poly"] or atoms
            fn = _pick_unlike_fn(pool, _fn_names_in(u), rng)
            if fn == "poly":
                expr = _poly_of_u(u, rich, rng)
                meta["productions"] = ["Poly", "u"]
                meta["shared_inner"] = True
                meta["chosen_outer"] = "poly"
                meta["compose_layers"] = _compose_layers(expr)
                meta["inner_latex"] = render_latex(u)
                meta["cost_spend"] = _spend_breakdown(
                    expr,
                    richness=rich,
                    pattern=pattern,
                    u=u,
                    atoms=atoms,
                    atoms_g=atoms_g,
                    nest_budget_used=nest,
                )
                return expr, meta
        expr = _apply_fn_of_u(fn, u)
        # Mid+: occasional Pow(fn(u), n) for trig pedagogy (sin² / tan³).
        wrap_power = bool(pattern.force_fn_power) or (
            fn in {"sin", "cos", "tan"}
            and rich.band != "low"
            and rich.conceptual_d >= 6
            and rng.random()
            < (0.55 if rich.band in ("high", "elite") else 0.4)
        )
        if wrap_power and fn in {"sin", "cos", "tan"}:
            n_lo = 2
            n_hi = max(n_lo, min(3, int(rich.power_max)))
            expr = Pow(expr, Fraction(int(rng.randint(n_lo, n_hi))))
        meta["productions"] = ["Apply", fn, "u"]
        meta["chosen_outer"] = fn
        meta["shared_inner"] = True
    elif pattern.kind == "diff_f_of_u":
        expr = _sample_f_hole(atoms, u, rich, rng)
        meta["productions"] = ["F", "u"]
        meta["shared_inner"] = True
    else:
        raise ValueError(f"unknown skeleton kind: {pattern.kind}")

    meta["inner_latex"] = render_latex(u)
    meta["inner_kind"] = _classify_inner_kind(u)
    meta["compose_layers"] = _compose_layers(expr)
    meta["cost_spend"] = _spend_breakdown(
        expr,
        richness=rich,
        pattern=pattern,
        u=u,
        atoms=atoms,
        atoms_g=atoms_g,
        nest_budget_used=nest,
    )
    return expr, meta


def sample_from_form(
    form_id: str,
    *,
    conceptual_d: float = 0.0,
    allows: Mapping[str, bool] | None = None,
    rng: random.Random | None = None,
    var: str = "x",
    derivative_order: int = 1,
    seed: int | None = None,
) -> tuple[ExprAST, ExprAST, str, str, dict[str, Any]]:
    """OpenStax form_id → pattern → filled ExprAST + derivative latex.

    Returns ``(expr, d_expr, body_latex, deriv_latex, inventory)``.
    """
    pattern = pattern_for_form(form_id)
    if pattern is None:
        raise KeyError(f"no skeleton pattern for form_id={form_id!r}")
    if rng is None:
        rng = random.Random(seed) if seed is not None else random.Random()
    allows = dict(allows or {})
    order = max(1, int(derivative_order))
    rich = richness_from_conceptual(
        conceptual_d,
        allow_roots=bool(allows.get("allow_roots")) or pattern.prefer_roots,
        derivative_order=order,
    )
    expr, meta = sample_expr_from_pattern(
        pattern, richness=rich, allows=allows, rng=rng, var=var, seed=seed
    )
    d_expr = expr
    for _ in range(order):
        d_expr = differentiate(d_expr, var)
    body = render_latex(expr, paren_style="minimal")
    deriv = render_latex(d_expr, paren_style="minimal")
    from question_engine.frameworks.primitives import poly_expression as poly_expr

    methods_hint = set(meta.pop("methods_hint", []) or [])
    inv: dict[str, Any] = {
        "core_form_id": form_id,
        "form_id": form_id,
        "skeleton_source": "expr_skeleton",
        "conceptual_difficulty": float(conceptual_d),
        "function_classes": sorted(poly_expr.function_classes_of(expr)),
        "methods_used": sorted(set(poly_expr.methods_used_of(expr)) | methods_hint),
        "chain_depth": int(poly_expr.chain_depth_of(expr)),
        "derivative_order": order,
        **meta,
    }
    if seed is not None:
        inv["rng_seed"] = int(seed)
    return expr, d_expr, body, deriv, inv
