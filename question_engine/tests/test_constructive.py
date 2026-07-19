"""Answer-first constructive generation (L1–L4) through PFD."""

from __future__ import annotations

import random
from fractions import Fraction

from question_engine.frameworks.primitives.constructive import (
    AffineTarget,
    NumericTarget,
    construct_affine,
    construct_numeric,
    construct_pfd,
    construct_rational_sum,
    verify_affine,
    verify_numeric,
    verify_pfd_combine,
)
from question_engine.frameworks.primitives.registry import (
    PRIM_EXPAND_SIMPLIFY,
    PRIM_NUMBERS,
    PRIM_OOO,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.generators.primitive_rational import (
    partial_fraction_decomposition,
    rational_add_subtract,
    rational_simplify,
)


def _ctx(d: float = 8.0):
    return build_context(
        {
            "difficulty": d,
            "integers_only": True,
            "only_x": True,
            "lock_variable": "x",
        },
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_OOO, PRIM_EXPAND_SIMPLIFY],
        rng=random.Random(0),
    )


def test_construct_numeric_hits_target():
    ctx = _ctx(10)
    for seed in range(12):
        ctx.rng = random.Random(seed)
        tgt = NumericTarget(value=Fraction(seed % 7 - 3))
        surface = construct_numeric(ctx, d=10, target=tgt)
        assert verify_numeric(surface, tgt)
        assert surface.value == tgt.value
        # seed + at least the D-gated inflator budget (may be 1 at D=10)
        assert "seed" in surface.inflators_applied


def test_expand_simplify_classroom_quality():
    """Low/mid D prompts must look like real expand work — no trivial cancel noise."""
    from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs
    from question_engine.generators import GENERATORS

    reload_knobs()
    bad = 0
    for d, seeds in [(0, 20), (5, 20), (8, 20)]:
        qs = GENERATORS["expand_simplify"](
            "expand_simplify",
            {
                "difficulty": d,
                "count": seeds,
                "seed": 11,
                "integers_only": True,
                "only_x": True,
            },
        )
        for q in qs:
            blob = (q.prompt_latex or "") + (q.prompt_text or "")
            # Trivial cancel pairs
            if " - " in blob and any(
                f"{k}x - {k}x" in blob.replace(" ", "")
                or f"{k}x-{k}x" in blob.replace(" ", "")
                for k in range(1, 10)
            ):
                bad += 1
            # Copy-equation no-sol pattern shouldn't appear in expand
            assert "=" not in (q.prompt_latex or "")
            if d == 0:
                assert "(" in (q.prompt_text or "") or "\\left(" in (q.prompt_latex or "")
    assert bad == 0


def test_construct_affine_hits_target():
    ctx = _ctx(8)
    tgt = AffineTarget(a=Fraction(3), b=Fraction(-2))
    surface = construct_affine(ctx, d=8, target=tgt)
    assert verify_affine(surface, tgt)
    assert surface.simplified_latex


def test_construct_affine_distributive_scope():
    """prefer_distributive_factorization → factored form; cancel off by default."""
    from question_engine.frameworks.primitives.constructive import ExpressionScope

    forms: set[str] = set()
    for seed in range(30):
        ctx = _ctx(6)
        ctx.rng = random.Random(seed)
        ctx.settings = {"cancel_clutter": {"amount": 0, "min_d": 0}}
        surface = construct_affine(
            ctx,
            d=6,
            scope=ExpressionScope(
                max_degree=1,
                allow_cancel_clutter=True,
                prefer_distributive_factorization=True,
            ),
        )
        assert verify_affine(surface, surface.target)
        form = surface.metadata.get("distributive_form")
        assert form in {"var_outer", "const_outer"}
        forms.add(str(form))
        assert surface.metadata.get("expanded_distributive_latex")
        assert not any(str(u).startswith("cancel:") for u in surface.inflators_applied)
        # Factored look: product of factor and paren group
        assert "(" in surface.text
    assert forms == {"var_outer", "const_outer"}


