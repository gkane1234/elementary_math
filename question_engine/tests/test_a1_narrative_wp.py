"""A1 narrative WP: OpenStax frames, not dumped equations."""

from __future__ import annotations

from collections import Counter

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.wp_packaging import looks_like_dumped_equation


_TYPES = (
    "mixture_word_problems",
    "distance_rate_time_word_problems",
    "work_word_problems",
    "age_word_problems",
    "coin_word_problems",
    "consecutive_integers_word_problems",
    "percent_word_problems",
)


def _q(type_id: str, d: float, seed: int):
    qs = _generate_for_type(
        type_id,
        {
            "difficulty": d,
            "seed": seed,
            "count": 1,
            "include_answer_key": True,
        },
    )
    assert qs, (type_id, d, seed)
    return qs[0]


def test_d0_is_story_not_dumped_equation():
    for type_id in _TYPES:
        for seed in (101, 207, 313, 419):
            q = _q(type_id, 0.0, seed)
            blob = (q.prompt_latex or "") + " " + (q.prompt_text or "")
            assert not looks_like_dumped_equation(blob), (type_id, seed, blob)
            assert "the equation is" not in blob.lower()
            assert "satisfy $" not in blob
            assert q.answer_latex
            assert (q.metadata or {}).get("frame_id"), (type_id, seed, q.metadata)


def test_multiple_frame_ids_across_seeds():
    for type_id in _TYPES:
        ids = set()
        for seed in range(40):
            q = _q(type_id, 16.0, 200 + seed)
            fid = str((q.metadata or {}).get("frame_id") or "")
            assert fid, (type_id, seed, q.prompt_text)
            ids.add(fid)
        assert len(ids) >= (2 if type_id == "consecutive_integers_word_problems" else 3), (
            type_id,
            ids,
        )


def test_drt_rotates_vehicles_not_one_slow_bus():
    vehicles = Counter()
    frames = Counter()
    slow_bus = 0
    for seed in range(48):
        q = _q("distance_rate_time_word_problems", 16.0, 300 + seed)
        text = (q.prompt_text or "").lower()
        meta = q.metadata or {}
        frames[str(meta.get("frame_id") or "")] += 1
        v = str(meta.get("vehicle") or "")
        if v:
            vehicles[v] += 1
        if "slow bus" in text:
            slow_bus += 1
        blob = text
        for token in ("bike", "bikes", "cyclist", "drives", "walk", "walker", "bus", "train"):
            if token in blob:
                vehicles[token] += 1
                break
    assert slow_bus < 20, slow_bus
    assert len(frames) >= 4, frames
    # Several OpenStax vehicles, not one Mad-Lib.
    distinct = {k for k in vehicles if k in {"bike", "bikes", "cyclist", "drives", "walk", "walker", "bus", "train", "car"}}
    assert len(distinct) >= 3, vehicles


def test_percent_wp_has_percent_of_discount_interest():
    kinds = Counter()
    for seed in range(36):
        q = _q("percent_word_problems", 0.0, 50 + seed)
        fid = str((q.metadata or {}).get("frame_id") or "")
        text = (q.prompt_text or "").lower()
        if fid.startswith("pct_percent_of") or "% of the" in text or "answered" in text or "survey" in text:
            kinds["percent_of"] += 1
        elif "sale" in text or "off" in text or fid == "pct_discount":
            kinds["discount"] += 1
        elif "interest" in text or fid == "pct_interest":
            kinds["interest"] += 1
        else:
            kinds["other"] += 1
    assert kinds["percent_of"] >= 1, kinds
    assert kinds["discount"] >= 1 or kinds["interest"] >= 1, kinds
    assert kinds["other"] == 0, kinds


def test_mixture_high_d_can_find_amount():
    asks = Counter()
    frames = Counter()
    for seed in range(40):
        q = _q("mixture_word_problems", 16.0, 80 + seed)
        fid = str((q.metadata or {}).get("frame_id") or "")
        frames[fid] += 1
        text = (q.prompt_text or "").lower()
        if "how many" in text or "find_amount" in fid:
            asks["find_amount"] += 1
        else:
            asks["blend"] += 1
    assert len(frames) >= 3, frames
    assert asks["find_amount"] >= 1, asks


def test_work_rotates_job_frames():
    frames = Counter()
    for seed in range(30):
        q = _q("work_word_problems", 0.0, 10 + seed)
        frames[str((q.metadata or {}).get("frame_id") or "")] += 1
    assert len(frames) >= 2, frames
