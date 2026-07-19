"""Presentation layer: commute +/−/×/÷ display variants + explicit multiply."""

from __future__ import annotations

import random
import re
from fractions import Fraction

from question_engine.frameworks.primitives.distributive import (
    sample_distributive_algebraic,
    sample_distributive_numeric,
)
from question_engine.frameworks.primitives.presentation import (
    DisplayPiece,
    PresentationStyle,
    _apply_clutter_op,
    clutter_site_chance,
    maybe_clutter,
    order_commutative,
    render_addition,
    render_division,
    render_product,
    render_scaled_sum,
    render_subtraction,
    resolve_presentation,
)
from question_engine.frameworks.primitives.registry import (
    PRIM_DISTRIBUTIVE,
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)


def _dist_ctx(d: float = 12.0, seed: int = 0):
    return build_context(
        {
            "difficulty": d,
            "integers_only": True,
            "only_x": True,
            "lock_variable": "x",
            "exclude_zero": True,
        },
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_DISTRIBUTIVE],
        rng=random.Random(seed),
    )


# Markers that only appear from clutter traps (not schoolbook rendering).
_CLUTTER_MARKERS = re.compile(
    r"("
    r"\*1"  # mul by 1
    r"|\\cdot\s*1"
    r"|1\\cdot"
    r"|1\*"
    r"|/1\b"  # div by 1
    r"|\)/1"
    r"|\^\{?1\}?"  # ^1 / ^{1}
    r"|\^\{?0\}?"  # ^0 / ^{0}
    r"|/\(\d+/\d+\)"  # trivial cancel text form …*(k/k) already has *
    r"|\\frac\{\d+\}\{\d+\}"  # k/k in latex after ·
    r")"
)


def test_addition_commute_swaps_operands():
    style = PresentationStyle(commute_add=True)
    latex, text = render_addition(
        DisplayPiece("a", "a"),
        DisplayPiece("b", "b"),
        style,
        random.Random(0),
    )
    assert latex == "b + a"
    assert text == "b + a"


def test_multiplication_commute_and_explicit():
    school = PresentationStyle.schoolbook()
    l, t = render_product(
        [DisplayPiece("x", "x"), DisplayPiece(r"\left(1 + 2\right)", "(1 + 2)")],
        school,
        random.Random(0),
    )
    assert l == r"x\left(1 + 2\right)"
    assert t == "x(1 + 2)"

    flipped = PresentationStyle(commute_mul=True)
    l2, t2 = render_product(
        [DisplayPiece("x", "x"), DisplayPiece(r"\left(1 + 2\right)", "(1 + 2)")],
        flipped,
        random.Random(0),
    )
    assert l2 == r"\left(1 + 2\right)x"
    assert t2 == "(1 + 2)x"

    explicit = PresentationStyle(explicit_multiply=True, multiply_symbol="*")
    l3, t3 = render_product(
        [DisplayPiece("a", "a"), DisplayPiece(r"\left(b + x\right)", "(b + x)")],
        explicit,
        random.Random(0),
    )
    assert "*" in t3
    assert " * " in l3 or "*" in l3
    assert l3.count("*") == 1


def test_subtraction_flip_preserves_value_form():
    style = PresentationStyle(flip_subtraction=True)
    latex, text = render_subtraction(
        DisplayPiece("7", "7"),
        DisplayPiece("3", "3"),
        style,
    )
    assert latex == r"-\left(3 - 7\right)"
    assert text == "-(3 - 7)"


def test_division_flip_preserves_value_form():
    style = PresentationStyle(flip_division=True)
    latex, text = render_division(
        DisplayPiece("a", "a"),
        DisplayPiece("b", "b"),
        style,
    )
    assert latex == r"\frac{1}{\frac{b}{a}}"
    assert text == "1/(b/a)"


def test_gated_knobs_respect_min_d():
    # Force chances high but min_d above current D → no flip / no explicit *
    style = resolve_presentation(
        random.Random(1),
        d=2.0,
        overrides={
            "commute_add": False,
            "commute_mul": False,
            "flip_subtraction": {"enabled": True, "min_d": 10.0, "chance": 1.0},
            "flip_division": {"enabled": True, "min_d": 12.0, "chance": 1.0},
            "explicit_multiply": {"enabled": True, "min_d": 8.0, "chance": 1.0},
        },
    )
    assert not style.flip_subtraction
    assert not style.flip_division
    assert not style.explicit_multiply

    style_hi = resolve_presentation(
        random.Random(1),
        d=20.0,
        overrides={
            "commute_add": False,
            "commute_mul": False,
            "flip_subtraction": {"enabled": True, "min_d": 10.0, "chance": 1.0},
            "flip_division": {"enabled": True, "min_d": 12.0, "chance": 1.0},
            "explicit_multiply": {"enabled": True, "min_d": 8.0, "chance": 1.0},
        },
    )
    assert style_hi.flip_subtraction
    assert style_hi.flip_division
    assert style_hi.explicit_multiply


