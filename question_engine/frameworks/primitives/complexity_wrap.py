"""D-gated complexity dressing — thin adapter over ``poly_expression`` Spec sampling.

Pattern
-------
1. **Core form** = pedagogical ``form_id`` / technique (bare at low D).
2. **High D** = sample small algebraic pieces via existing ExpressionSpec packs
   (``pack_compose_algebraic``, ``pack_poly_product``, ``sample_linear_expr``,
   ``sample_scale_coef``, ``sample_expression``) and compose them with the core.
3. Callers stamp ``core_form_id`` + ``wrappers_applied`` (+ optional
   ``dressing_spec`` snapshot).
4. **Honest shortfall** — dress count is D-gated / pedagogical only. At most
   one ``constant_multiple``. If real structure still undershoots target D,
   stamp ``difficulty_shortfall`` — never invent difficulty with ``cost_pad``
   and never inflate wraps to close a cost ledger.

This module does **not** invent a parallel string-template DSL. Wrapper kind
labels below name *which Spec role* was composed; the values come from Spec.
``difficulty_costs`` is a diagnostic ledger derived from real structure —
never a generation fill target.

Skip rules (callers + ``allowed`` filters)
-----------------------------------------
* **L'Hôpital** — only scale/sign on the whole quotient (preserves indet form).
  No cancel-factor / shift that would clear 0/0 or ∞/∞.
* **Removable** — no extra cancel-factor (hole already present).
* **Jump / continuity** — no whole-prompt Spec scale (breaks ``cases`` / prose).
  Jump meets target D via **structural** upgrades (richer sides, more pieces,
  Spec-sampled poly / factored / trig / exp presentations). When real
  structure still undershoots target D, stamp ``difficulty_shortfall`` —
  never invent cost via ``cost_pad``.
* **Quotient-required derivatives** — scale/sign only; no var-substitution that
  collapses ``u/v``.
* **u-sub / trig-sub / PFD / parts** — scale/sign only when ``du`` / trig form /
  factorization must stay intact; skip shifts that break the technique.
* **Essential tan(π/2)** — no horizontal shift (approach is symbolic).
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import Any, Literal, Sequence

from question_engine.frameworks.primitives import poly_expression as pe
from question_engine.frameworks.primitives.poly_expression import (
    Add,
    Const,
    ExprAST,
    ExpressionSpec,
    Mul,
    sample_linear_expr,
    sample_scale_coef,
    spec_snapshot,
)

CoreKind = Literal["rational_pow", "trig_osc", "trig_plain"]

# Labels for Spec roles actually composed (not a free-form template menu).
WRAPPER_KINDS: tuple[str, ...] = (
    "horizontal_shift",  # Spec affine → center / var map
    "sign",  # Spec scale coef ∈ {±1} flip, or negative sample_scale_coef
    "constant_multiple",  # Spec sample_scale_coef
    "cancel_factor",  # Spec linear factor in num+den
    "unfactored_form",  # Spec product presentation of den
    "spec_product_dress",  # Mul(core, Spec poly factor) — derivatives
)

# Domains / leaves that must not receive whole-expression Spec scale dressing.
# Jump still meets target D via structural enrichment in ``limits._sample_jump``.
SKIP_DOMAINS: frozenset[str] = frozenset(
    {
        "jump",
        "piecewise_jump",
        "continuity",
        "limit_continuity",
        "ftc",
        "first_fundamental_theorem",
        "second_fundamental_theorem",
    }
)


@dataclass
class CoreExpr:
    """Bare pedagogical expression before D-gated Spec dressing.

    Used by essential-discontinuity limits where the closed answer depends on
    singularity parity / approach. Dressing mutates fields using Spec samples.
    """

    kind: CoreKind
    var: str = "x"
    coef: int = 1
    power: int = 1
    center: int = 0
    trig: str = "sin"
    approach: int | str = 0
    hole: int | None = None
    unfactored: bool = False
    # How to present a cancel_factor wrap so top/bottom factors are not identical.
    # "expand_den" | "flip_num" | "scale_unit" — set when cancel_factor is applied.
    cancel_style: str | None = None
    cancel_unit: int = 1  # scale used by scale_unit presentation
    wrappers_applied: list[str] = field(default_factory=list)
    dressing_specs: list[dict[str, Any]] = field(default_factory=list)

    @property
    def answer_sign(self) -> int:
        return 1 if self.coef >= 0 else -1


# Max structural upgrade attempts for ladders (sides / pieces), not cost-fill.
MAX_STRUCTURE_UPGRADE_ATTEMPTS = 12
# Back-compat alias (do not use for ledger chasing).
MAX_COST_FILL_ATTEMPTS = MAX_STRUCTURE_UPGRADE_ATTEMPTS
# At most one constant scale dress — never the primary high-D path.
MAX_REPEATABLE_SCALE = 1
# Structural product dress may apply twice; constant_multiple is NOT repeatable.
REPEATABLE_DRESS: frozenset[str] = frozenset({"spec_product_dress"})
# Prefer these over bare constant scale when choosing dresses.
STRUCTURAL_DRESS: frozenset[str] = frozenset(
    {
        "horizontal_shift",
        "cancel_factor",
        "unfactored_form",
        "spec_product_dress",
        "jump_side_linear",
        "jump_side_quad",
        "jump_side_cubic",
        "jump_side_factored",
        "jump_side_trig",
        "jump_side_exp",
        "jump_side_log",
        "jump_side_root",
        "jump_three_piece",
        "jump_point_value",
        "removable_expand",
        "removable_extra_factor",
    }
)


@dataclass(frozen=True)
class DressResult:
    """Result of Spec-composing a core AST (derivatives / shared)."""

    expr: ExprAST
    wrappers_applied: tuple[str, ...]
    dressing_specs: tuple[dict[str, Any], ...]
    scale: int = 1  # net constant scale applied (for answer adjust when needed)


def _linear_factor(var: str, center: int) -> str:
    if center == 0:
        return var
    if center > 0:
        return rf"({var}-{center})"
    return rf"({var}+{-center})"


def _flipped_linear_factor(var: str, center: int) -> str:
    """Rewrite ``(x-c)`` as ``-(c-x)`` / ``(c-x)`` so cancel is less glaring."""
    if center == 0:
        return rf"(-{var})"
    # (x - c) = -(c - x)
    if center > 0:
        return rf"-({center}-{var})"
    # (x + |c|) = -(-|c| - x) awkward; use (|c| + x) already standard
    return rf"-({-center}+{var})"


def _expanded_linear_product(var: str, h: int, c: int, power: int) -> str:
    """Expand ``(x-h)(x-c)^power`` for cancel presentation (power==1 common)."""
    # (x-h)(x-c) = x^2 - (h+c)x + h*c
    if power == 1:
        s = h + c
        p = h * c
        mid = f"-{s}" if s > 0 else (f"+{-s}" if s < 0 else "")
        if s == 0:
            mid = ""
        elif abs(s) == 1:
            mid = f"-{var}" if s > 0 else f"+{var}"
        else:
            mid = f"-{s}{var}" if s > 0 else f"+{-s}{var}"
        const = f"+{p}" if p > 0 else (str(p) if p < 0 else "")
        if p == 0:
            const = ""
        body = f"{var}^{{2}}{mid}{const}"
        return body
    # Higher power: keep factored den core, only expand cancel×linear once
    return rf"({_linear_factor(var, h)})({_pow_den(_linear_factor(var, c), power)})"


def _pow_den(factor: str, power: int) -> str:
    if power <= 1:
        return factor
    return rf"{factor}^{{{power}}}"


def render_core_expr(core: CoreExpr) -> str:
    """Render current (possibly dressed) core to LaTeX body (no ``\\lim``)."""
    var = core.var
    if core.kind == "trig_plain":
        body = rf"\tan({var})" if core.trig == "tan" else rf"\{core.trig}({var})"
        if abs(core.coef) == 1:
            return (r"-" if core.coef < 0 else "") + body
        return rf"{core.coef}{body}"

    if core.kind == "trig_osc":
        inner = _linear_factor(var, int(core.center))
        osc = rf"\{core.trig}\left(\frac{{1}}{{{inner}}}\right)"
        if abs(core.coef) == 1:
            return (r"-" if core.coef < 0 else "") + osc
        return rf"{core.coef}{osc}"

    c = int(core.center)
    den_core = _pow_den(_linear_factor(var, c), core.power)
    k = core.coef
    hole = core.hole

    if hole is not None and hole != c:
        hfac = _linear_factor(var, hole)
        style = core.cancel_style or "expand_den"
        # Never leave identical cancel factors top and bottom (A2-style rewrite).
        if style == "flip_num":
            flipped = _flipped_linear_factor(var, hole)
            if abs(k) == 1:
                num = flipped if k > 0 else (
                    flipped[1:] if flipped.startswith("-") else rf"-{flipped}"
                )
            else:
                num = rf"{k}{flipped}"
            return rf"\frac{{{num}}}{{{hfac}{den_core}}}"
        scale = 1
        if style == "scale_unit":
            scale = abs(int(core.cancel_unit)) if abs(int(core.cancel_unit or 1)) != 1 else 2
        num_k = k * scale
        if abs(num_k) == 1:
            num = hfac if num_k > 0 else rf"-{hfac}"
        else:
            num = rf"{num_k}{hfac}"
        if core.power == 1:
            s = scale * (hole + c)
            p = scale * hole * c
            if s == 0:
                mid = ""
            elif abs(s) == 1:
                mid = f"-{var}" if s > 0 else f"+{var}"
            else:
                mid = f"-{s}{var}" if s > 0 else f"+{-s}{var}"
            const = f"+{p}" if p > 0 else (str(p) if p < 0 else "")
            if p == 0:
                const = ""
            lead = f"{scale}" if scale != 1 else ""
            den = f"{lead}{var}^{{2}}{mid}{const}"
        else:
            den = _expanded_linear_product(var, hole, c, core.power)
            if scale != 1:
                den = rf"{scale}\left({den}\right)"
        return rf"\frac{{{num}}}{{{den}}}"

    if core.unfactored:
        fac = _linear_factor(var, c)
        if core.power == 1:
            # Avoid identical fac/fac·fac — expand den to (x-c)^2 polynomial
            # (x-c)^2 = x^2 - 2c x + c^2
            s = 2 * c
            p = c * c
            mid = f"-{s}{var}" if s > 0 else (f"+{-s}{var}" if s < 0 else "")
            if abs(s) == 1:
                mid = f"-{var}" if s > 0 else f"+{var}"
            elif s == 0:
                mid = ""
            const = f"+{p}" if p > 0 else (str(p) if p < 0 else "")
            if p == 0:
                const = ""
            den = f"{var}^{{2}}{mid}{const}"
            num = fac if abs(k) == 1 else rf"{abs(k)}{fac}"
            if k < 0:
                num = rf"-{num}"
            return rf"\frac{{{num}}}{{{den}}}"
        num = fac if abs(k) == 1 else rf"{abs(k)}{fac}"
        if k < 0:
            num = rf"-{num}"
        return rf"\frac{{{num}}}{{{fac}^{{{core.power + 1}}}}}"

    if abs(k) == 1:
        return (r"-" if k < 0 else "") + rf"\frac{{1}}{{{den_core}}}"
    return rf"\frac{{{k}}}{{{den_core}}}"


# ---------------------------------------------------------------------------
# Policy — D budget + catalog intrinsic span
# ---------------------------------------------------------------------------


def form_intrinsic_span(form: dict[str, Any] | None) -> float:
    """Width of a catalog form's own D window (missing ``d_max`` → 20)."""
    if not form:
        return 20.0
    d_min = float(form.get("d_min") or 0)
    d_max = float(form["d_max"]) if form.get("d_max") is not None else 20.0
    return max(0.0, d_max - d_min)


