"""Convenience builders for common geometry figures."""

from __future__ import annotations

import math

from .figure import GeometryFigure
from .primitives import (
    AngleMark,
    CirclePrim,
    Label,
    Point,
    Polygon,
    RightAngleMark,
    Segment,
)


def angle_figure(
    p1_label: str,
    vertex_label: str,
    p2_label: str,
    measure_deg: float,
    *,
    show_measure: bool = True,
    kind: str = "angle",
) -> GeometryFigure:
    """Two rays forming an angle; optional measure label on the arc."""
    # Place vertex at origin; ray1 along +x; ray2 at measure_deg
    fig = GeometryFigure(kind=kind)
    v = Point(vertex_label, 0.0, 0.0, label=vertex_label, label_dx=-0.28, label_dy=-0.22)
    # Keep rays long enough to read
    length = 2.4
    # Bias obtuse angles upward for nicer framing
    base = 15.0 if measure_deg <= 90 else 5.0
    a1 = math.radians(base)
    a2 = math.radians(base + measure_deg)
    p1 = Point(
        p1_label,
        length * math.cos(a1),
        length * math.sin(a1),
        label=p1_label,
        label_dx=0.22,
        label_dy=0.12,
    )
    p2 = Point(
        p2_label,
        length * math.cos(a2),
        length * math.sin(a2),
        label=p2_label,
        label_dx=0.18,
        label_dy=0.18,
    )
    fig.add_point(v)
    fig.add_point(p1)
    fig.add_point(p2)
    fig.add(
        Segment(vertex_label, p1_label),
        Segment(vertex_label, p2_label),
        AngleMark(
            vertex=vertex_label,
            ray1=p1_label,
            ray2=p2_label,
            radius=0.55,
            label=f"{int(round(measure_deg))}°" if show_measure else None,
        ),
    )
    return fig


def triangle_figure(
    labels: tuple[str, str, str] | list[str],
    angles: tuple[float, float, float] | list[float],
    *,
    missing: str | None = None,
    side_labels: dict[str, str] | None = None,
    right_angle_at: str | None = None,
    kind: str = "triangle",
) -> GeometryFigure:
    """Triangle with vertex labels and angle marks (``?`` for missing)."""
    a_lbl, b_lbl, c_lbl = labels[0], labels[1], labels[2]
    ang_a, ang_b, ang_c = float(angles[0]), float(angles[1]), float(angles[2])

    # Place A at origin, AB along x-axis; locate C via angles at A and B
    scale = 3.2
    ax, ay = 0.0, 0.0
    bx, by = scale, 0.0
    # Law of sines with AB = scale: AC = scale * sin(B)/sin(C), etc.
    # From A: direction of AC is ang_a from AB
    ac = scale * math.sin(math.radians(ang_b)) / math.sin(math.radians(ang_c))
    cx = ax + ac * math.cos(math.radians(ang_a))
    cy = ay + ac * math.sin(math.radians(ang_a))

    fig = GeometryFigure(kind=kind)
    fig.add_point(Point(a_lbl, ax, ay, label=a_lbl, label_dx=-0.25, label_dy=-0.22))
    fig.add_point(Point(b_lbl, bx, by, label=b_lbl, label_dx=0.25, label_dy=-0.22))
    fig.add_point(Point(c_lbl, cx, cy, label=c_lbl, label_dx=0.0, label_dy=0.28))
    fig.add(
        Polygon([a_lbl, b_lbl, c_lbl]),
    )

    def mark(vertex: str, ray1: str, ray2: str, degrees: float, is_missing: bool) -> None:
        if right_angle_at == vertex or (not is_missing and abs(degrees - 90) < 0.5):
            fig.add(RightAngleMark(vertex=vertex, leg1=ray1, leg2=ray2))
            return
        label = "?" if is_missing else f"{int(round(degrees))}°"
        fig.add(
            AngleMark(
                vertex=vertex,
                ray1=ray1,
                ray2=ray2,
                radius=0.4,
                label=label,
            )
        )

    mark(a_lbl, b_lbl, c_lbl, ang_a, missing == a_lbl)
    mark(b_lbl, a_lbl, c_lbl, ang_b, missing == b_lbl)
    mark(c_lbl, a_lbl, b_lbl, ang_c, missing == c_lbl)

    if side_labels:
        # Midpoint labels for sides keyed as "AB", "BC", "CA"
        pts = {a_lbl: (ax, ay), b_lbl: (bx, by), c_lbl: (cx, cy)}
        for key, text in side_labels.items():
            if len(key) != 2:
                continue
            p, q = key[0], key[1]
            if p not in pts or q not in pts:
                continue
            mx = (pts[p][0] + pts[q][0]) / 2
            my = (pts[p][1] + pts[q][1]) / 2
            # Offset outward roughly
            fig.add(Label(text=text, x=mx, y=my - 0.28))

    return fig


