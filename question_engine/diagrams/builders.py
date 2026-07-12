"""Convenience builders for common geometry figures."""

from __future__ import annotations

import math

from .figure import GeometryFigure
from .primitives import (
    AngleMark,
    CirclePrim,
    Label,
    Line,
    Point,
    Polygon,
    RightAngleMark,
    Segment,
)

# Figure-units clearance from an edge stroke to the side-length label center.
_SIDE_LABEL_OFFSET = 0.48
# Vertex letter clearance from the polygon centroid (outward).
_VERTEX_LABEL_OFFSET = 0.32


def _centroid(pts: dict[str, tuple[float, float]] | list[tuple[float, float]]) -> tuple[float, float]:
    coords = list(pts.values()) if isinstance(pts, dict) else list(pts)
    n = len(coords)
    if n == 0:
        return 0.0, 0.0
    return sum(p[0] for p in coords) / n, sum(p[1] for p in coords) / n


def _unit(dx: float, dy: float) -> tuple[float, float]:
    length = math.hypot(dx, dy)
    if length < 1e-9:
        return 1.0, 0.0
    return dx / length, dy / length


def _outward_normal(
    p1: tuple[float, float],
    p2: tuple[float, float],
    centroid: tuple[float, float],
) -> tuple[float, float]:
    """Unit normal of segment p1→p2 pointing away from ``centroid``."""
    ux, uy = _unit(p2[0] - p1[0], p2[1] - p1[1])
    nx, ny = -uy, ux
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    # Flip if the normal points toward the interior.
    if nx * (mx - centroid[0]) + ny * (my - centroid[1]) < 0:
        nx, ny = -nx, -ny
    return nx, ny


def _side_length_label(
    p1: tuple[float, float],
    p2: tuple[float, float],
    centroid: tuple[float, float],
    text: str,
    *,
    offset: float = _SIDE_LABEL_OFFSET,
) -> Label:
    """Place a length label at the edge midpoint, offset outward along the normal."""
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    nx, ny = _outward_normal(p1, p2, centroid)
    return Label(text=text, x=mx + nx * offset, y=my + ny * offset)


def _exterior_point_label(
    x: float,
    y: float,
    centroid: tuple[float, float],
    text: str,
    *,
    offset: float = _SIDE_LABEL_OFFSET,
    fallback: tuple[float, float] = (0.0, -1.0),
) -> Label:
    """Offset a label from ``(x, y)`` away from ``centroid`` (for heights / diagonals)."""
    fx, fy = _unit(x - centroid[0], y - centroid[1])
    if abs(fx) + abs(fy) < 1e-9:
        fx, fy = _unit(fallback[0], fallback[1])
    return Label(text=text, x=x + fx * offset, y=y + fy * offset)


def _vertex_label_offset(
    x: float,
    y: float,
    centroid: tuple[float, float],
    *,
    offset: float = _VERTEX_LABEL_OFFSET,
) -> tuple[float, float]:
    dx, dy = _unit(x - centroid[0], y - centroid[1])
    if abs(dx) + abs(dy) < 1e-9:
        return offset * 0.7, offset * 0.7
    return dx * offset, dy * offset


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
        center = _centroid(pts)
        for key, text in side_labels.items():
            if len(key) != 2:
                continue
            p, q = key[0], key[1]
            if p not in pts or q not in pts:
                continue
            fig.add(_side_length_label(pts[p], pts[q], center, text))

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
        # Midpoint of radius OA, offset perpendicular (above the segment).
        fig.add(
            _side_length_label(
                (0.0, 0.0),
                (draw_r, 0.0),
                (0.0, 0.0),
                f"{int(radius)} {unit}",
            )
        )
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
    center = _centroid([(x, y) for _, x, y in vertices])
    for label, x, y in vertices:
        ldx, ldy = _vertex_label_offset(x, y, center)
        fig.add_point(Point(label, x, y, label=label, label_dx=ldx, label_dy=ldy))
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
    pts = {a: (0.0, 0.0), b: (w, 0.0), c: (w, h), d: (0.0, h)}
    center = _centroid(pts)
    fig.add(_side_length_label(pts[a], pts[b], center, f"{int(width)} {unit}"))
    fig.add(_side_length_label(pts[b], pts[c], center, f"{int(height)} {unit}"))
    return fig


