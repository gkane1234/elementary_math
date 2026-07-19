"""Tests for continuous difficulty budget + Layer 0 primitives + PrimitiveContext."""

from __future__ import annotations

import random

import pytest

from question_engine.frameworks.difficulty_budget import (
    DifficultyFactor,
    allocate_budget,
    clamp_difficulty,
    degrade_drop_most_expensive,
    select_upgrades,
    settings_difficulty,
)
from question_engine.frameworks.primitives import (
    PRIM_DISTRIBUTIVE,
    PRIM_EQUATIONS,
    PRIM_EVALUATE,
    PRIM_NUMBERS,
    PRIM_OOO,
    PRIM_VARIABLE,
    build_context,
    resolve_primitive,
    sample_number,
    sample_variable,
)
from question_engine.frameworks.primitives.numbers import (
    DECIMAL_LANES,
    FRACTION_LANES,
    INTEGER_LANES,
    LANE_MIN_D,
    NUMBER_PROFILES,
    eligible_lanes,
    resolve_constraints,
    select_lane,
)
from question_engine.frameworks.primitives.variables import (
    LANE_MIN_D as VAR_LANE_MIN_D,
    LANE_POOLS,
    VARIABLE_LANES,
    eligible_variable_lanes,
    resolve_variable_constraints,
    select_variable_lane,
)


def test_clamp_and_legacy_tier_shim():
    assert clamp_difficulty(-1) == 0.0
    assert clamp_difficulty(100) == 100.0
    assert clamp_difficulty(100, d_max=24) == 24.0
    assert settings_difficulty({"difficulty": 7.5}) == 7.5
    assert settings_difficulty({"difficulty_tier": "easy"}) == 3.0
    assert settings_difficulty({"difficulty_tier": "hard"}) == 14.0


def test_parse_optional_prereq_cap_none_sentinels():
    from question_engine.frameworks.difficulty_budget import parse_optional_prereq_cap

    for sentinel in (None, "", "  ", "none", "uncapped", "unlimited", float("nan"), float("inf")):
        assert parse_optional_prereq_cap(sentinel) is None
    assert parse_optional_prereq_cap(0) == 0.0
    assert parse_optional_prereq_cap("3.5") == 3.5
    assert parse_optional_prereq_cap(-2) == 0.0


def test_default_prereq_caps_are_uncapped():
    """Schema defaults and empty flat keys must not apply a hidden 24-style ceiling."""
    from question_engine.settings.domains.common import primitive_layered_settings

    fields = primitive_layered_settings(primitive_ids=["numbers", "ooo"])
    cap_fields = [f for f in fields if f.key.startswith("prereq_cap_")]
    assert cap_fields
    for field in cap_fields:
        assert field.default == ""
        assert field.max is None

    ctx = build_context(
        {"difficulty": 100, "prereq_cap_numbers": "", "prereq_cap_ooo": None},
        ["numbers", "ooo"],
        rng=random.Random(0),
    )
    # No finite caps → full topic D allocated; layer ceilings are topic_d, not 24.
    assert sum(ctx.plan.to_spend_dict().values()) == pytest.approx(100.0)
    for layer in ctx.plan.layers:
        assert layer.cap == pytest.approx(100.0)


def test_allocate_preserves_high_topic_d():
    ids = [PRIM_NUMBERS, PRIM_OOO]
    plan = allocate_budget(100.0, ids, rng=random.Random(0))
    assert plan.topic_d == 100.0
    assert plan.effective_for(PRIM_NUMBERS) + plan.effective_for(PRIM_OOO) == pytest.approx(
        100.0
    )


def test_allocate_prefers_downstream_on_average():
    ids = [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_OOO, PRIM_DISTRIBUTIVE]
    number_eff = []
    late_eff = []
    for seed in range(80):
        plan = allocate_budget(12.0, ids, rng=random.Random(seed))
        number_eff.append(plan.effective_for(PRIM_NUMBERS))
        late_eff.append(plan.effective_for(PRIM_DISTRIBUTIVE))
    assert sum(late_eff) / len(late_eff) > sum(number_eff) / len(number_eff)


def test_caps_clamp_effective():
    ids = [PRIM_NUMBERS, PRIM_OOO]
    plan = allocate_budget(
        20.0,
        ids,
        prereq_caps={PRIM_NUMBERS: 2.0, PRIM_OOO: 20.0},
        rng=random.Random(0),
    )
    assert plan.effective_for(PRIM_NUMBERS) <= 2.0 + 1e-9


def test_select_upgrades_priority_and_degrade():
    upgrades = [
        DifficultyFactor("a", 1),
        DifficultyFactor("b", 2),
        DifficultyFactor("c", 5),
    ]
    bought, rem, _ = select_upgrades(upgrades, 3.0, rng=random.Random(0))
    assert [f.id for f in bought] == ["a", "b"]
    assert rem == pytest.approx(0.0)
    kept, dropped = degrade_drop_most_expensive(bought)
    assert dropped == "b"
    assert [f.id for f in kept] == ["a"]


def test_friendly_wholes_never_fraction():
    for seed in range(30):
        n = sample_number(
            8.0,
            settings={"number_profile": "friendly_wholes"},
            rng=random.Random(seed),
        )
        assert n.value.denominator == 1
        assert n.value >= 0


def test_variable_lock_and_x_default():
    v = sample_variable(10.0, settings={"lock_variable": "y"}, rng=random.Random(0))
    assert v.name == "y" and v.locked
    assert v.lane is not None and v.lane.source == "lock"
    v2 = sample_variable(0.0, settings={"allow_other_letters": True}, rng=random.Random(1))
    assert v2.name == "x"
    assert v2.profile == "only_x"
    # Legacy allow_other_letters=False forces only_x even at high D
    for seed in range(20):
        v3 = sample_variable(
            14.0,
            settings={"allow_other_letters": False},
            rng=random.Random(seed),
        )
        assert v3.name == "x" and v3.profile == "only_x"


