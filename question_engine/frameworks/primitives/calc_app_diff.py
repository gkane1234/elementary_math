"""Constructive Calc-1 apps of differentiation (OpenStax Vol 1 Ch.4 / §3.4).

Leaves that were on ``calculus_foundations`` stubs. Each sampler builds a
polynomial whose critical / inflection / Newton data is known, so answers are
not metadata pads.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, Literal

from question_engine.generators.utils import (
    format_linear_latex,
    format_polynomial_latex,
    frac_latex,
)
from question_engine.settings.params import calc_application_structure_from_continuous

Kind = Literal[
    "relative_extrema",
    "absolute_extrema",
    "concavity",
    "newtons_method",
    "motion",
    "motion_integral",
    "de_intro",
    "slope_field",
    "separable",
    "growth_decay",
    "optimization",
    "increase_decrease",
    "mean_value",
    "rolles",
    "curve_sketching",
    "graphical_f_fp",
    "related_rates",
    "differentials",
    "linear_approximation",
]


@dataclass(frozen=True)
class AppDiffItem:
    prompt_latex: str
    answer_latex: str
    label: str
    form_id: str
    metadata: dict[str, Any] = field(default_factory=dict)


def _d(settings: dict[str, Any]) -> float:
    try:
        return max(0.0, float(settings.get("difficulty") or 0.0))
    except (TypeError, ValueError):
        return 0.0


def _cubic_odd(rng: random.Random) -> tuple[int, int, str]:
    """f = x^3 - 3 a^2 x + c with integer a≥1. Crit ±a; f'' = 6x."""
    a = rng.randint(1, 4)
    c = rng.choice([0, 1, -1, 2, -2])
    aa = 3 * a * a
    body = rf"x^{{3}}-{aa}x" if c == 0 else (
        rf"x^{{3}}-{aa}x+{c}" if c > 0 else rf"x^{{3}}-{aa}x-{abs(c)}"
    )
    return a, c, body


def _poly_eval(coeffs: list[int], x: int) -> int:
    v = 0
    for a in coeffs:
        v = v * x + a
    return v


def _shifted_cubic_integer_crits(
    rng: random.Random,
) -> tuple[int, int, int, list[int]]:
    """Ex. 4.17: integer crits p<q, f'=3(x-p)(x-q), p+q even so coeffs are ints."""
    p, q = rng.choice(((-1, 3), (-2, 4), (-3, 1), (-4, 2), (-1, 5), (-5, 1)))
    c = rng.choice([0, 1, -1, -2])
    a_coef = (3 * (p + q)) // 2
    b_coef = 3 * p * q
    return p, q, c, [1, -a_coef, b_coef, c]


RELATIVE_EXTREMA_GENERATOR = "relative_extrema"

_EXTREMA_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("parabola_vertex",),
    "medium": ("parabola_vertex", "cubic_first_derivative_test"),
    "hard": ("cubic_first_derivative_test", "cubic_shifted_extrema"),
    "expert": ("cubic_shifted_extrema",),
}


def relative_extrema_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _EXTREMA_BANDS["easy"]
    if d < 16.0:
        return _EXTREMA_BANDS["medium"]
    if d < 20.0:
        return _EXTREMA_BANDS["hard"]
    return _EXTREMA_BANDS["expert"]


def _extrema_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [RELATIVE_EXTREMA_GENERATOR],
        }
        for fid in forms
    ]


def _sample_parabola_vertex(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: f=(x-h)^2-k, relative min at the vertex."""
    h = rng.randint(1, 5)
    k = rng.randint(1, 6)
    prompt = rf"\text{{Find the relative minimum of }}f(x)=(x-{h})^{{2}}-{k}."
    answer = rf"\text{{relative minimum }}-{k}\text{{ at }}x={h}"
    return AppDiffItem(
        prompt, answer, "relative extrema", "parabola_vertex",
        {"h": h, "k": k},
    )


def _sample_cubic_odd_extrema(rng: random.Random) -> AppDiffItem:
    """Reuse ``_cubic_odd``: crits ±a. Mid-D leftover."""
    a, c, body = _cubic_odd(rng)
    ymax = 2 * a**3 + c
    ymin = -2 * a**3 + c
    prompt = rf"\text{{Find the relative extrema of }}f(x)={body}."
    answer = (
        rf"\text{{rel max }}{ymax}\text{{ at }}x={-a};"
        rf"\text{{ rel min }}{ymin}\text{{ at }}x={a}"
    )
    return AppDiffItem(
        prompt, answer, "relative extrema", "cubic_first_derivative_test",
        {"a": a, "c": c},
    )


def _sample_cubic_shifted_extrema(rng: random.Random) -> AppDiffItem:
    """Ex. 4.17 shape: integer crits p<q; rel max at p, rel min at q."""
    p, q, c, coeffs = _shifted_cubic_integer_crits(rng)
    body = format_polynomial_latex(coeffs, variable="x")
    ymax = _poly_eval(coeffs, p)
    ymin = _poly_eval(coeffs, q)
    prompt = rf"\text{{Find the relative extrema of }}f(x)={body}."
    answer = (
        rf"\text{{rel max }}{ymax}\text{{ at }}x={p};"
        rf"\text{{ rel min }}{ymin}\text{{ at }}x={q}"
    )
    return AppDiffItem(
        prompt, answer, "relative extrema", "cubic_shifted_extrema",
        {"p": p, "q": q, "c": c},
    )


_EXTREMA_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "parabola_vertex": _sample_parabola_vertex,
    "cubic_first_derivative_test": _sample_cubic_odd_extrema,
    "cubic_shifted_extrema": _sample_cubic_shifted_extrema,
}


def sample_relative_extrema(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """First-derivative test. High D unlocks Ex. 4.17 shifted crits."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = relative_extrema_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _extrema_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _EXTREMA_BUILDERS:
        fid = forms[0]
    item = _EXTREMA_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": RELATIVE_EXTREMA_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": RELATIVE_EXTREMA_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


ABSOLUTE_EXTREMA_GENERATOR = "absolute_extrema"

_ABS_EXTREMA_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("closed_interval_parabola",),
    "medium": ("closed_interval_parabola", "closed_interval_cubic"),
    "hard": ("closed_interval_cubic", "closed_interval_shifted_cubic"),
    "expert": ("closed_interval_shifted_cubic",),
}


def absolute_extrema_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _ABS_EXTREMA_BANDS["easy"]
    if d < 16.0:
        return _ABS_EXTREMA_BANDS["medium"]
    if d < 20.0:
        return _ABS_EXTREMA_BANDS["hard"]
    return _ABS_EXTREMA_BANDS["expert"]


def _abs_extrema_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [ABSOLUTE_EXTREMA_GENERATOR],
        }
        for fid in forms
    ]


def _closed_interval_answer(vals: dict[int, int]) -> str:
    mn = min(vals.values())
    mx = max(vals.values())
    xmin = next(x for x, v in vals.items() if v == mn)
    xmax = next(x for x, v in vals.items() if v == mx)
    return (
        rf"\text{{abs min }}{mn}\text{{ at }}x={xmin};"
        rf"\text{{ abs max }}{mx}\text{{ at }}x={xmax}"
    )


