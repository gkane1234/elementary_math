"""Small self-contained SVG figures for Grade 6 visual models."""

from __future__ import annotations

from xml.sax.saxutils import escape


def _svg(inner: str, width: int = 360, height: int = 220) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img"><rect width="100%" height="100%" '
        f'fill="#fff"/>{inner}</svg>'
    )


def area_model_svg(left: str, right_a: str, right_b: str) -> str:
    """Rectangle split to model ``left(right_a + right_b)``."""
    return _svg(
        '<rect x="50" y="55" width="250" height="110" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<rect x="50" y="55" width="125" height="110" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<line x1="175" y1="55" x2="175" y2="165" stroke="#1e3a8a" stroke-width="2"/>'
        f'<text x="34" y="115" text-anchor="middle" font-size="18">{escape(left)}</text>'
        f'<text x="112" y="188" text-anchor="middle" font-size="17">{escape(right_a)}</text>'
        f'<text x="238" y="188" text-anchor="middle" font-size="17">{escape(right_b)}</text>'
    )


def rectangle_measure_svg(base: str, height: str) -> str:
    """Rectangle with a labeled base and height."""
    return _svg(
        '<rect x="65" y="50" width="220" height="115" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        f'<text x="175" y="190" text-anchor="middle" font-size="17">{escape(base)}</text>'
        f'<text x="308" y="112" font-size="17">{escape(height)}</text>'
    )


def triangle_measure_svg(base: str, height: str) -> str:
    """Right triangle with its base and perpendicular height labeled."""
    return _svg(
        '<polygon points="70,165 285,165 70,48" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<path d="M70 148 h17 v17" fill="none" stroke="#1e3a8a" stroke-width="1.5"/>'
        f'<text x="177" y="190" text-anchor="middle" font-size="17">{escape(base)}</text>'
        f'<text x="45" y="108" font-size="17">{escape(height)}</text>'
    )


def _tape_segment_widths(weights: list[float], *, min_px: float = 40.0, target_px: float = 300.0) -> list[float]:
    """Allocate horizontal space proportional to weights, with a readable minimum."""
    if not weights:
        return []
    positive = [max(0.5, float(w)) for w in weights]
    total_w = sum(positive)
    raw = [target_px * w / total_w for w in positive]
    # Enforce minima, then rescale so the bar still fits roughly on target_px.
    bumped = [max(min_px, w) for w in raw]
    bumped_sum = sum(bumped)
    if bumped_sum <= target_px * 1.35:
        return bumped
    scale = (target_px * 1.35) / bumped_sum
    return [max(min_px, w * scale) for w in bumped]


