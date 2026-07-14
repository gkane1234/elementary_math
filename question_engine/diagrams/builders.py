"""Convenience builders for common geometry figures."""

from __future__ import annotations

import math
import random
from typing import Literal

from packages.polynomial_core import format_measurement_text

from .figure import GeometryFigure
from .primitives import (
    AngleMark,
    CirclePrim,
    Label,
    Line,
    Point,
    Polygon,
    Ray,
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


def starter_ray_figure(
    vertex_label: str,
    tip_label: str,
    *,
    kind: str = "draw_angle_ray",
) -> GeometryFigure:
    """Single labeled ray — scaffold for “draw an angle of N°” prompts."""
    fig = GeometryFigure(kind=kind)
    fig.add_point(
        Point(vertex_label, 0.0, 0.0, label=vertex_label, label_dx=-0.28, label_dy=-0.22)
    )
    fig.add_point(
        Point(tip_label, 2.4, 0.0, label=tip_label, label_dx=0.22, label_dy=-0.12)
    )
    fig.add(Ray(start=vertex_label, through=tip_label))
    return fig


def adjacent_angles_figure(
    piece_degrees: list[float] | tuple[float, ...],
    *,
    tip_labels: list[str] | tuple[str, ...],
    vertex_label: str,
    piece_labels: list[str | None] | tuple[str | None, ...],
    span_marks: list[tuple[int, int, str]] | tuple[tuple[int, int, str], ...] | None = None,
    use_line_through: bool = False,
    right_angle_tips: tuple[int, int] | None = None,
    kind: str = "adjacent_angles",
    length: float = 2.55,
    base_deg: float = 8.0,
) -> GeometryFigure:
    """Several rays from one vertex forming consecutive labeled wedges.

    ``piece_degrees[i]`` is the measure between ``tip_labels[i]`` and
    ``tip_labels[i + 1]``. Optional ``span_marks`` (start_tip, end_tip, text)
    mark a multi-piece angle (often ``?`` for the asked span).
    """
    pieces = [float(p) for p in piece_degrees]
    if len(pieces) < 1:
        raise ValueError("adjacent_angles_figure needs at least one piece")
    if len(tip_labels) != len(pieces) + 1:
        raise ValueError("tip_labels must have one more entry than piece_degrees")
    if len(piece_labels) != len(pieces):
        raise ValueError("piece_labels must match piece_degrees")

    total = sum(pieces)
    # Keep the whole fan readable and mostly above the base ray.
    if use_line_through and abs(total - 180.0) < 0.6:
        base = 0.0
    elif right_angle_tips is not None and abs(total - 90.0) < 0.6:
        base = 0.0
    else:
        base = base_deg if total <= 160 else max(2.0, 185.0 - total) / 2.0

    fig = GeometryFigure(kind=kind)
    fig.add_point(
        Point(
            vertex_label,
            0.0,
            0.0,
            label=vertex_label,
            label_dx=-0.28,
            label_dy=-0.22,
        )
    )

    cum = 0.0
    tip_angles = [base]
    for deg in pieces:
        cum += deg
        tip_angles.append(base + cum)

    for i, tip in enumerate(tip_labels):
        ang = math.radians(tip_angles[i])
        # Fan tip labels slightly outward along the ray.
        lx = 0.18 * math.cos(ang)
        ly = 0.18 * math.sin(ang)
        fig.add_point(
            Point(
                tip,
                length * math.cos(ang),
                length * math.sin(ang),
                label=tip,
                label_dx=lx,
                label_dy=ly,
                show_dot=False,
            )
        )

    if use_line_through and len(tip_labels) >= 2:
        fig.add(Line(tip_labels[0], tip_labels[-1]))
        for tip in tip_labels[1:-1]:
            fig.add(Segment(vertex_label, tip))
    else:
        for tip in tip_labels:
            fig.add(Segment(vertex_label, tip))

    # Inner wedge marks — staggered radii so labels do not collide.
    for i, label in enumerate(piece_labels):
        if label is None:
            continue
        radius = 0.42 + 0.18 * (i % 3)
        fig.add(
            AngleMark(
                vertex=vertex_label,
                ray1=tip_labels[i],
                ray2=tip_labels[i + 1],
                radius=radius,
                label=label,
                label_radius=radius + 0.32,
            )
        )

    if right_angle_tips is not None:
        i0, i1 = right_angle_tips
        fig.add(
            RightAngleMark(
                vertex=vertex_label,
                leg1=tip_labels[i0],
                leg2=tip_labels[i1],
            )
        )

    # Outer / spanning angle marks sit outside the piece arcs.
    for start_i, end_i, text in span_marks or ():
        if not (0 <= start_i < end_i <= len(tip_labels) - 1):
            continue
        span_pieces = end_i - start_i
        radius = 0.95 + 0.22 * max(0, span_pieces - 1)
        fig.add(
            AngleMark(
                vertex=vertex_label,
                ray1=tip_labels[start_i],
                ray2=tip_labels[end_i],
                radius=radius,
                label=text,
                label_radius=radius + 0.34,
            )
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


def _triangle_coords(
    labels: tuple[str, str, str] | list[str],
    angles: tuple[float, float, float] | list[float],
    *,
    scale: float,
    ox: float = 0.0,
    oy: float = 0.0,
) -> list[tuple[str, float, float]]:
    """Place a triangle with the first edge along +x; return labeled vertices."""
    a_lbl, b_lbl, c_lbl = labels[0], labels[1], labels[2]
    ang_a, ang_b, ang_c = float(angles[0]), float(angles[1]), float(angles[2])
    ax, ay = ox, oy
    bx, by = ox + scale, oy
    ac = scale * math.sin(math.radians(ang_b)) / math.sin(math.radians(ang_c))
    cx = ax + ac * math.cos(math.radians(ang_a))
    cy = ay + ac * math.sin(math.radians(ang_a))
    return [(a_lbl, ax, ay), (b_lbl, bx, by), (c_lbl, cx, cy)]


def _add_side_labels(
    fig: GeometryFigure,
    pts: dict[str, tuple[float, float]],
    side_labels: dict[str, str] | None,
) -> None:
    if not side_labels:
        return
    center = _centroid(pts)
    for key, text in side_labels.items():
        if len(key) != 2:
            continue
        p, q = key[0], key[1]
        if p not in pts or q not in pts:
            continue
        fig.add(_side_length_label(pts[p], pts[q], center, text))


def similar_figures_pair_figure(
    *,
    shape: Literal["triangle", "rectangle"] = "triangle",
    small_labels: tuple[str, ...] | list[str],
    large_labels: tuple[str, ...] | list[str],
    small_side_labels: dict[str, str] | None = None,
    large_side_labels: dict[str, str] | None = None,
    angles: tuple[float, float, float] = (50.0, 60.0, 70.0),
    aspect: tuple[float, float] = (3.0, 2.0),
    scale_factor: float = 2.0,
    kind: str = "similar_figures",
) -> GeometryFigure:
    """Two similar figures side-by-side with vertex and optional side labels.

    Side-label keys are two character codes from the *that figure's* labels
    (e.g. ``\"AB\"``, ``\"BC\"`` for triangle ABC).
    """
    visual_ratio = min(1.0 + 0.35 * max(scale_factor - 1.0, 0.0), 2.1)
    gap = 1.35

    if shape == "rectangle":
        if len(small_labels) < 4 or len(large_labels) < 4:
            raise ValueError("rectangle similar figures need 4 labels each")
        aw, ah = float(aspect[0]), float(aspect[1])
        small_scale = 2.5 / max(aw, ah, 1e-6)
        large_scale = small_scale * (1.0 + 0.55 * (visual_ratio - 0.5))
        sw, sh = aw * small_scale, ah * small_scale
        lw, lh = aw * large_scale, ah * large_scale
        sa, sb, sc, sd = small_labels[0], small_labels[1], small_labels[2], small_labels[3]
        la, lb, lc, ld = large_labels[0], large_labels[1], large_labels[2], large_labels[3]
        small_verts = [(sa, 0.0, 0.0), (sb, sw, 0.0), (sc, sw, sh), (sd, 0.0, sh)]
        ox = sw + gap
        large_verts = [
            (la, ox, 0.0),
            (lb, ox + lw, 0.0),
            (lc, ox + lw, lh),
            (ld, ox, lh),
        ]
        fig = GeometryFigure(kind=kind)
        for verts in (small_verts, large_verts):
            center = _centroid([(x, y) for _, x, y in verts])
            ids: list[str] = []
            for label, x, y in verts:
                ldx, ldy = _vertex_label_offset(x, y, center)
                fig.add_point(Point(label, x, y, label=label, label_dx=ldx, label_dy=ldy))
                ids.append(label)
            fig.add(Polygon(ids))
        small_pts = {lab: (x, y) for lab, x, y in small_verts}
        large_pts = {lab: (x, y) for lab, x, y in large_verts}
        _add_side_labels(fig, small_pts, small_side_labels)
        _add_side_labels(fig, large_pts, large_side_labels)
        return fig

    # triangle (default)
    if len(small_labels) < 3 or len(large_labels) < 3:
        raise ValueError("triangle similar figures need 3 labels each")
    small_base = 2.4
    large_base = small_base * visual_ratio
    small_verts = _triangle_coords(small_labels[:3], angles, scale=small_base)
    # Place large triangle to the right of the small one.
    small_max_x = max(x for _, x, _ in small_verts)
    large_verts = _triangle_coords(
        large_labels[:3],
        angles,
        scale=large_base,
        ox=small_max_x + gap,
        oy=0.0,
    )
    fig = GeometryFigure(kind=kind)
    for verts in (small_verts, large_verts):
        center = _centroid([(x, y) for _, x, y in verts])
        ids = []
        for label, x, y in verts:
            ldx, ldy = _vertex_label_offset(x, y, center)
            fig.add_point(Point(label, x, y, label=label, label_dx=ldx, label_dy=ldy))
            ids.append(label)
        fig.add(Polygon(ids))
    small_pts = {lab: (x, y) for lab, x, y in small_verts}
    large_pts = {lab: (x, y) for lab, x, y in large_verts}
    _add_side_labels(fig, small_pts, small_side_labels)
    _add_side_labels(fig, large_pts, large_side_labels)
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
                format_measurement_text(int(radius), unit),
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
    fig.add(_side_length_label(pts[a], pts[b], center, format_measurement_text(int(width), unit)))
    fig.add(_side_length_label(pts[b], pts[c], center, format_measurement_text(int(height), unit)))
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
                format_measurement_text(int(length), unit),
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


def triangle_base_height_figure(
    base: float,
    height: float,
    *,
    labels: tuple[str, str, str] = ("A", "B", "C"),
    layout: Literal["right", "interior", "exterior"] = "right",
    unit: str = "cm",
    kind: str = "triangle_area",
    foot_fraction: float | None = None,
) -> GeometryFigure:
    """Triangle with labeled base and perpendicular height.

    Layouts
    -------
    ``right``
        Right triangle; legs are the base and height (classic easy form).
    ``interior``
        Oblique acute-looking triangle; dashed altitude meets the base inside.
    ``exterior``
        Obtuse triangle; dashed altitude meets the base-line extension outside.
    """
    a_lbl, b_lbl, c_lbl = labels

    def _len(value: float) -> str:
        text = f"{int(value)}" if float(value).is_integer() else f"{value:g}"
        return format_measurement_text(text, unit)

    base_text = _len(base)
    height_text = _len(height)

    if layout == "right":
        return right_triangle_figure(
            float(base),
            float(height),
            labels=labels,
            right_angle_at=c_lbl,
            side_labels={
                f"{b_lbl}{c_lbl}": base_text,
                f"{a_lbl}{c_lbl}": height_text,
            },
            kind=kind,
        )

    scale = 3.2 / max(base, height, 1e-6)
    w, h = float(base) * scale, float(height) * scale
    foot_id = "_H"

    if layout == "exterior":
        # Foot left of A so angle at A is obtuse.
        overhang = 0.28 + random.random() * 0.22  # ~0.28–0.50 of base draw-width
        foot_x = -overhang * w
        ax, ay = 0.0, 0.0
        bx, by = w, 0.0
        cx, cy = foot_x, h
        fx, fy = foot_x, 0.0
    else:
        # Interior foot between A and B (avoid near-right and midpoint-only look).
        if foot_fraction is None:
            t = 0.28 + random.random() * 0.44  # ~0.28–0.72
        else:
            t = min(0.75, max(0.25, float(foot_fraction)))
        foot_x = t * w
        ax, ay = 0.0, 0.0
        bx, by = w, 0.0
        cx, cy = foot_x, h
        fx, fy = foot_x, 0.0

    pts = {a_lbl: (ax, ay), b_lbl: (bx, by), c_lbl: (cx, cy), foot_id: (fx, fy)}
    center = _centroid({a_lbl: pts[a_lbl], b_lbl: pts[b_lbl], c_lbl: pts[c_lbl]})

    fig = GeometryFigure(kind=kind)
    for lbl, (x, y) in ((a_lbl, (ax, ay)), (b_lbl, (bx, by)), (c_lbl, (cx, cy))):
        ldx, ldy = _vertex_label_offset(x, y, center)
        fig.add_point(Point(lbl, x, y, label=lbl, label_dx=ldx, label_dy=ldy))
    fig.add_point(Point(foot_id, fx, fy, label=None, show_dot=False))
    fig.add(Polygon([a_lbl, b_lbl, c_lbl]))
    # Dashed altitude to the base line; exterior also shows the base-line stub.
    fig.add(Segment(c_lbl, foot_id, style="dashed"))
    if layout == "exterior":
        nearest = a_lbl if abs(fx - ax) <= abs(fx - bx) else b_lbl
        fig.add(Segment(nearest, foot_id, style="dashed"))
    fig.add(RightAngleMark(vertex=foot_id, leg1=c_lbl, leg2=a_lbl if fx <= ax else b_lbl))
    fig.add(_side_length_label(pts[a_lbl], pts[b_lbl], center, base_text))
    # Height label midway on the altitude, offset away from the triangle interior.
    mid_h = ((cx + fx) / 2, (cy + fy) / 2)
    fig.add(
        _exterior_point_label(
            mid_h[0],
            mid_h[1],
            center,
            height_text,
            fallback=(-1.0, 0.0) if layout == "exterior" else (1.0, 0.0),
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
    skew_ratio: float | None = None,
) -> GeometryFigure:
    """Parallelogram with base along x and vertical height.

    When ``skew_ratio`` is None, uses a fixed slant so the figure is clearly
    not a rectangle. Pass a computed ratio for equal-side rhombus silhouettes.
    """
    a, b, c, d = labels
    scale = 3.0 / max(base, height, 1e-6)
    w, h = base * scale, height * scale
    skew = (skew_ratio if skew_ratio is not None else 0.35) * w
    pts = {a: (0.0, 0.0), b: (w, 0.0), c: (w + skew, h), d: (skew, h)}
    fig = polygon_figure(
        [(a, 0, 0), (b, w, 0), (c, w + skew, h), (d, skew, h)],
        kind=kind,
        fill="#dbeafe",
    )
    if show_dimensions:
        center = _centroid(pts)
        fig.add(_side_length_label(pts[a], pts[b], center, format_measurement_text(int(base), unit)))
        # Height is a vertical measure, not a side length — keep it clear of the right edge.
        fig.add(
            _exterior_point_label(
                w + skew,
                h / 2,
                center,
                format_measurement_text(int(height), unit),
                fallback=(1.0, 0.0),
            )
        )
    return fig


def rhombus_figure(
    side: float,
    height: float,
    *,
    labels: tuple[str, str, str, str] = ("A", "B", "C", "D"),
    show_dimensions: bool = True,
    unit: str = "cm",
    kind: str = "rhombus",
) -> GeometryFigure:
    """Rhombus ABCD with equal sides; base along x and vertical height.

    Area is still base × height. Height is clamped below ``side`` so the
    lateral edges can match the base length visually.
    """
    side = float(side)
    height = float(height)
    if height >= side:
        height = max(1.0, side * 0.75)
    # Draw-space: skew such that sqrt(skew^2 + h_draw^2) == base_draw.
    scale = 3.0 / max(side, height, 1e-6)
    w, h = side * scale, height * scale
    skew = math.sqrt(max(w * w - h * h, (0.15 * w) ** 2))
    return parallelogram_figure(
        side,
        height,
        labels=labels,
        show_dimensions=show_dimensions,
        unit=unit,
        kind=kind,
        skew_ratio=skew / w if w else 0.35,
    )


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
        fig.add(_side_length_label(pts[a], pts[b], center, format_measurement_text(int(base_bottom), unit)))
        fig.add(_side_length_label(pts[d], pts[c], center, format_measurement_text(int(base_top), unit)))
        fig.add(
            _exterior_point_label(
                w,
                h / 2,
                center,
                format_measurement_text(int(height), unit),
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
            (pts[c], format_measurement_text(int(diag_horizontal), unit), (1.0, 0.0)),
            (pts[b], format_measurement_text(int(diag_vertical), unit), (0.0, -1.0)),
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


def _angle_label_text(value: float | str | None, *, show: bool) -> str | None:
    if not show or value is None:
        return None
    if isinstance(value, str):
        return value
    return f"{int(round(value))}°"


def complementary_angles_figure(
    given_deg: float,
    *,
    given_label: float | str | None = None,
    unknown_label: str = "?",
    labels: tuple[str, str, str, str] | None = None,
    kind: str = "complementary_angles",
) -> GeometryFigure:
    """Right angle split by a ray into complementary pair (given + unknown)."""
    given = float(given_deg)
    given = max(12.0, min(78.0, given))
    a_lbl, v_lbl, b_lbl, c_lbl = labels or ("A", "O", "B", "C")
    length = 2.4
    fig = GeometryFigure(kind=kind)
    # Right angle: OA along +x, OC along +y; OB splits them.
    fig.add_point(Point(v_lbl, 0.0, 0.0, label=v_lbl, label_dx=-0.28, label_dy=-0.22))
    fig.add_point(
        Point(a_lbl, length, 0.0, label=a_lbl, label_dx=0.22, label_dy=-0.12, show_dot=False)
    )
    rad = math.radians(given)
    fig.add_point(
        Point(
            b_lbl,
            length * math.cos(rad),
            length * math.sin(rad),
            label=b_lbl,
            label_dx=0.18,
            label_dy=0.16,
            show_dot=False,
        )
    )
    fig.add_point(
        Point(c_lbl, 0.0, length, label=c_lbl, label_dx=-0.12, label_dy=0.22, show_dot=False)
    )
    given_text = _angle_label_text(
        given if given_label is None else given_label, show=True
    )
    fig.add(
        Segment(v_lbl, a_lbl),
        Segment(v_lbl, b_lbl),
        Segment(v_lbl, c_lbl),
        RightAngleMark(vertex=v_lbl, leg1=a_lbl, leg2=c_lbl),
        AngleMark(
            vertex=v_lbl,
            ray1=a_lbl,
            ray2=b_lbl,
            radius=0.7,
            label=given_text,
        ),
        AngleMark(
            vertex=v_lbl,
            ray1=b_lbl,
            ray2=c_lbl,
            radius=0.5,
            label=unknown_label,
        ),
    )
    return fig


def supplementary_angles_figure(
    given_deg: float,
    *,
    given_label: float | str | None = None,
    unknown_label: str = "?",
    labels: tuple[str, str, str, str] | None = None,
    kind: str = "supplementary_angles",
) -> GeometryFigure:
    """Straight line with a ray forming a supplementary (adjacent) pair."""
    given = float(given_deg)
    given = max(15.0, min(165.0, given))
    a_lbl, v_lbl, b_lbl, c_lbl = labels or ("A", "O", "B", "C")
    length = 2.6
    fig = GeometryFigure(kind=kind)
    fig.add_point(Point(v_lbl, 0.0, 0.0, label=v_lbl, label_dx=-0.05, label_dy=-0.32))
    fig.add_point(
        Point(a_lbl, -length, 0.0, label=a_lbl, label_dx=-0.22, label_dy=-0.12, show_dot=False)
    )
    fig.add_point(
        Point(c_lbl, length, 0.0, label=c_lbl, label_dx=0.22, label_dy=-0.12, show_dot=False)
    )
    # Measure given from the positive side (OC) up to the ray OB.
    rad = math.radians(given)
    fig.add_point(
        Point(
            b_lbl,
            length * 0.95 * math.cos(rad),
            length * 0.95 * math.sin(rad),
            label=b_lbl,
            label_dx=0.16,
            label_dy=0.18,
            show_dot=False,
        )
    )
    given_text = _angle_label_text(
        given if given_label is None else given_label, show=True
    )
    # Put the given on the acute/obtuse wedge BOC; unknown is the adjacent AOB.
    fig.add(
        Line(a_lbl, c_lbl),
        Segment(v_lbl, b_lbl),
        AngleMark(
            vertex=v_lbl,
            ray1=c_lbl,
            ray2=b_lbl,
            radius=0.55,
            label=given_text,
        ),
        AngleMark(
            vertex=v_lbl,
            ray1=b_lbl,
            ray2=a_lbl,
            radius=0.7,
            label=unknown_label,
        ),
    )
    return fig


def vertical_angles_figure(
    given_deg: float,
    *,
    given_label: float | str | None = None,
    unknown_label: str = "?",
    labels: tuple[str, str, str, str, str] | None = None,
    kind: str = "vertical_angles",
) -> GeometryFigure:
    """Two intersecting lines; mark a given angle and its vertical partner."""
    given = float(given_deg)
    given = max(20.0, min(160.0, given))
    # Avoid near-straight / near-right degeneracies for readability.
    if abs(given - 90.0) < 8:
        given = 70.0 if given < 90 else 110.0
    a_lbl, v_lbl, b_lbl, c_lbl, d_lbl = labels or ("A", "O", "B", "C", "D")
    length = 2.4
    fig = GeometryFigure(kind=kind)
    rad = math.radians(given)
    fig.add_point(Point(v_lbl, 0.0, 0.0, label=v_lbl, label_dx=-0.28, label_dy=-0.28))
    # Horizontal line A—O—B and oblique line C—O—D.
    fig.add_point(
        Point(a_lbl, -length, 0.0, label=a_lbl, label_dx=-0.22, label_dy=-0.12, show_dot=False)
    )
    fig.add_point(
        Point(b_lbl, length, 0.0, label=b_lbl, label_dx=0.22, label_dy=-0.12, show_dot=False)
    )
    fig.add_point(
        Point(
            c_lbl,
            length * math.cos(rad),
            length * math.sin(rad),
            label=c_lbl,
            label_dx=0.16,
            label_dy=0.18,
            show_dot=False,
        )
    )
    fig.add_point(
        Point(
            d_lbl,
            -length * math.cos(rad),
            -length * math.sin(rad),
            label=d_lbl,
            label_dx=-0.18,
            label_dy=-0.18,
            show_dot=False,
        )
    )
    given_text = _angle_label_text(
        given if given_label is None else given_label, show=True
    )
    fig.add(
        Line(a_lbl, b_lbl),
        Line(c_lbl, d_lbl),
        # Given: ∠BOC (between +x and oblique upper ray)
        AngleMark(
            vertex=v_lbl,
            ray1=b_lbl,
            ray2=c_lbl,
            radius=0.55,
            label=given_text,
        ),
        # Vertical: ∠AOD (opposite)
        AngleMark(
            vertex=v_lbl,
            ray1=a_lbl,
            ray2=d_lbl,
            radius=0.55,
            label=unknown_label,
        ),
    )
    return fig


def parallel_lines_transversal_figure(
    angle_deg: float,
    *,
    show_measure: bool = True,
    relation: str = "corresponding",
    unknown_label: str = "?",
    kind: str = "parallel_transversal",
) -> GeometryFigure:
    """Two horizontal parallels cut by a transversal; mark given + asked angles.

    ``relation`` selects which second angle is marked as unknown:
    corresponding, alternate interior, or same-side interior.
    """
    fig = GeometryFigure(kind=kind)
    # Lines y=0 and y=2; transversal through origin at angle_deg from +x
    angle = float(angle_deg)
    angle = max(25.0, min(155.0, angle))
    # Keep transversal clearly slanted (not near-vertical framing issues).
    if abs(angle - 90.0) < 12:
        angle = 55.0 if angle < 90 else 125.0

    fig.add_point(Point("L1a", -2.8, 0.0, show_dot=False))
    fig.add_point(Point("L1b", 2.8, 0.0, show_dot=False))
    fig.add_point(Point("L2a", -2.8, 2.2, show_dot=False))
    fig.add_point(Point("L2b", 2.8, 2.2, show_dot=False))
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    # Transversal through P=(0,0) and Q=(0,2.2) projected along direction.
    # Extend so both intersections are interior to the drawn parallels.
    t_low = -1.6
    t_high = (2.2 / sin_a) + 1.2 if abs(sin_a) > 1e-6 else 4.0
    fig.add_point(Point("T1", t_low * cos_a, t_low * sin_a, show_dot=False))
    fig.add_point(Point("T2", t_high * cos_a, t_high * sin_a, show_dot=False))
    fig.add_point(Point("P", 0.0, 0.0, label="P", label_dx=-0.32, label_dy=-0.28))
    qx = 2.2 * cos_a / sin_a if abs(sin_a) > 1e-6 else 0.0
    fig.add_point(Point("Q", qx, 2.2, label="Q", label_dx=0.28, label_dy=0.22))

    given_text = f"{int(round(angle))}°" if show_measure else None
    rel = relation.strip().lower().replace("-", " ").replace("_", " ")

    fig.add(
        Line("L1a", "L1b"),
        Line("L2a", "L2b"),
        Segment("T1", "T2"),
        # Given: lower interior-ish angle at P between +x and transversal up.
        AngleMark(
            vertex="P",
            ray1="L1b",
            ray2="T2",
            radius=0.45,
            label=given_text,
        ),
    )

    # Ask angle at Q depending on relationship to the given at P.
    # Given at P is the NE angle (between +x and transversal toward Q).
    if "same" in rel and "side" in rel:
        # Same-side interior: NW at Q (between -x and transversal down toward P)
        # Actually SSI: interior angles on the same side of transversal.
        # Given NE at P is interior (above L1). Same-side interior on the right:
        # SE region at Q? Interior between parallels: at Q, right-of-transversal
        # interior is between +x (L2b) and transversal down (T1) when transversal
        # slopes up-right — that's the SE wedge.
        fig.add(
            AngleMark(
                vertex="Q",
                ray1="L2b",
                ray2="T1",
                radius=0.45,
                label=unknown_label,
            )
        )
    elif "alternate" in rel:
        # Alternate interior: NW at Q (left of transversal, below L2)
        fig.add(
            AngleMark(
                vertex="Q",
                ray1="L2a",
                ray2="T1",
                radius=0.45,
                label=unknown_label,
            )
        )
    else:
        # Corresponding: NE at Q (between +x and transversal up)
        fig.add(
            AngleMark(
                vertex="Q",
                ray1="L2b",
                ray2="T2",
                radius=0.45,
                label=unknown_label,
            )
        )
    return fig
