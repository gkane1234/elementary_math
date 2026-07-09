"""Settings package."""

from .domains import equation_coef_settings, polynomial_coef_settings, polynomial_factoring_settings, radical_settings
from .standard import merge_settings, standard_question_settings

__all__ = [
    "equation_coef_settings",
    "merge_settings",
    "polynomial_coef_settings",
    "polynomial_factoring_settings",
    "radical_settings",
    "standard_question_settings",
]