def form_span_is_narrow(form: dict[str, Any] | None, *, threshold: float = 8.0) -> bool:
    """True when the form itself has little internal D ladder."""
    return form_intrinsic_span(form) <= threshold


def n_wraps_for_d(
    d: float,
    rng: random.Random,
    *,
    form: dict[str, Any] | None = None,
) -> int:
    """How many Spec dresses to apply — 0 at low D; bias up when form span is narrow.

    Dress count is pedagogical / D-gated only — never inflated to close a
    cost ledger.
    """
    d = float(d)
    if d < 4:
        return 0
    narrow = form_span_is_narrow(form)
    # Always-on threshold: high D dresses even wide-span forms.
    if d >= 16:
        base = 2 if rng.random() < (0.65 if narrow else 0.45) else 1
    elif d >= 12:
        if narrow or rng.random() < 0.85:
            base = 2 if (narrow and rng.random() < 0.4) else 1
        else:
            base = 0
    elif d >= 8:
        p = 0.9 if narrow else 0.7
        base = 1 if rng.random() < p else 0
    elif d >= 4:
        p = 0.7 if narrow else 0.45
        base = 1 if rng.random() < p else 0
    else:
        base = 0
    return base


def _dress_kind_base(tag: str) -> str:
    """Strip repeat suffix from ``constant_multiple#2`` → ``constant_multiple``."""
    return str(tag).split("#", 1)[0]