def tape_svg(
    parts: int | None = None,
    total: int | str | None = None,
    *,
    inequality: bool = False,
    labels: list[str] | None = None,
    weights: list[float] | None = None,
    title: str | None = None,
) -> str:
    """Tape / bar diagram with labels drawn *inside* each segment.

    Two common Grade 6 forms:

    - Uniform algebra: equal boxes labeled ``x`` (pass ``parts`` + ``total``, or
      ``labels=["x","x","x"]``).
    - Non-uniform missing piece: unequal segments with known sizes inside and one
      ``?`` (pass ``labels`` + proportional ``weights``).

    ``parts``/``total`` remain supported for the classic equal-parts case.
    """
    _ = inequality  # Prompt carries = / ≤; kept for call-site compatibility.

    if labels is None:
        if parts is None or total is None:
            raise ValueError("tape_svg requires labels, or both parts and total")
        labels = ["x"] * max(1, int(parts))
        if title is None:
            title = "Equal-size parts"
        weights = [1.0] * len(labels)
    else:
        labels = [str(lab) for lab in labels]
        if not labels:
            raise ValueError("tape_svg labels must be non-empty")
        if weights is None:
            weights = [1.0] * len(labels)
        elif len(weights) != len(labels):
            raise ValueError("tape_svg weights must match labels length")

    if total is None:
        raise ValueError("tape_svg requires total")

    seg_widths = _tape_segment_widths(list(weights), min_px=40.0, target_px=max(220.0, 48.0 * len(labels)))
    bar_h = 48
    bar_y = 78
    left = 28
    x = left
    parts_svg: list[str] = []
    for label, w in zip(labels, seg_widths):
        # Missing piece gets a lighter dashed cell; known / x cells are solid.
        if label.strip() == "?":
            fill = "#eff6ff"
            dash = ' stroke-dasharray="4 3"'
        else:
            fill = "#bfdbfe"
            dash = ""
        cx = x + w / 2
        cy = bar_y + bar_h / 2 + 6
        font = 20 if len(label) <= 2 else 16
        parts_svg.append(
            f'<rect x="{x:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" '
            f'fill="{fill}" stroke="#1e3a8a" stroke-width="1.5"{dash}/>'
            f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" '
            f'font-size="{font}" fill="#1e3a8a">{escape(label)}</text>'
        )
        x += w

    bar_right = x
    total_x = bar_right + 18
    eq_x = bar_right + 6
    svg_w = int(max(330, total_x + 56))
    title_svg = ""
    if title:
        title_svg = (
            f'<text x="{(left + bar_right) / 2:.1f}" y="52" text-anchor="middle" '
            f'font-size="14" fill="#4b5563">{escape(title)}</text>'
        )
    # Bracket under the whole tape emphasizing the total length.
    bracket = (
        f'<path d="M{left:.1f} {bar_y + bar_h + 10} '
        f'v8 h{bar_right - left:.1f} v-8" fill="none" stroke="#6b7280" stroke-width="1.5"/>'
    )
    return _svg(
        f"{title_svg}{''.join(parts_svg)}"
        f'<text x="{eq_x:.1f}" y="{bar_y + bar_h / 2 + 7:.1f}" font-size="20" fill="#1e3a8a">=</text>'
        f'<text x="{total_x:.1f}" y="{bar_y + bar_h / 2 + 7:.1f}" font-size="18" fill="#1e3a8a">'
        f"{escape(str(total))}</text>"
        f"{bracket}",
        width=svg_w,
        height=180,
    )


def hanger_svg(parts: int, total: int, *, inequality: bool = False) -> str:
    _ = inequality  # API parity with tape_svg; prompt carries = / ≤
    left = 50
    blocks = "".join(
        f'<rect x="{left + i * 32}" y="105" width="28" height="28" rx="3" fill="#bfdbfe" stroke="#1e3a8a"/>'
        for i in range(parts)
    )
    return _svg(
        f'<line x1="170" y1="25" x2="170" y2="55" stroke="#374151" stroke-width="3"/>'
        f'<line x1="45" y1="55" x2="295" y2="55" stroke="#374151" stroke-width="3"/>'
        f'<line x1="70" y1="55" x2="70" y2="105" stroke="#374151" stroke-width="2"/>'
        f'<line x1="270" y1="55" x2="270" y2="105" stroke="#374151" stroke-width="2"/>'
        f'{blocks}<text x="75" y="153" font-size="17">x blocks</text>'
        f'<text x="250" y="120" font-size="22">{total}</text>',
        height=180,
    )


def grid_polygon_svg(points: list[tuple[int, int]], *, shaded: bool = False) -> str:
    scale, ox, oy = 28, 55, 175
    lines = "".join(
        f'<line x1="{ox + i * scale}" y1="35" x2="{ox + i * scale}" y2="{oy}" stroke="#d1d5db"/>'
        for i in range(9)
    ) + "".join(
        f'<line x1="{ox}" y1="{oy - i * scale}" x2="{ox + 8 * scale}" y2="{oy - i * scale}" stroke="#d1d5db"/>'
        for i in range(6)
    )
    coords = " ".join(f"{ox + x * scale},{oy - y * scale}" for x, y in points)
    fill = "#93c5fd" if shaded else "#dbeafe"
    return _svg(
        f'{lines}<line x1="{ox}" y1="{oy}" x2="{ox + 8 * scale}" y2="{oy}" stroke="#374151"/>'
        f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="35" stroke="#374151"/>'
        f'<polygon points="{coords}" fill="{fill}" stroke="#1e3a8a" stroke-width="2"/>'
    )


