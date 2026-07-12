"""Render graph_spec / number_line_spec metadata to SVG (mirrors QuestionGraph.tsx)."""

from __future__ import annotations

import math
import re
from typing import Any

WIDTH = 280
HEIGHT = 120
PLANE_HEIGHT = 220
PADDING = 24


def _map_x(value: float, spec: dict, width: int) -> float:
    span = (spec["x_max"] - spec["x_min"]) or 1.0
    return PADDING + ((value - spec["x_min"]) / span) * (width - PADDING * 2)


def _map_y(value: float, spec: dict, height: int) -> float:
    span = (spec["y_max"] - spec["y_min"]) or 1.0
    return height - PADDING - ((value - spec["y_min"]) / span) * (height - PADDING * 2)


def _evaluate_linear(expression: str, x: float) -> float | None:
    normalized = re.sub(r"\s+", "", expression)
    linear = re.match(
        r"^(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\*x\+(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)$",
        normalized,
        re.I,
    )
    if linear:
        return float(linear.group(1)) * x + float(linear.group(2))
    linear_minus = re.match(
        r"^(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\*x-(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)$",
        normalized,
        re.I,
    )
    if linear_minus:
        return float(linear_minus.group(1)) * x - float(linear_minus.group(2))
    abs_match = re.match(
        r"^(-?\d+(?:\.\d+)?)?\*?abs\(x([+-]\d+(?:\.\d+)?)?\)([+-]\d+(?:\.\d+)?)?$",
        normalized,
    )
    if abs_match:
        scale = float(abs_match.group(1)) if abs_match.group(1) else 1.0
        shift = float(abs_match.group(2)) if abs_match.group(2) else 0.0
        tail = float(abs_match.group(3)) if abs_match.group(3) else 0.0
        return scale * abs(x + shift) + tail
    return None


def _evaluate_graph_function(expression: str, x: float) -> float | None:
    normalized = re.sub(r"\s+", "", expression)
    linear = _evaluate_linear(normalized, x)
    if linear is not None:
        return linear
    cubic = re.match(
        r"^(-?\d+(?:\.\d+)?)\*x\^3\+(-?\d+(?:\.\d+)?)\*x\^2\+(-?\d+(?:\.\d+)?)\*x\+(-?\d+(?:\.\d+)?)$",
        normalized,
    )
    if cubic:
        a, b, c, d = (
            float(cubic.group(1)),
            float(cubic.group(2)),
            float(cubic.group(3)),
            float(cubic.group(4)),
        )
        return ((a * x + b) * x + c) * x + d
    quad = re.match(
        r"^(-?\d+(?:\.\d+)?)\*x\^2\+(-?\d+(?:\.\d+)?)\*x\+(-?\d+(?:\.\d+)?)$",
        normalized,
    )
    if not quad:
        return None
    a, b, c = float(quad.group(1)), float(quad.group(2)), float(quad.group(3))
    return a * x * x + b * x + c


def _clip_segment_to_view(
    x0: float, y0: float, x1: float, y1: float, spec: dict
) -> tuple[tuple[float, float], tuple[float, float]] | None:
    xmin, xmax = spec["x_min"], spec["x_max"]
    ymin, ymax = spec["y_min"], spec["y_max"]
    t0, t1 = 0.0, 1.0
    dx, dy = x1 - x0, y1 - y0
    checks = [(-dx, x0 - xmin), (dx, xmax - x0), (-dy, y0 - ymin), (dy, ymax - y0)]
    for p, q in checks:
        if p == 0:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return None
            if r > t0:
                t0 = r
        else:
            if r < t0:
                return None
            if r < t1:
                t1 = r
    return (x0 + t0 * dx, y0 + t0 * dy), (x0 + t1 * dx, y0 + t1 * dy)


