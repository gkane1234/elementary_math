"""Shared generation primitives (Layer 0+), difficulty context, leaf→primitive map."""

from question_engine.frameworks.primitives.constructive import (
    AffineTarget,
    CancelPlan,
    ExpressionScope,
    NumericTarget,
    PartialFractionTarget,
    PolynomialTarget,
    RationalPolyTarget,
    SurfaceExpression,
    construct_affine,
    construct_numeric,
    construct_pfd,
    construct_poly,
    construct_rational_sum,
)
from question_engine.frameworks.primitives.distributive import (
    DISTRIBUTIVE_SETTINGS_SCHEMA,
    sample_distributive_algebraic,
    sample_distributive_numeric,
)
from question_engine.frameworks.primitives.equations import (
    EQUATIONS_SETTINGS_SCHEMA,
    sample_linear_equation,
)
from question_engine.frameworks.primitives.evaluate import (
    EVALUATE_SETTINGS_SCHEMA,
    sample_evaluate_expression,
    sample_evaluate_linear_expression,
)
from question_engine.frameworks.primitives.expand_simplify import (
    EXPAND_SIMPLIFY_SETTINGS_SCHEMA,
    sample_expand_simplify,
    sample_linear_expression_to_simplify,
)
from question_engine.frameworks.primitives.expression_structure import (
    sample_structured_expression,
)
from question_engine.frameworks.primitives.expression_exponents import (
    EXP_TYPES,
    exp_number_chance,
    exp_paren_chance,
    exponents_unlocked,
)
from question_engine.frameworks.primitives.factor_gcf import (
    FACTOR_GCF_SETTINGS_SCHEMA,
    sample_factor_gcf,
)
from question_engine.frameworks.primitives.inequalities import (
    INEQUALITIES_SETTINGS_SCHEMA,
    sample_linear_inequality,
)
from question_engine.frameworks.primitives.like_terms import (
    LIKE_TERMS_SETTINGS_SCHEMA,
    sample_like_terms,
)
from question_engine.frameworks.primitives.numbers import (
    NUMBER_PROFILES,
    NUMBER_SETTINGS_SCHEMA,
    PROFILE_CATALOG,
    SampledNumber,
    audit_lane_selection,
    audit_samples,
    eligible_lanes,
    sample_number,
    select_lane,
)
from question_engine.frameworks.primitives.ooo import OOO_SETTINGS_SCHEMA, sample_ooo_expression
from question_engine.frameworks.primitives.expression_policy import (
    LINEAR_ABS_POLICY,
    LINEAR_POLICY,
    POLYNOMIAL_POLICY_DEFAULT,
    SYSTEMS_POLICY,
    ExpressionPolicy,
    assert_linear_sample,
    polynomial_policy,
    resolve_policy,
)
from question_engine.frameworks.primitives.registry import (
    CORE_PRIMITIVES,
    LEAF_TO_PRIMITIVE,
    PRIM_DISTRIBUTIVE,
    PRIM_EQUATIONS,
    PRIM_EVALUATE,
    PRIM_EXPAND_SIMPLIFY,
    PRIM_FACTOR_GCF,
    PRIM_FACTOR_POLY,
    PRIM_INEQUALITIES,
    PRIM_LIKE_TERMS,
    PRIM_NUMBERS,
    PRIM_OOO,
    PRIM_POLYNOMIALS,
    PRIM_VARIABLE,
    SETTINGS_SCHEMAS,
    PrimitiveContext,
    build_context,
    get_primitive_spec,
    resolve_primitive,
)
from question_engine.frameworks.primitives.variables import (
    DEFAULT_VARIABLES,
    LANE_CATALOG as VARIABLE_LANE_CATALOG,
    LANE_MIN_D as VARIABLE_LANE_MIN_D,
    VARIABLE_LANES,
    VARIABLE_SETTINGS_SCHEMA,
    SampledVariable,
    audit_variable_lane_selection,
    eligible_variable_lanes,
    sample_variable,
    select_variable_lane,
)

