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

# Diff AST latex uses integer-valued Fraction exponents, so d/dx[x^2] can
# render as 2x^{1}. Reverse-chain strips that; chain-rule leaves keep it.
_UNIT_EXPONENT = "^{1}"

InnerClass = Literal["poly", "trig", "exp", "log", "invtrig", "composite"]
OuterClass = Literal["power", "exp", "ln", "trig", "invtrig"]

DEFAULT_INNERS: frozenset[str] = frozenset({"poly", "trig", "exp", "log"})
DEFAULT_OUTERS: frozenset[str] = frozenset({"power", "exp", "ln", "trig"})

# Teacher-facing families from ``u_substitution.json`` (OpenStax Vol 1 §5.5–5.7).
# Values are catalog ``form_id`` sets; ``auto`` / ``None`` = D-weighted catalog mix.
U_SUB_FORM_PRESETS: dict[str, frozenset[str] | None] = {
    "auto": None,
    "power_linear": frozenset({"power_linear_du"}),
    "power_quadratic": frozenset({"power_quad_x_du", "root_quad_x_du"}),
    "power_cubic": frozenset({"power_cubic_x2_du"}),
    "du_over_u": frozenset({"du_over_u_linear", "du_over_u_trig"}),
    "exp_chain": frozenset(
        {
            "exp_of_poly",
            "exp_of_trig",
            "nested_trig_exp",
            "exp_of_cubic",
            "exp_of_quartic",
            "exp_over_power_of_exp",
            "exp_of_sqrt",
        }
    ),
    "trig_chain": frozenset(
        {
            "trig_of_linear",
            "sec2_of_u",
            "du_over_u_trig",
            "composite_ln_of_trig",
            "trig_over_linear_trig_power",
        }
    ),
    "arctan_chain": frozenset({"arctan_of_linear", "arctan_of_ln"}),
    "ln_power_chain": frozenset(
        {"ln_squared_chain", "ln_power_over_x", "power_of_one_plus_ln"}
    ),
    "alteration": frozenset({"alteration_linear_over_root"}),
    "challenging": frozenset(
        {
            "alteration_linear_over_root",
            "nested_trig_exp",
            "ln_squared_chain",
            "arctan_of_linear",
            "sec2_of_u",
            "root_quad_x_du",
            "power_cubic_x2_du",
            "exp_of_cubic",
            "exp_of_quartic",
            "exp_root_chain",
            "exp_power_of_exp",
            "composite_ln_of_trig",
        }
    ),
    # Calc BC drill bank §1 (not OpenStax). Mid/high D; D=0 auto stays easy.
    "bc_bank": frozenset(
        {
            "power_quad_neg",
            "power_cubic_neg",
            "root_quad_minus",
            "power_quad_m3_2",
            "ln_power_over_x",
            "power_of_one_plus_ln",
            "exp_over_power_of_exp",
            "exp_e2x_over_power",
            "trig_over_linear_trig_power",
            "ln_ln_nested",
            "ln_over_x_sqrt",
            "arctan_of_ln",
            "du_over_u_quadratic",
            "du_over_ln_of_poly",
            "cos_of_ln_over_x",
            "sin_of_sqrt",
            "exp_of_sqrt",
            "root_ln_of_linear",
            "ln_sq_over_root_ln_cube",
            "power_hex_neg",
            "root_of_x4",
        }
    ),
}

U_SUB_FORM_PRESET_OPTIONS: tuple[str, ...] = tuple(U_SUB_FORM_PRESETS.keys())

