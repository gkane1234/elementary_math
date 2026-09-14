"""Tests for skeleton numeric vs format difficulty bands."""

from __future__ import annotations

from question_engine.frameworks.primitives.factor_sampler import constraints_from_settings
from question_engine.frameworks.primitives.rational_skeleton import rational_skeleton_caps
from question_engine.frameworks.primitives.skeleton_difficulty import (
    SkeletonDifficultyBands,
    complex_fraction_tier_from_format,
    format_bias_for_tier,
    numeric_bias_for_tier,
    skeleton_format_tier,
    skeleton_numeric_tier,
)


def test_numeric_tier_increases_before_format_at_same_d():
    assert skeleton_numeric_tier(2) == 0
    assert skeleton_format_tier(2) == 0
    assert skeleton_numeric_tier(8) == 2
    assert skeleton_format_tier(8) == 0
    assert skeleton_numeric_tier(16) == 3
    assert skeleton_format_tier(16) == 2


def test_format_unlocks_are_sequential_not_bundled_at_14():
    caps_7 = rational_skeleton_caps(7.0)
    caps_8 = rational_skeleton_caps(8.0)
    caps_12 = rational_skeleton_caps(12.0)
    caps_16 = rational_skeleton_caps(16.0)

    # Low D: phase-0/1 box, no insert-cancel, no factored preference.
    assert caps_7.max_inventory_factors == 2
    assert caps_7.insert_cancel_pairs is False
    assert caps_7.prefer_factored_prompt is False
    assert caps_8.prefer_factored_prompt is False
    assert caps_8.max_inventory_factors == 2

    # Mid D (10–15): one format dim (factored prompt) — still 2-factor box.
    assert caps_12.prefer_factored_prompt is True
    assert caps_12.max_inventory_factors == 2
    assert caps_12.insert_cancel_pairs is False

    # High D (16+): structural unlock (3-factor + insert-cancel).
    assert caps_16.max_inventory_factors == 3
    assert caps_16.insert_cancel_pairs is True


def test_numeric_bias_widens_without_format_expand_at_low_d():
    low = constraints_from_settings({}, d=4.0)
    mid_num = constraints_from_settings({}, d=12.0)
    assert low.expand_weight <= mid_num.expand_weight
    assert low.nonmonic_weight <= mid_num.nonmonic_weight
    # Format tier 1 at D=12 still caps inventory at 2.
    assert rational_skeleton_caps(12.0).max_inventory_factors == 2


def test_expand_weight_tracks_format_tier_not_numeric_tier():
    fmt1 = format_bias_for_tier(1)["expand_weight"]
    fmt2 = format_bias_for_tier(2)["expand_weight"]
    assert fmt1 < fmt2
    cons_8 = constraints_from_settings({}, d=8.0)
    cons_16 = constraints_from_settings({}, d=16.0)
    assert cons_8.expand_weight == format_bias_for_tier(0)["expand_weight"]
    assert cons_16.expand_weight == fmt2


def test_complex_fraction_tier_is_deterministic_by_format():
    assert complex_fraction_tier_from_format(0) == "easy"
    assert complex_fraction_tier_from_format(1) == "easy"
    assert complex_fraction_tier_from_format(2) == "medium"
    assert complex_fraction_tier_from_format(3) == "hard"


def test_bands_from_d_roundtrip():
    b = SkeletonDifficultyBands.from_d(16.0)
    assert b.numeric_tier == skeleton_numeric_tier(16.0)
    assert b.format_tier == skeleton_format_tier(16.0)
    assert numeric_bias_for_tier(b.numeric_tier)["const_hi_default"] >= 7
