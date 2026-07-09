"""Direct and inverse variation — framework-backed with variation settings profile."""

from question_engine.frameworks.linear import DirectVariationFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "direct_inverse_variation",
    DirectVariationFramework(),
    profile="variation",
)
