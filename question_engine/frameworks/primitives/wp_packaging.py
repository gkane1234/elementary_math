"""Story packaging for linear / inequality / proportion word problems.

Pick a typed OpenStax story frame first, then fill slots so reverse algebra
matches. Same SolveLinear / SolveInequality species. The prompt is the story —
it does not dump ``$3x+2=17$``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.primitives._algebra_render import num_latex
from question_engine.frameworks.primitives.equation_skeleton import (
    use_solve_inequality_skeleton,
    use_solve_linear_skeleton,
)
from question_engine.frameworks.primitives.registry import PrimitiveContext
from question_engine.frameworks.primitives.skeleton_difficulty import SkeletonDifficultyBands
from question_engine.frameworks.primitives.word_problems import WPKind, WordProblemItem
from question_engine.word_problems.names import pick_name
from question_engine.word_problems.things import pick_things

FrameKind = Literal[
    "number",
    "money",
    "count",
    "compare",
    "budget",
    "rate",
    "geometry",
    "scale",
]


# OpenStax EA 2.6 d=rt vehicles (bike / drive / walk / bus / train).
_RATE_VEHICLES: tuple[tuple[str, str], ...] = (
    ("bike", "rides a bike"),
    ("car", "drives"),
    ("walk", "walks"),
    ("bus", "rides a bus"),
    ("train", "rides a train"),
)
_TICKET_THINGS = ("tickets", "notebooks", "pencils", "stickers", "markers")
_COST_ITEMS = ("pencils", "notebooks", "markers", "erasers")
_CALORIE_DRINKS = ("energy drink", "smoothie", "chocolate shake", "soda")

_INEQ_PHRASE = {
    "<": "less than",
    ">": "more than",
    "\\le": "at most",
    "\\ge": "at least",
}
_OP_TEXT = {"<": "<", ">": ">", "\\le": "<=", "\\ge": ">="}
_FEE_ITEMS = ("pen", "snack", "cover", "bag")
_DUMP_MARKERS = (
    "the equation is",
    "giving $",
    "satisfy $",
    "reduces to $",
    "uses a proportion $",
    "costs satisfy",
)


@dataclass(frozen=True)
class WpFrame:
    """Typed story frame. Reverse ops must be allowed at this species / D."""

    frame_id: str
    species: str
    ops: tuple[str, ...]
    kind: FrameKind
    min_format_tier: int = 0
    allow_neg: bool = False
    variant: str = ""


@dataclass(frozen=True)
class PackedStory:
    latex: str
    text: str
    answer_latex: str
    frame_id: str
    variant: str
    hidden_eq: str
    units: str = ""


@dataclass
class SlotEq:
    """Math stamp for a frame-filled story (SolveLinear-compatible metadata)."""

    solution: Fraction
    leading: Fraction
    transforms: tuple[str, ...]
    steps: str
    latex: str
    upgrades: tuple[str, ...]
    effective_d: float
    metadata: dict[str, Any]
    n_ops: int = 1
    op: str = "="
    relation: str = "="
    var_latex: str = "x"
    flipped: bool = False
    solution_latex: str = ""


# Catalog families (algebra1_linear_applications.json) → concrete variants.
# Distinct frame_id per OpenStax story type (not Mad-Lib name swaps).
FRAMES: tuple[WpFrame, ...] = (
    # One-step — IA §2.2 / EA §2.1–2.2 number + money + tickets.
    WpFrame("number_one_step", "one", ("add",), "number", variant="add"),
    WpFrame("number_one_step", "one", ("sub",), "number", variant="sub"),
    WpFrame("number_one_step", "one", ("mul",), "number", variant="mul"),
    WpFrame("number_one_step", "one", ("div",), "number", variant="div"),
    WpFrame("money_spent", "one", ("sub",), "money", variant="spent"),
    WpFrame("money_received", "one", ("add",), "money", variant="received"),
    WpFrame("money_shared", "one", ("mul",), "money", variant="shared"),
    WpFrame("money_donations", "one", ("mul",), "money", variant="each"),
    WpFrame("count_tickets", "one", ("mul",), "count", variant="tickets"),
    WpFrame("count_groups", "one", ("div",), "count", variant="groups"),
    # Two-step — IA §2.2 Ex 2.15 / 2.14 / 2.19; unit+fee.
    WpFrame("number_two_step", "two", ("add", "mul"), "number"),
    WpFrame("money_two_step", "two", ("add", "mul"), "money"),
    WpFrame("compare_twice", "two", ("add", "mul"), "count", variant="twice_more"),
    WpFrame("earnings_two_step", "two", ("add", "mul"), "money", variant="twice_less"),
    # Inequality — EA §2.7 translate / §3.6; IA §2.5 budget.
    WpFrame("ineq_score", "one", (), "compare", variant="score"),
    WpFrame("ineq_height", "one", (), "compare", variant="height"),
    WpFrame("ineq_checkout", "one", (), "compare", variant="checkout"),
    WpFrame("ineq_points", "one", ("add",), "compare", variant="add_points"),
    WpFrame("ineq_lost", "one", ("sub",), "compare", variant="lost_points"),
    WpFrame("ineq_tickets", "one", ("mul",), "count", variant="ineq_tickets"),
    WpFrame("ineq_budget", "two", ("add", "mul"), "budget", min_format_tier=1),
    # Proportion — EA §8.7 (unit rate, recipe, calories, dosage).
    WpFrame("prop_recipe", "proportion", (), "scale", variant="recipe"),
    WpFrame("prop_unit_rate", "proportion", (), "rate", variant="unit_rate"),
    WpFrame("prop_calories", "proportion", (), "scale", variant="calories"),
    WpFrame("prop_dosage", "proportion", (), "scale", variant="dosage"),
    # Systems applications — EA §5.4 (number, tickets, geometry, motion).
    WpFrame("sys_number", "systems", (), "number"),
    WpFrame("sys_tickets", "systems", (), "money"),
    WpFrame("sys_geometry", "systems", (), "geometry", min_format_tier=1),
    WpFrame("sys_motion", "systems", (), "rate", min_format_tier=1),
)


def use_wp_packaging(settings: dict[str, Any] | None, kind: WPKind) -> bool:
    """Live default is packaging; opt out to the old equation-dump stub."""
    s = dict(settings or {})
    if "use_wp_packaging" in s:
        return bool(s.get("use_wp_packaging"))
    if kind in {"one_step", "two_step"}:
        return use_solve_linear_skeleton(s)
    if kind == "inequality":
        return use_solve_inequality_skeleton(s)
    if kind == "proportion":
        if bool(s.get("use_sample_linear_equation")) or bool(s.get("use_legacy_equations")):
            return False
        return True
    if kind == "similar_figures":
        if bool(s.get("use_legacy_similar_figures")):
            return False
        if "use_wp_packaging" in s:
            return bool(s.get("use_wp_packaging"))
        return True
    if kind == "systems":
        if bool(s.get("use_legacy_systems")):
            return False
        if bool(s.get("use_sample_linear_equation")) or bool(s.get("use_legacy_equations")):
            return False
        return True
    return True


def sample_packaged_word_problem(ctx: PrimitiveContext, kind: WPKind) -> WordProblemItem:
    """Pick a story frame first, then fill slots whose reverse algebra matches."""
    if kind == "proportion":
        return _package_proportion(ctx)
    if kind == "similar_figures":
        return _package_similar_figures(ctx)
    if kind == "inequality":
        return _package_inequality(ctx)
    if kind == "systems":
        return _package_systems(ctx)
    return _package_equation(ctx, kind=kind)


def _to_item(
    eq: Any,
    story: PackedStory,
    *,
    kind: str,
    extra_meta: dict[str, Any] | None = None,
) -> WordProblemItem:
    packed = dict(getattr(eq, "metadata", None) or {})
    packed.update(extra_meta or {})
    packed.update(
        {
            "frame_id": story.frame_id,
            "frame_variant": story.variant,
            "units": story.units,
            "construction": "wp_packaging",
        }
    )
    return WordProblemItem(
        latex=story.latex,
        text=story.text,
        answer_latex=story.answer_latex,
        kind=kind,
        equation_latex=story.hidden_eq or getattr(eq, "latex", ""),
        upgrades=tuple(getattr(eq, "upgrades", ()) or ()),
        effective_d=float(getattr(eq, "effective_d", 0.0) or 0.0),
        shape_id=story.frame_id,
        frame=story.frame_id,
        metadata=packed,
    )


def _esc_text(s: str) -> str:
    return (
        s.replace("$", r"\$")
        .replace("%", r"\%")
        .replace("#", r"\#")
        .replace("&", r"\&")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def _ntext(n: Fraction) -> str:
    if n.denominator == 1:
        return str(n.numerator)
    if n.numerator < 0:
        return f"-{abs(n.numerator)}/{n.denominator}"
    return f"{n.numerator}/{n.denominator}"


def compose_story(*parts: Any) -> tuple[str, str]:
    """Join prose strings and ``Fraction`` math chunks into (latex, text)."""
    latex_out: list[str] = []
    text_out: list[str] = []
    buf = ""

    def flush() -> None:
        nonlocal buf
        if buf:
            latex_out.append(r"\text{" + _esc_text(buf) + "}")
            text_out.append(buf)
            buf = ""

    for p in parts:
        if isinstance(p, Fraction):
            flush()
            latex_out.append(num_latex(p))
            text_out.append(_ntext(p))
        elif isinstance(p, tuple) and len(p) == 2:
            flush()
            latex_out.append(str(p[0]))
            text_out.append(str(p[1]))
        else:
            buf += str(p)
    flush()
    return "".join(latex_out), "".join(text_out)


def _ranges(ctx: PrimitiveContext) -> tuple[int, int, int, int]:
    """(addend_hi, mul_hi, sol_hi, format_tier) from numeric-then-format bands."""
    bands = SkeletonDifficultyBands.from_d(float(ctx.topic_d))
    nt = bands.numeric_tier
    add_hi = (4, 9, 16, 28, 40)[nt]
    mul_hi = (4, 6, 8, 10, 12)[nt]
    sol_hi = (6, 9, 12, 16, 24)[nt]
    return add_hi, mul_hi, sol_hi, bands.format_tier


def _ri(ctx: PrimitiveContext, lo: int, hi: int) -> int:
    return int(ctx.rng.randint(lo, max(lo, hi)))


def _slot_eq(
    ctx: PrimitiveContext,
    *,
    s: Fraction,
    leading: Fraction,
    trans: tuple[str, ...],
    steps: str,
    rhs: Fraction,
    ineq: bool = False,
    op: str = "=",
    flipped: bool = False,
    var: str = "x",
) -> SlotEq:
    n_ops = 2 if steps == "two" else 1
    rel = op if ineq else "="
    bands = SkeletonDifficultyBands.from_d(float(ctx.topic_d))
    pattern = "SolveInequality" if ineq else "SolveLinear"
    meta = {
        "skeleton_pattern": pattern,
        "species": steps,
        "n_ops": n_ops,
        "steps": steps,
        "transforms": list(trans),
        "rhs": str(rhs),
        "leading": str(leading),
        "numeric_tier": bands.numeric_tier,
        "format_tier": bands.format_tier,
        "flipped": flipped,
        "relation": rel,
        "construction": "wp_packaging",
    }
    return SlotEq(
        solution=s,
        leading=leading,
        transforms=trans,
        steps=steps,
        latex="",
        upgrades=("one_step",) if n_ops == 1 else ("two_step",),
        effective_d=float(ctx.topic_d),
        metadata=meta,
        n_ops=n_ops,
        op=rel,
        relation=rel,
        var_latex=var,
        flipped=flipped,
        solution_latex=_answer_ineq_op(var, rel, s) if ineq else num_latex(s),
    )


def _answer_ineq_op(var: str, op: str, s: Fraction) -> str:
    return f"{var} {op} {num_latex(s)}"


def _pick_ineq_op(ctx: PrimitiveContext) -> str:
    return str(ctx.rng.choice(("<", ">", r"\le", r"\ge")))


def _frame_ids_for(
    *,
    species: str,
    format_tier: int,
    ineq: bool,
) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for fr in FRAMES:
        if fr.species != species:
            continue
        if fr.min_format_tier > format_tier:
            continue
        is_ineq = fr.frame_id.startswith("ineq")
        if ineq != is_ineq:
            continue
        if fr.frame_id not in seen:
            seen.add(fr.frame_id)
            ids.append(fr.frame_id)
    return ids


def _frames_named(fid: str) -> list[WpFrame]:
    return [f for f in FRAMES if f.frame_id == fid]


def _rotate_for_d(ctx: PrimitiveContext, items: list[str]) -> list[str]:
    """Shift a shuffled catalog so the same seed is not one frame at every D."""
    if len(items) <= 1:
        return items
    d = float(getattr(ctx, "topic_d", 0.0) or 0.0)
    rot = int(max(0.0, d) // 5) % len(items)
    if not rot:
        return items
    return items[rot:] + items[:rot]


def _try_frames(
    ctx: PrimitiveContext,
    ids: list[str],
    *,
    ineq: bool,
    skip_div: bool = False,
) -> tuple[PackedStory, SlotEq] | None:
    """Pick one frame_id uniformly, then try remaining ids if a fill fails."""
    if not ids:
        return None
    order = list(ids)
    ctx.rng.shuffle(order)
    order = _rotate_for_d(ctx, order)
    for fid in order:
        pool = _frames_named(fid)
        ctx.rng.shuffle(pool)
        for fr in pool:
            if skip_div and fr.variant == "div":
                continue
            filled = _fill_from_schema(ctx, fr, ineq=ineq)
            if filled is not None:
                return filled
    return None


def _package_equation(ctx: PrimitiveContext, *, kind: str) -> WordProblemItem:
    bands = SkeletonDifficultyBands.from_d(float(ctx.topic_d))
    species = "one" if kind == "one_step" else "two"
    ids = _frame_ids_for(species=species, format_tier=bands.format_tier, ineq=False)
    if species == "one" and bands.format_tier == 0:
        # OpenStax §2.1–2.2: add/sub/mul; x/a=b later. Groups uses div — skip at D=0.
        ids = [i for i in ids if i != "count_groups"]
    filled = _try_frames(
        ctx, ids, ineq=False, skip_div=species == "one" and bands.format_tier == 0
    )
    if filled is not None:
        story, eq = filled
        return _to_item(
            eq, story, kind=kind, extra_meta={"skeleton_pattern": "SolveLinear"}
        )
    story, eq = _fill_number_fallback_slots(ctx, ineq=False)
    return _to_item(eq, story, kind=kind, extra_meta={"skeleton_pattern": "SolveLinear"})


def _package_inequality(ctx: PrimitiveContext) -> WordProblemItem:
    bands = SkeletonDifficultyBands.from_d(float(ctx.topic_d))
    one_ids = _frame_ids_for(species="one", format_tier=bands.format_tier, ineq=True)
    budget_ids = _frame_ids_for(species="two", format_tier=bands.format_tier, ineq=True)
    one_ids = [i for i in one_ids if i != "ineq_budget"]
    # IA §2.5 budget vehicles (car / phone / tablets) should dominate high D,
    # not remain a rare extra next to one-step score/points.
    if bands.format_tier >= 1 and budget_ids:
        p_budget = 0.55 if bands.format_tier == 1 else 0.7
        ids = budget_ids if ctx.rng.random() < p_budget else one_ids
    else:
        ids = one_ids
    filled = _try_frames(ctx, ids, ineq=True)
    if filled is None and ids != one_ids:
        filled = _try_frames(ctx, one_ids, ineq=True)
    if filled is not None:
        story, eq = filled
        return _to_item(
            eq,
            story,
            kind="inequality",
            extra_meta={"skeleton_pattern": "SolveInequality"},
        )
    story, eq = _fill_number_fallback_slots(ctx, ineq=True)
    return _to_item(
        eq,
        story,
        kind="inequality",
        extra_meta={"skeleton_pattern": "SolveInequality"},
    )


def _fill_from_schema(
    ctx: PrimitiveContext,
    fr: WpFrame,
    *,
    ineq: bool,
) -> tuple[PackedStory, SlotEq] | None:
    name = pick_name(rng=ctx.rng)
    things = pick_things(1, rng=ctx.rng)[0]
    if fr.kind == "number" and fr.species == "one":
        return _fill_number_one(ctx, fr, ineq=ineq)
    if fr.kind == "number" and fr.species == "two":
        return _fill_number_two(ctx, fr, ineq=ineq)
    if fr.frame_id == "money_spent":
        return _fill_money_spent(ctx, name)
    if fr.frame_id == "money_received":
        return _fill_money_received(ctx, name)
    if fr.frame_id == "money_donations":
        return _fill_money_donations(ctx, name)
    if fr.frame_id == "money_shared":
        return _fill_money_shared(ctx, name)
    if fr.frame_id == "count_tickets":
        things = ctx.rng.choice(_TICKET_THINGS)
        return _fill_tickets(ctx, name, things, ineq=False)
    if fr.frame_id == "count_groups":
        return _fill_groups(ctx, name, things)
    if fr.frame_id == "money_two_step":
        return _fill_money_two(ctx, name, things)
    if fr.frame_id == "compare_twice":
        return _fill_compare_twice(ctx, name, things)
    if fr.frame_id == "earnings_two_step":
        return _fill_earnings_two(ctx, name)
    if fr.frame_id == "ineq_score":
        return _fill_ineq_compare(ctx, name)
    if fr.frame_id == "ineq_height":
        return _fill_ineq_height(ctx)
    if fr.frame_id == "ineq_checkout":
        return _fill_ineq_checkout(ctx)
    if fr.frame_id == "ineq_points":
        return _fill_ineq_points(ctx, name)
    if fr.frame_id == "ineq_lost":
        return _fill_ineq_lost(ctx, name)
    if fr.frame_id == "ineq_tickets":
        things = ctx.rng.choice(_TICKET_THINGS)
        return _fill_tickets(ctx, name, things, ineq=True)
    if fr.kind == "budget":
        return _fill_ineq_budget(ctx, name, things)
    return None


def _answer_eq(s: Fraction, *, units: str = "") -> str:
    body = num_latex(s)
    if units == "$":
        if s < 0:
            return f"-\\${num_latex(abs(s))}"
        return f"\\${body}"
    if units:
        return f"{body}\\text{{ {units}}}"
    return body


def _answer_ineq(eq: Any, s: Fraction) -> str:
    op = str(getattr(eq, "op", None) or getattr(eq, "relation", ">") or ">")
    var = str(getattr(eq, "var_latex", None) or "x")
    return f"{var} {op} {num_latex(s)}"


def _hidden_one(eq: Any, a: Fraction, rhs: Fraction, s: Fraction) -> str:
    trans = tuple(eq.transforms or ())
    op = trans[0] if trans else "add"
    rel = str(getattr(eq, "relation", None) or "=")
    var = str(getattr(eq, "var_latex", None) or "x")
    if op == "add":
        return f"{var} + {num_latex(a)} {rel} {num_latex(rhs)}"
    if op == "sub":
        return f"{var} - {num_latex(a)} {rel} {num_latex(rhs)}"
    if op == "div":
        return f"\\frac{{{var}}}{{{num_latex(a)}}} {rel} {num_latex(rhs)}"
    return f"{num_latex(a)}{var} {rel} {num_latex(rhs)}"


def _hidden_two(eq: Any, a: Fraction, b: Fraction, rhs: Fraction) -> str:
    rel = str(getattr(eq, "relation", None) or "=")
    var = str(getattr(eq, "var_latex", None) or "x")
    if b < 0:
        return f"{num_latex(a)}{var} - {num_latex(abs(b))} {rel} {num_latex(rhs)}"
    return f"{num_latex(a)}{var} + {num_latex(b)} {rel} {num_latex(rhs)}"


def _fill_number_one(
    ctx: PrimitiveContext,
    fr: WpFrame,
    *,
    ineq: bool = False,
) -> tuple[PackedStory, SlotEq]:
    add_hi, mul_hi, sol_hi, ft = _ranges(ctx)
    variant = fr.variant or "add"
    if ft == 0 and variant == "div":
        variant = "mul"
    op_word = _INEQ_PHRASE.get(_pick_ineq_op(ctx), "more than") if ineq else ""
    rel = f" {op_word}" if ineq else ""
    ask = " What numbers work?" if ineq else " What is the number?"
    var = "x"
    if variant == "add":
        s = Fraction(_ri(ctx, 1, sol_hi))
        a = Fraction(_ri(ctx, 1, add_hi))
        rhs = s + a
        latex, text = compose_story("A number plus ", a, " is", rel, " ", rhs, ".", ask)
        trans = ("add",)
        leading = Fraction(1)
    elif variant == "sub":
        a = Fraction(_ri(ctx, 1, add_hi))
        s = Fraction(_ri(ctx, int(a) + 1, int(a) + sol_hi))
        rhs = s - a
        latex, text = compose_story("", a, " less than a number is", rel, " ", rhs, ".", ask)
        trans = ("sub",)
        leading = Fraction(1)
    elif variant == "div":
        a = Fraction(_ri(ctx, 2, mul_hi))
        rhs = Fraction(_ri(ctx, 2, sol_hi))
        s = a * rhs
        latex, text = compose_story(
            "A number divided by ", a, " is", rel, " ", rhs, ".", ask
        )
        trans = ("div",)
        leading = a
    else:
        a = Fraction(_ri(ctx, 2, mul_hi))
        s = Fraction(_ri(ctx, 2, sol_hi))
        rhs = a * s
        latex, text = compose_story("", a, " times a number is", rel, " ", rhs, ".", ask)
        trans = ("mul",)
        leading = a
    op = _pick_ineq_op(ctx) if ineq else "="
    eq = _slot_eq(
        ctx, s=s, leading=leading, trans=trans, steps="one", rhs=rhs, ineq=ineq, op=op, var=var
    )
    hidden = _hidden_one(eq, a if variant != "mul" else leading, rhs, s)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_ineq(eq, s) if ineq else _answer_eq(s),
        frame_id="number_one_step",
        variant=variant,
        hidden_eq=hidden,
    )
    return story, eq


def _fill_number_two(
    ctx: PrimitiveContext,
    fr: WpFrame,
    *,
    ineq: bool = False,
) -> tuple[PackedStory, SlotEq]:
    _add_hi, mul_hi, sol_hi, _ft = _ranges(ctx)
    a = Fraction(_ri(ctx, 2, mul_hi))
    s = Fraction(_ri(ctx, 2, sol_hi))
    if ctx.rng.random() < 0.45:
        b = Fraction(-_ri(ctx, 1, min(8, int(a * s) - 1) if int(a * s) > 2 else 1))
    else:
        b = Fraction(_ri(ctx, 1, 8))
    rhs = a * s + b
    if rhs <= 0:
        b = Fraction(_ri(ctx, 1, 8))
        rhs = a * s + b
    rel = ""
    if ineq:
        rel = f" {_INEQ_PHRASE.get(_pick_ineq_op(ctx), 'more than')}"
    ask = ". What numbers work?" if ineq else ". Find the number."
    if b < 0:
        latex, text = compose_story(
            "", abs(b), " less than ", a, " times a number is", rel, " ", rhs, ask
        )
        variant = "less"
    else:
        latex, text = compose_story(
            "The sum of ", a, " times a number and ", b, " is", rel, " ", rhs, ask
        )
        variant = "sum"
    op = _pick_ineq_op(ctx) if ineq else "="
    eq = _slot_eq(
        ctx,
        s=s,
        leading=a,
        trans=("add", "mul"),
        steps="two",
        rhs=rhs,
        ineq=ineq,
        op=op,
    )
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_ineq(eq, s) if ineq else _answer_eq(s),
        frame_id="number_two_step",
        variant=variant,
        hidden_eq=_hidden_two(eq, a, b, rhs),
    )
    return story, eq


def _fill_money_spent(ctx: PrimitiveContext, name: str) -> tuple[PackedStory, SlotEq]:
    add_hi, _m, sol_hi, _ft = _ranges(ctx)
    spent = _ri(ctx, 1, add_hi)
    left = _ri(ctx, 1, sol_hi)
    start = spent + left
    s = Fraction(start)
    a = Fraction(spent)
    rhs = Fraction(left)
    latex, text = compose_story(
        f"{name} had some money, spent ${spent}, and has ${left} left. "
        f"How much did {name} start with?"
    )
    eq = _slot_eq(ctx, s=s, leading=Fraction(1), trans=("sub",), steps="one", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units="$"),
        frame_id="money_spent",
        variant="spent",
        hidden_eq=_hidden_one(eq, a, rhs, s),
        units="$",
    )
    return story, eq


def _fill_money_received(ctx: PrimitiveContext, name: str) -> tuple[PackedStory, SlotEq]:
    add_hi, _m, sol_hi, _ft = _ranges(ctx)
    rec = _ri(ctx, 1, add_hi)
    start = _ri(ctx, 1, sol_hi)
    total = start + rec
    s = Fraction(start)
    a = Fraction(rec)
    rhs = Fraction(total)
    latex, text = compose_story(
        f"{name} had some money, received ${rec}, and now has ${total}. "
        f"How much did {name} start with?"
    )
    eq = _slot_eq(ctx, s=s, leading=Fraction(1), trans=("add",), steps="one", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units="$"),
        frame_id="money_received",
        variant="received",
        hidden_eq=_hidden_one(eq, a, rhs, s),
        units="$",
    )
    return story, eq


def _fill_money_donations(ctx: PrimitiveContext, name: str) -> tuple[PackedStory, SlotEq]:
    _a, mul_hi, sol_hi, _ft = _ranges(ctx)
    n = _ri(ctx, 2, mul_hi)
    each = _ri(ctx, 2, sol_hi)
    total = n * each
    s = Fraction(each)
    a = Fraction(n)
    rhs = Fraction(total)
    latex, text = compose_story(
        f"{name} collected {n} equal donations totaling ${total}. "
        f"How much was each donation?"
    )
    eq = _slot_eq(ctx, s=s, leading=a, trans=("mul",), steps="one", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units="$"),
        frame_id="money_donations",
        variant="each",
        hidden_eq=_hidden_one(eq, a, rhs, s),
        units="$",
    )
    return story, eq


def _fill_money_shared(ctx: PrimitiveContext, name: str) -> tuple[PackedStory, SlotEq]:
    _a, mul_hi, sol_hi, _ft = _ranges(ctx)
    n = _ri(ctx, 2, mul_hi)
    each = _ri(ctx, 2, sol_hi)
    total = n * each
    s = Fraction(each)
    a = Fraction(n)
    rhs = Fraction(total)
    latex, text = compose_story(
        f"{name} shared ${total} equally among {n} friends. "
        f"How much did each friend receive?"
    )
    eq = _slot_eq(ctx, s=s, leading=a, trans=("mul",), steps="one", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units="$"),
        frame_id="money_shared",
        variant="shared",
        hidden_eq=_hidden_one(eq, a, rhs, s),
        units="$",
    )
    return story, eq


def _fill_tickets(
    ctx: PrimitiveContext,
    name: str,
    things: str,
    *,
    ineq: bool,
) -> tuple[PackedStory, SlotEq]:
    _a, mul_hi, sol_hi, _ft = _ranges(ctx)
    price = _ri(ctx, 2, mul_hi)
    count = _ri(ctx, 2, sol_hi)
    total = price * count
    s = Fraction(count)
    a = Fraction(price)
    rhs = Fraction(total)
    op = _pick_ineq_op(ctx) if ineq else "="
    if ineq:
        word = _INEQ_PHRASE.get(op, "more than")
        latex, text = compose_story(
            f"{things.capitalize()} cost ${price} each. {name} can spend {word} "
            f"${total}. How many {things} can {name} buy?"
        )
        eq = _slot_eq(
            ctx, s=s, leading=a, trans=("mul",), steps="one", rhs=rhs, ineq=True, op=op
        )
        story = PackedStory(
            latex=latex,
            text=text,
            answer_latex=_answer_ineq(eq, s),
            frame_id="ineq_tickets",
            variant="ineq_tickets",
            hidden_eq=_hidden_one(eq, a, rhs, s),
            units=things,
        )
        return story, eq
    latex, text = compose_story(
        f"{things.capitalize()} cost ${price} each. {name} spends ${total}. "
        f"How many {things} did {name} buy?"
    )
    eq = _slot_eq(ctx, s=s, leading=a, trans=("mul",), steps="one", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units=things),
        frame_id="count_tickets",
        variant="tickets",
        hidden_eq=_hidden_one(eq, a, rhs, s),
        units=things,
    )
    return story, eq


def _fill_groups(
    ctx: PrimitiveContext, name: str, things: str
) -> tuple[PackedStory, SlotEq]:
    _a, mul_hi, sol_hi, _ft = _ranges(ctx)
    groups = _ri(ctx, 2, mul_hi)
    each = _ri(ctx, 2, sol_hi)
    total = groups * each
    s = Fraction(total)
    a = Fraction(groups)
    rhs = Fraction(each)
    latex, text = compose_story(
        f"{name} divided some {things} into {groups} equal groups with "
        f"{each} in each group. How many {things} were there?"
    )
    eq = _slot_eq(ctx, s=s, leading=a, trans=("div",), steps="one", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units=things),
        frame_id="count_groups",
        variant="groups",
        hidden_eq=_hidden_one(eq, a, rhs, s),
        units=things,
    )
    return story, eq


def _fill_money_two(
    ctx: PrimitiveContext, name: str, things: str
) -> tuple[PackedStory, SlotEq]:
    _a, mul_hi, sol_hi, _ft = _ranges(ctx)
    price = _ri(ctx, 2, mul_hi)
    count = _ri(ctx, 2, sol_hi)
    fee = _ri(ctx, 1, 8)
    total = price * count + fee
    s = Fraction(count)
    a = Fraction(price)
    b = Fraction(fee)
    rhs = Fraction(total)
    fee_item = ctx.rng.choice(_FEE_ITEMS)
    latex, text = compose_story(
        f"{name} buys {things} at ${price} each and a ${fee} {fee_item}. "
        f"The total is ${total}. How many {things} did {name} buy?"
    )
    eq = _slot_eq(ctx, s=s, leading=a, trans=("add", "mul"), steps="two", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units=things),
        frame_id="money_two_step",
        variant="unit_plus_fee",
        hidden_eq=_hidden_two(eq, a, b, rhs),
        units=things,
    )
    return story, eq


def _fill_compare_twice(
    ctx: PrimitiveContext, name: str, things: str
) -> tuple[PackedStory, SlotEq]:
    """IA §2.2 Ex 2.14: three more than twice the notebooks."""
    _a, _m, sol_hi, _ft = _ranges(ctx)
    n = _ri(ctx, 2, sol_hi)
    extra = _ri(ctx, 1, 8)
    twice = 2
    known = twice * n + extra
    s = Fraction(n)
    a = Fraction(twice)
    b = Fraction(extra)
    rhs = Fraction(known)
    known_items = ctx.rng.choice(("textbooks", "puzzles", "stickers"))
    if known_items == things:
        known_items = "textbooks"
    latex, text = compose_story(
        f"The number of {known_items} {name} bought was {extra} more than twice "
        f"the number of {things}. {name} bought {known} {known_items}. "
        f"How many {things} were there?"
    )
    eq = _slot_eq(ctx, s=s, leading=a, trans=("add", "mul"), steps="two", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units=things),
        frame_id="compare_twice",
        variant="twice_more",
        hidden_eq=_hidden_two(eq, a, b, rhs),
        units=things,
    )
    return story, eq


def _fill_earnings_two(ctx: PrimitiveContext, name: str) -> tuple[PackedStory, SlotEq]:
    """IA §2.2 Ex 2.19 scaled: together T; one earns k less than twice the other."""
    other = pick_name(rng=ctx.rng, exclude=[name])
    _a, _m, sol_hi, _ft = _ranges(ctx)
    b_earn = _ri(ctx, 4, max(8, sol_hi))
    k = _ri(ctx, 1, min(6, b_earn))
    a_earn = 2 * b_earn - k
    together = a_earn + b_earn  # 3b - k
    s = Fraction(b_earn)
    leading = Fraction(3)
    b = Fraction(-k)
    rhs = Fraction(together)
    latex, text = compose_story(
        f"{name} and {other} together earn ${together}. {name} earns ${k} less "
        f"than twice what {other} earns. How much does {other} earn?"
    )
    eq = _slot_eq(ctx, s=s, leading=leading, trans=("add", "mul"), steps="two", rhs=rhs)
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_eq(s, units="$"),
        frame_id="earnings_two_step",
        variant="twice_less",
        hidden_eq=_hidden_two(eq, leading, b, rhs),
        units="$",
    )
    return story, eq


def _fill_ineq_compare(ctx: PrimitiveContext, name: str) -> tuple[PackedStory, SlotEq]:
    _a, _m, sol_hi, _ft = _ranges(ctx)
    threshold = _ri(ctx, 10, max(16, sol_hi + 10))
    op = _pick_ineq_op(ctx)
    word = _INEQ_PHRASE.get(op, "more than")
    s = Fraction(threshold)
    latex, text = compose_story(
        f"{name} wants a score {word} {threshold}. "
        f"Write an inequality for the score."
    )
    eq = _slot_eq(
        ctx, s=s, leading=Fraction(1), trans=(), steps="one", rhs=s, ineq=True, op=op
    )
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_ineq(eq, s),
        frame_id="ineq_score",
        variant="score",
        hidden_eq=f"x {op} {num_latex(s)}",
        units="points",
    )
    return story, eq


def _fill_ineq_height(ctx: PrimitiveContext) -> tuple[PackedStory, SlotEq]:
    """EA §2.7 #504: a child's height must be at least n inches."""
    inches = _ri(ctx, 40, 60) if _ranges(ctx)[2] > 6 else _ri(ctx, 48, 60)
    op = ctx.rng.choice((r"\ge", ">"))
    word = _INEQ_PHRASE.get(op, "at least")
    s = Fraction(inches)
    latex, text = compose_story(
        f"A child's height must be {word} {inches} inches to ride in the front "
        f"seat. Write an inequality for the height h."
    )
    eq = _slot_eq(
        ctx,
        s=s,
        leading=Fraction(1),
        trans=(),
        steps="one",
        rhs=s,
        ineq=True,
        op=op,
        var="h",
    )
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_ineq(eq, s),
        frame_id="ineq_height",
        variant="height",
        hidden_eq=f"h {op} {num_latex(s)}",
        units="inches",
    )
    return story, eq


