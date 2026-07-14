"""Regression: markup / discount / tax / tip keys match calculator cents math."""

from __future__ import annotations

import random
import re
from decimal import Decimal, ROUND_HALF_UP

from question_engine.frameworks.word_problem import PercentWordProblemFramework
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset


def _round_cents(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _parse_money(answer: str | None) -> Decimal:
    assert answer is not None
    cleaned = str(answer).replace(r"\$", "").replace("$", "").replace("\\", "").strip()
    return Decimal(cleaned)


def _parse_prompt_money(text: str, pattern: str) -> Decimal:
    m = re.search(pattern, text)
    assert m, text
    return Decimal(m.group(1))


def test_wp_percent_presets_differ_by_tier():
    easy = lookup_difficulty_preset("easy", type_id="pa_markup_discount_and_tax")
    medium = lookup_difficulty_preset("medium", type_id="pa_markup_discount_and_tax")
    hard = lookup_difficulty_preset("hard", type_id="pa_markup_discount_and_tax")
    assert easy["allow_price_cents"] is False
    assert easy["allow_multi_step"] is False
    assert medium["allow_price_cents"] is True
    assert medium["allow_decimal_rates"] is True
    assert medium["allow_multi_step"] is False
    assert hard["allow_multi_step"] is True
    assert hard["allow_decimal_rates"] is True


def test_markup_discount_tax_answers_match_calculator():
    fw = PercentWordProblemFramework()
    seen = {"discount": 0, "tax": 0, "markup": 0, "tip": 0, "multi": 0}

    for tier in ("easy", "medium", "hard"):
        settings = apply_difficulty_presets(
            {"difficulty_tier": tier, "count": 1},
            type_id="pa_markup_discount_and_tax",
        )
        for seed in range(40):
            random.seed(seed + hash(tier) % 10_000)
            _latex, text, answer = fw.build_prompt(settings)
            keyed = _parse_money(answer)

            if "final price" in text:
                seen["multi"] += 1
                m = re.search(
                    r"priced at \$([0-9]+(?:\.[0-9]+)?)\. "
                    r"It is ([0-9]+(?:\.[0-9]+)?)% off, and then "
                    r"([0-9]+(?:\.[0-9]+)?)% sales tax is added",
                    text,
                )
                assert m, text
                price = Decimal(m.group(1))
                discount = Decimal(m.group(2))
                tax = Decimal(m.group(3))
                sale = _round_cents(price * (Decimal(100) - discount) / Decimal(100))
                expected = _round_cents(sale * (Decimal(100) + tax) / Decimal(100))
                assert keyed == expected, text

            elif "on sale for" in text:
                seen["discount"] += 1
                price = _parse_prompt_money(
                    text, r"priced at \$([0-9]+(?:\.[0-9]+)?)\. It is on sale for"
                )
                rate = Decimal(
                    re.search(r"on sale for ([0-9]+(?:\.[0-9]+)?)% off", text).group(1)
                )
                expected = _round_cents(price * (Decimal(100) - rate) / Decimal(100))
                assert keyed == expected, text

            elif "sales tax added" in text:
                seen["tax"] += 1
                price = _parse_prompt_money(
                    text, r"A \$([0-9]+(?:\.[0-9]+)?) purchase has"
                )
                rate = Decimal(
                    re.search(r"has ([0-9]+(?:\.[0-9]+)?)% sales tax", text).group(1)
                )
                expected = _round_cents(price * (Decimal(100) + rate) / Decimal(100))
                assert keyed == expected, text

            elif "marks up" in text:
                seen["markup"] += 1
                price = _parse_prompt_money(
                    text, r"marks up a \$([0-9]+(?:\.[0-9]+)?) item by"
                )
                rate = Decimal(
                    re.search(r"by ([0-9]+(?:\.[0-9]+)?)%", text).group(1)
                )
                expected = _round_cents(price * (Decimal(100) + rate) / Decimal(100))
                assert keyed == expected, text

            elif "tip" in text:
                seen["tip"] += 1
                price = _parse_prompt_money(
                    text, r"tip on a \$([0-9]+(?:\.[0-9]+)?) bill"
                )
                rate = Decimal(
                    re.search(r"leaves a ([0-9]+(?:\.[0-9]+)?)% tip", text).group(1)
                )
                if "How much is the tip" in text:
                    expected = _round_cents(price * rate / Decimal(100))
                else:
                    expected = _round_cents(price * (Decimal(100) + rate) / Decimal(100))
                assert keyed == expected, text

            else:
                raise AssertionError(f"Unrecognized prompt: {text}")

            # Easy/Medium: no discount-then-tax multi-step
            if tier in {"easy", "medium"}:
                assert "final price" not in text

    assert seen["discount"] > 0
    assert seen["tax"] > 0
    assert seen["markup"] > 0
    assert seen["tip"] > 0


def test_easy_avoids_price_cents_and_decimal_rates():
    fw = PercentWordProblemFramework()
    settings = apply_difficulty_presets(
        {"difficulty_tier": "easy"},
        type_id="pa_markup_discount_and_tax",
    )
    for seed in range(60):
        random.seed(seed)
        _latex, text, _answer = fw.build_prompt(settings)
        # Whole-dollar prices in prompts (no cents shown).
        for m in re.finditer(r"\$([0-9]+(?:\.[0-9]+)?)", text):
            assert "." not in m.group(1), text
        # Integer percent rates only.
        for m in re.finditer(r"([0-9]+(?:\.[0-9]+)?)%", text):
            assert "." not in m.group(1), text


def test_known_truncation_bug_fixed():
    """Former //100 construction keyed $85 @ 15% tax as $97 instead of $97.75."""
    fw = PercentWordProblemFramework()
    settings = {
        "difficulty": "easy",
        "allow_discount": False,
        "allow_tax": True,
        "allow_markup": False,
        "allow_tip": False,
        "allow_price_cents": False,
        "allow_decimal_rates": False,
        "allow_multi_step": False,
    }
    # Force the formerly-broken numbers via monkeypatching samplers.
    fw._sample_price = staticmethod(lambda _s, _t: Decimal(85))  # type: ignore[method-assign]
    fw._sample_rate = staticmethod(lambda _s, _t, _v: Decimal(15))  # type: ignore[method-assign]
    _latex, text, answer = fw.build_prompt(settings)
    assert "85" in text and "15%" in text
    assert _parse_money(answer) == Decimal("97.75")
