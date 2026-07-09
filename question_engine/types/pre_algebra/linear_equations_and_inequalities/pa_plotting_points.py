"""PA plotting points — coordinate-plane settings profile."""

from question_engine.frameworks.linear import PlottingPointsFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "pa_plotting_points",
    PlottingPointsFramework(),
    profile="coordinate_plane",
)
