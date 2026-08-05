"""Word-problem wrappers that call primitive equation / system samplers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from question_engine.frameworks.primitives.equations import sample_linear_equation
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
    shape_id: str = ""
    n_constraints: int = 0
    frame: str = ""


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
    # Narrative samplers: continuous-D upgrades + composed presentation.
    if kind == "coin":
        from question_engine.frameworks.primitives.narrative_wp import sample_coin_wp

        return sample_coin_wp(ctx)
    if kind == "age":
        from question_engine.frameworks.primitives.narrative_wp import sample_age_wp

        return sample_age_wp(ctx)
    if kind == "consecutive":
        from question_engine.frameworks.primitives.narrative_wp import sample_consecutive_wp

        return sample_consecutive_wp(ctx)
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
    """Real inequality word problems with continuous effort (not equation stubs)."""
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    d = float(ctx.topic_d)
    name = ctx.rng.choice(_NAMES)
    # Effort ladder: compare-only → one-step rearrange → two-step with awkward nums
    # → inclusive “at least/at most” with messier totals.
    if d < 5:
        # Compare: x > k style after translating words.
        k = ctx.rng.randint(3, 12)
        op = ctx.rng.choice([">", "\\ge"])
        word = "more than" if op == ">" else "at least"
        latex = (
            f"\\text{{{name} wants a score {word} }} {k}"
            f"\\text{{. Write an inequality for the score }} x\\text{{.}}"
        )
        text = f"{name} wants a score {word} {k}. Write an inequality for the score x."
        answer = f"x {op} {k}"
        upgrades: tuple[str, ...] = ("compare_only",)
        eff = d
    elif d < 12:
        # One-step: x + a ≥ b or similar.
        a = ctx.rng.randint(2, 9)
        need = ctx.rng.randint(8, 20)
        total = need + a
        latex = (
            f"\\text{{{name} already has }} {a}"
            f"\\text{{ points and needs at least }} {total}"
            f"\\text{{ points in total. What scores }} x "
            f"\\text{{ on the next round work?}}"
        )
        text = (
            f"{name} already has {a} points and needs at least {total} points in total. "
            f"What scores x on the next round work?"
        )
        answer = f"x \\ge {need}"
        upgrades = ("one_step_translate",)
        eff = d
    elif d < 18:
        # Two-step: ax + b ≤ c
        a = ctx.rng.randint(2, 5)
        b = ctx.rng.randint(1, 8)
        x_sol = ctx.rng.randint(2, 8)
        rhs = a * x_sol + b
        latex = (
            f"\\text{{{name} buys }} x \\text{{ notebooks at \\$}}{a}"
            f"\\text{{ each and a }} \\${b}"
            f"\\text{{ pen. The total must be at most \\$}}{rhs}"
            f"\\text{{. How many notebooks can }} {name}\\text{{ buy?}}"
        )
        text = (
            f"{name} buys x notebooks at ${a} each and a ${b} pen. "
            f"The total must be at most ${rhs}. How many notebooks can {name} buy?"
        )
        answer = f"x \\le {x_sol}"
        upgrades = ("two_step_story",)
        eff = d
    else:
        # Harder: larger coeffs / “fewer than” with leftover rearrange.
        a = ctx.rng.randint(3, 8)
        b = ctx.rng.randint(5, 20)
        x_sol = ctx.rng.randint(4, 12)
        rhs = a * x_sol + b
        latex = (
            f"\\text{{{name} rents a bike for \\$}}{b}"
            f"\\text{{ plus \\$}}{a}\\text{{ per hour. }} "
            f"{name}\\text{{ can spend less than \\$}}{rhs}"
            f"\\text{{. For how many hours }} x \\text{{ can }} {name}"
            f"\\text{{ ride?}}"
        )
        text = (
            f"{name} rents a bike for ${b} plus ${a} per hour. "
            f"{name} can spend less than ${rhs}. For how many hours x can {name} ride?"
        )
        answer = f"x < {x_sol}"
        upgrades = ("two_step_strict", "larger_coeffs")
        eff = d

    return WordProblemItem(
        latex=latex,
        text=text,
        answer_latex=answer,
        kind="inequality",
        equation_latex=answer,
        upgrades=upgrades,
        effective_d=eff,
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
