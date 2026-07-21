"""GCF/LCM prompts must use distinct numbers and distinct nouns."""

from __future__ import annotations

import math
import random
import re

from question_engine.frameworks.number import (
    GcfLcmFramework,
    GcfLcmWordFramework,
    _factor_bounds,
    _sample_gcf_pair,
    _sample_lcm_pair,
    _sample_values_for_gcf,
)
from question_engine.frameworks.word_problem import GcfLcmWordFramework as WpGcfLcmWordFramework
from question_engine.word_problems.things import (
    SAME_LETTER_MIN_DIFFICULTY,
    THINGS_BY_LETTER,
    first_letter,
    pick_things,
)

_SETTINGS = {
    "count": 1,
    "include_answer_key": True,
    "factor_min": 4,
    "factor_max": 60,
    "require_gcf_greater_than_one": True,
}

_NOUN_RE = re.compile(
    r"(?:You have \d+ (\S+) and \d+ (\S+)\.|(\S+) come in packs of \d+ and (\S+) come in packs of \d+\.)"
)


def _nouns_from_word_prompt(prompt: str) -> tuple[str, str]:
    """Extract the two plural nouns from a GCF/LCM word prompt."""
    match = _NOUN_RE.search(prompt)
    assert match, prompt
    if match.group(1) and match.group(2):
        return match.group(1), match.group(2).rstrip(".")
    return match.group(3), match.group(4)


def _numbers_from_gcf_lcm_prompt(prompt: str) -> list[int]:
    """Parse integers listed after 'of' in a Find-the-GCF/LCM prompt."""
    match = re.search(r"of\s*\}?\s*([\d,\s]+)", prompt)
    assert match, prompt
    return [int(p.strip()) for p in match.group(1).split(",") if p.strip()]


def test_sample_values_for_gcf_are_distinct():
    random.seed(7)
    for count in (2, 3):
        for require_gt_one in (True, False):
            for _ in range(80):
                values = _sample_values_for_gcf(
                    4, 60, count, require_gt_one=require_gt_one
                )
                assert len(values) == count
                assert len(set(values)) == count
                if require_gt_one:
                    assert math.gcd(*values) >= 2


def test_sample_gcf_and_lcm_pairs_are_distinct():
    random.seed(19)
    for require_gt_one in (True, False):
        for _ in range(80):
            a, b, g = _sample_gcf_pair(4, 60, require_gt_one=require_gt_one)
            assert a != b
            assert math.gcd(a, b) == g
            if require_gt_one:
                assert g >= 2
    for _ in range(80):
        a, b = _sample_lcm_pair(4, 60)
        assert a != b


def test_gcf_lcm_framework_prompts_use_distinct_numbers():
    random.seed(23)
    for mode in ("gcf", "lcm"):
        framework = GcfLcmFramework(mode=mode)
        for _ in range(60):
            prompt, _, answer = framework.build_prompt(_SETTINGS)
            values = _numbers_from_gcf_lcm_prompt(prompt)
            assert len(values) >= 2
            assert len(set(values)) == len(values), prompt
            if mode == "gcf":
                assert str(math.gcd(*values)) == answer
            else:
                assert str(math.lcm(*values)) == answer


def test_gcf_lcm_word_frameworks_use_distinct_amounts():
    random.seed(29)
    number_fw = GcfLcmWordFramework()
    wp_fw = WpGcfLcmWordFramework()
    for _ in range(80):
        prompt, text, _ = number_fw.build_prompt(_SETTINGS)
        nums = [int(n) for n in re.findall(r"\b(\d+)\b", prompt)]
        assert len(nums) >= 2
        assert nums[0] != nums[1], prompt
        assert "bags" in text or "packs" in text

        latex, text, _ = wp_fw.build_prompt(_SETTINGS)
        blob = f"{latex}\n{text}"
        amounts = [int(n) for n in re.findall(r"\b(\d+)\b", blob)]
        assert len(amounts) >= 2
        assert amounts[0] != amounts[1], blob


def test_pick_things_never_duplicates_and_prefers_distinct_letters():
    rng = random.Random(41)
    for _ in range(100):
        a, b = pick_things(2, rng=rng, prefer_same_first_letter=False)
        assert a != b
        assert first_letter(a) != first_letter(b)


def test_pick_things_can_prefer_same_first_letter():
    rng = random.Random(43)
    same = 0
    for _ in range(80):
        a, b = pick_things(2, rng=rng, prefer_same_first_letter=True)
        assert a != b
        if first_letter(a) == first_letter(b):
            same += 1
    # Letters with ≥2 nouns dominate the bank; expect mostly same-letter pairs.
    assert same >= 60


def test_gcf_lcm_word_low_d_distinct_nouns_and_letters():
    random.seed(47)
    fw = GcfLcmWordFramework()
    settings = {**_SETTINGS, "difficulty": 0}
    bank = {t for vals in THINGS_BY_LETTER.values() for t in vals}
    for _ in range(60):
        prompt, text, _ = fw.build_prompt(settings)
        assert prompt == f"\\text{{{text}}}"
        n1, n2 = _nouns_from_word_prompt(text)
        assert n1.lower() != n2.lower(), text
        assert first_letter(n1) != first_letter(n2), text
        assert n1.lower() in bank
        assert n2.lower() in bank


def test_gcf_lcm_word_high_d_can_share_first_letter():
    random.seed(53)
    fw = GcfLcmWordFramework()
    settings = {**_SETTINGS, "difficulty": SAME_LETTER_MIN_DIFFICULTY}
    shared = 0
    for _ in range(80):
        _prompt, text, _ = fw.build_prompt(settings)
        n1, n2 = _nouns_from_word_prompt(text)
        assert n1.lower() != n2.lower(), text
        if first_letter(n1) == first_letter(n2):
            shared += 1
    assert shared >= 40


def test_gcf_lcm_word_continuous_d_scales_factor_bounds():
    lo0, hi0 = _factor_bounds({"difficulty": 0})
    lo20, hi20 = _factor_bounds({"difficulty": 20})
    lo40, hi40 = _factor_bounds({"difficulty": 40})
    assert lo0 == 2 and lo20 == 2 and lo40 == 2
    assert hi0 < hi20 < hi40
    assert hi0 == 12  # continuous_abs_max(base=12) at D=0