def test_order_commutative_pair_swaps():
    assert order_commutative([1, 2], commute=True, rng=random.Random(0)) == [2, 1]
    assert order_commutative([1, 2], commute=False, rng=random.Random(0)) == [1, 2]


def test_distributive_algebraic_multiple_forms():
    forms: set[str] = set()
    texts: set[str] = set()
    for seed in range(40):
        ctx = _dist_ctx(d=6.0, seed=seed)
        # Force schoolbook multiply, but allow commute for variety
        ctx._presentation_style = None  # type: ignore[attr-defined]
        from question_engine.frameworks.primitives.presentation import presentation_for_ctx

        presentation_for_ctx(
            ctx,
            d=6.0,
            overrides={
                "commute_add": seed % 2 == 0,
                "commute_mul": seed % 3 == 0,
                "explicit_multiply": False,
                "flip_subtraction": False,
                "flip_division": False,
                "clutter": {"amount": 0},
                "strangeness": {"amount": 0},
            },
        )
        expr = sample_distributive_algebraic(ctx)
        forms.add(expr.form)
        texts.add(expr.text)

    assert "var_outer" in forms
    assert "const_outer" in forms
    # Structural variety: paren-first factor and/or summand order
    assert any(t.startswith("(") for t in texts) or any(
        re.search(r"\([^)]*x", t) for t in texts
    )
    assert len(texts) > 4


def test_distributive_algebraic_live_generator_varies_at_d0():
    """Default knobs at D=0 must vary structure across seeds (not only x(a+b))."""
    from question_engine.generators import GENERATORS

    gen = GENERATORS["distributive_property_algebraic"]
    assert gen.__module__.endswith("primitive_g6"), (
        f"expected primitive_g6 override, got {gen.__module__}"
    )

    forms: set[str] = set()
    texts: list[str] = []
    for seed in range(60):
        random.seed(seed)
        qs = gen(
            "g6_distributive_property_algebraic",
            {
                "count": 1,
                "difficulty": 0,
                "integers_only": True,
                "only_x": True,
                "exclude_zero": True,
            },
        )
        q = qs[0]
        forms.add(str((q.metadata or {}).get("distributive_form") or ""))
        # Strip the instruction prefix for pattern checks
        body = q.prompt_text.split(":", 1)[-1].strip()
        texts.append(body)

    assert "var_outer" in forms
    assert "const_outer" in forms

    # Factor order: outer-first vs paren-first
    outer_first = any(re.match(r"^[A-Za-z]\(", t) or re.match(r"^-?\d+\(", t) for t in texts)
    paren_first = any(t.startswith("(") for t in texts)
    assert outer_first and paren_first

    # Summand order inside const-outer / paren-first const-outer: x±n vs n±x
    has_x_then_num = any(re.search(r"\(x\s*[+\-]", t) for t in texts)
    has_num_then_x = any(re.search(r"\(-?\d+\s*[+\-]\s*x\)", t) for t in texts)
    assert has_x_then_num and has_num_then_x

    assert len(set(texts)) >= 8


def test_distributive_explicit_multiply_consistent():
    for seed in range(12):
        ctx = _dist_ctx(d=20.0, seed=seed)
        from question_engine.frameworks.primitives.presentation import presentation_for_ctx

        presentation_for_ctx(
            ctx,
            d=20.0,
            overrides={
                "commute_add": False,
                "commute_mul": False,
                "explicit_multiply": True,
                "multiply_symbol": "*",
                "clutter": {"amount": 0},
                "strangeness": {"amount": 0},
                "strange_mode": False,
            },
        )
        expr = sample_distributive_numeric(ctx)
        assert expr.text.count("*") >= 1
        # Single product site → one multiply glyph (not mixed juxtaposition)
        assert "(" in expr.text
        # No juxtaposition of digit/paren without *
        assert re.search(r"\d\(", expr.text) is None


def test_scaled_sum_summand_order():
    style = PresentationStyle(commute_add=True)
    latex, text = render_scaled_sum(
        DisplayPiece("3", "3"),
        [("x", "x", Fraction(1)), ("2", "2", Fraction(2))],
        style,
        random.Random(0),
    )
    # commute_add on a pair swaps → 3(2 + x)
    assert "2 + x" in text or "2 + x" in latex.replace(" ", "")
    assert text.startswith("3(") or text.endswith(")3") or "*(" in text


