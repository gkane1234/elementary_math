"""Similar-figures types should default to paired-figure diagrams."""

from __future__ import annotations

import random

from question_engine.diagrams import similar_figures_pair_figure
from question_engine.frameworks.geometry import SimilarTrianglesFramework
from question_engine.frameworks.geometry_extended import RemainingGeometryFramework
from question_engine.frameworks.word_problem import SimilarFiguresWordFramework
from question_engine.generators.word_problems import GENERATORS as WP


def test_similar_figures_pair_emits_svg():
    fig = similar_figures_pair_figure(
        shape="triangle",
        small_labels=("A", "B", "C"),
        large_labels=("D", "E", "F"),
        small_side_labels={"AB": "4 cm", "BC": "6 cm"},
        large_side_labels={"DE": "8 cm", "EF": "?"},
        scale_factor=2,
    )
    meta = fig.to_metadata()
    assert "<svg" in meta["diagram_svg"]
    assert "A" in meta["diagram_svg"] and "F" in meta["diagram_svg"]
    assert "?" in meta["diagram_svg"]


def test_wp_similar_figures_default_has_diagram():
    random.seed(11)
    gen = WP["wp_similar_figures"]
    with_diagram = 0
    for _ in range(12):
        q = gen("pa_similar_figures", {"count": 1, "prompt_style": "diagram"})[0]
        if (q.metadata or {}).get("diagram_svg"):
            with_diagram += 1
            assert "<svg" in q.metadata["diagram_svg"]
    assert with_diagram >= 10


def test_wp_similar_figures_description_only_skips_diagram():
    random.seed(12)
    gen = WP["wp_similar_figures"]
    for _ in range(8):
        q = gen(
            "pa_similar_figures",
            {"count": 1, "prompt_style": "description_only", "include_figure": False},
        )[0]
        assert not (q.metadata or {}).get("diagram_svg")
        assert "similar" in (q.prompt_text or "").lower()


def test_geo_similar_triangles_default_has_pair_diagram():
    random.seed(13)
    fw = SimilarTrianglesFramework()
    with_diagram = 0
    for _ in range(10):
        q = fw.generate_batch(
            "geo_similarity_similar_triangles",
            {"count": 1, "prompt_style": "diagram", "include_diagram": True},
        )[0]
        svg = (q.metadata or {}).get("diagram_svg") or ""
        if svg:
            with_diagram += 1
            assert "A" in svg and "D" in svg
    assert with_diagram >= 9


def test_geo_similar_triangles_description_only_skips_svg():
    random.seed(14)
    q = SimilarTrianglesFramework().generate_batch(
        "geo_similarity_similar_triangles",
        {
            "count": 1,
            "prompt_style": "description_only",
            "include_figure": False,
            "include_diagram": False,
        },
    )[0]
    assert not (q.metadata or {}).get("diagram_svg")
    assert "Find" in (q.prompt_latex or "")


def test_geo_similar_polygons_default_has_diagram():
    random.seed(15)
    q = RemainingGeometryFramework("similar_polygons").generate_batch(
        "geo_similarity_similar_polygons",
        {"count": 1, "prompt_style": "diagram", "include_diagram": True},
    )[0]
    svg = (q.metadata or {}).get("diagram_svg") or ""
    assert "<svg" in svg
    assert "A" in svg and "E" in svg
