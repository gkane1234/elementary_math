from .basic import GENERATORS as _BASIC_GENERATORS
from .calculus import GENERATORS as _CALCULUS_GENERATORS
from .calculus_pilot import GENERATORS as _CALCULUS_PILOT_GENERATORS
from .calculus_derivative_rules import GENERATORS as _CALCULUS_DERIV_RULES_GENERATORS
from .equations import GENERATORS as _EQUATION_GENERATORS
from .geometry import GENERATORS as _GEOMETRY_GENERATORS
from .grade6 import GENERATORS as _GRADE6_GENERATORS
from .graphing import GENERATORS as _GRAPHING_GENERATORS
from .hand_written import GENERATORS as _HAND_WRITTEN_GENERATORS
from .linear import GENERATORS as _LINEAR_GENERATORS
from .misc import GENERATORS as _MISC_GENERATORS
from .numbers import GENERATORS as _NUMBER_GENERATORS
from .primitive_g6 import GENERATORS as _PRIMITIVE_G6_GENERATORS
from .primitive_linear import GENERATORS as _PRIMITIVE_LINEAR_GENERATORS
from .primitive_polynomial import GENERATORS as _PRIMITIVE_POLYNOMIAL_GENERATORS
from .primitive_rational import GENERATORS as _PRIMITIVE_RATIONAL_GENERATORS
from .algebra2 import GENERATORS as _ALGEBRA2_GENERATORS
from .precalc import GENERATORS as _PRECALC_GENERATORS
from .word_problems import GENERATORS as _WORD_PROBLEM_GENERATORS
from .statistics import GENERATORS as _STATISTICS_GENERATORS
from .advanced import GENERATORS as _ADVANCED_GENERATORS
from .grade_level import GENERATORS as _GRADE_LEVEL_GENERATORS

GENERATORS = {
    **_BASIC_GENERATORS,
    **_NUMBER_GENERATORS,
    **_GRADE6_GENERATORS,
    **_EQUATION_GENERATORS,
    **_LINEAR_GENERATORS,
    **_GRAPHING_GENERATORS,
    **_GEOMETRY_GENERATORS,
    **_MISC_GENERATORS,
    **_HAND_WRITTEN_GENERATORS,
    **_PRECALC_GENERATORS,
    **_ALGEBRA2_GENERATORS,
    **_CALCULUS_GENERATORS,
    **_CALCULUS_PILOT_GENERATORS,
    **_WORD_PROBLEM_GENERATORS,
    **_STATISTICS_GENERATORS,
    **_ADVANCED_GENERATORS,
    **_GRADE_LEVEL_GENERATORS,
    # Last so enriched derivative-rule builders override thin calc/advanced keys.
    **_CALCULUS_DERIV_RULES_GENERATORS,
    # Primitive-layered G6 / early algebra overrides (experiment/difficulty-slider).
    **_PRIMITIVE_G6_GENERATORS,
    # Linear finish: abs / compound / proportions / forms / systems / WP.
    **_PRIMITIVE_LINEAR_GENERATORS,
    # Polynomial expression stack (policy max_degree≥2).
    **_PRIMITIVE_POLYNOMIAL_GENERATORS,
    # Constructive rationals + PFD (L2–L4).
    **_PRIMITIVE_RATIONAL_GENERATORS,
}

__all__ = ["GENERATORS"]