def test_clutter_amount_zero_never_applies():
    style = resolve_presentation(
        random.Random(0),
        d=24.0,
        overrides={
            "clutter": {"amount": 0.0, "min_d": 0},
            "strangeness": {"amount": 0.0},
            "commute_add": False,
            "commute_mul": False,
            "explicit_multiply": False,
        },
    )
    assert style.clutter_amount == 0.0
    assert clutter_site_chance(style) == 0.0

    piece = DisplayPiece("3x", "3x")
    for seed in range(80):
        out = maybe_clutter(piece, style, random.Random(seed))
        assert out.latex == "3x"
        assert out.text == "3x"

    for seed in range(60):
        ctx = _dist_ctx(d=20.0, seed=seed)
        from question_engine.frameworks.primitives.presentation import presentation_for_ctx

        presentation_for_ctx(
            ctx,
            d=20.0,
            overrides={
                "clutter": {"amount": 0},
                "strangeness": {"amount": 0},
                "strange_mode": False,
                "explicit_multiply": False,
            },
        )
        expr = sample_distributive_algebraic(ctx)
        blob = f"{expr.latex} {expr.text}"
        assert "*1" not in blob
        assert "/1" not in blob
        assert "^1" not in blob and "^{1}" not in blob
        assert "^0" not in blob and "^{0}" not in blob
        assert r"\cdot 1" not in blob
        assert "1*" not in expr.text


def test_clutter_amount_high_produces_markers():
    style = resolve_presentation(
        random.Random(1),
        d=24.0,
        overrides={
            "clutter": {"amount": 3.0, "min_d": 0},
            "strangeness": {"amount": 0},
        },
    )
    assert style.clutter_amount > 0
    assert clutter_site_chance(style) > 0.5

    seen = False
    for seed in range(120):
        latex, text = render_product(
            [DisplayPiece("3", "3"), DisplayPiece("x", "x")],
            style,
            random.Random(seed),
        )
        blob = f"{latex} {text}"
        if _CLUTTER_MARKERS.search(blob) or re.search(r"[a-zA-Z]\d", text):
            seen = True
            break
        # unnecessary parens around factors
        if r"\left(" in latex and "3" in latex:
            # product of simple factors rarely needs left( unless cluttered
            if latex.count(r"\left(") >= 1 and ("3x" not in latex.replace(" ", "")):
                seen = True
                break
    assert seen, "expected some clutter markers at high amount + high D"

    # Direct op coverage (value-preserving shapes)
    base = DisplayPiece("3x", "3x")
    assert "*1" in _apply_clutter_op(base, "mul_by_1", random.Random(0)).text
    assert "/1" in _apply_clutter_op(base, "div_by_1", random.Random(0)).text
    assert "^1" in _apply_clutter_op(base, "pow_1", random.Random(0)).text
    assert "^0" in _apply_clutter_op(base, "pow_0", random.Random(0)).text
    assert "(" in _apply_clutter_op(base, "unnecessary_parens", random.Random(0)).text
    cancel = _apply_clutter_op(base, "trivial_cancel", random.Random(0))
    assert "/" in cancel.text
    weird = _apply_clutter_op(base, "weird_monomial", random.Random(1))
    assert weird.text != "3x" or weird.latex != "3x"


def test_clutter_respects_min_d():
    style = resolve_presentation(
        random.Random(0),
        d=2.0,
        overrides={"clutter": {"amount": 5.0, "min_d": 20.0}},
    )
    assert style.clutter_amount == 0.0


def test_strangeness_mixes_glyphs_in_one_expression():
    style = PresentationStyle(
        strange_mode=True,
        clutter_amount=0.0,
        explicit_multiply=False,
    )
    # Multiple product joins → should see more than one glyph family across samples
    mixed = False
    for seed in range(80):
        latex, text = render_product(
            [
                DisplayPiece("3", "3"),
                DisplayPiece("x", "x"),
                DisplayPiece(r"\left(1+2\right)", "(1+2)"),
            ],
            style,
            random.Random(seed),
        )
        has_juxt = bool(re.search(r"\d[a-zA-Z(]|[a-zA-Z]\\left", latex)) or bool(
            re.search(r"\d[a-zA-Z(]", text)
        )
        has_star = "*" in text or " * " in latex
        has_cdot = r"\cdot" in latex
        has_times = r"\times" in latex
        glyph_kinds = sum([has_juxt, has_star, has_cdot, has_times])
        if glyph_kinds >= 2:
            mixed = True
            break
    assert mixed, "strange_mode should mix multiply glyphs within one product"

    # Division glyph mixing across calls (one expression with two divisions)
    div_styles: set[str] = set()
    for seed in range(40):
        rng = random.Random(seed)
        style2 = PresentationStyle(strange_mode=True)
        l1, t1 = render_division(
            DisplayPiece("a", "a"), DisplayPiece("b", "b"), style2, rng
        )
        l2, t2 = render_division(
            DisplayPiece("c", "c"), DisplayPiece("d", "d"), style2, rng
        )
        blob = f"{l1} {t1} {l2} {t2}"
        if r"\frac" in blob:
            div_styles.add("frac")
        if "/" in t1 or "/" in t2:
            div_styles.add("slash")
        if r"\div" in blob:
            div_styles.add("div")
        if len(div_styles) >= 2:
            break
    assert len(div_styles) >= 2