def _sample_function_path(fn: str, spec: dict, width: int, height: int) -> list[str]:
    mid_x = (spec["x_min"] + spec["x_max"]) / 2
    y_at_min = _evaluate_graph_function(fn, spec["x_min"])
    y_at_max = _evaluate_graph_function(fn, spec["x_max"])
    y_at_mid = _evaluate_graph_function(fn, mid_x)
    is_linear = (
        y_at_min is not None
        and y_at_max is not None
        and y_at_mid is not None
        and abs(y_at_mid - (y_at_min + y_at_max) / 2) < 1e-6
    )
    if is_linear and y_at_min is not None and y_at_max is not None:
        clipped = _clip_segment_to_view(
            spec["x_min"], y_at_min, spec["x_max"], y_at_max, spec
        )
        if not clipped:
            return []
        (cx0, cy0), (cx1, cy1) = clipped
        return [
            f"{_map_x(cx0, spec, width)},{_map_y(cy0, spec, height)}",
            f"{_map_x(cx1, spec, width)},{_map_y(cy1, spec, height)}",
        ]

    points: list[str] = []
    steps = 80
    for index in range(steps + 1):
        x = spec["x_min"] + ((spec["x_max"] - spec["x_min"]) * index) / steps
        y = _evaluate_graph_function(fn, x)
        if y is None or y < spec["y_min"] or y > spec["y_max"]:
            continue
        points.append(f"{_map_x(x, spec, width)},{_map_y(y, spec, height)}")
    return points


def _blank_coordinate_plane(spec: dict) -> dict:
    return {**spec, "functions": [], "points": [], "show_points": False, "regions": []}


def _half_plane_polygon_points(region: dict, spec: dict, width: int, height: int) -> list[str] | None:
    """Return SVG point strings for a half-plane clipped to the view box."""
    try:
        m = float(region["m"])
        b = float(region["b"])
        op = str(region.get("op", ">="))
    except (KeyError, TypeError, ValueError):
        return None
    xmin, xmax = float(spec["x_min"]), float(spec["x_max"])
    ymin, ymax = float(spec["y_min"]), float(spec["y_max"])
    above = op in {">", ">="}
    eps = 1e-9

    def on_side(x: float, y: float) -> bool:
        line_y = m * x + b
        return y >= line_y - eps if above else y <= line_y + eps

    corners = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
    edges = [
        (corners[0], corners[1]),
        (corners[1], corners[2]),
        (corners[2], corners[3]),
        (corners[3], corners[0]),
    ]
    hits: list[tuple[float, float]] = []
    for (x0, y0), (x1, y1) in edges:
        f0 = y0 - (m * x0 + b)
        f1 = y1 - (m * x1 + b)
        if abs(f0) < eps:
            hits.append((x0, y0))
        if abs(f1) < eps:
            hits.append((x1, y1))
        if f0 * f1 < 0:
            t = f0 / (f0 - f1)
            hits.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))

    uniq: list[tuple[float, float]] = []
    seen: set[str] = set()
    for p in [c for c in corners if on_side(*c)] + hits:
        key = f"{p[0]:.6f},{p[1]:.6f}"
        if key in seen:
            continue
        seen.add(key)
        uniq.append(p)
    if len(uniq) < 3:
        return None
    cx = sum(p[0] for p in uniq) / len(uniq)
    cy = sum(p[1] for p in uniq) / len(uniq)
    uniq.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    return [f"{_map_x(x, spec, width)},{_map_y(y, spec, height)}" for x, y in uniq]