def _sample_closed_interval_parabola(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: f=x^2 on [0,b] (vertex at the left endpoint)."""
    b = rng.randint(2, 5)
    prompt = (
        rf"\text{{Find the absolute extrema of }}f(x)=x^{{2}}"
        rf"\text{{ on }}[0,{b}]."
    )
    answer = _closed_interval_answer({0: 0, b: b * b})
    return AppDiffItem(
        prompt, answer, "absolute extrema", "closed_interval_parabola",
        {"b": b, "interval": (0, b)},
    )


def _sample_closed_interval_cubic(rng: random.Random) -> AppDiffItem:
    """Reuse ``_cubic_odd`` on [-2a, 2a]. Mid-D leftover; crits ±a."""
    a, c, body = _cubic_odd(rng)
    lo, hi = -2 * a, 2 * a
    vals = {
        lo: (lo**3) - 3 * a * a * lo + c,
        -a: 2 * a**3 + c,
        a: -2 * a**3 + c,
        hi: (hi**3) - 3 * a * a * hi + c,
    }
    prompt = (
        rf"\text{{Find the absolute extrema of }}f(x)={body}"
        rf"\text{{ on }}[{lo},{hi}]."
    )
    return AppDiffItem(
        prompt, _closed_interval_answer(vals), "absolute extrema",
        "closed_interval_cubic",
        {"a": a, "c": c, "interval": (lo, hi)},
    )


def _sample_closed_interval_shifted(rng: random.Random) -> AppDiffItem:
    """Ex. 4.17 cubic on a closed interval containing both integer crits.

    Pad one side past the half-span so an endpoint strictly beats the matching
    local extremum (OpenStax §4.3 closed-interval method).
    """
    p, q, c, coeffs = _shifted_cubic_integer_crits(rng)
    body = format_polynomial_latex(coeffs, variable="x")
    extra = (q - p) // 2 + 1
    if rng.choice((True, False)):
        lo, hi = p - extra, q + 1
    else:
        lo, hi = p - 1, q + extra
    vals = {
        lo: _poly_eval(coeffs, lo),
        p: _poly_eval(coeffs, p),
        q: _poly_eval(coeffs, q),
        hi: _poly_eval(coeffs, hi),
    }
    prompt = (
        rf"\text{{Find the absolute extrema of }}f(x)={body}"
        rf"\text{{ on }}[{lo},{hi}]."
    )
    return AppDiffItem(
        prompt, _closed_interval_answer(vals), "absolute extrema",
        "closed_interval_shifted_cubic",
        {"p": p, "q": q, "c": c, "interval": (lo, hi)},
    )


_ABS_EXTREMA_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "closed_interval_parabola": _sample_closed_interval_parabola,
    "closed_interval_cubic": _sample_closed_interval_cubic,
    "closed_interval_shifted_cubic": _sample_closed_interval_shifted,
}


def sample_absolute_extrema(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Closed-interval EVT. High D unlocks Ex. 4.17 shifted crits."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = absolute_extrema_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _abs_extrema_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _ABS_EXTREMA_BUILDERS:
        fid = forms[0]
    item = _ABS_EXTREMA_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": ABSOLUTE_EXTREMA_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": ABSOLUTE_EXTREMA_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


INCREASE_DECREASE_GENERATOR = "intervals_increase_decrease"

_INCDEC_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("parabola_increasing",),
    "medium": ("parabola_increasing", "cubic_odd_sign_chart"),
    "hard": ("cubic_odd_sign_chart", "cubic_shifted_sign_chart"),
    "expert": ("cubic_shifted_sign_chart",),
}


def increase_decrease_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _INCDEC_BANDS["easy"]
    if d < 16.0:
        return _INCDEC_BANDS["medium"]
    if d < 20.0:
        return _INCDEC_BANDS["hard"]
    return _INCDEC_BANDS["expert"]


def _incdec_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [INCREASE_DECREASE_GENERATOR],
        }
        for fid in forms
    ]


def _poly_body(coeffs: list[int]) -> str:
    return format_polynomial_latex(coeffs, variable="x")


def _sample_parabola_increasing(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: f=x^2+bx+c, increasing on (-b/2, ∞)."""
    b = rng.randint(-8, 8)
    while b == 0:
        b = rng.randint(-8, 8)
    c = rng.randint(-5, 5)
    crit = frac_latex(Fraction(-b, 2))
    body = _poly_body([1, b, c])
    prompt = rf"\text{{Find the intervals where }}f(x)={body}\text{{ is increasing.}}"
    answer = rf"\left({crit},\infty\right)"
    return AppDiffItem(
        prompt, answer, "intervals of increase", "parabola_increasing",
        {"b": b, "c": c, "crit": str(Fraction(-b, 2))},
    )


def _sample_cubic_odd_sign_chart(rng: random.Random) -> AppDiffItem:
    """Reuse ``_cubic_odd``: f'=3(x-a)(x+a). OpenStax §4.5 odd-cubic shape."""
    a, c, body = _cubic_odd(rng)
    prompt = (
        rf"\text{{Find the intervals of increase and decrease of }}f(x)={body}."
    )
    answer = (
        rf"\text{{increasing on }}(-\infty,{-a})\cup({a},\infty);"
        rf"\text{{ decreasing on }}({-a},{a})"
    )
    return AppDiffItem(
        prompt, answer, "intervals of increase", "cubic_odd_sign_chart",
        {"a": a, "c": c},
    )


def _sample_cubic_shifted_sign_chart(rng: random.Random) -> AppDiffItem:
    """Ex. 4.17 shape: integer crits p<q, f'=3(x-p)(x-q), p+q even."""
    p, q, c, coeffs = _shifted_cubic_integer_crits(rng)
    body = _poly_body(coeffs)
    prompt = (
        rf"\text{{Find the intervals of increase and decrease of }}f(x)={body}."
    )
    answer = (
        rf"\text{{increasing on }}(-\infty,{p})\cup({q},\infty);"
        rf"\text{{ decreasing on }}({p},{q})"
    )
    return AppDiffItem(
        prompt, answer, "intervals of increase", "cubic_shifted_sign_chart",
        {"p": p, "q": q, "c": c},
    )


_INCDEC_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "parabola_increasing": _sample_parabola_increasing,
    "cubic_odd_sign_chart": _sample_cubic_odd_sign_chart,
    "cubic_shifted_sign_chart": _sample_cubic_shifted_sign_chart,
}


def sample_intervals_increase(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """First-derivative sign chart. Reuses extrema cubics; D=0 stays the old parabola."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = increase_decrease_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _incdec_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _INCDEC_BUILDERS:
        fid = forms[0]
    item = _INCDEC_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": INCREASE_DECREASE_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": INCREASE_DECREASE_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


CONCAVITY_GENERATOR = "intervals_concavity"

_CONCAVITY_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("odd_power_positive_ray",),
    "medium": ("odd_power_positive_ray", "cubic_second_derivative"),
    "hard": ("cubic_second_derivative", "cubic_shifted_inflection"),
    "expert": ("cubic_shifted_inflection",),
}


def concavity_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _CONCAVITY_BANDS["easy"]
    if d < 16.0:
        return _CONCAVITY_BANDS["medium"]
    if d < 20.0:
        return _CONCAVITY_BANDS["hard"]
    return _CONCAVITY_BANDS["expert"]


def _concavity_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [CONCAVITY_GENERATOR],
        }
        for fid in forms
    ]


def _sample_odd_power_positive_ray(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: f=x^p on (0,∞) is concave up."""
    p = rng.choice([3, 5])
    prompt = (
        rf"\text{{Determine the concavity of }}f(x)=x^{{{p}}}"
        rf"\text{{ on }}(0,\infty)."
    )
    return AppDiffItem(
        prompt, r"\text{concave up}", "concavity", "odd_power_positive_ray",
        {"p": p},
    )


def _sample_cubic_second_derivative(rng: random.Random) -> AppDiffItem:
    """Reuse ``_cubic_odd``: f''=6x, inflection at 0. Mid-D leftover."""
    a, c, body = _cubic_odd(rng)
    prompt = rf"\text{{Find the intervals of concavity of }}f(x)={body}."
    answer = (
        r"\text{concave down on }(-\infty,0);\text{ concave up on }(0,\infty)"
    )
    return AppDiffItem(
        prompt, answer, "concavity", "cubic_second_derivative",
        {"a": a, "inflection": 0},
    )


def _sample_cubic_shifted_inflection(rng: random.Random) -> AppDiffItem:
    """Ex. 4.19 shape: f=±(x³−3hx²)+bx+c, inflection at h≠0."""
    h = rng.choice((-3, -2, -1, 1, 2, 3, 4))
    b = rng.choice((-9, -6, 0, 6, 9))
    c = rng.choice((0, 1, -1, 2, -2, 30))
    leading_pos = rng.choice((True, False))
    if leading_pos:
        coeffs = [1, -3 * h, b, c]
        down = rf"(-\infty,{h})"
        up = rf"({h},\infty)"
    else:
        coeffs = [-1, 3 * h, b, c]
        down = rf"({h},\infty)"
        up = rf"(-\infty,{h})"
    body = _poly_body(coeffs)
    prompt = (
        rf"\text{{Find the intervals of concavity of }}f(x)={body}"
        rf"\text{{ and the inflection point.}}"
    )
    answer = (
        rf"\text{{concave down on }}{down};\text{{ concave up on }}{up};"
        rf"\text{{ inflection at }}x={h}"
    )
    return AppDiffItem(
        prompt, answer, "concavity", "cubic_shifted_inflection",
        {"h": h, "b": b, "c": c, "leading_pos": leading_pos, "inflection": h},
    )


_CONCAVITY_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "odd_power_positive_ray": _sample_odd_power_positive_ray,
    "cubic_second_derivative": _sample_cubic_second_derivative,
    "cubic_shifted_inflection": _sample_cubic_shifted_inflection,
}


def sample_concavity(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Second-derivative sign chart. High D unlocks Ex. 4.19 shifted inflections."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = concavity_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _concavity_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _CONCAVITY_BUILDERS:
        fid = forms[0]
    item = _CONCAVITY_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": CONCAVITY_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": CONCAVITY_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


MVT_GENERATOR = "mean_value_theorem"

_MVT_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("mvt_x_squared",),
    "medium": ("mvt_x_squared", "mvt_k_x_cubed"),
    "hard": ("mvt_k_x_cubed", "mvt_sqrt_x"),
    "expert": ("mvt_sqrt_x",),
}