def _coordinate_plane_viewport(
    *point_sets: list[tuple[int, int]],
    pad_cells: int = 1,
) -> tuple[int, int, int, int]:
    """Return integer (x_min, x_max, y_min, y_max) covering origin and points."""
    xs = [0]
    ys = [0]
    for points in point_sets:
        xs.extend(int(p[0]) for p in points)
        ys.extend(int(p[1]) for p in points)
    x_min = min(xs) - pad_cells
    x_max = max(xs) + pad_cells
    y_min = min(ys) - pad_cells
    y_max = max(ys) + pad_cells
    # Keep the grid readable.
    x_min = max(x_min, -10)
    x_max = min(x_max, 12)
    y_min = max(y_min, -10)
    y_max = min(y_max, 12)
    if x_min >= x_max:
        x_min, x_max = -5, 5
    if y_min >= y_max:
        y_min, y_max = -5, 5
    return x_min, x_max, y_min, y_max


def coordinate_polygon_svg(
    points: list[tuple[int, int]],
    *,
    labels: list[str] | None = None,
) -> str:
    """Polygon on a labeled coordinate plane (Grade 6 perimeter / transforms)."""
    return coordinate_transform_svg(points, labels=labels)


def coordinate_transform_svg(
    original: list[tuple[int, int]],
    *,
    image: list[tuple[int, int]] | None = None,
    labels: list[str] | None = None,
    image_labels: list[str] | None = None,
    blank: bool = False,
) -> str:
    """Coordinate-plane figure for geometric transformations.

    - Prompt (``image=None``): show the pre-image polygon.
    - Answer key (``image`` set): show original lightly and the image solid.
    - ``blank=True``: axes/grid only (student work plane).
    """
    sets = [original]
    if image:
        sets.append(image)
    x_min, x_max, y_min, y_max = _coordinate_plane_viewport(*sets)
    scale = 26
    pad = 36
    width = pad * 2 + (x_max - x_min) * scale
    height = pad * 2 + (y_max - y_min) * scale

    def px(x: int | float) -> float:
        return pad + (float(x) - x_min) * scale

    def py(y: int | float) -> float:
        return pad + (y_max - float(y)) * scale

    grid = "".join(
        f'<line x1="{px(x)}" y1="{py(y_max)}" x2="{px(x)}" y2="{py(y_min)}" stroke="#e5e7eb"/>'
        for x in range(x_min, x_max + 1)
    ) + "".join(
        f'<line x1="{px(x_min)}" y1="{py(y)}" x2="{px(x_max)}" y2="{py(y)}" stroke="#e5e7eb"/>'
        for y in range(y_min, y_max + 1)
    )
    axes = (
        f'<line x1="{px(x_min)}" y1="{py(0)}" x2="{px(x_max)}" y2="{py(0)}" stroke="#374151" stroke-width="1.5"/>'
        f'<line x1="{px(0)}" y1="{py(y_min)}" x2="{px(0)}" y2="{py(y_max)}" stroke="#374151" stroke-width="1.5"/>'
    )
    ticks = "".join(
        f'<text x="{px(x)}" y="{py(0) + 14}" text-anchor="middle" font-size="11" fill="#4b5563">'
        f"{x}</text>"
        for x in range(x_min, x_max + 1)
        if x != 0
    ) + "".join(
        f'<text x="{px(0) - 10}" y="{py(y) + 4}" text-anchor="end" font-size="11" fill="#4b5563">'
        f"{y}</text>"
        for y in range(y_min, y_max + 1)
        if y != 0
    )
    if blank:
        return _svg(f"{grid}{axes}{ticks}", width=int(width), height=int(height))

    def _poly(
        points: list[tuple[int, int]],
        *,
        fill: str,
        stroke: str,
        opacity: str = "0.7",
        dash: str | None = None,
        labs: list[str] | None = None,
        lab_color: str = "#1e3a8a",
    ) -> str:
        poly = " ".join(f"{px(x)},{py(y)}" for x, y in points)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        dots = "".join(
            f'<circle cx="{px(x)}" cy="{py(y)}" r="3.5" fill="{stroke}"/>' for x, y in points
        )
        label_text = ""
        if labs:
            for lab, (x, y) in zip(labs, points):
                label_text += (
                    f'<text x="{px(x) + 6}" y="{py(y) - 6}" font-size="12" fill="{lab_color}">'
                    f"{escape(lab)}</text>"
                )
        return (
            f'<polygon points="{poly}" fill="{fill}" fill-opacity="{opacity}" '
            f'stroke="{stroke}" stroke-width="2"{dash_attr}/>'
            f"{dots}{label_text}"
        )

    body = _poly(
        original,
        fill="#dbeafe",
        stroke="#1e3a8a",
        opacity="0.35" if image else "0.7",
        dash="5 4" if image else None,
        labs=labels,
        lab_color="#64748b" if image else "#1e3a8a",
    )
    if image:
        body += _poly(
            image,
            fill="#bbf7d0",
            stroke="#166534",
            opacity="0.75",
            labs=image_labels,
            lab_color="#166534",
        )
    return _svg(f"{grid}{axes}{ticks}{body}", width=int(width), height=int(height))


