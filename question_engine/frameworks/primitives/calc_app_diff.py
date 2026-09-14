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

from question_engine.generators.utils import format_polynomial_latex, frac_latex
from question_engine.settings.params import calc_application_structure_from_continuous

Kind = Literal[
    "relative_extrema",
    "absolute_extrema",
    "concavity",
    "newtons_method",
    "motion",
    "motion_integral",
    "de_intro",
    "optimization",
    "increase_decrease",
    "curve_sketching",
    "graphical_f_fp",
    "related_rates",
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


def sample_relative_extrema(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    d = _d(settings)
    if d < 8.0:
        h = rng.randint(1, 5)
        k = rng.randint(1, 6)
        prompt = rf"\text{{Find the relative minimum of }}f(x)=(x-{h})^{{2}}-{k}."
        answer = rf"\text{{relative minimum }}-{k}\text{{ at }}x={h}"
        return AppDiffItem(
            prompt, answer, "relative extrema", "parabola_vertex",
            {"h": h, "k": k},
        )
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


def sample_absolute_extrema(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    d = _d(settings)
    if d < 8.0:
        b = rng.randint(2, 5)
        prompt = (
            rf"\text{{Find the absolute extrema of }}f(x)=x^{{2}}"
            rf"\text{{ on }}[0,{b}]."
        )
        answer = (
            rf"\text{{abs min }}0\text{{ at }}x=0;"
            rf"\text{{ abs max }}{b * b}\text{{ at }}x={b}"
        )
        return AppDiffItem(
            prompt, answer, "absolute extrema", "closed_interval_parabola",
            {"b": b},
        )
    a, c, body = _cubic_odd(rng)
    lo, hi = -2 * a, 2 * a
    f_lo = (lo**3) - 3 * a * a * lo + c
    f_hi = (hi**3) - 3 * a * a * hi + c
    f_neg = 2 * a**3 + c  # at -a
    f_pos = -2 * a**3 + c  # at a
    vals = {lo: f_lo, -a: f_neg, a: f_pos, hi: f_hi}
    mn = min(vals.values())
    mx = max(vals.values())
    xmin = [x for x, v in vals.items() if v == mn][0]
    xmax = [x for x, v in vals.items() if v == mx][0]
    prompt = (
        rf"\text{{Find the absolute extrema of }}f(x)={body}"
        rf"\text{{ on }}[{lo},{hi}]."
    )
    answer = (
        rf"\text{{abs min }}{mn}\text{{ at }}x={xmin};"
        rf"\text{{ abs max }}{mx}\text{{ at }}x={xmax}"
    )
    return AppDiffItem(
        prompt, answer, "absolute extrema", "closed_interval_cubic",
        {"a": a, "interval": (lo, hi)},
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
    p, q = rng.choice(((-1, 3), (-2, 4), (-3, 1), (-4, 2), (-1, 5), (-5, 1)))
    c = rng.choice([0, 1, -1, -2])
    a_coef = (3 * (p + q)) // 2
    b_coef = 3 * p * q
    body = _poly_body([1, -a_coef, b_coef, c])
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


def sample_concavity(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    d = _d(settings)
    if d < 8.0:
        p = rng.choice([3, 5])
        prompt = (
            rf"\text{{Determine the concavity of }}f(x)=x^{{{p}}}"
            rf"\text{{ on }}(0,\infty)."
        )
        return AppDiffItem(
            prompt, r"\text{concave up}", "concavity", "odd_power_positive_ray",
            {"p": p},
        )
    a, c, body = _cubic_odd(rng)
    prompt = rf"\text{{Find the intervals of concavity of }}f(x)={body}."
    answer = (
        r"\text{concave down on }(-\infty,0);\text{ concave up on }(0,\infty)"
    )
    return AppDiffItem(
        prompt, answer, "concavity", "cubic_second_derivative",
        {"a": a, "inflection": 0},
    )


def sample_newton(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    d = _d(settings)
    if d < 10.0:
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
    a = rng.choice([2, 3, 5, 7, 10])
    x0 = rng.choice([1, 2])
    if x0**3 == a:
        x0 = 1
    fx = x0**3 - a
    fpx = 3 * x0 * x0
    x1 = Fraction(x0) - Fraction(fx, fpx)
    steps = 2 if d >= 16.0 else 1
    if steps == 1:
        prompt = (
            rf"\text{{Use one Newton step for }}f(x)=x^{{3}}-{a}"
            rf"\text{{ from }}x_0={x0}."
        )
        return AppDiffItem(
            prompt, rf"x_1={frac_latex(x1)}", "Newton", "newton_one_cubic",
            {"steps": 1, "x0": x0, "a": a},
        )
    # Second iterate from x1 (rational).
    x1n, x1d = x1.numerator, x1.denominator
    # f(x1)=x1^3-a, f'(x1)=3 x1^2
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


def sample_motion(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    d = _d(settings)
    n = rng.randint(2, 6)
    if d < 8.0:
        prompt = rf"s(t)=t^{{2}}-{n}t.\quad\text{{Find }}v({n})."
        return AppDiffItem(
            prompt, str(n), "motion", "eval_velocity",
            {"n": n, "ask": "v"},
        )
    if d < 16.0:
        # v=2t-n = 0 at t=n/2; require even n
        n = rng.choice([2, 4, 6])
        prompt = rf"s(t)=t^{{2}}-{n}t.\quad\text{{When is the particle at rest?}}"
        t_rest = frac_latex(Fraction(n, 2))
        return AppDiffItem(
            prompt, rf"t={t_rest}", "motion", "particle_at_rest",
            {"n": n, "ask": "rest"},
        )
    prompt = rf"s(t)=t^{{2}}-{n}t.\quad\text{{Find }}a(t)."
    return AppDiffItem(
        prompt, "2", "motion", "acceleration_const",
        {"n": n, "ask": "a"},
    )


def sample_motion_integral(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    d = _d(settings)
    b = rng.randint(2, 5)
    if d < 8.0:
        prompt = (
            rf"v(t)=2t.\quad\text{{Find the displacement from }}t=0\text{{ to }}t={b}."
        )
        return AppDiffItem(
            prompt, str(b * b), "motion integral", "disp_linear_v",
            {"b": b},
        )
    if d < 16.0:
        prompt = (
            rf"v(t)={b}.\quad\text{{Find the displacement from }}t=0\text{{ to }}t={b}."
        )
        return AppDiffItem(
            prompt, str(b * b), "motion integral", "disp_const_v",
            {"b": b},
        )
    # v=2t-2c changes sign at t=c; displacement on [0,2c]
    c = rng.randint(1, 3)
    # s(t)=t^2-2c t, disp = s(2c)-s(0)=0
    prompt = (
        rf"v(t)=2t-{2 * c}.\quad\text{{Find the displacement from }}"
        rf"t=0\text{{ to }}t={2 * c}."
    )
    return AppDiffItem(
        prompt, "0", "motion integral", "disp_sign_change",
        {"c": c, "note": "net displacement zero"},
    )


def sample_de_intro(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    d = _d(settings)
    if d < 8.0:
        k = rng.randint(2, 5)
        prompt = rf"\text{{Verify that }}y=Ce^{{{k}x}}\text{{ solves }}y'={k}y."
        answer = rf"y'={k}Ce^{{{k}x}}={k}y"
        return AppDiffItem(
            prompt, answer, "DE intro", "verify_exp",
            {"k": k},
        )
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


def sample_curve_sketching(rng: random.Random, settings: dict[str, Any]) -> AppDiffItem:
    d = _d(settings)
    if d < 8.0:
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
        {"a": a},
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
    "newtons_method": sample_newton,
    "motion": sample_motion,
    "motion_integral": sample_motion_integral,
    "de_intro": sample_de_intro,
    "optimization": sample_optimization,
    "increase_decrease": sample_intervals_increase,
    "curve_sketching": sample_curve_sketching,
    "graphical_f_fp": sample_graphical_f_fp,
    "related_rates": sample_related_rates,
}


def sample_app_diff(
    kind: Kind,
    settings: dict[str, Any],
    *,
    rng: random.Random | None = None,
) -> AppDiffItem:
    rng = rng or random.Random()
    return _SAMPLERS[kind](rng, settings)