def render_number_line_svg(spec: dict) -> str:
    axis = {
        "x_min": float(spec["min_value"]),
        "x_max": float(spec["max_value"]),
        "y_min": -1.0,
        "y_max": 1.0,
    }
    y = HEIGHT / 2
    start_x = _map_x(axis["x_min"], axis, WIDTH)
    end_x = _map_x(axis["x_max"], axis, WIDTH)
    blank = bool(spec.get("blank"))
    show_zero = spec.get("show_zero", True) is not False
    zero_in_range = axis["x_min"] <= 0 <= axis["x_max"]
    boundary_x = _map_x(float(spec["boundary"]), axis, WIDTH)
    boundary_high = spec.get("boundary_high")
    boundary_high_x = (
        _map_x(float(boundary_high), axis, WIDTH) if boundary_high is not None else None
    )
    direction = spec.get("direction", "right")
    if direction == "right":
        shade_start, shade_end = boundary_x, end_x
    elif direction == "left":
        shade_start, shade_end = start_x, boundary_x
    else:
        shade_start = boundary_x
        shade_end = boundary_high_x if boundary_high_x is not None else boundary_x
    outside = direction == "outside" and boundary_high_x is not None

    parts = [
        f'<svg class="question-graph number-line-graph" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'role="img" aria-label="{"Blank number line" if blank else "Number line"}">',
        f'<line x1="{start_x}" y1="{y}" x2="{end_x}" y2="{y}" class="graph-axis" />',
    ]
    if not blank and outside:
        parts.append(
            f'<polygon points="{start_x},{y - 8} {boundary_x},{y - 8} '
            f'{boundary_x},{y + 8} {start_x},{y + 8}" class="graph-shade" />'
        )
        parts.append(
            f'<polygon points="{boundary_high_x},{y - 8} {end_x},{y - 8} '
            f'{end_x},{y + 8} {boundary_high_x},{y + 8}" class="graph-shade" />'
        )
    elif not blank:
        parts.append(
            f'<polygon points="{shade_start},{y - 8} {shade_end},{y - 8} '
            f'{shade_end},{y + 8} {shade_start},{y + 8}" class="graph-shade" />'
        )
    if show_zero and zero_in_range:
        zx = _map_x(0, axis, WIDTH)
        parts.append(
            f'<g><line x1="{zx}" y1="{y - 6}" x2="{zx}" y2="{y + 6}" class="graph-tick" />'
            f'<text x="{zx}" y="{y + 20}" text-anchor="middle" class="graph-label">0</text></g>'
        )
    if not blank:
        cls = "graph-boundary-filled" if spec.get("inclusive") else "graph-boundary-open"
        parts.append(f'<circle cx="{boundary_x}" cy="{y}" r="5" class="{cls}" />')
        if boundary_high_x is not None:
            parts.append(
                f'<circle cx="{boundary_high_x}" cy="{y}" r="5" class="{cls}" />'
            )
    parts.append("</svg>")
    return "".join(parts)


def render_coordinate_plane_svg(spec: dict, *, blank_role: bool = False) -> str:
    width, height = WIDTH, PLANE_HEIGHT
    functions = [] if blank_role else list(spec.get("functions") or [])
    points = [] if blank_role else list(spec.get("points") or [])
    regions = [] if blank_role else list(spec.get("regions") or [])
    show_points = (not blank_role) and spec.get("show_points", True) is not False and bool(points)
    show_grid = spec.get("show_grid", True) is not False
    blank = blank_role or (not functions and not points and not regions)
    origin_x = _map_x(0, spec, width)
    origin_y = _map_y(0, spec, height)

    parts = [
        f'<svg class="question-graph coordinate-plane-graph" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{"Blank coordinate plane" if blank else "Coordinate plane"}">',
    ]
    if show_grid:
        x = math.ceil(spec["x_min"])
        while x <= math.floor(spec["x_max"]):
            px = _map_x(x, spec, width)
            parts.append(
                f'<line x1="{px}" y1="{PADDING}" x2="{px}" y2="{height - PADDING}" class="graph-grid" />'
            )
            x += 1
        y = math.ceil(spec["y_min"])
        while y <= math.floor(spec["y_max"]):
            py = _map_y(y, spec, height)
            parts.append(
                f'<line x1="{PADDING}" y1="{py}" x2="{width - PADDING}" y2="{py}" class="graph-grid" />'
            )
            y += 1
    parts.append(
        f'<line x1="{PADDING}" y1="{origin_y}" x2="{width - PADDING}" y2="{origin_y}" class="graph-axis" />'
    )
    parts.append(
        f'<line x1="{origin_x}" y1="{PADDING}" x2="{origin_x}" y2="{height - PADDING}" class="graph-axis" />'
    )
    for region in regions:
        if not isinstance(region, dict) or region.get("kind") != "half_plane":
            continue
        poly = _half_plane_polygon_points(region, spec, width, height)
        if poly:
            parts.append(f'<polygon points="{" ".join(poly)}" class="graph-shade" />')
    for idx, fn in enumerate(functions):
        line_points = _sample_function_path(str(fn), spec, width, height)
        if len(line_points) <= 1:
            continue
        dashed = False
        if idx < len(regions) and isinstance(regions[idx], dict):
            op = str(regions[idx].get("op", ""))
            dashed = op in {">", "<"}
        dash_attr = ' stroke-dasharray="6 4"' if dashed else ""
        parts.append(
            f'<polyline points="{" ".join(line_points)}" class="graph-line" fill="none"{dash_attr} />'
        )
    if show_points:
        for pt in points:
            if not isinstance(pt, (list, tuple)) or len(pt) < 2:
                continue
            px = _map_x(float(pt[0]), spec, width)
            py = _map_y(float(pt[1]), spec, height)
            parts.append(f'<circle cx="{px}" cy="{py}" r="4" class="graph-point" />')
    parts.append("</svg>")
    return "".join(parts)


