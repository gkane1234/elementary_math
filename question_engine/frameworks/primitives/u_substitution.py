"""Shared u-substitution integrand sampler (Calc 1).

Pattern
-------
1. Pick inner ``u = g(x)`` under ``USubSpec`` constraints.
2. Pick outer antiderivative shape ``F(u)`` (power / ln / exp / invtrig / …).
3. Emit integrand ``F'(g(x)) · g'(x)`` so u-sub is forced and solvable
   by construction.

OpenStax-inspired shapes (Vol. 1 §5.5 / Vol. 2 §1.5):
  - ``e^{cos x} sin x``  (u=cos x)
  - ``(ln g) · g'/g`` via outer ln after u=g, or directly ∫ g'/g
  - ``sin(u) u'``, ``sec²(u) u'``, poly powers with matching chain factor
  - composite: ``e^{sin x} cos x``, ``1/(1+(ln x)²) · (1/x)``

Packs/topics pass different ``USubSpec`` knobs; multi-trick wraps a
PFD-rational in ``u`` by choosing ``g`` whose ``g'`` appears as a factor.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import Any, Literal, Sequence

from question_engine.generators.utils import (
    format_linear_latex,
    frac_latex,
    random_int_range,
)

InnerClass = Literal["poly", "trig", "exp", "log", "invtrig", "composite"]
OuterClass = Literal["power", "exp", "ln", "trig", "invtrig"]

DEFAULT_INNERS: frozenset[str] = frozenset({"poly", "trig", "exp", "log"})
DEFAULT_OUTERS: frozenset[str] = frozenset({"power", "exp", "ln", "trig"})


@dataclass
class USubSpec:
    """Constraints for sampling one u-sub integrand."""

    variable: str = "x"
    d_spend: float = 6.0
    coef_abs_max: int = 5
    degree_max: int = 4
    include_plus_c: bool = True

    # What g(x) may be
    u_inner_allowed: frozenset[str] = DEFAULT_INNERS
    # What F(u) / outer antiderivative class may be
    u_outer_allowed: frozenset[str] = DEFAULT_OUTERS

    allow_trig_inner: bool = True
    allow_exp_inner: bool = True
    allow_log_inner: bool = True
    allow_poly_inner: bool = True
    allow_invtrig_inner: bool = False
    allow_composite_inner: bool = True  # e.g. cos as inner of exp outer

    require_du_factor: bool = True  # always emit visible g'
    prefer_composite: bool = False  # bias e^{trig}·trig'
    pack: str = "u_sub_general"

    def snapshot(self) -> dict[str, Any]:
        return {
            "pack": self.pack,
            "variable": self.variable,
            "d_spend": self.d_spend,
            "coef_abs_max": self.coef_abs_max,
            "degree_max": self.degree_max,
            "u_inner_allowed": sorted(self.u_inner_allowed),
            "u_outer_allowed": sorted(self.u_outer_allowed),
            "allow_trig_inner": self.allow_trig_inner,
            "allow_exp_inner": self.allow_exp_inner,
            "allow_log_inner": self.allow_log_inner,
            "allow_poly_inner": self.allow_poly_inner,
            "allow_invtrig_inner": self.allow_invtrig_inner,
            "allow_composite_inner": self.allow_composite_inner,
            "require_du_factor": self.require_du_factor,
            "prefer_composite": self.prefer_composite,
        }


@dataclass(frozen=True)
class USubSample:
    prompt_latex: str
    answer_latex: str
    u_latex: str
    du_latex: str
    outer_family: str
    inner_family: str
    metadata: dict[str, Any] = field(default_factory=dict)


def _coef(rng: random.Random, hi: int, *, exclude_zero: bool = True) -> int:
    excl = {0} if exclude_zero else set()
    return random_int_range(-hi, hi, exclude=excl) if hi > 0 else (1 if exclude_zero else 0)


def _plus_c(body: str, *, include: bool) -> str:
    return rf"{body}+C" if include else body


def _resolved_inners(spec: USubSpec) -> list[str]:
    allowed = set(spec.u_inner_allowed)
    if not spec.allow_trig_inner:
        allowed.discard("trig")
    if not spec.allow_exp_inner:
        allowed.discard("exp")
    if not spec.allow_log_inner:
        allowed.discard("log")
    if not spec.allow_poly_inner:
        allowed.discard("poly")
    if not spec.allow_invtrig_inner:
        allowed.discard("invtrig")
    if not spec.allow_composite_inner:
        allowed.discard("composite")
    return sorted(allowed) or ["poly"]


def _resolved_outers(spec: USubSpec) -> list[str]:
    return sorted(spec.u_outer_allowed) or ["power"]


# ---------------------------------------------------------------------------
# Pack constructors (topic → Spec)
# ---------------------------------------------------------------------------


def pack_u_sub_power(d: float, **kw: Any) -> USubSpec:
    """Algebraic u-sub: poly / quadratic inners, power outers."""
    return USubSpec(
        d_spend=d,
        u_inner_allowed=frozenset({"poly"}),
        u_outer_allowed=frozenset({"power"}),
        allow_trig_inner=False,
        allow_exp_inner=False,
        allow_log_inner=False,
        allow_poly_inner=True,
        allow_composite_inner=False,
        prefer_composite=False,
        pack="u_sub_power",
        **{k: v for k, v in kw.items() if k in USubSpec.__dataclass_fields__},
    )


def pack_u_sub_ln_exp(d: float, **kw: Any) -> USubSpec:
    """Log/exp substitution — OpenStax e^{cos}sin, ln-chain, etc."""
    rich = d >= 6.0
    inners = {"poly", "trig", "exp", "log"} if rich else {"poly", "exp", "log"}
    outers = {"exp", "ln", "power"} if d < 8 else {"exp", "ln", "power", "trig"}
    base = dict(
        d_spend=d,
        u_inner_allowed=frozenset(inners),
        u_outer_allowed=frozenset(outers),
        allow_trig_inner=rich,
        allow_exp_inner=True,
        allow_log_inner=True,
        allow_poly_inner=True,
        allow_composite_inner=rich,
        prefer_composite=d >= 8.0,
        pack="u_sub_ln_exp",
    )
    base.update({k: v for k, v in kw.items() if k in USubSpec.__dataclass_fields__})
    return USubSpec(**base)


def pack_u_sub_trig(d: float, **kw: Any) -> USubSpec:
    return USubSpec(
        d_spend=d,
        u_inner_allowed=frozenset({"trig", "poly"}),
        u_outer_allowed=frozenset({"trig", "power", "exp"}),
        allow_trig_inner=True,
        allow_exp_inner=False,
        allow_log_inner=False,
        prefer_composite=d >= 6,
        allow_composite_inner=True,
        pack="u_sub_trig",
        **{k: v for k, v in kw.items() if k in USubSpec.__dataclass_fields__},
    )


def pack_u_sub_invtrig(d: float, **kw: Any) -> USubSpec:
    return USubSpec(
        d_spend=d,
        u_inner_allowed=frozenset({"poly"}),
        u_outer_allowed=frozenset({"invtrig", "power"}),
        allow_trig_inner=False,
        allow_exp_inner=False,
        allow_log_inner=False,
        allow_invtrig_inner=False,
        allow_composite_inner=False,
        pack="u_sub_invtrig",
        **{k: v for k, v in kw.items() if k in USubSpec.__dataclass_fields__},
    )


def pack_u_sub_for_pfd_wrap(d: float, **kw: Any) -> USubSpec:
    """Inner g for multi-trick: u=e^x / sin / cos / ln / ax+b — du must appear."""
    return USubSpec(
        d_spend=d,
        u_inner_allowed=frozenset({"exp", "trig", "log", "poly"}),
        u_outer_allowed=frozenset({"power"}),  # outer unused; wrap supplies rational
        allow_trig_inner=True,
        allow_exp_inner=True,
        allow_log_inner=True,
        allow_poly_inner=True,
        allow_composite_inner=False,
        prefer_composite=False,
        pack="u_sub_pfd_wrap",
        **{k: v for k, v in kw.items() if k in USubSpec.__dataclass_fields__},
    )


def pack_u_sub_general(d: float, **kw: Any) -> USubSpec:
    return USubSpec(
        d_spend=d,
        prefer_composite=d >= 8,
        allow_composite_inner=d >= 6,
        pack="u_sub_general",
        **{k: v for k, v in kw.items() if k in USubSpec.__dataclass_fields__},
    )


# ---------------------------------------------------------------------------
# Inner g(x) + g'(x)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _Inner:
    family: str
    u_latex: str
    du_factor_latex: str  # multiplies F'(u) in the integrand
    answer_u: str  # how to write F(u) back — usually u_latex
    classes: tuple[str, ...]


def _sample_inner(spec: USubSpec, rng: random.Random) -> _Inner:
    var = spec.variable
    hi = max(1, spec.coef_abs_max)
    pool = _resolved_inners(spec)
    # Composite bias: pick trig inner when composite preferred
    if spec.prefer_composite and "trig" in pool and rng.random() < 0.65:
        kind = "trig"
    else:
        kind = rng.choice(pool)

    if kind == "trig":
        fn = rng.choice(["sin", "cos", "tan"] if spec.d_spend >= 10 else ["sin", "cos"])
        k = rng.randint(1, max(1, min(4, hi)))
        arg = format_linear_latex(k, 0, variable=var) if k != 1 else var
        if k == 1:
            arg = var
        else:
            arg = f"{k}{var}"
        u = rf"\{fn}({arg})" if fn != "tan" else rf"\tan({arg})"
        # d/dx sin(kx)=k cos(kx); cos→−k sin; tan→k sec²
        if fn == "sin":
            du = rf"\cos({arg})" if k == 1 else rf"{k}\cos({arg})"
        elif fn == "cos":
            du = rf"-\sin({arg})" if k == 1 else rf"-{k}\sin({arg})"
        else:
            du = rf"\sec^{{2}}({arg})" if k == 1 else rf"{k}\sec^{{2}}({arg})"
        return _Inner("trig_" + fn, u, du, u, ("trig",))

    if kind == "exp":
        k = rng.randint(1, max(1, min(4, hi)))
        arg = var if k == 1 else f"{k}{var}"
        u = rf"e^{{{arg}}}"
        du = u if k == 1 else rf"{k}e^{{{arg}}}"
        return _Inner("exp", u, du, u, ("exp",))

    if kind == "log":
        a = rng.randint(1, max(1, min(3, hi)))
        b = _coef(rng, hi, exclude_zero=False)
        # Need ax+b > 0 region; use a>0
        inner = format_linear_latex(a, b, variable=var)
        u = rf"\ln|{inner}|"
        du = rf"\frac{{{a}}}{{{inner}}}"
        return _Inner("log", u, du, u, ("log",))

    if kind == "invtrig":
        u = rf"\arctan({var})"
        du = rf"\frac{{1}}{{1+{var}^{{2}}}}"
        return _Inner("invtrig", u, du, u, ("invtrig",))

    # poly: linear or quadratic
    if spec.d_spend >= 8 and rng.random() < 0.4:
        # u = x² + c
        c = rng.randint(1, max(1, hi))
        u = rf"{var}^{{2}}+{c}"
        du = rf"2{var}"
        return _Inner("poly_quad", u, du, rf"\left({u}\right)", ("algebraic",))
    a = rng.randint(1, max(1, min(4, hi)))
    b = _coef(rng, hi, exclude_zero=False)
    if a == 1 and b == 0:
        a = 2
    u = format_linear_latex(a, b, variable=var)
    du = str(a)
    return _Inner("poly_linear", u, du, rf"\left({u}\right)", ("algebraic",))


# ---------------------------------------------------------------------------
# Outer F and F' · du
# ---------------------------------------------------------------------------


def _sample_outer_on_inner(
    spec: USubSpec, rng: random.Random, inner: _Inner
) -> tuple[str, str, str, list[str]]:
    """Return (integrand_without_int, antideriv_body, outer_family, classes)."""
    outers = _resolved_outers(spec)
    # Composite OpenStax hits: e^{trig} · trig'
    if (
        spec.allow_composite_inner
        and (spec.prefer_composite or spec.d_spend >= 6)
        and inner.family.startswith("trig_")
        and "exp" in outers
        and rng.random() < (0.7 if spec.prefer_composite else 0.35)
    ):
        # ∫ e^{sin/cos} · (matching du) — if du is -sin for u=cos, still OK
        integrand = rf"e^{{{inner.u_latex}}}{inner.du_factor_latex}"
        # Clean: e^{cos x}(-sin x) → write e^{cos x}sin x with sign absorbed in answer
        if inner.du_factor_latex.startswith("-"):
            # du = -k sin → integrand e^u (-k sin) ; prefer ∫ e^{cos} sin with answer -e^{cos}
            pos_du = inner.du_factor_latex[1:]
            integrand = rf"e^{{{inner.u_latex}}}{pos_du}"
            answer = _plus_c(rf"-e^{{{inner.u_latex}}}", include=spec.include_plus_c)
        else:
            answer = _plus_c(rf"e^{{{inner.u_latex}}}", include=spec.include_plus_c)
        return integrand, answer, "exp_of_trig", ["exp", "trig"]

    # ln(g)·(g'/g) style via outer power of ln, or classic g'/g
    if (
        "ln" in outers
        and inner.family in {"poly_linear", "poly_quad", "trig_sin", "trig_cos", "exp"}
        and rng.random() < 0.25
        and spec.d_spend >= 8
    ):
        # ∫ ln(u)/u · u' wait — for u=inner, ∫ ln(u) (u'/u) = ∫ ln(u)/u du = (ln u)²/2
        # u'/u · ln(u) = du/u · ln(u)
        if inner.family.startswith("trig"):
            # skip awkward
            pass
        else:
            integrand = (
                rf"\frac{{{inner.du_factor_latex}}}{{{inner.u_latex}}}"
                rf"\ln|{inner.u_latex}|"
            )
            answer = _plus_c(
                rf"\frac{{1}}{{2}}\left(\ln|{inner.u_latex}|\right)^{{2}}",
                include=spec.include_plus_c,
            )
            return integrand, answer, "ln_squared_chain", ["log"]

    kind = rng.choice(outers)

    if kind == "exp" or (
        kind != "ln" and "exp" in outers and inner.family.startswith("trig_") and rng.random() < 0.4
    ):
        integrand = rf"e^{{{inner.u_latex}}}{inner.du_factor_latex}"
        if inner.du_factor_latex.startswith("-"):
            integrand = rf"e^{{{inner.u_latex}}}{inner.du_factor_latex[1:]}"
            answer = _plus_c(rf"-e^{{{inner.u_latex}}}", include=spec.include_plus_c)
        else:
            answer = _plus_c(rf"e^{{{inner.u_latex}}}", include=spec.include_plus_c)
        return integrand, answer, "exp_chain", ["exp", *inner.classes]

    if kind == "ln":
        # ∫ (1/u) u' = ln|u|
        integrand = rf"\frac{{{inner.du_factor_latex}}}{{{inner.u_latex}}}"
        answer = _plus_c(rf"\ln|{inner.u_latex}|", include=spec.include_plus_c)
        return integrand, answer, "du_over_u", ["log", *inner.classes]

    if kind == "trig":
        fn = rng.choice(["sin", "cos"])
        if fn == "sin":
            integrand = rf"\cos({inner.u_latex}){inner.du_factor_latex}"
            answer = _plus_c(rf"\sin({inner.u_latex})", include=spec.include_plus_c)
        else:
            integrand = rf"\sin({inner.u_latex}){inner.du_factor_latex}"
            answer = _plus_c(rf"-\cos({inner.u_latex})", include=spec.include_plus_c)
        # Fix double-negative / juxtaposition for poly du factors
        if inner.du_factor_latex.startswith("-") and fn == "sin":
            integrand = rf"\sin({inner.u_latex}){inner.du_factor_latex}"
        return integrand, answer, "trig_of_u", ["trig", *inner.classes]

    if kind == "invtrig":
        # ∫ 1/(1+u²) u' = arctan(u)
        integrand = (
            rf"\frac{{{inner.du_factor_latex}}}{{1+({inner.u_latex})^{{2}}}}"
        )
        answer = _plus_c(rf"\arctan({inner.u_latex})", include=spec.include_plus_c)
        return integrand, answer, "arctan_chain", ["invtrig", *inner.classes]

    # power: ∫ u^n u'
    n = rng.randint(2, max(2, min(5, spec.degree_max)))
    if inner.family == "poly_linear" and inner.du_factor_latex.isdigit():
        a = int(inner.du_factor_latex)
        # Prefer visible a(ax+b)^n
        if rng.random() < 0.55:
            integrand = rf"{a}\left({inner.u_latex}\right)^{{{n}}}"
            answer = _plus_c(
                rf"\frac{{1}}{{{n + 1}}}\left({inner.u_latex}\right)^{{{n + 1}}}",
                include=spec.include_plus_c,
            )
            return integrand, answer, "linear_power_with_du", ["algebraic"]
        integrand = rf"\left({inner.u_latex}\right)^{{{n}}}"
        answer = _plus_c(
            rf"\frac{{1}}{{{a * (n + 1)}}}\left({inner.u_latex}\right)^{{{n + 1}}}",
            include=spec.include_plus_c,
        )
        return integrand, answer, "linear_power", ["algebraic"]

    integrand = rf"\left({inner.u_latex}\right)^{{{n}}}{inner.du_factor_latex}"
    answer = _plus_c(
        rf"\frac{{1}}{{{n + 1}}}\left({inner.u_latex}\right)^{{{n + 1}}}",
        include=spec.include_plus_c,
    )
    return integrand, answer, "power_chain", list(inner.classes) or ["algebraic"]


def sample_u_sub(
    spec: USubSpec,
    *,
    rng: random.Random | None = None,
) -> USubSample:
    """Sample ∫ F'(g(x)) g'(x) dx under ``spec`` constraints."""
    rng = rng or random.Random()
    inner = _sample_inner(spec, rng)
    body, answer, outer_fam, classes = _sample_outer_on_inner(spec, rng, inner)
    var = spec.variable
    prompt = rf"\int {body}\,d{var}"
    meta = {
        "construction": "shared_u_sub",
        "u_sub_spec": spec.snapshot(),
        "u_latex": inner.u_latex,
        "du_factor": inner.du_factor_latex,
        "outer_family": outer_fam,
        "inner_family": inner.family,
        "family": f"{outer_fam}__{inner.family}",
        "function_classes": sorted(set(classes)),
        "tricks_required": ["u_sub"],
        "nest": 1 + (1 if "trig" in inner.family and "exp" in outer_fam else 0),
    }
    return USubSample(
        prompt_latex=prompt,
        answer_latex=answer,
        u_latex=inner.u_latex,
        du_latex=inner.du_factor_latex,
        outer_family=outer_fam,
        inner_family=inner.family,
        metadata=meta,
    )


def sample_u_inner_only(
    spec: USubSpec,
    *,
    rng: random.Random | None = None,
    prefer: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Sample only ``u=g(x)`` + ``du`` for multi-trick wraps (PFD in u)."""
    rng = rng or random.Random()
    if prefer:
        narrowed = [p for p in prefer if p in _resolved_inners(spec)]
        if narrowed:
            spec = replace(
                spec,
                u_inner_allowed=frozenset(narrowed),
                prefer_composite=False,
            )
    inner = _sample_inner(spec, rng)
    return {
        "family": inner.family,
        "u_latex": inner.u_latex,
        "du_factor_latex": inner.du_factor_latex,
        "answer_u": inner.answer_u,
        "classes": list(inner.classes),
        "u_sub_spec": spec.snapshot(),
    }


def usub_spec_from_integral_flavor(
    flavor: str,
    *,
    d: float,
    variable: str = "x",
    coef_abs_max: int = 5,
    degree_max: int = 4,
    include_plus_c: bool = True,
) -> USubSpec:
    """Map integral leaf flavor → constraint pack."""
    kw = dict(
        variable=variable,
        coef_abs_max=coef_abs_max,
        degree_max=degree_max,
        include_plus_c=include_plus_c,
    )
    if flavor in {"ln_exp", "log_exp"}:
        return pack_u_sub_ln_exp(d, **kw)
    if flavor == "invtrig":
        return pack_u_sub_invtrig(d, **kw)
    if flavor == "trig":
        return pack_u_sub_trig(d, **kw)
    if flavor in {"power", "algebraic"}:
        return pack_u_sub_power(d, **kw)
    if flavor == "pfd_wrap":
        return pack_u_sub_for_pfd_wrap(d, **kw)
    return pack_u_sub_general(d, **kw)
