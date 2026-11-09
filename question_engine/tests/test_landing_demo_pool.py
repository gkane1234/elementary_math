"""The landing demo only offers types whose five bands actually change the sheet.

Bands are D 0–5, 5–10, 10–15, 15–20, and 20–25. The pool is the Grade 6
verified_ramp audit plus the pre-algebra first-tranche verified_ramp topics,
restricted to types where the same seed replays the same five questions, and
adjacent bands produce different prompts, for seeds 1, 7, and 101. One topic
per sheet (no related-topic mix).
"""

from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path

from question_engine.api.handler import handle_generate

ROOT = Path(__file__).resolve().parents[2]
POOL_PATH = ROOT / "config" / "landing-demo-types.json"
G6_TRACKING = ROOT / "scripts" / "output" / "topic_fit" / "g6_difficulty" / "TRACKING.json"

PA_VERIFIED = {
    "pa_naming_decimal_places_and_rounding",
    "pa_writing_numbers_with_words",
    "pa_integers_adding_and_subtracting",
    "pa_integers_multiplying",
    "pa_integers_dividing",
    "pa_factoring",
    "pa_greatest_common_factor",
    "pa_least_common_multiple",
    "pa_simplifying_fractions",
    "pa_converting_fractions_and_decimals",
    "pa_fractions_decimals_and_percents",
    "pa_simple_and_compound_interest",
    "pa_squares_and_square_roots",
}

SEEDS = (1, 7, 101)


def _pool() -> dict:
    return json.loads(POOL_PATH.read_text())


def _sheet(type_id: str, d_min: float, d_max: float, seed: int) -> tuple[tuple[str, ...], tuple[float, ...]]:
    with contextlib.redirect_stdout(io.StringIO()):
        status, _headers, raw = handle_generate(
            {
                "title": type_id,
                "worksheet_settings": {},
                "progressive": {
                    "seeds": [type_id],
                    "count": 5,
                    "d_min": d_min,
                    "d_max": d_max,
                    "include_related": False,
                    "max_topics": 1,
                    "base_settings": {"seed": seed},
                },
            }
        )
    data = json.loads(raw)
    assert status == 200, data.get("error")
    questions = data["questions"]
    prompts = tuple((q.get("prompt_latex") or q.get("prompt_text") or "").strip() for q in questions)
    topics = tuple(q.get("topic") for q in questions)
    diffs = tuple(round(float(d), 6) for d in data["progressive"]["difficulties"])
    assert topics == (type_id,) * 5
    assert all(prompts)
    return prompts, diffs


def test_demo_bands_are_the_five_distinct_ranges():
    pool = _pool()
    assert pool["count"] == 5
    assert pool["start_band"] == 1
    assert [(band["d_min"], band["d_max"]) for band in pool["bands"]] == [
        (0, 5),
        (5, 10),
        (10, 15),
        (15, 20),
        (20, 25),
    ]


def test_demo_types_come_from_the_verified_ramp_audits():
    pool = _pool()
    tracking = json.loads(G6_TRACKING.read_text())
    verified = {
        topic["type_id"]
        for topic in tracking["topics"]
        if topic.get("status") == "verified_ramp"
    }
    ids = [entry["id"] for entry in pool["types"]]
    assert ids
    assert len(ids) == len(set(ids))
    for type_id in ids:
        assert type_id in verified or type_id in PA_VERIFIED


def test_each_demo_band_changes_the_five_questions():
    pool = _pool()
    bands = [(band["d_min"], band["d_max"]) for band in pool["bands"]]
    for entry in pool["types"]:
        type_id = entry["id"]
        for seed in SEEDS:
            sheets = []
            for d_min, d_max in bands:
                prompts, diffs = _sheet(type_id, d_min, d_max, seed)
                again, _again_diffs = _sheet(type_id, d_min, d_max, seed)
                assert prompts == again, (type_id, seed, d_min, d_max)
                expect = tuple(round(d_min + (d_max - d_min) * (i / 4), 6) for i in range(5))
                assert diffs == expect, (type_id, seed, diffs)
                sheets.append(prompts)
            for index in range(len(sheets) - 1):
                assert sheets[index] != sheets[index + 1], (
                    f"{type_id} seed {seed} band {bands[index]} matches {bands[index + 1]}"
                )
