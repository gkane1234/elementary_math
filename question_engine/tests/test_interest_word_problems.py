"""Regression tests for simple / compound interest word problems."""

from __future__ import annotations

import random
import re

from question_engine.frameworks.word_problem import InterestWordProblemFramework


def _parse_money(answer: str | None) -> float:
    assert answer is not None
    cleaned = str(answer).replace(r"\$", "").replace("$", "").replace(",", "")
    return float(cleaned)


def test_simple_interest_find_interest_matches_prt():
    fw = InterestWordProblemFramework()
    hits = 0
    for seed in range(120):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt(
            {"difficulty": "easy", "interest_kind": "simple"}
        )
        if "How much interest is earned?" not in text:
            continue
        if "compounded" in text:
            continue
        m = re.search(
            r"invests \$([\d.]+) at ([\d.]+)% simple interest for (\d+) years?",
            text,
        )
        assert m, text
        p, r, t = float(m.group(1)), float(m.group(2)), int(m.group(3))
        expected = p * (r / 100.0) * t
        assert abs(_parse_money(answer) - expected) < 0.005, (text, answer)
        hits += 1
    assert hits >= 20, hits


def test_compound_interest_matches_formula():
    fw = InterestWordProblemFramework()
    freq_to_n = {
        "annually": 1,
        "semiannually": 2,
        "quarterly": 4,
        "monthly": 12,
    }
    hits = 0
    for seed in range(150):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt(
            {"difficulty": "hard", "interest_kind": "compound"}
        )
        if "balance at the end" not in text:
            continue
        m = re.search(
            r"invests \$([\d.]+) (?:in an account that pays |at )([\d.]+)% interest "
            r"compounded (\w+) for (\d+) years?",
            text,
        )
        assert m, text
        p, r, freq, t = (
            float(m.group(1)),
            float(m.group(2)),
            m.group(3),
            int(m.group(4)),
        )
        n = freq_to_n[freq]
        expected = p * (1 + r / (100 * n)) ** (n * t)
        assert abs(_parse_money(answer) - expected) < 0.015, (text, answer, expected)
        hits += 1
    assert hits >= 15, hits


def test_pa_interest_never_asks_for_rate_principal_or_time():
    """G6/PA interest is forward plug-in only (find I or A given P, r, t)."""
    fw = InterestWordProblemFramework()
    banned = (
        "annual interest rate",
        "What was the principal?",
        "How many years does this take?",
        "interest rate?",
    )
    forward_ok = 0
    for seed in range(250):
        random.seed(seed)
        for difficulty in ("easy", "medium", "hard", 0, 8, 14, 22):
            _latex, text, answer = fw.build_prompt({"difficulty": difficulty})
            lowered = text.lower()
            assert not any(b.lower() in lowered for b in banned), text
            assert "%" in text or "\\%" in _latex, text
            assert (
                "how much interest is earned?" in lowered
                or "balance at the end of the term" in lowered
                or "account balance at the end of the term" in lowered
            ), text
            assert answer is not None and answer.startswith("\\$"), (text, answer)
            forward_ok += 1
    assert forward_ok >= 200, forward_ok


def test_no_discount_tax_markup_prompts():
    fw = InterestWordProblemFramework()
    banned = ("sale for", "sales tax", "marks up", "selling price", "sale price")
    for seed in range(80):
        random.seed(seed)
        for difficulty in ("easy", "medium", "hard"):
            _latex, text, _answer = fw.build_prompt({"difficulty": difficulty})
            lowered = text.lower()
            assert not any(b in lowered for b in banned), text
            assert "interest" in lowered or "compounded" in lowered, text


def test_easy_simple_interest_is_whole_dollars_when_finding_i():
    fw = InterestWordProblemFramework()
    for seed in range(60):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt(
            {"difficulty": "easy", "interest_kind": "simple"}
        )
        if "How much interest is earned?" not in text:
            continue
        value = _parse_money(answer)
        assert abs(value - round(value)) < 1e-9, (text, answer)
