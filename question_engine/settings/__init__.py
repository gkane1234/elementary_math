"""Settings package."""

from .domains import equation_coef_settings, polynomial_coef_settings, polynomial_factoring_settings, radical_settings
from .profiles import PROFILE_BUILDERS, polynomial_settings, equation_settings
from .resolve import TypeSettingConfig, resolve_type_settings
from .standard import merge_settings, standard_question_settings

__all__ = [
    "PROFILE_BUILDERS",
    "TypeSettingConfig",
    "equation_coef_settings",
    "equation_settings",
    "merge_settings",
    "polynomial_coef_settings",
    "polynomial_factoring_settings",
    "polynomial_settings",
    "radical_settings",
    "resolve_type_settings",
    "standard_question_settings",
]