def _fill_ineq_checkout(ctx: PrimitiveContext) -> tuple[PackedStory, SlotEq]:
    """EA §2.7 #507: express lane at most n items."""
    cap = _ri(ctx, 4, 12)
    op = ctx.rng.choice((r"\le", "<"))
    word = _INEQ_PHRASE.get(op, "at most")
    s = Fraction(cap)
    latex, text = compose_story(
        f"The number of items a shopper can have in the express check-out lane "
        f"is {word} {cap}. Write an inequality for the number of items n."
    )
    eq = _slot_eq(
        ctx,
        s=s,
        leading=Fraction(1),
        trans=(),
        steps="one",
        rhs=s,
        ineq=True,
        op=op,
        var="n",
    )
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_ineq(eq, s),
        frame_id="ineq_checkout",
        variant="checkout",
        hidden_eq=f"n {op} {num_latex(s)}",
        units="items",
    )
    return story, eq


def _fill_ineq_points(ctx: PrimitiveContext, name: str) -> tuple[PackedStory, SlotEq]:
    add_hi, _m, sol_hi, _ft = _ranges(ctx)
    have = _ri(ctx, 2, add_hi + 2)
    score = _ri(ctx, 2, sol_hi)
    need = have + score
    s = Fraction(score)
    a = Fraction(have)
    rhs = Fraction(need)
    op = ctx.rng.choice((r"\ge", ">"))
    word = _INEQ_PHRASE.get(op, "at least")
    latex, text = compose_story(
        f"{name} already has {have} points and needs {word} {need} points "
        f"in total. What scores on the next round work?"
    )
    eq = _slot_eq(
        ctx, s=s, leading=Fraction(1), trans=("add",), steps="one", rhs=rhs, ineq=True, op=op
    )
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_ineq(eq, s),
        frame_id="ineq_points",
        variant="add_points",
        hidden_eq=_hidden_one(eq, a, rhs, s),
        units="points",
    )
    return story, eq


