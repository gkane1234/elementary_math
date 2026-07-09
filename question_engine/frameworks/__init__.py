"""Reusable generator frameworks for question types."""

from .base import QuestionFramework
from .equation import (
    EquationFramework,
    EquationParams,
    LinearEquationFramework,
    OneStepEquationsFramework,
)
from .geometry import GeometryFigureSpec, GeometryFramework
from .graphing import CoordinatePlaneSpec, GraphingFramework
from .inequality import InequalityFramework, NumberLineSpec
from .number import NumberFramework, NumberParams, PercentFramework, RationalFramework
from .statistics import ChartSpec, DataSetSpec, StatisticsFramework
from .trigonometry import RightTriangleSpec, TrigFramework
from .word_problem import WordProblemFramework, WordProblemTemplate

__all__ = [
    "QuestionFramework",
    "EquationFramework",
    "EquationParams",
    "LinearEquationFramework",
    "OneStepEquationsFramework",
    "NumberFramework",
    "NumberParams",
    "PercentFramework",
    "RationalFramework",
    "InequalityFramework",
    "NumberLineSpec",
    "WordProblemFramework",
    "WordProblemTemplate",
    "GeometryFigureSpec",
    "GeometryFramework",
    "CoordinatePlaneSpec",
    "GraphingFramework",
    "ChartSpec",
    "DataSetSpec",
    "StatisticsFramework",
    "RightTriangleSpec",
    "TrigFramework",
]
