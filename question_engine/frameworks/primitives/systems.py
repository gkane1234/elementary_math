"""2×2 linear systems — elimination / substitution / graphing metadata."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import num_latex, sample_integerish
from question_engine.frameworks.primitives.linear_forms import LineCoeffs, slope_intercept_latex
from question_engine.frameworks.primitives.registry import PRIM_EQUATIONS, PrimitiveContext

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

_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("messy_coeffs", 2.0, ("structure",)),
    DifficultyFactor("special_none", 3.0, ("structure",)),
    DifficultyFactor("special_infinite", 3.5, ("structure",)),
)

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
    purchased, _, _ = select_upgrades(_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    settings = ctx.settings_for(PRIM_EQUATIONS)
    force_method = method or str(settings.get("method", "auto")).strip().lower()
    force_sol = str(settings.get("solution_type", "auto")).strip().lower()

    if force_method not in {"elimination", "substitution", "graphing"}:
        force_method = ctx.rng.choice(["elimination", "substitution", "graphing"])

    for _ in range(14):
        try:
            return _build(ctx, ids, eff, force_method, force_sol)  # type: ignore[arg-type]
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            drop = max(ids, key=lambda i: next(f.cost for f in _UPGRADES if f.id == i))
            ids.remove(drop)
            ctx.note_degraded(drop)
    return _build(ctx, set(), eff, force_method, "unique")  # type: ignore[arg-type]


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


def _build(
    ctx: PrimitiveContext,
    ids: set[str],
    eff: float,
    method: Method,
    force_sol: str,
) -> LinearSystem:
    messy = "messy_coeffs" in ids
    span = 6 if messy else 4

    # Solution type
    if force_sol == "none" or (force_sol == "auto" and "special_none" in ids):
        sol_type: SolutionType = "none"
    elif force_sol == "infinite" or (force_sol == "auto" and "special_infinite" in ids):
        sol_type = "infinite"
    else:
        sol_type = "unique"

    if sol_type == "unique":
        x = Fraction(ctx.rng.randint(-span, span))
        y = Fraction(ctx.rng.randint(-span, span))
        a1 = ctx.rng.randint(-span, span) or 1
        b1 = ctx.rng.randint(-span, span) or 1
        a2 = ctx.rng.randint(-span, span) or 1
        b2 = ctx.rng.randint(-span, span) or 1
        # Ensure independent
        if a1 * b2 == a2 * b1:
            b2 = b1 + (1 if b1 >= 0 else -1)
        c1 = int(a1 * x + b1 * y)
        c2 = int(a2 * x + b2 * y)
        ans = f"x = {num_latex(x)},\\ y = {num_latex(y)}"
    elif sol_type == "none":
        x = y = Fraction(0)
        a1 = ctx.rng.randint(1, span)
        b1 = ctx.rng.randint(1, span)
        k = ctx.rng.randint(2, 4)
        a2, b2 = k * a1, k * b1
        c1 = ctx.rng.randint(1, span)
        c2 = k * c1 + ctx.rng.choice([-2, -1, 1, 2])  # parallel distinct
        ans = r"\text{no solution}"
    else:
        x = y = Fraction(0)
        a1 = ctx.rng.randint(1, span)
        b1 = ctx.rng.randint(1, span)
        k = ctx.rng.randint(2, 4)
        a2, b2 = k * a1, k * b1
        c1 = ctx.rng.randint(1, span)
        c2 = k * c1
        ans = r"\text{infinitely many solutions}"

    eq1 = _eq_std(a1, b1, c1)
    eq2 = _eq_std(a2, b2, c2)
    # Slope-intercept for graphing metadata when possible
    def to_line(a: int, b: int, c: int) -> LineCoeffs:
        if b == 0:
            # vertical-ish: x = c/a — represent as huge slope sentinel via m=None not allowed
            return LineCoeffs(m=Fraction(0), b=Fraction(c, a) if a else Fraction(0))
        m = Fraction(-a, b)
        bb = Fraction(c, b)
        return LineCoeffs(m=m, b=bb)

    line1 = to_line(a1, b1, c1)
    line2 = to_line(a2, b2, c2)

    if method == "substitution" and b1 != 0:
        # Present first as y = ...
        y_expr = slope_intercept_latex(line1.m, line1.b).replace("y = ", "")
        latex = (
            f"\\begin{{cases}} y = {y_expr} \\\\ {eq2} \\end{{cases}}"
            f"\\quad \\text{{(substitution)}}"
        )
        text = f"y = {y_expr}; {eq2} (substitution)"
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
        upgrades=tuple(sorted(ids | {sol_type, method})),
        effective_d=eff,
    )