def mvt_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _MVT_BANDS["easy"]
    if d < 16.0:
        return _MVT_BANDS["medium"]
    if d < 20.0:
        return _MVT_BANDS["hard"]
    return _MVT_BANDS["expert"]


def _mvt_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [MVT_GENERATOR],
        }
        for fid in forms
    ]


def _sample_mvt_x_squared(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: f=x² on [0,b], c=b/2."""
    b = rng.randint(2, 4)
    prompt = (
        rf"\text{{Find }}c\text{{ guaranteed by the Mean Value Theorem for }}"
        rf"f(x)=x^{{2}}\text{{ on }}[0,{b}]."
    )
    answer = frac_latex(Fraction(b, 2))
    return AppDiffItem(
        prompt, answer, "Mean Value Theorem", "mvt_x_squared",
        {"b": b, "c": str(Fraction(b, 2))},
    )


def _sample_mvt_k_x_cubed(rng: random.Random) -> AppDiffItem:
    """Existing cubic on the core: f=kx³ on [0,b], c=b/√3."""
    k = rng.randint(1, 3)
    b = rng.randint(2, 6)
    f = format_polynomial_latex([k, 0, 0, 0], variable="x")
    prompt = (
        rf"\text{{Find }}c\text{{ guaranteed by the Mean Value Theorem for }}"
        rf"f(x)={f}\text{{ on }}[0,{b}]."
    )
    answer = rf"\frac{{{b}}}{{\sqrt{{3}}}}"
    return AppDiffItem(
        prompt, answer, "Mean Value Theorem", "mvt_k_x_cubed",
        {"k": k, "b": b},
    )


def _sample_mvt_sqrt_x(rng: random.Random) -> AppDiffItem:
    """OpenStax Ex. 4.15: f=√x on [0,b], c=b/4."""
    b = rng.choice((4, 9, 16, 25))
    prompt = (
        rf"\text{{Find }}c\text{{ guaranteed by the Mean Value Theorem for }}"
        rf"f(x)=\sqrt{{x}}\text{{ on }}[0,{b}]."
    )
    answer = frac_latex(Fraction(b, 4))
    return AppDiffItem(
        prompt, answer, "Mean Value Theorem", "mvt_sqrt_x",
        {"b": b, "c": str(Fraction(b, 4))},
    )


_MVT_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "mvt_x_squared": _sample_mvt_x_squared,
    "mvt_k_x_cubed": _sample_mvt_k_x_cubed,
    "mvt_sqrt_x": _sample_mvt_sqrt_x,
}


def sample_mean_value(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Find c with f'(c)=(f(b)-f(a))/(b-a). High D locks out x² leftovers."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = mvt_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _mvt_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _MVT_BUILDERS:
        fid = forms[0]
    item = _MVT_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": MVT_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": MVT_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


ROLLES_GENERATOR = "rolles_theorem"

_ROLLES_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("rolles_even_quad",),
    "medium": ("rolles_even_quad", "rolles_two_roots"),
    "hard": ("rolles_two_roots", "rolles_cubic_odd"),
    "expert": ("rolles_cubic_odd",),
}


def rolles_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _ROLLES_BANDS["easy"]
    if d < 16.0:
        return _ROLLES_BANDS["medium"]
    if d < 20.0:
        return _ROLLES_BANDS["hard"]
    return _ROLLES_BANDS["expert"]


def _rolles_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [ROLLES_GENERATOR],
        }
        for fid in forms
    ]


def _sample_rolles_even_quad(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: f=x²−n² on [−n,n], c=0."""
    n = rng.randint(2, 5)
    body = _poly_body([1, 0, -n * n])
    prompt = (
        rf"\text{{Find }}c\text{{ guaranteed by Rolle's Theorem for }}"
        rf"f(x)={body}\text{{ on }}[{-n},{n}]."
    )
    return AppDiffItem(
        prompt, "0", "Rolle's Theorem", "rolles_even_quad",
        {"n": n, "c": 0},
    )


def _sample_rolles_two_roots(rng: random.Random) -> AppDiffItem:
    """Ex. 4.14 first: f=(x−a)(x−b) on [a,b], midpoint c≠0 (not even-quad)."""
    a, b = -2, 0
    for _ in range(24):
        lo = rng.randint(-4, 1)
        hi = lo + rng.randint(2, 5)
        if lo + hi != 0:
            a, b = lo, hi
            break
    mid = Fraction(a + b, 2)
    body = _poly_body([1, -(a + b), a * b])
    prompt = (
        rf"\text{{Find }}c\text{{ guaranteed by Rolle's Theorem for }}"
        rf"f(x)={body}\text{{ on }}[{a},{b}]."
    )
    return AppDiffItem(
        prompt, frac_latex(mid), "Rolle's Theorem", "rolles_two_roots",
        {"a": a, "b": b, "c": str(mid)},
    )


def _sample_rolles_cubic_odd(rng: random.Random) -> AppDiffItem:
    """Ex. 4.14 second: f=x³−n²x on [−n,n], c=±n/√3."""
    n = rng.choice((2, 3, 4))
    body = _poly_body([1, 0, -n * n, 0])
    prompt = (
        rf"\text{{Find all }}c\text{{ guaranteed by Rolle's Theorem for }}"
        rf"f(x)={body}\text{{ on }}[{-n},{n}]."
    )
    answer = rf"c=\pm\frac{{{n}}}{{\sqrt{{3}}}}"
    return AppDiffItem(
        prompt, answer, "Rolle's Theorem", "rolles_cubic_odd",
        {"n": n},
    )


_ROLLES_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "rolles_even_quad": _sample_rolles_even_quad,
    "rolles_two_roots": _sample_rolles_two_roots,
    "rolles_cubic_odd": _sample_rolles_cubic_odd,
}


def sample_rolles(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Find c with f'(c)=0 when f(a)=f(b). High D locks out even-quad c=0."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = rolles_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _rolles_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _ROLLES_BUILDERS:
        fid = forms[0]
    item = _ROLLES_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": ROLLES_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": ROLLES_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


NEWTON_GENERATOR = "newtons_method"

_NEWTON_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("newton_one_quad",),
    "medium": ("newton_one_quad", "newton_one_cubic"),
    "hard": ("newton_one_cubic", "newton_two_cubic"),
    "expert": ("newton_two_cubic",),
}


def newton_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _NEWTON_BANDS["easy"]
    if d < 16.0:
        return _NEWTON_BANDS["medium"]
    if d < 20.0:
        return _NEWTON_BANDS["hard"]
    return _NEWTON_BANDS["expert"]


def _newton_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [NEWTON_GENERATOR],
        }
        for fid in forms
    ]


