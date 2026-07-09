"""A2 direct and inverse variation — framework-backed with variation settings profile."""

from question_engine.frameworks.linear import DirectVariationFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "a2_direct_and_inverse_variation_direct_and_inverse_variation",
    DirectVariationFramework(),
    profile="variation",
)
