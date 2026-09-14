"""Unit checks for live rating stratified-D policy (v1)."""

from __future__ import annotations

from question_engine.ml.live_rating import (
    DIFFICULTY_GRID,
    nearest_grid_bin,
    pick_next_difficulty,
    ratings_for_engine_rev,
    rotate_ratings_if_engine_changed,
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


def test_ratings_for_engine_rev_isolates_train_set():
    rows = [
        {"engine_rev": "a", "rating_1_to_5": 3},
        {"engine_rev": "b", "rating_1_to_5": 4},
        {"engine_rev": "a", "rating_1_to_5": 2},
    ]
    assert len(ratings_for_engine_rev(rows, "a")) == 2
    assert len(ratings_for_engine_rev(rows, "b")) == 1
    assert len(ratings_for_engine_rev(rows, None)) == 3


def test_rotate_ratings_archives_on_rev_change(tmp_path):
    ratings = tmp_path / "ratings.jsonl"
    ratings.write_text('{"engine_rev":"old","rating_1_to_5":3}\n', encoding="utf-8")
    state = {"engine_rev": "old"}
    rotated = rotate_ratings_if_engine_changed(
        tmp_path, state, ratings, "new"
    )
    assert rotated is True
    assert not ratings.is_file()
    hist = list((tmp_path / "history").glob("ratings.old.*.jsonl"))
    assert len(hist) == 1
    assert state["engine_rev"] == "new"
    assert state["learning_reset"] is True


def test_ratings_for_engine_rev_filters_pairs():
    rows = [
        {"record_kind": "pair", "pair_id": "p1", "engine_rev": "a", "winner": "a",
         "left": {"type_id": "t"}, "right": {"type_id": "t"}},
        {"record_kind": "pair", "pair_id": "p2", "engine_rev": "b", "winner": "b",
         "left": {"type_id": "t"}, "right": {"type_id": "t"}},
        {"engine_rev": "a", "rating_1_to_5": 3},
    ]
    assert len(ratings_for_engine_rev(rows, "a")) == 2
    assert len(ratings_for_engine_rev(rows, "b")) == 1