def test_d_drives_variable_lane_eligibility():
    default = resolve_variable_constraints({})
    assert eligible_variable_lanes(0.0, default) == ["only_x"]
    assert eligible_variable_lanes(2.0, default) == ["only_x"]
    assert eligible_variable_lanes(3.0, default) == ["only_x", "xyz"]
    mid = eligible_variable_lanes(6.0, default)
    assert mid == ["only_x", "xyz", "abctuvwxyz"]
    high = set(eligible_variable_lanes(10.0, default))
    assert "whole_alphabet" in high
    assert "greek" not in high
    top = set(eligible_variable_lanes(12.0, default))
    assert "greek" in top
    for lid, min_d in VAR_LANE_MIN_D.items():
        assert lid in eligible_variable_lanes(min_d, default)
        if min_d > 0:
            assert lid not in eligible_variable_lanes(min_d - 0.01, default)


def test_variable_constraints_filter_lanes():
    only = resolve_variable_constraints({"only_x": True})
    assert eligible_variable_lanes(14.0, only) == ["only_x"]

    no_greek = resolve_variable_constraints({"allow_greek": False})
    pool = eligible_variable_lanes(14.0, no_greek)
    assert "greek" not in pool
    assert "whole_alphabet" in pool

    capped = resolve_variable_constraints({"max_variable_lane": "xyz"})
    assert eligible_variable_lanes(14.0, capped) == ["only_x", "xyz"]


def test_higher_d_admits_harder_variable_lanes():
    seen_high: set[str] = set()
    for seed in range(80):
        v = sample_variable(14.0, settings={}, rng=random.Random(seed))
        seen_high.add(v.profile)
        assert v.name in LANE_POOLS[v.profile]
        assert v.latex
        assert v.lane is not None and v.lane.source == "auto"
    assert "greek" in seen_high or "whole_alphabet" in seen_high

    seen_low: set[str] = set()
    for seed in range(40):
        v = sample_variable(1.0, settings={}, rng=random.Random(seed))
        seen_low.add(v.profile)
        assert v.name == "x"
    assert seen_low == {"only_x"}


def test_force_variable_lane_override():
    lane = select_variable_lane(
        0.0,
        settings={"variable_lane": "greek", "only_x": True},
        rng=random.Random(0),
    )
    assert lane.source == "force"
    assert lane.profile == "greek"

    v = sample_variable(
        0.0,
        settings={"force_variable_lane": "xyz"},
        rng=random.Random(1),
    )
    assert v.profile == "xyz"
    assert v.name in ("x", "y", "z")
    assert v.lane is not None and v.lane.source == "force"


def test_greek_samples_use_latex_commands():
    v = sample_variable(
        14.0,
        settings={"variable_lane": "greek"},
        rng=random.Random(0),
    )
    assert v.profile == "greek"
    assert v.latex.startswith("\\")
    assert v.name in LANE_POOLS["greek"]


def test_context_records_variable_lane():
    ctx = build_context(
        {"difficulty": 12, "prereq_cap_variable": 12},
        [PRIM_NUMBERS, PRIM_VARIABLE],
        rng=random.Random(7),
    )
    vars_ = [ctx.sample_variable() for _ in range(6)]
    meta = ctx.metadata()
    var_entries = [e for e in meta["sample_log"] if e.get("primitive") == PRIM_VARIABLE]
    assert len(var_entries) == 6
    assert all("lane" in e and "lane_selection" in e for e in var_entries)
    assert all(v.lane is not None for v in vars_)


@pytest.mark.parametrize("lane", VARIABLE_LANES)
def test_all_variable_lanes_sample(lane: str):
    v = sample_variable(5.0, settings={"variable_lane": lane}, rng=random.Random(0))
    assert v.profile == lane
    assert v.name in LANE_POOLS[lane]
    assert v.latex


def test_leaf_resolves_to_shared_primitive():
    assert resolve_primitive("order_of_operations") == PRIM_OOO
    assert resolve_primitive("g6_distributive_property_numeric") == PRIM_DISTRIBUTIVE
    assert resolve_primitive("foundations_math:whole_numbers") == PRIM_NUMBERS


def test_context_uniform_ceiling_across_instances():
    ctx = build_context(
        {
            "difficulty": 10,
            "prereq_caps": {PRIM_NUMBERS: 3, PRIM_VARIABLE: 0, PRIM_OOO: 10},
            "prereq_settings": {
                PRIM_NUMBERS: {"number_profile": "friendly_wholes"},
                PRIM_VARIABLE: {"lock_variable": "x"},
            },
        },
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_OOO],
        rng=random.Random(42),
    )
    assert ctx.effective_d(PRIM_NUMBERS) <= 3.0 + 1e-9
    assert ctx.effective_d(PRIM_VARIABLE) <= 0.0 + 1e-9
    nums = [ctx.sample_number() for _ in range(8)]
    for n in nums:
        assert n.profile == "friendly_wholes"
        assert n.effective_d <= 3.0 + 1e-9
        assert n.value.denominator == 1
        assert n.lane is not None and n.lane.source == "force"
    vars_ = [ctx.sample_variable() for _ in range(5)]
    assert all(v.name == "x" for v in vars_)
    meta = ctx.metadata()
    assert "spend" in meta and PRIM_NUMBERS in meta["spend"]
    assert any(
        "lane_selection" in e
        for e in meta["sample_log"]
        if e.get("primitive") == PRIM_NUMBERS
    )


@pytest.mark.parametrize("profile", NUMBER_PROFILES)
def test_all_profiles_sample(profile: str):
    n = sample_number(5.0, settings={"number_profile": profile}, rng=random.Random(0))
    assert n.profile == profile
    assert n.latex


def test_d_drives_lane_eligibility():
    default = resolve_constraints({})
    low = eligible_lanes(0.0, default)
    assert low == ["friendly_wholes", "signed_small"]
    mid = set(eligible_lanes(5.0, default))
    assert "unit_fractions" in mid
    assert "simple_rations" in mid
    assert "friendly_decimals" in mid
    assert "difficult_rations" not in mid
    high = set(eligible_lanes(10.0, default))
    assert "difficult_rations" in high
    assert "awkward_decimals" in high
    # Threshold table matches catalog mins
    for pid, min_d in LANE_MIN_D.items():
        assert pid in eligible_lanes(min_d, default)
        if min_d > 0:
            assert pid not in eligible_lanes(min_d - 0.01, default)