def _dress_already_applied(kind: str, applied: Sequence[str]) -> bool:
    bases = {_dress_kind_base(a) for a in applied}
    return kind in bases


def _repeat_count(kind: str, applied: Sequence[str]) -> int:
    return sum(1 for a in applied if _dress_kind_base(a) == kind)


def _can_repeat_dress(kind: str, applied: Sequence[str]) -> bool:
    if kind == "constant_multiple":
        return _repeat_count(kind, applied) < MAX_REPEATABLE_SCALE
    if kind not in REPEATABLE_DRESS:
        return not _dress_already_applied(kind, applied)
    if kind == "spec_product_dress":
        return _repeat_count(kind, applied) < 2
    return not _dress_already_applied(kind, applied)


def _pick_dress_kind(candidates: Sequence[str], rng: random.Random) -> str:
    """Prefer structural Spec dresses over bare constant scale."""
    cands = list(candidates)
    if not cands:
        raise ValueError("empty dress candidates")
    structural = [k for k in cands if k in STRUCTURAL_DRESS or k == "sign"]
    if structural and "constant_multiple" in cands:
        # Only scale when no structural option remains, or rarely as accent.
        if rng.random() < 0.85:
            return rng.choice(structural)
    return rng.choice(cands)

def _next_dress_tag(kind: str, applied: Sequence[str]) -> str:
    """Unique tag for accounting; first use is bare kind, repeats get ``#n``."""
    n = sum(1 for a in applied if _dress_kind_base(a) == kind)
    return kind if n == 0 else f"{kind}#{n + 1}"


def should_apply_dressing(
    d: float,
    *,
    form: dict[str, Any] | None = None,
    domain: str | None = None,
) -> bool:
    if domain and (
        domain in SKIP_DOMAINS
        or any(domain.startswith(s) for s in ("piecewise", "continuity", "ftc"))
    ):
        return False
    return n_wraps_for_d(d, random.Random(0), form=form) > 0 or float(d) >= 4


def _dress_spec(d: float, var: str, *, coef_hi: int = 4) -> ExpressionSpec:
    """Reuse A1/PC compose pack with tight overrides for affine dressing pieces."""
    return pe.pack_compose_algebraic(
        max(0.0, min(float(d), 10.0)),
        variable=var,
        coef_hi=max(2, coef_hi),
        power_max=1,
        course_tag="calc",
        degree_max=1,
        degree_min=1,
        term_count_min=2,
        term_count_max=2,
        require_sum=True,
        require_product=False,
        max_nesting=0,
        composition_depth=0,
        forbid_product=True,
    )


def _factor_dress_spec(d: float, var: str, *, coef_hi: int = 3) -> ExpressionSpec:
    """Reuse poly-product pack for cancel / unfactored linear factors."""
    return pe.pack_poly_product(
        max(0.0, min(float(d), 12.0)),
        variable=var,
        coef_hi=max(2, coef_hi),
        power_max=1,
        special=True,
        course_tag="calc",
        degree_max=1,
        max_factors=2,
        factor_count_min=2,
        factor_count_max=2,
        max_nesting=0,
    )


def _linear_constant_term(expr: ExprAST) -> int | None:
    """If ``expr`` is ``ax+b`` (or ``x+b`` / ``b``), return integer ``b``."""
    if isinstance(expr, Const) and isinstance(expr.value, int):
        return int(expr.value)
    if isinstance(expr, Add) and len(expr.terms) == 2:
        a, b = expr.terms
        for t in (a, b):
            if isinstance(t, Const) and isinstance(t.value, int):
                return int(t.value)
    return None


