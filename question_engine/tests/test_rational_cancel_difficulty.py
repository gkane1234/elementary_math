"""Continuous-difficulty cancel unlocks for rational simplify and add/subtract."""

from __future__ import annotations

from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs
from question_engine.frameworks.primitives.rational_cancel import (
    ALL_AVAILABLE_CANCEL,
    allowed_rational_cancel_counts,
    continuous_rational_cancel_max,
    continuous_rational_lcd_factors_max,
    continuous_rational_term_count_max,
    resolve_rational_cancel_count,
)
from question_engine.generators.primitive_rational import (
    rational_add_subtract,
    rational_simplify,
)


def test_cancel_unlock_thresholds():
    reload_knobs()
    assert allowed_rational_cancel_counts(0) == (1,)
    assert allowed_rational_cancel_counts(3.9) == (1,)
    assert set(allowed_rational_cancel_counts(4)) == {0, 1}
    assert set(allowed_rational_cancel_counts(6)) == {0, 1, 2}
    assert set(allowed_rational_cancel_counts(10)) == {0, 1, 2, 3}
    assert set(allowed_rational_cancel_counts(14)) == {0, 1, 2, 3, 4}
    # Past unlock_4: exact counts grow unboundedly (no plateau at 4).
    d24 = set(allowed_rational_cancel_counts(24))
    assert {0, 1, 2, 3, 4}.issubset(d24)
    assert max(d24) == continuous_rational_cancel_max(24)
    assert max(d24) > 4
    d40 = set(allowed_rational_cancel_counts(40))
    assert max(d40) > max(d24)
    d1000 = set(allowed_rational_cancel_counts(1000))
    assert max(d1000) >= 100


def test_continuous_structure_maxes_unbounded():
    reload_knobs()
    assert continuous_rational_lcd_factors_max({}) is None
    assert continuous_rational_term_count_max({}) is None

    d0_lcd = continuous_rational_lcd_factors_max({"difficulty": 0})
    d40_lcd = continuous_rational_lcd_factors_max({"difficulty": 40})
    d1000_lcd = continuous_rational_lcd_factors_max({"difficulty": 1000})
    assert d0_lcd is not None and d0_lcd <= 3
    assert d40_lcd is not None and d40_lcd >= 8
    assert d1000_lcd is not None and d1000_lcd >= 100
    assert d1000_lcd > d40_lcd > d0_lcd

    d0_t = continuous_rational_term_count_max({"difficulty": 0})
    d40_t = continuous_rational_term_count_max({"difficulty": 40})
    d1000_t = continuous_rational_term_count_max({"difficulty": 1000})
    assert d0_t == 2
    assert d40_t is not None and d40_t >= 6
    assert d1000_t is not None and d1000_t >= 100
    assert d1000_t > d40_t > d0_t

    assert continuous_rational_cancel_max(0) == 1
    assert continuous_rational_cancel_max(40) >= 8
    assert continuous_rational_cancel_max(1000) >= 100


def test_explicit_cancel_factor_count_overrides_difficulty():
    assert resolve_rational_cancel_count({"cancel_factor_count": 3, "difficulty": 0}) == 3
    assert resolve_rational_cancel_count({"cancel_factor_count": "0", "difficulty": 0}) == 0
    assert resolve_rational_cancel_count({"cancel_factor_count": "auto", "difficulty": 0}) == 1
    assert resolve_rational_cancel_count({"cancel_factor_count": "random", "difficulty": 0}) == 1
    # UI "4" / "all" → all-available sentinel (clamped later by builders).
    assert resolve_rational_cancel_count({"cancel_factor_count": "all", "difficulty": 0}) == ALL_AVAILABLE_CANCEL
    assert resolve_rational_cancel_count({"cancel_factor_count": "4", "difficulty": 0}) == ALL_AVAILABLE_CANCEL
    # Integer 4 is exact (not the UI all-available label).
    assert resolve_rational_cancel_count({"cancel_factor_count": 4, "difficulty": 0}) == 4
    assert resolve_rational_cancel_count({"cancel_factor_count": 12, "difficulty": 0}) == 12