def test_integers_only_never_fractions_or_decimals():
    settings = {"integers_only": True}
    for d in (0, 4, 8, 12, 14):
        pool = eligible_lanes(d, resolve_constraints(settings))
        assert set(pool) <= INTEGER_LANES
        for seed in range(20):
            n = sample_number(
                float(d), settings=settings, rng=random.Random(seed + d * 31)
            )
            assert n.profile in INTEGER_LANES
            assert n.value.denominator == 1
            assert n.display == "integer"
            assert n.lane is not None and n.lane.source == "auto"


def test_no_decimals_and_no_fractions_constraints():
    no_dec = resolve_constraints({"allow_decimals": False})
    pool = eligible_lanes(12.0, no_dec)
    assert not (set(pool) & DECIMAL_LANES)
    assert set(pool) & FRACTION_LANES

    no_frac = resolve_constraints({"allow_fractions": False})
    pool2 = eligible_lanes(12.0, no_frac)
    assert not (set(pool2) & FRACTION_LANES)
    assert set(pool2) & DECIMAL_LANES


def test_higher_d_admits_harder_lanes_in_samples():
    """Across many auto draws, high D should sometimes pick difficult / awkward lanes."""
    seen_high: set[str] = set()
    for seed in range(60):
        n = sample_number(12.0, settings={}, rng=random.Random(seed))
        seen_high.add(n.profile)
    assert "difficult_rations" in seen_high or "awkward_decimals" in seen_high

    seen_low: set[str] = set()
    for seed in range(40):
        n = sample_number(1.0, settings={}, rng=random.Random(seed))
        seen_low.add(n.profile)
    assert seen_low <= {"friendly_wholes", "signed_small"}


def test_force_override_still_works():
    lane = select_lane(
        12.0,
        settings={"number_profile": "unit_fractions", "integers_only": True},
        rng=random.Random(0),
    )
    assert lane.source == "force"
    assert lane.profile == "unit_fractions"

    n = sample_number(
        12.0,
        settings={"force_number_profile": "awkward_decimals"},
        rng=random.Random(1),
    )
    assert n.profile == "awkward_decimals"
    assert n.lane is not None and n.lane.source == "force"


def test_auto_default_when_profile_auto():
    n = sample_number(0.0, settings={"number_profile": "auto"}, rng=random.Random(0))
    assert n.lane is not None and n.lane.source == "auto"
    assert n.profile in {"friendly_wholes", "signed_small"}


def test_allow_negatives_false_excludes_signed_small():
    pool = eligible_lanes(5.0, resolve_constraints({"allow_negatives": False}))
    assert "signed_small" not in pool
    assert "friendly_wholes" in pool
    for seed in range(25):
        n = sample_number(
            6.0,
            settings={"integers_only": True, "allow_negatives": False},
            rng=random.Random(seed),
        )
        assert n.value >= 0


def test_number_domain_integers_alias():
    c = resolve_constraints({"number_domain": "integers"})
    assert c.integers_only
    assert not c.allow_fractions and not c.allow_decimals


def test_ooo_and_distributive_generate():
    from question_engine.generators.primitive_g6 import (
        distributive_property,
        order_of_operations,
    )

    ooo = order_of_operations(
        "OOO",
        {
            "count": 3,
            "include_answer_key": True,
            "difficulty": 8,
            "integers_only": True,
            "prereq_cap_numbers": 4,
            "prereq_cap_ooo": 10,
        },
    )
    assert len(ooo) == 3
    assert all(q.answer_latex for q in ooo)
    assert "spend" in ooo[0].metadata

    dist = distributive_property(
        "Dist",
        {
            "count": 2,
            "include_answer_key": True,
            "difficulty": 5,
            "integers_only": True,
        },
    )
    assert len(dist) == 2
    # Instruction lives in catalog/metadata; stem is the expression only.
    assert all(
        "distributive" not in (q.prompt_text or "").lower()
        and "distributive" not in (q.prompt_latex or "").lower()
        for q in dist
    )
    assert all(q.prompt_latex.strip() for q in dist)
    # Metadata should record selected lanes
    log = dist[0].metadata.get("sample_log") or []
    number_entries = [e for e in log if e.get("primitive") == PRIM_NUMBERS]
    assert number_entries
    assert all("lane" in e for e in number_entries)


def test_layer1_primitives_generate_smoke():
    from question_engine.generators.primitive_g6 import (
        combining_like_terms,
        evaluate_algebraic_expressions,
        expand_then_simplify,
        factor_gcf,
        multi_step_equations,
        multi_step_inequalities,
        one_step_equations,
        one_step_inequalities,
        two_step_equations,
        two_step_inequalities,
    )

    base = {
        "count": 2,
        "include_answer_key": True,
        "difficulty": 6,
        "integers_only": True,
        "only_x": True,
    }
    builders = [
        (evaluate_algebraic_expressions, "evaluate"),
        (combining_like_terms, "like_terms"),
        (expand_then_simplify, "expand_simplify"),
        (one_step_equations, "equations"),
        (two_step_equations, "equations"),
        (multi_step_equations, "equations"),
        (one_step_inequalities, "inequalities"),
        (two_step_inequalities, "inequalities"),
        (multi_step_inequalities, "inequalities"),
        (factor_gcf, "factor_gcf"),
    ]
    for fn, engine in builders:
        qs = fn(engine, dict(base))
        assert len(qs) == 2
        assert all(q.answer_latex for q in qs)
        assert "spend" in qs[0].metadata
        assert qs[0].metadata.get("primitive_engine") == engine or engine in str(
            qs[0].metadata.get("primitive_engine")
        )


