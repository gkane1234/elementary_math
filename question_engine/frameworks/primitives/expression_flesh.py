"""Expression flesher: Spec effort rewrites a fixed conceptual skeleton.

Pipeline
--------
1. **Conceptual skeleton (topic)** — fixed goal form + answer from undressed core.
2. **Expression flesher** (this module) — catalog of value-preserving /
   simplify-to-core moves, gated by Spec budget + ``allow_*`` + leaf safety.

This is **not** an Algebra-1-only catalogue. It fleshes any topic's skeleton so
the student sees a different presentation with the **same answer after
simplify**. Under the hood it may reuse constructive / ``poly_compose`` /
presentation helpers — that is an implementation detail, not the product name.

Conceptual difficulty owns **skeleton richness** (OpenStax pattern + hole fill
in ``expr_skeleton``). Spec difficulty only spends this identity-extra catalog.
Dummy ``+k-k`` / naked cancel-quot are demoted (weight 0).

Public entry points: ``flesh_from_skeleton``, ``n_dress_layers``.

Honest limitations
------------------
* Equivalence is by construction (cancel pairs, identity wraps, poly inflate);
  we do not CAS-prove every sample.
* Technique-critical leaves restrict moves (jump, FTC, L'Hôpital, …).
* ``constant_multiple`` / bare sign flip are **not** Spec levers here (they
  change the answer).
* Poly inflate only applies to parseable pure-poly latex islands; otherwise
  that catalog slot is skipped (honest shortfall, not densify).
* Trig identity wraps are stubbed for later — not implemented.
"""

from __future__ import annotations

import re
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, Mapping, Sequence

# ---------------------------------------------------------------------------
# Catalog registry — plug new moves here (trig identities later, etc.)
# ---------------------------------------------------------------------------


ApplyFn = Callable[
    ["FleshApplyCtx"],
    str | None,
]


@dataclass(frozen=True)
class FleshMove:
    """One value-preserving presentation move in the flesher catalog."""

    move_id: str
    detail: str
    kind: str = "effort"  # effort | prereq
    requires_allows: frozenset[str] = frozenset()
    max_once: bool = False
    # Soft weight when picking among eligible moves (higher = more often).
    weight: float = 1.0


@dataclass
class FleshApplyCtx:
    body: str
    var: str
    rng: random.Random
    allows: Mapping[str, bool]
    spec_d: float


def _allow_on(allows: Mapping[str, bool], key: str) -> bool:
    return bool(allows.get(key))


# --- Move implementations -------------------------------------------------


def _needs_group(body: str) -> bool:
    body = (body or "").strip()
    if not body:
        return False
    depth = 0
    for i, ch in enumerate(body):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        elif depth == 0 and ch in "+-" and i > 0:
            return True
        elif depth == 0 and ch in "*/":
            return True
    return False


def _paren(body: str) -> str:
    body = (body or "").strip()
    if not body:
        return body
    if body.startswith(r"\left(") and body.endswith(r"\right)"):
        return body
    if _needs_group(body) or body.startswith("-"):
        return rf"\left({body}\right)"
    return body


def _linear_fac(var: str, a: int) -> str:
    if a == 0:
        return var
    if a > 0:
        return rf"{var}-{a}"
    return rf"{var}+{-a}"


def _apply_cancel_quot_bait(ctx: FleshApplyCtx) -> str | None:
    """Write body as a canceling quotient (same after simplify)."""
    body, var, rng = ctx.body, ctx.var, ctx.rng
    a = int(rng.choice([1, 2, 3, -1, -2, -3]))
    fac = _linear_fac(var, a)
    core = _paren(body)
    style = rng.choice(["plain", "flip_den", "scale_unit"])
    if style == "flip_den" and a != 0:
        if a > 0:
            den = rf"-\left({a}-{var}\right)"
            num = rf"-\left({a}-{var}\right){core}"
        else:
            den = rf"-\left({-a}+{var}\right)"
            num = rf"-\left({-a}+{var}\right){core}"
        return rf"\frac{{{num}}}{{{den}}}"
    if style == "scale_unit":
        u = int(rng.choice([2, 3, 4]))
        num = rf"{u}\left({fac}\right){core}"
        den = rf"{u}\left({fac}\right)"
        return rf"\frac{{{num}}}{{{den}}}"
    num = rf"\left({fac}\right){core}"
    return rf"\frac{{{num}}}{{{fac}}}"


