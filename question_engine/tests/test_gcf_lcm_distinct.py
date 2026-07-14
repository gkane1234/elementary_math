"""GCF/LCM prompts must use distinct numbers (no GCF(a,a) / LCM(a,a))."""

from __future__ import annotations

import math
import random
import re

from question_engine.frameworks.number import (
    GcfLcmFramework,
    GcfLcmWordFramework,
    _sample_gcf_pair,
    _sample_lcm_pair,
    _sample_values_for_gcf,
)
from question_engine.frameworks.word_problem import GcfLcmWordFramework as WpGcfLcmWordFramework

_SETTINGS = {
    "count": 1,
    "include_answer_key": True,
    "factor_min": 4,
    "factor_max": 60,
    "require_gcf_greater_than_one": True,
}


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
        prompt, kind, _ = number_fw.build_prompt(_SETTINGS)
        nums = [int(n) for n in re.findall(r"\b(\d+)\b", prompt)]
        assert len(nums) >= 2
        assert nums[0] != nums[1], prompt
        assert "GCF" in kind or "LCM" in kind

        latex, text, _ = wp_fw.build_prompt(_SETTINGS)
        blob = f"{latex}\n{text}"
        amounts = [int(n) for n in re.findall(r"\b(\d+)\b", blob)]
        assert len(amounts) >= 2
        assert amounts[0] != amounts[1], blob