def test_layer1_constraints_integers_and_lock_x():
    from question_engine.generators.primitive_g6 import (
        combining_like_terms,
        evaluate_algebraic_expressions,
        one_step_equations,
    )

    settings = {
        "count": 4,
        "include_answer_key": True,
        "difficulty": 8,
        "integers_only": True,
        "lock_variable": "x",
        "prereq_cap_numbers": 4,
        "prereq_cap_variable": 0,
    }
    for fn in (evaluate_algebraic_expressions, combining_like_terms, one_step_equations):
        qs = fn("T", dict(settings))
        for q in qs:
            log = q.metadata.get("sample_log") or []
            vars_ = [e for e in log if e.get("primitive") == PRIM_VARIABLE]
            assert vars_
            assert all(e.get("name") == "x" for e in vars_)
            nums = [e for e in log if e.get("primitive") == PRIM_NUMBERS]
            assert nums
            assert "spend" in q.metadata


def test_equation_force_steps():
    from question_engine.generators.primitive_g6 import (
        one_step_equations,
        two_step_equations,
    )

    one = one_step_equations(
        "One",
        {"count": 5, "include_answer_key": True, "difficulty": 12, "integers_only": True},
    )
    assert all(q.metadata.get("steps") == "one" for q in one)
    two = two_step_equations(
        "Two",
        {"count": 5, "include_answer_key": True, "difficulty": 2, "integers_only": True},
    )
    assert all(q.metadata.get("steps") == "two" for q in two)


def test_leaf_resolves_layer1():
    assert resolve_primitive("g6_evaluating_algebraic_expressions") == "evaluate"
    assert resolve_primitive("g6_combining_like_terms") == "like_terms"
    assert resolve_primitive("one_step_equations") == "equations"
    assert resolve_primitive("two_step_inequalities") == "inequalities"
    assert resolve_primitive("polynomial_factoring_common_factor") == "factor_gcf"


def test_evaluate_linear_term_formula_unbounded():
    from question_engine.frameworks.primitives.evaluate import (
        DIV_UNLOCK,
        MUL_UNLOCK,
        TERM_SCALE,
        min_d_for_n_terms,
        op_pool_for_d,
        target_n_parens,
        target_n_terms,
    )

    # Mid-range feel: D≈0–3 → 1–2 terms
    assert target_n_terms(0) == 1
    assert target_n_terms(1.0) == 1
    assert target_n_terms(1.5) == 2
    assert target_n_terms(3.0) == 2
    assert target_n_terms(4.5) == 3
    assert target_n_terms(10.5) == 4

    # No hard cap — grows for arbitrarily large D
    assert target_n_terms(100) > target_n_terms(50) > target_n_terms(20)
    assert target_n_terms(1e6) >= 20

    # Inverse matches floors
    for n in range(1, 12):
        d = min_d_for_n_terms(n)
        assert target_n_terms(d) >= n
        if n > 1:
            assert target_n_terms(d - 1e-9) == n - 1

    assert TERM_SCALE == 1.5
    assert op_pool_for_d(0) == ("+", "-")
    assert "*" in op_pool_for_d(MUL_UNLOCK)
    assert "/" in op_pool_for_d(DIV_UNLOCK)
    assert target_n_parens(0) == 0
    assert target_n_parens(100) > target_n_parens(10)


def test_evaluate_linear_stays_affine_and_grows_terms():
    import re

    from question_engine.frameworks.primitives import PRIM_EVALUATE, build_context
    from question_engine.frameworks.primitives.evaluate import (
        sample_evaluate_expression,
        target_n_terms,
    )

    def _ctx(topic_d: float, seed: int):
        return build_context(
            {
                "difficulty": topic_d,
                "integers_only": True,
                "lock_variable": "x",
                "prereq_cap_numbers": 0.5,
                "prereq_cap_variable": 0,
                "prereq_cap_evaluate": 24,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EVALUATE],
            rng=random.Random(seed),
        )

    for d, seed in [(0, 1), (5, 2), (10, 3), (20, 4), (24, 5)]:
        for s in range(seed, seed + 8):
            expr = sample_evaluate_expression(_ctx(d, s))
            assert expr.value == expr.coeff_a * expr.subst_value + expr.coeff_b
            for blob in (expr.latex, expr.text):
                assert "^{2}" not in blob
                assert "^2" not in blob
                assert "x^2" not in blob.lower()
                assert not re.search(r"x\s*[·*]\s*x", blob)
                assert "xx" not in blob.replace(" ", "")
            # Constructive: complexity is inflator/recursion depth, not leaf-count formula.
            assert expr.n_terms >= 1
            assert "seed" in expr.upgrades or len(expr.upgrades) >= 1

    low_ops = [len(sample_evaluate_expression(_ctx(1.0, s)).upgrades) for s in range(20)]
    high_ops = [len(sample_evaluate_expression(_ctx(20.0, s)).upgrades) for s in range(20)]
    assert max(high_ops) >= max(low_ops)

    low_depth = [sample_evaluate_expression(_ctx(1.0, s)).nest_depth for s in range(25)]
    high_depth = [sample_evaluate_expression(_ctx(22.0, s)).nest_depth for s in range(25)]
    assert max(high_depth) >= max(low_depth)