def segment_figure(
    length: float,
    *,
    labels: tuple[str, str] = ("A", "B"),
    show_length: bool = True,
    unit: str = "cm",
    kind: str = "segment",
) -> GeometryFigure:
    """Horizontal segment with optional length label."""
    a, b = labels
    draw_len = 3.2
    fig = GeometryFigure(kind=kind)
    fig.add_point(Point(a, 0.0, 0.0, label=a, label_dx=-0.25, label_dy=-0.2))
    fig.add_point(Point(b, draw_len, 0.0, label=b, label_dx=0.2, label_dy=-0.2))
    fig.add(Segment(a, b))
    if show_length:
        # Offset above the horizontal segment (away from a synthetic centroid below).
        fig.add(
            _side_length_label(
                (0.0, 0.0),
                (draw_len, 0.0),
                (draw_len / 2, -1.0),
                f"{int(length)} {unit}",
            )
        )
    return fig


def right_triangle_figure(
    leg_a: float,
    leg_b: float,
    *,
    labels: tuple[str, str, str] = ("A", "B", "C"),
    right_angle_at: str = "C",
    side_labels: dict[str, str] | None = None,
    angle_labels: dict[str, str] | None = None,
    kind: str = "right_triangle",
) -> GeometryFigure:
    """Right triangle with right angle at ``right_angle_at`` (default C).

    Layout places the right angle at the origin when ``right_angle_at`` is C:
    C=(0,0), B=(leg_a,0), A=(0,leg_b) after visual scaling.
    """
    a_lbl, b_lbl, c_lbl = labels
    # Visual scale
    scale = 3.0 / max(leg_a, leg_b, 1e-6)
    w, h = leg_a * scale, leg_b * scale

    # Map: right angle vertex -> coords
    if right_angle_at == c_lbl:
        coords = {c_lbl: (0.0, 0.0), b_lbl: (w, 0.0), a_lbl: (0.0, h)}
        legs = (b_lbl, a_lbl)
    elif right_angle_at == a_lbl:
        coords = {a_lbl: (0.0, 0.0), c_lbl: (w, 0.0), b_lbl: (0.0, h)}
        legs = (c_lbl, b_lbl)
    else:
        coords = {b_lbl: (0.0, 0.0), c_lbl: (w, 0.0), a_lbl: (0.0, h)}
        legs = (c_lbl, a_lbl)

    fig = GeometryFigure(kind=kind)
    for lbl, (x, y) in coords.items():
        dx = -0.25 if x < 0.1 else (0.2 if x > w * 0.5 else 0.0)
        dy = -0.22 if y < 0.1 else 0.25
        fig.add_point(Point(lbl, x, y, label=lbl, label_dx=dx, label_dy=dy))
    fig.add(Polygon([a_lbl, b_lbl, c_lbl]))
    fig.add(RightAngleMark(vertex=right_angle_at, leg1=legs[0], leg2=legs[1]))

    if side_labels:
        pts = coords
        center = _centroid(pts)
        for key, text in side_labels.items():
            if len(key) != 2 or key[0] not in pts or key[1] not in pts:
                continue
            p, q = key[0], key[1]
            fig.add(_side_length_label(pts[p], pts[q], center, text))

    if angle_labels:
        for vertex, text in angle_labels.items():
            if vertex not in coords:
                continue
            others = [lbl for lbl in (a_lbl, b_lbl, c_lbl) if lbl != vertex]
            fig.add(
                AngleMark(
                    vertex=vertex,
                    ray1=others[0],
                    ray2=others[1],
                    radius=0.4,
                    label=text,
                )
            )
    return fig


def parallelogram_figure(
    base: float,
    height: float,
    *,
    labels: tuple[str, str, str, str] = ("A", "B", "C", "D"),
    show_dimensions: bool = True,
    unit: str = "cm",
    kind: str = "parallelogram",
) -> GeometryFigure:
    """Parallelogram with base along x and vertical height."""
    a, b, c, d = labels
    scale = 3.0 / max(base, height, 1e-6)
    w, h = base * scale, height * scale
    skew = w * 0.35
    pts = {a: (0.0, 0.0), b: (w, 0.0), c: (w + skew, h), d: (skew, h)}
    fig = polygon_figure(
        [(a, 0, 0), (b, w, 0), (c, w + skew, h), (d, skew, h)],
        kind=kind,
        fill="#dbeafe",
    )
    if show_dimensions:
        center = _centroid(pts)
        fig.add(_side_length_label(pts[a], pts[b], center, f"{int(base)} {unit}"))
        # Height is a vertical measure, not a side length — keep it clear of the right edge.
        fig.add(
            _exterior_point_label(
                w + skew,
                h / 2,
                center,
                f"{int(height)} {unit}",
                fallback=(1.0, 0.0),
            )
        )
    return fig