def test_construct_affine_cancel_clutter_opt_in():
    from question_engine.frameworks.primitives.constructive import ExpressionScope

    hits = 0
    for seed in range(60):
        ctx = _ctx(24)
        ctx.rng = random.Random(seed)
        ctx.settings = {"cancel_clutter": {"amount": 3.0, "min_d": 0}}
        surface = construct_affine(
            ctx,
            d=24,
            scope=ExpressionScope(
                max_degree=1,
                allow_cancel_clutter=True,
                prefer_distributive_factorization=True,
            ),
        )
        assert verify_affine(surface, surface.target)
        if any(str(u).startswith("cancel:") for u in surface.inflators_applied):
            hits += 1
            assert " + (" in surface.text or surface.text.startswith("(")
    assert hits >= 15


def test_rational_add_and_simplify_smoke():
    ctx = _ctx(6)
    add = construct_rational_sum(ctx, d=6, cancel_count=0)
    assert add.level == "L3"
    assert "+" in add.latex or add.latex.count(r"\frac") >= 2
    assert add.simplified_latex

    simp = construct_rational_sum(ctx, d=8, cancel_count=1)
    assert simp.level == "L2"
    assert simp.metadata.get("cancel_plan", {}).get("cancel_count", 0) >= 1


def test_pfd_seed_then_combine():
    ctx = _ctx(6)
    surface = construct_pfd(ctx, d=6)
    assert surface.level == "L4"
    assert verify_pfd_combine(surface)
    assert r"\frac" in surface.latex
    assert "+" in surface.simplified_latex or surface.simplified_latex.count(r"\frac") >= 2


def test_generators_wire_rational_and_pfd():
    qs = rational_add_subtract(
        "rational_expression_simplification",
        {"count": 2, "include_answer_key": True, "difficulty": 5, "integers_only": True},
    )
    assert len(qs) == 2
    assert qs[0].answer_latex

    qs2 = rational_simplify(
        "rational_simplification",
        {"count": 1, "include_answer_key": True, "difficulty": 7, "integers_only": True},
    )
    assert qs2[0].metadata.get("level") in {"L2", "L3"}

    qs3 = partial_fraction_decomposition(
        "pc_partial_fraction_decomposition",
        {"count": 2, "include_answer_key": True, "difficulty": 6, "only_x": True},
    )
    assert "Decompose" in qs3[0].prompt_text
    assert qs3[0].answer_latex


def test_recursive_disguise_can_nest_numeric_blocks():
    """With recurse enabled, high-D numeric construction may nest recurse tags."""
    from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs

    reload_knobs()
    hits = 0
    for seed in range(40):
        ctx = build_context(
            {
                "difficulty": 16,
                "integers_only": True,
                "only_x": True,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_OOO],
            rng=random.Random(seed),
        )
        surface = construct_numeric(ctx, d=16, target=NumericTarget(value=Fraction(5)))
        assert verify_numeric(surface, surface.target)
        assert surface.value == Fraction(5)
        if any(t.startswith("recurse:") for t in surface.inflators_applied):
            hits += 1
            assert "\\left(" in surface.latex or "(" in surface.latex
    assert hits >= 1, "expected at least one recursive disguise across seeds"


def test_recursive_affine_still_verifies():
    ctx = _ctx(14)
    tgt = AffineTarget(a=Fraction(2), b=Fraction(3))
    for seed in range(20):
        ctx.rng = random.Random(seed)
        surface = construct_affine(ctx, d=14, target=tgt)
        assert verify_affine(surface, tgt)


def _force_recurse_at_depth(_ctx, _d, depth, _parent, *, max_depth: int = 2) -> bool:
    """Test helper: always recurse until max_depth (avoids infinite nesting)."""
    return depth < max_depth


