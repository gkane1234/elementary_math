"""Answer-first constructive generation (L1–L4) through PFD."""

from __future__ import annotations

import random
from fractions import Fraction

from question_engine.frameworks.primitives.constructive import (
    AffineTarget,
    ExpressionScope,
    NumericTarget,
    PolynomialTarget,
    construct_affine,
    construct_numeric,
    construct_pfd,
    construct_poly,
    construct_rational_sum,
    seed_poly_target,
    verify_affine,
    verify_numeric,
    verify_pfd_combine,
    verify_poly,
)
from question_engine.frameworks.primitives.expression_policy import polynomial_policy
from question_engine.frameworks.primitives.poly_helpers import poly_degree
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


def _poly_ctx(d: float = 8.0, *, max_degree: int = 3):
    return build_context(
        {
            "difficulty": d,
            "integers_only": True,
            "only_x": True,
            "lock_variable": "x",
            "max_degree": max_degree,
        },
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_OOO, PRIM_EXPAND_SIMPLIFY],
        rng=random.Random(0),
        policy=polynomial_policy(max_degree=max_degree),
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


def test_construct_poly_hits_target():
    ctx = _poly_ctx(8, max_degree=3)
    tgt = PolynomialTarget.from_dict({2: Fraction(3), 0: Fraction(-2)})
    surface = construct_poly(
        ctx,
        d=8,
        target=tgt,
        scope=ExpressionScope(max_degree=3),
    )
    assert verify_poly(surface, tgt)
    assert surface.poly_coeffs == tgt.coeffs_dict()
    assert surface.simplified_latex
    assert surface.metadata.get("poly_degree") == 2


def test_construct_poly_degree_respected():
    """Seeded / inflated degree stays within scope.max_degree and ≥ 2."""
    for max_deg, d in ((2, 0), (2, 5), (3, 10), (4, 15)):
        for seed in range(12):
            ctx = _poly_ctx(d, max_degree=max_deg)
            ctx.rng = random.Random(seed)
            surface = construct_poly(
                ctx,
                d=d,
                scope=ExpressionScope(max_degree=max_deg),
            )
            assert verify_poly(surface, surface.target)
            deg = int(surface.metadata["poly_degree"])
            assert 2 <= deg <= max_deg
            assert poly_degree(surface.poly_coeffs or {}) == deg
            blob = surface.latex + (surface.simplified_latex or "")
            assert f"^{{{deg}}}" in blob or "^" in blob


def test_construct_poly_single_and_multi_hot():
    single_hits = 0
    multi_hits = 0
    for seed in range(40):
        ctx = _poly_ctx(10, max_degree=4)
        ctx.rng = random.Random(seed)
        single = construct_poly(
            ctx,
            d=10,
            scope=ExpressionScope(max_degree=4, prefer_single_hot=True),
        )
        assert verify_poly(single, single.target)
        assert single.metadata.get("n_hot_terms") == 1
        single_hits += 1

        ctx.rng = random.Random(seed + 100)
        multi = construct_poly(
            ctx,
            d=10,
            scope=ExpressionScope(max_degree=4, prefer_single_hot=False),
        )
        assert verify_poly(multi, multi.target)
        assert multi.metadata.get("n_hot_terms", 0) >= 1
        if multi.metadata.get("n_hot_terms", 0) >= 2:
            multi_hits += 1
    assert single_hits == 40
    assert multi_hits >= 8


def test_construct_poly_rejects_low_scope():
    ctx = _poly_ctx(5)
    try:
        construct_poly(ctx, d=5, scope=ExpressionScope(max_degree=1))
        assert False, "expected ValueError"
    except ValueError as e:
        assert "max_degree" in str(e)


def test_seed_poly_target_honors_degree_cap():
    ctx = _poly_ctx(12, max_degree=3)
    for seed in range(20):
        ctx.rng = random.Random(seed)
        tgt = seed_poly_target(ctx, max_degree=3, d=12)
        assert 2 <= tgt.degree <= 3


