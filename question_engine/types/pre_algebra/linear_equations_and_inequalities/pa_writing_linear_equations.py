"""PA writing linear equations — form conversions, simplify, or read from a graph."""

from question_engine.frameworks.linear import WritingLinearEquationsFramework
from question_engine.types._graphing_type import register_graphing_type

register_graphing_type(
    "pa_writing_linear_equations",
    WritingLinearEquationsFramework(),
    setting_defaults={
        "include_graph_metadata": True,
        "show_points": False,
        "ask_mode": "mixed",
    },
)
