"""Register linear-framework catalog types with inherited setting profiles."""

from __future__ import annotations

from typing import Any

from ..frameworks.base import QuestionFramework
from ._framework_type import register_framework_type


def register_linear_type(
    type_id: str,
    framework: QuestionFramework,
    *,
    profile: str = "linear",
    inherits: tuple[str, ...] = (),
    exclude_settings: tuple[str, ...] = (),
    setting_defaults: dict[str, Any] | None = None,
) -> type:
    """Wire a catalog linear type to ``register_framework_type`` + profile inheritance."""
    return register_framework_type(
        type_id,
        framework,
        setting_profile=profile,
        inherits=inherits,
        exclude_settings=exclude_settings,
        setting_defaults=setting_defaults,
    )
