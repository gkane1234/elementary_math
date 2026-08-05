"""Figure family registry: diversity under seed + batch index; continuous D unlocks."""

from __future__ import annotations

import random

from question_engine.diagrams.figure_families import (
    FIGURE_FAMILIES,
    TYPE_ID_FAMILY,
    apply_batch_seed,
    complexity_for_difficulty,
    sample_figure,
    sample_figure_from_settings,
)
from question_engine.generators import GENERATORS


def test_registry_has_core_families():
    for fid in (
        "angle_rays",
        "complementary_angles",
        "right_triangle",
        "triangle_area",
        "circle_radius",
        "percent_shade",
        "number_line",
        "function_sketch",
        "decimal_grid",
        "box_plot",
    ):
        assert fid in FIGURE_FAMILIES


def test_sample_figure_unique_under_different_seeds():
    specs = []
    for seed in range(12):
        sample = sample_figure("angle_rays", difficulty=10, seed=seed, batch_index=0, build=True)
        assert sample.figure is not None
        specs.append(
            (
                round(sample.params["base_deg"], 3),
                round(sample.params["measure_deg"], 3),
                sample.figure.to_svg(),
            )
        )
    # Not all clones: orientations or measures must differ across seeds.
    unique_params = {(b, m) for b, m, _ in specs}
    unique_svg = {s for _, _, s in specs}
    assert len(unique_params) >= 4
    assert len(unique_svg) >= 4


def test_batch_index_diversifies_same_seed():
    svgs = []
    for i in range(8):
        sample = sample_figure(
            "complementary_angles",
            difficulty=12,
            seed=42,
            batch_index=i,
            build=True,
        )
        assert sample.figure is not None
        svgs.append(sample.figure.to_svg())
    assert len(set(svgs)) >= 3


def test_higher_d_unlocks_richer_complexity():
    assert complexity_for_difficulty(2) == "simple"
    assert complexity_for_difficulty(8) == "standard"
    assert complexity_for_difficulty(20) == "complex"
    easy = sample_figure("triangle_area", difficulty=2, seed=1)
    hard = sample_figure("triangle_area", difficulty=20, seed=1)
    assert easy.complexity == "simple"
    assert hard.complexity == "complex"
    assert easy.params["layout"] == "right"
    assert hard.params["layout"] in {"right", "interior", "exterior"}


def test_type_id_family_map_covers_high_impact():
    for tid in (
        "geo_basics_classifying_angles",
        "pa_angle_relationships",
        "g6_introduction_to_percents",
        "g6_triangles",
        "geo_right_pythagorean_theorem",
        "geo_parallel_parallel_lines_and_transversals",
        "geo_basics_segment_addition_postulate",
        "g6_decimal_addition_with_diagrams",
        "g6_decimal_multiplication_with_area_diagrams",
        "g6_solving_percent_problems_with_diagrams",
        "calc_app_diff_slope_tangent_and_normal_lines",
    ):
        assert tid in TYPE_ID_FAMILY
        assert TYPE_ID_FAMILY[tid] in FIGURE_FAMILIES


def test_function_sketch_batch_svgs_unique():
    svgs = []
    for i in range(8):
        sample = sample_figure(
            "function_sketch",
            difficulty=18,
            seed=11,
            batch_index=i,
        )
        svg = (sample.diagram_spec or {}).get("diagram_svg") or ""
        assert "<svg" in svg
        svgs.append(svg)
    assert len(set(svgs)) >= 3


def test_decimal_grid_params_vary_with_batch_index():
    styles = []
    for i in range(10):
        sample = sample_figure("decimal_grid", difficulty=16, seed=3, batch_index=i)
        styles.append((sample.params.get("style"), sample.params.get("places")))
    assert len(set(styles)) >= 2


def test_g6_with_diagrams_emit_svg():
    cases = [
        "g6_decimal_addition_with_diagrams",
        "g6_decimal_subtraction_with_diagrams",
        "g6_decimal_multiplication_with_area_diagrams",
        "g6_solving_percent_problems_with_diagrams",
    ]
    from question_engine.core.base import QUESTION_TYPES
    import question_engine.generators  # noqa: F401

    for tid in cases:
        qt = QUESTION_TYPES[tid]
        qs = qt.generate({"count": 6, "seed": 21, "difficulty": 12, "include_answer_key": True})
        with_svg = sum(1 for q in qs if (q.metadata or {}).get("diagram_svg"))
        assert with_svg >= 5, (tid, with_svg)
        fps = set()
        for q in qs:
            meta = q.metadata or {}
            params = meta.get("figure_params") or {}
            param_key = tuple(
                sorted((k, params[k]) for k in params if isinstance(params[k], (int, float, str, bool)))
            )
            fps.add(
                (
                    meta.get("figure_family"),
                    param_key,
                    hash(meta.get("diagram_svg") or ""),
                    hash(meta.get("answer_diagram_svg") or ""),
                )
            )
        assert len(fps) >= 2, (tid, fps)


