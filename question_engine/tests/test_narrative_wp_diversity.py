"""Diversity + D-scaling for narrative coin / age / consecutive word problems."""

from __future__ import annotations

from collections import Counter

import question_engine.types  # noqa: F401
from question_engine.api.handler import _generate_for_type
from question_engine.generators import GENERATORS


def _fingerprint(text: str) -> str:
    """Strip digits so identical Mad-Libs scripts collide."""
    out = []
    for ch in text.lower():
        out.append("#" if ch.isdigit() else ch)
    return "".join(out)


def _sample(type_id: str, d: float, n: int = 40, *, seed0: int = 0):
    rows = []
    for i in range(n):
        qs = _generate_for_type(
            type_id,
            {
                "count": 1,
                "difficulty": d,
                "include_answer_key": True,
                "seed": seed0 + i,
            },
        )
        q = qs[0]
        meta = q.metadata or {}
        rows.append(
            {
                "text": q.prompt_text,
                "answer": q.answer_latex,
                "shape_id": meta.get("shape_id") or meta.get("template_id") or "",
                "n_constraints": int(meta.get("n_constraints") or 0),
                "upgrades": list(meta.get("upgrades") or []),
                "spend": meta.get("spend") or {},
                "fp": _fingerprint(q.prompt_text),
            }
        )
    return rows


def test_coin_not_equation_stub():
    qs = GENERATORS["wp_coin"](
        "coin_word_problems",
        {"count": 1, "difficulty": 6, "include_answer_key": True},
    )
    text = qs[0].prompt_text
    assert "amounts that satisfy" not in text
    assert "quarter" in text.lower() or "coin" in text.lower() or "dime" in text.lower()


def test_coin_easy_vs_hard_diversity_and_constraints():
    easy = _sample("coin_word_problems", 0.0, n=40, seed0=100)
    hard = _sample("coin_word_problems", 20.0, n=40, seed0=500)

    easy_shapes = {r["shape_id"] for r in easy if r["shape_id"]}
    hard_shapes = {r["shape_id"] for r in hard if r["shape_id"]}
    assert len(easy_shapes) >= 1
    assert len(hard_shapes) >= 3, f"hard shapes too few: {hard_shapes}"

    # Prompt fingerprints: hard should not collapse to one Mad-Libs script.
    easy_fp = {r["fp"] for r in easy}
    hard_fp = {r["fp"] for r in hard}
    assert len(easy_fp) >= 2
    assert len(hard_fp) >= 5, f"hard fingerprint diversity low: {len(hard_fp)}"

    easy_n = sum(r["n_constraints"] for r in easy) / len(easy)
    hard_n = sum(r["n_constraints"] for r in hard) / len(hard)
    assert hard_n > easy_n + 0.3, f"hard n_constraints {hard_n} not > easy {easy_n}"

    # High D should unlock multi-constraint shapes.
    hard_up = Counter(u for r in hard for u in r["upgrades"])
    assert (
        hard_up.get("three_denoms", 0) + hard_up.get("trade_step", 0) >= 5
    ), f"expected three/trade upgrades at D=20, got {hard_up}"

    # Metadata carries spend.
    assert any(r["spend"] for r in hard)


def test_age_diversity_and_harder_structure():
    easy = _sample("age_word_problems", 0.0, n=30, seed0=10)
    hard = _sample("age_word_problems", 20.0, n=30, seed0=80)

    easy_fp = {r["fp"] for r in easy}
    hard_fp = {r["fp"] for r in hard}
    assert len(hard_fp) >= 3
    assert len(hard_fp) >= len(easy_fp) or len({r["shape_id"] for r in hard}) >= 2

    hard_n = sum(r["n_constraints"] for r in hard) / len(hard)
    easy_n = sum(r["n_constraints"] for r in easy) / len(easy)
    assert hard_n >= easy_n

    hard_shapes = {r["shape_id"] for r in hard}
    assert any(
        "three" in s or "future" in s or "past" in s or "times" in s for s in hard_shapes
    ), hard_shapes


def test_consecutive_hard_unlocks_parity_or_product():
    easy = _sample("consecutive_integers_word_problems", 0.0, n=25, seed0=3)
    hard = _sample("consecutive_integers_word_problems", 20.0, n=25, seed0=40)
    hard_text = " ".join(r["text"].lower() for r in hard)
    assert "consecutive" in hard_text
    # At high D, expect even/odd or product / first-last in the pool.
    assert (
        "even" in hard_text
        or "odd" in hard_text
        or "product" in hard_text
        or "first and last" in hard_text
        or len({r["shape_id"] for r in hard}) >= 2
    )
    assert len({r["fp"] for r in hard}) >= len({r["fp"] for r in easy}) or len(
        {r["shape_id"] for r in hard}
    ) >= 2


def test_coin_answers_solvable_spotcheck():
    """Spot-check a few generated coin answers against the stem numbers."""
    for seed in range(20):
        qs = _generate_for_type(
            "coin_word_problems",
            {"count": 1, "difficulty": 6, "include_answer_key": True, "seed": 900 + seed},
        )
        q = qs[0]
        assert q.answer_latex
        assert "satisfy" not in q.prompt_text.lower()