def _apply_add_cancel_const(ctx: FleshApplyCtx) -> str | None:
    k = int(ctx.rng.choice([1, 2, 3, 4, 5, 6]))
    core = _paren(ctx.body)
    if ctx.rng.random() < 0.5:
        return rf"{core}+{k}-{k}"
    return rf"\left({core}+{k}\right)-{k}"


def _apply_add_cancel_linear(ctx: FleshApplyCtx) -> str | None:
    a = int(ctx.rng.choice([1, 2, 3, -1, -2]))
    b = int(ctx.rng.choice([0, 1, 2, 3, -1, -2]))
    var = ctx.var
    if a == 1:
        lin = var if b == 0 else (rf"{var}+{b}" if b > 0 else rf"{var}-{abs(b)}")
    elif a == -1:
        lin = rf"-{var}" if b == 0 else (
            rf"-{var}+{b}" if b > 0 else rf"-{var}-{abs(b)}"
        )
    else:
        lin = rf"{a}{var}" if b == 0 else (
            rf"{a}{var}+{b}" if b > 0 else rf"{a}{var}-{abs(b)}"
        )
    core = _paren(ctx.body)
    if ctx.rng.random() < 0.5:
        return rf"{core}+\left({lin}\right)-\left({lin}\right)"
    return rf"\left({core}+\left({lin}\right)\right)-\left({lin}\right)"


def _apply_double_neg(ctx: FleshApplyCtx) -> str | None:
    return rf"-\left(-{_paren(ctx.body)}\right)"


def _apply_exp_ln_id(ctx: FleshApplyCtx) -> str | None:
    """e^{\\ln(body)} ≡ body (requires allow_exp + allow_log)."""
    if not (_allow_on(ctx.allows, "allow_exp") and _allow_on(ctx.allows, "allow_log")):
        return None
    return rf"e^{{\ln\left({_paren(ctx.body)}\right)}}"


def _apply_ln_exp_id(ctx: FleshApplyCtx) -> str | None:
    """\\ln(e^{body}) ≡ body (requires allow_exp + allow_log)."""
    if not (_allow_on(ctx.allows, "allow_exp") and _allow_on(ctx.allows, "allow_log")):
        return None
    return rf"\ln\left(e^{{{_paren(ctx.body)}}}\right)"


# --- Pure-poly island parse + compose_inflate bridge ----------------------

_MONO_RE = re.compile(
    r"""
    ^\s*
    (?P<sign>[+-]?)
    \s*
    (?:
        (?P<coef>\d+)?\s*
        (?:
            (?P<var>[A-Za-z]|\\[A-Za-z]+)
            (?:\^\{(?P<pbrace>-?\d+)\}|\^(?P<pplain>-?\d+))?
        )?
        |
        (?P<const>\d+)
    )
    \s*$
    """,
    re.VERBOSE,
)


def _strip_outer_left_right(body: str) -> str:
    s = (body or "").strip()
    while s.startswith(r"\left(") and s.endswith(r"\right)"):
        inner = s[len(r"\left(") : -len(r"\right)")].strip()
        if not inner:
            break
        s = inner
    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1].strip()
    return s