# Complete schemas after leaf modules import (avoid circular imports in registry).
SETTINGS_SCHEMAS[PRIM_OOO] = OOO_SETTINGS_SCHEMA
SETTINGS_SCHEMAS[PRIM_DISTRIBUTIVE] = DISTRIBUTIVE_SETTINGS_SCHEMA
SETTINGS_SCHEMAS[PRIM_EVALUATE] = EVALUATE_SETTINGS_SCHEMA
SETTINGS_SCHEMAS[PRIM_LIKE_TERMS] = LIKE_TERMS_SETTINGS_SCHEMA
SETTINGS_SCHEMAS[PRIM_EXPAND_SIMPLIFY] = EXPAND_SIMPLIFY_SETTINGS_SCHEMA
SETTINGS_SCHEMAS[PRIM_EQUATIONS] = EQUATIONS_SETTINGS_SCHEMA
SETTINGS_SCHEMAS[PRIM_INEQUALITIES] = INEQUALITIES_SETTINGS_SCHEMA
SETTINGS_SCHEMAS[PRIM_FACTOR_GCF] = FACTOR_GCF_SETTINGS_SCHEMA
from question_engine.frameworks.primitives.polynomials import POLYNOMIALS_SETTINGS_SCHEMA
from question_engine.frameworks.primitives.factor_poly import FACTOR_POLY_SETTINGS_SCHEMA

SETTINGS_SCHEMAS[PRIM_POLYNOMIALS] = POLYNOMIALS_SETTINGS_SCHEMA
SETTINGS_SCHEMAS[PRIM_FACTOR_POLY] = FACTOR_POLY_SETTINGS_SCHEMA

__all__ = [
    "CORE_PRIMITIVES",
    "DEFAULT_VARIABLES",
    "EXPRESSION_POLICY",
    "LEAF_TO_PRIMITIVE",
    "LINEAR_ABS_POLICY",
    "LINEAR_POLICY",
    "NUMBER_PROFILES",
    "NUMBER_SETTINGS_SCHEMA",
    "POLYNOMIAL_POLICY_DEFAULT",
    "PROFILE_CATALOG",
    "PRIM_DISTRIBUTIVE",
    "PRIM_EQUATIONS",
    "PRIM_EVALUATE",
    "PRIM_EXPAND_SIMPLIFY",
    "PRIM_FACTOR_GCF",
    "PRIM_FACTOR_POLY",
    "PRIM_INEQUALITIES",
    "PRIM_LIKE_TERMS",
    "PRIM_NUMBERS",
    "PRIM_OOO",
    "PRIM_POLYNOMIALS",
    "PRIM_VARIABLE",
    "PrimitiveContext",
    "ExpressionPolicy",
    "SETTINGS_SCHEMAS",
    "SYSTEMS_POLICY",
    "SampledNumber",
    "SampledVariable",
    "ExpressionScope",
    "VARIABLE_LANE_CATALOG",
    "VARIABLE_LANE_MIN_D",
    "VARIABLE_LANES",
    "VARIABLE_SETTINGS_SCHEMA",
    "PolynomialTarget",
    "assert_linear_sample",
    "audit_lane_selection",
    "audit_samples",
    "audit_variable_lane_selection",
    "build_context",
    "construct_affine",
    "construct_numeric",
    "construct_poly",
    "eligible_lanes",
    "eligible_variable_lanes",
    "get_primitive_spec",
    "polynomial_policy",
    "resolve_policy",
    "resolve_primitive",
    "sample_distributive_algebraic",
    "sample_distributive_numeric",
    "sample_evaluate_expression",
    "sample_evaluate_linear_expression",
    "sample_expand_simplify",
    "sample_factor_gcf",
    "sample_like_terms",
    "sample_linear_equation",
    "sample_linear_expression_to_simplify",
    "sample_linear_inequality",
    "sample_number",
    "sample_ooo_expression",
    "sample_structured_expression",
    "EXP_TYPES",
    "exp_number_chance",
    "exp_paren_chance",
    "exponents_unlocked",
    "sample_variable",
    "select_lane",
    "select_variable_lane",
]

# Back-compat alias
EXPRESSION_POLICY = LINEAR_POLICY

