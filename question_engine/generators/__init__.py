from .basic import GENERATORS as _BASIC_GENERATORS
from .calculus import GENERATORS as _CALCULUS_GENERATORS
from .calculus_pilot import GENERATORS as _CALCULUS_PILOT_GENERATORS
from .calculus_derivative_rules import GENERATORS as _CALCULUS_DERIV_RULES_GENERATORS
from .calculus_limits import GENERATORS as _CALCULUS_LIMITS_GENERATORS
from .calculus_integrals import GENERATORS as _CALCULUS_INTEGRALS_GENERATORS
from .calculus_app_diff import GENERATORS as _CALCULUS_APP_DIFF_GENERATORS
from .equations import GENERATORS as _EQUATION_GENERATORS
from .geometry import GENERATORS as _GEOMETRY_GENERATORS
from .grade6 import GENERATORS as _GRADE6_GENERATORS
from .graphing import GENERATORS as _GRAPHING_GENERATORS
from .hand_written import GENERATORS as _HAND_WRITTEN_GENERATORS
from .linear import GENERATORS as _LINEAR_GENERATORS
from .misc import GENERATORS as _MISC_GENERATORS
from .numbers import GENERATORS as _NUMBER_GENERATORS
from .primitive_g6 import GENERATORS as _PRIMITIVE_G6_GENERATORS
from .primitive_geometry import GENERATORS as _PRIMITIVE_GEOMETRY_GENERATORS
from .primitive_linear import GENERATORS as _PRIMITIVE_LINEAR_GENERATORS
from .primitive_polynomial import GENERATORS as _PRIMITIVE_POLYNOMIAL_GENERATORS
from .primitive_rational import GENERATORS as _PRIMITIVE_RATIONAL_GENERATORS
from .primitive_pa import GENERATORS as _PRIMITIVE_PA_GENERATORS
from .primitive_a1 import GENERATORS as _PRIMITIVE_A1_GENERATORS
from .primitive_a2 import GENERATORS as _PRIMITIVE_A2_GENERATORS
from .primitive_precalc import GENERATORS as _PRIMITIVE_PRECALC_GENERATORS
from .pc_deferred import GENERATORS as _PC_DEFERRED_GENERATORS
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
    **_PC_DEFERRED_GENERATORS,
    **_ALGEBRA2_GENERATORS,
    **_CALCULUS_GENERATORS,
    **_CALCULUS_PILOT_GENERATORS,
    **_WORD_PROBLEM_GENERATORS,
    **_STATISTICS_GENERATORS,
    **_ADVANCED_GENERATORS,
    **_GRADE_LEVEL_GENERATORS,
    # Last so enriched derivative-rule builders override thin calc/advanced keys.
    **_CALCULUS_DERIV_RULES_GENERATORS,
    # Spec limits / integrals (override thin calc/advanced/pilot keys).
    **_CALCULUS_LIMITS_GENERATORS,
    **_CALCULUS_INTEGRALS_GENERATORS,
    **_CALCULUS_APP_DIFF_GENERATORS,
    # Primitive-layered G6 / early algebra overrides (experiment/difficulty-slider).
    **_PRIMITIVE_G6_GENERATORS,
    # G6 geometry / measurement (overrides shared geo keys for G6 leaves only).
    **_PRIMITIVE_GEOMETRY_GENERATORS,
    # Linear finish: abs / compound / proportions / forms / systems / WP.
    **_PRIMITIVE_LINEAR_GENERATORS,
    # Polynomial expression stack (policy max_degree≥2).
    **_PRIMITIVE_POLYNOMIAL_GENERATORS,
    # Constructive rationals + PFD (L2–L4).
    **_PRIMITIVE_RATIONAL_GENERATORS,
    # PA catalog wrappers (stamp pattern; reuse G6/number/geo engines).
    **_PRIMITIVE_PA_GENERATORS,
    # A1 leftover poly / quadratic / radical / numeric-rational stamps.
    **_PRIMITIVE_A1_GENERATORS,
    # PC trig skeletons (§7.1–7.5 identity / factoring-equation species).
    **_PRIMITIVE_PRECALC_GENERATORS,
    # A2 poly-only / exp-log / sequences / trig (non-graph) stamps.
    **_PRIMITIVE_A2_GENERATORS,
}

__all__ = ["GENERATORS"]
