"""Domain-specific setting field builders."""

from .equation import equation_coef_settings
from .geometry import geometry_settings
from .inequality import inequality_settings
from .polynomial import polynomial_coef_settings, polynomial_factoring_settings
from .radical import radical_settings
from .word_problem import word_problem_settings

__all__ = [
    "equation_coef_settings",
    "polynomial_coef_settings",
    "polynomial_factoring_settings",
    "radical_settings",
    "inequality_settings",
    "word_problem_settings",
    "geometry_settings",
]