def test_expand_simplify_formula_and_linear():
    import re

    from question_engine.frameworks.primitives import PRIM_EXPAND_SIMPLIFY, build_context
    from question_engine.frameworks.primitives.expand_simplify import (
        GROUP_SCALE,
        NEST_SCALE,
        min_d_for_n_groups,
        min_d_for_nest_extra,
        sample_expand_simplify,
        target_n_groups,
        target_n_lone,
        target_nest_extra,
    )

    assert target_n_groups(0) == 1
    assert target_n_groups(1.5) == 2
    assert target_n_groups(4.5) == 3
    assert target_n_groups(100) > target_n_groups(50)
    assert GROUP_SCALE == 1.5
    for n in range(1, 10):
        d = min_d_for_n_groups(n)
        assert target_n_groups(d) >= n
    assert target_n_lone(0) == 0
    assert target_n_lone(3) >= 1

    assert NEST_SCALE == 4.0
    assert target_nest_extra(0) == 0
    assert target_nest_extra(3.99) == 0
    assert target_nest_extra(4.0) == 1
    assert target_nest_extra(12.0) == 2
    assert target_nest_extra(100) > target_nest_extra(20)
    for e in range(0, 6):
        d = min_d_for_nest_extra(e)
        assert target_nest_extra(d) >= e
        if e > 0:
            assert target_nest_extra(d - 1e-9) == e - 1

    def _ctx(topic_d: float, seed: int):
        return build_context(
            {
                "difficulty": topic_d,
                "integers_only": True,
                "lock_variable": "x",
                "prereq_cap_numbers": 1,
                "prereq_cap_variable": 0,
                "prereq_cap_expand_simplify": 24,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EXPAND_SIMPLIFY],
            rng=random.Random(seed),
        )

    for d, seed in [(0, 1), (5, 2), (12, 3), (20, 4)]:
        for s in range(seed, seed + 6):
            expr = sample_expand_simplify(_ctx(d, s))
            # Constructive: answer-first affine; n_groups ≈ distribute inflators.
            assert expr.n_groups >= 1
            assert expr.nest_depth >= 1
            assert expr.coeff_a != 0 or expr.coeff_b != 0
            assert "seed" in expr.upgrades or expr.simplified_latex
            for blob in (expr.latex, expr.text, expr.simplified_latex):
                assert "^{2}" not in blob
                assert "^2" not in blob
                assert not re.search(r"x\s*[·*]\s*x", blob)

    low_g = [sample_expand_simplify(_ctx(1.0, s)).n_groups for s in range(15)]
    high_up = [
        len(sample_expand_simplify(_ctx(20.0, s)).upgrades) for s in range(15)
    ]
    assert max(low_g) <= 4
    assert max(high_up) >= 2

    # Low effective spend: shallow nesting.
    low_nest = [sample_expand_simplify(_ctx(2.0, s)) for s in range(20)]
    assert all(e.nest_depth <= 3 for e in low_nest)

    pooled = [sample_expand_simplify(_ctx(d, s)) for d in (8.0, 14.0, 20.0, 24.0) for s in range(12)]
    mid = [e for e in pooled if e.effective_d >= 4.0]
    deep = [e for e in pooled if e.effective_d >= 12.0]
    assert mid, "expected samples with expand spend ≥ 4"
    assert any(e.nest_depth >= 2 for e in mid)
    assert deep, "expected samples with expand spend ≥ 12"
    assert max(e.nest_depth for e in deep) >= 2
    assert any(e.text.count("(") >= 2 for e in mid)

    # Spot-check: nested expand stays linear after simplify.
    for e in mid + deep:
        assert e.coeff_a != 0 or e.coeff_b != 0
        assert e.simplified_latex
        assert "x^2" not in e.simplified_text.lower()


