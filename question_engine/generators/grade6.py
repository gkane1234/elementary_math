"""Grade 6 number-sense generators: fractions, integers, factors, absolute value."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.number import (
    AbsoluteValueFramework,
    CompareOrderFramework,
    DecimalArithmeticFramework,
    DivisibilityFramework,
    FractionDecimalConvertFramework,
    FractionDivideWordFramework,
    GcfLcmFramework,
    GcfLcmWordFramework,
    IntegerArithmeticFramework,
    LikeDenominatorFractionFramework,
    OppositeFramework,
    PrimeFactorizationFramework,
    RationalFramework,
    UnlikeDenominatorFractionFramework,
)

_FRAC_ADD_LIKE = LikeDenominatorFractionFramework("+")
_FRAC_SUB_LIKE = LikeDenominatorFractionFramework("-")
_FRAC_ADD_UNLIKE = UnlikeDenominatorFractionFramework("+")
_FRAC_SUB_UNLIKE = UnlikeDenominatorFractionFramework("-")
_FRAC_MULTIPLY = RationalFramework("*")
_FRAC_DIVIDE = RationalFramework("/")
_FRAC_DIVIDE_GROUPS = FractionDivideWordFramework(mode="groups")
_FRAC_DIVIDE_EACH = FractionDivideWordFramework(mode="each")
_FRAC_OF_WHOLE = FractionDivideWordFramework(mode="whole")

_INT_ADD_SUB = IntegerArithmeticFramework("+-")
_INT_MULTIPLY = IntegerArithmeticFramework("*")
_INT_DIVIDE = IntegerArithmeticFramework("/")
_INT_NEGATIVE = IntegerArithmeticFramework("+-")

_GCF = GcfLcmFramework(mode="gcf")
_LCM = GcfLcmFramework(mode="lcm")
_GCF_LCM_WORD = GcfLcmWordFramework()
_PRIME_FACTOR = PrimeFactorizationFramework()

_ABS_EVAL = AbsoluteValueFramework(mode="evaluate")
_ABS_COMPARE = AbsoluteValueFramework(mode="compare")
_ABS_ORDER = AbsoluteValueFramework(mode="order")

_OPPOSITE = OppositeFramework()
_COMPARE = CompareOrderFramework(mode="compare")
_ORDER = CompareOrderFramework(mode="order")
_FRAC_DECIMAL = FractionDecimalConvertFramework()
_DIVISIBILITY = DivisibilityFramework()


def _framework_generator(framework, topic: str, settings: dict) -> list[Question]:
    return framework.generate_batch(topic, settings)


def g6_fraction_add_like(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_ADD_LIKE, topic, settings)


def g6_fraction_subtract_like(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_SUB_LIKE, topic, settings)


def g6_fraction_add_unlike(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_ADD_UNLIKE, topic, settings)


def g6_fraction_subtract_unlike(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_SUB_UNLIKE, topic, settings)


def g6_fraction_multiply(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_MULTIPLY, topic, settings)


def g6_fraction_divide(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_DIVIDE, topic, settings)


def g6_fraction_divide_groups(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_DIVIDE_GROUPS, topic, settings)


def g6_fraction_divide_each(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_DIVIDE_EACH, topic, settings)


def g6_fraction_of_whole(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_OF_WHOLE, topic, settings)


def g6_integer_add_subtract(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_INT_ADD_SUB, topic, settings)


def g6_integer_multiply(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_INT_MULTIPLY, topic, settings)


def g6_integer_divide(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_INT_DIVIDE, topic, settings)


def g6_negative_number_operations(topic: str, settings: dict) -> list[Question]:
    settings = {**settings, "allow_negative": True}
    op = settings.get("integer_op", "+-")
    framework = IntegerArithmeticFramework(op if op in ("*", "/") else "+-")
    return _framework_generator(framework, topic, settings)


def g6_greatest_common_factor(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_GCF, topic, settings)


def g6_least_common_multiple(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_LCM, topic, settings)


def g6_gcf_and_lcm_word_problems(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_GCF_LCM_WORD, topic, settings)


def g6_factoring(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_PRIME_FACTOR, topic, settings)


def g6_absolute_values(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_ABS_EVAL, topic, settings)


def g6_comparing_with_absolute_values(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_ABS_COMPARE, topic, settings)


def g6_ordering_with_absolute_values(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_ABS_ORDER, topic, settings)


def g6_opposites_of_numbers(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_OPPOSITE, topic, settings)


def g6_comparing_numbers(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_COMPARE, topic, settings)


def g6_ordering_numbers(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_ORDER, topic, settings)


def g6_relating_percents_fractions_and_decimals(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_DECIMAL, topic, settings)


def g6_divisibility(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DIVISIBILITY, topic, settings)


def g6_numeric_expressions_with_exponents(topic: str, settings: dict) -> list[Question]:
    from .numbers import order_of_operations

    settings = {**settings, "pemdas_complexity": "exponent"}
    return order_of_operations(topic, settings)


def g6_long_division_with_remainders(topic: str, settings: dict) -> list[Question]:
    return g6_integer_divide(topic, settings)


_DECIMAL_DIVIDE_WHOLE = DecimalArithmeticFramework("/")


def g6_dividing_decimals_by_whole_numbers(topic: str, settings: dict) -> list[Question]:
    settings = {**settings, "allow_negative": False}
    return _framework_generator(_DECIMAL_DIVIDE_WHOLE, topic, settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "g6_fraction_add_like": g6_fraction_add_like,
    "g6_fraction_subtract_like": g6_fraction_subtract_like,
    "g6_fraction_add_unlike": g6_fraction_add_unlike,
    "g6_fraction_subtract_unlike": g6_fraction_subtract_unlike,
    "g6_fraction_multiply": g6_fraction_multiply,
    "g6_fraction_divide": g6_fraction_divide,
    "g6_fraction_divide_groups": g6_fraction_divide_groups,
    "g6_fraction_divide_each": g6_fraction_divide_each,
    "g6_fraction_of_whole": g6_fraction_of_whole,
    "g6_integer_add_subtract": g6_integer_add_subtract,
    "g6_integer_multiply": g6_integer_multiply,
    "g6_integer_divide": g6_integer_divide,
    "g6_negative_number_operations": g6_negative_number_operations,
    "g6_greatest_common_factor": g6_greatest_common_factor,
    "g6_least_common_multiple": g6_least_common_multiple,
    "g6_gcf_and_lcm_word_problems": g6_gcf_and_lcm_word_problems,
    "g6_factoring": g6_factoring,
    "g6_absolute_values": g6_absolute_values,
    "g6_comparing_with_absolute_values": g6_comparing_with_absolute_values,
    "g6_ordering_with_absolute_values": g6_ordering_with_absolute_values,
    "g6_opposites_of_numbers": g6_opposites_of_numbers,
    "g6_comparing_numbers": g6_comparing_numbers,
    "g6_ordering_numbers": g6_ordering_numbers,
    "g6_relating_percents_fractions_and_decimals": g6_relating_percents_fractions_and_decimals,
    "g6_divisibility": g6_divisibility,
    "g6_numeric_expressions_with_exponents": g6_numeric_expressions_with_exponents,
    "g6_long_division_with_remainders": g6_long_division_with_remainders,
    "g6_dividing_decimals_by_whole_numbers": g6_dividing_decimals_by_whole_numbers,
}
