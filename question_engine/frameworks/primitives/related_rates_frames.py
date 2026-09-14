"""OpenStax-style related-rates story frames (Calc Vol 1 §4.1).

Rotate distinct geometry frames at the same D — not circle/sphere/cone only.
Algebra shapes stay closed-form (differentiate + plug). High D adds chain
(similar-triangle inverse, two given rates, angle) rather than padded costs.
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


def _frac(num: int, den: int) -> str:
    g = math.gcd(num, den)
    num //= g
    den //= g
    if den < 0:
        num, den = -num, -den
    if den == 1:
        return str(num)
    return rf"\frac{{{num}}}{{{den}}}"


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
    # Give dV/dt = 4π r^2 * m so the answer is m cm/s.
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
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{A }}{L}\text{{-ft ladder leans against a wall. The base slides "
            rf"away at }} {dxdt}\text{{ ft/s. How fast is the top sliding down when "
            rf"the base is }} {x}\text{{ ft from the wall?}}"
        ),
        answer_latex=_frac(x * dxdt, y),
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
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{A }}{H}\text{{-ft lamp post casts a shadow of a }}{h}\text{{-ft "
            rf"person walking away at }} {dxdt}\text{{ ft/s. How fast is the tip of "
            rf"the shadow moving away from the post when the person is }} {x}"
            rf"\text{{ ft from the post?}}"
        ),
        answer_latex=_frac(H * dxdt, H - h),
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
    dxdt = rng.randint(2, max(2, rate_max + 2))
    return RelatedRatesItem(
        prompt_latex=(
            rf"\text{{An airplane flies at a constant elevation of }} {h}\text{{ km. "
            rf"A spotter is }} {x}\text{{ km horizontally from the point on the ground "
            rf"directly below the plane. If the plane's horizontal speed is }} "
            rf"{dxdt}\text{{ km/s, how fast is the distance from the spotter to the "
            rf"plane changing?}}"
        ),
        answer_latex=_frac(x * dxdt, s),
        label="related rates airplane",
        frame_id="airplane_distance",
        metadata={"s": s, "x": x, "h": h, "dxdt": dxdt, "quantity": "slant_rate"},
    )


def _cone_drain(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    """Inverse similar-triangle cone: given dV/dt, find dh/dt (OpenStax gravel/funnel)."""
    k = rng.choice([2, 3, 4])
    h = rng.randint(2, max(2, min(8, r_max)))
    m = rng.randint(1, max(1, rate_max))
    # V = (1/3)π r^2 h with r = k h → V = (k^2/3) π h^3
    # dV/dt = k^2 π h^2 dh/dt. Give dV/dt = n π with n = k^2 h^2 m so dh/dt = m.
    n = k * k * h * h * m
    if rng.choice([True, False]):
        prompt = (
            rf"\text{{Gravel falls onto a conical pile with radius }} {k}\text{{ times "
            rf"the height at }} {n}\pi\text{{ ft}}^{{3}}\text{{/min. How fast is the "
            rf"height increasing when }} h = {h}\text{{ ft?}}"
        )
        story = "gravel"
    else:
        prompt = (
            rf"\text{{Water drains from a conical tank (similar shape, }} r={k}h\text{{) "
            rf"at }} {n}\pi\text{{ ft}}^{{3}}\text{{/s. How fast is the water height "
            rf"falling when }} h = {h}\text{{ ft?}}"
        )
        story = "funnel"
    return RelatedRatesItem(
        prompt_latex=prompt,
        answer_latex=str(m),
        label="related rates cone drain",
        frame_id="cone_drain",
        metadata={
            "k": k,
            "h": h,
            "dvdt_over_pi": n,
            "dhdt": m,
            "story": story,
            "quantity": "height_rate",
        },
    )


def _two_rate_distance(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    """Two given rates on a right triangle (OpenStax bikes / planes / helicopter)."""
    triples = ((5, 3, 4), (10, 6, 8), (13, 5, 12), (15, 9, 12), (25, 7, 24), (25, 15, 20))
    pool = [t for t in triples if t[1] <= max(5, r_max + 2)] or list(triples)
    s, x, y = rng.choice(pool)
    dxdt = rng.randint(2, max(2, rate_max + 1))
    dydt = rng.randint(2, max(2, rate_max + 1))
    # s^2 = x^2 + y^2 → ds/dt = (x dx/dt + y dy/dt) / s
    ans = _frac(x * dxdt + y * dydt, s)
    kind = rng.choice(["bikes", "cars", "planes", "helicopter"])
    if kind == "bikes":
        prompt = (
            rf"\text{{Two bicyclists leave the same intersection, one riding east at }} "
            rf"{dxdt}\text{{ mph and the other north at }} {dydt}\text{{ mph. How fast "
            rf"is the distance between them changing when they are }} {x}\text{{ mi "
            rf"east and }} {y}\text{{ mi north of the intersection?}}"
        )
    elif kind == "cars":
        prompt = (
            rf"\text{{Two cars leave an intersection, one east at }} {dxdt}\text{{ mi/h "
            rf"and one north at }} {dydt}\text{{ mi/h. How fast is the distance between "
            rf"the cars changing when they are }} {x}\text{{ mi east and }} {y}"
            rf"\text{{ mi north of the intersection?}}"
        )
    elif kind == "planes":
        prompt = (
            rf"\text{{Airplane A flies east at }} {dxdt}\text{{ mi/h and airplane B flies "
            rf"north at }} {dydt}\text{{ mi/h, both at the same altitude. When A is }} "
            rf"{x}\text{{ mi east of an airport and B is }} {y}\text{{ mi north of it, "
            rf"how fast is the distance between the airplanes changing?}}"
        )
    else:
        prompt = (
            rf"\text{{A helicopter rises at }} {dydt}\text{{ ft/s while you run along the "
            rf"ground at }} {dxdt}\text{{ ft/s starting from under it. How fast is the "
            rf"distance between you changing when the helicopter is }} {y}\text{{ ft up "
            rf"and you are }} {x}\text{{ ft away?}}"
        )
    return RelatedRatesItem(
        prompt_latex=prompt,
        answer_latex=ans,
        label="related rates two-rate distance",
        frame_id="two_rate_distance",
        metadata={
            "s": s,
            "x": x,
            "y": y,
            "dxdt": dxdt,
            "dydt": dydt,
            "story": kind,
            "quantity": "slant_rate",
        },
    )


def _rocket_angle(rng: random.Random, *, r_max: int, rate_max: int) -> RelatedRatesItem:
    """Elevation angle of a rocket/camera (OpenStax Example 4.3 / ex. 38)."""
    # x fixed, h changing, θ = arctan(h/x) → dθ/dt = x/(x^2+h^2) · dh/dt = x dh/dt / s^2
    triples = ((3, 4, 5), (5, 12, 13), (8, 6, 10), (9, 12, 15), (7, 24, 25))
    pool = [t for t in triples if t[0] <= max(8, r_max + 4)] or list(triples)
    x, h, s = rng.choice(pool)
    dhdt = rng.randint(2, max(2, rate_max + 2))
    ans = _frac(x * dhdt, s * s)
    if rng.choice([True, False]):
        prompt = (
            rf"\text{{A rocket rises vertically. A camera }} {x}\text{{ ft from the "
            rf"launch pad stays aimed at the rocket. When the rocket is }} {h}\text{{ ft "
            rf"up, its speed is }} {dhdt}\text{{ ft/s. How fast is the camera's elevation "
            rf"angle changing?}}"
        )
        story = "rocket"
    else:
        prompt = (
            rf"\text{{A bottle rocket rises at }} {dhdt}\text{{ ft/s. You stand }} "
            rf"{x}\text{{ ft from the launch point. How fast is the angle of elevation "
            rf"changing when the rocket is }} {h}\text{{ ft in the air?}}"
        )
        story = "bottle_rocket"
    return RelatedRatesItem(
        prompt_latex=prompt,
        answer_latex=ans,
        label="related rates rocket angle",
        frame_id="rocket_angle",
        metadata={
            "x": x,
            "h": h,
            "s": s,
            "dhdt": dhdt,
            "story": story,
            "quantity": "angle_rate",
        },
    )


_FRAME_BUILDERS: dict[str, Callable[..., RelatedRatesItem]] = {
    "expanding_circle": _circle_area,
    "expanding_sphere": _sphere_volume,
    "balloon_radius": _balloon_radius,
    "cone_similar": _cone_similar,
    "sliding_ladder": _ladder,
    "lamp_shadow": _shadow,
    "airplane_distance": _airplane,
    "cone_drain": _cone_drain,
    "two_rate_distance": _two_rate_distance,
    "rocket_angle": _rocket_angle,
}

# Shared live-loop model key: every related-rates story updates this generator.
RELATED_RATES_GENERATOR = "related_rates_simple"

# D-band unlocks (OpenStax §4.1 rotation). D=0 stays circle-only (old easy).
# Easy leftovers lock out at higher bands (same idea as PFD d_max).
FRAME_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("expanding_circle",),
    "medium": ("expanding_circle", "expanding_sphere", "balloon_radius"),
    "hard": ("balloon_radius", "cone_similar", "sliding_ladder"),
    "very_hard": (
        "sliding_ladder",
        "lamp_shadow",
        "airplane_distance",
        "cone_drain",
    ),
    "expert": (
        "lamp_shadow",
        "airplane_distance",
        "cone_drain",
        "two_rate_distance",
        "rocket_angle",
    ),
}

# Catalog-shaped rows for ``select_form_id``. D gates match ``related_frames_for_difficulty``.
# Not a JSON ``openstax_form_catalogs/*.json`` — WP Python frames, same picker API.
_FRAME_D_GATES: dict[str, tuple[float, float | None]] = {
    "expanding_circle": (0.0, 9.999),
    "expanding_sphere": (4.0, 9.999),
    "balloon_radius": (4.0, 15.999),
    "cone_similar": (10.0, 15.999),
    "sliding_ladder": (10.0, 19.999),
    "lamp_shadow": (16.0, None),
    "airplane_distance": (16.0, None),
    "cone_drain": (16.0, None),
    "two_rate_distance": (20.0, None),
    "rocket_angle": (20.0, None),
}


def related_frames_for_difficulty(d: float) -> tuple[str, ...]:
    """Map continuous D → OpenStax §4.1 frames. Easy leftovers lock out at high D."""
    if d < 4.0:
        return FRAME_BANDS["easy"]
    if d < 10.0:
        return FRAME_BANDS["medium"]
    if d < 16.0:
        return FRAME_BANDS["hard"]
    if d < 20.0:
        return FRAME_BANDS["very_hard"]
    return FRAME_BANDS["expert"]


def related_rates_form_rows(
    frames: tuple[str, ...] | list[str],
    *,
    apply_d_gates: bool = False,
) -> list[dict[str, Any]]:
    """In-memory ``select_form_id`` rows. Pre-filtered pools keep equal D-weights."""
    rows: list[dict[str, Any]] = []
    for fid in frames:
        if fid not in _FRAME_BUILDERS:
            continue
        d_min, d_max = _FRAME_D_GATES.get(str(fid), (0.0, None))
        row: dict[str, Any] = {
            "form_id": str(fid),
            "d_min": float(d_min) if apply_d_gates else 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [RELATED_RATES_GENERATOR],
        }
        if apply_d_gates and d_max is not None:
            row["d_max"] = float(d_max)
        rows.append(row)
    return rows


def related_rates_live_metadata(item: RelatedRatesItem) -> dict[str, Any]:
    """Stamp live-loop keys: ``form_id`` = frame id, shared ``generator``."""
    fid = str(item.frame_id)
    return {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": RELATED_RATES_GENERATOR,
        "frame_id": fid,
        "related_rates_frame": fid,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": RELATED_RATES_GENERATOR,
        },
    }


def sample_related_rates_frame(
    rng: random.Random,
    *,
    frames: tuple[str, ...],
    r_max: int = 5,
    rate_max: int = 3,
    d: float = 0.0,
    quality_weights: dict[str, float] | None = None,
) -> RelatedRatesItem:
    """Pick a D-eligible OpenStax frame via ``select_form_id`` (live quality tilt)."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    allowed = [f for f in frames if f in _FRAME_BUILDERS]
    if not allowed:
        allowed = ["expanding_circle"]
    pool = related_rates_form_rows(allowed, apply_d_gates=False)
    form = select_form_id(
        pool, d=float(d), rng=rng, quality_weights=quality_weights
    )
    frame_id = str(form.get("form_id") or allowed[0])
    if frame_id not in _FRAME_BUILDERS:
        frame_id = allowed[0]
    return _FRAME_BUILDERS[frame_id](rng, r_max=r_max, rate_max=rate_max)
