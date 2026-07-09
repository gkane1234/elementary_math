"""Geo parallel points — coordinate-plane settings profile."""

from question_engine.frameworks.linear import PlottingPointsFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "geo_parallel_points_of_the_coordinate_plane",
    PlottingPointsFramework(),
    profile="coordinate_plane",
)
