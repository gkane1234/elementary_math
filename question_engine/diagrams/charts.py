"""SVG chart builders for statistics question metadata (``diagram_svg``)."""

from __future__ import annotations

from collections import Counter
from xml.sax.saxutils import escape


def _svg_wrap(inner: str, *, width: int = 320, height: int = 200, view_box: str | None = None) -> str:
    vb = view_box or f"0 0 {width} {height}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="{vb}" role="img">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
        f"{inner}</svg>"
    )


def dot_plot_svg(
    values: list[float],
    *,
    title: str = "Dot plot",
    width: int = 340,
    height: int = 180,
    blank: bool = False,
    tick_min: float | None = None,
    tick_max: float | None = None,
) -> str:
    """Render a simple one-axis dot plot.

    When ``blank`` is True, only the axis and tick labels are drawn (no dots),
    suitable as student workspace for create-from-data prompts.
    """
    if not values and tick_min is None and tick_max is None:
        return _svg_wrap("", width=width, height=height)

    counts = Counter(int(v) if v == int(v) else v for v in values) if values else Counter()
    if tick_min is not None and tick_max is not None:
        lo, hi = float(tick_min), float(tick_max)
    elif counts:
        keys = sorted(counts.keys())
        lo, hi = float(keys[0]), float(keys[-1])
    else:
        return _svg_wrap("", width=width, height=height)

    if hi < lo:
        lo, hi = hi, lo
    span = max(hi - lo, 1.0)
    pad_x, axis_y = 40, height - 40
    usable = width - 2 * pad_x

    # Integer ticks across the range for a usable blank axis.
    tick_lo = int(lo) if lo == int(lo) else int(lo // 1)
    tick_hi = int(hi) if hi == int(hi) else int(hi) + (0 if hi == int(hi) else 1)
    tick_values = list(range(tick_lo, tick_hi + 1))
    if not tick_values:
        tick_values = [tick_lo]

    parts: list[str] = [
        f'<text x="{width // 2}" y="18" text-anchor="middle" font-size="13" '
        f'fill="#374151" font-family="system-ui,sans-serif">{escape(title)}</text>',
        f'<line x1="{pad_x}" y1="{axis_y}" x2="{width - pad_x}" y2="{axis_y}" '
        f'stroke="#1f2937" stroke-width="1.5"/>',
    ]
    for tick in tick_values:
        x = pad_x + ((float(tick) - lo) / span) * usable
        parts.append(
            f'<line x1="{x:.1f}" y1="{axis_y - 4}" x2="{x:.1f}" y2="{axis_y + 4}" '
            f'stroke="#1f2937" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{axis_y + 16}" text-anchor="middle" font-size="11" '
            f'fill="#4b5563" font-family="system-ui,sans-serif">{escape(str(tick))}</text>'
        )

    if not blank:
        for key, count in counts.items():
            x = pad_x + ((float(key) - lo) / span) * usable
            for i in range(count):
                cy = axis_y - 12 - i * 14
                parts.append(
                    f'<circle cx="{x:.1f}" cy="{cy}" r="5" fill="#2563eb" '
                    f'stroke="#1e40af" stroke-width="0.8"/>'
                )
    return _svg_wrap("".join(parts), width=width, height=height)


def histogram_svg(
    values: list[float],
    bins: list[tuple[float, float]],
    *,
    title: str = "Histogram",
    width: int = 360,
    height: int = 200,
    blank: bool = False,
) -> str:
    """Render a simple histogram from precomputed bins.

    When ``blank`` is True, only the axes and bin labels are drawn (no bars),
    suitable as student workspace for create-from-data prompts.
    """
    if not bins:
        return _svg_wrap("", width=width, height=height)

    def count_bin(low: float, high: float) -> int:
        if not values:
            return 0
        return sum(
            1
            for v in values
            if low <= v < high or (v == high and high == max(values))
        )

    counts = [count_bin(lo, hi) for lo, hi in bins]
    max_c = max(counts) if counts else 1
    # Blank axes still need a y-scale so students can sketch frequencies.
    y_max = max(max_c, 1) if not blank else max(len(values) if values else 1, 4)
    pad_l, pad_r, pad_t, pad_b = 36, 16, 28, 36
    chart_w = width - pad_l - pad_r
    chart_h = height - pad_t - pad_b
    bar_w = chart_w / max(len(bins), 1)
    axis_y = pad_t + chart_h
    parts: list[str] = [
        f'<text x="{width // 2}" y="18" text-anchor="middle" font-size="13" '
        f'fill="#374151" font-family="system-ui,sans-serif">{escape(title)}</text>',
        # x-axis
        f'<line x1="{pad_l}" y1="{axis_y}" x2="{width - pad_r}" '
        f'y2="{axis_y}" stroke="#1f2937" stroke-width="1.5"/>',
        # y-axis
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{axis_y}" '
        f'stroke="#1f2937" stroke-width="1.5"/>',
    ]
    # Light y-tick marks for blank workspace / completed plot scale.
    for tick in range(0, int(y_max) + 1):
        if y_max > 8 and tick % 2 != 0 and tick != 0:
            continue
        ty = axis_y - (tick / y_max) * (chart_h - 4)
        parts.append(
            f'<line x1="{pad_l - 4}" y1="{ty:.1f}" x2="{pad_l}" y2="{ty:.1f}" '
            f'stroke="#1f2937" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{pad_l - 8}" y="{ty + 3:.1f}" text-anchor="end" font-size="9" '
            f'fill="#4b5563" font-family="system-ui,sans-serif">{tick}</text>'
        )

    for i, ((lo, hi), c) in enumerate(zip(bins, counts)):
        x = pad_l + i * bar_w + 2
        if not blank and c > 0:
            bh = (c / max(y_max, 1)) * (chart_h - 4)
            y = axis_y - bh
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(bar_w - 4, 2):.1f}" height="{bh:.1f}" '
                f'fill="#93c5fd" stroke="#2563eb" stroke-width="1"/>'
            )
        parts.append(
            f'<text x="{x + bar_w / 2 - 2:.1f}" y="{axis_y + 14}" text-anchor="middle" '
            f'font-size="9" fill="#4b5563" font-family="system-ui,sans-serif">'
            f"{int(lo)}-{int(hi)}</text>"
        )
    return _svg_wrap("".join(parts), width=width, height=height)