def _sample_shift_center(
    rng: random.Random,
    d: float,
    var: str,
    *,
    avoid: set[int],
    abs_max: int,
) -> tuple[int, dict[str, Any]]:
    """Integer singularity/approach from Spec linear sample (not a hardcoded pool)."""
    spec = _dress_spec(d, var, coef_hi=min(5, max(2, abs_max)))
    snap = spec_snapshot(spec)
    for _ in range(10):
        lin = sample_linear_expr(spec, rng)
        b = _linear_constant_term(lin)
        if b is None:
            # Fall back: Spec scale coef as center magnitude
            c = sample_scale_coef(spec, rng)
        else:
            # ax+b with approach at root ≈ −b when a=1 → center −b for (x−c)
            c = -int(b)
        if c == 0:
            c = sample_scale_coef(replace(spec, allow_negative_coefs=True), rng)
        if c in avoid:
            continue
        if abs(c) > abs_max:
            c = max(-abs_max, min(abs_max, c))
            if c == 0 or c in avoid:
                continue
        return int(c), snap
    # Last resort: Spec coef with avoid filter
    for _ in range(12):
        c = sample_scale_coef(spec, rng)
        if c not in avoid and c != 0 and abs(c) <= abs_max:
            return int(c), snap
    pool = [i for i in range(-abs_max, abs_max + 1) if i != 0 and i not in avoid]
    return (rng.choice(pool) if pool else 2), snap


# ---------------------------------------------------------------------------
# CoreExpr path (essential limits) — Spec-backed field updates
# ---------------------------------------------------------------------------


def complexity_wrap(
    expr: CoreExpr,
    d: float,
    rng: random.Random,
    *,
    allowed: Sequence[str] | None = None,
    approach_abs_max: int = 5,
    form: dict[str, Any] | None = None,
) -> CoreExpr:
    """Apply Spec-sampled dresses; returns new ``CoreExpr`` (kind preserved).

    Natural D-gated dress budget. Prefers structural wraps over constant scale.
    Does **not** invent cost_pad or inflate wrap count to close a ledger gap —
    callers stamp ``difficulty_shortfall`` when under.
    """
    allow = set(allowed) if allowed is not None else set(WRAPPER_KINDS)
    # Essential path does not use AST product dress
    allow.discard("spec_product_dress")
    core = replace(
        expr,
        wrappers_applied=list(expr.wrappers_applied),
        dressing_specs=list(expr.dressing_specs),
    )
    n = n_wraps_for_d(float(d), rng, form=form)
    if n <= 0:
        return core
    n = min(n, max(1, len(allow)))

    var = core.var
    for _ in range(n):
        candidates: list[str] = []
        if "sign" in allow and _can_repeat_dress("sign", core.wrappers_applied):
            candidates.append("sign")
        if "constant_multiple" in allow and _can_repeat_dress(
            "constant_multiple", core.wrappers_applied
        ):
            if abs(core.coef) == 1 or _dress_already_applied(
                "constant_multiple", core.wrappers_applied
            ):
                candidates.append("constant_multiple")
        if (
            "horizontal_shift" in allow
            and _can_repeat_dress("horizontal_shift", core.wrappers_applied)
            and core.kind in {"rational_pow", "trig_osc"}
            and not isinstance(core.approach, str)
        ):
            candidates.append("horizontal_shift")
        if (
            "cancel_factor" in allow
            and _can_repeat_dress("cancel_factor", core.wrappers_applied)
            and core.kind == "rational_pow"
            and core.hole is None
        ):
            candidates.append("cancel_factor")
        if (
            "unfactored_form" in allow
            and _can_repeat_dress("unfactored_form", core.wrappers_applied)
            and core.kind == "rational_pow"
            and not core.unfactored
            and core.hole is None
        ):
            candidates.append("unfactored_form")

        if not candidates:
            break
        kind = _pick_dress_kind(candidates, rng)
        tag = _next_dress_tag(kind, core.wrappers_applied)
        if kind == "sign":
            spec = _dress_spec(d, var)
            m = sample_scale_coef(replace(spec, allow_negative_coefs=True), rng)
            core.coef = -abs(int(core.coef)) if m < 0 else -int(core.coef)
            if core.coef > 0:
                core.coef = -core.coef
            core.wrappers_applied.append(tag)
            core.dressing_specs.append(spec_snapshot(spec))
        elif kind == "constant_multiple":
            spec = _dress_spec(d, var, coef_hi=4)
            m = sample_scale_coef(spec, rng)
            while abs(m) == 1:
                m = sample_scale_coef(spec, rng)
            new_coef = int(core.coef) * int(m)
            # Keep classroom-sized coefs — single scale only (no stack to 3456).
            if abs(new_coef) > 12:
                new_coef = int((1 if new_coef > 0 else -1) * abs(int(m)))
            core.coef = new_coef
            core.wrappers_applied.append(tag)
            core.dressing_specs.append(spec_snapshot(spec))
        elif kind == "horizontal_shift":
            avoid = {int(core.center)}
            if core.hole is not None:
                avoid.add(int(core.hole))
            new_c, snap = _sample_shift_center(
                rng, d, var, avoid=avoid, abs_max=approach_abs_max
            )
            core.center = new_c
            core.approach = new_c
            core.wrappers_applied.append(tag)
            core.dressing_specs.append(snap)
        elif kind == "cancel_factor":
            avoid = {int(core.center)}
            hole, snap = _sample_shift_center(
                rng, d, var, avoid=avoid, abs_max=approach_abs_max
            )
            core.hole = hole
            core.cancel_style = rng.choice(["expand_den", "flip_num", "scale_unit"])
            if core.cancel_style == "scale_unit":
                core.cancel_unit = int(rng.choice([2, 3, 4]))
            core.wrappers_applied.append(tag)
            core.dressing_specs.append(snap)
        elif kind == "unfactored_form":
            # Presentation role — Spec product pack stamps the dressing snapshot
            spec = _factor_dress_spec(d, var)
            core.unfactored = True
            core.wrappers_applied.append(tag)
            core.dressing_specs.append(spec_snapshot(spec))

    return core


def wrap_meta(core: CoreExpr, *, core_form_id: str) -> dict[str, Any]:
    """Metadata stamp: pedagogical id + Spec dresses actually applied."""
    meta: dict[str, Any] = {
        "core_form_id": core_form_id,
        "wrappers_applied": list(core.wrappers_applied),
        "wrap_kind": core.kind,
        "wrap_center": core.center,
        "wrap_coef": core.coef,
    }
    if core.dressing_specs:
        meta["dressing_spec"] = core.dressing_specs[-1]
        meta["dressing_specs"] = list(core.dressing_specs)
    return meta