def _sample_newton_one_quad(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: one step on f=x²−a (OpenStax square-root shape)."""
    a = rng.choice([2, 3, 5, 10])
    x0 = rng.choice([1, 2])
    if x0 * x0 == a:
        x0 = 1 if a != 1 else 2
    fx = x0 * x0 - a
    fpx = 2 * x0
    x1 = Fraction(x0) - Fraction(fx, fpx)
    prompt = (
        rf"\text{{Use one Newton step for }}f(x)=x^{{2}}-{a}"
        rf"\text{{ from }}x_0={x0}."
    )
    return AppDiffItem(
        prompt, rf"x_1={frac_latex(x1)}", "Newton", "newton_one_quad",
        {"steps": 1, "x0": x0, "a": a},
    )


def _newton_cubic_start(rng: random.Random) -> tuple[int, int, Fraction]:
    """Old-path cubic: f=x³−a, first iterate from x0∈{1,2}."""
    a = rng.choice([2, 3, 5, 7, 10])
    x0 = rng.choice([1, 2])
    if x0**3 == a:
        x0 = 1
    fx = x0**3 - a
    fpx = 3 * x0 * x0
    x1 = Fraction(x0) - Fraction(fx, fpx)
    return a, x0, x1


def _sample_newton_one_cubic(rng: random.Random) -> AppDiffItem:
    """Mid-D leftover: one step on f=x³−a."""
    a, x0, x1 = _newton_cubic_start(rng)
    prompt = (
        rf"\text{{Use one Newton step for }}f(x)=x^{{3}}-{a}"
        rf"\text{{ from }}x_0={x0}."
    )
    return AppDiffItem(
        prompt, rf"x_1={frac_latex(x1)}", "Newton", "newton_one_cubic",
        {"steps": 1, "x0": x0, "a": a},
    )


def _sample_newton_two_cubic(rng: random.Random) -> AppDiffItem:
    """High D: two steps on f=x³−a (old-path expert)."""
    a, x0, x1 = _newton_cubic_start(rng)
    x1n, x1d = x1.numerator, x1.denominator
    x1_3 = x1**3
    fp = 3 * x1 * x1
    x2 = x1 - (x1_3 - a) / fp
    prompt = (
        rf"\text{{Use two Newton steps for }}f(x)=x^{{3}}-{a}"
        rf"\text{{ from }}x_0={x0}."
    )
    return AppDiffItem(
        prompt, rf"x_2={frac_latex(x2)}", "Newton", "newton_two_cubic",
        {"steps": 2, "x0": x0, "x1": str(x1), "a": a, "x1_frac": (x1n, x1d)},
    )


_NEWTON_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "newton_one_quad": _sample_newton_one_quad,
    "newton_one_cubic": _sample_newton_one_cubic,
    "newton_two_cubic": _sample_newton_two_cubic,
}


def sample_newton(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Newton iterates. High D locks out one-quad leftovers for two cubic steps."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = newton_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _newton_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _NEWTON_BUILDERS:
        fid = forms[0]
    item = _NEWTON_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": NEWTON_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": NEWTON_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


DIFFERENTIALS_GENERATOR = "differentials"

_DIFF_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("poly_power", "poly_quad", "trig", "exp", "ln"),
    "medium": (
        "poly_power", "poly_quad", "trig", "exp", "ln", "radical", "reciprocal",
    ),
    "hard": (
        "radical", "reciprocal", "product", "quotient", "chain_exp", "eval_dx",
    ),
    "expert": ("product", "quotient", "chain_exp", "eval_dx"),
}


def differential_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _DIFF_BANDS["easy"]
    if d < 16.0:
        return _DIFF_BANDS["medium"]
    if d < 20.0:
        return _DIFF_BANDS["hard"]
    return _DIFF_BANDS["expert"]


def _diff_d(settings: dict[str, Any]) -> float:
    if "difficulty" in settings and settings["difficulty"] is not None:
        try:
            return max(0.0, float(settings["difficulty"]))
        except (TypeError, ValueError):
            pass
    tier = str(settings.get("difficulty_tier", "")).strip().lower()
    return {"easy": 0.0, "medium": 8.0, "hard": 16.0}.get(tier, _d(settings))


def _diff_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [DIFFERENTIALS_GENERATOR],
        }
        for fid in forms
    ]


def _diff_poly_y(rng: random.Random, coeffs: list[int], x: str) -> str:
    """Old-path poly display: standard / reversed / factored x(x+b)."""
    from question_engine.generators.calculus_pilot import _poly_display

    style = rng.choice(["standard", "reversed", "factored_linear"])
    return _poly_display(coeffs, x, style=style)


def _sample_diff_poly_power(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D=0: y=x^n, n∈{2,3,4,5}."""
    n = rng.randint(2, 5)
    y = f"{x}^{{{n}}}"
    dy = rf"{n}{x}^{{{n - 1}}}\,d{x}" if n - 1 != 1 else rf"{n}{x}\,d{x}"
    if n - 1 == 0:
        dy = rf"{n}\,d{x}"
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy={dy}",
        "differential",
        "poly_power",
        {"n": n, "variant": f"power:{n}"},
    )


def _sample_diff_poly_quad(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D=0: OpenStax Ex. 4.8 y=x^2+bx (also reversed / factored)."""
    b = rng.randint(1, 5)
    coeffs = [1, b, 0]
    y = _diff_poly_y(rng, coeffs, x)
    inner = format_linear_latex(2, b, variable=x)
    dy = rf"\left({inner}\right)\,d{x}"
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy={dy}",
        "differential",
        "poly_quad",
        {"b": b},
    )


def _sample_diff_trig(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D=0: y=sin/cos/tan (OpenStax Ex. 4.8 includes cos x)."""
    fn = rng.choice(["sin", "cos", "tan"])
    if fn == "sin":
        y = rng.choice([rf"\sin({x})", rf"\sin {x}"])
        dy = rf"\cos({x})\,d{x}"
    elif fn == "cos":
        y = rng.choice([rf"\cos({x})", rf"\cos {x}"])
        dy = rf"-\sin({x})\,d{x}"
    else:
        y = rf"\tan({x})"
        dy = rf"\sec^{{2}}({x})\,d{x}"
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy={dy}",
        "differential",
        "trig",
        {"variant": fn},
    )


def _sample_diff_exp(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D=0 leftover: y=e^{kx} / exp(kx)."""
    k = rng.randint(1, 4)
    form = rng.choice(["e", "exp"])
    y = rng.choice(
        [
            rf"e^{{{k}{x}}}" if k != 1 else rf"e^{{{x}}}",
            rf"\exp({k}{x})" if k != 1 else rf"\exp({x})",
        ]
    )
    dy = rf"{k}e^{{{k}{x}}}\,d{x}" if k != 1 else rf"e^{{{x}}}\,d{x}"
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy={dy}",
        "differential",
        "exp",
        {"k": k, "variant": f"{form}:k{k}"},
    )


def _sample_diff_ln(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D=0 leftover: y=ln x / ln|x| / log(x)."""
    form = rng.choice(["ln", "ln_abs", "log"])
    y = rng.choice([rf"\ln({x})", rf"\ln|{x}|", rf"\log({x})"])
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy=\frac{{1}}{{{x}}}\,d{x}",
        "differential",
        "ln",
        {"variant": form},
    )


def _sample_diff_radical(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D≥5 unlock: y=√x or x^{1/2}."""
    form = rng.choice(["sqrt", "half_power"])
    y = rng.choice([rf"\sqrt{{{x}}}", rf"{x}^{{1/2}}"])
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy=\frac{{1}}{{2\sqrt{{{x}}}}}\,d{x}",
        "differential",
        "radical",
        {"variant": form},
    )


def _sample_diff_reciprocal(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D≥5 unlock: y=1/x or x^{-1}."""
    form = rng.choice(["frac", "neg_power"])
    y = rng.choice([rf"\frac{{1}}{{{x}}}", rf"{x}^{{-1}}"])
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy=-\frac{{1}}{{{x}^{{2}}}}\,d{x}",
        "differential",
        "reciprocal",
        {"variant": form},
    )


def _sample_diff_product(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path nested: y=x sin x."""
    form = rng.choice(["juxtapose", "sin_first", "cdot"])
    y = rng.choice(
        [rf"{x}\sin({x})", rf"\sin({x})\,{x}", rf"{x}\cdot\sin({x})"]
    )
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy=\left(\sin({x})+{x}\cos({x})\right)\,d{x}",
        "differential",
        "product",
        {"variant": form},
    )


def _sample_diff_quotient(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path nested: y=x/(x+1)."""
    form = rng.choice(["frac", "neg_power"])
    y = rng.choice(
        [
            rf"\frac{{{x}}}{{{x}+1}}",
            rf"{x}({x}+1)^{{-1}}",
        ]
    )
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy=\frac{{1}}{{\left({x}+1\right)^{{2}}}}\,d{x}",
        "differential",
        "quotient",
        {"variant": form},
    )


def _sample_diff_chain_exp(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path nested: y=e^{x^2}."""
    form = rng.choice(["e", "exp"])
    y = rng.choice([rf"e^{{{x}^{{2}}}}", rf"\exp({x}^{{2}})"])
    return AppDiffItem(
        rf"\text{{For }}y={y},\text{{ find }}dy.",
        rf"dy=2{x}e^{{{x}^{{2}}}}\,d{x}",
        "differential",
        "chain_exp",
        {"variant": form},
    )


def _sample_diff_eval_dx(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path nested: OpenStax Ex. 4.8 evaluate dy at x=a, dx=h."""
    a = rng.randint(2, 5)
    h = rng.choice([Fraction(1, 10), Fraction(1, 5), Fraction(1, 2)])
    b = rng.randint(1, 4)
    coeffs = [1, b, 0]
    y = _diff_poly_y(rng, coeffs, x)
    slope = 2 * a + b
    dy_val = frac_latex(Fraction(slope) * h)
    prompt = (
        rf"\text{{For }}y={y},\text{{ find }}dy\text{{ when }}"
        rf"{x}={a}\text{{ and }}d{x}={frac_latex(h)}."
    )
    return AppDiffItem(
        prompt, dy_val, "differential evaluation", "eval_dx",
        {"a": a, "h": str(h), "b": b},
    )


_DIFF_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "poly_power": _sample_diff_poly_power,
    "poly_quad": _sample_diff_poly_quad,
    "trig": _sample_diff_trig,
    "exp": _sample_diff_exp,
    "ln": _sample_diff_ln,
    "radical": _sample_diff_radical,
    "reciprocal": _sample_diff_reciprocal,
    "product": _sample_diff_product,
    "quotient": _sample_diff_quotient,
    "chain_exp": _sample_diff_chain_exp,
    "eval_dx": _sample_diff_eval_dx,
}