def test_multistep_ops_formula_and_smoke():
    from question_engine.frameworks.primitives import PRIM_EQUATIONS, PRIM_INEQUALITIES, build_context
    from question_engine.frameworks.primitives.equations import (
        STEP_SCALE,
        min_d_for_n_ops,
        sample_linear_equation,
        target_n_ops,
    )
    from question_engine.frameworks.primitives.inequalities import sample_linear_inequality
    from question_engine.generators.primitive_g6 import (
        expand_then_simplify,
        multi_step_equations,
        multi_step_inequalities,
    )

    assert target_n_ops(0) == 3
    assert target_n_ops(2) == 4
    assert target_n_ops(6) == 6
    assert target_n_ops(24) == 15
    assert target_n_ops(194) == 100
    assert target_n_ops(1000) > target_n_ops(500)
    assert target_n_ops(100) > target_n_ops(50)
    assert STEP_SCALE == 2.0
    for n in range(3, 12):
        d = min_d_for_n_ops(n)
        assert target_n_ops(d) >= n

    def _eq_ctx(d: float, seed: int):
        return build_context(
            {
                "difficulty": d,
                "integers_only": True,
                "lock_variable": "x",
                "force_steps": "multi",
                "prereq_cap_numbers": 1,
                "prereq_cap_variable": 0,
                "prereq_cap_equations": 24,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            rng=random.Random(seed),
        )

    for d, seed in [(0, 1), (4, 2), (14, 3), (24, 4)]:
        for s in range(seed, seed + 5):
            eq = sample_linear_equation(_eq_ctx(d, s), force_steps="multi")
            assert eq.steps == "multi"
            # Multi-step floors at 4 ops (both sides); never collapses below that.
            assert eq.n_ops == max(4, target_n_ops(eq.effective_d))
            assert eq.n_ops >= 4

    low = [sample_linear_equation(_eq_ctx(0.5, s), force_steps="multi").n_ops for s in range(12)]
    high = [sample_linear_equation(_eq_ctx(20.0, s), force_steps="multi").n_ops for s in range(12)]
    assert max(low) == 4
    assert max(high) >= 5
    assert sum(high) / len(high) > sum(low) / len(low)

    def _ineq_ctx(d: float, seed: int):
        return build_context(
            {
                "difficulty": d,
                "integers_only": True,
                "lock_variable": "x",
                "force_steps": "multi",
                "prereq_cap_numbers": 1,
                "prereq_cap_variable": 0,
                "prereq_cap_inequalities": 24,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
            rng=random.Random(seed),
        )

    for s in range(10):
        ineq = sample_linear_inequality(_ineq_ctx(10.0, s), force_steps="multi")
        assert ineq.steps == "multi"
        assert ineq.n_ops >= 3
        assert ineq.solution_latex

    base = {
        "count": 3,
        "include_answer_key": True,
        "difficulty": 8,
        "integers_only": True,
        "only_x": True,
    }
    for fn, engine in (
        (expand_then_simplify, "expand_simplify"),
        (multi_step_equations, "equations"),
        (multi_step_inequalities, "inequalities"),
    ):
        qs = fn(engine, dict(base))
        assert len(qs) == 3
        assert all(q.answer_latex for q in qs)
        assert "spend" in qs[0].metadata
        assert qs[0].metadata.get("primitive_engine") == engine
        if engine != "expand_simplify":
            assert all(q.metadata.get("steps") == "multi" for q in qs)
            assert all(int(q.metadata.get("n_ops") or 0) >= 3 for q in qs)
        if engine == "inequalities":
            assert qs[0].metadata.get("number_line_spec")
            assert qs[0].metadata.get("answer_number_line_spec")


def test_leaf_resolves_expand_and_multistep():
    assert resolve_primitive("expand_simplify") == "expand_simplify"
    assert resolve_primitive("a2_beginning_algebra_simplifying_algebraic_expressions") == (
        "expand_simplify"
    )
    assert resolve_primitive("multi_step_equations") == "equations"
    assert resolve_primitive("pa_multi_step_inequalities") == "inequalities"
    assert resolve_primitive("geo_review_multi_step_equations") == "equations"


def test_ooo_shapes_vary_across_seeds():
    from question_engine.frameworks.primitives.ooo import sample_ooo_expression

    def _ctx(seed: int, d: float = 10.0):
        return build_context(
            {
                "difficulty": d,
                "integers_only": True,
                "prereq_cap_numbers": 2,
                "prereq_cap_ooo": 40,
            },
            [PRIM_NUMBERS, PRIM_OOO],
            rng=random.Random(seed),
        )

    shapes = {sample_ooo_expression(_ctx(s)).shape_id for s in range(24)}
    texts = {sample_ooo_expression(_ctx(s)).text for s in range(24)}
    assert len(shapes) >= 4
    assert len(texts) >= 8


def test_ooo_flat_grows_ops_sparse_parens():
    """Flat sum-of-products: many ×/÷, few parentheses; answers match text eval."""
    from fractions import Fraction

    from question_engine.frameworks.primitives.ooo import sample_ooo_expression

    def _ctx(d: float, seed: int):
        return build_context(
            {
                "difficulty": d,
                "integers_only": True,
                "prereq_cap_numbers": 2,
                "prereq_cap_ooo": 40,
            },
            [PRIM_NUMBERS, PRIM_OOO],
            rng=random.Random(seed),
        )

    def _eval_text(text: str) -> Fraction:
        return Fraction(eval(text.replace(" ", ""), {"__builtins__": {}}))

    low = [sample_ooo_expression(_ctx(2.0, s)) for s in range(20)]
    high = [sample_ooo_expression(_ctx(20.0, s)) for s in range(20)]

    assert all(_eval_text(e.text) == e.value for e in low + high)
    assert sum(e.n_ops for e in high) > sum(e.n_ops for e in low)
    assert max(e.n_ops for e in high) >= 8

    # Precedence without nesting: most high-D samples have ×/÷ and no group parens.
    muldiv_high = sum(1 for e in high if "\\times" in e.latex or "\\div" in e.latex)
    assert muldiv_high >= 15
    group_paren_rate = sum(1 for e in high if e.nest_depth > 0) / len(high)
    assert group_paren_rate <= 0.5

    # No ugly "+ -N" / "× -N" schoolbook renders.
    for e in low + high:
        assert "+ -" not in e.latex
        assert "\\times -" not in e.latex
        assert "* -" not in e.text.replace(" ", "")


def test_multistep_equations_compose_simplify_sides():
    from question_engine.frameworks.primitives.equations import sample_linear_equation
    from question_engine.generators.primitive_g6 import (
        expand_then_simplify,
        multi_step_equations,
    )

    def _eq_ctx(d: float, seed: int):
        return build_context(
            {
                "difficulty": d,
                "integers_only": True,
                "lock_variable": "x",
                "force_steps": "multi",
                "prereq_cap_numbers": 1,
                "prereq_cap_variable": 0,
                "prereq_cap_equations": 24,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            rng=random.Random(seed),
        )

    rich = 0
    for s in range(20):
        eq = sample_linear_equation(_eq_ctx(8.0, s), force_steps="multi")
        assert "=" in eq.text
        assert eq.steps == "multi"
        if "(" in eq.text or "\\left(" in eq.latex:
            rich += 1
        assert "compose_simplify" in eq.upgrades or "clear_fractions" in eq.upgrades or (
            "identity" in eq.upgrades or "no_solution" in eq.upgrades
        )
    assert rich >= 12

    # A2 simplifying leaf → expand/simplify stems (no Solve verb in body).
    qs = expand_then_simplify(
        "Simplify",
        {
            "count": 4,
            "include_answer_key": True,
            "difficulty": 6,
            "integers_only": True,
            "only_x": True,
        },
    )
    assert all("solve" not in q.prompt_text.lower() for q in qs)
    assert all(q.prompt_latex.strip() and q.prompt_text.strip() for q in qs)

    eq_qs = multi_step_equations(
        "Eq",
        {
            "count": 4,
            "include_answer_key": True,
            "difficulty": 10,
            "integers_only": True,
            "only_x": True,
        },
    )
    assert all("=" in q.prompt_text for q in eq_qs)
    # "Solve for …" is the catalog instruction header, not repeated in the stem.
    assert all("solve" not in q.prompt_text.lower() for q in eq_qs)


def test_expression_policy_linear_default_and_degree_gate():
    from question_engine.frameworks.primitives import (
        LINEAR_POLICY,
        POLYNOMIAL_POLICY_DEFAULT,
        PRIM_FACTOR_GCF,
        assert_linear_sample,
        build_context,
        resolve_policy,
    )
    from question_engine.frameworks.primitives.factor_gcf import sample_factor_gcf

    assert resolve_policy(None).max_degree == 1
    assert resolve_policy("factor_gcf").max_degree == 1
    assert resolve_policy("polynomial_factoring_common_factor").family == "polynomial"
    assert POLYNOMIAL_POLICY_DEFAULT.max_degree >= 2

    for s in range(40):
        ctx2 = build_context(
            {
                "difficulty": 20,
                "integers_only": True,
                "lock_variable": "x",
                "prereq_cap_numbers": 2,
                "prereq_cap_variable": 0,
                "prereq_cap_factor_gcf": 24,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_GCF],
            rng=random.Random(s),
            leaf_id="g6_factor_gcf",
        )
        expr = sample_factor_gcf(ctx2)
        assert expr.max_degree <= 1
        assert_linear_sample(expr.latex, expr.text, policy=LINEAR_POLICY)
        assert "^{2}" not in expr.latex
        assert "variable_gcf" not in expr.upgrades


def test_special_solutions_and_clear_fractions():
    from question_engine.frameworks.primitives import PRIM_EQUATIONS, build_context
    from question_engine.frameworks.primitives.equations import sample_linear_equation

    def _ctx(extra, seed):
        return build_context(
            {
                "difficulty": 16,
                "integers_only": True,
                "lock_variable": "x",
                "force_steps": "multi",
                "prereq_cap_numbers": 4,
                "prereq_cap_variable": 0,
                "prereq_cap_equations": 24,
                **extra,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            rng=random.Random(seed),
        )

    id_eq = sample_linear_equation(
        _ctx({"allow_special_solutions": "identity"}, 1), force_steps="multi"
    )
    assert id_eq.solution_kind == "identity"
    assert "all real" in id_eq.solution_latex.lower() or "real" in id_eq.solution_latex

    no_eq = sample_linear_equation(
        _ctx({"allow_special_solutions": "no_sol"}, 2), force_steps="multi"
    )
    assert no_eq.solution_kind == "no_solution"

    frac_eq = sample_linear_equation(
        _ctx({"clear_fractions": True, "allow_special_solutions": "none"}, 3),
        force_steps="multi",
    )
    assert frac_eq.solution_kind == "unique"
    assert "clear_fractions" in frac_eq.upgrades


def test_linear_family_generators_smoke():
    from question_engine.generators import GENERATORS

    keys = [
        "absolute_value_equations",
        "absolute_value_inequalities",
        "compound_inequalities",
        "solving_proportions",
        "literal_equations",
        "slope",
        "writing_linear_equations",
        "graphing_linear_equations",
        "graphing_linear_inequalities",
        "systems_elimination",
        "systems_substitution",
        "systems_graphing",
        "wp_one_step_equation",
        "wp_mixture",
        "wp_systems",
        "wp_proportion",
        "factor_gcf",
        "polynomial_factoring_common_factor",
    ]
    base = {
        "count": 2,
        "include_answer_key": True,
        "difficulty": 8,
        "integers_only": True,
        "only_x": True,
    }
    for key in keys:
        assert key in GENERATORS, key
        qs = GENERATORS[key](key, dict(base))
        assert len(qs) == 2, key
        assert qs[0].prompt_latex
        assert qs[0].answer_latex
        meta = qs[0].metadata or {}
        assert "expression_policy" in meta or "spend" in meta
        # Linear leaves must not emit x^2 (poly factor_gcf may).
        if key not in {"polynomial_factoring_common_factor"}:
            blob = (qs[0].prompt_latex or "") + (qs[0].answer_latex or "")
            assert "^{2}" not in blob, f"{key}: {blob}"


def test_leaf_resolves_linear_finish():
    assert resolve_primitive("absolute_value_equations") == "equations"
    assert resolve_primitive("compound_inequalities") == "inequalities"
    assert resolve_primitive("systems_elimination") == "equations"
    assert resolve_primitive("wp_mixture") == "equations"
    assert resolve_primitive("solving_proportions") == "equations"


def test_poly_degree_targeting_and_policy_separation():
    from question_engine.frameworks.primitives.expression_policy import (
        LINEAR_POLICY,
        POLYNOMIAL_POLICY_DEFAULT,
        resolve_policy,
    )
    from question_engine.frameworks.primitives.poly_helpers import (
        min_d_for_degree,
        target_poly_degree,
    )

    assert target_poly_degree(0, LINEAR_POLICY) == 1
    assert target_poly_degree(20, LINEAR_POLICY) == 1
    assert target_poly_degree(0, POLYNOMIAL_POLICY_DEFAULT) == 2
    assert target_poly_degree(min_d_for_degree(3), POLYNOMIAL_POLICY_DEFAULT) >= 3
    assert target_poly_degree(100, POLYNOMIAL_POLICY_DEFAULT) <= POLYNOMIAL_POLICY_DEFAULT.max_degree

    assert resolve_policy("polynomial_add_subtract").family == "polynomial"
    assert resolve_policy("combining_like_terms").max_degree == 1
    assert resolve_policy("quadratic_factoring").max_degree == 2


def test_poly_primitives_smoke_and_degree():
    from question_engine.frameworks.primitives import (
        LINEAR_POLICY,
        PRIM_EVALUATE,
        PRIM_EXPAND_SIMPLIFY,
        PRIM_LIKE_TERMS,
        PRIM_NUMBERS,
        PRIM_VARIABLE,
        assert_linear_sample,
        build_context,
        polynomial_policy,
    )
    from question_engine.frameworks.primitives.evaluate import sample_evaluate_expression
    from question_engine.frameworks.primitives.expand_simplify import sample_expand_simplify
    from question_engine.frameworks.primitives.factor_poly import (
        PRIM_FACTOR_POLY,
        sample_quadratic_factoring,
        sample_special_factoring,
    )
    from question_engine.frameworks.primitives.like_terms import sample_like_terms
    from question_engine.frameworks.primitives.polynomials import (
        PRIM_POLYNOMIALS,
        sample_polynomial_add_subtract,
        sample_polynomial_multiply,
        sample_polynomial_naming,
    )

    base = {
        "difficulty": 10,
        "integers_only": True,
        "lock_variable": "x",
        "prereq_cap_numbers": 3,
        "prereq_cap_variable": 0,
    }

    # Linear like-terms still degree-1.
    ctx_lin = build_context(
        {**base, "prereq_cap_like_terms": 20},
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_LIKE_TERMS],
        rng=random.Random(1),
        policy=LINEAR_POLICY,
        leaf_id="combining_like_terms",
    )
    lt = sample_like_terms(ctx_lin)
    assert lt.max_degree <= 1
    assert_linear_sample(lt.latex, lt.text, policy=LINEAR_POLICY)

    poly = polynomial_policy(max_degree=3)
    ctx_poly = build_context(
        {**base, "prereq_cap_like_terms": 20, "expression_family": "polynomial"},
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_LIKE_TERMS],
        rng=random.Random(2),
        policy=poly,
        leaf_id="poly_combine_like_terms",
    )
    plt = sample_like_terms(ctx_poly)
    assert plt.max_degree >= 2
    assert "^{2}" in plt.latex or "^2" in plt.latex or "^{3}" in plt.latex

    ctx_add = build_context(
        {**base, "prereq_cap_polynomials": 20},
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_POLYNOMIALS],
        rng=random.Random(3),
        policy=poly,
        leaf_id="polynomial_add_subtract",
    )
    add = sample_polynomial_add_subtract(ctx_add)
    assert add.degree >= 2
    name = sample_polynomial_naming(ctx_add)
    assert name.degree >= 2
    mul = sample_polynomial_multiply(ctx_add)
    assert mul.degree >= 2

    ctx_exp = build_context(
        {**base, "prereq_cap_expand_simplify": 20},
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EXPAND_SIMPLIFY],
        rng=random.Random(4),
        policy=poly,
        leaf_id="poly_expand_simplify",
    )
    exp = sample_expand_simplify(ctx_exp)
    assert exp.max_degree >= 2

    ctx_ev = build_context(
        {**base, "prereq_cap_evaluate": 20},
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EVALUATE],
        rng=random.Random(5),
        policy=poly,
        leaf_id="evaluate_polynomial",
    )
    ev = sample_evaluate_expression(ctx_ev)
    assert ev.max_degree >= 2

    ctx_fac = build_context(
        {**base, "prereq_cap_factor_poly": 20},
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
        rng=random.Random(6),
        policy=polynomial_policy(max_degree=2),
        leaf_id="quadratic_factoring",
    )
    qf = sample_quadratic_factoring(ctx_fac)
    assert qf.degree == 2
    sp = sample_special_factoring(ctx_fac)
    assert sp.degree == 2