def extract_prompt_graph(metadata: dict[str, Any] | None) -> dict[str, Any] | None:
    if not metadata:
        return None
    number_line = metadata.get("number_line_spec")
    graph_spec = metadata.get("graph_spec")
    graph_role = metadata.get("graph_role")
    if not number_line and not graph_spec:
        return None
    if graph_role == "blank" and isinstance(graph_spec, dict):
        graph_spec = _blank_coordinate_plane(graph_spec)
    return {
        "number_line_spec": number_line if isinstance(number_line, dict) else None,
        "graph_spec": graph_spec if isinstance(graph_spec, dict) else None,
        "graph_role": graph_role,
    }


def extract_answer_graph(metadata: dict[str, Any] | None) -> dict[str, Any] | None:
    if not metadata:
        return None
    number_line = metadata.get("answer_number_line_spec")
    graph_spec = metadata.get("answer_graph_spec")
    if not number_line and not graph_spec:
        return None
    return {
        "number_line_spec": number_line if isinstance(number_line, dict) else None,
        "graph_spec": graph_spec if isinstance(graph_spec, dict) else None,
        "graph_role": "stimulus",
    }


def render_graph_from_extracted(graph: dict[str, Any] | None) -> str:
    if not graph:
        return ""
    if graph.get("number_line_spec"):
        return render_number_line_svg(graph["number_line_spec"])
    if graph.get("graph_spec"):
        return render_coordinate_plane_svg(
            graph["graph_spec"],
            blank_role=graph.get("graph_role") == "blank",
        )
    return ""


def render_prompt_visuals(metadata: dict[str, Any] | None) -> str:
    """Prompt-side graphs + geometry diagram SVG."""
    parts: list[str] = []
    parts.append(render_graph_from_extracted(extract_prompt_graph(metadata)))
    if metadata:
        svg = metadata.get("diagram_svg")
        if isinstance(svg, str) and svg.lstrip().startswith("<svg"):
            parts.append(f'<div class="question-diagram">{svg}</div>')
    return "".join(parts)


def render_answer_visuals(metadata: dict[str, Any] | None) -> str:
    return render_graph_from_extracted(extract_answer_graph(metadata))


def has_visuals(metadata: dict[str, Any] | None) -> bool:
    if not metadata:
        return False
    if isinstance(metadata.get("diagram_svg"), str) and metadata["diagram_svg"].lstrip().startswith(
        "<svg"
    ):
        return True
    if metadata.get("number_line_spec") or metadata.get("graph_spec"):
        return True
    return False
