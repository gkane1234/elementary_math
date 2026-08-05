"""Unit checks for live rating stratified-D policy (v1)."""

from __future__ import annotations

from question_engine.ml.live_rating import (
    DIFFICULTY_GRID,
    nearest_grid_bin,
    pick_next_difficulty,
)
from question_engine.ml.knob_introspect import has_continuous_difficulty


def test_nearest_grid_bin():
    assert nearest_grid_bin(7.2) == 8.0
    assert nearest_grid_bin(0.0) == 0.0
    assert nearest_grid_bin(24.0) == 25.0


def test_pick_prefers_underfilled_after_one_band():
    stuffed = [
        {"theta_requested": {"difficulty": 8.0}, "rating_1_to_5": 3}
        for _ in range(5)
    ]
    nxt = pick_next_difficulty(stuffed)
    assert nxt != 8.0
    assert nxt in DIFFICULTY_GRID


def test_empty_starts_mid_grid():
    mid = DIFFICULTY_GRID[len(DIFFICULTY_GRID) // 2]
    assert pick_next_difficulty([]) == mid


def test_g6_ratios_has_continuous_d():
    import question_engine.types  # noqa: F401

    assert has_continuous_difficulty("g6_introduction_to_ratios")