def sample_differentials(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """dy = f'(x) dx. High D locks out D=0 log/power leftovers; D=22 nested only."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _diff_d(settings)
    forms = differential_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _diff_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _DIFF_BUILDERS:
        fid = forms[0]
    item = _DIFF_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": DIFFERENTIALS_GENERATOR,
        "structure_id": f"{DIFFERENTIALS_GENERATOR}:{fid}",
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": DIFFERENTIALS_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


LINEAR_APPROX_GENERATOR = "linear_approximation"

_LINAPPROX_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("quad", "sqrt"),
    "medium": ("quad", "sqrt", "quad_estimate", "reciprocal", "exp"),
    "hard": ("sqrt", "reciprocal", "exp"),
    "expert": ("reciprocal", "exp"),
}


def linear_approx_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _LINAPPROX_BANDS["easy"]
    if d < 16.0:
        return _LINAPPROX_BANDS["medium"]
    if d < 20.0:
        return _LINAPPROX_BANDS["hard"]
    return _LINAPPROX_BANDS["expert"]


def _linapprox_d(settings: dict[str, Any]) -> float:
    if "difficulty" in settings and settings["difficulty"] is not None:
        try:
            return max(0.0, float(settings["difficulty"]))
        except (TypeError, ValueError):
            pass
    tier = str(settings.get("difficulty_tier", "")).strip().lower()
    return {"easy": 0.0, "medium": 8.0, "hard": 16.0}.get(tier, _d(settings))


def _linapprox_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [LINEAR_APPROX_GENERATOR],
        }
        for fid in forms
    ]


def _sample_linapprox_quad(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D=0 leftover: L(x) of f=x² at a∈{1,2,3,4}."""
    a = rng.randint(1, 4)
    fa = a * a
    fp = 2 * a
    f_body = rf"{x}^{{2}}"
    L = rf"{fa}+{fp}({x}-{a})" if fp != 1 else rf"{fa}+({x}-{a})"
    prompt = (
        rf"\text{{Find the linear approximation of }}f({x})={f_body}"
        rf"\text{{ at }}{x}={a}."
    )
    return AppDiffItem(
        prompt, rf"L({x})={L}", "linear approximation", "quad",
        {"a": a, "variant": "formula"},
    )


def _sample_linapprox_quad_estimate(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D≥8 leftover: use L of x² to estimate f(a+h)."""
    a = rng.randint(1, 4)
    fa = a * a
    fp = 2 * a
    f_body = rf"{x}^{{2}}"
    h = rng.choice([Fraction(1, 10), Fraction(1, 5), Fraction(1, 2)])
    x0 = a + h
    est = fa + fp * h
    prompt = (
        rf"\text{{Use the linear approximation of }}f({x})={f_body}"
        rf"\text{{ at }}{x}={a}\text{{ to estimate }}f({frac_latex(x0)})."
    )
    return AppDiffItem(
        prompt, frac_latex(est), "linear approximation", "quad_estimate",
        {"a": a, "h": str(h), "variant": "estimate"},
    )


def _sample_linapprox_sqrt(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D=0 leftover: L(x) of √x at a perfect square (OpenStax Ex. 4.5)."""
    a = rng.choice([1, 4, 9])
    fa_s = {1: "1", 4: "2", 9: "3"}[a]
    prompt = (
        rf"\text{{Find the linear approximation of }}f({x})=\sqrt{{{x}}}"
        rf"\text{{ at }}{x}={a}."
    )
    answer = rf"L({x})={fa_s}+\frac{{1}}{{{2 * int(fa_s)}}}({x}-{a})"
    return AppDiffItem(
        prompt, answer, "linear approximation", "sqrt",
        {"a": a, "variant": "formula"},
    )


def _sample_linapprox_reciprocal(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D≥10 unlock: L(x) of 1/x at a∈{2,…,5}."""
    a = rng.randint(2, 5)
    prompt = (
        rf"\text{{Find the linear approximation of }}f({x})=\frac{{1}}{{{x}}}"
        rf"\text{{ at }}{x}={a}."
    )
    answer = rf"L({x})=\frac{{1}}{{{a}}}-\frac{{1}}{{{a * a}}}({x}-{a})"
    return AppDiffItem(
        prompt, answer, "linear approximation", "reciprocal",
        {"a": a, "variant": "formula"},
    )


def _sample_linapprox_exp(rng: random.Random, x: str = "x") -> AppDiffItem:
    """Old-path D≥10 unlock: L(x) of e^x at 0."""
    prompt = (
        rf"\text{{Find the linear approximation of }}f({x})=e^{{{x}}}"
        rf"\text{{ at }}{x}=0."
    )
    return AppDiffItem(
        prompt, rf"L({x})=1+{x}", "linear approximation", "exp",
        {"a": 0, "variant": "formula"},
    )


_LINAPPROX_BUILDERS: dict[str, Callable[[random.Random, str], AppDiffItem]] = {
    "quad": _sample_linapprox_quad,
    "quad_estimate": _sample_linapprox_quad_estimate,
    "sqrt": _sample_linapprox_sqrt,
    "reciprocal": _sample_linapprox_reciprocal,
    "exp": _sample_linapprox_exp,
}


def sample_linear_approximation(
    rng: random.Random, settings: dict[str, Any]
) -> AppDiffItem:
    """L(x)=f(a)+f'(a)(x−a). High D locks out x² leftovers; D=22 reciprocal/exp only."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _linapprox_d(settings)
    x = str(settings.get("variable") or "x")
    forms = linear_approx_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _linapprox_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _LINAPPROX_BUILDERS:
        fid = forms[0]
    item = _LINAPPROX_BUILDERS[fid](rng, x)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": LINEAR_APPROX_GENERATOR,
        "structure_id": f"{LINEAR_APPROX_GENERATOR}:{fid}",
        "tricks_required": ["linearization"],
        "spec_snapshot": {
            "pack": "structured_linear_approximation",
            "form_id": fid,
            "family": fid,
            "generator": LINEAR_APPROX_GENERATOR,
            "variant": item.metadata.get("variant"),
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


MOTION_GENERATOR = "motion_along_a_line"

_MOTION_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("eval_velocity",),
    "medium": ("eval_velocity", "particle_at_rest"),
    "hard": ("particle_at_rest", "cubic_at_rest"),
    "expert": ("cubic_at_rest", "cubic_speed_sign"),
}


def motion_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _MOTION_BANDS["easy"]
    if d < 16.0:
        return _MOTION_BANDS["medium"]
    if d < 20.0:
        return _MOTION_BANDS["hard"]
    return _MOTION_BANDS["expert"]


def _motion_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [MOTION_GENERATOR],
        }
        for fid in forms
    ]


def _sample_eval_velocity(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: s=t²−nt, v(n)=n."""
    n = rng.randint(2, 6)
    prompt = rf"s(t)=t^{{2}}-{n}t.\quad\text{{Find }}v({n})."
    return AppDiffItem(
        prompt, str(n), "motion along a line", "eval_velocity",
        {"n": n, "ask": "v"},
    )


def _sample_particle_at_rest(rng: random.Random) -> AppDiffItem:
    """Old-path mid D leftover: s=t²−nt, rest at t=n/2 (even n)."""
    n = rng.choice([2, 4, 6])
    prompt = rf"s(t)=t^{{2}}-{n}t.\quad\text{{When is the particle at rest?}}"
    t_rest = frac_latex(Fraction(n, 2))
    return AppDiffItem(
        prompt, rf"t={t_rest}", "motion along a line", "particle_at_rest",
        {"n": n, "ask": "rest"},
    )


def _positive_cubic_rest_times(
    rng: random.Random,
) -> tuple[int, int, int, list[int]]:
    """Ex. 3.36: v=3(t−p)(t−q) with p,q>0 and p+q even so coeffs are ints."""
    p, q = rng.choice(((1, 3), (2, 4), (1, 5), (2, 6), (3, 5)))
    c = rng.choice([0, 1, -1, 2, 4])
    a_coef = (3 * (p + q)) // 2
    b_coef = 3 * p * q
    return p, q, c, [1, -a_coef, b_coef, c]


def _sample_cubic_at_rest(rng: random.Random) -> AppDiffItem:
    """OpenStax Ex. 3.36: cubic s(t), particle at rest at two positive times."""
    p, q, c, coeffs = _positive_cubic_rest_times(rng)
    body = format_polynomial_latex(coeffs, variable="t")
    prompt = rf"s(t)={body}.\quad\text{{When is the particle at rest?}}"
    answer = rf"t={p},\,t={q}"
    return AppDiffItem(
        prompt, answer, "motion along a line", "cubic_at_rest",
        {"p": p, "q": q, "c": c, "ask": "rest"},
    )


def _sample_cubic_speed_sign(rng: random.Random) -> AppDiffItem:
    """OpenStax Ex. 3.35: s=t³−kt+c; direction and speeding up / slowing down."""
    t0 = rng.choice((1, 2))
    k = rng.choice([2, 4, 5, 6, 8])
    if k == 3 * t0 * t0:
        k = 4 if t0 == 1 else 8
    c = rng.choice([0, 1, 2, -1])
    body = format_polynomial_latex([1, 0, -k, c], variable="t")
    v = 3 * t0 * t0 - k
    a = 6 * t0
    direction = "left to right" if v > 0 else "right to left"
    speed = "speeding up" if (v > 0) == (a > 0) else "slowing down"
    prompt = (
        rf"s(t)={body}.\quad\text{{Find }}v({t0})\text{{ and }}a({t0})."
        rf"\text{{ Is the particle moving left to right or right to left? "
        rf"Speeding up or slowing down?}}"
    )
    answer = (
        rf"v({t0})={v},\,a({t0})={a};\text{{ {direction}; {speed}}}"
    )
    return AppDiffItem(
        prompt, answer, "motion along a line", "cubic_speed_sign",
        {"t0": t0, "k": k, "c": c, "v": v, "a": a, "ask": "speed_sign"},
    )


_MOTION_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "eval_velocity": _sample_eval_velocity,
    "particle_at_rest": _sample_particle_at_rest,
    "cubic_at_rest": _sample_cubic_at_rest,
    "cubic_speed_sign": _sample_cubic_speed_sign,
}


def sample_motion(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """s(t)→v/a motion. High D locks out t²−nt leftovers for OpenStax cubics."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = motion_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _motion_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _MOTION_BUILDERS:
        fid = forms[0]
    item = _MOTION_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": MOTION_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": MOTION_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


MOTION_INTEGRAL_GENERATOR = "motion_along_a_line_integral"

_MOTION_INT_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("disp_linear_v",),
    "medium": ("disp_linear_v", "disp_const_v"),
    "hard": ("disp_const_v", "disp_sign_change"),
    "expert": ("disp_sign_change",),
}


def motion_integral_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _MOTION_INT_BANDS["easy"]
    if d < 16.0:
        return _MOTION_INT_BANDS["medium"]
    if d < 20.0:
        return _MOTION_INT_BANDS["hard"]
    return _MOTION_INT_BANDS["expert"]


def _motion_int_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [MOTION_INTEGRAL_GENERATOR],
        }
        for fid in forms
    ]