def test_l2_cancel_recurse_appears_in_prompt(monkeypatch):
    """Forced L2 recurse must change the student prompt and keep metadata honest."""
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._should_recurse",
        _force_recurse_at_depth,
    )
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._pick_child_kind",
        lambda _ctx, _parent: "L1_numeric",
    )
    ctx = _ctx(10)
    forced = construct_rational_sum(ctx, d=10, cancel_count=1)
    assert forced.level == "L2"
    assert any(t.startswith("recurse:") for t in forced.inflators_applied)
    assert forced.metadata.get("recurse_hits", 0) >= 1
    assert "\\left(" in forced.latex
    assert forced.simplified_latex


def test_l3_sum_recurse_can_nest_blocks(monkeypatch):
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._should_recurse",
        _force_recurse_at_depth,
    )
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._pick_child_kind",
        lambda _ctx, _parent: "L1_numeric",
    )
    ctx = _ctx(8)
    surface = construct_rational_sum(ctx, d=8, cancel_count=0)
    assert surface.level == "L3"
    assert any(t.startswith("recurse:") for t in surface.inflators_applied)
    assert surface.metadata.get("recurse_hits", 0) >= 1
    assert "\\left(" in surface.latex or "(" in surface.latex


def test_l4_pfd_recurse_not_noop(monkeypatch):
    """L4 recurse must nest into the prompt (no pass stub) and still verify."""
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._should_recurse",
        _force_recurse_at_depth,
    )
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._pick_child_kind",
        lambda _ctx, _parent: "L1_numeric",
    )
    ctx = _ctx(8)
    surface = construct_pfd(ctx, d=8)
    assert surface.level == "L4"
    assert verify_pfd_combine(surface)
    assert any(t.startswith("recurse:L1_") for t in surface.inflators_applied)
    assert surface.metadata.get("recurse_hits", 0) >= 1
    assert "\\left(" in surface.latex
    # Answer key stays a clean PF sum
    assert surface.simplified_latex.count(r"\frac") >= 2


def _assert_no_bare_left_right(latex: str) -> None:
    """KaTeX shows literal 'left'/'right' when \\\\left / bare left leak into latex."""
    # Double-escaped TeX: string contains \\left (two backslashes) → renders as word "left"
    assert r"\\left" not in latex
    assert r"\\right" not in latex
    # Strip valid commands; leftover word tokens must not remain
    stripped = latex.replace(r"\left", "").replace(r"\right", "")
    assert "left" not in stripped
    assert "right" not in stripped


def test_l4_pfd_latex_no_bare_left_right(monkeypatch):
    """L1_numeric disguise must emit \\left/\\right, never double-escaped or bare words."""
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._should_recurse",
        _force_recurse_at_depth,
    )
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._pick_child_kind",
        lambda _ctx, _parent: "L1_numeric",
    )
    for seed in range(8):
        ctx = _ctx(10)
        ctx.rng = random.Random(seed)
        surface = construct_pfd(ctx, d=10)
        assert any(t.startswith("recurse:L1_numeric") for t in surface.inflators_applied)
        assert r"\left(" in surface.latex
        assert r"\right)" in surface.latex
        _assert_no_bare_left_right(surface.latex)
        _assert_no_bare_left_right(surface.simplified_latex or "")


def test_l4_pfd_affine_recurse(monkeypatch):
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._should_recurse",
        _force_recurse_at_depth,
    )
    monkeypatch.setattr(
        "question_engine.frameworks.primitives.constructive._pick_child_kind",
        lambda _ctx, _parent: "L1_affine",
    )
    ctx = _ctx(10)
    surface = construct_pfd(ctx, d=10)
    assert verify_pfd_combine(surface)
    assert any(t.startswith("recurse:") for t in surface.inflators_applied)
    assert "\\left(" in surface.latex


def test_relatedness_knobs_only_list_l1_children():
    """Honesty: L2/L3/L4 relatedness lists only implemented L1 children."""
    from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs

    knobs = reload_knobs()
    allowed = knobs["constructive"]["recurse"]["allowed_child_levels"]
    for parent in ("L2_rational", "L3_rational_sum", "L4_pfd"):
        kids = set(allowed[parent])
        assert kids <= {"L1_numeric", "L1_affine"}
        assert "L1_numeric" in kids or "L1_affine" in kids