def try_parse_pure_poly_latex(body: str, var: str) -> dict[int, Fraction] | None:
    """Parse a narrow class of univariate poly latex → coeffs, or None.

    Accepts sums of monomials like ``2x^{3}+x-4``. Rejects fractions, functions,
    nested parens, products of sums — those are not pure poly islands.
    """
    s = _strip_outer_left_right(body)
    if not s:
        return None
    # Hard reject exotic tokens.
    banned = (
        r"\frac",
        r"\sin",
        r"\cos",
        r"\tan",
        r"\ln",
        r"\log",
        r"\sqrt",
        r"\left",
        r"\right",
        "e^",
        "(",
        ")",
        "/",
        "*",
        r"\cdot",
    )
    if any(tok in s for tok in banned):
        return None

    # Split on top-level + / - keeping signs.
    parts: list[str] = []
    cur = ""
    for i, ch in enumerate(s):
        if ch in "+-" and i > 0 and cur:
            parts.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        parts.append(cur)
    if not parts:
        return None

    coeffs: dict[int, Fraction] = {}
    var_plain = var.lstrip("\\")
    var_cmds = {var, var_plain, rf"\{var_plain}"}

    for part in parts:
        m = _MONO_RE.match(part.strip())
        if not m:
            return None
        sign = -1 if m.group("sign") == "-" else 1
        if m.group("const") is not None and m.group("var") is None:
            deg = 0
            coef = Fraction(int(m.group("const"))) * sign
        elif m.group("var") is None and m.group("coef") is not None:
            # Bare integer matched as coef without var (e.g. ``-1``).
            deg = 0
            coef = Fraction(int(m.group("coef"))) * sign
        else:
            v = m.group("var")
            if v is None:
                return None
            if v not in var_cmds and v.lstrip("\\") != var_plain:
                return None
            p_raw = m.group("pbrace") or m.group("pplain")
            deg = int(p_raw) if p_raw is not None else 1
            c_raw = m.group("coef")
            coef = Fraction(int(c_raw) if c_raw else 1) * sign
        coeffs[deg] = coeffs.get(deg, Fraction(0)) + coef
        if coeffs[deg] == 0:
            del coeffs[deg]
    return coeffs or {0: Fraction(0)}


def _apply_poly_inflate(ctx: FleshApplyCtx) -> str | None:
    """Extract pure poly island → compose_inflate → splice (same expanded value)."""
    coeffs = try_parse_pure_poly_latex(ctx.body, ctx.var)
    if coeffs is None:
        return None
    # Skip trivial constants — inflate noise without pedagogy.
    if set(coeffs.keys()) <= {0}:
        return None
    try:
        from question_engine.frameworks.difficulty_budget import allocate_budget
        from question_engine.frameworks.primitives.poly_compose import (
            compose_inflate,
            render_node,
            tree_from_target,
        )
        from question_engine.frameworks.primitives.presentation import (
            PresentationStyle,
        )
        from question_engine.frameworks.primitives.registry import (
            PRIM_NUMBERS,
            PRIM_VARIABLE,
            PrimitiveContext,
        )
        from question_engine.frameworks.primitives.variables import SampledVariable
    except Exception:
        return None

    budget = 1 if float(ctx.spec_d) < 16 else (2 if float(ctx.spec_d) < 28 else 3)
    plan = allocate_budget(
        max(4.0, float(ctx.spec_d)),
        [PRIM_NUMBERS, PRIM_VARIABLE],
        rng=ctx.rng,
    )
    prim_ctx = PrimitiveContext(
        topic_d=float(ctx.spec_d),
        plan=plan,
        rng=ctx.rng,
    )
    var_obj = SampledVariable(
        name=ctx.var.lstrip("\\") or "x",
        effective_d=float(ctx.spec_d),
        cost=0.0,
        locked=True,
    )
    root = tree_from_target(coeffs)
    try:
        root, _tags, _depths = compose_inflate(
            prim_ctx,
            root,
            budget=budget,
            var=var_obj,
            prefer_distribute=True,
        )
        latex, _text = render_node(
            root, var_obj, PresentationStyle.schoolbook(), ctx.rng
        )
    except Exception:
        return None
    latex = (latex or "").strip()
    if not latex or latex == ctx.body.strip():
        return None
    return latex


# Registry: move_id → (FleshMove meta, apply fn)
_APPLY: dict[str, ApplyFn] = {
    "cancel_quot_bait": _apply_cancel_quot_bait,
    "add_cancel_const": _apply_add_cancel_const,
    "add_cancel_linear": _apply_add_cancel_linear,
    "double_neg": _apply_double_neg,
    "exp_ln_id": _apply_exp_ln_id,
    "ln_exp_id": _apply_ln_exp_id,
    "poly_inflate": _apply_poly_inflate,
}