def _sample_disp_linear_v(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: v=2t on [0,b]; displacement b²."""
    b = rng.randint(2, 5)
    prompt = (
        rf"v(t)=2t.\quad\text{{Find the displacement from }}t=0\text{{ to }}t={b}."
    )
    return AppDiffItem(
        prompt, str(b * b), "motion integral", "disp_linear_v",
        {"b": b},
    )


def _sample_disp_const_v(rng: random.Random) -> AppDiffItem:
    """Old exclusive D=8: constant v=b on [0,b]; displacement b²."""
    b = rng.randint(2, 5)
    prompt = (
        rf"v(t)={b}.\quad\text{{Find the displacement from }}t=0\text{{ to }}t={b}."
    )
    return AppDiffItem(
        prompt, str(b * b), "motion integral", "disp_const_v",
        {"b": b},
    )


def _sample_disp_sign_change(rng: random.Random) -> AppDiffItem:
    """v=2t−2c changes sign at t=c; net displacement on [0,2c] is 0."""
    c = rng.randint(1, 3)
    prompt = (
        rf"v(t)=2t-{2 * c}.\quad\text{{Find the displacement from }}"
        rf"t=0\text{{ to }}t={2 * c}."
    )
    return AppDiffItem(
        prompt, "0", "motion integral", "disp_sign_change",
        {"c": c, "note": "net displacement zero"},
    )


_MOTION_INT_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "disp_linear_v": _sample_disp_linear_v,
    "disp_const_v": _sample_disp_const_v,
    "disp_sign_change": _sample_disp_sign_change,
}


def sample_motion_integral(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Displacement from v(t). High D locks out linear leftover for sign-change."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = motion_integral_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _motion_int_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _MOTION_INT_BUILDERS:
        fid = forms[0]
    item = _MOTION_INT_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": MOTION_INTEGRAL_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": MOTION_INTEGRAL_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


DE_INTRO_GENERATOR = "de_introduction"

_DE_INTRO_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("verify_exp",),
    "medium": ("verify_exp", "verify_euler"),
    "hard": ("verify_euler",),
    "expert": ("verify_euler",),
}


def de_intro_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _DE_INTRO_BANDS["easy"]
    if d < 16.0:
        return _DE_INTRO_BANDS["medium"]
    if d < 20.0:
        return _DE_INTRO_BANDS["hard"]
    return _DE_INTRO_BANDS["expert"]


def _de_intro_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [DE_INTRO_GENERATOR],
        }
        for fid in forms
    ]


def _sample_verify_exp(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: y=Ce^{kx} solves y'=ky (OpenStax Vol 2 §4.1 verify)."""
    k = rng.randint(2, 5)
    prompt = rf"\text{{Verify that }}y=Ce^{{{k}x}}\text{{ solves }}y'={k}y."
    answer = rf"y'={k}Ce^{{{k}x}}={k}y"
    return AppDiffItem(
        prompt, answer, "DE intro", "verify_exp",
        {"k": k},
    )


def _sample_verify_euler(rng: random.Random) -> AppDiffItem:
    """Old exclusive D≥8: y=Cx^n solves x y'=n y for x>0."""
    n = rng.randint(2, 4)
    prompt = (
        rf"\text{{Verify that }}y=Cx^{{{n}}}\text{{ solves }}"
        rf"x\,y'={n}y\text{{ for }}x>0."
    )
    answer = rf"y'={n}Cx^{{{n - 1}}}\Rightarrow x y'={n}y"
    return AppDiffItem(
        prompt, answer, "DE intro", "verify_euler",
        {"n": n},
    )


_DE_INTRO_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "verify_exp": _sample_verify_exp,
    "verify_euler": _sample_verify_euler,
}


def sample_de_intro(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Verify a proposed DE solution. High D locks out exponential leftover."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = de_intro_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _de_intro_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _DE_INTRO_BUILDERS:
        fid = forms[0]
    item = _DE_INTRO_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": DE_INTRO_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": DE_INTRO_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


SLOPE_FIELD_GENERATOR = "slope_field_interpret"

_SLOPE_FIELD_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("sf_x",),
    "medium": ("sf_x", "sf_x_plus_y"),
    "hard": ("sf_x_plus_y", "sf_xy"),
    "expert": ("sf_xy",),
}


def slope_field_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _SLOPE_FIELD_BANDS["easy"]
    if d < 16.0:
        return _SLOPE_FIELD_BANDS["medium"]
    if d < 20.0:
        return _SLOPE_FIELD_BANDS["hard"]
    return _SLOPE_FIELD_BANDS["expert"]


def _slope_field_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [SLOPE_FIELD_GENERATOR],
        }
        for fid in forms
    ]


def _sample_sf_x(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: evaluate y'=x at a lattice point (OpenStax Vol 2 §4.2)."""
    px = rng.randint(-3, 3)
    py = rng.randint(-3, 3)
    prompt = rf"\text{{For }}y'=x,\text{{ what is the slope at }}({px},{py})?"
    answer = str(px)
    return AppDiffItem(
        prompt, answer, "slope field interpret", "sf_x",
        {"px": px, "py": py},
    )


def _sample_sf_x_plus_y(rng: random.Random) -> AppDiffItem:
    """Old mid: evaluate y'=x+y at a lattice point."""
    px = rng.randint(-3, 3)
    py = rng.randint(-3, 3)
    prompt = rf"\text{{For }}y'=x+y,\text{{ what is the slope at }}({px},{py})?"
    answer = str(px + py)
    return AppDiffItem(
        prompt, answer, "slope field interpret", "sf_x_plus_y",
        {"px": px, "py": py},
    )


def _sample_sf_xy(rng: random.Random) -> AppDiffItem:
    """Old exclusive D≥16: evaluate y'=xy at a lattice point."""
    px = rng.randint(-3, 3)
    py = rng.randint(-3, 3)
    prompt = rf"\text{{For }}y'=xy,\text{{ what is the slope at }}({px},{py})?"
    answer = str(px * py)
    return AppDiffItem(
        prompt, answer, "slope field interpret", "sf_xy",
        {"px": px, "py": py},
    )


_SLOPE_FIELD_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "sf_x": _sample_sf_x,
    "sf_x_plus_y": _sample_sf_x_plus_y,
    "sf_xy": _sample_sf_xy,
}


