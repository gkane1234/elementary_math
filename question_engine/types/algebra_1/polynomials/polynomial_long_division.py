import random
import uuid

from packages.polynomial_core import Polynomial

from question_engine.base import QuestionType, register
from question_engine.latex_helpers import long_division_answer_latex, polynomial_fraction_latex
from question_engine.models import Question
from question_engine.settings.generator_profiles import schema_for_generator


def _normalize_range(min_value: int, max_value: int) -> tuple[int, int]:
    if min_value > max_value:
        return max_value, min_value
    return min_value, max_value


def _create_long_division_problem(
    numerator_degree_min: int,
    numerator_degree_max: int,
    denominator_degree_min: int,
    denominator_degree_max: int,
    coef_min: int,
    coef_max: int,
    divide_cleanly: bool,
    positive_leading: bool,
) -> tuple[Polynomial, Polynomial, Polynomial, Polynomial]:
    num_min, num_max = _normalize_range(numerator_degree_min, numerator_degree_max)
    den_min, den_max = _normalize_range(denominator_degree_min, denominator_degree_max)

    for _ in range(200):
        denominator_degree = random.randint(max(1, den_min), max(1, den_max))
        if divide_cleanly:
            quotient_degree = random.randint(
                max(0, num_min - denominator_degree),
                max(0, num_max - denominator_degree),
            )
            remainder_degree = -1
        else:
            max_quotient_degree = max(0, num_max - denominator_degree)
            quotient_degree = random.randint(0, max_quotient_degree)
            remainder_degree = random.randint(0, denominator_degree - 1)

        divisor = Polynomial.random_polynomial(
            denominator_degree,
            coef_min,
            coef_max,
            positive_leading=positive_leading,
        )
        quotient = Polynomial.random_polynomial(
            quotient_degree,
            coef_min,
            coef_max,
            positive_leading=positive_leading,
        )
        dividend = quotient * divisor

        if not divide_cleanly:
            remainder = Polynomial.random_polynomial(
                remainder_degree,
                coef_min,
                coef_max,
                positive_leading=positive_leading,
            )
            dividend = dividend + remainder
        else:
            remainder = Polynomial(((0, 0),))

        if num_min <= dividend.deg() <= num_max:
            return dividend, divisor, quotient, remainder

    denominator_degree = max(1, den_min)
    quotient_degree = max(0, num_min - denominator_degree)
    divisor = Polynomial.random_polynomial(
        denominator_degree,
        coef_min,
        coef_max,
        positive_leading=positive_leading,
    )
    quotient = Polynomial.random_polynomial(
        quotient_degree,
        coef_min,
        coef_max,
        positive_leading=positive_leading,
    )
    dividend = quotient * divisor
    remainder = Polynomial(((0, 0),))
    if not divide_cleanly:
        remainder = Polynomial.random_polynomial(
            min(1, denominator_degree - 1),
            coef_min,
            coef_max,
            positive_leading=positive_leading,
        )
        dividend = dividend + remainder
    return dividend, divisor, quotient, remainder


@register
class PolynomialLongDivisionQuestionType(QuestionType):
    id = "polynomial_long_division"
    name = "Dividing"
    category = "Algebra 1 — Polynomials"
    description = "Divide polynomials with configurable degree ranges and remainders."
    instruction_latex = "\\text{Divide using polynomial long division.}"
    instruction_text = "Divide using polynomial long division."

    def settings_schema(self):
        return schema_for_generator(self.id)

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        numerator_degree_min = int(settings.get("numerator_degree_min", 2))
        numerator_degree_max = int(settings.get("numerator_degree_max", 4))
        denominator_degree_min = int(settings.get("denominator_degree_min", 1))
        denominator_degree_max = int(settings.get("denominator_degree_max", 2))
        coef_min = int(settings.get("coef_min", -6))
        coef_max = int(settings.get("coef_max", 6))
        divide_cleanly = bool(settings.get("divide_cleanly", True))
        positive_leading = bool(settings.get("positive_leading_coefficient", True))
        include_answer_key = bool(settings.get("include_answer_key", False))

        questions: list[Question] = []
        for _ in range(count):
            dividend, divisor, quotient, remainder = _create_long_division_problem(
                numerator_degree_min,
                numerator_degree_max,
                denominator_degree_min,
                denominator_degree_max,
                coef_min,
                coef_max,
                divide_cleanly,
                positive_leading,
            )

            answer_latex = None
            if include_answer_key:
                answer_latex = long_division_answer_latex(quotient, remainder, divisor)

            questions.append(
                Question(
                    id=str(uuid.uuid4()),
                    topic=self.id,
                    prompt_latex=polynomial_fraction_latex(dividend, divisor),
                    prompt_text=f"({dividend}) / ({divisor})",
                    answer_latex=answer_latex,
                    metadata={
                        "numerator_degree": dividend.deg(),
                        "denominator_degree": divisor.deg(),
                        "has_remainder": not remainder.is_zero(),
                    },
                )
            )

        return questions
