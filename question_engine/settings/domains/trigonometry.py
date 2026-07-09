"""Settings fields for trigonometry question types."""

from __future__ import annotations

from ...core.models import SettingField


def trigonometry_settings(
    *,
    angle_unit_default: str = "degrees",
    angle_min_default: int = 0,
    angle_max_default: int = 360,
) -> list[SettingField]:
    return [
        SettingField(
            "angle_unit",
            "Angle unit",
            "select",
            angle_unit_default,
            options=["degrees", "radians", "both"],
            group="trigonometry",
        ),
        SettingField(
            "angle_min",
            "Angle min",
            "int",
            angle_min_default,
            min=0,
            max=720,
            group="trigonometry",
        ),
        SettingField(
            "angle_max",
            "Angle max",
            "int",
            angle_max_default,
            min=0,
            max=720,
            group="trigonometry",
        ),
        SettingField(
            "unit_circle_only",
            "Unit circle angles only",
            "bool",
            True,
            group="trigonometry",
        ),
        SettingField(
            "allow_sin",
            "Include sine",
            "bool",
            True,
            group="trigonometry",
        ),
        SettingField(
            "allow_cos",
            "Include cosine",
            "bool",
            True,
            group="trigonometry",
        ),
        SettingField(
            "allow_tan",
            "Include tangent",
            "bool",
            True,
            group="trigonometry",
        ),
        SettingField(
            "allow_cot",
            "Include cotangent",
            "bool",
            False,
            group="trigonometry",
        ),
        SettingField(
            "allow_reciprocal_identities",
            "Include reciprocal identities",
            "bool",
            True,
            group="trigonometry",
        ),
        SettingField(
            "allow_pythagorean_identities",
            "Include Pythagorean identities",
            "bool",
            True,
            group="trigonometry",
        ),
    ]
