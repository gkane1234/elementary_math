"""Number, ratio, rate, percent, and fraction question generators."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.number import (
    DecimalArithmeticFramework,
    DistributiveFramework,
    OrderOfOperationsFramework,
    PercentFramework,
    ProportionFramework,
    RationalFramework,
    RatioFramework,
    ScientificNotationFramework,
    UnitRateFramework,
)

_RATIONAL_ADD_SUBTRACT = RationalFramework("+-")
_RATIONAL_MULTIPLY = RationalFramework("*")
_RATIONAL_DIVIDE = RationalFramework("/")
_DISTRIBUTIVE = DistributiveFramework()
_DISTRIBUTIVE_ALGEBRAIC = DistributiveFramework(algebraic=True)
_PERCENTS = PercentFramework()
_PERCENT_OF_CHANGE = PercentFramework(percent_change=True)
_PROPORTIONS = ProportionFramework()
_RATIO_INTRO = RatioFramework()
_RATIO_EQUIVALENT = RatioFramework(equivalent=True)
_UNIT_RATE = UnitRateFramework()
_DECIMAL_ADD = DecimalArithmeticFramework("+")
_DECIMAL_SUBTRACT = DecimalArithmeticFramework("-")
_DECIMAL_MULTIPLY = DecimalArithmeticFramework("*")
_ORDER_OF_OPERATIONS = OrderOfOperationsFramework()
_SCI_NOTATION_WRITE = ScientificNotationFramework(mode="write")
_SCI_NOTATION_OPS = ScientificNotationFramework(mode="operations")
_SCI_NOTATION_ADD_SUB = ScientificNotationFramework(mode="add_subtract")


def _framework_generator(framework, topic: str, settings: dict) -> list[Question]:
    return framework.generate_batch(topic, settings)


def rational_add_subtract(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIONAL_ADD_SUBTRACT, topic, settings)


def rational_multiply(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIONAL_MULTIPLY, topic, settings)


def rational_divide(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIONAL_DIVIDE, topic, settings)


def distributive_property(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DISTRIBUTIVE, topic, settings)


def percents(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_PERCENTS, topic, settings)


def percent_of_change(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_PERCENT_OF_CHANGE, topic, settings)


def solving_proportions(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_PROPORTIONS, topic, settings)


def scientific_notation_write(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_SCI_NOTATION_WRITE, topic, settings)


def scientific_notation_operations(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_SCI_NOTATION_OPS, topic, settings)


def scientific_notation_add_subtract(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_SCI_NOTATION_ADD_SUB, topic, settings)


def g6_introduction_to_ratios(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIO_INTRO, topic, settings)


def g6_equivalent_ratios(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIO_EQUIVALENT, topic, settings)


def g6_unit_rates(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_UNIT_RATE, topic, settings)


def g6_decimal_addition(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DECIMAL_ADD, topic, settings)


def g6_decimal_subtraction(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DECIMAL_SUBTRACT, topic, settings)


def g6_decimal_multiplication(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DECIMAL_MULTIPLY, topic, settings)


def order_of_operations(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_ORDER_OF_OPERATIONS, topic, settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "rational_add_subtract": rational_add_subtract,
    "rational_multiply": rational_multiply,
    "rational_divide": rational_divide,
    "distributive_property": distributive_property,
    "percents": percents,
    "percent_of_change": percent_of_change,
    "solving_proportions": solving_proportions,
    "scientific_notation_write": scientific_notation_write,
    "scientific_notation_operations": scientific_notation_operations,
    "scientific_notation_add_subtract": scientific_notation_add_subtract,
    "g6_introduction_to_ratios": g6_introduction_to_ratios,
    "g6_equivalent_ratios": g6_equivalent_ratios,
    "g6_unit_rates": g6_unit_rates,
    "g6_decimal_addition": g6_decimal_addition,
    "g6_decimal_subtraction": g6_decimal_subtraction,
    "g6_decimal_multiplication": g6_decimal_multiplication,
    "order_of_operations": order_of_operations,
}
