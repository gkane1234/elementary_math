"""Geometric plane transformations — not function/quadratic graph transforms."""

from __future__ import annotations

import random

from question_engine.core.registry import get_catalog_entry
from question_engine.frameworks.geometry_extended import GeometricTransformationsFramework
from question_engine.generators.geometry import GENERATORS
from question_engine.qa.topic_fit import check_miswire
from question_engine.settings.presets import apply_difficulty_presets


def test_pa_transformations_not_wired_to_quadratic_graph():
    entry = get_catalog_entry("pa_transformations")
    assert entry.generator == "geo_transformations"
    fails, _ = check_miswire(entry.id, entry.generator)
    assert not any("graph_transformations" in f for f in fails)


def test_miswire_flag_for_old_quadratic_alias():
    fails, _ = check_miswire("pa_transformations", "graph_transformations")
    assert any("geometric shape transforms" in f for f in fails)


def test_geo_catalog_uses_geo_transformations():
    entry = get_catalog_entry(
        "geo_transformations_translations_rotations_reflections_and_dilations"
    )
    assert entry.generator == "geo_transformations"


def test_samples_are_geometric_not_quadratic():
    random.seed(7)
    fw = GeometricTransformationsFramework()
    for tier in ("easy", "medium", "hard"):
        settings = apply_difficulty_presets(
            {
                "count": 1,
                "include_answer_key": True,
                "difficulty_tier": tier,
                "include_graph_metadata": True,
                "include_diagram": True,
            },
            type_id="pa_transformations",
        )
        qs = fw.generate_batch("pa_transformations", settings)
        assert len(qs) == 1
        prompt = qs[0].prompt_latex
        assert "x^2" not in prompt
        assert "f(x)" not in prompt
        assert "translation of } f(x)" not in prompt
        low = prompt.lower()
        assert any(
            token in low or token in prompt
            for token in (
                "triangle",
                "rectangle",
                "square",
                "parallelogram",
                "quadrilateral",
                r"\triangle",
            )
        )
        meta = qs[0].metadata or {}
        assert meta.get("kind") == "geometric_transformation"
        assert meta.get("image_points")
        assert meta.get("answer_graph_spec") or meta.get("diagram_svg")
        if tier == "easy":
            assert "translat" in low or "translated" in prompt
        if tier == "medium":
            assert "dilat" not in low


def test_generator_registry_key():
    assert "geo_transformations" in GENERATORS