FLESH_CATALOG: dict[str, FleshMove] = {
    "cancel_quot_bait": FleshMove(
        "cancel_quot_bait",
        "cancel common factor (same after simplify)",
        kind="prereq",
        max_once=True,
        weight=0.0,  # demoted: naked bait too obvious for Spec
    ),
    "add_cancel_const": FleshMove(
        "add_cancel_const",
        "add/subtract canceling constant (demoted — too weak alone)",
        weight=0.0,
    ),
    "add_cancel_linear": FleshMove(
        "add_cancel_linear",
        "add/subtract canceling linear (demoted — too weak alone)",
        weight=0.0,
    ),
    "double_neg": FleshMove(
        "double_neg",
        "double negation (same after simplify)",
        max_once=True,
        weight=0.9,
    ),
    "exp_ln_id": FleshMove(
        "exp_ln_id",
        r"e^{\ln(·)} identity wrap",
        kind="prereq",
        requires_allows=frozenset({"allow_exp", "allow_log"}),
        max_once=True,
        weight=1.2,
    ),
    "ln_exp_id": FleshMove(
        "ln_exp_id",
        r"\ln(e^{·}) identity wrap",
        kind="prereq",
        requires_allows=frozenset({"allow_exp", "allow_log"}),
        max_once=True,
        weight=1.2,
    ),
    "poly_inflate": FleshMove(
        "poly_inflate",
        "poly-core compose inflate (pure poly islands only)",
        max_once=True,
        weight=1.3,
    ),
    # Stub slots — registered so callers / docs see intent; apply returns None.
    "trig_pythag_id": FleshMove(
        "trig_pythag_id",
        "trig Pythagorean identity wrap (stub — not implemented)",
        requires_allows=frozenset({"allow_trig"}),
        max_once=True,
        weight=0.0,
    ),
}

# Default Spec pool: identity / poly-island extras (not dummy ±cancel).
CORE_FLESH_MOVES: tuple[str, ...] = (
    "double_neg",
    "exp_ln_id",
    "ln_exp_id",
    "poly_inflate",
)

# Back-compat alias used by older structure_moves / tests.
PRESERVE_MOVES: tuple[str, ...] = CORE_FLESH_MOVES