def test_clamp_cancel_to_available():
    from question_engine.frameworks.primitives.rational_cancel import (
        clamp_cancel_to_available,
    )

    assert clamp_cancel_to_available(2, 3) == 2
    assert clamp_cancel_to_available(3, 2) == 2
    assert clamp_cancel_to_available(0, 4) == 0
    assert clamp_cancel_to_available(2, 0) == 0
    assert clamp_cancel_to_available(-1, 2) == 0
    assert clamp_cancel_to_available(ALL_AVAILABLE_CANCEL, 7) == 7


def test_low_d_defaults_to_one_cancel_for_both_generators():
    for fn, topic in (
        (rational_simplify, "a2_rational_expressions_simplifying"),
        (rational_add_subtract, "a2_rational_expressions_adding_and_subtracting"),
    ):
        qs = fn(
            topic,
            {
                "count": 8,
                "include_answer_key": True,
                "difficulty": 0,
                "integers_only": True,
                "cancel_factor_count": "auto",
            },
        )
        assert len(qs) == 8
        for q in qs:
            assert q.metadata.get("cancel_factor_count") == 1


def test_forced_cancel_counts_on_both_generators():
    for k in (0, 1, 2, 3, 4):
        for fn, topic in (
            (rational_simplify, "a2_rational_expressions_simplifying"),
            (rational_add_subtract, "a2_rational_expressions_adding_and_subtracting"),
        ):
            qs = fn(
                topic,
                {
                    "count": 3,
                    "include_answer_key": True,
                    "difficulty": 20,
                    "integers_only": True,
                    "cancel_factor_count": k,
                },
            )
            assert len(qs) == 3
            for q in qs:
                assert q.metadata.get("cancel_factor_count") == k
                assert q.answer_latex
                constructive = q.metadata.get("constructive") or {}
                assert constructive.get("cancel_factor_count") == k


def test_high_d_samples_only_unlocked_counts():
    allowed = set(allowed_rational_cancel_counts(14))
    seen: set[int] = set()
    for seed_offset in range(40):
        qs = rational_simplify(
            "a2_rational_expressions_simplifying",
            {
                "count": 1,
                "include_answer_key": True,
                "difficulty": 14,
                "integers_only": True,
                "cancel_factor_count": "auto",
            },
        )
        k = qs[0].metadata.get("cancel_factor_count")
        assert k in allowed
        seen.add(int(k))
    # With 40 draws over a 5-count pool, expect more than just the default.
    assert len(seen) >= 2


def test_d40_and_d1000_structure_possible():
    """D=40 large-ish; D=1000 absurd factor/term ceilings are reachable."""
    reload_knobs()
    from question_engine.frameworks.primitives import PRIM_NUMBERS, PRIM_VARIABLE, build_context
    from question_engine.frameworks.primitives.constructive import construct_rational_sum
    from question_engine.frameworks.primitives.expression_policy import POLYNOMIAL_POLICY_DEFAULT

    assert continuous_rational_lcd_factors_max({"difficulty": 40}) >= 8
    assert continuous_rational_term_count_max({"difficulty": 40}) >= 6
    assert continuous_rational_lcd_factors_max({"difficulty": 1000}) >= 100
    assert continuous_rational_term_count_max({"difficulty": 1000}) >= 100

    # Forced large structure via constructive (factors-first, linear in n).
    ctx40 = build_context(
        {"difficulty": 40, "integers_only": True},
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
    )
    surface40 = construct_rational_sum(
        ctx40, d=40, cancel_count=6, as_sum=True, n_terms=8
    )
    assert surface40.metadata.get("cancel_factor_count") == 6
    assert surface40.metadata.get("n_terms") == 8
    assert surface40.latex

    qs40 = rational_add_subtract(
        "a2_rational_expressions_adding_and_subtracting",
        {
            "count": 1,
            "include_answer_key": True,
            "difficulty": 40,
            "integers_only": True,
            "cancel_factor_count": 6,
        },
    )
    assert len(qs40) == 1
    assert qs40[0].metadata.get("cancel_factor_count") == 6
    assert qs40[0].prompt_latex

    # Absurd but factors-first: many cancel inserts on a single L2 fraction.
    qs1000 = rational_simplify(
        "a2_rational_expressions_simplifying",
        {
            "count": 1,
            "include_answer_key": True,
            "difficulty": 1000,
            "integers_only": True,
            "cancel_factor_count": 40,
        },
    )
    assert len(qs1000) == 1
    assert qs1000[0].metadata.get("cancel_factor_count") == 40
    assert qs1000[0].prompt_latex