def _fill_ineq_lost(ctx: PrimitiveContext, name: str) -> tuple[PackedStory, SlotEq]:
    add_hi, _m, sol_hi, _ft = _ranges(ctx)
    lost = _ri(ctx, 1, add_hi)
    now = _ri(ctx, 1, sol_hi)
    start = now + lost
    s = Fraction(start)
    a = Fraction(lost)
    rhs = Fraction(now)
    op = _pick_ineq_op(ctx)
    word = _INEQ_PHRASE.get(op, "more than")
    latex, text = compose_story(
        f"{name} had some points, lost {lost}, and now has {word} {now}. "
        f"What starting scores work?"
    )
    eq = _slot_eq(
        ctx, s=s, leading=Fraction(1), trans=("sub",), steps="one", rhs=rhs, ineq=True, op=op
    )
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_ineq(eq, s),
        frame_id="ineq_lost",
        variant="lost_points",
        hidden_eq=_hidden_one(eq, a, rhs, s),
        units="points",
    )
    return story, eq


def _fill_ineq_budget(
    ctx: PrimitiveContext, name: str, things: str
) -> tuple[PackedStory, SlotEq]:
    """IA §2.5: car rental, tablets, phone plan — not bike-only."""
    _a, mul_hi, sol_hi, _ft = _ranges(ctx)
    price = _ri(ctx, 2, mul_hi)
    count = _ri(ctx, 2, sol_hi)
    fee = _ri(ctx, 1, 12)
    cap = price * count + fee
    s = Fraction(count)
    a = Fraction(price)
    b = Fraction(fee)
    rhs = Fraction(cap)
    op = ctx.rng.choice((r"\le", "<"))
    word = _INEQ_PHRASE.get(op, "at most")
    flavor = ctx.rng.choice(("car_rental", "tablets", "phone", "unit_plus_fee"))
    if flavor == "car_rental":
        latex, text = compose_story(
            f"{name} rents a car for ${fee} plus ${price} per mile. "
            f"{name} can spend {word} ${cap}. For how many miles can {name} drive?"
        )
        units = "miles"
        variant = "car_rental"
    elif flavor == "tablets":
        latex, text = compose_story(
            f"{name} has ${cap} to buy tablets that cost ${price} each, plus a "
            f"${fee} delivery fee. How many tablets can {name} buy?"
        )
        units = "tablets"
        variant = "tablets"
    elif flavor == "phone":
        latex, text = compose_story(
            f"{name}'s phone plan costs ${fee} plus ${price} per text. "
            f"{name} wants the bill {word} ${cap}. How many texts can {name} send?"
        )
        units = "texts"
        variant = "phone"
    else:
        fee_item = ctx.rng.choice(_FEE_ITEMS)
        latex, text = compose_story(
            f"{name} buys {things} at ${price} each and a ${fee} {fee_item}. "
            f"The total must be {word} ${cap}. How many {things} can {name} buy?"
        )
        units = things
        variant = "unit_plus_fee"
    eq = _slot_eq(
        ctx,
        s=s,
        leading=a,
        trans=("add", "mul"),
        steps="two",
        rhs=rhs,
        ineq=True,
        op=op,
    )
    story = PackedStory(
        latex=latex,
        text=text,
        answer_latex=_answer_ineq(eq, s),
        frame_id="ineq_budget",
        variant=variant,
        hidden_eq=_hidden_two(eq, a, b, rhs),
        units=units,
    )
    return story, eq


