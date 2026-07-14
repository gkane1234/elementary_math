"""Regression tests for simple / compound interest word problems."""

from __future__ import annotations

import random
import re

from question_engine.frameworks.word_problem import InterestWordProblemFramework


def _parse_money(answer: str | None) -> float:
    assert answer is not None
    cleaned = str(answer).replace(r"\$", "").replace("$", "").replace(",", "")
    return float(cleaned)


def _parse_percent(answer: str | None) -> float:
    assert answer is not None
    cleaned = str(answer).replace(r"\%", "").replace("%", "").strip()
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


def test_simple_find_rate_and_principal():
    fw = InterestWordProblemFramework()
    rate_hits = 0
    principal_hits = 0
    for seed in range(200):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt(
            {"difficulty": "hard", "interest_kind": "simple"}
        )
        if "What is the annual interest rate?" in text:
            m = re.search(
                r"invests \$([\d.]+) and earns \$([\d.]+) in simple interest after "
                r"(\d+) years?",
                text,
            )
            assert m, text
            p, interest, t = float(m.group(1)), float(m.group(2)), int(m.group(3))
            expected = (interest / (p * t)) * 100
            assert abs(_parse_percent(answer) - expected) < 0.05, (text, answer)
            rate_hits += 1
        elif "What was the principal?" in text:
            m = re.search(
                r"earned \$([\d.]+) in simple interest after (\d+) years? at "
                r"([\d.]+)% per year",
                text,
            )
            assert m, text
            interest, t, r = float(m.group(1)), int(m.group(2)), float(m.group(3))
            expected = interest / ((r / 100.0) * t)
            assert abs(_parse_money(answer) - expected) < 0.015, (text, answer)
            principal_hits += 1
    assert rate_hits >= 5, rate_hits
    assert principal_hits >= 5, principal_hits


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