def cube_net_svg(side: int, *, invalid: bool = False) -> str:
    cell, ox, oy = 42, 112, 22
    cells = [(1, 0), (1, 1), (0, 1), (2, 1), (1, 2), (1, 3)]
    if invalid:
        cells[-1] = (3, 1)
    rects = "".join(
        f'<rect x="{ox + x * cell}" y="{oy + y * cell}" width="{cell}" height="{cell}" '
        f'fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        for x, y in cells
    )
    return _svg(rects, 310, 220)


def prism_svg(length: str, width: str, height: str) -> str:
    return _svg(
        '<polygon points="75,80 205,80 250,45 120,45" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="75,80 205,80 205,160 75,160" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="205,80 250,45 250,125 205,160" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
        f'<text x="140" y="180" text-anchor="middle" font-size="16">{escape(length)}</text>'
        f'<text x="270" y="105" font-size="16">{escape(width)}</text>'
        f'<text x="55" y="125" font-size="16">{escape(height)}</text>'
    )


# Grade 6 classify/naming solids (unlabeled isometric sketches).
POLYHEDRON_KINDS: tuple[str, ...] = (
    "cube",
    "rectangular prism",
    "triangular prism",
    "square pyramid",
    "triangular pyramid",
)


def _cube_solid_svg() -> str:
    return _svg(
        '<polygon points="110,70 200,70 245,35 155,35" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="110,70 200,70 200,160 110,160" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="200,70 245,35 245,125 200,160" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
    )


def _rectangular_prism_solid_svg() -> str:
    return _svg(
        '<polygon points="70,75 220,75 265,40 115,40" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="70,75 220,75 220,155 70,155" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="220,75 265,40 265,120 220,155" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
    )


def _triangular_prism_solid_svg() -> str:
    # Right triangular prism: front triangle extruded back-right.
    return _svg(
        '<polygon points="80,150 200,150 140,55" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="200,150 250,120 190,30 140,55" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="80,150 140,55 190,30 130,125" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<line x1="140" y1="55" x2="190" y2="30" stroke="#1e3a8a" stroke-width="2"/>'
    )


def _square_pyramid_solid_svg() -> str:
    return _svg(
        '<polygon points="90,155 230,155 255,120 115,120" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="90,155 230,155 172,40" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="230,155 255,120 172,40" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<line x1="115" y1="120" x2="172" y2="40" stroke="#1e3a8a" stroke-width="1.5" stroke-dasharray="4 3"/>'
    )


def _triangular_pyramid_solid_svg() -> str:
    return _svg(
        '<polygon points="100,160 250,160 175,115" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="100,160 250,160 175,40" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="250,160 175,115 175,40" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<line x1="100" y1="160" x2="175" y2="115" stroke="#1e3a8a" stroke-width="1.5" stroke-dasharray="4 3"/>'
    )


def polyhedron_svg(kind: str) -> str:
    """Unlabeled isometric sketch for a Grade 6 polyhedron name."""
    builders = {
        "cube": _cube_solid_svg,
        "rectangular prism": _rectangular_prism_solid_svg,
        "triangular prism": _triangular_prism_solid_svg,
        "square pyramid": _square_pyramid_solid_svg,
        "triangular pyramid": _triangular_pyramid_solid_svg,
    }
    try:
        return builders[kind]()
    except KeyError as exc:
        raise ValueError(f"Unknown polyhedron kind: {kind}") from exc
