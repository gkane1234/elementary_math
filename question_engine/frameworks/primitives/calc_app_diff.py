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

from question_engine.generators.utils import frac_latex
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
    "curve_sketching",
    "graphical_f_fp",
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
    structure = calc_application_structure_from_continuous(settings)
    frames = tuple(structure["opt_frames"]) if structure and structure.get("opt_frames") else ("rectangle_perimeter",)
    d = _d(settings)
    if d < 8.0:
        frames = ("rectangle_perimeter",)
    elif d < 16.0:
        frames = ("rectangle_perimeter", "garden_three_sides")
    else:
        frames = ("garden_three_sides", "open_box")
    fid = rng.choice(frames)
    if fid == "rectangle_perimeter":
        peri = 4 * rng.randint(3, 12)
        side = peri // 4
        prompt = (
            rf"\text{{A rectangle has perimeter }}{peri}."
            rf"\text{{ What dimensions maximize area?}}"
        )
        return AppDiffItem(
            prompt, f"{side} by {side}", "optimization", "rectangle_perimeter",
            {"frame_id": fid, "peri": peri},
        )
    if fid == "garden_three_sides":
        # Fence L on three sides; max area at width L/4, length L/2.
        L = 4 * rng.randint(4, 10)
        w, ell = L // 4, L // 2
        prompt = (
            rf"\text{{A rectangular garden uses a wall as one side and }}"
            rf"{L}\text{{ ft of fence for the other three. What dimensions maximize area?}}"
        )
        return AppDiffItem(
            prompt, rf"{w}\text{{ (sides) by }}{ell}\text{{ (along wall)}}",
            "optimization", "garden_three_sides",
            {"frame_id": fid, "L": L},
        )
    # open box from square sheet, cut x, V=x(S-2x)^2, x=S/6
    S = 6 * rng.randint(2, 5)
    x = S // 6
    vol = (2 * S**3) // 27
    prompt = (
        rf"\text{{An open box is made from a }}{S}\text{{ by }}{S}"
        rf"\text{{ square sheet by cutting equal squares from each corner. "
        rf"What cut size }}x\text{{ maximizes volume?}}"
    )
    return AppDiffItem(
        prompt, str(x), "optimization", "open_box",
        {"frame_id": fid, "S": S, "V": vol},
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
    "curve_sketching": sample_curve_sketching,
    "graphical_f_fp": sample_graphical_f_fp,
}


def sample_app_diff(
    kind: Kind,
    settings: dict[str, Any],
    *,
    rng: random.Random | None = None,
) -> AppDiffItem:
    rng = rng or random.Random()
    return _SAMPLERS[kind](rng, settings)
