"""Squares and square roots: topic placement and difficulty forms."""

from __future__ import annotations

import random
import re

from question_engine.catalogs.pre_algebra import CATALOG as PA_CATALOG
from question_engine.core.base import QUESTION_TYPES
from question_engine.core.registry import get_catalog_entry
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset


def test_pa_squares_catalog_under_factors_and_exponents_not_right_triangles():
    entries = [e for e in PA_CATALOG if e.id == "pa_squares_and_square_roots"]
    assert len(entries) == 1
    entry = entries[0]
    assert entry.category == "Pre-Algebra — Factors and Exponents"
    assert entry.generator == "pa_squares_and_square_roots"

    right_ids = {e.id for e in PA_CATALOG if e.category == "Pre-Algebra — Right Triangles"}
    assert "pa_squares_and_square_roots" not in right_ids
    assert "pythagorean_theorem" in right_ids


def test_pa_squares_difficulty_presets():
    easy = lookup_difficulty_preset("easy", type_id="pa_squares_and_square_roots")
    medium = lookup_difficulty_preset("medium", type_id="pa_squares_and_square_roots")
    hard = lookup_difficulty_preset("hard", type_id="pa_squares_and_square_roots")

    assert easy["perfect_squares_only"] is True
    assert easy["allow_squares"] is True
    assert easy["allow_square_roots"] is True
    assert easy["allow_extract_square_factors"] is False
    assert easy["base_max"] <= 12

    assert medium["perfect_squares_only"] is True
    assert medium["base_min"] >= 10
    assert medium["base_max"] > easy["base_max"]

    assert hard["perfect_squares_only"] is False
    assert hard["allow_extract_square_factors"] is True
    assert hard["base_max"] >= medium["base_max"]


def test_pa_squares_easy_mix_perfect_roots_and_squares():
    qt = QUESTION_TYPES["pa_squares_and_square_roots"]
    random.seed(42)
    qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "easy", "count": 40, "include_answer_key": True},
            type_id="pa_squares_and_square_roots",
        )
    )

    root_re = re.compile(r"^\\sqrt\{(\d+)\}$")
    square_re = re.compile(r"^(\d+)\^\{2\}$")
    word_re = re.compile(r"squared")

    saw_root = saw_square = saw_word = False
    for q in qs:
        assert q.topic == "pa_squares_and_square_roots"
        m_root = root_re.match(q.prompt_latex)
        m_square = square_re.match(q.prompt_latex)
        if m_root:
            saw_root = True
            rad = int(m_root.group(1))
            root = int(rad**0.5)
            assert root * root == rad
            assert q.answer_latex == str(root)
        elif m_square:
            saw_square = True
            n = int(m_square.group(1))
            assert q.answer_latex == str(n * n)
        elif word_re.search(q.prompt_latex):
            saw_word = True
            assert q.answer_latex is not None
            assert q.answer_latex.isdigit()
        else:
            raise AssertionError(f"Unexpected easy prompt: {q.prompt_latex}")

    assert saw_root and saw_square and saw_word


def test_pa_squares_medium_larger_perfects_hard_allows_non_perfect():
    qt = QUESTION_TYPES["pa_squares_and_square_roots"]

    random.seed(3)
    medium_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "medium", "count": 30, "include_answer_key": True},
            type_id="pa_squares_and_square_roots",
        )
    )
    for q in medium_qs:
        m = re.match(r"^\\sqrt\{(\d+)\}$", q.prompt_latex)
        if m:
            rad = int(m.group(1))
            root = int(rad**0.5)
            assert root * root == rad
            assert 10 <= root <= 25

    random.seed(11)
    hard_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "hard", "count": 40, "include_answer_key": True},
            type_id="pa_squares_and_square_roots",
        )
    )
    non_perfect_or_extract = False
    for q in hard_qs:
        m = re.match(r"^\\sqrt\{(\d+)\}$", q.prompt_latex)
        if not m:
            continue
        rad = int(m.group(1))
        root = int(rad**0.5)
        if root * root != rad:
            non_perfect_or_extract = True
            assert q.answer_latex is not None
            assert "\\sqrt" in q.answer_latex or q.answer_latex.isdigit()
    assert non_perfect_or_extract


def test_pa_squares_type_not_aliased_to_radical_simplification():
    entry = get_catalog_entry("pa_squares_and_square_roots")
    assert entry.generator == "pa_squares_and_square_roots"
    assert "pa_squares_and_square_roots" in QUESTION_TYPES
    # Right-triangle topics must not reuse this generator as radical_simplification alias.
    assert QUESTION_TYPES["pa_squares_and_square_roots"].category == (
        "Pre-Algebra — Factors and Exponents"
    )
