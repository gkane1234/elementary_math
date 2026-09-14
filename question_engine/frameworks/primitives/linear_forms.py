"""Slope + writing linear forms — shared affine line helper (not 1-var solve)."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import num_latex, sample_integerish
from question_engine.frameworks.primitives.registry import PRIM_EQUATIONS, PrimitiveContext
from question_engine.frameworks.primitives.skeleton_difficulty import SkeletonDifficultyBands

LINEAR_FORMS_SETTINGS_SCHEMA: dict[str, Any] = {
    "slope_mode": {
        "type": "enum",
        "values": ["auto", "from_points", "from_equation"],
        "default": "auto",
    },
    "writing_mode": {
        "type": "enum",
        "values": ["auto", "slope_intercept", "point_slope", "standard", "from_points"],
        "default": "auto",
    },
    "more_on_slope_mode": {
        "type": "enum",
        "values": ["auto", "parallel", "perpendicular", "relationship", "write_parallel"],
        "default": "auto",
    },
}

_SLOPE_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("from_equation", 2.0, ("structure",)),
    DifficultyFactor("negative_slope", 1.0, ("structure",)),
    DifficultyFactor("fraction_slope", 2.5, ("structure",)),
)

_WRITE_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("point_slope", 1.5, ("structure",)),
    DifficultyFactor("standard", 2.0, ("structure",)),
    DifficultyFactor("from_two_points", 2.5, ("structure",)),
)


@dataclass(frozen=True)
class LineCoeffs:
    """y = m x + b  (or Ax + By = C when in standard)."""

    m: Fraction
    b: Fraction
    a_std: Fraction = Fraction(0)  # A in Ax+By=C
    b_std: Fraction = Fraction(1)
    c_std: Fraction = Fraction(0)


@dataclass(frozen=True)
class SlopeQuestion:
    latex: str
    text: str
    answer_latex: str
    slope: Fraction
    mode: str
    upgrades: tuple[str, ...]
    effective_d: float
    line: LineCoeffs | None = None
    points: tuple[tuple[int, int], tuple[int, int]] | None = None
    equation_form: str = ""


@dataclass(frozen=True)
class WritingLinearQuestion:
    latex: str
    text: str
    answer_latex: str
    mode: str
    line: LineCoeffs
    upgrades: tuple[str, ...]
    effective_d: float


def sample_line_coeffs(ctx: PrimitiveContext, *, allow_frac_m: bool = False) -> LineCoeffs:
    """Shared sampler for graphing / systems / writing."""
    if allow_frac_m:
        num = int(sample_integerish(ctx, exclude_zero=True).value)
        den = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value)) or 2
        if den == 1 and ctx.rng.random() < 0.5:
            den = 2
        m = Fraction(num, den)
    else:
        m = Fraction(sample_integerish(ctx, exclude_zero=True).value)
    b = Fraction(sample_integerish(ctx, exclude_zero=False).value)
    return LineCoeffs(m=m, b=b)


def slope_intercept_latex(m: Fraction, b: Fraction) -> str:
    if m == 0:
        return f"y = {num_latex(b)}"
    if m == 1:
        left = "y = x"
    elif m == -1:
        left = "y = -x"
    else:
        left = f"y = {num_latex(m)}x"
    if b == 0:
        return left
    if b > 0:
        return f"{left} + {num_latex(b)}"
    return f"{left} - {num_latex(abs(b))}"


def point_slope_latex(m: Fraction, x1: int, y1: int) -> str:
    m_l = num_latex(m)
    x_part = f"x - {x1}" if x1 >= 0 else f"x + {abs(x1)}"
    if y1 == 0:
        return f"y = {m_l}({x_part})" if m not in {1, -1} else (
            f"y = {x_part}" if m == 1 else f"y = -({x_part})"
        )
    if y1 > 0:
        return f"y - {y1} = {m_l}({x_part})"
    return f"y + {abs(y1)} = {m_l}({x_part})"


def standard_form_latex(a: Fraction, b: Fraction, c: Fraction) -> str:
    # Ax + By = C
    def term(coef: Fraction, var: str) -> str:
        if coef == 0:
            return ""
        if coef == 1:
            return var
        if coef == -1:
            return f"-{var}"
        return f"{num_latex(coef)}{var}"

    left_x = term(a, "x")
    left_y = term(b, "y")
    if left_x and left_y:
        if b > 0:
            left = f"{left_x} + {left_y}"
        else:
            left = f"{left_x} - {term(abs(b), 'y')}"
    else:
        left = left_x or left_y or "0"
    return f"{left} = {num_latex(c)}"


def sample_slope(ctx: PrimitiveContext) -> SlopeQuestion:
    eff = ctx.effective_d(PRIM_EQUATIONS)
    purchased, _, _ = select_upgrades(_SLOPE_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    settings = {
        **dict(getattr(ctx, "settings", None) or {}),
        **ctx.settings_for(PRIM_EQUATIONS),
    }
    force = str(settings.get("slope_mode", "auto")).strip().lower()
    if bool(settings.get("from_equation")):
        force = "from_equation"
    ask = str(settings.get("ask_mode", "")).strip().lower()
    if ask in {"from_points", "from_equation"}:
        force = ask
    eq_form = str(settings.get("equation_form", "")).strip().lower()

    for _ in range(12):
        try:
            return _build_slope(ctx, ids, eff, force, eq_form)
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            drop = max(ids, key=lambda i: next(f.cost for f in _SLOPE_UPGRADES if f.id == i))
            ids.remove(drop)
            ctx.note_degraded(drop)
    return _build_slope(ctx, set(), eff, force, eq_form)


def sample_writing_linear(ctx: PrimitiveContext) -> WritingLinearQuestion:
    eff = ctx.effective_d(PRIM_EQUATIONS)
    purchased, _, _ = select_upgrades(_WRITE_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    settings = ctx.settings_for(PRIM_EQUATIONS)
    force = str(settings.get("writing_mode", "auto")).strip().lower()

    for _ in range(12):
        try:
            return _build_write(ctx, ids, eff, force)
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            drop = max(ids, key=lambda i: next(f.cost for f in _WRITE_UPGRADES if f.id == i))
            ids.remove(drop)
            ctx.note_degraded(drop)
    return _build_write(ctx, set(), eff, force)


def _build_slope(
    ctx: PrimitiveContext, ids: set[str], eff: float, force: str, eq_form: str = ""
) -> SlopeQuestion:
    allow_frac = "fraction_slope" in ids
    if force == "from_equation" or (force == "auto" and "from_equation" in ids):
        line = sample_line_coeffs(ctx, allow_frac_m=allow_frac)
        if "negative_slope" in ids and line.m > 0:
            line = LineCoeffs(m=-line.m, b=line.b)
        form = eq_form or "slope_intercept"
        if form == "point_slope":
            x1 = int(sample_integerish(ctx, exclude_zero=False).value)
            y1 = int(line.m * x1 + line.b)
            eq = point_slope_latex(line.m, x1, y1)
        elif form == "standard":
            den = line.m.denominator
            a = line.m.numerator
            bb = -den
            c = -line.b * den
            if a < 0:
                a, bb, c = -a, -bb, -c
            eq = standard_form_latex(Fraction(a), Fraction(bb), Fraction(c))
        else:
            form = "slope_intercept"
            eq = slope_intercept_latex(line.m, line.b)
        return SlopeQuestion(
            latex=f"\\text{{Find the slope of the line }} {eq}.",
            text=f"Find the slope of the line {eq}.",
            answer_latex=num_latex(line.m),
            slope=line.m,
            mode="from_equation",
            upgrades=tuple(sorted(ids)),
            effective_d=eff,
            line=line,
            equation_form=form,
        )

    # from points
    x1 = int(sample_integerish(ctx, exclude_zero=False).value)
    y1 = int(sample_integerish(ctx, exclude_zero=False).value)
    dx = abs(int(sample_integerish(ctx, exclude_zero=True).value)) or 1
    if allow_frac:
        dy = int(sample_integerish(ctx, exclude_zero=True).value)
    else:
        m_int = int(sample_integerish(ctx, exclude_zero=True).value)
        dy = m_int * dx
    if "negative_slope" in ids and dy > 0:
        dy = -dy
    x2, y2 = x1 + dx, y1 + dy
    slope = Fraction(dy, dx)
    return SlopeQuestion(
        latex=(
            f"\\text{{Find the slope of the line through }} "
            f"({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        ),
        text=f"Find the slope of the line through ({x1}, {y1}) and ({x2}, {y2}).",
        answer_latex=num_latex(slope),
        slope=slope,
        mode="from_points",
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
        points=((x1, y1), (x2, y2)),
        line=LineCoeffs(m=slope, b=Fraction(y1) - slope * x1),
    )


def _build_write(
    ctx: PrimitiveContext, ids: set[str], eff: float, force: str
) -> WritingLinearQuestion:
    line = sample_line_coeffs(ctx, allow_frac_m=False)
    mode: str

    if force in {"point_slope", "standard", "slope_intercept", "from_points"}:
        mode = force
    elif "from_two_points" in ids:
        mode = "from_points"
    elif "standard" in ids:
        mode = "standard"
    elif "point_slope" in ids:
        mode = "point_slope"
    else:
        mode = "slope_intercept"

    if mode == "from_points":
        x1 = int(sample_integerish(ctx, exclude_zero=False).value)
        y1 = int(line.m * x1 + line.b)
        x2 = x1 + (2 if ctx.rng.random() < 0.5 else 3)
        y2 = int(line.m * x2 + line.b)
        latex = (
            f"\\text{{Write an equation of the line through }} "
            f"({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        )
        text = f"Write an equation of the line through ({x1}, {y1}) and ({x2}, {y2})."
        ans = slope_intercept_latex(line.m, line.b)
    elif mode == "point_slope":
        x1 = int(sample_integerish(ctx, exclude_zero=False).value)
        y1 = int(line.m * x1 + line.b)
        latex = (
            f"\\text{{Write the point-slope equation of the line with slope }} "
            f"{num_latex(line.m)} \\text{{ through }} ({x1}, {y1})."
        )
        text = f"Write point-slope form: slope {line.m} through ({x1}, {y1})."
        ans = point_slope_latex(line.m, x1, y1)
    elif mode == "standard":
        # Convert y = mx + b → m x - y = -b  (or clear fractions)
        a = line.m.numerator
        # mx - y = -b → multiply by den
        den = line.m.denominator
        a = line.m.numerator
        bb = -den
        c = -line.b * den
        # Prefer positive A
        if a < 0:
            a, bb, c = -a, -bb, -c
        line = LineCoeffs(m=line.m, b=line.b, a_std=Fraction(a), b_std=Fraction(bb), c_std=Fraction(c))
        latex = (
            f"\\text{{Write }} {slope_intercept_latex(line.m, line.b)} "
            f"\\text{{ in standard form }} Ax + By = C."
        )
        text = f"Write {slope_intercept_latex(line.m, line.b)} in standard form."
        ans = standard_form_latex(line.a_std, line.b_std, line.c_std)
    else:
        m = line.m
        b = line.b
        x1 = int(sample_integerish(ctx, exclude_zero=False).value)
        y1 = int(m * x1 + b)
        latex = (
            f"\\text{{Write the slope-intercept equation of the line with slope }} "
            f"{num_latex(m)} \\text{{ and }} y\\text{{-intercept }} {num_latex(b)}."
        )
        text = f"Write slope-intercept: m={m}, b={b}."
        ans = slope_intercept_latex(m, b)

    return WritingLinearQuestion(
        latex=latex,
        text=text,
        answer_latex=ans,
        mode=mode,
        line=line,
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
    )


def sample_graphable_line(ctx: PrimitiveContext) -> LineCoeffs:
    """Line for graphing leaves — D=0 through origin like old y=x / y=3x."""
    bands = SkeletonDifficultyBands.from_d(ctx.effective_d(PRIM_EQUATIONS))
    nt, ft = bands.numeric_tier, bands.format_tier
    if ft == 0 and nt == 0:
        m = Fraction(int(ctx.rng.choice([1, 2, 3, -1, -2])))
        return LineCoeffs(m=m, b=Fraction(0))
    m = Fraction(int(ctx.rng.choice([-3, -2, -1, 1, 2, 3, 4][: 4 + min(nt, 3)])))
    if ft == 0:
        b = Fraction(0) if ctx.rng.random() < 0.45 else Fraction(
            int(ctx.rng.randint(-3 - nt, 3 + nt))
        )
    else:
        b = Fraction(int(ctx.rng.randint(-4 - nt, 4 + nt)))
    if ft >= 2 and ctx.rng.random() < 0.25:
        # Horizontal unlock (OpenStax EA §4.2).
        return LineCoeffs(m=Fraction(0), b=b if b != 0 else Fraction(2))
    return LineCoeffs(m=m, b=b)


def graphable_line_latex(line: LineCoeffs) -> str:
    if line.b_std == 0 and line.a_std != 0:
        return f"x = {num_latex(line.c_std)}"
    return slope_intercept_latex(line.m, line.b)


def sample_more_on_slope(ctx: PrimitiveContext) -> SlopeQuestion:
    """Parallel / perpendicular (OpenStax EA §4.6) — not a slope-from-points clone."""
    eff = ctx.effective_d(PRIM_EQUATIONS)
    bands = SkeletonDifficultyBands.from_d(eff)
    nt, ft = bands.numeric_tier, bands.format_tier
    settings = ctx.settings_for(PRIM_EQUATIONS)
    force = str(settings.get("more_on_slope_mode", "auto")).strip().lower()
    rng = ctx.rng

    mag = 1 + nt
    m = Fraction(int(rng.choice([n for n in range(-mag - 2, mag + 3) if n not in (0,)])))
    if nt == 0:
        m = Fraction(int(rng.choice([1, 2, 3, -1, -2, -3])))

    if force == "auto":
        if ft == 0:
            mode = "parallel" if rng.random() < 0.65 else "relationship"
        elif ft == 1:
            mode = rng.choice(["perpendicular", "relationship", "parallel"])
        else:
            mode = rng.choice(["write_parallel", "write_perpendicular", "perpendicular"])
    else:
        mode = force

    if mode == "parallel":
        latex = (
            f"\\text{{A line has slope }} {num_latex(m)}. "
            f"\\text{{ What is the slope of a line parallel to it?}}"
        )
        text = f"A line has slope {m}. What is the slope of a line parallel to it?"
        ans = num_latex(m)
        upgrades = ("parallel",)
    elif mode == "perpendicular":
        perp = Fraction(-1, m)
        latex = (
            f"\\text{{A line has slope }} {num_latex(m)}. "
            f"\\text{{ What is the slope of a line perpendicular to it?}}"
        )
        text = f"A line has slope {m}. What is the slope of a line perpendicular to it?"
        ans = num_latex(perp)
        upgrades = ("perpendicular",)
    elif mode in {"write_parallel", "write_perpendicular"}:
        x1 = int(rng.randint(-4 - nt, 4 + nt))
        y1 = int(rng.randint(-4 - nt, 4 + nt))
        given = slope_intercept_latex(m, Fraction(int(rng.randint(-3, 3))))
        use_perp = mode == "write_perpendicular"
        slope_out = Fraction(-1, m) if use_perp else m
        b_out = Fraction(y1) - slope_out * x1
        word = "perpendicular" if use_perp else "parallel"
        latex = (
            f"\\text{{Write the slope-intercept equation of the line }} {word} "
            f"\\text{{ to }} {given} \\text{{ that passes through }} ({x1}, {y1})."
        )
        text = (
            f"Write the line {word} to {given} through ({x1}, {y1})."
        )
        ans = slope_intercept_latex(slope_out, b_out)
        upgrades = ("write_parallel",) if not use_perp else ("write_perpendicular",)
        m = slope_out
    else:
        # relationship: parallel / perpendicular / neither (D=0 biases parallel).
        kind = "parallel"
        if ft == 0:
            kind = "parallel"
        else:
            kind = rng.choice(["parallel", "perpendicular", "neither"])
        if kind == "parallel":
            m2 = m
        elif kind == "perpendicular":
            m2 = Fraction(-1, m)
        else:
            m2 = m + Fraction(int(rng.choice([-2, -1, 1, 2])))
            if m2 == 0:
                m2 = m + Fraction(1)
            if m2 == Fraction(-1, m):
                m2 = m + Fraction(2)
        latex = (
            f"\\text{{Two lines have slopes }} {num_latex(m)} \\text{{ and }} "
            f"{num_latex(m2)}. \\text{{ Are the lines parallel, perpendicular, or neither?}}"
        )
        text = (
            f"Two lines have slopes {m} and {m2}. "
            "Are they parallel, perpendicular, or neither?"
        )
        ans = kind
        upgrades = ("relationship", kind)

    return SlopeQuestion(
        latex=latex,
        text=text,
        answer_latex=ans,
        slope=m,
        mode=mode,
        upgrades=upgrades,
        effective_d=eff,
        line=LineCoeffs(m=m, b=Fraction(0)),
    )