def _fill_number_fallback_slots(
    ctx: PrimitiveContext, *, ineq: bool
) -> tuple[PackedStory, SlotEq]:
    fr = WpFrame("number_one_step", "one", ("add",), "number", variant="add")
    if ineq:
        return _fill_ineq_compare(ctx, pick_name(rng=ctx.rng))
    return _fill_number_one(ctx, fr, ineq=False)


def _package_proportion(ctx: PrimitiveContext) -> WordProblemItem:
    """EA §8.7: recipe scale, unit-rate cost, calories, pediatric dosage."""
    d = float(ctx.topic_d)
    nt = SkeletonDifficultyBands.from_d(d).numeric_tier
    ft = SkeletonDifficultyBands.from_d(d).format_tier
    rng = ctx.rng
    frames = ["prop_recipe", "prop_unit_rate", "prop_calories", "prop_dosage"]
    rng.shuffle(frames)
    frames = _rotate_for_d(ctx, frames)
    fid = frames[0]
    n1 = rng.randint(2, 3 + nt)
    extra = rng.randint(2, 4 + nt)
    n2 = n1 + extra
    if fid == "prop_calories":
        each = rng.randint(8, 20 + 6 * nt)
    else:
        each = rng.randint(2, (4, 6, 8, 10, 12)[nt])
    amt1 = n1 * each
    amt2 = n2 * each
    name = pick_name(rng=rng)
    things = pick_things(1, rng=rng)[0]
    units = ""
    if fid == "prop_recipe":
        latex, text = compose_story(
            f"{name}'s recipe for {n1} dozen cookies uses {amt1} cups of flour. "
            f"How many cups are needed for {n2} dozen cookies?"
        )
        ans = _answer_eq(Fraction(amt2), units="cups")
        units = "cups"
        variant = "recipe"
        hidden = rf"\frac{{{n1}}}{{{amt1}}} = \frac{{{n2}}}{{x}}"
    elif fid == "prop_calories":
        drink = rng.choice(_CALORIE_DRINKS)
        latex, text = compose_story(
            f"A {n1}-ounce {drink} has {amt1} calories. "
            f"How many calories are in a {n2}-ounce {drink}?"
        )
        ans = _answer_eq(Fraction(amt2), units="calories")
        units = "calories"
        variant = "calories"
        hidden = rf"\frac{{{n1}}}{{{amt1}}} = \frac{{{n2}}}{{x}}"
    elif fid == "prop_dosage":
        # EA 8.7: 5 ml per 25 lb (integer ratio).
        per, per_wt = rng.choice(((5, 25), (15, 5), (10, 25)))
        wt = per_wt * rng.randint(2, 3 + nt)
        dose = per * (wt // per_wt)
        latex, text = compose_story(
            f"A pediatrician prescribes {per} milliliters of medicine for every "
            f"{per_wt} pounds of a child's weight. If {name} weighs {wt} pounds, "
            f"how many milliliters should be prescribed?"
        )
        ans = _answer_eq(Fraction(dose), units="ml")
        units = "ml"
        amt2 = dose
        n1, amt1, n2 = per_wt, per, wt
        variant = "dosage"
        hidden = rf"\frac{{{per}}}{{{per_wt}}} = \frac{{x}}{{{wt}}}"
    else:
        latex, text = compose_story(
            f"If {n1} {things} cost ${amt1}, how much do {n2} {things} cost "
            f"at the same rate?"
        )
        ans = _answer_eq(Fraction(amt2), units="$")
        units = "$"
        variant = "unit_rate"
        fid = "prop_unit_rate"
        hidden = rf"\frac{{{n1}}}{{{amt1}}} = \frac{{{n2}}}{{x}}"
    meta = {
        "skeleton_pattern": "ProportionRate",
        "species": "proportion",
        "frame_id": fid,
        "frame_variant": variant,
        "numeric_tier": nt,
        "format_tier": ft,
        "transforms": ["cross_multiply"],
        "n_ops": 1,
        "construction": "wp_packaging",
        "unit_count": n1,
        "target_count": n2,
        "units": units,
    }
    return WordProblemItem(
        latex=latex,
        text=text,
        answer_latex=ans,
        kind="proportion",
        equation_latex=hidden,
        upgrades=(),
        effective_d=d,
        shape_id=fid,
        frame=fid,
        metadata=meta,
    )


def _use_similar_diagram(settings: dict[str, Any]) -> bool:
    style = str(settings.get("prompt_style", "diagram")).strip().lower()
    if style in {"description_only", "description", "text", "text_only"}:
        return False
    if "include_figure" in settings:
        return bool(settings["include_figure"])
    if "include_diagram" in settings:
        return bool(settings["include_diagram"])
    return True


def _package_systems(ctx: PrimitiveContext) -> WordProblemItem:
    """OpenStax EA §5.4 applications — number, tickets, rectangle, opposite-direction.

    D=0 stays number or tickets with small positive ints. Does not dump a
    ``cases`` environment into the prompt. Opt out with ``use_legacy_systems``.
    """
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    nt = bands.numeric_tier
    ft = bands.format_tier
    rng = ctx.rng
    ids = ["sys_number", "sys_tickets"]
    if ft >= 1:
        ids.extend(["sys_geometry", "sys_motion"])
    fid = str(rng.choice(ids))
    name = pick_name(rng=ctx.rng)

    if fid == "sys_number":
        smaller = _ri(ctx, 2, 4 + nt)
        more = _ri(ctx, 2, 5 + nt)
        larger = smaller + more
        total = smaller + larger
        latex, text = compose_story(
            "The sum of two numbers is ",
            Fraction(total),
            ". One number is ",
            Fraction(more),
            " more than the other. Find the two numbers.",
        )
        ans = rf"{smaller} \text{{ and }} {larger}"
        hidden = rf"x + y = {total},\ y = x + {more}"
    elif fid == "sys_tickets":
        adults = _ri(ctx, 2, 5 + nt)
        children = _ri(ctx, 2, 6 + nt)
        a_price = int(rng.choice((8, 10, 12, 15)))
        c_price = int(rng.choice((4, 5, 6, 7)))
        sold = adults + children
        total = a_price * adults + c_price * children
        latex, text = compose_story(
            f"{name} sold {sold} tickets for a total of ${total}. "
            f"Adult tickets cost ${a_price} and child tickets cost ${c_price}. "
            "How many adult tickets and how many child tickets were sold?"
        )
        ans = rf"{adults} \text{{ adult}},\ {children} \text{{ child}}"
        hidden = (
            rf"a + c = {sold},\ {a_price}a + {c_price}c = {total}"
        )
    elif fid == "sys_geometry":
        width = _ri(ctx, 3, 8 + nt)
        extra = _ri(ctx, 2, 6 + nt)
        length = width + extra
        peri = 2 * (length + width)
        latex, text = compose_story(
            "The length of a rectangle is ",
            Fraction(extra),
            " inches more than the width. The perimeter is ",
            Fraction(peri),
            " inches. Find the length and the width.",
        )
        ans = rf"{length} \text{{ in by }} {width} \text{{ in}}"
        hidden = rf"L = W + {extra},\ 2L + 2W = {peri}"
    else:
        slow = _ri(ctx, 30, 50 + 5 * nt)
        extra = int(rng.choice((10, 15, 20, 25)))
        fast = slow + extra
        hours = int(rng.choice((2, 3, 4)))
        dist = (slow + fast) * hours
        latex, text = compose_story(
            f"Two cars leave at the same time in opposite directions. "
            f"One travels ",
            Fraction(extra),
            " mph faster than the other. After ",
            Fraction(hours),
            " hours they are ",
            Fraction(dist),
            " miles apart. Find the two speeds.",
        )
        ans = rf"{slow} \text{{ mph and }} {fast} \text{{ mph}}"
        hidden = rf"r + (r + {extra}) = {slow + fast},\ ({slow}+{fast})({hours}) = {dist}"
        fid = "sys_motion"

    return WordProblemItem(
        latex=latex,
        text=text,
        answer_latex=ans,
        kind="systems",
        equation_latex=hidden,
        upgrades=("systems_wp", fid),
        effective_d=d,
        shape_id=fid,
        frame=fid,
        metadata={
            "skeleton_pattern": "SystemsWP",
            "species": "systems",
            "frame_id": fid,
            "construction": "wp_packaging",
            "numeric_tier": nt,
            "format_tier": ft,
            "n_ops": 2,
            "n_constraints": 2,
        },
    )


def use_variation_packaging(settings: dict[str, Any] | None) -> bool:
    """Live default rotates direct + inverse OpenStax EA §8.9 frames."""
    s = dict(settings or {})
    if "use_variation_packaging" in s:
        return bool(s.get("use_variation_packaging"))
    if bool(s.get("use_legacy_variation")):
        return False
    return True


def sample_variation_packaged(ctx: PrimitiveContext) -> WordProblemItem:
    """Direct and inverse variation with story rotation (not inverse-only)."""
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    rng = ctx.rng
    k = _ri(ctx, 2, 6 + nt)
    x = _ri(ctx, 2, 4 + nt)
    direct_ids = ["var_direct_k", "var_direct_point", "var_direct_rate"]
    inverse_ids = ["var_inverse_k", "var_inverse_point"]
    if ft >= 1:
        direct_ids.append("var_direct_cost")
        inverse_ids.append("var_inverse_pressure")
    use_direct = rng.random() < 0.5
    fid = str(rng.choice(direct_ids if use_direct else inverse_ids))
    name = pick_name(rng=rng)

    if fid == "var_direct_k":
        latex = rf"\text{{Write a direct variation equation with }} k = {k}."
        text = f"Write a direct variation equation with k = {k}."
        ans = rf"y = {k}x"
        hidden = rf"y = {k}x"
    elif fid == "var_direct_point":
        y = k * x
        latex = (
            rf"\text{{If }} y \text{{ varies directly with }} x "
            rf"\text{{ and }} y = {y} \text{{ when }} x = {x}, "
            rf"\text{{ write the equation.}}"
        )
        text = (
            f"If y varies directly with x and y = {y} when x = {x}, "
            f"write the equation."
        )
        ans = rf"y = {k}x"
        hidden = rf"y = {k}x,\ y = {k} \cdot {x}"
    elif fid == "var_direct_rate":
        hours = int(rng.choice((2, 3, 4, 5)))
        dist = k * hours
        latex = (
            rf"\text{{{name} travels at a constant speed. In {hours} hours "
            rf"{name} goes {dist} miles. Write the distance }} d \text{{ "
            rf"as a function of time }} t \text{{ in hours.}}"
        )
        text = (
            f"{name} travels at a constant speed. In {hours} hours {name} "
            f"goes {dist} miles. Write the distance d as a function of "
            f"time t in hours."
        )
        ans = rf"d = {k}t"
        hidden = rf"d = {k}t,\ d = {k} \cdot {hours}"
    elif fid == "var_direct_cost":
        y = k * x
        thing = pick_things(1, rng=rng)[0]
        latex = (
            rf"\text{{The cost of {thing} varies directly with the number "
            rf"purchased. {x} {thing} cost \${y}. Write the cost }} C "
            rf"\text{{ as a function of the number }} n \text{{ purchased.}}"
        )
        text = (
            f"The cost of {thing} varies directly with the number purchased. "
            f"{x} {thing} cost ${y}. Write the cost C as a function of the "
            f"number n purchased."
        )
        ans = rf"C = {k}n"
        hidden = rf"C = {k}n"
    elif fid == "var_inverse_k":
        latex = rf"\text{{Write an inverse variation equation with }} k = {k}."
        text = f"Write an inverse variation equation with k = {k}."
        ans = rf"y = \frac{{{k}}}{{x}}"
        hidden = rf"y = \frac{{{k}}}{{x}}"
    else:
        y_val = Fraction(k, x)
        y_tex = num_latex(y_val)
        if fid == "var_inverse_pressure":
            latex = (
                rf"\text{{The pressure of a fixed amount of gas varies "
                rf"inversely with its volume. When the volume is {x} "
                rf"liters, the pressure is {y_tex} atm. Write the "
                rf"pressure }} P \text{{ as a function of volume }} V."
            )
            text = (
                f"The pressure of a fixed amount of gas varies inversely "
                f"with its volume. When the volume is {x} liters, the "
                f"pressure is {y_val} atm. Write the pressure P as a "
                f"function of volume V."
            )
            ans = rf"P = \frac{{{k}}}{{V}}"
            hidden = rf"P = \frac{{{k}}}{{V}}"
        else:
            latex = (
                rf"\text{{If }} y \text{{ varies inversely with }} x "
                rf"\text{{ and }} y = {y_tex} \text{{ when }} x = {x}, "
                rf"\text{{ write the equation.}}"
            )
            text = (
                f"If y varies inversely with x and y = {y_val} when x = {x}, "
                f"write the equation."
            )
            ans = rf"y = \frac{{{k}}}{{x}}"
            hidden = rf"y = \frac{{{k}}}{{x}}"

    return WordProblemItem(
        latex=latex,
        text=text,
        answer_latex=ans,
        kind="variation",
        equation_latex=hidden,
        upgrades=("variation_packaging", fid),
        effective_d=d,
        shape_id=fid,
        frame=fid,
        metadata={
            "skeleton_pattern": "VariationEq",
            "species": "variation",
            "frame_id": fid,
            "construction": "variation_packaging",
            "numeric_tier": nt,
            "format_tier": ft,
            "variation_kind": "direct" if use_direct else "inverse",
        },
    )


def _package_similar_figures(ctx: PrimitiveContext) -> WordProblemItem:
    """Scale-factor story + optional pair diagram on a proportion frame.

    OpenStax EA §8.7: similar triangles (Ex 8.78) at D=0; quadrilaterals and
    larger scale later. Does not dump ``a/b = x/c``.
    """
    from question_engine.diagrams import similar_figures_pair_figure

    d = float(ctx.topic_d)
    nt = SkeletonDifficultyBands.from_d(d).numeric_tier
    ft = SkeletonDifficultyBands.from_d(d).format_tier
    rng = ctx.rng
    settings = dict(getattr(ctx, "settings", None) or {})
    if ft == 0:
        shape = "triangle"
    elif ft == 1:
        shape = "triangle" if rng.random() < 0.4 else "rectangle"
    else:
        shape = "rectangle" if rng.random() < 0.7 else "triangle"
    # D=0: scale 2 (OpenStax easy). Higher numeric_tier widens the scale.
    ratio = 2 if nt == 0 else rng.randint(2, 3 + min(2, nt))
    small = rng.randint(2, 4) if nt == 0 else rng.randint(2, 4 + nt)
    other_small = rng.randint(2, 5) if nt == 0 else rng.randint(2, 5 + nt)
    if other_small == small:
        other_small += 1
    large = small * ratio
    other_large = other_small * ratio
    unit = "cm"
    use_diagram = _use_similar_diagram(settings)
    ask_scale = ft >= 1 and rng.random() < 0.3
    fid = "similar_triangles" if shape == "triangle" else "similar_quad"

    if shape == "triangle":
        # OpenStax Ex 8.78 uses ABC ~ XYZ; also keep ABC ~ DEF.
        if rng.random() < 0.5:
            small_labels = ("A", "B", "C")
            large_labels = ("X", "Y", "Z")
            pairs = (("AB", "XY"), ("BC", "YZ"), ("AC", "XZ"))
            similar_stmt_l = r"\triangle ABC \sim \triangle XYZ"
            similar_stmt_t = "Triangle ABC ~ triangle XYZ"
        else:
            small_labels = ("A", "B", "C")
            large_labels = ("D", "E", "F")
            pairs = (("AB", "DE"), ("BC", "EF"), ("AC", "DF"))
            similar_stmt_l = r"\triangle ABC \sim \triangle DEF"
            similar_stmt_t = "Triangle ABC ~ triangle DEF"
        angles = (50.0, 60.0, 70.0)
        aspect = (3.0, 2.0)
    else:
        small_labels = ("A", "B", "C", "D")
        large_labels = ("E", "F", "G", "H")
        pairs = (("AB", "EF"), ("AD", "EH"), ("BC", "FG"))
        similar_stmt_l = r"ABCD \sim EFGH"
        similar_stmt_t = "Quadrilateral ABCD ~ EFGH"
        angles = (50.0, 60.0, 70.0)
        aspect = (3.0, 2.0)

    given_pair, missing_pair = rng.sample(list(pairs), 2)
    corresponding = given_pair
    other_pair = missing_pair
    missing = other_pair[1]
    hidden = rf"\frac{{{small}}}{{{large}}} = \frac{{{other_small}}}{{x}}"

    if ask_scale:
        latex, text = compose_story(
            f"{similar_stmt_t}. The figures are similar. Corresponding sides "
            f"{corresponding[0]} and {corresponding[1]} measure {small} {unit} and "
            f"{large} {unit}. Find the scale factor from the smaller to the larger."
        )
        if use_diagram:
            latex = (
                rf"{similar_stmt_l}.\ "
                rf"\text{{The figures are similar. Corresponding sides {corresponding[0]} and {corresponding[1]} "
                rf"measure {small} {unit} and {large} {unit}. Find the scale factor from the smaller to the larger.}}"
            )
            text = (
                f"{similar_stmt_t}. The figures are similar. Corresponding sides "
                f"{corresponding[0]} and {corresponding[1]} measure {small} {unit} and "
                f"{large} {unit}. Find the scale factor from the smaller to the larger."
            )
        ans = num_latex(Fraction(ratio))
        hidden = rf"\frac{{{large}}}{{{small}}} = {ratio}"
        ask = "scale_factor"
    else:
        latex, text = compose_story(
            f"{similar_stmt_t}. The figures are similar. Corresponding sides "
            f"{corresponding[0]} and {corresponding[1]} measure {small} {unit} and "
            f"{large} {unit}. If {other_pair[0]} is {other_small} {unit}, find {missing}."
        )
        if use_diagram:
            latex = (
                rf"{similar_stmt_l}.\ "
                rf"\text{{The figures are similar. Corresponding sides {corresponding[0]} and {corresponding[1]} "
                rf"measure {small} {unit} and {large} {unit}. If {other_pair[0]} is "
                rf"{other_small} {unit}, find {missing}.}}"
            )
            text = (
                f"{similar_stmt_t}. The figures are similar. Corresponding sides "
                f"{corresponding[0]} and {corresponding[1]} measure {small} {unit} and "
                f"{large} {unit}. If {other_pair[0]} is {other_small} {unit}, find {missing}."
            )
        ans = _answer_eq(Fraction(other_large), units=unit)
        ask = "missing_side"

    meta: dict[str, Any] = {
        "skeleton_pattern": "SimilarFigures",
        "species": "proportion",
        "frame_id": fid,
        "numeric_tier": nt,
        "format_tier": ft,
        "transforms": ["cross_multiply", "scale_factor"],
        "n_ops": 1,
        "construction": "wp_packaging",
        "scale_factor": ratio,
        "shape": shape,
        "ask": ask,
        "missing_side": missing if ask == "missing_side" else "",
    }
    if use_diagram:
        small_sides = {corresponding[0]: f"{small} {unit}"}
        large_sides = {corresponding[1]: f"{large} {unit}"}
        if ask == "missing_side":
            small_sides[other_pair[0]] = f"{other_small} {unit}"
            large_sides[other_pair[1]] = "?"
        fig = similar_figures_pair_figure(
            shape=shape,  # type: ignore[arg-type]
            small_labels=small_labels,
            large_labels=large_labels,
            small_side_labels=small_sides,
            large_side_labels=large_sides,
            angles=angles,
            aspect=aspect,
            scale_factor=float(ratio),
        )
        meta.update(fig.to_metadata())
    return WordProblemItem(
        latex=latex,
        text=text,
        answer_latex=ans,
        kind="similar_figures",
        equation_latex=hidden,
        upgrades=("similar_figures",),
        effective_d=d,
        shape_id=fid,
        frame=fid,
        metadata=meta,
    )


def sample_write_one_step(ctx: PrimitiveContext, *, other: bool) -> WordProblemItem:
    """Write d=rt / cost / perimeter then find the value (SolveLinear one-step).

    Rate (``g6_constant_rate_equations``): OpenStax EA §2.6 vehicles × {d, r, t}.
    Other (``g6_equations_for_other_relationships``): cost, tickets, square, triangle.
    D=0 stays the product / one-step form (find d / find c / find P).
    """
    d = float(ctx.topic_d)
    story = _fill_other_write(ctx, d) if other else _fill_rate_write(ctx, d)
    trans = ["mul"]
    if story.frame_id == "write_triangle":
        trans = ["add"]
    elif story.frame_id == "write_cost_invert" or story.frame_id == "write_square_invert" or (
        story.frame_id == "write_rate" and story.variant.endswith(("_time", "_rate"))
    ):
        trans = ["div"]
    packed = {
        "skeleton_pattern": "SolveLinear",
        "frame_id": story.frame_id,
        "frame_variant": story.variant,
        "construction": "wp_packaging",
        "species": "one",
        "n_ops": 1,
        "steps": "one",
        "transforms": trans,
    }
    if story.units:
        packed["units"] = story.units
    if story.frame_id == "write_rate" and "_" in story.variant:
        vehicle, _, ask = story.variant.partition("_")
        packed["vehicle"] = vehicle
        packed["ask"] = ask
    return WordProblemItem(
        latex=story.latex,
        text=story.text,
        answer_latex=story.answer_latex,
        kind="write_one_step",
        equation_latex=story.hidden_eq,
        upgrades=("write_one_step",),
        effective_d=d,
        shape_id=story.frame_id,
        frame=story.frame_id,
        metadata=packed,
    )


def _fill_rate_write(ctx: PrimitiveContext, d: float) -> PackedStory:
    """EA §2.6: bike / drive / walk / bus / train; ask d, t, or r."""
    _add, mul_hi, sol_hi, _ft = _ranges(ctx)
    rate = _ri(ctx, 2, mul_hi)
    hours = _ri(ctx, 2, sol_hi)
    distance = rate * hours
    vid, verb = ctx.rng.choice(_RATE_VEHICLES)
    name = pick_name(rng=ctx.rng)
    if d < 5:
        mode = "find_distance"
    elif d < 12:
        mode = "find_distance" if ctx.rng.random() < 0.55 else "find_time"
    else:
        mode = ctx.rng.choice(["find_distance", "find_time", "find_rate"])

    if mode == "find_time":
        latex, text = compose_story(
            f"{name} {verb} at ",
            Fraction(rate),
            " miles per hour and covers ",
            Fraction(distance),
            " miles at a constant rate. Write an equation for the time t in hours, then find t.",
        )
        ans = rf"t = {distance}\div {rate};\; t = {hours}"
        hidden = rf"{distance} = {rate}t"
        variant = f"{vid}_time"
    elif mode == "find_rate":
        latex, text = compose_story(
            f"{name} {verb} and covers ",
            Fraction(distance),
            " miles in ",
            Fraction(hours),
            " hours at a constant rate. Write an equation for the speed r in mph, then find r.",
        )
        ans = rf"r = {distance}\div {hours};\; r = {rate}"
        hidden = rf"{distance} = r\cdot {hours}"
        variant = f"{vid}_rate"
    else:
        latex, text = compose_story(
            f"{name} {verb} at ",
            Fraction(rate),
            " miles per hour. Write an equation for the distance d after ",
            Fraction(hours),
            " hours, then find d.",
        )
        ans = rf"d = {rate}\cdot {hours};\; d = {distance}"
        hidden = rf"d = {rate}\cdot {hours}"
        variant = f"{vid}_distance"
    return PackedStory(
        latex=latex,
        text=text,
        answer_latex=ans,
        frame_id="write_rate",
        variant=variant,
        hidden_eq=hidden,
        units="miles",
    )


def _fill_other_write(ctx: PrimitiveContext, d: float) -> PackedStory:
    """EA §2.6 P=a+b+c / cost / tickets / 4s=P — not pencils-only.

    D=0 stays cost / tickets (old easy). Square invert (solve for s) and
    triangle third-side unlock with D, matching OpenStax §2.6 / §8.7 Be Prepared.
    """
    _add, mul_hi, sol_hi, _ft = _ranges(ctx)
    a = _ri(ctx, 2, mul_hi)
    n = _ri(ctx, 2, sol_hi)
    total = a * n
    name = pick_name(rng=ctx.rng)
    item = ctx.rng.choice(_COST_ITEMS)

    if d < 5:
        kind = ctx.rng.choice(["cost", "tickets"])
    elif d < 12:
        kind = ctx.rng.choice(["cost", "tickets", "square", "triangle"])
    else:
        kind = ctx.rng.choice(["square_invert", "triangle", "invert_cost", "tickets"])

    if kind == "invert_cost":
        latex, text = compose_story(
            f"{item.capitalize()} cost ",
            Fraction(a),
            " cents each. The total cost is ",
            Fraction(total),
            f" cents. Write an equation for the number of {item} n, then find n.",
        )
        ans = rf"{a}n = {total};\; n = {n}"
        return PackedStory(
            latex=latex,
            text=text,
            answer_latex=ans,
            frame_id="write_cost_invert",
            variant=item,
            hidden_eq=rf"{a}n = {total}",
            units=item,
        )
    if kind == "tickets":
        latex, text = compose_story(
            "Tickets cost $",
            Fraction(a),
            " each. Write an equation for the total T for ",
            Fraction(n),
            " tickets, then find T.",
        )
        ans = rf"T = {a}\cdot {n};\; T = {total}"
        return PackedStory(
            latex=latex,
            text=text,
            answer_latex=ans,
            frame_id="write_tickets",
            variant="tickets",
            hidden_eq=rf"T = {a}\cdot {n}",
            units="$",
        )
    if kind == "square":
        side = n
        peri = 4 * side
        latex, text = compose_story(
            "A square has side length ",
            Fraction(side),
            ". Write an equation for the perimeter P, then find P.",
        )
        ans = rf"P = 4\cdot {side};\; P = {peri}"
        return PackedStory(
            latex=latex,
            text=text,
            answer_latex=ans,
            frame_id="write_square",
            variant="perimeter",
            hidden_eq=rf"P = 4\cdot {side}",
            units="",
        )
    if kind == "square_invert":
        # Old high-D / EA §2.6: given P, write 4s = P and find s.
        side = n
        peri = 4 * side
        latex, text = compose_story(
            "A square has perimeter ",
            Fraction(peri),
            ". Write an equation for the side length s, then find s.",
        )
        ans = rf"4s = {peri};\; s = {side}"
        return PackedStory(
            latex=latex,
            text=text,
            answer_latex=ans,
            frame_id="write_square_invert",
            variant="side",
            hidden_eq=rf"4s = {peri}",
            units="",
        )
    if kind == "triangle":
        # EA §2.6 / §8.7 Be Prepared: P = a+b+c, two sides given, find the third.
        s1 = _ri(ctx, 3, sol_hi)
        s2 = _ri(ctx, 3, sol_hi)
        s3 = _ri(ctx, 3, max(3, s1 + s2 - 1))
        if s3 >= s1 + s2:
            s3 = s1 + s2 - 1
        peri = s1 + s2 + s3
        latex, text = compose_story(
            f"A triangle has perimeter {peri}. Two sides measure {s1} and {s2}. "
            f"Write an equation for the third side s, then find s."
        )
        ans = rf"{s1} + {s2} + s = {peri};\; s = {s3}"
        return PackedStory(
            latex=latex,
            text=text,
            answer_latex=ans,
            frame_id="write_triangle",
            variant="third_side",
            hidden_eq=rf"{s1}+{s2}+s={peri}",
            units="",
        )
    latex, text = compose_story(
        f"{item.capitalize()} cost ",
        Fraction(a),
        " cents each. Write an equation for the cost c of ",
        Fraction(n),
        f" {item}, then find c.",
    )
    ans = rf"c = {a}\cdot {n};\; c = {total}"
    return PackedStory(
        latex=latex,
        text=text,
        answer_latex=ans,
        frame_id="write_cost",
        variant=item,
        hidden_eq=rf"c = {a}\cdot {n}",
        units="cents",
    )


def looks_like_dumped_equation(prompt: str) -> bool:
    blob = (prompt or "").lower()
    if any(m in blob for m in _DUMP_MARKERS):
        return True
    if "after a one-step change" in blob or "applies two operations" in blob:
        return True
    return False