def trapezoid_figure(
    base_bottom: float,
    base_top: float,
    height: float,
    *,
    labels: tuple[str, str, str, str] = ("A", "B", "C", "D"),
    show_dimensions: bool = True,
    unit: str = "cm",
    kind: str = "trapezoid",
) -> GeometryFigure:
    """Isosceles trapezoid ABCD (AB bottom base)."""
    a, b, c, d = labels
    scale = 3.2 / max(base_bottom, height, 1e-6)
    w, h = base_bottom * scale, height * scale
    top = base_top * scale
    inset = (w - top) / 2
    pts = {
        a: (0.0, 0.0),
        b: (w, 0.0),
        c: (w - inset, h),
        d: (inset, h),
    }
    fig = polygon_figure(
        [(a, 0, 0), (b, w, 0), (c, w - inset, h), (d, inset, h)],
        kind=kind,
        fill="#dbeafe",
    )
    if show_dimensions:
        center = _centroid(pts)
        fig.add(_side_length_label(pts[a], pts[b], center, f"{int(base_bottom)} {unit}"))
        fig.add(_side_length_label(pts[d], pts[c], center, f"{int(base_top)} {unit}"))
        fig.add(
            _exterior_point_label(
                w,
                h / 2,
                center,
                f"{int(height)} {unit}",
                fallback=(1.0, 0.0),
            )
        )
    return fig


def kite_figure(
    diag_horizontal: float,
    diag_vertical: float,
    *,
    labels: tuple[str, str, str, str] = ("A", "B", "C", "D"),
    show_dimensions: bool = True,
    unit: str = "cm",
    kind: str = "kite",
) -> GeometryFigure:
    """Kite with perpendicular diagonals crossing at mid of horizontal."""
    a, b, c, d = labels
    scale = 3.0 / max(diag_horizontal, diag_vertical, 1e-6)
    hx, vy = diag_horizontal * scale / 2, diag_vertical * scale / 2
    # A top, B right, C bottom, D left; diagonals AC vertical, BD horizontal
    pts = {a: (0.0, vy), b: (hx, 0.0), c: (0.0, -vy), d: (-hx, 0.0)}
    fig = polygon_figure(
        [(a, 0, vy), (b, hx, 0), (c, 0, -vy), (d, -hx, 0)],
        kind=kind,
        fill="#dbeafe",
    )
    if show_dimensions:
        center = _centroid(pts)
        # Diagonals meet at the centroid, so tip midpoints are unusable.
        # Place each length outside a tip, then shift along the tip tangent so
        # the text clears the vertex letter.
        for tip, text, tangent in (
            (pts[c], f"{int(diag_horizontal)} {unit}", (1.0, 0.0)),
            (pts[b], f"{int(diag_vertical)} {unit}", (0.0, -1.0)),
        ):
            ox, oy = _unit(tip[0] - center[0], tip[1] - center[1])
            tx, ty = _unit(tangent[0], tangent[1])
            fig.add(
                Label(
                    text=text,
                    x=tip[0] + ox * _SIDE_LABEL_OFFSET + tx * 0.55,
                    y=tip[1] + oy * _SIDE_LABEL_OFFSET + ty * 0.55,
                )
            )
    return fig


def parallel_lines_transversal_figure(
    angle_deg: float,
    *,
    show_measure: bool = True,
    kind: str = "parallel_transversal",
) -> GeometryFigure:
    """Two horizontal parallels cut by a transversal; mark one interior angle."""
    fig = GeometryFigure(kind=kind)
    # Lines y=0 and y=2; transversal through origin at angle_deg from +x
    fig.add_point(Point("L1a", -2.5, 0.0, show_dot=False))
    fig.add_point(Point("L1b", 2.5, 0.0, show_dot=False))
    fig.add_point(Point("L2a", -2.5, 2.0, show_dot=False))
    fig.add_point(Point("L2b", 2.5, 2.0, show_dot=False))
    rad = math.radians(angle_deg)
    # Transversal points
    fig.add_point(Point("T1", -1.5 * math.cos(rad), -1.5 * math.sin(rad), show_dot=False))
    fig.add_point(Point("T2", 2.8 * math.cos(rad), 2.8 * math.sin(rad), show_dot=False))
    fig.add_point(Point("P", 0.0, 0.0, label="P", label_dx=-0.3, label_dy=-0.25))
    fig.add(
        Line("L1a", "L1b"),
        Line("L2a", "L2b"),
        Segment("T1", "T2"),
        AngleMark(
            vertex="P",
            ray1="L1b",
            ray2="T2",
            radius=0.45,
            label=f"{int(round(angle_deg))}°" if show_measure else "?",
        ),
    )
    return fig