# Diff ``FORM_PATTERNS`` ids that reverse to honest Calc-1 u-sub (F(g), integrand F'g').
_REVERSE_CHAIN_FORMS: dict[str, tuple[tuple[int, tuple[str, ...]], ...]] = {
    "power": (
        (0, ("chain_power_linear",)),
    ),
    "ln_exp": (
        (0, ("exp_basic", "ln_basic")),
        (2, ("exp_basic", "ln_basic", "chain_nested")),
        (3, ("chain_nested", "exp_basic", "ln_basic")),
    ),
    "trig": (
        (0, ("chain_trig_poly", "trig_basic")),
        (2, ("chain_trig_poly", "chain_nested", "trig_basic")),
        (3, ("chain_nested", "chain_trig_poly")),
    ),
    "invtrig": (
        (0, ("invtrig_arctan",)),
        (2, ("invtrig_arctan", "invtrig_arcsin")),
    ),
}


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


def resolve_u_sub_form_preset(name: str | None) -> frozenset[str] | None:
    """Return catalog form_ids for a named preset, or None for auto."""
    key = str(name or "auto").strip().lower()
    if key in {"", "none", "auto"}:
        return None
    if key not in U_SUB_FORM_PRESETS:
        return None
    return U_SUB_FORM_PRESETS[key]


def _elide_unit_exponents(tex: str) -> str:
    """Drop a trailing integer exponent 1 (``x^{1}`` → ``x``).

    ``^{10}`` / ``^{12}`` are left alone because they are not the substring
    ``^{1}`` (the ``1`` is not followed by ``}``).
    """
    return tex.replace(_UNIT_EXPONENT, "")


def _reverse_chain_form_ids(flavor: str, format_tier: int) -> tuple[str, ...]:
    table = _REVERSE_CHAIN_FORMS.get(flavor) or _REVERSE_CHAIN_FORMS["power"]
    chosen: tuple[str, ...] = table[0][1]
    for min_tier, forms in table:
        if format_tier >= min_tier:
            chosen = forms
    return chosen


def _peel_integer_const(expr: Any) -> tuple[int | None, Any]:
    from question_engine.frameworks.primitives.poly_expression import Const, Mul

    if not isinstance(expr, Mul):
        return None, expr
    consts: list[int] = []
    rest: list[Any] = []
    for factor in expr.factors:
        if isinstance(factor, Const) and isinstance(factor.value, int):
            consts.append(int(factor.value))
        elif isinstance(factor, Const) and isinstance(factor.value, Fraction) and factor.value.denominator == 1:
            consts.append(int(factor.value))
        else:
            rest.append(factor)
    if not consts:
        return None, expr
    k = 1
    for c in consts:
        k *= c
    if abs(k) <= 1:
        return None, expr
    if not rest:
        return k, Const(1)
    if len(rest) == 1:
        return k, rest[0]
    return k, Mul(tuple(rest))