def circle_figure(
    radius: float,
    *,
    center_label: str = "O",
    radius_point_label: str = "A",
    show_radius_length: bool = True,
    unit: str = "cm",
    kind: str = "circle",
) -> GeometryFigure:
    """Circle with center and a drawn radius segment."""
    # Draw at a comfortable visual size; label shows the true radius value
    draw_r = 1.8
    fig = GeometryFigure(kind=kind)
    fig.add_point(
        Point(center_label, 0.0, 0.0, label=center_label, label_dx=-0.28, label_dy=-0.2)
    )
    fig.add_point(
        Point(
            radius_point_label,
            draw_r,
            0.0,
            label=radius_point_label,
            label_dx=0.25,
            label_dy=0.0,
        )
    )
    fig.add(
        CirclePrim(center=center_label, radius=draw_r),
        Segment(center_label, radius_point_label),
    )
    if show_radius_length:
        fig.add(Label(text=f"{int(radius)} {unit}", x=draw_r / 2, y=0.28))
    return fig


def polygon_figure(
    vertices: list[tuple[str, float, float]],
    *,
    closed: bool = True,
    fill: str | None = None,
    kind: str = "polygon",
) -> GeometryFigure:
    """Arbitrary polygon from ``(label, x, y)`` vertices."""
    fig = GeometryFigure(kind=kind)
    ids: list[str] = []
    for label, x, y in vertices:
        fig.add_point(Point(label, x, y, label=label))
        ids.append(label)
    fig.add(Polygon(ids, closed=closed, fill=fill))
    return fig


def rectangle_figure(
    width: float,
    height: float,
    *,
    labels: tuple[str, str, str, str] = ("A", "B", "C", "D"),
    show_dimensions: bool = True,
    unit: str = "cm",
    kind: str = "rectangle",
) -> GeometryFigure:
    """Axis-aligned rectangle ABCD (A bottom-left, counterclockwise)."""
    a, b, c, d = labels
    # Normalize visual size
    scale = 3.0 / max(width, height, 1e-6)
    w, h = width * scale, height * scale
    return polygon_figure(
        [(a, 0, 0), (b, w, 0), (c, w, h), (d, 0, h)],
        kind=kind,
    ) if not show_dimensions else _rectangle_with_dims(a, b, c, d, w, h, width, height, unit, kind)


def _rectangle_with_dims(
    a: str,
    b: str,
    c: str,
    d: str,
    w: float,
    h: float,
    width: float,
    height: float,
    unit: str,
    kind: str,
) -> GeometryFigure:
    fig = polygon_figure([(a, 0, 0), (b, w, 0), (c, w, h), (d, 0, h)], kind=kind)
    fig.add(Label(text=f"{int(width)} {unit}", x=w / 2, y=-0.35))
    fig.add(Label(text=f"{int(height)} {unit}", x=w + 0.45, y=h / 2))
    return fig