def sample_slope_field(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Eval y' at a point. High D locks out y'=x leftover, then y'=x+y leftover."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = slope_field_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _slope_field_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _SLOPE_FIELD_BUILDERS:
        fid = forms[0]
    item = _SLOPE_FIELD_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": SLOPE_FIELD_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": SLOPE_FIELD_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


SEPARABLE_GENERATOR = "separable_diff_eq"

_SEPARABLE_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("sep_poly",),
    "medium": ("sep_poly", "sep_exp"),
    "hard": ("sep_exp", "sep_homogeneous"),
    "expert": ("sep_homogeneous",),
}


def separable_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _SEPARABLE_BANDS["easy"]
    if d < 16.0:
        return _SEPARABLE_BANDS["medium"]
    if d < 20.0:
        return _SEPARABLE_BANDS["hard"]
    return _SEPARABLE_BANDS["expert"]


def _separable_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [SEPARABLE_GENERATOR],
        }
        for fid in forms
    ]


def _sample_sep_poly(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: dy/dx=ax, y(0)=c0 (OpenStax Vol 2 §4.3 separate+integrate)."""
    a = rng.randint(1, 3)
    c0 = rng.randint(1, 5)
    rhs = "x" if a == 1 else rf"{a}x"
    prompt = rf"\text{{Solve }}\frac{{dy}}{{dx}}={rhs},\ y(0)={c0}."
    if a == 1:
        answer = rf"y=\frac{{1}}{{2}}x^2+{c0}"
    elif a == 2:
        answer = rf"y=x^2+{c0}"
    elif a % 2 == 0:
        answer = rf"y={a // 2}x^2+{c0}"
    else:
        answer = rf"y=\frac{{{a}}}{{2}}x^2+{c0}"
    return AppDiffItem(
        prompt, answer, "separable DE", "sep_poly",
        {"a": a, "c0": c0},
    )


def _sample_sep_exp(rng: random.Random) -> AppDiffItem:
    """Old exclusive D=8: dy/dx=ky, y(0)=c0."""
    k = rng.randint(2, 4)
    c0 = rng.randint(1, 5)
    prompt = rf"\text{{Solve }}\frac{{dy}}{{dx}}={k}y,\ y(0)={c0}."
    answer = rf"y={c0}e^{{{k}x}}"
    return AppDiffItem(
        prompt, answer, "separable DE", "sep_exp",
        {"k": k, "c0": c0},
    )


def _sample_sep_homogeneous(_rng: random.Random) -> AppDiffItem:
    """Old exclusive D≥16: dy/dx=y/x for x>0, y(1)=4."""
    prompt = r"\text{Solve }\frac{dy}{dx}=\frac{y}{x}\text{ for }x>0,\ y(1)=4."
    answer = r"y=4x"
    return AppDiffItem(
        prompt, answer, "separable DE", "sep_homogeneous",
        {"c0": 4},
    )


_SEPARABLE_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "sep_poly": _sample_sep_poly,
    "sep_exp": _sample_sep_exp,
    "sep_homogeneous": _sample_sep_homogeneous,
}


def sample_separable_de(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Separable IVP. High D locks out poly leftover, then exp leftover."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = separable_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _separable_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _SEPARABLE_BUILDERS:
        fid = forms[0]
    item = _SEPARABLE_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": SEPARABLE_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": SEPARABLE_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


GROWTH_DECAY_GENERATOR = "calc_continuous_growth_decay"

_GROWTH_DECAY_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("egd_growth_story",),
    "medium": ("egd_growth_story", "egd_decay_story", "egd_ivp"),
    "hard": ("egd_decay_story", "egd_ivp", "egd_doubling", "egd_half_life"),
    "expert": ("egd_doubling", "egd_half_life"),
}

_EGD_GROWTH_CONTEXTS = (
    ("A", "population", "people", "years"),
    ("A", "bacterial culture", "cells", "hours"),
    ("An", "investment", "dollars", "years"),
)
_EGD_DECAY_CONTEXTS = (
    ("A", "radioactive sample", "grams", "years"),
    ("A", "medicine dose", "mg", "hours"),
    ("A", "population", "people", "years"),
)


def growth_decay_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _GROWTH_DECAY_BANDS["easy"]
    if d < 16.0:
        return _GROWTH_DECAY_BANDS["medium"]
    if d < 20.0:
        return _GROWTH_DECAY_BANDS["hard"]
    return _GROWTH_DECAY_BANDS["expert"]


def _growth_decay_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [GROWTH_DECAY_GENERATOR],
        }
        for fid in forms
    ]


def _sample_egd_growth_story(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: story find y(t) from y'=ky (OpenStax Vol 1 §6.8)."""
    k = rng.randint(1, 3)
    y0 = rng.choice([10, 20, 50, 100])
    t = rng.randint(1, 3)
    art, name, unit, time_unit = rng.choice(_EGD_GROWTH_CONTEXTS)
    prompt = (
        rf"\text{{{art} {name} of }}{y0}\text{{ {unit} grows continuously according to }}"
        rf"y'={k}y.\text{{ Find }}y({t})\text{{ ({time_unit}).}}"
    )
    answer = rf"{y0}e^{{{k * t}}}"
    return AppDiffItem(
        prompt, answer, "continuous growth/decay", "egd_growth_story",
        {"k": k, "y0": y0, "t": t},
    )


def _sample_egd_decay_story(rng: random.Random) -> AppDiffItem:
    """Old exclusive D=8: story find y(t) from y'=-ky."""
    k = rng.randint(1, 3)
    y0 = rng.choice([80, 100, 200])
    t = rng.randint(1, 4)
    art, name, unit, time_unit = rng.choice(_EGD_DECAY_CONTEXTS)
    prompt = (
        rf"\text{{{art} {name} of }}{y0}\text{{ {unit} decays continuously according to }}"
        rf"y'=-{k}y.\text{{ Find }}y({t})\text{{ ({time_unit}).}}"
    )
    answer = rf"{y0}e^{{-{k * t}}}"
    return AppDiffItem(
        prompt, answer, "continuous growth/decay", "egd_decay_story",
        {"k": k, "y0": y0, "t": t},
    )


def _sample_egd_ivp(rng: random.Random) -> AppDiffItem:
    """Old exclusive D=8: solve y'=ky, y(0)=y0."""
    k = rng.randint(2, 4)
    y0 = rng.randint(2, 8)
    prompt = rf"\text{{Solve }}y'={k}y,\ y(0)={y0}."
    answer = rf"y={y0}e^{{{k}x}}"
    return AppDiffItem(
        prompt, answer, "continuous growth/decay", "egd_ivp",
        {"k": k, "y0": y0},
    )


def _sample_egd_doubling(rng: random.Random) -> AppDiffItem:
    """Old exclusive D≥16: amount after n doubling times."""
    y0 = rng.choice([50, 100, 200])
    n_dbl = rng.randint(2, 4)
    art, name, unit, _tu = rng.choice(_EGD_GROWTH_CONTEXTS)
    prompt = (
        rf"\text{{{art} {name} of }}{y0}\text{{ {unit} doubles continuously every }}"
        rf"T\text{{ years. How much is present after }}{n_dbl}T\text{{ years?}}"
    )
    answer = str(y0 * (2 ** n_dbl))
    return AppDiffItem(
        prompt, answer, "continuous growth/decay", "egd_doubling",
        {"y0": y0, "n": n_dbl},
    )


def _sample_egd_half_life(rng: random.Random) -> AppDiffItem:
    """Old exclusive D≥16: amount after n half-lives."""
    y0 = rng.choice([64, 128, 256])
    n_half = rng.randint(2, 4)
    art, name, unit, _tu = rng.choice(_EGD_DECAY_CONTEXTS)
    prompt = (
        rf"\text{{{art} {name} of }}{y0}\text{{ {unit} has continuous half-life }}"
        rf"T.\text{{ How much remains after }}{n_half}T?"
    )
    answer = str(y0 // (2 ** n_half))
    return AppDiffItem(
        prompt, answer, "continuous growth/decay", "egd_half_life",
        {"y0": y0, "n": n_half},
    )


_GROWTH_DECAY_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "egd_growth_story": _sample_egd_growth_story,
    "egd_decay_story": _sample_egd_decay_story,
    "egd_ivp": _sample_egd_ivp,
    "egd_doubling": _sample_egd_doubling,
    "egd_half_life": _sample_egd_half_life,
}


def sample_growth_decay(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Continuous y'=ky. High D locks out easy growth leftover, then mid IVP/decay."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = growth_decay_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _growth_decay_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _GROWTH_DECAY_BUILDERS:
        fid = forms[0]
    item = _GROWTH_DECAY_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": GROWTH_DECAY_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": GROWTH_DECAY_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


def sample_optimization(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """OpenStax §4.7 WP frames; ``form_id`` is the frame id for the live loop."""
    from question_engine.frameworks.primitives.optimization_frames import (
        optimization_frames_for_difficulty,
        optimization_live_metadata,
        sample_optimization_frame,
    )

    d = _d(settings)
    structure = calc_application_structure_from_continuous(settings)
    if structure is None:
        frames: tuple[str, ...] = ("rectangle_perimeter",)
    else:
        raw = structure.get("opt_frames")
        frames = tuple(str(f) for f in raw) if raw else optimization_frames_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    item = sample_optimization_frame(
        rng, frames=frames, d=d, quality_weights=quality_weights
    )
    meta = optimization_live_metadata(item)
    return AppDiffItem(
        item.prompt_latex,
        item.answer_latex,
        item.label,
        item.frame_id,
        meta,
    )


CURVE_SKETCH_GENERATOR = "curve_sketching"

_SKETCH_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("parabola_sketch",),
    "medium": ("parabola_sketch", "cubic_sketch_checklist"),
    "hard": ("cubic_sketch_checklist", "cubic_shifted_sketch"),
    "expert": ("cubic_shifted_sketch",),
}


def curve_sketch_forms_for_difficulty(d: float) -> tuple[str, ...]:
    if d < 8.0:
        return _SKETCH_BANDS["easy"]
    if d < 16.0:
        return _SKETCH_BANDS["medium"]
    if d < 20.0:
        return _SKETCH_BANDS["hard"]
    return _SKETCH_BANDS["expert"]


def _sketch_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [CURVE_SKETCH_GENERATOR],
        }
        for fid in forms
    ]