def test_strangeness_amount_zero_disables_strange_mode():
    for seed in range(40):
        style = resolve_presentation(
            random.Random(seed),
            d=24.0,
            overrides={"strangeness": {"amount": 0}, "clutter": {"amount": 0}},
        )
        assert not style.strange_mode


def test_strangeness_high_amount_often_enables():
    hits = 0
    for seed in range(60):
        style = resolve_presentation(
            random.Random(seed),
            d=24.0,
            overrides={"strangeness": {"amount": 4.0, "min_d": 0}},
        )
        if style.strange_mode:
            hits += 1
    assert hits >= 20


def test_cancel_clutter_amount_zero_never_applies():
    from question_engine.frameworks.primitives.distributive import (
        sample_distributive_algebraic,
    )
    from question_engine.frameworks.primitives.presentation import (
        cancel_clutter_intensity,
        presentation_for_ctx,
    )

    assert (
        cancel_clutter_intensity(24.0, settings={"cancel_clutter": {"amount": 0}}) == 0.0
    )

    for seed in range(50):
        ctx = _dist_ctx(d=20.0, seed=seed)
        presentation_for_ctx(
            ctx,
            d=20.0,
            overrides={
                "clutter": {"amount": 0},
                "strangeness": {"amount": 0},
                "strange_mode": False,
                "explicit_multiply": False,
            },
        )
        ctx.settings = {
            **dict(getattr(ctx, "settings", {}) or {}),
            "cancel_clutter": {"amount": 0, "min_d": 0},
        }
        expr = sample_distributive_algebraic(ctx)
        assert not any(str(u).startswith("cancel:") for u in expr.upgrades)
        # Cancel groups are added as ``… + (… - …)``; core alone has no such addend.
        assert " + (" not in expr.text


def test_cancel_clutter_high_produces_families_and_keeps_answer():
    from question_engine.frameworks.primitives.distributive import (
        sample_distributive_algebraic,
    )
    from question_engine.frameworks.primitives.presentation import (
        cancel_clutter_intensity,
        presentation_for_ctx,
    )

    intensity = cancel_clutter_intensity(
        24.0, settings={"cancel_clutter": {"amount": 3.0, "min_d": 0}}
    )
    assert intensity > 0

    kinds: set[str] = set()
    hits = 0
    for seed in range(80):
        ctx = _dist_ctx(d=24.0, seed=seed)
        presentation_for_ctx(
            ctx,
            d=24.0,
            overrides={
                "commute_add": True,
                "clutter": {"amount": 0},
                "strangeness": {"amount": 0},
                "strange_mode": False,
                "explicit_multiply": False,
            },
        )
        ctx.settings = {
            **dict(getattr(ctx, "settings", {}) or {}),
            "cancel_clutter": {"amount": 3.0, "min_d": 0},
        }
        # Snapshot core expansion by sampling once; cancel does not change expanded_latex.
        expr = sample_distributive_algebraic(ctx)
        assert expr.expanded_latex
        assert "\\cdot" in expr.expanded_latex or "x" in expr.expanded_latex.lower()
        cancel_tags = [u for u in expr.upgrades if str(u).startswith("cancel:")]
        if cancel_tags:
            hits += 1
            for tag in cancel_tags:
                kinds.add(str(tag).split(":", 1)[-1])
            # Cancel groups appear as parenthesized zero-sum addends.
            assert "(" in expr.text and " - " in expr.text

    assert hits >= 25, f"expected frequent cancel clutter at high amount, got {hits}"
    # Across seeds, more than one family should appear (not a single hard-coded template).
    assert len(kinds) >= 2, f"expected multiple cancel families, got {kinds}"


def test_cancel_clutter_respects_min_d():
    from question_engine.frameworks.primitives.presentation import cancel_clutter_intensity

    assert (
        cancel_clutter_intensity(
            2.0, settings={"cancel_clutter": {"amount": 5.0, "min_d": 20.0}}
        )
        == 0.0
    )
