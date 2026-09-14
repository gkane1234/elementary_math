"""OpenStax-style applied-optimization story frames (Calc Vol 1 §4.7).

Rotate distinct frames at the same D — not rectangle-perimeter only.
Algebra stays closed-form (known max from a first-derivative critical point).
High D locks out easy leftovers and unlocks inscribed / cylinder / revenue.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class OptimizationItem:
    prompt_latex: str
    answer_latex: str
    label: str
    frame_id: str
    metadata: dict[str, Any]


OPTIMIZATION_GENERATOR = "optimization_applied"


def _n_sqrt2(n: int) -> str:
    if n == 1:
        return r"\sqrt{2}"
    if n == -1:
        return r"-\sqrt{2}"
    return rf"{n}\sqrt{{2}}"


def _rectangle_perimeter(rng: random.Random) -> OptimizationItem:
    """Ex. 319 cattle pen / old D=0: max area given perimeter is a square."""
    n = rng.randint(3, 12)
    peri = 4 * n
    if rng.choice([True, False]):
        prompt = (
            rf"\text{{A rectangle has perimeter }}{peri}."
            rf"\text{{ What dimensions maximize area?}}"
        )
        story = "generic_rectangle"
    else:
        prompt = (
            rf"\text{{You have }}{peri}\text{{ ft of fencing to construct a "
            rf"rectangular pen. What dimensions maximize the area?}}"
        )
        story = "cattle_pen"
    return OptimizationItem(
        prompt_latex=prompt,
        answer_latex=f"{n} by {n}",
        label="optimization",
        frame_id="rectangle_perimeter",
        metadata={"peri": peri, "side": n, "story": story},
    )


def _garden_three_sides(rng: random.Random) -> OptimizationItem:
    """Ex. 4.32 garden+wall / Ex. 320 river: fence on three sides."""
    n = rng.randint(4, 10)
    L = 4 * n
    w, ell = n, 2 * n
    if rng.choice([True, False]):
        prompt = (
            rf"\text{{A rectangular garden uses a wall as one side and }}"
            rf"{L}\text{{ ft of fence for the other three. What dimensions maximize area?}}"
        )
        answer = rf"{w}\text{{ (sides) by }}{ell}\text{{ (along wall)}}"
        story = "garden_wall"
    else:
        prompt = (
            rf"\text{{You have }}{L}\text{{ ft of fencing to make a rectangular pen "
            rf"along a river (no fence on the river side). What dimensions maximize area?}}"
        )
        answer = rf"{w}\text{{ (sides) by }}{ell}\text{{ (along river)}}"
        story = "river_pen"
    return OptimizationItem(
        prompt_latex=prompt,
        answer_latex=answer,
        label="optimization",
        frame_id="garden_three_sides",
        metadata={"L": L, "w": w, "ell": ell, "story": story},
    )


def _open_box(rng: random.Random) -> OptimizationItem:
    """Square sheet, cut equal corners (square case of Ex. 4.33). x=S/6."""
    n = rng.randint(2, 5)
    S = 6 * n
    prompt = (
        rf"\text{{An open box is made from a }}{S}\text{{ by }}{S}"
        rf"\text{{ square sheet by cutting equal squares from each corner. "
        rf"What cut size }}x\text{{ maximizes volume?}}"
    )
    return OptimizationItem(
        prompt_latex=prompt,
        answer_latex=str(n),
        label="optimization",
        frame_id="open_box",
        metadata={"S": S, "x": n},
    )


def _open_box_rect(rng: random.Random) -> OptimizationItem:
    """Ex. 4.33 rectangular sheet 24×36 (and integer scale). Cut x=6k."""
    k = rng.choice([1, 2])
    L, W, x = 24 * k, 36 * k, 6 * k
    prompt = (
        rf"\text{{An open-top box is made from a }}{L}\text{{ in. by }}{W}"
        rf"\text{{ in. sheet by cutting equal squares from each corner. "
        rf"What cut size }}x\text{{ maximizes volume?}}"
    )
    return OptimizationItem(
        prompt_latex=prompt,
        answer_latex=str(x),
        label="optimization",
        frame_id="open_box_rect",
        metadata={"L": L, "W": W, "x": x},
    )


def _linear_revenue(rng: random.Random) -> OptimizationItem:
    """Ex. 4.35 / Checkpoint 4.34: R(p)=p(N-kp), max at p=N/(2k)."""
    k, m = rng.choice(((5, 100), (5, 75), (4, 50), (2, 80), (5, 60)))
    n0 = 2 * k * m
    prompt = (
        rf"\text{{A rental company rents }}n(p)={n0}-{k}p\text{{ cars per day "
        rf"at price }}p\text{{ dollars. What price maximizes revenue }}R=p\,n(p)?"
    )
    return OptimizationItem(
        prompt_latex=prompt,
        answer_latex=str(m),
        label="optimization",
        frame_id="linear_revenue",
        metadata={"N": n0, "k": k, "p_star": m},
    )


def _inscribed_ellipse(rng: random.Random) -> OptimizationItem:
    """Ex. 4.36 ellipse / Checkpoint 4.35 circle: max inscribed rectangle."""
    if rng.choice([True, False]):
        r = rng.choice([1, 2, 3, 5])
        prompt = (
            rf"\text{{A rectangle is inscribed in the circle }}x^{{2}}+y^{{2}}={r * r}."
            rf"\text{{ What dimensions maximize its area?}}"
        )
        side = _n_sqrt2(r)
        answer = rf"{side}\text{{ by }}{side}"
        meta: dict[str, Any] = {"a": r, "b": r, "shape": "circle"}
    else:
        a, b = rng.choice(((2, 1), (4, 2), (3, 1), (4, 1)))
        prompt = (
            rf"\text{{A rectangle is inscribed in the ellipse }}"
            rf"\frac{{x^{{2}}}}{{{a * a}}}+\frac{{y^{{2}}}}{{{b * b}}}=1."
            rf"\text{{ What dimensions maximize its area?}}"
        )
        answer = rf"{_n_sqrt2(a)}\text{{ by }}{_n_sqrt2(b)}"
        meta = {"a": a, "b": b, "shape": "ellipse"}
    return OptimizationItem(
        prompt_latex=prompt,
        answer_latex=answer,
        label="optimization",
        frame_id="inscribed_ellipse",
        metadata=meta,
    )


def _closed_cylinder(rng: random.Random) -> OptimizationItem:
    """Ex. 345: closed cylinder, given V, min surface. h=2r when V=2π r^3."""
    n = rng.choice([1, 2, 3])
    # V = 2 π n^3  (n=2 → 16π, the OpenStax number)
    v_over_pi = 2 * n * n * n
    prompt = (
        rf"\text{{Find the dimensions of the closed cylinder of volume }}"
        rf"{v_over_pi}\pi\text{{ that has the least surface area.}}"
    )
    answer = rf"r={n},\ h={2 * n}"
    return OptimizationItem(
        prompt_latex=prompt,
        answer_latex=answer,
        label="optimization",
        frame_id="closed_cylinder",
        metadata={"r": n, "h": 2 * n, "V_over_pi": v_over_pi},
    )


def _inscribed_triangle(rng: random.Random) -> OptimizationItem:
    """Ex. 343: largest rectangle in the triangle x/a + y/b = 1 (first quadrant)."""
    a, b = rng.choice(((4, 6), (6, 8), (4, 8), (10, 6), (8, 4)))
    prompt = (
        rf"\text{{Find the dimensions of the largest rectangle in the first quadrant "
        rf"that fits in the triangle bounded by }}x=0,\ y=0,\text{{ and }}"
        rf"\frac{{x}}{{{a}}}+\frac{{y}}{{{b}}}=1."
    )
    answer = f"{a // 2} by {b // 2}"
    return OptimizationItem(
        prompt_latex=prompt,
        answer_latex=answer,
        label="optimization",
        frame_id="inscribed_triangle",
        metadata={"a": a, "b": b},
    )


_FRAME_BUILDERS: dict[str, Callable[[random.Random], OptimizationItem]] = {
    "rectangle_perimeter": _rectangle_perimeter,
    "garden_three_sides": _garden_three_sides,
    "open_box": _open_box,
    "open_box_rect": _open_box_rect,
    "linear_revenue": _linear_revenue,
    "inscribed_ellipse": _inscribed_ellipse,
    "closed_cylinder": _closed_cylinder,
    "inscribed_triangle": _inscribed_triangle,
}

# D=0 stays rectangle-only (old easy). Easy leftovers lock out at higher bands.
FRAME_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("rectangle_perimeter",),
    "medium": ("rectangle_perimeter", "garden_three_sides"),
    "hard": ("garden_three_sides", "open_box", "linear_revenue"),
    "expert": (
        "open_box",
        "open_box_rect",
        "inscribed_ellipse",
        "closed_cylinder",
        "inscribed_triangle",
    ),
}

_FRAME_D_GATES: dict[str, tuple[float, float | None]] = {
    "rectangle_perimeter": (0.0, 15.999),
    "garden_three_sides": (8.0, 19.999),
    "open_box": (16.0, None),
    "linear_revenue": (16.0, 19.999),
    "open_box_rect": (20.0, None),
    "inscribed_ellipse": (20.0, None),
    "closed_cylinder": (20.0, None),
    "inscribed_triangle": (20.0, None),
}


def optimization_frames_for_difficulty(d: float) -> tuple[str, ...]:
    """Map continuous D → OpenStax §4.7 frames. Easy leftovers lock out at high D."""
    if d < 8.0:
        return FRAME_BANDS["easy"]
    if d < 16.0:
        return FRAME_BANDS["medium"]
    if d < 20.0:
        return FRAME_BANDS["hard"]
    return FRAME_BANDS["expert"]


def optimization_form_rows(
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
            "generator_keys": [OPTIMIZATION_GENERATOR],
        }
        if apply_d_gates and d_max is not None:
            row["d_max"] = float(d_max)
        rows.append(row)
    return rows


def optimization_live_metadata(item: OptimizationItem) -> dict[str, Any]:
    """Stamp live-loop keys: ``form_id`` = frame id, shared ``generator``."""
    fid = str(item.frame_id)
    return {
        **item.metadata,
        "form_id": fid,
        "family": fid,
        "generator": OPTIMIZATION_GENERATOR,
        "frame_id": fid,
        "spec_snapshot": {
            "form_id": fid,
            "family": fid,
            "generator": OPTIMIZATION_GENERATOR,
        },
    }


def sample_optimization_frame(
    rng: random.Random,
    *,
    frames: tuple[str, ...],
    d: float = 0.0,
    quality_weights: dict[str, float] | None = None,
) -> OptimizationItem:
    """Pick a D-eligible OpenStax frame via ``select_form_id`` (live quality tilt)."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    allowed = [f for f in frames if f in _FRAME_BUILDERS]
    if not allowed:
        allowed = ["rectangle_perimeter"]
    pool = optimization_form_rows(allowed, apply_d_gates=False)
    form = select_form_id(
        pool, d=float(d), rng=rng, quality_weights=quality_weights
    )
    frame_id = str(form.get("form_id") or allowed[0])
    if frame_id not in _FRAME_BUILDERS:
        frame_id = allowed[0]
    return _FRAME_BUILDERS[frame_id](rng)
