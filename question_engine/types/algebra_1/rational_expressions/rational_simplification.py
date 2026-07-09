import random
import uuid

from packages.polynomial_core import (
    FactorablePolynomialOptions,
    create_factorable_polynomial_with_exact_degree,
)

from question_engine.base import QuestionType, register
from question_engine.factoring_settings import build_factorable_options, shared_factoring_settings
from question_engine.latex_helpers import polynomial_fraction_latex
from question_engine.models import Question, SettingField


def _normalize_range(min_value: int, max_value: int) -> tuple[int, int]:
    if min_value > max_value:
        return max_value, min_value
    return min_value, max_value


def _create_factorable_polynomial_exact(
    base_options: FactorablePolynomialOptions,
    exact_degree: int,
):
    result = create_factorable_polynomial_with_exact_degree(base_options, exact_degree)
    return result.polynomial, result.factors, result.method


def _create_rational_simplification_problem(
    settings: dict,
    numerator_degree_min: int,
    numerator_degree_max: int,
    denominator_degree_min: int,
    denominator_degree_max: int,
) -> tuple:
    num_min, num_max = _normalize_range(numerator_degree_min, numerator_degree_max)
    den_min, den_max = _normalize_range(denominator_degree_min, denominator_degree_max)
    base_options = build_factorable_options(settings, num_min, num_max)

    for _ in range(200):
        target_num_degree = random.randint(num_min, num_max)
        target_den_degree = random.randint(den_min, den_max)
        max_common = min(target_num_degree, target_den_degree)

        if max_common < 1:
            continue

        common_degree = random.randint(1, max_common)
        reduced_num_degree = target_num_degree - common_degree
        reduced_den_degree = target_den_degree - common_degree

        if reduced_den_degree < 1:
            continue

        common_factor, _, _ = _create_factorable_polynomial_exact(base_options, common_degree)
        reduced_numerator, _, _ = _create_factorable_polynomial_exact(base_options, reduced_num_degree)
        reduced_denominator, _, _ = _create_factorable_polynomial_exact(base_options, reduced_den_degree)

        numerator = common_factor * reduced_numerator
        denominator = common_factor * reduced_denominator

        if (
            numerator.deg() == target_num_degree
            and denominator.deg() == target_den_degree
            and not reduced_denominator.is_zero()
        ):
            return numerator, denominator, reduced_numerator, reduced_denominator

    target_num_degree = num_min
    target_den_degree = den_min
    common_degree = 1
    reduced_num_degree = max(0, target_num_degree - common_degree)
    reduced_den_degree = max(1, target_den_degree - common_degree)

    common_factor, _, _ = _create_factorable_polynomial_exact(base_options, common_degree)
    reduced_numerator, _, _ = _create_factorable_polynomial_exact(base_options, reduced_num_degree)
    reduced_denominator, _, _ = _create_factorable_polynomial_exact(base_options, reduced_den_degree)

    return (
        common_factor * reduced_numerator,
        common_factor * reduced_denominator,
        reduced_numerator,
        reduced_denominator,
    )


@register
class RationalSimplificationQuestionType(QuestionType):
    id = "rational_simplification"
    name = "Simplifying and excluded values"
    category = "Algebra 1 — Rational Expressions"
    description = "Simplify rational expressions by canceling common polynomial factors."
    instruction_latex = "\\text{Simplify.}"
    instruction_text = "Simplify."

    def settings_schema(self) -> list[SettingField]:
        return [
            SettingField("count", "Number of questions", "int", 10, min=1, max=50),
            SettingField(
                "max_columns",
                "Columns (auto-fit up to 3)",
                "select",
                "auto",
                options=["auto", "1", "2", "3"],
            ),
            SettingField("numerator_degree_min", "Numerator degree min", "int", 2, min=1, max=8),
            SettingField("numerator_degree_max", "Numerator degree max", "int", 4, min=1, max=8),
            SettingField("denominator_degree_min", "Denominator degree min", "int", 2, min=1, max=8),
            SettingField("denominator_degree_max", "Denominator degree max", "int", 4, min=1, max=8),
            SettingField("coef_min", "Coefficient min", "int", -8, min=-20, max=20),
            SettingField("coef_max", "Coefficient max", "int", 8, min=-20, max=20),
            SettingField("positive_leading_coefficient", "Positive leading coefficients", "bool", True),
            *shared_factoring_settings(),
            SettingField("include_answer_key", "Include answer key", "bool", False),
        ]

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        numerator_degree_min = int(settings.get("numerator_degree_min", 2))
        numerator_degree_max = int(settings.get("numerator_degree_max", 4))
        denominator_degree_min = int(settings.get("denominator_degree_min", 2))
        denominator_degree_max = int(settings.get("denominator_degree_max", 4))
        include_answer_key = bool(settings.get("include_answer_key", False))

        questions: list[Question] = []
        for _ in range(count):
            numerator, denominator, reduced_numerator, reduced_denominator = (
                _create_rational_simplification_problem(
                    settings,
                    numerator_degree_min,
                    numerator_degree_max,
                    denominator_degree_min,
                    denominator_degree_max,
                )
            )

            answer_latex = None
            if include_answer_key:
                answer_latex = polynomial_fraction_latex(reduced_numerator, reduced_denominator)

            questions.append(
                Question(
                    id=str(uuid.uuid4()),
                    topic=self.id,
                    prompt_latex=polynomial_fraction_latex(numerator, denominator),
                    prompt_text=f"({numerator}) / ({denominator})",
                    answer_latex=answer_latex,
                    metadata={
                        "numerator_degree": numerator.deg(),
                        "denominator_degree": denominator.deg(),
                    },
                )
            )

        return questions
