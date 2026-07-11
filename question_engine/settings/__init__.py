"""Settings package."""

from .domains import equation_coef_settings, polynomial_coef_settings, polynomial_factoring_settings, radical_settings
from .profiles import PROFILE_BUILDERS, polynomial_settings, equation_settings
from .resolve import TypeSettingConfig, resolve_type_settings
from .standard import merge_settings, standard_question_settings
from .presets import (
    PROFILE_DIFFICULTY_PRESETS,
    apply_difficulty_presets,
    lookup_difficulty_preset,
)

__all__ = [
    "PROFILE_BUILDERS",
    "PROFILE_DIFFICULTY_PRESETS",
    "TypeSettingConfig",
    "apply_difficulty_presets",
    "equation_coef_settings",
    "equation_settings",
    "lookup_difficulty_preset",
    "merge_settings",
    "polynomial_coef_settings",
    "polynomial_factoring_settings",
    "polynomial_settings",
    "radical_settings",
    "resolve_type_settings",
    "standard_question_settings",
]