def test_a1_add_subtract_honors_cancel_counts():
    import question_engine.types  # noqa: F401
    from question_engine.core.base import QUESTION_TYPES

    qt = QUESTION_TYPES["rational_expression_simplification"]
    for k in (0, 1, 2):
        qs = qt.generate(
            {
                "count": 3,
                "include_answer_key": True,
                # No continuous ``difficulty`` — keep explicit max_lcd_factors.
                "difficulty_tier": "hard",
                "integers_only": True,
                "cancel_factor_count": k,
                "add_subtract_structure": "complex",
                "max_lcd_factors": 3,
                "allow_polynomial_terms": True,
                "allow_full_lcd_terms": True,
            }
        )
        assert len(qs) == 3
        for q in qs:
            assert q.prompt_latex
            assert q.answer_latex
            actual = q.metadata.get("cancelled_lcd_factor_count")
            if k == 0:
                assert actual == 0
            else:
                assert actual == k or (
                    k >= 3 and actual >= 1
                )  # all-available remap edge
            assert q.metadata.get("cancel_factor_count") is not None


def test_a1_add_subtract_clamps_when_not_enough_lcd_factors():
    """Request more cancels than capacity → cancel all available, do not fail."""
    import question_engine.types  # noqa: F401
    from question_engine.core.base import QUESTION_TYPES

    qt = QUESTION_TYPES["rational_expression_simplification"]
    qs = qt.generate(
        {
            "count": 4,
            "include_answer_key": True,
            # No continuous ``difficulty`` — keep explicit max_lcd_factors=2.
            "difficulty_tier": "medium",
            "integers_only": True,
            "cancel_factor_count": 3,
            "add_subtract_structure": "complex",
            # No poly remainder allowed → capacity = max_lcd_factors - 1 = 1.
            "max_lcd_factors": 2,
            "allow_polynomial_terms": False,
            "allow_full_lcd_terms": False,
            "inflation_chance": 0,
        }
    )
    assert len(qs) == 4
    for q in qs:
        assert q.prompt_latex
        assert q.answer_latex
        assert q.metadata.get("cancelled_lcd_factor_count") == 1
        assert q.metadata.get("requested_cancel_factor_count") == 3
        assert q.metadata.get("cancel_factor_count") == 1


def test_a1_continuous_d_overrides_emh_lcd_plateau():
    """Continuous D must not stay stuck at hard's max_lcd_factors=3."""
    import question_engine.types  # noqa: F401
    from question_engine.core.base import QUESTION_TYPES
    from question_engine.frameworks.primitives.rational_cancel import (
        apply_continuous_rational_structure,
        continuous_rational_lcd_factors_max,
        continuous_rational_term_count_max,
    )

    assert continuous_rational_lcd_factors_max({"difficulty": 40}) >= 8
    assert continuous_rational_term_count_max({"difficulty": 40}) >= 6

    # Even if EMH hard plateaus leak in, continuous rewrite lifts the ceiling.
    lifted = apply_continuous_rational_structure(
        {
            "difficulty": 40,
            "add_subtract_structure": "complex",
            "max_lcd_factors": 3,
            "term_count": 3,
        }
    )
    assert int(lifted["max_lcd_factors"]) >= 8

    qt = QUESTION_TYPES["rational_expression_simplification"]
    qs = qt.generate(
        {
            "count": 1,
            "include_answer_key": True,
            "difficulty": 40,
            "integers_only": True,
            "cancel_factor_count": 5,
            "add_subtract_structure": "complex",
            "allow_polynomial_terms": True,
            "allow_full_lcd_terms": True,
        }
    )
    assert len(qs) == 1
    assert qs[0].prompt_latex
    assert qs[0].metadata.get("max_lcd_factors", 0) >= 5
    assert qs[0].metadata.get("cancelled_lcd_factor_count") == 5