def _sample_parabola_sketch(rng: random.Random) -> AppDiffItem:
    """Old-path D=0: vertex + concavity of (x−h)²."""
    h = rng.randint(1, 4)
    prompt = (
        rf"\text{{For }}f(x)=(x-{h})^{{2}},\text{{ list the vertex "
        rf"and concavity.}}"
    )
    answer = rf"\text{{vertex }}({h},0);\text{{ concave up}}"
    return AppDiffItem(
        prompt, answer, "curve sketch", "parabola_sketch",
        {"h": h},
    )


def _sample_cubic_sketch_checklist(rng: random.Random) -> AppDiffItem:
    """Reuse ``_cubic_odd``: extrema at ±a, inflection at 0. Mid-D leftover."""
    a, c, body = _cubic_odd(rng)
    ymax, ymin = 2 * a**3 + c, -2 * a**3 + c
    prompt = (
        rf"\text{{For }}f(x)={body},\text{{ list relative extrema and "
        rf"the inflection point.}}"
    )
    answer = (
        rf"\text{{rel max }}{ymax}\text{{ at }}x={-a};"
        rf"\text{{ rel min }}{ymin}\text{{ at }}x={a};"
        rf"\text{{ inflection at }}x=0"
    )
    return AppDiffItem(
        prompt, answer, "curve sketch", "cubic_sketch_checklist",
        {"a": a, "c": c, "inflection": 0},
    )


def _sample_cubic_shifted_sketch(rng: random.Random) -> AppDiffItem:
    """Translate ``_cubic_odd`` so the inflection is at h≠0 (same idea as Ex. 4.19)."""
    a, k, _ = _cubic_odd(rng)
    h = rng.choice((-3, -2, -1, 1, 2, 3, 4))
    coeffs = [
        1,
        -3 * h,
        3 * h * h - 3 * a * a,
        -h**3 + 3 * a * a * h + k,
    ]
    body = _poly_body(coeffs)
    xmax, xmin = h - a, h + a
    ymax, ymin = 2 * a**3 + k, -2 * a**3 + k
    prompt = (
        rf"\text{{For }}f(x)={body},\text{{ list relative extrema and "
        rf"the inflection point.}}"
    )
    answer = (
        rf"\text{{rel max }}{ymax}\text{{ at }}x={xmax};"
        rf"\text{{ rel min }}{ymin}\text{{ at }}x={xmin};"
        rf"\text{{ inflection at }}x={h}"
    )
    return AppDiffItem(
        prompt, answer, "curve sketch", "cubic_shifted_sketch",
        {"a": a, "h": h, "k": k, "inflection": h},
    )


_SKETCH_BUILDERS: dict[str, Callable[[random.Random], AppDiffItem]] = {
    "parabola_sketch": _sample_parabola_sketch,
    "cubic_sketch_checklist": _sample_cubic_sketch_checklist,
    "cubic_shifted_sketch": _sample_cubic_shifted_sketch,
}


def sample_curve_sketching(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Checklist of vertex / extrema / inflection. High D locks out inflect-at-0."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = _d(settings)
    forms = curve_sketch_forms_for_difficulty(d)
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    form = select_form_id(
        _sketch_form_rows(forms), d=d, rng=rng, quality_weights=quality_weights
    )
    fid = str(form.get("form_id") or forms[0])
    if fid not in _SKETCH_BUILDERS:
        fid = forms[0]
    item = _SKETCH_BUILDERS[fid](rng)
    meta = {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": CURVE_SKETCH_GENERATOR,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": CURVE_SKETCH_GENERATOR,
        },
    }
    return AppDiffItem(
        item.prompt_latex, item.answer_latex, item.label, fid, meta
    )


def sample_related_rates(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """OpenStax §4.1 WP frames; ``form_id`` is the frame id for the live loop."""
    from question_engine.frameworks.primitives.related_rates_frames import (
        related_frames_for_difficulty,
        related_rates_live_metadata,
        sample_related_rates_frame,
    )

    d = _d(settings)
    structure = calc_application_structure_from_continuous(settings)
    if structure is None:
        frames: tuple[str, ...] = ("expanding_circle",)
        r_max, rate_max = 10, 5
    else:
        raw = structure.get("related_frames") or structure.get("related_shapes") or (
            "expanding_circle",
        )
        legacy = {
            "circle": "expanding_circle",
            "sphere": "expanding_sphere",
            "cone": "cone_similar",
        }
        frames = tuple(legacy.get(str(f), str(f)) for f in raw) or related_frames_for_difficulty(d)
        r_max = max(3, int(structure["radius_max"]))
        rate_max = max(1, int(structure["rate_max"]))
    qw = settings.get("live_quality_form_weights")
    quality_weights = qw if isinstance(qw, dict) else None
    item = sample_related_rates_frame(
        rng,
        frames=frames,
        r_max=r_max,
        rate_max=rate_max,
        d=d,
        quality_weights=quality_weights,
    )
    meta = related_rates_live_metadata(item)
    return AppDiffItem(
        item.prompt_latex,
        item.answer_latex,
        item.label,
        item.frame_id,
        meta,
    )


def sample_graphical_f_fp(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    """Sign-of-f' questions (no figure bank). OpenStax §4.5 skill without graphs."""
    d = _d(settings)
    if d < 8.0:
        c = rng.randint(1, 5)
        prompt = (
            rf"f'(x)=x-{c}.\text{{ On which interval is }}f\text{{ decreasing?}}"
        )
        answer = rf"(-\infty,{c})"
        return AppDiffItem(
            prompt, answer, "graphical f/f'", "fp_linear_sign",
            {"c": c},
        )
    a = rng.randint(1, 4)
    prompt = (
        rf"f'(x)=x^{{2}}-{a * a}.\text{{ On which intervals is }}f"
        rf"\text{{ increasing?}}"
    )
    answer = rf"(-\infty,{-a})\cup({a},\infty)"
    return AppDiffItem(
        prompt, answer, "graphical f/f'", "fp_quadratic_sign",
        {"a": a},
    )


_SAMPLERS: dict[Kind, Callable[[random.Random, dict[str, Any]], AppDiffItem]] = {
    "relative_extrema": sample_relative_extrema,
    "absolute_extrema": sample_absolute_extrema,
    "concavity": sample_concavity,
    "mean_value": sample_mean_value,
    "rolles": sample_rolles,
    "newtons_method": sample_newton,
    "motion": sample_motion,
    "motion_integral": sample_motion_integral,
    "de_intro": sample_de_intro,
    "slope_field": sample_slope_field,
    "separable": sample_separable_de,
    "growth_decay": sample_growth_decay,
    "optimization": sample_optimization,
    "increase_decrease": sample_intervals_increase,
    "curve_sketching": sample_curve_sketching,
    "graphical_f_fp": sample_graphical_f_fp,
    "related_rates": sample_related_rates,
    "differentials": sample_differentials,
    "linear_approximation": sample_linear_approximation,
}


def sample_app_diff(
    kind: Kind,
    settings: dict[str, Any],
    *,
    rng: random.Random | None = None,
) -> AppDiffItem:
    rng = rng or random.Random()
    return _SAMPLERS[kind](rng, settings)