def test_poly_family_generators_smoke():
    from question_engine.generators import GENERATORS

    keys = [
        "polynomial_naming",
        "polynomial_add_subtract",
        "polynomial_multiply",
        "polynomial_multiply_special",
        "evaluate_polynomial",
        "poly_combine_like_terms",
        "poly_expand_simplify",
        "polynomial_factoring_common_factor",
        "quadratic_factoring",
        "polynomial_factoring_special_cases",
        "polynomial_factoring_grouping",
    ]
    base = {
        "count": 2,
        "include_answer_key": True,
        "difficulty": 8,
        "integers_only": True,
        "only_x": True,
        "max_degree": 3,
    }
    for key in keys:
        assert key in GENERATORS, key
        qs = GENERATORS[key](key, dict(base))
        assert len(qs) == 2, key
        assert qs[0].prompt_latex
        assert qs[0].answer_latex
        meta = qs[0].metadata or {}
        assert meta.get("expression_policy", {}).get("family") == "polynomial" or meta.get(
            "spend"
        )
        # Poly galleries should show degree > 1 somewhere across samples.
        blob = (qs[0].prompt_latex or "") + (qs[0].answer_latex or "")
        # Naming answers are words; prompts still need higher powers for most keys.
        if key not in {"polynomial_naming"}:
            policy_deg = (meta.get("expression_policy") or {}).get("max_degree", 0)
            assert (
                "^{2}" in blob
                or "^2" in blob
                or "^{3}" in blob
                or meta.get("degree", 0) >= 2
                or meta.get("max_degree", 0) >= 2
                or policy_deg >= 2
            ), f"{key}: no poly degree signal in {blob!r} meta={meta}"


