"""OpenStax-style related-rates story frames (Calc Vol 1 §4.1).

Rotate distinct geometry frames at the same D — not circle/sphere/cone only.
Algebra shapes stay solvable by one differentiation + plug-in.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class RelatedRatesItem:
    prompt_latex: str
    answer_latex: str
    label: str
    frame_id: str
    metadata: dict[str, Any]


def _circle_area(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    r = rng.randint(2, max(2, r_max))
    drdt = rng.randint(1, max(1, rate_max))
    # dA/dt = 2 π r dr/dt
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{The radius of a circle increases at }} {drdt}\text{{ cm/s. "
            rf"How fast is the area increasing when }} r = {r}\text{{ cm?}}"
        ),
        answer_latex=rf"{2 * r * drdt}\pi",
        label="related rates circle",
        frame_id="expanding_circle",
        metadata={"r": r, "drdt": drdt, "quantity": "area"},
    )


def _sphere_volume(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    r = rng.randint(2, max(2, r_max))
    drdt = rng.randint(1, max(1, rate_max))
    # dV/dt = 4 π r^2 dr/dt
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{The radius of a sphere increases at }} {drdt}\text{{ cm/s. "
            rf"How fast is the volume increasing when }} r = {r}\text{{ cm?}}"
        ),
        answer_latex=rf"{4 * r * r * drdt}\pi",
        label="related rates sphere",
        frame_id="expanding_sphere",
        metadata={"r": r, "drdt": drdt, "quantity": "volume"},
    )


def _balloon_radius(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    """OpenStax §4.1 balloon: volume rate given, find dr/dt."""
    r = rng.randint(2, max(2, min(8, r_max)))
    # Choose integer dV/dt so dr/dt = dV/(4π r^2) is a clean multiple of 1/π
    # dr/dt = k / (4 r^2) with answer (k/(4 r^2)) / π? Better: give dV/dt = 4π r^2 * m
    # so answer is m cm/s.
    m = rng.randint(1, max(1, rate_max))
    dvdt = 4 * r * r * m  # without π in the numeric coeff; prompt includes π
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{A spherical balloon is filled with air at }} "
            rf"{dvdt}\pi\text{{ cm}}^{{3}}\text{{/s. How fast is the radius "
            rf"increasing when }} r = {r}\text{{ cm?}}"
        ),
        answer_latex=str(m),
        label="related rates balloon",
        frame_id="balloon_radius",
        metadata={"r": r, "dvdt_over_pi": dvdt, "drdt": m, "quantity": "radius"},
    )


def _cone_similar(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    """Cone with fixed similar-shape ratio h = k r (old path used k=3)."""
    k = rng.choice([2, 3, 4])
    r = rng.randint(2, max(2, r_max))
    drdt = rng.randint(1, max(1, rate_max))
    # V = (1/3)π r^2 h = (1/3)π r^2 (k r) = (k/3) π r^3
    # dV/dt = k π r^2 dr/dt
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{A cone keeps }} h={k}r\text{{ while the radius increases at }} "
            rf"{drdt}\text{{ cm/s. How fast is the volume increasing when }} "
            rf"r = {r}\text{{ cm?}}"
        ),
        answer_latex=rf"{k * r * r * drdt}\pi",
        label="related rates cone",
        frame_id="cone_similar",
        metadata={"r": r, "drdt": drdt, "k": k, "quantity": "volume"},
    )


def _ladder(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    """Sliding ladder / Pythagorean related rates (OpenStax ladder shape)."""
    # Choose 3-4-5 style so height stays integer: L^2 = x^2 + y^2
    triples = ((5, 3, 4), (10, 6, 8), (13, 5, 12), (15, 9, 12), (25, 7, 24), (25, 15, 20))
    # Filter by size vs r_max (use x as "base" span proxy)
    pool = [t for t in triples if t[1] <= max(5, r_max + 2)] or list(triples)
    L, x, y = rng.choice(pool)
    dxdt = rng.randint(1, max(1, rate_max))
    # x dx/dt + y dy/dt = 0 → dy/dt = -(x/y) dx/dt
    # answer magnitude as positive "sliding down" rate
    # Keep fraction if needed
    num = x * dxdt
    den = y
    g = math.gcd(num, den)
    num //= g
    den //= g
    if den == 1:
        ans = str(num)
    else:
        ans = rf"\frac{{{num}}}{{{den}}}"
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{A }}{L}\text{{-ft ladder leans against a wall. The base slides "
            rf"away at }} {dxdt}\text{{ ft/s. How fast is the top sliding down when "
            rf"the base is }} {x}\text{{ ft from the wall?}}"
        ),
        answer_latex=ans,
        label="related rates ladder",
        frame_id="sliding_ladder",
        metadata={"L": L, "x": x, "y": y, "dxdt": dxdt, "quantity": "height_rate"},
    )


def _shadow(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    """Person walking away from a lamp post — tip of shadow (similar triangles)."""
    # Lamp height H, person height h, distance from post x, shadow length s
    # H / (x+s) = h / s → tip rate d(x+s)/dt = H/(H-h) · dx/dt
    H = rng.choice([12, 15, 16, 18, 20])
    h = rng.choice([5, 6])
    if H <= h:
        H = h + 6
    dxdt = rng.randint(2, max(2, rate_max + 1))
    x = rng.randint(4, max(4, r_max + 2))
    tip_num = H * dxdt
    tip_den = H - h
    g = math.gcd(tip_num, tip_den)
    tip_num //= g
    tip_den //= g
    ans = str(tip_num) if tip_den == 1 else rf"\frac{{{tip_num}}}{{{tip_den}}}"
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{A }}{H}\text{{-ft lamp post casts a shadow of a }}{h}\text{{-ft "
            rf"person walking away at }} {dxdt}\text{{ ft/s. How fast is the tip of "
            rf"the shadow moving away from the post when the person is }} {x}"
            rf"\text{{ ft from the post?}}"
        ),
        answer_latex=ans,
        label="related rates shadow",
        frame_id="lamp_shadow",
        metadata={
            "H": H,
            "h": h,
            "x": x,
            "dxdt": dxdt,
            "quantity": "shadow_tip_rate",
        },
    )


def _airplane(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    """Airplane at constant elevation; ground distance related to slant range."""
    # Elevation h fixed, ground distance x, slant s: s^2 = x^2 + h^2
    # 2 s ds/dt = 2 x dx/dt → ds/dt = (x/s) dx/dt
    triples = ((5, 3, 4), (10, 6, 8), (13, 5, 12), (15, 9, 12), (25, 7, 24))
    pool = [t for t in triples if t[2] <= max(8, r_max + 4)] or list(triples)
    s, x, h = rng.choice(pool)
    dxdt = rng.randint(2, max(2, rate_max + 2)) * 100  # mph-ish scale optional
    # Keep numbers modest: use ft/s style small ints
    dxdt = rng.randint(2, max(2, rate_max + 2))
    num = x * dxdt
    den = s
    g = math.gcd(num, den)
    num //= g
    den //= g
    ans = str(num) if den == 1 else rf"\frac{{{num}}}{{{den}}}"
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{An airplane flies at a constant elevation of }} {h}\text{{ km. "
            rf"A spotter is }} {x}\text{{ km horizontally from the point on the ground "
            rf"directly below the plane. If the plane's horizontal speed is }} "
            rf"{dxdt}\text{{ km/s, how fast is the distance from the spotter to the "
            rf"plane changing?}}"
        ),
        answer_latex=ans,
        label="related rates airplane",
        frame_id="airplane_distance",
        metadata={"s": s, "x": x, "h": h, "dxdt": dxdt, "quantity": "slant_rate"},
    )


_FRAME_BUILDERS: dict[str, Callable[..., RelatedRatesItem]] = {
    "expanding_circle": _circle_area,
    "expanding_sphere": _sphere_volume,
    "balloon_radius": _balloon_radius,
    "cone_similar": _cone_similar,
    "sliding_ladder": _ladder,
    "lamp_shadow": _shadow,
    "airplane_distance": _airplane,
}


# D-band unlocks (OpenStax §4.1 rotation). D=0 stays circle-only (old easy).
FRAME_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("expanding_circle",),
    "medium": ("expanding_circle", "expanding_sphere", "balloon_radius"),
    "hard": (
        "expanding_circle",
        "expanding_sphere",
        "balloon_radius",
        "cone_similar",
        "sliding_ladder",
        "lamp_shadow",
        "airplane_distance",
    ),
}


def sample_related_rates_frame(
    rng: random.Random,
    *,
    frames: tuple[str, ...],
    r_max: int = 5,
    rate_max: int = 3,
) -> RelatedRatesItem:
    allowed = [f for f in frames if f in _FRAME_BUILDERS]
    if not allowed:
        allowed = ["expanding_circle"]
    frame_id = rng.choice(allowed)
    return _FRAME_BUILDERS[frame_id](rng, r_max=r_max, rate_max=rate_max)
