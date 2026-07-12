"""GeometryFigure — compose primitives and emit TikZ / SVG / metadata."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any
from xml.sax.saxutils import escape

from .primitives import (
    AngleMark,
    Arc,
    CirclePrim,
    Label,
    Line,
    Point,
    Polygon,
    Primitive,
    Ray,
    RightAngleMark,
    Segment,
    ShadedRegion,
)


def _norm(dx: float, dy: float) -> tuple[float, float]:
    length = math.hypot(dx, dy)
    if length < 1e-9:
        return 1.0, 0.0
    return dx / length, dy / length


def _angle_of(dx: float, dy: float) -> float:
    return math.degrees(math.atan2(dy, dx))


def _escape_tikz(text: str) -> str:
    return (
        text.replace("\\", "\\textbackslash{}")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("_", "\\_")
        .replace("%", "\\%")
        .replace("&", "\\&")
        .replace("#", "\\#")
        .replace("$", "\\$")
    )


@dataclass
class GeometryFigure:
    """Composable geometry figure that emits LaTeX (TikZ) and SVG."""

    points: dict[str, Point] = field(default_factory=dict)
    elements: list[Primitive] = field(default_factory=list)
    padding: float = 0.55
    scale: float = 40.0  # SVG pixels per figure unit
    stroke: str = "#1f2937"
    stroke_width: float = 1.75
    label_color: str = "#374151"
    mark_color: str = "#2563eb"
    kind: str = "geometry"

    def add_point(self, point: Point) -> Point:
        self.points[point.id] = point
        return point

    def add(self, *elements: Primitive) -> GeometryFigure:
        self.elements.extend(elements)
        return self

    def pt(self, point_id: str) -> Point:
        return self.points[point_id]

    def bounds(self) -> tuple[float, float, float, float]:
        xs: list[float] = []
        ys: list[float] = []
        for p in self.points.values():
            xs.append(p.x)
            ys.append(p.y)
        for el in self.elements:
            if isinstance(el, CirclePrim):
                c = self.pt(el.center)
                xs.extend([c.x - el.radius, c.x + el.radius])
                ys.extend([c.y - el.radius, c.y + el.radius])
            elif isinstance(el, Label):
                xs.append(el.x)
                ys.append(el.y)
            elif isinstance(el, ShadedRegion) and el.coords:
                for x, y in el.coords:
                    xs.append(x)
                    ys.append(y)
            elif isinstance(el, (Ray, Line)):
                a = self.pt(el.through_a if isinstance(el, Line) else el.start)
                b = self.pt(el.through_b if isinstance(el, Line) else el.through)
                ux, uy = _norm(b.x - a.x, b.y - a.y)
                ext = el.extend
                if isinstance(el, Line):
                    xs.extend([a.x - ux * ext, b.x + ux * ext])
                    ys.extend([a.y - uy * ext, b.y + uy * ext])
                else:
                    xs.append(b.x + ux * ext)
                    ys.append(b.y + uy * ext)
        if not xs:
            return 0.0, 0.0, 1.0, 1.0
        return min(xs), min(ys), max(xs), max(ys)

    def to_diagram_spec(self) -> dict[str, Any]:
        """Structured spec for clients / export tooling."""
        labels = [p.label or p.id for p in self.points.values() if p.label or p.show_dot]
        segments = [
            (el.start, el.end) for el in self.elements if isinstance(el, Segment)
        ]
        angles = [
            el.label
            for el in self.elements
            if isinstance(el, AngleMark) and el.label is not None
        ]
        return {
            "kind": self.kind,
            "labels": labels,
            "segments": segments,
            "angles": angles,
            "points": {
                pid: {"x": p.x, "y": p.y, "label": p.label}
                for pid, p in self.points.items()
            },
        }

    def to_metadata(self) -> dict[str, Any]:
        """Attach both web SVG and export LaTeX to question metadata."""
        return {
            "diagram_spec": self.to_diagram_spec(),
            "diagram_latex": self.to_tikz(),
            "diagram_svg": self.to_svg(),
        }

    # ------------------------------------------------------------------ TikZ
    def to_tikz(self) -> str:
        lines = [
            r"\begin{tikzpicture}[scale=1, every node/.style={font=\small}]",
        ]
        for p in self.points.values():
            lines.append(f"  \\coordinate ({p.id}) at ({p.x:.3f},{p.y:.3f});")
            if p.show_dot:
                lines.append(f"  \\fill ({p.id}) circle (1.2pt);")
            if p.label:
                lines.append(
                    f"  \\node at ({p.x + p.label_dx:.3f},{p.y + p.label_dy:.3f}) "
                    f"{{{_escape_tikz(p.label)}}};"
                )

        for el in self.elements:
            lines.extend(self._tikz_element(el))

        lines.append(r"\end{tikzpicture}")
        return "\n".join(lines)

    def _tikz_element(self, el: Primitive) -> list[str]:
        if isinstance(el, Segment):
            style = "dashed" if el.style == "dashed" else "thick"
            out = [f"  \\draw[{style}] ({el.start}) -- ({el.end});"]
            if el.ticks:
                out.extend(self._tikz_ticks(el.start, el.end, el.ticks))
            return out
        if isinstance(el, Ray):
            a, b = self.pt(el.start), self.pt(el.through)
            ux, uy = _norm(b.x - a.x, b.y - a.y)
            ex, ey = b.x + ux * el.extend, b.y + uy * el.extend
            return [f"  \\draw[thick] ({el.start}) -- ({ex:.3f},{ey:.3f});"]
        if isinstance(el, Line):
            a, b = self.pt(el.through_a), self.pt(el.through_b)
            ux, uy = _norm(b.x - a.x, b.y - a.y)
            x1, y1 = a.x - ux * el.extend, a.y - uy * el.extend
            x2, y2 = b.x + ux * el.extend, b.y + uy * el.extend
            return [f"  \\draw[thick] ({x1:.3f},{y1:.3f}) -- ({x2:.3f},{y2:.3f});"]
        if isinstance(el, Polygon):
            path = " -- ".join(f"({v})" for v in el.vertices)
            if el.closed:
                path += " -- cycle"
            if el.fill:
                return [
                    f"  \\fill[fill={el.fill}, fill opacity={el.fill_opacity}] {path};",
                    f"  \\draw[thick] {path};",
                ]
            return [f"  \\draw[thick] {path};"]
        if isinstance(el, CirclePrim):
            if el.fill:
                return [
                    f"  \\fill[fill={el.fill}, fill opacity={el.fill_opacity}] "
                    f"({el.center}) circle ({el.radius:.3f});",
                    f"  \\draw[thick] ({el.center}) circle ({el.radius:.3f});",
                ]
            return [f"  \\draw[thick] ({el.center}) circle ({el.radius:.3f});"]
        if isinstance(el, Arc):
            return [
                f"  \\draw[thick] ({el.center}) ++({el.start_deg:.2f}:{el.radius:.3f}) "
                f"arc ({el.start_deg:.2f}:{el.end_deg:.2f}:{el.radius:.3f});"
            ]
        if isinstance(el, AngleMark):
            return self._tikz_angle_mark(el)
        if isinstance(el, RightAngleMark):
            return self._tikz_right_angle(el)
        if isinstance(el, Label):
            return [
                f"  \\node at ({el.x:.3f},{el.y:.3f}) {{{_escape_tikz(el.text)}}};"
            ]
        if isinstance(el, ShadedRegion):
            if el.coords:
                pts = " -- ".join(f"({x:.3f},{y:.3f})" for x, y in el.coords)
            else:
                pts = " -- ".join(f"({v})" for v in el.vertices)
            return [
                f"  \\fill[{el.fill}, fill opacity={el.fill_opacity}] {pts} -- cycle;"
            ]
        return []

    def _tikz_ticks(self, start: str, end: str, count: int) -> list[str]:
        a, b = self.pt(start), self.pt(end)
        mx, my = (a.x + b.x) / 2, (a.y + b.y) / 2
        ux, uy = _norm(b.x - a.x, b.y - a.y)
        px, py = -uy, ux
        out: list[str] = []
        spacing = 0.08
        for i in range(count):
            offset = (i - (count - 1) / 2) * spacing
            cx, cy = mx + ux * offset, my + uy * offset
            out.append(
                f"  \\draw[thick] ({cx - px * 0.12:.3f},{cy - py * 0.12:.3f}) -- "
                f"({cx + px * 0.12:.3f},{cy + py * 0.12:.3f});"
            )
        return out

    def _tikz_angle_mark(self, el: AngleMark) -> list[str]:
        v, p1, p2 = self.pt(el.vertex), self.pt(el.ray1), self.pt(el.ray2)
        a1 = _angle_of(p1.x - v.x, p1.y - v.y)
        a2 = _angle_of(p2.x - v.x, p2.y - v.y)
        # Sweep the smaller interior angle from a1 toward a2
        start, end = self._ordered_arc(a1, a2)
        out = [
            f"  \\draw[{self.mark_color}] ({el.vertex}) ++({start:.2f}:{el.radius:.3f}) "
            f"arc ({start:.2f}:{end:.2f}:{el.radius:.3f});"
        ]
        if el.label:
            mid = (start + end) / 2
            lr = el.label_radius if el.label_radius is not None else el.radius + 0.35
            lx = v.x + lr * math.cos(math.radians(mid))
            ly = v.y + lr * math.sin(math.radians(mid))
            out.append(f"  \\node at ({lx:.3f},{ly:.3f}) {{{_escape_tikz(el.label)}}};")
        return out

    def _tikz_right_angle(self, el: RightAngleMark) -> list[str]:
        v, p1, p2 = self.pt(el.vertex), self.pt(el.leg1), self.pt(el.leg2)
        u1x, u1y = _norm(p1.x - v.x, p1.y - v.y)
        u2x, u2y = _norm(p2.x - v.x, p2.y - v.y)
        s = el.size
        a = (v.x + u1x * s, v.y + u1y * s)
        c = (v.x + u2x * s, v.y + u2y * s)
        b = (v.x + (u1x + u2x) * s, v.y + (u1y + u2y) * s)
        return [
            f"  \\draw[thick] ({a[0]:.3f},{a[1]:.3f}) -- ({b[0]:.3f},{b[1]:.3f}) -- "
            f"({c[0]:.3f},{c[1]:.3f});"
        ]

    @staticmethod
    def _ordered_arc(a1: float, a2: float) -> tuple[float, float]:
        """Return (start, end) sweeping the smaller angle from a1 to a2."""
        a1 = a1 % 360
        a2 = a2 % 360
        ccw = (a2 - a1) % 360
        if ccw <= 180:
            return a1, a1 + ccw
        return a2, a2 + ((a1 - a2) % 360)

    # ------------------------------------------------------------------ SVG
    def to_svg(self) -> str:
        xmin, ymin, xmax, ymax = self.bounds()
        pad = self.padding
        xmin -= pad
        ymin -= pad
        xmax += pad
        ymax += pad
        width = max(xmax - xmin, 0.5)
        height = max(ymax - ymin, 0.5)
        px = width * self.scale
        py = height * self.scale

        def sx(x: float) -> float:
            return (x - xmin) * self.scale

        def sy(y: float) -> float:
            return (ymax - y) * self.scale

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {px:.1f} {py:.1f}" '
            f'width="{px:.1f}" height="{py:.1f}" role="img" aria-label="Geometry diagram">',
        ]

        for el in self.elements:
            parts.extend(self._svg_element(el, sx, sy))

        for p in self.points.values():
            if p.show_dot:
                parts.append(
                    f'<circle cx="{sx(p.x):.1f}" cy="{sy(p.y):.1f}" r="3" '
                    f'fill="{self.stroke}"/>'
                )
            if p.label:
                parts.append(
                    f'<text x="{sx(p.x + p.label_dx):.1f}" y="{sy(p.y + p.label_dy):.1f}" '
                    f'class="diagram-label" fill="{self.label_color}" font-size="13" '
                    f'text-anchor="middle" dominant-baseline="middle">'
                    f"{escape(p.label)}</text>"
                )

        parts.append("</svg>")
        return "".join(parts)

    def _svg_element(self, el: Primitive, sx, sy) -> list[str]:  # noqa: ANN001
        sw = self.stroke_width
        stroke = self.stroke
        if isinstance(el, Segment):
            a, b = self.pt(el.start), self.pt(el.end)
            dash = ' stroke-dasharray="6 4"' if el.style == "dashed" else ""
            out = [
                f'<line x1="{sx(a.x):.1f}" y1="{sy(a.y):.1f}" x2="{sx(b.x):.1f}" '
                f'y2="{sy(b.y):.1f}" stroke="{stroke}" stroke-width="{sw}"'
                f'{dash} fill="none"/>'
            ]
            if el.ticks:
                out.extend(self._svg_ticks(el.start, el.end, el.ticks, sx, sy))
            return out
        if isinstance(el, Ray):
            a, b = self.pt(el.start), self.pt(el.through)
            ux, uy = _norm(b.x - a.x, b.y - a.y)
            ex, ey = b.x + ux * el.extend, b.y + uy * el.extend
            return [
                f'<line x1="{sx(a.x):.1f}" y1="{sy(a.y):.1f}" x2="{sx(ex):.1f}" '
                f'y2="{sy(ey):.1f}" stroke="{stroke}" stroke-width="{sw}" fill="none"/>'
            ]
        if isinstance(el, Line):
            a, b = self.pt(el.through_a), self.pt(el.through_b)
            ux, uy = _norm(b.x - a.x, b.y - a.y)
            x1, y1 = a.x - ux * el.extend, a.y - uy * el.extend
            x2, y2 = b.x + ux * el.extend, b.y + uy * el.extend
            return [
                f'<line x1="{sx(x1):.1f}" y1="{sy(y1):.1f}" x2="{sx(x2):.1f}" '
                f'y2="{sy(y2):.1f}" stroke="{stroke}" stroke-width="{sw}" fill="none"/>'
            ]
        if isinstance(el, Polygon):
            pts = " ".join(
                f"{sx(self.pt(v).x):.1f},{sy(self.pt(v).y):.1f}" for v in el.vertices
            )
            if el.fill:
                return [
                    f'<polygon points="{pts}" fill="{el.fill}" '
                    f'fill-opacity="{el.fill_opacity}" stroke="{stroke}" '
                    f'stroke-width="{sw}"/>'
                ]
            tag = "polygon" if el.closed else "polyline"
            return [
                f'<{tag} points="{pts}" fill="none" stroke="{stroke}" '
                f'stroke-width="{sw}"/>'
            ]
        if isinstance(el, CirclePrim):
            c = self.pt(el.center)
            r = el.radius * self.scale
            fill = el.fill or "none"
            opacity = f' fill-opacity="{el.fill_opacity}"' if el.fill else ""
            return [
                f'<circle cx="{sx(c.x):.1f}" cy="{sy(c.y):.1f}" r="{r:.1f}" '
                f'fill="{fill}"{opacity} stroke="{stroke}" stroke-width="{sw}"/>'
            ]
        if isinstance(el, Arc):
            return [self._svg_arc(el, sx, sy)]
        if isinstance(el, AngleMark):
            return self._svg_angle_mark(el, sx, sy)
        if isinstance(el, RightAngleMark):
            return self._svg_right_angle(el, sx, sy)
        if isinstance(el, Label):
            return [
                f'<text x="{sx(el.x):.1f}" y="{sy(el.y):.1f}" class="diagram-label" '
                f'fill="{self.label_color}" font-size="13" text-anchor="middle" '
                f'dominant-baseline="middle" stroke="#ffffff" stroke-width="3.5" '
                f'paint-order="stroke fill">{escape(el.text)}</text>'
            ]
        if isinstance(el, ShadedRegion):
            if el.coords:
                pts = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in el.coords)
            else:
                pts = " ".join(
                    f"{sx(self.pt(v).x):.1f},{sy(self.pt(v).y):.1f}" for v in el.vertices
                )
            return [
                f'<polygon points="{pts}" fill="{el.fill}" '
                f'fill-opacity="{el.fill_opacity}" stroke="none"/>'
            ]
        return []

    def _svg_ticks(self, start: str, end: str, count: int, sx, sy) -> list[str]:  # noqa: ANN001
        a, b = self.pt(start), self.pt(end)
        mx, my = (a.x + b.x) / 2, (a.y + b.y) / 2
        ux, uy = _norm(b.x - a.x, b.y - a.y)
        px, py = -uy, ux
        out: list[str] = []
        spacing = 0.08
        for i in range(count):
            offset = (i - (count - 1) / 2) * spacing
            cx, cy = mx + ux * offset, my + uy * offset
            out.append(
                f'<line x1="{sx(cx - px * 0.12):.1f}" y1="{sy(cy - py * 0.12):.1f}" '
                f'x2="{sx(cx + px * 0.12):.1f}" y2="{sy(cy + py * 0.12):.1f}" '
                f'stroke="{self.stroke}" stroke-width="{self.stroke_width}"/>'
            )
        return out

    def _svg_arc(self, el: Arc, sx, sy) -> str:  # noqa: ANN001
        c = self.pt(el.center)
        start = math.radians(el.start_deg)
        end = math.radians(el.end_deg)
        x1 = c.x + el.radius * math.cos(start)
        y1 = c.y + el.radius * math.sin(start)
        x2 = c.x + el.radius * math.cos(end)
        y2 = c.y + el.radius * math.sin(end)
        sweep = (el.end_deg - el.start_deg) % 360
        large = 1 if sweep > 180 else 0
        # SVG y is flipped; negate sweep direction
        return (
            f'<path d="M {sx(x1):.1f} {sy(y1):.1f} A {el.radius * self.scale:.1f} '
            f'{el.radius * self.scale:.1f} 0 {large} 0 {sx(x2):.1f} {sy(y2):.1f}" '
            f'fill="none" stroke="{self.stroke}" stroke-width="{self.stroke_width}"/>'
        )

    def _svg_angle_mark(self, el: AngleMark, sx, sy) -> list[str]:  # noqa: ANN001
        v, p1, p2 = self.pt(el.vertex), self.pt(el.ray1), self.pt(el.ray2)
        a1 = _angle_of(p1.x - v.x, p1.y - v.y)
        a2 = _angle_of(p2.x - v.x, p2.y - v.y)
        start, end = self._ordered_arc(a1, a2)
        arc = Arc(center=el.vertex, radius=el.radius, start_deg=start, end_deg=end)
        # Temporarily use mark color via path rewrite
        path = self._svg_arc(arc, sx, sy).replace(
            f'stroke="{self.stroke}"', f'stroke="{self.mark_color}"'
        )
        out = [path]
        if el.label:
            mid = (start + end) / 2
            lr = el.label_radius if el.label_radius is not None else el.radius + 0.35
            lx = v.x + lr * math.cos(math.radians(mid))
            ly = v.y + lr * math.sin(math.radians(mid))
            out.append(
                f'<text x="{sx(lx):.1f}" y="{sy(ly):.1f}" class="diagram-label" '
                f'fill="{self.mark_color}" font-size="12" text-anchor="middle" '
                f'dominant-baseline="middle">{escape(el.label)}</text>'
            )
        return out

    def _svg_right_angle(self, el: RightAngleMark, sx, sy) -> list[str]:  # noqa: ANN001
        v, p1, p2 = self.pt(el.vertex), self.pt(el.leg1), self.pt(el.leg2)
        u1x, u1y = _norm(p1.x - v.x, p1.y - v.y)
        u2x, u2y = _norm(p2.x - v.x, p2.y - v.y)
        s = el.size
        a = (v.x + u1x * s, v.y + u1y * s)
        c = (v.x + u2x * s, v.y + u2y * s)
        b = (v.x + (u1x + u2x) * s, v.y + (u1y + u2y) * s)
        return [
            f'<polyline points="{sx(a[0]):.1f},{sy(a[1]):.1f} '
            f'{sx(b[0]):.1f},{sy(b[1]):.1f} {sx(c[0]):.1f},{sy(c[1]):.1f}" '
            f'fill="none" stroke="{self.stroke}" stroke-width="{self.stroke_width}"/>'
        ]