def n_dress_layers(spec_d: float) -> int:
    """How many expression-flesh layers for Spec difficulty budget."""
    d = max(0.0, float(spec_d))
    if d < 1.0:
        return 0
    if d < 4.0:
        return 1 if d >= 2.0 else 0
    if d < 8.0:
        return 1
    if d < 16.0:
        return 2
    if d < 28.0:
        return 3
    return min(5, 3 + int((d - 28) // 20))


# Alias kept for older imports / gallery copy.
n_presentation_layers = n_dress_layers


def safe_moves_for_leaf(leaf: str | None) -> tuple[str, ...]:
    """Restrict fleshes that would break technique-critical structure."""
    leaf = (leaf or "").strip()
    skip_quot = {
        "limit_jump",
        "limit_continuity",
        "lhopitals_rule",
        "first_fundamental_theorem",
        "second_fundamental_theorem",
    }
    base = list(CORE_FLESH_MOVES)
    if leaf in skip_quot or "jump" in leaf or "continuity" in leaf or "lhopital" in leaf:
        return tuple(
            m
            for m in base
            if m
            not in {
                "cancel_quot_bait",
                # Identity wraps can also wreck piecewise / FTC display structure.
                "exp_ln_id",
                "ln_exp_id",
            }
        )
    return tuple(base)


def eligible_moves(
    *,
    leaf: str | None = None,
    allowed: Sequence[str] | None = None,
    allows: Mapping[str, bool] | None = None,
) -> list[str]:
    """Catalog ids that pass leaf safety + allow_* gates."""
    allows = allows or {}
    pool = list(allowed) if allowed is not None else list(safe_moves_for_leaf(leaf))
    out: list[str] = []
    for mid in pool:
        meta = FLESH_CATALOG.get(mid)
        if meta is None:
            continue
        if meta.weight <= 0:
            continue  # stubs
        if meta.requires_allows and not all(
            _allow_on(allows, k) for k in meta.requires_allows
        ):
            continue
        if mid not in _APPLY:
            continue
        out.append(mid)
    return out


def _move_base(tag: str) -> str:
    return str(tag).split("#", 1)[0]


def _weighted_pick(rng: random.Random, ids: Sequence[str]) -> str:
    weights = [float(FLESH_CATALOG[i].weight) for i in ids]
    total = sum(weights) or 1.0
    r = rng.random() * total
    acc = 0.0
    for mid, w in zip(ids, weights):
        acc += w
        if r <= acc:
            return mid
    return ids[-1]


def flesh_from_skeleton(
    body: str,
    spec_d: float,
    rng: random.Random,
    *,
    var: str = "x",
    leaf: str | None = None,
    allowed: Sequence[str] | None = None,
    allows: Mapping[str, bool] | None = None,
) -> tuple[str, list[str]]:
    """Rewrite ``body`` with Spec flesh layers; simplified value unchanged.

    Returns ``(fleshed_latex, wrapper_tags)``. Empty wraps when Spec≈0 or no
    safe move applies. Callers must keep the **undressed** calculus answer.
    """
    body = (body or "").strip()
    if not body:
        return body, []
    n = n_dress_layers(spec_d)
    if n <= 0:
        return body, []

    pool = eligible_moves(leaf=leaf, allowed=allowed, allows=allows)
    if not pool:
        return body, []

    out = body
    applied: list[str] = []
    for i in range(n):
        unused = [
            m
            for m in pool
            if m not in {_move_base(t) for t in applied}
            or not FLESH_CATALOG[m].max_once
        ]
        # Prefer unused; allow repeats of non-max_once at high Spec.
        choices = unused or [
            m for m in pool if not FLESH_CATALOG[m].max_once
        ] or pool
        move = _weighted_pick(rng, choices)
        meta = FLESH_CATALOG[move]
        if meta.max_once and any(_move_base(t) == move for t in applied):
            alt = [m for m in choices if m != move]
            if not alt:
                break
            move = _weighted_pick(rng, alt)

        ctx = FleshApplyCtx(
            body=out,
            var=var,
            rng=rng,
            allows=allows or {},
            spec_d=float(spec_d),
        )
        apply = _APPLY.get(move)
        if apply is None:
            continue
        new_body = apply(ctx)
        if new_body is None or new_body.strip() == out.strip():
            # Honest skip — try a different move once.
            alt = [m for m in choices if m != move]
            if not alt:
                continue
            move = _weighted_pick(rng, alt)
            apply = _APPLY.get(move)
            if apply is None:
                continue
            ctx = FleshApplyCtx(
                body=out,
                var=var,
                rng=rng,
                allows=allows or {},
                spec_d=float(spec_d),
            )
            new_body = apply(ctx)
            if new_body is None or new_body.strip() == out.strip():
                continue
        out = new_body
        tag = move if move not in {_move_base(t) for t in applied} else f"{move}#{i + 1}"
        applied.append(tag)
    return out, applied


# Back-compat names (thin aliases — prefer flesh_from_skeleton in new code).
dress_body_preserving_answer = flesh_from_skeleton
dress_display_preserving = flesh_from_skeleton


def stamp_flesh_sources(wrappers: Sequence[str]) -> list[dict[str, str]]:
    """Difficulty sources for expression-flesh wraps."""
    out: list[dict[str, str]] = []
    for w in wrappers:
        base = _move_base(w)
        meta = FLESH_CATALOG.get(base)
        out.append(
            {
                "kind": meta.kind if meta else "effort",
                "tag": base,
                "detail": meta.detail if meta else "expression flesh",
            }
        )
    return out


# Back-compat
stamp_presentation_sources = stamp_flesh_sources


def flesh_meta(
    *,
    undressed_body: str,
    wrappers: Sequence[str],
    answer_preserved: bool = True,
) -> dict[str, Any]:
    return {
        "undressed_body_latex": undressed_body,
        "wrappers_applied": list(wrappers),
        "spec_answer_preserved": bool(answer_preserved),
        "expression_flesh": True,
        # Legacy flag for older meta readers / galleries.
        "spec_presentation": True,
    }


presentation_meta = flesh_meta


def catalog_move_ids(*, include_stubs: bool = False) -> list[str]:
    """List registered move ids (for docs / tests)."""
    out = []
    for mid, meta in FLESH_CATALOG.items():
        if meta.weight <= 0 and not include_stubs:
            continue
        out.append(mid)
    return out
