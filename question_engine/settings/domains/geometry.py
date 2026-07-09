"""Settings fields for geometry measurement question types."""

from __future__ import annotations

from ...core.models import SettingField


def geometry_metadata_settings() -> list[SettingField]:
    return [
        SettingField(
            "include_diagram",
            "Include diagram metadata",
            "bool",
            False,
            group="geometry",
        ),
    ]


def measurement_unit_settings(
    *,
    default: str = "cm",
) -> list[SettingField]:
    return [
        SettingField(
            "measurement_unit",
            "Length unit",
            "select",
            default,
            options=["cm", "in", "m", "ft"],
            group="geometry",
        ),
    ]


def side_length_settings(
    *,
    side_min_default: int = 3,
    side_max_default: int = 20,
) -> list[SettingField]:
    return [
        SettingField(
            "side_min",
            "Side length min",
            "int",
            side_min_default,
            min=1,
            max=100,
            group="geometry",
        ),
        SettingField(
            "side_max",
            "Side length max",
            "int",
            side_max_default,
            min=1,
            max=100,
            group="geometry",
        ),
    ]


def angle_bounds_settings(
    *,
    angle_min_default: int = 10,
    angle_max_default: int = 170,
) -> list[SettingField]:
    return [
        SettingField(
            "angle_min",
            "Angle measure min",
            "int",
            angle_min_default,
            min=1,
            max=359,
            group="geometry",
        ),
        SettingField(
            "angle_max",
            "Angle measure max",
            "int",
            angle_max_default,
            min=1,
            max=359,
            group="geometry",
        ),
    ]


def angle_unit_settings(
    *,
    default: str = "degrees",
) -> list[SettingField]:
    return [
        SettingField(
            "angle_unit",
            "Angle unit",
            "select",
            default,
            options=["degrees", "radians"],
            group="geometry",
        ),
    ]


def triangle_type_settings() -> list[SettingField]:
    return [
        SettingField(
            "allow_acute",
            "Allow acute triangles",
            "bool",
            True,
            group="geometry",
        ),
        SettingField(
            "allow_right",
            "Allow right triangles",
            "bool",
            True,
            group="geometry",
        ),
        SettingField(
            "allow_obtuse",
            "Allow obtuse triangles",
            "bool",
            True,
            group="geometry",
        ),
        SettingField(
            "allow_equilateral",
            "Allow equilateral triangles",
            "bool",
            True,
            group="geometry",
        ),
        SettingField(
            "allow_isosceles",
            "Allow isosceles triangles",
            "bool",
            True,
            group="geometry",
        ),
        SettingField(
            "allow_scalene",
            "Allow scalene triangles",
            "bool",
            True,
            group="geometry",
        ),
    ]


def polygon_sides_settings(
    *,
    sides_min_default: int = 3,
    sides_max_default: int = 8,
) -> list[SettingField]:
    return [
        SettingField(
            "polygon_sides_min",
            "Polygon sides min",
            "int",
            sides_min_default,
            min=3,
            max=12,
            group="geometry",
        ),
        SettingField(
            "polygon_sides_max",
            "Polygon sides max",
            "int",
            sides_max_default,
            min=3,
            max=12,
            group="geometry",
        ),
    ]


def circle_radius_settings(
    *,
    radius_min_default: int = 2,
    radius_max_default: int = 15,
) -> list[SettingField]:
    return [
        SettingField(
            "radius_min",
            "Radius min",
            "int",
            radius_min_default,
            min=1,
            max=50,
            group="geometry",
        ),
        SettingField(
            "radius_max",
            "Radius max",
            "int",
            radius_max_default,
            min=1,
            max=50,
            group="geometry",
        ),
    ]


def similarity_ratio_settings(
    *,
    ratio_min_default: int = 2,
    ratio_max_default: int = 5,
) -> list[SettingField]:
    return [
        SettingField(
            "similarity_ratio_min",
            "Similarity ratio min",
            "int",
            ratio_min_default,
            min=2,
            max=10,
            group="geometry",
        ),
        SettingField(
            "similarity_ratio_max",
            "Similarity ratio max",
            "int",
            ratio_max_default,
            min=2,
            max=10,
            group="geometry",
        ),
    ]


def proof_difficulty_settings() -> list[SettingField]:
    return [
        SettingField(
            "proof_difficulty",
            "Proof difficulty",
            "select",
            "basic",
            options=["basic", "intermediate", "advanced"],
            group="geometry",
        ),
    ]


def geometry_settings() -> list[SettingField]:
    """Backward-compatible base geometry settings."""
    return [
        *geometry_metadata_settings(),
        *measurement_unit_settings(),
        *side_length_settings(),
    ]