def test_leaf_resolves_poly_family():
    assert resolve_primitive("polynomial_add_subtract") == "polynomials"
    assert resolve_primitive("quadratic_factoring") == "factor_poly"
    assert resolve_primitive("evaluate_polynomial") == "evaluate"
    assert resolve_primitive("poly_expand_simplify") == "expand_simplify"


def _count_signed_terms(latex: str) -> int:
    import re

    s = (latex or "").replace(" ", "")
    if not s:
        return 0
    parts = re.split(r"(?=[+-])", s)
    return len([p for p in parts if p and p not in "+-"])


def test_like_terms_difficulty_term_anchors():
    """D=0 = 2 like + 2 unlike; D≈5 stays around 3–4 terms (not huge)."""
    from collections import Counter

    from question_engine.generators.primitive_g6 import combining_like_terms

    qs0 = combining_like_terms(
        "Combining like terms",
        {
            "difficulty": 0,
            "count": 40,
            "include_answer_key": True,
            "seed": 7,
            "integers_only": True,
        },
    )
    counts0 = [_count_signed_terms(q.prompt_latex or q.prompt) for q in qs0]
    # Simplest shape: always 4 display terms (2 alike + 2 different).
    assert all(n == 4 for n in counts0), Counter(counts0)
    # No structure upgrades / no negatives at D=0.
    for q in qs0:
        ups = q.metadata.get("upgrades") or []
        assert ups == []
        prompt = q.prompt_latex or ""
        assert " - " not in prompt
        assert not prompt.lstrip().startswith("-")

    qs5 = combining_like_terms(
        "Combining like terms",
        {
            "difficulty": 5,
            "count": 50,
            "include_answer_key": True,
            "seed": 11,
            "integers_only": True,
        },
    )
    counts5 = [_count_signed_terms(q.prompt_latex or q.prompt) for q in qs5]
    dist5 = Counter(counts5)
    assert set(dist5) <= {3, 4}, dist5
    # Typical feel: 3 or 4 terms (prefer 3, but allow near-even RNG).
    assert dist5[3] + dist5[4] == len(counts5)
    assert dist5[3] >= len(counts5) // 3, dist5
    assert max(counts5) <= 4
    # Mild band: no sign/structure upgrades yet.
    for q in qs5:
        assert (q.metadata.get("upgrades") or []) == []
        assert " - " not in (q.prompt_latex or "")

