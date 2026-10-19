"""Topic-fit form scores stay independent of effort and tilt form choice."""

from __future__ import annotations

import random

from question_engine.api.handler import _attach_form_quality_weights, _generate_for_type
from question_engine.frameworks.primitives.openstax_form_catalogs import select_form_id
from question_engine.ml.form_quality import FormQualityStore, difficulty_band, record_from_rated_item
import question_engine.types  # noqa: F401


def _forms() -> list[dict]:
    return [
        {"form_id": "plain", "d_min": 0, "d_weight": 1.0},
        {"form_id": "favored", "d_min": 0, "d_weight": 1.0},
    ]


def test_rating_is_centered_and_banded(tmp_path) -> None:
    store = FormQualityStore(tmp_path / "scores.json")
    low = store.record(type_id="calc_diff_quotient_rule", form_id="quotient_poly", difficulty=2, rating_1_to_5=5)
    mid = store.record(type_id="calc_diff_quotient_rule", form_id="quotient_poly", difficulty=8, rating_1_to_5=1)
    assert difficulty_band(2) == "low"
    assert difficulty_band(8) == "mid"
    assert low["centered_sum"] == 2
    assert mid["centered_sum"] == -2
    assert store.weights("calc_diff_quotient_rule", 8) == {"quotient_poly": -2 / 5}
    assert store.weights("calc_diff_quotient_rule", 2) == {"quotient_poly": 2 / 5}


def test_shrink_keeps_one_rating_from_dominating(tmp_path) -> None:
    store = FormQualityStore(tmp_path / "scores.json")
    store.record(type_id="topic", form_id="a", difficulty=6, rating_1_to_5=5)
    for _ in range(50):
        store.record(type_id="topic", form_id="b", difficulty=6, rating_1_to_5=4)
    weights = store.weights("topic", 6)
    assert weights["a"] == 2 / 5
    assert weights["b"] > weights["a"]


def test_generate_attaches_weights_without_reading_effort(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("FORM_QUALITY_PATH", str(tmp_path / "scores.json"))
    FormQualityStore().record(
        type_id="calc_diff_quotient_rule",
        form_id="quotient_poly",
        difficulty=6,
        rating_1_to_5=5,
    )
    attached = _attach_form_quality_weights(
        "calc_diff_quotient_rule",
        {"difficulty": 6, "y_effort": 99},
    )
    assert attached["live_quality_form_weights"] == {"quotient_poly": 2 / 5}
    assert "y_effort" not in FormQualityStore().load()["rows"]
    caller = _attach_form_quality_weights(
        "calc_diff_quotient_rule",
        {"difficulty": 6, "live_quality_form_weights": {"other": 1.0}},
    )
    assert caller["live_quality_form_weights"] == {"other": 1.0}


def test_positive_score_is_sampled_more_often() -> None:
    favored = 0
    for seed in range(200):
        picked = select_form_id(
            _forms(),
            d=6,
            rng=random.Random(seed),
            quality_weights={"favored": 2.0, "plain": 0.0},
        )
        if picked["form_id"] == "favored":
            favored += 1
    assert favored > 150


def test_live_rating_item_updates_the_store(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("FORM_QUALITY_PATH", str(tmp_path / "scores.json"))
    recorded = record_from_rated_item(
        {
            "rating_1_to_5": 4,
            "theta_requested": {"type_id": "calc_diff_quotient_rule", "difficulty": 9},
            "metadata": {"form_id": "quotient_poly", "y_effort": 12},
        }
    )
    assert recorded is not None
    assert recorded["centered_sum"] == 1
    assert record_from_rated_item({"rating_1_to_5": 5, "metadata": {}}) is None


def test_generate_for_type_puts_weights_on_the_question(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("FORM_QUALITY_PATH", str(tmp_path / "scores.json"))
    FormQualityStore().record(
        type_id="calc_diff_quotient_rule",
        form_id="quotient_poly",
        difficulty=6,
        rating_1_to_5=5,
    )
    questions = _generate_for_type(
        "calc_diff_quotient_rule",
        {"count": 1, "difficulty": 6, "include_answer_key": True},
    )
    weights = questions[0].metadata["generation_settings"]["live_quality_form_weights"]
    assert weights["quotient_poly"] == 2 / 5