def sample_reverse_chain_integral(
    *,
    d: float,
    flavor: str = "power",
    variable: str = "x",
    include_plus_c: bool = True,
    allow_trig: bool = False,
    allow_exp: bool = False,
    allow_log: bool = False,
    allow_invtrig: bool = False,
    omit_du_constant: bool | None = None,
    rng: random.Random | None = None,
    seed: int | None = None,
) -> USubSample:
    """Build ∫ F'(g(x)) g'(x) dx by sampling F∘g from Diff ``expr_skeleton``.

    Antiderivative is the undressed ``F(g)`` (plus +C). Numeric hardness follows
    ``skeleton_numeric_tier``; nested inners / missing chain constants follow
    ``skeleton_format_tier``.
    """
    from question_engine.frameworks.primitives.expr_skeleton import sample_from_form
    from question_engine.frameworks.primitives.poly_expression import (
        Const,
        Mul,
        differentiate,
        render_latex,
    )
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        SkeletonDifficultyBands,
    )

    rng = rng or (random.Random(seed) if seed is not None else random.Random())
    bands = SkeletonDifficultyBands.from_d(d)
    flavor_key = flavor if flavor in _REVERSE_CHAIN_FORMS else "power"
    form_ids = _reverse_chain_form_ids(flavor_key, bands.format_tier)
    form_id = rng.choice(form_ids)
    # Numeric hardness first; cap C so Calc-1 u-sub stays F(g) with affine/poly
    # inner — not arctan(arctan(poly)) or power towers (OpenStax Vol 1 §5.5–5.7).
    conceptual_raw = float((0, 4, 8, 14, 20)[bands.numeric_tier])
    cap = {
        "power": 8.0,
        "ln_exp": 8.0 if bands.format_tier < 3 else 12.0,
        "trig": 8.0 if bands.format_tier < 3 else 12.0,
        "invtrig": 4.0,
    }.get(flavor_key, 8.0)
    conceptual = min(conceptual_raw, cap)
    allows = {
        "allow_trig": bool(allow_trig) or flavor_key == "trig" or form_id.startswith("trig") or form_id == "chain_trig_poly" or form_id == "chain_nested",
        "allow_exp": bool(allow_exp) or flavor_key == "ln_exp" or form_id in {"exp_basic", "chain_nested"},
        "allow_log": bool(allow_log) or flavor_key == "ln_exp" or form_id in {"ln_basic", "chain_nested"},
        "allow_invtrig": bool(allow_invtrig) or flavor_key == "invtrig" or form_id.startswith("invtrig"),
        "allow_chain": True,
        "allow_roots": bands.format_tier >= 1 and flavor_key == "power",
        "require_chain": True,
    }
    # Chain-nested with specials off stays algebraic.
    if flavor_key == "power" and form_id == "chain_nested":
        allows["allow_trig"] = False
        allows["allow_exp"] = False
        allows["allow_log"] = False
        form_id = "chain_nested_power"

    F, Fp, f_latex, fp_latex, inv = sample_from_form(
        form_id,
        conceptual_d=conceptual,
        allows=allows,
        rng=rng,
        var=variable,
        seed=seed,
    )
    hide = omit_du_constant
    if hide is None:
        hide = bands.format_tier >= 2
    integ_expr = Fp
    ans_expr = F
    peeled_k: int | None = None
    if hide:
        peeled_k, rest = _peel_integer_const(Fp)
        if peeled_k is not None:
            integ_expr = rest
            ans_expr = Mul((Const(Fraction(1, peeled_k)), F))
            # Keep +C on the scaled antiderivative of the shown integrand.
            fp_latex = render_latex(integ_expr, paren_style="minimal")
            f_latex = render_latex(ans_expr, paren_style="minimal")

    f_latex = _elide_unit_exponents(f_latex)
    fp_latex = _elide_unit_exponents(fp_latex)

    # Construction check: d/dx of undressed F (before peel) matches full Fp.
    check = differentiate(F, variable)
    prompt = rf"\int {fp_latex}\,d{variable}"
    answer = rf"{f_latex}+C" if include_plus_c else f_latex
    meta = {
        "construction": "reverse_chain_expr_skeleton",
        "form_id": form_id,
        "core_form_id": form_id,
        "openstax_form": form_id,
        "family": form_id,
        "u_latex": inv.get("inner_latex"),
        "outer_family": form_id,
        "inner_family": inv.get("inner_kind"),
        "function_classes": inv.get("function_classes") or ["algebraic"],
        "tricks_required": ["u_sub"],
        "skeleton_source": "expr_skeleton",
        "omit_du_constant": bool(peeled_k is not None),
        "du_constant_omitted": peeled_k,
        "numeric_tier": bands.numeric_tier,
        "format_tier": bands.format_tier,
        "conceptual_difficulty": conceptual,
        "deriv_check_latex": _elide_unit_exponents(
            render_latex(check, paren_style="minimal")
        ),
        **{k: v for k, v in inv.items() if k not in {"form_id", "core_form_id"}},
    }
    return USubSample(
        prompt_latex=prompt,
        answer_latex=answer,
        u_latex=str(inv.get("inner_latex") or ""),
        du_latex="",
        outer_family=form_id,
        inner_family=str(inv.get("inner_kind") or ""),
        metadata=meta,
    )