def test_ui_all_available_returns_quickly_and_stays_capped():
    """UI cancel_factor_count=\"4\" must not hang or grow to continuous D max."""
    import time

    import question_engine.types  # noqa: F401
    from question_engine.core.base import QUESTION_TYPES
    from question_engine.frameworks.primitives.rational_cancel import (
        ALL_AVAILABLE_FACTOR_CAP,
        sample_all_available_factor_count,
    )

    assert sample_all_available_factor_count({"difficulty": 1000}) <= ALL_AVAILABLE_FACTOR_CAP

    qt = QUESTION_TYPES["rational_expression_simplification"]
    for d in (0, 20, 40):
        t0 = time.perf_counter()
        qs = qt.generate(
            {
                "count": 3,
                "include_answer_key": True,
                "difficulty": d,
                "integers_only": True,
                "cancel_factor_count": "4",  # UI: All available
                "add_subtract_structure": "complex",
                "allow_polynomial_terms": True,
                "allow_full_lcd_terms": True,
            }
        )
        elapsed = time.perf_counter() - t0
        assert elapsed < 3.0, f"all-available hung at d={d}: {elapsed:.2f}s"
        assert len(qs) == 3
        for q in qs:
            assert q.prompt_latex
            assert q.answer_latex
            assert "\\neq" in (q.answer_latex or "")
            cancelled = int(q.metadata.get("cancelled_lcd_factor_count") or 0)
            assert cancelled >= 1
            assert cancelled <= ALL_AVAILABLE_FACTOR_CAP
            assert int(q.metadata.get("max_lcd_factors") or 0) <= ALL_AVAILABLE_FACTOR_CAP


def test_canceled_factors_appear_in_domain_restrictions():
    """Every LCD / canceled linear factor must contribute an x≠ restriction."""
    import question_engine.types  # noqa: F401
    from packages.polynomial_core import (
        excluded_values_from_factors,
        linear_factor_excluded_value,
    )
    from packages.polynomial_core.polynomial import Polynomial
    from question_engine.core.base import QUESTION_TYPES

    # Helper sanity: non-monic canceled factors are exact fractions.
    assert linear_factor_excluded_value(Polynomial([3, -2])) == __import__(
        "fractions"
    ).Fraction(2, 3)
    assert len(excluded_values_from_factors([Polynomial([3, -2]), Polynomial([1, -4])])) == 2

    qt = QUESTION_TYPES["rational_expression_simplification"]
    for _ in range(20):
        qs = qt.generate(
            {
                "count": 1,
                "include_answer_key": True,
                "include_solution_details": True,
                "difficulty_tier": "hard",
                "integers_only": True,
                "cancel_factor_count": 2,
                "add_subtract_structure": "complex",
                "max_lcd_factors": 3,
                "allow_polynomial_terms": True,
                "allow_full_lcd_terms": True,
            }
        )
        q = qs[0]
        sol = q.metadata.get("solution") or {}
        lcd_factors = sol.get("lcd_factors") or []
        cancelled = sol.get("cancelled_lcd_factors") or []
        excl = q.metadata.get("excluded_values") or []
        assert len(cancelled) >= 1
        assert len(excl) >= len(lcd_factors)
        assert "\\neq" in (q.answer_latex or "")


def test_constructive_simplify_includes_domain_for_cancels():
    qs = rational_simplify(
        "a2_rational_expressions_simplifying",
        {
            "count": 5,
            "include_answer_key": True,
            "difficulty": 8,
            "integers_only": True,
            "cancel_factor_count": 1,
        },
    )
    assert len(qs) == 5
    for q in qs:
        assert q.metadata.get("cancel_factor_count") == 1
        excl = q.metadata.get("excluded_values") or []
        assert len(excl) >= 1
        assert "\\neq" in (q.answer_latex or "")
