"""Domain-specific setting field builders."""

from .equation import equation_coef_settings
from .common import (
    answer_format_settings,
    continuous_difficulty_settings,
    difficulty_settings,
    multiple_choice_settings,
    sign_restrictions,
    term_count_settings,
)
from .geometry import geometry_settings
from .inequality import inequality_settings
from .misc import misc_expression_settings
from .polynomial import polynomial_coef_settings, polynomial_factoring_settings
from .radical import (
    radical_add_subtract_form_settings,
    radical_divide_form_settings,
    radical_equation_form_settings,
    radical_settings,
)
from .rational import (
    fraction_form_settings,
    rational_equation_form_settings,
    rational_expression_extra_settings,
    rational_multiply_divide_settings,
    rational_operation_settings,
)
from .word_problem import (
    consecutive_integers_settings,
    distance_rate_time_settings,
    mixture_problem_settings,
    percent_word_problem_settings,
    similar_figures_prompt_settings,
    word_problem_settings,
    work_problem_settings,
)

from .calculus import derivative_settings, integral_settings, limit_settings
from .logarithm import exponential_equation_settings, logarithm_settings
from .sequence import sequence_settings
from .trigonometry import trigonometry_settings

__all__ = [
    "equation_coef_settings",
    "misc_expression_settings",
    "polynomial_coef_settings",
    "polynomial_factoring_settings",
    "radical_settings",
    "radical_add_subtract_form_settings",
    "radical_equation_form_settings",
    "radical_divide_form_settings",
    "rational_expression_extra_settings",
    "rational_equation_form_settings",
    "rational_multiply_divide_settings",
    "rational_operation_settings",
    "fraction_form_settings",
    "inequality_settings",
    "consecutive_integers_settings",
    "distance_rate_time_settings",
    "mixture_problem_settings",
    "percent_word_problem_settings",
    "similar_figures_prompt_settings",
    "word_problem_settings",
    "work_problem_settings",
    "geometry_settings",
    "trigonometry_settings",
    "logarithm_settings",
    "exponential_equation_settings",
    "sequence_settings",
    "limit_settings",
    "derivative_settings",
    "integral_settings",
]
