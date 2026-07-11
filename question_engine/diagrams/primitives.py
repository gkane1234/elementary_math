"""Geometry diagram primitives for the figure DSL."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Point:
    """Named point in figure coordinates (y increases upward)."""

    id: str
    x: float
    y: float
    label: str | None = None
    label_dx: float = 0.18
    label_dy: float = 0.18
    show_dot: bool = True


@dataclass
class Segment:
    """Line segment between two named points."""

    start: str
    end: str
    ticks: int = 0
    style: Literal["solid", "dashed"] = "solid"


@dataclass
class Ray:
    """Ray starting at ``start`` and passing through ``through``."""

    start: str
    through: str
    extend: float = 1.4


@dataclass
class Line:
    """Infinite line through two named points (drawn as a long segment)."""

    through_a: str
    through_b: str
    extend: float = 1.6


@dataclass
class Polygon:
    """Closed or open polygon through named vertices (arbitrary shapes)."""

    vertices: list[str]
    closed: bool = True
    fill: str | None = None
    fill_opacity: float = 0.25


@dataclass
class CirclePrim:
    """Circle centered at a named point."""

    center: str
    radius: float
    fill: str | None = None
    fill_opacity: float = 0.2


@dataclass
class Arc:
    """Circular arc centered at a named point (degrees, CCW from +x)."""

    center: str
    radius: float
    start_deg: float
    end_deg: float


@dataclass
class AngleMark:
    """Arc mark at a vertex between two rays."""

    vertex: str
    ray1: str
    ray2: str
    radius: float = 0.45
    label: str | None = None
    label_radius: float | None = None


@dataclass
class RightAngleMark:
    """Square mark indicating a right angle."""

    vertex: str
    leg1: str
    leg2: str
    size: float = 0.32


@dataclass
class Label:
    """Free-floating text label in figure coordinates."""

    text: str
    x: float
    y: float
    anchor: Literal["c", "n", "s", "e", "w", "ne", "nw", "se", "sw"] = "c"


@dataclass
class ShadedRegion:
    """Filled polygon region (by point ids or explicit coordinates)."""

    vertices: list[str] = field(default_factory=list)
    coords: list[tuple[float, float]] = field(default_factory=list)
    fill: str = "#93c5fd"
    fill_opacity: float = 0.35


# Union alias for type hints
Primitive = (
    Segment
    | Ray
    | Line
    | Polygon
    | CirclePrim
    | Arc
    | AngleMark
    | RightAngleMark
    | Label
    | ShadedRegion
)