# ---------------------------------------------------------------------------
# ExprAST path (derivatives) — compose Spec pieces onto sampled cores
# ---------------------------------------------------------------------------


def allowed_wraps_for_derivative(
    *,
    form_id: str = "",
    require_quotient: bool = False,
) -> tuple[str, ...]:
    """Technique-safe wraps for derivatives.

    ``spec_product_dress`` is only allowed on forms that already teach the
    product rule — multiplying a bare power/trig core by ``(ax+b)`` would
    swap the pedagogical technique.
    """
    if require_quotient:
        return ("sign", "constant_multiple")
    fid = form_id or ""
    if fid.startswith("product") or "_product" in fid or fid.endswith("_product"):
        return ("sign", "constant_multiple", "spec_product_dress")
    return ("sign", "constant_multiple")


def dress_derivative_ast(
    expr: ExprAST,
    d: float,
    rng: random.Random,
    *,
    var: str = "x",
    form: dict[str, Any] | None = None,
    form_id: str = "",
    allowed: Sequence[str] | None = None,
    require_quotient: bool = False,
) -> DressResult | None:
    """Compose Spec-sampled scale / product factors onto a derivative core AST.

    Skip var-substitution when ``require_quotient`` (would break u/v structure).
    Returns ``None`` when budget is 0 (caller keeps bare core).

    Natural D-gated dress only — prefers ``spec_product_dress`` over bare scale.
    Does not inflate wraps to close a cost gap; callers stamp shortfall.
    """
    fid = form_id or str((form or {}).get("form_id") or "")
    if allowed is not None:
        allow = set(allowed)
    else:
        allow = set(
            allowed_wraps_for_derivative(
                form_id=fid, require_quotient=require_quotient
            )
        )
    if require_quotient:
        allow &= {"sign", "constant_multiple"}
    n = n_wraps_for_d(float(d), rng, form=form)
    if n <= 0:
        return None
    n = min(n, max(1, len(allow)))

    out = expr
    applied: list[str] = []
    snaps: list[dict[str, Any]] = []
    net_scale = 1
    extra_factors: list[ExprAST] = []

    for _ in range(n):
        candidates = []
        for k in ("sign", "constant_multiple", "spec_product_dress"):
            if k not in allow:
                continue
            if _can_repeat_dress(k, applied):
                candidates.append(k)
        if not candidates:
            break
        kind = _pick_dress_kind(candidates, rng)
        tag = _next_dress_tag(kind, applied)
        if kind == "sign":
            spec = _dress_spec(d, var)
            net_scale *= -1
            applied.append(tag)
            snaps.append(spec_snapshot(spec))
        elif kind == "constant_multiple":
            spec = _dress_spec(d, var, coef_hi=4)
            m = sample_scale_coef(spec, rng)
            while abs(m) == 1:
                m = sample_scale_coef(spec, rng)
            net_scale *= int(m)
            applied.append(tag)
            snaps.append(spec_snapshot(spec))
        elif kind == "spec_product_dress":
            spec = _dress_spec(d, var, coef_hi=3)
            factor = sample_linear_expr(spec, rng)
            extra_factors.append(factor)
            applied.append(tag)
            snaps.append(spec_snapshot(spec))

    if not applied:
        return None
    for fac in extra_factors:
        out = Mul((fac, out))
    if net_scale != 1:
        out = Mul((Const(int(net_scale)), out))
    return DressResult(
        expr=out,
        wrappers_applied=tuple(applied),
        dressing_specs=tuple(snaps),
        scale=net_scale,
    )


