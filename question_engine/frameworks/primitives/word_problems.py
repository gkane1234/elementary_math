"""Word-problem wrappers that call primitive equation / system samplers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from question_engine.frameworks.primitives.equations import sample_linear_equation
from question_engine.frameworks.primitives.inequalities import sample_linear_inequality
from question_engine.frameworks.primitives.proportions import sample_proportion
from question_engine.frameworks.primitives.registry import PrimitiveContext
from question_engine.frameworks.primitives.systems import sample_linear_system

WPKind = Literal[
    "one_step",
    "two_step",
    "mixture",
    "distance",
    "work",
    "age",
    "coin",
    "consecutive",
    "percent",
    "proportion",
    "inequality",
    "systems",
]


@dataclass(frozen=True)
class WordProblemItem:
    latex: str
    text: str
    answer_latex: str
    kind: str
    equation_latex: str
    upgrades: tuple[str, ...]
    effective_d: float


_NAMES = ("Alex", "Jordan", "Sam", "Riley", "Casey", "Taylor")


def sample_word_problem(ctx: PrimitiveContext, kind: WPKind) -> WordProblemItem:
    if kind == "systems":
        return _wp_systems(ctx)
    if kind == "proportion":
        return _wp_proportion(ctx)
    if kind == "inequality":
        return _wp_inequality(ctx)
    if kind in {"one_step", "two_step"}:
        return _wp_steps(ctx, kind)
    return _wp_story_equation(ctx, kind)


def _wp_steps(ctx: PrimitiveContext, kind: WPKind) -> WordProblemItem:
    force = "one" if kind == "one_step" else "two"
    eq = sample_linear_equation(ctx, force_steps=force)  # type: ignore[arg-type]
    name = ctx.rng.choice(_NAMES)
    if force == "one":
        story = (
            f"{name} thinks of a number. After a one-step change, "
            f"the equation is ${eq.latex}$. What was the number?"
        )
    else:
        story = (
            f"{name} starts with a number and applies two operations, "
            f"giving ${eq.latex}$. What was the starting number?"
        )
    return WordProblemItem(
        latex=f"\\text{{{story}}}",
        text=story.replace("$", ""),
        answer_latex=f"{eq.var_latex} = {eq.solution_latex}",
        kind=kind,
        equation_latex=eq.latex,
        upgrades=eq.upgrades,
        effective_d=eq.effective_d,
    )


def _wp_story_equation(ctx: PrimitiveContext, kind: WPKind) -> WordProblemItem:
    eq = sample_linear_equation(ctx, force_steps="two")
    name = ctx.rng.choice(_NAMES)
    templates: dict[str, tuple[str, str]] = {
        "mixture": (
            f"{name} mixes two solutions. The amounts satisfy ${eq.latex}$. "
            f"Find ${eq.var_latex}$.",
            f"{name} mixes two solutions. The amounts satisfy {eq.text}. Find {eq.var_name}.",
        ),
        "distance": (
            f"{name} travels so that distance, rate, and time give ${eq.latex}$. "
            f"Find ${eq.var_latex}$.",
            f"{name} travels so that DRT gives {eq.text}. Find {eq.var_name}.",
        ),
        "work": (
            f"Two workers' rates combine to ${eq.latex}$. Find ${eq.var_latex}$.",
            f"Two workers' rates combine to {eq.text}. Find {eq.var_name}.",
        ),
        "age": (
            f"Ages of {name} and a sibling satisfy ${eq.latex}$. Find ${eq.var_latex}$.",
            f"Ages satisfy {eq.text}. Find {eq.var_name}.",
        ),
        "coin": (
            f"A coin collection is worth amounts that satisfy ${eq.latex}$. "
            f"Find ${eq.var_latex}$.",
            f"Coins satisfy {eq.text}. Find {eq.var_name}.",
        ),
        "consecutive": (
            f"Consecutive integers satisfy ${eq.latex}$. Find ${eq.var_latex}$.",
            f"Consecutive integers satisfy {eq.text}. Find {eq.var_name}.",
        ),
        "percent": (
            f"A percent problem reduces to ${eq.latex}$. Find ${eq.var_latex}$.",
            f"A percent problem reduces to {eq.text}. Find {eq.var_name}.",
        ),
    }
    latex, text = templates.get(kind, templates["mixture"])
    return WordProblemItem(
        latex=f"\\text{{{latex}}}" if not latex.startswith("\\") else latex,
        text=text,
        answer_latex=f"{eq.var_latex} = {eq.solution_latex}",
        kind=kind,
        equation_latex=eq.latex,
        upgrades=eq.upgrades,
        effective_d=eq.effective_d,
    )


def _wp_proportion(ctx: PrimitiveContext) -> WordProblemItem:
    prop = sample_proportion(ctx)
    name = ctx.rng.choice(_NAMES)
    story = (
        f"{name} uses a proportion ${prop.latex}$ to scale a recipe. "
        f"Find ${prop.var_latex}$."
    )
    return WordProblemItem(
        latex=f"\\text{{{name} uses a proportion }} {prop.latex} "
        f"\\text{{ to scale a recipe. Find }} {prop.var_latex}.",
        text=story.replace("$", ""),
        answer_latex=prop.solution_latex,
        kind="proportion",
        equation_latex=prop.latex,
        upgrades=prop.upgrades,
        effective_d=prop.effective_d,
    )


def _wp_inequality(ctx: PrimitiveContext) -> WordProblemItem:
    ineq = sample_linear_inequality(ctx, force_steps="two")
    name = ctx.rng.choice(_NAMES)
    return WordProblemItem(
        latex=(
            f"\\text{{{name} needs a quantity satisfying }} {ineq.latex}"
            f"\\text{{. Solve.}}"
        ),
        text=f"{name} needs a quantity satisfying {ineq.text}. Solve.",
        answer_latex=ineq.solution_latex,
        kind="inequality",
        equation_latex=ineq.latex,
        upgrades=ineq.upgrades,
        effective_d=ineq.effective_d,
    )


def _wp_systems(ctx: PrimitiveContext) -> WordProblemItem:
    sys = sample_linear_system(ctx, method="elimination")
    name = ctx.rng.choice(_NAMES)
    return WordProblemItem(
        latex=(
            f"\\text{{{name} buys two items. The costs satisfy }} "
            f"{sys.latex}"
        ),
        text=f"{name} buys two items. The costs satisfy {sys.text}.",
        answer_latex=sys.solution_latex,
        kind="systems",
        equation_latex=sys.latex,
        upgrades=sys.upgrades,
        effective_d=sys.effective_d,
    )