def test_construct_poly_samples_at_d_levels_print():
    """Print real latex at D=0,5,10,15 proving degree ≥ 2 appears."""
    examples: list[str] = []
    for d in (0, 5, 10, 15):
        ctx = _poly_ctx(d, max_degree=4)
        ctx.rng = random.Random(d * 17 + 3)
        surface = construct_poly(
            ctx,
            d=d,
            scope=ExpressionScope(max_degree=4),
        )
        assert verify_poly(surface, surface.target)
        deg = surface.metadata["poly_degree"]
        assert deg >= 2
        line = (
            f"D={d}: prompt={surface.latex}  "
            f"simp={surface.simplified_latex}  "
            f"deg={deg} hot={surface.metadata.get('n_hot_terms')} "
            f"inflators={surface.inflators_applied}"
        )
        examples.append(line)
        print(line)
        assert "^" in surface.simplified_latex or "^" in surface.latex
    assert len(examples) == 4


def test_simplify_polynomials_generator_smoke():
    """Live path: simplify_polynomials yields degree≥2 stems that verify."""
    from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs
    from question_engine.generators import GENERATORS

    reload_knobs()
    gen = GENERATORS["simplify_polynomials"]
    for d in (0, 5, 10, 15, 20):
        qs = gen(
            "simplify_polynomials",
            {
                "difficulty": d,
                "count": 6,
                "seed": 42 + d,
                "integers_only": True,
                "only_x": True,
                "include_answer_key": True,
                "max_degree": 4,
            },
        )
        assert len(qs) == 6
        for q in qs:
            assert q.prompt_latex
            assert q.answer_latex
            assert "=" not in (q.prompt_latex or "")
            meta = q.metadata or {}
            assert meta.get("primitive_engine") == "construct_poly"
            assert int(meta.get("poly_degree") or 0) >= 2
            if d > 0:
                # Surface should differ from standard form after inflation
                # (compare post-normalization, matching Question.__post_init__).
                from packages.polynomial_core import normalize_expression_signs

                p = normalize_expression_signs(q.prompt_latex or "").replace(" ", "")
                a = normalize_expression_signs(q.answer_latex or "").replace(" ", "")
                assert p != a
            print(
                f"D={d}: {q.prompt_latex}  ->  {q.answer_latex}  "
                f"(deg={meta.get('poly_degree')} hot={meta.get('n_hot_terms')})"
            )


def test_construct_poly_compose_nests_and_verifies():
    """Budget > 1 accumulates compose tags; surface still ≡ target."""
    from fractions import Fraction

    tgt = PolynomialTarget.from_dict(
        {2: Fraction(3), 1: Fraction(4), 0: Fraction(5)},
        single_hot=False,
    )
    nested = 0
    for seed in range(30):
        ctx = _poly_ctx(20, max_degree=3)
        ctx.rng = random.Random(seed)
        surface = construct_poly(
            ctx,
            d=20,
            target=tgt,
            min_inflators=4,
            scope=ExpressionScope(max_degree=3, prefer_single_hot=False),
        )
        assert verify_poly(surface, tgt)
        assert surface.metadata.get("compose") is True
        compose_tags = [t for t in surface.inflators_applied if str(t).startswith("compose:")]
        if len(compose_tags) >= 2:
            nested += 1
        # Not just a bare standard-form render of the target
        assert surface.latex != surface.simplified_latex or compose_tags
    assert nested >= 10


def test_construct_poly_level_bias_prefers_root():
    """Over many samples, more compose hits at depth 0 than deeper levels."""
    root_hits = 0
    deep_hits = 0
    for seed in range(80):
        ctx = _poly_ctx(25, max_degree=4)
        ctx.rng = random.Random(seed)
        surface = construct_poly(
            ctx,
            d=25,
            min_inflators=5,
            scope=ExpressionScope(max_degree=4),
        )
        assert verify_poly(surface, surface.target)
        counts = surface.metadata.get("compose_depth_counts") or {}
        root_hits += int(counts.get("0", 0))
        for k, v in counts.items():
            if str(k) != "0":
                deep_hits += int(v)
    assert root_hits > 0
    # With level_bias=0.5, root should dominate when deep nodes exist
    assert root_hits >= deep_hits


