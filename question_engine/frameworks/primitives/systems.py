"""2×2 linear systems — elimination / substitution / graphing metadata."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.primitives._algebra_render import num_latex
from question_engine.frameworks.primitives.linear_forms import LineCoeffs, slope_intercept_latex
from question_engine.frameworks.primitives.registry import PRIM_EQUATIONS, PrimitiveContext
from question_engine.frameworks.primitives.skeleton_difficulty import SkeletonDifficultyBands

SYSTEMS_SETTINGS_SCHEMA: dict[str, Any] = {
    "method": {
        "type": "enum",
        "values": ["auto", "elimination", "substitution", "graphing"],
        "default": "auto",
    },
    "solution_type": {
        "type": "enum",
        "values": ["auto", "unique", "none", "infinite"],
        "default": "auto",
    },
}

SolutionType = Literal["unique", "none", "infinite"]
Method = Literal["elimination", "substitution", "graphing"]


@dataclass(frozen=True)
class LinearSystem:
    latex: str
    text: str
    solution_latex: str
    method: Method
    solution_type: SolutionType
    x: Fraction
    y: Fraction
    line1: LineCoeffs
    line2: LineCoeffs
    upgrades: tuple[str, ...]
    effective_d: float


def sample_linear_system(
    ctx: PrimitiveContext,
    *,
    method: Method | None = None,
) -> LinearSystem:
    ctx.policy.assert_degree(1, where="systems")
    eff = ctx.effective_d(PRIM_EQUATIONS)
    bands = SkeletonDifficultyBands.from_d(eff)
    settings = ctx.settings_for(PRIM_EQUATIONS)
    force_method = method or str(settings.get("method", "auto")).strip().lower()
    force_sol = str(settings.get("solution_type", "auto")).strip().lower()

    if force_method not in {"elimination", "substitution", "graphing"}:
        force_method = ctx.rng.choice(["elimination", "substitution", "graphing"])

    return _build(ctx, bands, eff, force_method, force_sol)  # type: ignore[arg-type]


def _eq_std(a: int, b: int, c: int) -> str:
    def t(coef: int, var: str) -> str:
        if coef == 0:
            return ""
        if coef == 1:
            return var
        if coef == -1:
            return f"-{var}"
        return f"{coef}{var}"

    xs = t(a, "x")
    ys = t(b, "y")
    if xs and ys:
        left = f"{xs} + {ys}" if b > 0 else f"{xs} - {t(abs(b), 'y')}"
    else:
        left = xs or ys or "0"
    return f"{left} = {c}"


def _to_line(a: int, b: int, c: int) -> LineCoeffs:
    if b == 0:
        return LineCoeffs(m=Fraction(0), b=Fraction(c, a) if a else Fraction(0))
    return LineCoeffs(m=Fraction(-a, b), b=Fraction(c, b))


def _span(nt: int) -> int:
    return 3 + nt


def _pick_sol_type(
    method: Method, bands: SkeletonDifficultyBands, force_sol: str, rng
) -> SolutionType:
    if force_sol in {"unique", "none", "infinite"}:
        return force_sol  # type: ignore[return-value]
    # Graphing: unique at D=0; parallel / no-solution from D≈8 (old path).
    if method == "graphing" and bands.numeric_tier >= 2 and rng.random() < 0.55:
        return "none"
    if method == "graphing" and bands.format_tier >= 2 and rng.random() < 0.25:
        return "infinite"
    # Elimination: specials only after format unlock (OpenStax later examples).
    if method == "elimination" and bands.format_tier >= 2:
        r = rng.random()
        if r < 0.15:
            return "none"
        if r < 0.25:
            return "infinite"
    return "unique"


def _elim_unique_coeffs(
    ctx: PrimitiveContext, nt: int, ft: int, x: Fraction, y: Fraction
) -> tuple[int, int, int, int, int, int]:
    """OpenStax EA §5.3: opposite at D=0; multiply one, then both."""
    rng = ctx.rng
    if ft == 0:
        # Already opposite (Ex 5.26: x+y / x−y). Small integers first.
        mag = 1 if nt == 0 else rng.randint(1, 1 + nt)
        if rng.random() < 0.5:
            a1, a2 = mag, -mag
            b1 = 1 if nt == 0 else rng.randint(1, 1 + nt)
            b2 = (b1 + 1) if nt == 0 else rng.randint(1, 2 + nt)
            if b2 == b1:
                b2 = b1 + 1
            if rng.random() < 0.5:
                b1, b2 = -b1, b2
        else:
            b1, b2 = mag, -mag
            a1 = 1 if nt == 0 else rng.randint(1, 1 + nt)
            a2 = (a1 + 1) if nt == 0 else rng.randint(1, 2 + nt)
            if a2 == a1:
                a2 = a1 + 1
    elif ft == 1:
        # Multiply one equation (Ex 5.25 / 5.27-ish): one pair not opposite yet.
        a1 = rng.randint(1, 2 + nt)
        b1 = rng.randint(1, 2 + nt)
        k = rng.randint(2, 3 + min(nt, 2))
        if rng.random() < 0.5:
            a2 = rng.randint(1, 2 + nt)
            b2 = -k * b1 if rng.random() < 0.5 else rng.randint(1, 3 + nt)
            if a1 * b2 == a2 * b1:
                b2 += 1
        else:
            a2 = -k * a1 if rng.random() < 0.5 else rng.randint(1, 3 + nt)
            b2 = rng.randint(1, 2 + nt)
            if a1 * b2 == a2 * b1:
                a2 += 1
        if rng.random() < 0.4:
            a1 = -a1
    else:
        # Multiply both (Ex 5.28): independent messy integer coeffs.
        span = _span(nt) + 2
        for _ in range(16):
            a1 = rng.randint(-span, span) or 1
            b1 = rng.randint(-span, span) or 1
            a2 = rng.randint(-span, span) or 1
            b2 = rng.randint(-span, span) or 1
            if a1 * b2 != a2 * b1 and abs(a1) != abs(a2) and abs(b1) != abs(b2):
                break
        else:
            a1, b1, a2, b2 = 3, -2, 5, -6
    c1 = int(a1 * x + b1 * y)
    c2 = int(a2 * x + b2 * y)
    return a1, b1, c1, a2, b2, c2


def _sub_unique_coeffs(
    ctx: PrimitiveContext, nt: int, x: Fraction, y: Fraction
) -> tuple[int, int, int, int, int, int, Fraction, Fraction]:
    """First equation already solved for y (old D=0: y=x+k)."""
    rng = ctx.rng
    m = Fraction(1 if nt == 0 else rng.choice([-2, -1, 1, 2, 3][: 3 + min(nt, 2)]))
    b = y - m * x
    # ax + by = c independent of y = mx + b.
    span = _span(nt)
    a2 = rng.randint(-span, span) or 2
    b2 = rng.randint(-span, span) or 1
    if nt == 0:
        a2 = rng.choice([-3, -2, 2, 3, 4])
        b2 = rng.choice([-2, -1, 1, 2])
    c2 = int(a2 * x + b2 * y)
    # Standard form of y = mx + b → mx - y = -b
    den = m.denominator
    a1 = int(m.numerator)
    b1 = -den
    c1 = int(-b * den)
    return a1, b1, c1, a2, b2, c2, m, b


def _special_parallel(ctx: PrimitiveContext, nt: int, infinite: bool):
    span = max(2, _span(nt))
    a1 = ctx.rng.randint(1, span)
    b1 = ctx.rng.randint(1, span)
    k = ctx.rng.randint(2, 3 + min(nt, 2))
    a2, b2 = k * a1, k * b1
    c1 = ctx.rng.randint(1, span)
    c2 = k * c1 if infinite else k * c1 + ctx.rng.choice([-2, -1, 1, 2])
    return a1, b1, c1, a2, b2, c2


def _build(
    ctx: PrimitiveContext,
    bands: SkeletonDifficultyBands,
    eff: float,
    method: Method,
    force_sol: str,
) -> LinearSystem:
    nt, ft = bands.numeric_tier, bands.format_tier
    sol_type = _pick_sol_type(method, bands, force_sol, ctx.rng)
    upgrades: list[str] = [sol_type, method]

    if sol_type == "unique":
        span = _span(nt)
        x = Fraction(ctx.rng.randint(-span, span))
        y = Fraction(ctx.rng.randint(-span, span))
        if method == "substitution":
            a1, b1, c1, a2, b2, c2, m, bb = _sub_unique_coeffs(ctx, nt, x, y)
            line1 = LineCoeffs(m=m, b=bb)
            line2 = _to_line(a2, b2, c2)
        elif method == "elimination":
            a1, b1, c1, a2, b2, c2 = _elim_unique_coeffs(ctx, nt, ft, x, y)
            if ft == 0:
                upgrades.append("opposite_coeffs")
            elif ft == 1:
                upgrades.append("multiply_one")
            else:
                upgrades.append("multiply_both")
            line1 = _to_line(a1, b1, c1)
            line2 = _to_line(a2, b2, c2)
        else:
            # Graphing: integer intercepts at D=0 (OpenStax EA §5.1).
            if nt == 0:
                m1 = Fraction(ctx.rng.choice([-2, -1, 1, 2]))
                m2 = Fraction(ctx.rng.choice([-3, -2, -1, 1, 2, 3]))
                if m2 == m1:
                    m2 = -m1 if m1 != 0 else Fraction(2)
                b1 = y - m1 * x
                b2 = y - m2 * x
                # Prefer integer intercepts.
                if b1.denominator != 1 or b2.denominator != 1:
                    x = Fraction(ctx.rng.choice([-2, -1, 0, 1, 2]))
                    y = Fraction(ctx.rng.choice([-2, -1, 0, 1, 2]))
                    b1 = y - m1 * x
                    b2 = y - m2 * x
                line1 = LineCoeffs(m=m1, b=b1)
                line2 = LineCoeffs(m=m2, b=b2)
                a1, b1c, c1 = int(m1.numerator), -int(m1.denominator), int(-b1 * m1.denominator)
                a2, b2c, c2 = int(m2.numerator), -int(m2.denominator), int(-b2 * m2.denominator)
                b1, b2 = b1c, b2c
            else:
                a1 = ctx.rng.randint(-_span(nt), _span(nt)) or 1
                b1c = ctx.rng.randint(-_span(nt), _span(nt)) or 1
                a2 = ctx.rng.randint(-_span(nt), _span(nt)) or 1
                b2c = ctx.rng.randint(-_span(nt), _span(nt)) or 1
                if a1 * b2c == a2 * b1c:
                    b2c = b1c + (1 if b1c >= 0 else -1)
                c1 = int(a1 * x + b1c * y)
                c2 = int(a2 * x + b2c * y)
                b1, b2 = b1c, b2c
                line1 = _to_line(a1, b1, c1)
                line2 = _to_line(a2, b2, c2)
        ans = f"x = {num_latex(x)},\\ y = {num_latex(y)}"
    else:
        x = y = Fraction(0)
        a1, b1, c1, a2, b2, c2 = _special_parallel(
            ctx, nt, infinite=(sol_type == "infinite")
        )
        line1 = _to_line(a1, b1, c1)
        line2 = _to_line(a2, b2, c2)
        ans = (
            r"\text{infinitely many solutions}"
            if sol_type == "infinite"
            else r"\text{no solution}"
        )
        upgrades.append("special_infinite" if sol_type == "infinite" else "special_none")

    eq1 = _eq_std(a1, b1, c1)
    eq2 = _eq_std(a2, b2, c2)

    if method == "substitution" and sol_type == "unique":
        y_expr = slope_intercept_latex(line1.m, line1.b).replace("y = ", "")
        latex = f"\\begin{{cases}} y = {y_expr} \\\\ {eq2} \\end{{cases}}"
        text = f"y = {y_expr}; {eq2}"
    elif method == "graphing":
        latex = (
            f"\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}"
            f"\\quad \\text{{Solve by graphing.}}"
        )
        text = f"{eq1}; {eq2}. Solve by graphing."
    else:
        latex = f"\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}"
        text = f"{eq1}; {eq2}"

    return LinearSystem(
        latex=latex,
        text=text,
        solution_latex=ans,
        method=method,
        solution_type=sol_type,
        x=x,
        y=y,
        line1=line1,
        line2=line2,
        upgrades=tuple(sorted(set(upgrades))),
        effective_d=eff,
    )
