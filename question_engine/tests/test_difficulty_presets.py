"""Tests for difficulty-tier setting presets."""

from __future__ import annotations

from question_engine.settings.presets import (
    apply_difficulty_presets,
    lookup_difficulty_preset,
)
from question_engine.settings.resolve import TypeSettingConfig, resolve_type_settings


def test_equation_hard_preset_widens_coefficients():
    easy = lookup_difficulty_preset("easy", setting_profile="equation")
    hard = lookup_difficulty_preset("hard", setting_profile="equation")
    assert easy["coef_max"] < hard["coef_max"]
    assert hard["integer_only"] is False


def test_apply_presets_fills_gaps_but_keeps_overrides():
    resolved = apply_difficulty_presets(
        {"difficulty_tier": "hard", "coef_max": 7},
        setting_profile="equation",
    )
    assert resolved["coef_max"] == 7
    assert resolved["coef_min"] == -20
    assert resolved["difficulty_tier"] == "hard"


def test_difficulty_group_appears_before_domain_groups():
    schema = resolve_type_settings(
        TypeSettingConfig(setting_profile="equation", inherits=("common_enrichment",))
    )
    groups = [field.group for field in schema if field.group]
    assert "difficulty" in groups
    assert "equation" in groups
    assert groups.index("difficulty") < groups.index("equation")