def box_plot_svg(
    summary: dict[str, float],
    *,
    title: str = "Box plot",
    width: int = 360,
    height: int = 140,
) -> str:
    """Render a horizontal box-and-whisker plot from a five-number summary."""
    keys = ("min", "q1", "median", "q3", "max")
    if not all(k in summary for k in keys):
        return _svg_wrap("", width=width, height=height)
    lo, hi = float(summary["min"]), float(summary["max"])
    span = max(hi - lo, 1e-6)
    pad_l, pad_r = 40, 40
    usable = width - pad_l - pad_r
    mid_y = height // 2 + 8

    def x_of(v: float) -> float:
        return pad_l + ((v - lo) / span) * usable

    xs = {k: x_of(float(summary[k])) for k in keys}
    parts: list[str] = [
        f'<text x="{width // 2}" y="18" text-anchor="middle" font-size="13" '
        f'fill="#374151" font-family="system-ui,sans-serif">{escape(title)}</text>',
        # whiskers
        f'<line x1="{xs["min"]:.1f}" y1="{mid_y}" x2="{xs["q1"]:.1f}" y2="{mid_y}" '
        f'stroke="#1f2937" stroke-width="1.5"/>',
        f'<line x1="{xs["q3"]:.1f}" y1="{mid_y}" x2="{xs["max"]:.1f}" y2="{mid_y}" '
        f'stroke="#1f2937" stroke-width="1.5"/>',
        f'<line x1="{xs["min"]:.1f}" y1="{mid_y - 12}" x2="{xs["min"]:.1f}" y2="{mid_y + 12}" '
        f'stroke="#1f2937" stroke-width="1.5"/>',
        f'<line x1="{xs["max"]:.1f}" y1="{mid_y - 12}" x2="{xs["max"]:.1f}" y2="{mid_y + 12}" '
        f'stroke="#1f2937" stroke-width="1.5"/>',
        # box
        f'<rect x="{xs["q1"]:.1f}" y="{mid_y - 18}" width="{max(xs["q3"] - xs["q1"], 2):.1f}" '
        f'height="36" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>',
        # median
        f'<line x1="{xs["median"]:.1f}" y1="{mid_y - 18}" x2="{xs["median"]:.1f}" y2="{mid_y + 18}" '
        f'stroke="#1e40af" stroke-width="2"/>',
    ]
    for k, label_y in (("min", mid_y + 28), ("median", mid_y - 28), ("max", mid_y + 28)):
        parts.append(
            f'<text x="{xs[k]:.1f}" y="{label_y}" text-anchor="middle" font-size="10" '
            f'fill="#4b5563" font-family="system-ui,sans-serif">'
            f'{escape(str(int(summary[k]) if summary[k] == int(summary[k]) else summary[k]))}</text>'
        )
    return _svg_wrap("".join(parts), width=width, height=height)
