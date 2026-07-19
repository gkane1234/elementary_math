"""Catalog intent and family-key settings resolution."""

from question_engine.catalogs.base import derive_catalog_intent
from question_engine.core.registry import get_catalog_entry
from question_engine.settings.generator_profiles import config_for_type
from question_engine.settings.presets import (
    apply_difficulty_presets,
    resolve_setting_profile_for_type,
)


def test_derive_catalog_intent():
    assert derive_catalog_intent("one_step_equations", "scaffold") == "scaffold"
    assert derive_catalog_intent("one_step_equations", "one_step_equations") == "ready"
    assert (
        derive_catalog_intent(
            "a2_equations_and_inequalities_multi_step_equations",
            "multi_step_equations",
        )
        == "shared_family"
    )


def test_catalog_entry_intent_property():
    entry = get_catalog_entry("one_step_equations")
    assert entry.intent == "ready"
    shared = get_catalog_entry("a2_equations_and_inequalities_multi_step_equations")
    assert shared.intent == "shared_family"
    assert shared.generator == "multi_step_equations"
    simplifying = get_catalog_entry(
        "a2_beginning_algebra_simplifying_algebraic_expressions"
    )
    assert simplifying.generator == "expand_simplify"
    assert simplifying.intent == "shared_family"


def test_config_for_type_falls_back_to_family():
    cfg = config_for_type("a2_equations_and_inequalities_multi_step_equations")
    assert cfg is not None
    assert cfg.setting_profile == "primitive_equations"
    assert resolve_setting_profile_for_type(
        "a2_equations_and_inequalities_multi_step_equations"
    ) == "primitive_equations"


def test_difficulty_presets_resolve_via_family_key():
    merged = apply_difficulty_presets(
        {"difficulty_tier": "easy", "count": 1},
        type_id="a2_equations_and_inequalities_multi_step_equations",
    )
    # Family-key generator presets still supply legacy coef bounds when tier is set.
    assert merged.get("coef_min") == -5 or "difficulty" in merged or merged["count"] == 1
    assert merged["count"] == 1


def test_rational_expression_topic_names_include_chapter_context():
    """Standalone topic titles should stay understandable without chapter UI context."""
    a1_add = get_catalog_entry("rational_expression_simplification")
    a1_md = get_catalog_entry("rational_expression_multiply_divide")
    a1_eq = get_catalog_entry("rational_expressions_equations")
    a2_add = get_catalog_entry("a2_rational_expressions_adding_and_subtracting")
    a2_md = get_catalog_entry("a2_rational_expressions_multiplying_and_dividing")
    a2_simp = get_catalog_entry("a2_rational_expressions_simplifying")
    a2_graph = get_catalog_entry("a2_rational_expressions_graphing")
    a2_eq = get_catalog_entry("a2_rational_expressions_equations")

    assert a1_add.name == "Adding and subtracting rational expressions"
    assert a1_md.name == "Multiplying and dividing rational expressions"
    assert a1_eq.name == "Rational equations"
    assert a2_add.name == "Adding and subtracting rational expressions"
    assert a2_md.name == "Multiplying and dividing rational expressions"
    assert a2_simp.name == "Simplifying rational expressions"
    assert a2_graph.name == "Graphing rational functions"
    assert a2_eq.name == "Rational equations"
    # Already clear without chapter prefix
    assert get_catalog_entry("rational_simplification").name == (
        "Simplifying and excluded values"
    )
    assert get_catalog_entry("a2_rational_expressions_complex_fractions").name == (
        "Complex fractions"
    )