def dress_meta(
    *,
    core_form_id: str,
    wrappers_applied: Sequence[str],
    dressing_specs: Sequence[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    meta: dict[str, Any] = {
        "core_form_id": core_form_id,
        "wrappers_applied": list(wrappers_applied),
    }
    if dressing_specs:
        meta["dressing_spec"] = dressing_specs[-1]
        meta["dressing_specs"] = list(dressing_specs)
    return meta


# ---------------------------------------------------------------------------
# Integral / limit latex helpers — Spec scale only (technique-safe)
# ---------------------------------------------------------------------------


def sample_safe_scale(
    d: float,
    rng: random.Random,
    *,
    var: str = "x",
) -> tuple[int, dict[str, Any]]:
    """Spec-sampled nonzero scale for technique-preserving const dress."""
    spec = _dress_spec(d, var, coef_hi=4)
    m = sample_scale_coef(spec, rng)
    while abs(m) == 1 and float(d) >= 8:
        m = sample_scale_coef(spec, rng)
        if abs(m) != 1:
            break
    if abs(m) == 1:
        # Mid D may still pick ±1 as "sign"
        m = -1 if rng.random() < 0.5 else sample_scale_coef(
            replace(spec, allow_negative_coefs=False), rng
        )
        if abs(m) == 1:
            m = rng.choice([2, 3, -2, -3])
    return int(m), spec_snapshot(spec)


_INT_BODY_RE = re.compile(r"^-?\d+$")
_FRAC_INT_RE = re.compile(r"^\\frac\{(-?\d+)\}\{(-?\d+)\}$")
_LEADING_INT_RE = re.compile(r"^(\d+)((?:\\|[A-Za-z\(]).*)$")


def _has_top_level_addsub(body: str) -> bool:
    """True when ``+``/``-`` appears outside ``{...}`` (not a unary leading minus)."""
    depth = 0
    for i, ch in enumerate(body):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        elif depth == 0 and ch in "+-" and i > 0:
            return True
    return False


def scale_latex_body(body: str, scale: int) -> str:
    """Prefix a latex body with a constant multiple (paren if needed).

    Absorbs an existing leading unary minus into ``scale`` so we never emit
    ``-4-\\frac{...}`` or ``--42x`` style juxtaposition bugs.

    Critical: never concatenate a scale onto a leading digit (``-2`` + ``2`` →
    ``-22``). Pure integers multiply; sums/differences are parenthesized;
    leading numeric coefficients are absorbed when safe.
    """
    body = (body or "").strip()
    if not body or scale == 1:
        return body
    while body.startswith("-"):
        scale = -scale
        body = body[1:].lstrip()
    if not body:
        return body
    if scale == 1:
        return body

    # Pure integer → multiply numerically
    if _INT_BODY_RE.match(body):
        return str(int(body) * scale)

    # Bare integer fraction → multiply via Fraction
    m_frac = _FRAC_INT_RE.match(body)
    if m_frac:
        val = Fraction(int(m_frac.group(1)), int(m_frac.group(2))) * scale
        if val.denominator == 1:
            return str(val.numerator)
        sign = "-" if val < 0 else ""
        return rf"{sign}\frac{{{abs(val.numerator)}}}{{{val.denominator}}}"

    # Absorb leading integer coefficient: 2\sqrt{x} * 3 → 6\sqrt{x}
    m_lead = _LEADING_INT_RE.match(body)
    if m_lead and not _has_top_level_addsub(body):
        new_coef = int(m_lead.group(1)) * scale
        rest = m_lead.group(2)
        if new_coef == 1:
            return rest
        if new_coef == -1:
            return rf"-{rest}"
        return rf"{new_coef}{rest}"

    needs_group = _has_top_level_addsub(body)
    if scale == -1:
        if needs_group:
            return rf"-\left({body}\right)"
        return rf"-{body}"

    if needs_group:
        return rf"{scale}\left({body}\right)"
    # Leading digit that we couldn't absorb (rare) — force explicit product
    if body[0].isdigit():
        return rf"{scale}\cdot {body}"
    # Fractions / trig / grouped: juxtapose the integer
    return rf"{scale}{body}"


def split_lim_prompt(prompt: str) -> tuple[str, str] | None:
    """Split ``\\lim_{...} BODY`` on the balanced subscript brace (not rfind)."""
    key = r"\lim_"
    i = prompt.find(key)
    if i < 0:
        return None
    j = i + len(key)
    if j >= len(prompt) or prompt[j] != "{":
        return None
    depth = 0
    k = j
    while k < len(prompt):
        ch = prompt[k]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                k += 1
                break
        k += 1
    else:
        return None
    head = prompt[:k]
    body = prompt[k:].lstrip()
    if not body:
        return None
    return head + " ", body


def scale_answer_latex(answer: str, scale: int) -> str:
    """Scale a simple answer latex by an integer (best-effort).

    Indefinite integrals: strip trailing ``+C``, scale the antiderivative body
    (parenthesizing sums so every term is scaled), then restore ``+C``.
    """
    if scale == 1 or not answer:
        return answer
    # Preserve +C
    plus_c = ""
    body = answer
    if answer.endswith("+C"):
        plus_c = "+C"
        body = answer[: -len("+C")].rstrip()
    elif answer.endswith("+ C"):
        plus_c = "+C"
        body = answer[: -len("+ C")].rstrip()
    if body in {r"\text{DNE}", r"\infty", r"-\infty"}:
        if body == r"\text{DNE}":
            return body
        if scale < 0:
            return r"-\infty" if body == r"\infty" else r"\infty"
        return body
    scaled = scale_latex_body(body, scale)
    return scaled + plus_c if plus_c else scaled


# ---------------------------------------------------------------------------
# Difficulty cost accounting (heuristic; relates to effective D / effort)
# ---------------------------------------------------------------------------

# Dress wrapper kind → incremental D cost
DRESS_FEATURE_COSTS: dict[str, float] = {
    "sign": 0.5,
    "constant_multiple": 1.5,
    "horizontal_shift": 2.0,
    "cancel_factor": 2.5,
    "unfactored_form": 1.5,
    "spec_product_dress": 3.0,
    # Jump structural upgrades (real piecewise complexity, not whole-prompt scale).
    "jump_side_linear": 2.0,
    "jump_side_quad": 3.0,
    "jump_side_cubic": 4.0,
    "jump_side_factored": 2.5,
    "jump_side_trig": 3.5,
    "jump_side_exp": 3.5,
    "jump_side_log": 3.5,
    "jump_side_root": 3.0,
    "jump_three_piece": 4.0,
    "jump_point_value": 1.5,
    # Removable structural upgrades (expanded / extra non-identical factors).
    "removable_expand": 2.0,
    "removable_extra_factor": 3.0,
}

# Spec upgrade / method / flag → incremental D cost
SPEC_FEATURE_COSTS: dict[str, float] = {
    "allow_trig": 1.5,
    "allow_exp": 1.5,
    "allow_log": 1.5,
    "allow_roots": 1.0,
    "allow_invtrig": 2.0,
    "use_product": 2.0,
    "use_quotient": 2.5,
    "use_chain": 2.0,
    "use_roots": 1.0,
    "chain_depth_2": 1.5,
    "fn_power": 1.5,
    "product": 2.0,
    "quotient": 2.5,
    "chain": 2.0,
    "mix_classes": 1.5,
    "class_trig": 1.5,
    "class_exp": 1.5,
    "class_log": 1.5,
    "lhopital_twice": 4.0,
}

# form_id prefix / exact → base cost when catalog d_min missing
_FORM_BASE_COST_EXACT: dict[str, float] = {
    "poly_direct": 0.0,
    "power_poly": 0.0,
    "product_two_poly": 0.0,
    "quotient_poly": 0.0,
    "trig_basic": 0.0,
    "exp_basic": 0.0,
    "ln_basic": 0.0,
    "sqrt_x": 1.0,
    "one_over_sqrt_x": 1.5,
    "ln_alone": 2.0,
    "arctan_alone": 3.0,
    "arcsin_alone": 3.0,
    "poly_sum": 0.5,
    "neg_power": 2.0,
    "rewrite_over_x": 3.0,
    "essential_1_over_x": 3.0,
    "essential_1_over_x_sq": 4.0,
    "essential_sin_1_over_x": 4.0,
    "essential_cos_1_over_x": 4.0,
    "essential_tan_asymptote": 5.0,
    "essential_rational_va": 4.0,
    # Bare const||const jump — D=0 basics stay near zero (catalog d_min=0).
    "piecewise_jump": 0.0,
    "piecewise_jump_const": 0.0,
    "piecewise_jump_linear": 6.0,
    "piecewise_jump_poly": 10.0,
    "continuity_classify": 0.0,
    "continuity_classify_continuous": 0.0,
    "continuity_classify_removable": 0.0,
    "continuity_classify_jump": 0.0,
    "continuity_classify_essential": 0.0,
}

_FORM_BASE_COST_PREFIX: tuple[tuple[str, float], ...] = (
    ("lhopital_multipass", 10.0),
    ("lhopital_0_0", 4.0),
    ("lhopital_inf", 8.0),
    ("lhopital_1_inf", 9.0),
    ("lhopital_0_inf", 8.0),
    ("lhopital_", 6.0),
    ("removable_", 3.0),
    ("essential_", 4.0),
    ("indet_", 6.0),
    ("power_", 1.0),
    ("chain_", 4.0),
    ("product_", 5.0),
    ("quotient_", 6.0),
    ("trig_", 3.0),
    ("u_sub", 5.0),
    ("cyclic_", 8.0),
    ("poly1_", 4.0),
    ("poly2_", 6.0),
    ("basic_", 1.0),
    ("direct_", 2.0),
    ("inf_", 5.0),
    ("piecewise", 6.0),
)

# Always-omit structural noise (present on almost every derivative sample).
_BASELINE_METHOD_FEATURES: frozenset[str] = frozenset({"power", "sum"})


def form_base_cost(
    form_id: str,
    catalog_form: dict[str, Any] | None = None,
) -> float:
    """Base difficulty cost of a pedagogical form_id.

    Exact basic forms (``power_poly``, ``quotient_poly``, …) stay at 0 so
    ``difficulty: 0`` reports near-zero totals. Specialty / prefixed forms keep
    heuristic floors; catalog ``d_min`` is preferred for basics.
    """
    fid = str(form_id or "")
    heur = 0.0
    if fid in _FORM_BASE_COST_EXACT:
        heur = _FORM_BASE_COST_EXACT[fid]
    else:
        for prefix, cost in _FORM_BASE_COST_PREFIX:
            if fid.startswith(prefix):
                heur = cost
                break
        else:
            heur = 2.0 if fid else 0.0
    if catalog_form is not None and catalog_form.get("d_min") is not None:
        d_min = float(catalog_form["d_min"])
        if fid in _FORM_BASE_COST_EXACT and _FORM_BASE_COST_EXACT[fid] == 0.0:
            return d_min
        return max(d_min, heur)
    return heur


def build_difficulty_costs(
    *,
    form_id: str | None = None,
    catalog_form: dict[str, Any] | None = None,
    wrappers_applied: Sequence[str] | None = None,
    upgrades: Sequence[str] | None = None,
    methods_used: Sequence[str] | None = None,
    function_classes: Sequence[str] | None = None,
    effort_features: dict[str, Any] | None = None,
    spec_snapshot: dict[str, Any] | None = None,
    baseline_features: Sequence[str] | None = None,
) -> tuple[list[dict[str, Any]], float]:
    """Build ``difficulty_costs`` rows and their total.

    Each row: ``{source, feature, cost}`` with
    ``source ∈ {"form", "dress", "spec"}``.

    Total is a heuristic sum for gallery transparency. Leaf-required methods
    (``baseline_features`` / ``_BASELINE_METHOD_FEATURES``) are omitted so D=0
    basics stay near zero. When filling toward a target D, overshoot is OK —
    callers require ``total >= target``, not equality.
    """
    costs: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    baseline = set(baseline_features or ()) | set(_BASELINE_METHOD_FEATURES)

    def _add(source: str, feature: str, cost: float) -> None:
        key = (source, feature)
        if not feature or key in seen:
            return
        if feature in baseline or _dress_kind_base(feature) in baseline:
            return
        seen.add(key)
        costs.append(
            {"source": source, "feature": str(feature), "cost": float(cost)}
        )

    fid = str(
        form_id
        or (catalog_form or {}).get("form_id")
        or (effort_features or {}).get("form")
        or ""
    )
    if fid:
        _add("form", fid, form_base_cost(fid, catalog_form))

    for w in wrappers_applied or ():
        w_s = str(w)
        base = _dress_kind_base(w_s)
        # Gallery-friendly alias for constant scale dress; keep #n for repeats
        suffix = w_s[len(base) :] if w_s.startswith(base) else ""
        if base == "constant_multiple":
            feat = f"spec_scale{suffix}"
        elif base == "sign":
            feat = f"spec_sign{suffix}"
        else:
            feat = w_s
        _add("dress", feat, DRESS_FEATURE_COSTS.get(base, 1.0))

    for u in upgrades or ():
        u_s = str(u)
        if u_s in SPEC_FEATURE_COSTS:
            _add("spec", u_s, SPEC_FEATURE_COSTS[u_s])

    for m in methods_used or ():
        m_s = str(m)
        if m_s in SPEC_FEATURE_COSTS:
            _add("spec", m_s, SPEC_FEATURE_COSTS[m_s])

    for cls in function_classes or ():
        c_s = str(cls)
        flag = {
            "trig": "allow_trig",
            "exp": "allow_exp",
            "log": "allow_log",
            "invtrig": "allow_invtrig",
            "root": "allow_roots",
            "roots": "allow_roots",
        }.get(c_s)
        if flag and flag in SPEC_FEATURE_COSTS:
            _add("spec", flag, SPEC_FEATURE_COSTS[flag])

    # Spec snapshot allow_* only when not already covered by function_classes /
    # upgrades — avoids double-counting leaf-default allows on every sample.
    snap = spec_snapshot or {}
    for flag in (
        "allow_trig",
        "allow_exp",
        "allow_log",
        "allow_roots",
        "allow_invtrig",
    ):
        if snap.get(flag) and ("spec", flag) not in seen:
            # Only stamp if the problem actually used a matching class, or the
            # upgrade was purchased (already handled). Skip bare leaf defaults.
            pass

    ef = effort_features or {}
    lh_steps = int(ef.get("lhopital_steps") or 0)
    if lh_steps >= 2:
        _add("spec", "lhopital_twice", SPEC_FEATURE_COSTS["lhopital_twice"])
    elif lh_steps == 1 and ("spec", "lhopital_twice") not in seen:
        _add("spec", "lhopital_steps", 3.0)

    nest = int(ef.get("nest_depth") or ef.get("nest") or 0)
    if nest >= 2:
        _add("spec", "nest_depth", 1.0 * nest)

    total = float(sum(float(c["cost"]) for c in costs))
    return costs, total


def stamp_difficulty_costs(
    meta: dict[str, Any],
    *,
    catalog_form: dict[str, Any] | None = None,
    upgrades: Sequence[str] | None = None,
    baseline_features: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Write ``difficulty_costs`` / ``difficulty_cost_total`` onto sample meta.

    ``baseline_features`` should list leaf-required methods/upgrades (e.g.
    ``use_quotient`` on the quotient leaf) so D=0 totals stay near zero.
    """
    costs, total = build_difficulty_costs(
        form_id=str(
            meta.get("core_form_id")
            or meta.get("form_id")
            or meta.get("openstax_form")
            or meta.get("family")
            or ""
        ),
        catalog_form=catalog_form,
        wrappers_applied=meta.get("wrappers_applied") or [],
        upgrades=upgrades
        if upgrades is not None
        else list(meta.get("upgrades") or []),
        methods_used=meta.get("methods_used")
        or (meta.get("effort_features") or {}).get("methods")
        or [],
        function_classes=meta.get("function_classes") or [],
        effort_features=meta.get("effort_features")
        if isinstance(meta.get("effort_features"), dict)
        else None,
        spec_snapshot=meta.get("spec_snapshot")
        if isinstance(meta.get("spec_snapshot"), dict)
        else None,
        baseline_features=baseline_features,
    )
    meta["difficulty_costs"] = costs
    meta["difficulty_cost_total"] = total
    return meta


def record_difficulty_shortfall(
    meta: dict[str, Any],
    target_d: float,
    *,
    catalog_form: dict[str, Any] | None = None,
    upgrades: Sequence[str] | None = None,
    baseline_features: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Stamp honest ``difficulty_shortfall`` when real cost is under target.

    Never invents difficulty via ``cost_pad``. Leaves ``difficulty_cost_total``
    as the sum of real form / dress / Spec rows only.
    """
    stamp_difficulty_costs(
        meta,
        catalog_form=catalog_form,
        upgrades=upgrades,
        baseline_features=baseline_features,
    )
    # Strip any legacy cost_pad rows if present in older callers / snapshots.
    wraps = [w for w in (meta.get("wrappers_applied") or []) if w != "cost_pad"]
    meta["wrappers_applied"] = wraps
    costs = [
        c
        for c in (meta.get("difficulty_costs") or [])
        if c.get("feature") != "cost_pad"
    ]
    total = float(sum(float(c["cost"]) for c in costs))
    meta["difficulty_costs"] = costs
    meta["difficulty_cost_total"] = total
    gap = float(target_d) - total
    if gap > 1e-9 and float(target_d) >= 4.0:
        meta["difficulty_shortfall"] = float(gap)
    else:
        meta.pop("difficulty_shortfall", None)
    return meta


def allowed_wraps_for_limit(
    *,
    form: str,
    form_id: str = "",
    technique: str = "",
) -> tuple[str, ...]:
    """Technique-safe wrap allow-list for post-sample limit dressing."""
    fid = form_id or form
    if form in SKIP_DOMAINS or fid.startswith("piecewise") or form == "continuity":
        return ()
    if "lhopital" in fid or technique == "lhopital" or form.startswith("indet_"):
        return ("sign", "constant_multiple")
    if form.startswith("removable") or fid.startswith("removable"):
        # Structure comes from in-sampler expand / extra-factor — no scale dress.
        return ()
    if form in {"essential"} or fid.startswith("essential"):
        # Handled in-sampler via CoreExpr
        return ()
    if "inf" in form or fid.startswith("inf_"):
        return ("sign", "constant_multiple")
    # Direct eval — scale/sign only (shift would need answer recompute)
    return ("sign", "constant_multiple")


def allowed_wraps_for_integral(
    *,
    technique: str,
    tricks: Sequence[str],
    form_id: str = "",
) -> tuple[str, ...]:
    """Technique-safe wraps for integrals — prefer Spec scale only."""
    tricks_l = {str(t) for t in tricks}
    if technique in SKIP_DOMAINS or "ftc" in technique:
        return ()
    # Trig-sub / PFD factorization / multi-trick: scale only
    if "trig_sub" in tricks_l or technique == "trig_sub":
        return ("sign", "constant_multiple")
    if "pfd" in tricks_l or "parts" in tricks_l:
        return ("sign", "constant_multiple")
    if "u_sub" in tricks_l:
        # Outer const is fine; shift would break du match
        return ("sign", "constant_multiple")
    if form_id.startswith("u_sub") or "substitution" in technique:
        return ("sign", "constant_multiple")
    return ("sign", "constant_multiple")