def test_calc_tangent_attaches_function_sketch():
    from question_engine.core.base import QUESTION_TYPES
    import question_engine.generators  # noqa: F401

    qt = QUESTION_TYPES["calc_app_diff_slope_tangent_and_normal_lines"]
    qs = qt.generate({"count": 5, "seed": 4, "difficulty": 10, "include_answer_key": True})
    with_svg = sum(1 for q in qs if (q.metadata or {}).get("diagram_svg"))
    assert with_svg >= 4
    assert any((q.metadata or {}).get("figure_family") == "function_sketch" for q in qs)


def _diagram_fingerprint(q) -> tuple:
    meta = q.metadata or {}
    spec = meta.get("diagram_spec") or {}
    svg = meta.get("diagram_svg") or ""
    params = meta.get("figure_params") or {}
    points = spec.get("points") or {}
    point_key = tuple(
        sorted((pid, round(p.get("x", 0), 2), round(p.get("y", 0), 2)) for pid, p in points.items())
    )
    return (
        spec.get("kind"),
        meta.get("figure_family"),
        tuple(sorted((k, params[k]) for k in params if isinstance(params[k], (int, float, str, bool)))),
        point_key,
        hash(svg) if svg else 0,
    )


def test_worksheet_batches_not_identical_figures():
    cases = [
        ("geo_classifying_angles", "geo_basics_classifying_angles"),
        ("geo_angle_relationships", "pa_angle_relationships"),
        ("geo_pythagorean_theorem", "geo_right_pythagorean_theorem"),
        ("geo_circle_measure", "pa_circles"),
        ("geo_triangle_area", "g6_triangles"),
    ]
    for gen_key, topic in cases:
        gen = GENERATORS[gen_key]
        qs = gen(topic, {"count": 10, "seed": 99, "difficulty": 12, "include_answer_key": True})
        assert len(qs) == 10
        fps = [_diagram_fingerprint(q) for q in qs]
        # Must have diagram content on most items.
        with_svg = sum(1 for q in qs if (q.metadata or {}).get("diagram_svg"))
        assert with_svg >= 8, (gen_key, with_svg)
        assert len(set(fps)) >= 3, (gen_key, fps)


def test_percent_shade_batch_varies_patterns_or_svg():
    gen = GENERATORS["g6_introduction_to_percents"]
    qs = gen(
        "g6_introduction_to_percents",
        {"count": 10, "seed": 5, "difficulty": 22, "include_answer_key": True},
    )
    svgs = [(q.metadata or {}).get("diagram_svg") for q in qs]
    assert all(s and "<svg" in s for s in svgs)
    assert len(set(svgs)) >= 3


def test_apply_batch_seed_reproducible():
    settings = {"seed": 17, "difficulty": 8}
    apply_batch_seed(settings, 0)
    a = random.random()
    apply_batch_seed(settings, 0)
    b = random.random()
    assert a == b
    apply_batch_seed(settings, 1)
    c = random.random()
    assert c != a


def test_sample_figure_from_settings_uses_difficulty():
    sample = sample_figure_from_settings(
        "percent_shade",
        {"difficulty": 25, "seed": 3, "_batch_index": 2},
    )
    assert sample.complexity == "complex"
    assert "shade_pattern" in sample.params


def test_figure_heavy_types_expose_continuous_difficulty():
    import question_engine.generators  # noqa: F401
    from question_engine.core.base import QUESTION_TYPES

    for tid in (
        "geo_basics_classifying_angles",
        "g6_numbers_on_a_number_line",
        "g6_points_on_the_coordinate_plane",
        "g6_introduction_to_percents",
        "g6_equations_tape_diagrams",
        "pa_circles",
        "geo_right_pythagorean_theorem",
    ):
        qt = QUESTION_TYPES[tid]
        keys = {f.key for f in qt.settings_schema()}
        assert "difficulty" in keys, tid