def test_construct_poly_compose_gallery_print():
    """Large gallery at many D bands — prompt → answer."""
    bands = (0, 3, 5, 8, 10, 15, 20, 25, 50)
    for d in bands:
        print(f"\n=== D={d} ===")
        for i in range(5):
            ctx = _poly_ctx(d, max_degree=4)
            ctx.rng = random.Random(d * 100 + i * 17 + 3)
            surface = construct_poly(
                ctx,
                d=d,
                min_inflators=(0 if d <= 0 else 1),
                scope=ExpressionScope(max_degree=4),
            )
            assert verify_poly(surface, surface.target)
            depths = surface.metadata.get("compose_depth_counts")
            print(
                f"  [{i}] {surface.latex}  ->  {surface.simplified_latex}  "
                f"depths={depths} tags={[t for t in surface.inflators_applied if str(t).startswith('compose:')][:6]}"
            )


def test_simplify_polynomials_constrained_course_targets():
    """PA/A2 thin variants: particular PolynomialTarget constraints only."""
    from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs
    from question_engine.generators import GENERATORS

    reload_knobs()
    gen = GENERATORS["simplify_polynomials"]

    print("\n=== PA simplifying (deg=2, max_terms=3) ===")
    for d in (0, 5, 10, 15):
        qs = gen(
            "pa_polynomials_simplifying",
            {
                "difficulty": d,
                "count": 4,
                "seed": 100 + d,
                "integers_only": True,
                "only_x": True,
                "include_answer_key": True,
                "max_degree": 2,
                "min_degree": 2,
                "max_terms": 3,
                "prefer_single_hot": True,
            },
        )
        for q in qs:
            meta = q.metadata or {}
            deg = int(meta.get("poly_degree") or 0)
            n_terms = int(meta.get("n_terms") or 0)
            assert deg == 2
            assert 1 <= n_terms <= 3
            print(f"  D={d}: {q.prompt_latex} -> {q.answer_latex} (terms={n_terms})")

    print("\n=== A2 simplifying (max_degree=5, multi-hot) ===")
    for d in (0, 10, 20):
        qs = gen(
            "a2_polynomial_functions_simplifying",
            {
                "difficulty": d,
                "count": 4,
                "seed": 200 + d,
                "integers_only": True,
                "only_x": True,
                "include_answer_key": True,
                "max_degree": 5,
                "prefer_single_hot": False,
            },
        )
        for q in qs:
            meta = q.metadata or {}
            deg = int(meta.get("poly_degree") or 0)
            assert 2 <= deg <= 5
            print(
                f"  D={d}: {q.prompt_latex} -> {q.answer_latex} "
                f"(deg={deg} hot={meta.get('n_hot_terms')} terms={meta.get('n_terms')})"
            )


def test_rational_add_and_simplify_smoke():
    ctx = _ctx(6)
    add = construct_rational_sum(ctx, d=6, cancel_count=0, as_sum=True)
    assert add.level == "L3"
    assert "+" in add.latex or add.latex.count(r"\frac") >= 2
    assert add.simplified_latex
    assert add.metadata.get("cancel_factor_count") == 0

    simp = construct_rational_sum(ctx, d=8, cancel_count=1, as_sum=False)
    assert simp.level == "L2"
    assert simp.metadata.get("cancel_plan", {}).get("cancel_count", 0) >= 1


def test_rational_cancel_counts_l2_and_l3():
    ctx = _ctx(12)
    for k in (0, 1, 2, 3, 4):
        simp = construct_rational_sum(ctx, d=12, cancel_count=k, as_sum=False)
        assert simp.level == "L2"
        assert simp.metadata.get("cancel_factor_count") == k
        add = construct_rational_sum(ctx, d=12, cancel_count=k, as_sum=True)
        assert add.level == "L3"
        assert add.metadata.get("cancel_factor_count") == k
        assert add.latex.count(r"\frac") >= 2 or "+" in add.latex


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
    surface = construct_rational_sum(ctx, d=8, cancel_count=0, as_sum=True)
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
        assert kids <= {"L1_numeric", "L1_affine", "L1_poly"}
        assert "L1_numeric" in kids or "L1_affine" in kids
    assert "L1_poly" in allowed
    assert set(allowed["L1_poly"]) <= {"L1_poly", "L1_affine", "L1_numeric"}
