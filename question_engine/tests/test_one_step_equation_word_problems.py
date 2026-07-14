"""Regression tests for one-step equation word-problem answers."""

from __future__ import annotations

import random
import re

from question_engine.frameworks.word_problem import OneStepEquationWordFramework


def _dollar_answer(answer: str | None) -> int:
    assert answer is not None
    cleaned = str(answer).replace(r"\$", "").replace("$", "").replace("\\", "")
    return int(cleaned)


def test_one_step_word_problem_answers_match_story():
    """Keyed answers must match the narrative for +, −, ×, and ÷ stories."""
    fw = OneStepEquationWordFramework()
    seen = {"subtract": 0, "add": 0, "multiply": 0, "divide": 0}

    for seed in range(80):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt({})
        keyed = _dollar_answer(answer)

        if "spent" in text and "left" in text:
            seen["subtract"] += 1
            m = re.search(
                r"spent \$(\d+), and has \$(\d+) left\. How much did .+ start with\?",
                text,
            )
            assert m, text
            spent, left = int(m.group(1)), int(m.group(2))
            assert keyed == left + spent

        elif "received" in text and "start with" in text:
            seen["add"] += 1
            m = re.search(
                r"received \$(\d+), and now has \$(\d+)\. How much did .+ start with\?",
                text,
            )
            assert m, text
            received, total = int(m.group(1)), int(m.group(2))
            assert keyed == total - received
            assert keyed > 0

        elif "donations totaling" in text:
            seen["multiply"] += 1
            m = re.search(
                r"collected (\d+) equal donations totaling \$(\d+)\. "
                r"How much was each donation\?",
                text,
            )
            assert m, text
            factor, total = int(m.group(1)), int(m.group(2))
            assert total % factor == 0
            assert keyed == total // factor

        elif "shared" in text and "equally" in text:
            seen["divide"] += 1
            m = re.search(
                r"shared \$(\d+) equally among (\d+) friends\. "
                r"How much did each friend receive\?",
                text,
            )
            assert m, text
            total, factor = int(m.group(1)), int(m.group(2))
            assert total % factor == 0
            assert keyed == total // factor
            # Must not key the total (the original bug).
            assert keyed != total

        else:
            raise AssertionError(f"Unrecognized one-step story: {text}")

    # Seeds should hit every branch; if sampling drifts, this catches it.
    assert all(count >= 5 for count in seen.values()), seen


def test_share_equally_keys_quotient_not_total():
    """Explicit Lucia-style divide case: each friend gets total / friends."""
    fw = OneStepEquationWordFramework()
    # Exhaust seeds until we hit a share-equally story (ops are random).
    for seed in range(40):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt({})
        if "shared" not in text:
            continue
        m = re.search(r"shared \$(\d+) equally among (\d+) friends", text)
        assert m, text
        total, friends = int(m.group(1)), int(m.group(2))
        assert _dollar_answer(answer) == total // friends
        return
    raise AssertionError("No share-equally sample in seeds 0..39")
